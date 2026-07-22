#!/usr/bin/env python3
"""
validate_relations.py — Validatore delle relazioni tra dataset.

Legge un file YAML di relazioni (es. relations-appalti.yaml), esegue
le query di verifica su DuckDB, e produce un report con lo stato di
ogni relazione.

Uso:
  python validate_relations.py relations-appalti.yaml
  python validate_relations.py relations-appalti.yaml --verbose

Formato atteso del YAML:
  relations:
    - from: anac_bandi_gara
      via: cig
      to: anac_aggiudicazioni
      cardinality: "1:1"
      ...
"""

import sys
import json
import yaml
import duckdb
from pathlib import Path
from datetime import date

# I dataset clean sono in dataset-incubator/out/data/clean/
# Lo script è in dataset-incubator/registry/ → parents[1] = dataset-incubator/
CLEAN_BASE = Path(__file__).resolve().parents[1] / "out" / "data" / "clean"
CATALOG_PATH = Path(__file__).resolve().parent / "clean_catalog.json"

# Cache del catalogo: {slug: gcs_path}
_CATALOG_CACHE: dict[str, str] | None = None


def _load_catalog() -> dict[str, str]:
    """Carica clean_catalog.json e restituisce {slug: gcs_path}."""
    global _CATALOG_CACHE
    if _CATALOG_CACHE is not None:
        return _CATALOG_CACHE
    _CATALOG_CACHE = {}
    if not CATALOG_PATH.exists():
        return _CATALOG_CACHE
    with open(CATALOG_PATH) as f:
        cat = json.load(f)
    for entry in cat.get("datasets", []):
        slug = entry.get("slug")
        loc = entry.get("location", {})
        path = loc.get("path") if isinstance(loc, dict) else None
        if slug and path:
            _CATALOG_CACHE[slug] = path
    return _CATALOG_CACHE


def resolve_parquet_glob(slug: str) -> str | None:
    """Trova il pattern glob per TUTTI gli anni di un dataset.

    Restituisce un path con * per l'anno, così DuckDB carica tutti gli anni
    insieme. Cerca prima in locale, poi su GCS via catalogo.
    """
    import glob as glob_mod

    # 1. Locale: pattern glob su anni
    local_glob = str(CLEAN_BASE / slug / "*" / f"{slug}_*_clean.parquet")
    files = glob_mod.glob(local_glob)
    if files:
        return local_glob

    # 2. GCS via catalogo
    catalog = _load_catalog()
    gcs_pattern = catalog.get(slug)
    if gcs_pattern:
        return gcs_pattern

    return None


def validate_relation(con: duckdb.DuckDBPyConnection, rel: dict, verbose: bool = False) -> dict:
    """Valida una singola relazione: conta match tra due dataset."""
    from_slug = rel["from"]
    to_slug = rel["to"]
    via = rel["via"]
    as_col = rel.get("as", via)

    # Relazioni con normalizer complesso o bridge non verificabili via JOIN diretto
    normalized_by = rel.get("normalized_by")
    bridge_required = rel.get("bridge_required")
    if bridge_required or (normalized_by and normalized_by != "direct"):
        hint = normalized_by or f"via bridge: {bridge_required}"
        return {
            "rel": f"{from_slug}.{via} → {to_slug}.{as_col}",
            "status": "⏭️",
            "details": f"Normalizer/bridge non applicabile in JOIN diretto: {hint}",
            "match_pct": rel.get("validated_match"),
        }

    from_path = resolve_parquet_glob(from_slug)
    to_path = resolve_parquet_glob(to_slug)

    result = {
        "rel": f"{from_slug}.{via} → {to_slug}.{as_col}",
        "status": "ERROR",
        "details": "",
        "match_pct": None,
        "prev_match": rel.get("validated_match"),
    }

    if not from_path:
        result["status"] = "⏭️"
        result["details"] = f"Parquet non trovato per {from_slug} (solo GCS)"
        return result
    if not to_path:
        result["status"] = "⏭️"
        result["details"] = f"Parquet non trovato per {to_slug} (solo GCS)"
        return result

    try:
        # Per qualsiasi cardinalità (1:1, 1:N, N:1), la metrica è:
        # "quante chiavi sorgente distinte hanno almeno un match sul target"
        query = f"""
            WITH from_keys AS (
                SELECT DISTINCT {via} AS k
                FROM read_parquet('{from_path}')
                WHERE {via} IS NOT NULL
            )
            SELECT
                (SELECT COUNT(*) FROM from_keys) AS tot,
                (SELECT COUNT(*) FROM from_keys WHERE k IN (
                    SELECT DISTINCT {as_col}
                    FROM read_parquet('{to_path}')
                    WHERE {as_col} IS NOT NULL
                )) AS match
        """

        if verbose:
            print(f"  Query: {query[:120]}...")

        row = con.execute(query).fetchone()
        result["tot_from"] = row[0]
        result["match"] = row[1]
        result["match_pct"] = round(100.0 * row[1] / max(row[0], 1), 1) if row[0] else 0.0

        # Status: fallisce solo se match = 0 (relazione completamente assente)
        if result["match_pct"] == 0:
            result["status"] = "❌"
        else:
            result["status"] = "✅"

        result["details"] = (
            f"{result['match']} chiavi su {result['tot_from']} ({result['match_pct']}%)"
        )

    except Exception as e:
        result["status"] = "❌"
        result["details"] = str(e).split("\n")[0]

    return result


def main():
    if len(sys.argv) < 2:
        print("Uso: python validate_relations.py <file.yaml> [--verbose]")
        sys.exit(1)

    yaml_path = Path(sys.argv[1])
    verbose = "--verbose" in sys.argv

    if not yaml_path.exists():
        print(f"❌ File non trovato: {yaml_path}")
        sys.exit(1)

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    relations = data.get("relations", [])
    if not relations:
        print("❌ Nessuna relazione trovata nel file")
        sys.exit(1)

    con = duckdb.connect()

    domain = data.get("domain", "unknown")
    updated = data.get("updated_at", date.today().isoformat())

    print(f"\n{'=' * 60}")
    print(f"  Validazione relazioni — dominio: {domain}")
    print(f"  File: {yaml_path.name}")
    print(f"  Aggiornato: {updated}")
    print(f"  Relazioni da validare: {len(relations)}")
    print(f"{'=' * 60}\n")

    results = []
    ok = err = warn = 0

    for i, rel in enumerate(relations, 1):
        label = f"{rel['from']}.{rel['via']} → {rel['to']}.{rel.get('as', rel['via'])}"
        card = rel.get("cardinality", "?")
        prev = rel.get("validated_match")

        print(f"  [{i}/{len(relations)}] {label}  ({card})")
        if verbose:
            print(f"       Previo: {prev} | Nota: {rel.get('note', '')[:100]}")

        r = validate_relation(con, rel, verbose)
        results.append(r)

        status_icon = r["status"]
        details = r["details"]
        pct = r.get("match_pct")

        if pct is not None:
            prev_str = f" (era {prev * 100:.0f}%)" if prev else ""
            print(f"       {status_icon}  {pct:.1f}% match  {prev_str}")
        print(f"       {details}")

        if r["status"] == "✅":
            ok += 1
        elif r["status"] == "⚠️":
            warn += 1
        elif r["status"] == "❌":
            err += 1
        # ⏭️ skip non conta

        print()

    # Report finale
    print(f"{'=' * 60}")
    print("  REPORT FINALE")
    print(f"{'=' * 60}")
    print(f"  ✅  OK:     {ok}")
    print(f"  ⚠️  WARN:   {warn}")
    print(f"  ❌  ERROR:  {err}")
    print(f"  ⏭️  SKIP:   {len(results) - ok - warn - err}")
    print(f"  {'=' * 60}")

    # Exit non-zero se ci sono errori veri
    if err > 0:
        print(f"\n  ❌ {err} errore(i) — fail")
        sys.exit(1)

    # Mostra range match
    if results:
        pcts = [r.get("match_pct") for r in results if r.get("match_pct") is not None]
        if pcts:
            print(f"\n  Range match: {min(pcts):.1f}% – {max(pcts):.1f}%")

    con.close()


if __name__ == "__main__":
    main()
