#!/usr/bin/env python3
"""
join-scanner — Scopre automaticamente le chiavi di join territoriali di un dataset.

Per ogni colonna del dataset, prova a matchare con ogni chiave di comuni_master
usando vari normalizer (direct, LPAD, RIGHT, UPPER+TRIM, REPLACE brackets, ...)
e riporta il match rate.

Uso::

    python tools/join-scanner/scan_join_keys.py <slug> [--year N]

Esempio::

    python tools/join-scanner/scan_join_keys.py mim_anagrafica_scuole_statali
    python tools/join-scanner/scan_join_keys.py mef_partecipazioni --year 2023
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb

# ── Paths ─────────────────────────────────────────────────────────────────
DI_ROOT = Path(__file__).resolve().parents[2]
SYNONYMS_PATH = DI_ROOT / "registry" / "_key_synonyms.py"
CATALOG_PATH = DI_ROOT / "registry" / "clean_catalog.json"

GCS_BASE = "https://storage.googleapis.com/dataciviclab-clean"

# ── Hubs: elenco di hub su cui fare scan, in ordine di priorità ────────
# Ogni hub ha:
#   slug: identificativo
#   url: GCS URL del clean parquet (year = 2026 per i registry)
#   label: nome leggibile
#   key_map: mappa famiglia di chiave → hub_column + normalizer
#     (stessa struttura del vecchio KEY_MAP)

HUBS = [
    {
        "slug": "comuni_master",
        "url": f"{GCS_BASE}/comuni_master/2026/comuni_master_2026_clean.parquet",
        "label": "comuni_master (hub comuni)",
        "key_map": {
            "codice_istat": {
                "hub_column": "codice_istat",
                "normalizers": [
                    ("direct", "{col}"),
                    ("LPAD(6)", "LPAD(CAST({col} AS VARCHAR), 6, '0')"),
                    ("RIGHT(6)", "RIGHT({col}, 6)"),
                ],
            },
            "codice_catastale": {
                "hub_column": "codice_catastale",
                "normalizers": [
                    ("direct", "{col}"),
                    ("UPPER TRIM", "UPPER(TRIM({col}))"),
                ],
            },
            "codice_fiscale": {
                "hub_column": "codice_fiscale",
                "normalizers": [
                    ("direct", "{col}"),
                    ("REPLACE brackets", "REPLACE(REPLACE({col}, '[', ''), ']', '')"),
                ],
            },
            "codice_ipa": {
                "hub_column": "codice_ipa",
                "normalizers": [
                    ("direct", "{col}"),
                    ("LOWER", "LOWER({col})"),
                ],
            },
            "comune_nome": {
                "hub_column": "denominazione",
                "normalizers": [
                    ("UPPER TRIM", "UPPER(TRIM({col}))"),
                    (
                        "UPPER TRIM + apostrofo→accento",
                        'REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(UPPER(TRIM({col})), "U\'", chr(217)), "O\'", chr(210)), "I\'", chr(204)), "E\'", chr(200)), "A\'", chr(192))',
                    ),
                ],
            },
            "partita_iva": {
                "hub_column": "codice_fiscale",
                "normalizers": [
                    ("direct", "{col}"),
                    ("REPLACE brackets", "REPLACE(REPLACE({col}, '[', ''), ']', '')"),
                ],
            },
            "regione": {
                "hub_column": "regione",
                "normalizers": [
                    ("UPPER TRIM", "UPPER(TRIM({col}))"),
                ],
            },
            "provincia": {
                "hub_column": "sigla_provincia",
                "normalizers": [
                    ("UPPER TRIM", "UPPER(TRIM({col}))"),
                ],
            },
        },
    },
    {
        "slug": "bdap_anagrafe_enti",
        "url": f"{GCS_BASE}/bdap_anagrafe_enti/2026/bdap_anagrafe_enti_2026_clean.parquet",
        "label": "bdap_anagrafe_enti (bridge enti → comune)",
        "key_map": {
            "id_ente": {
                "hub_column": "id_ente",
                "normalizers": [
                    ("direct (INT)", "{col}"),
                    ("cast VARCHAR", "CAST({col} AS VARCHAR)"),
                ],
            },
            "codice_ente_siope": {
                "hub_column": "codice_ente_siope",
                "normalizers": [
                    ("direct", "{col}"),
                ],
            },
            "codice_ente_ipa": {
                "hub_column": "codice_ente_ipa",
                "normalizers": [
                    ("direct", "{col}"),
                ],
            },
            "codice_ente_miur": {
                "hub_column": "codice_ente_miur",
                "normalizers": [
                    ("direct", "{col}"),
                ],
            },
            "codice_ente_ssn": {
                "hub_column": "codice_ente_ssn",
                "normalizers": [
                    ("direct", "{col}"),
                ],
            },
            "cf": {
                "hub_column": "cf",
                "normalizers": [
                    ("direct", "{col}"),
                    ("REPLACE brackets", "REPLACE(REPLACE({col}, '[', ''), ']', '')"),
                ],
            },
            "piva": {
                "hub_column": "piva",
                "normalizers": [
                    ("direct", "{col}"),
                ],
            },
        },
        # Dopo il match su BDAP, risale al comune via codice_istat_comune
        "bridge_to_hub": {
            "hub_slug": "comuni_master",
            "via": "codice_istat_comune",
        },
    },
]


def load_synonyms() -> dict[str, list[str]]:
    """Carica KEY_SYNONYMS da _key_synonyms.py."""
    ns: dict = {}
    exec(SYNONYMS_PATH.read_text(), ns)
    return ns.get("KEY_SYNONYMS", {})


def load_catalog() -> list[dict]:
    """Carica clean_catalog.json, restituisce lista dataset."""
    data = json.loads(CATALOG_PATH.read_text())
    return data.get("datasets", data if isinstance(data, list) else [])


def find_dataset_in_catalog(slug: str, catalog: list[dict]) -> dict | None:
    for ds in catalog:
        if ds.get("slug") == slug:
            return ds
    return None


def resolve_gcs_url(slug: str, year: int) -> str:
    """Costruisce URL GCS per il clean parquet."""
    return f"{GCS_BASE}/{slug}/{year}/{slug}_{year}_clean.parquet"


def probe_year(slug: str, catalog_ds: dict | None) -> int | None:
    """Trova un anno per cui il parquet esiste su GCS."""
    # Prima prova dal catalogo
    if catalog_ds:
        period = catalog_ds.get("period", {})
        end = period.get("end")
        if end:
            return int(end)
        years = catalog_ds.get("years", [])
        if years:
            return int(max(years)) if isinstance(years, list) else int(years)
    # Fallback: prova anni recenti
    for year in [2025, 2024, 2023, 2026]:
        import urllib.request

        url = resolve_gcs_url(slug, year)
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    return year
        except Exception:
            continue
    return None


def load_parquet(url: str, con: duckdb.DuckDBConnection | None = None) -> duckdb.DuckDBPyRelation:
    """Carica un parquet da URL via DuckDB. Se specificata una connessione, usa quella."""
    if con:
        return con.read_parquet(url)
    return duckdb.read_parquet(url)


def get_columns(rel: duckdb.DuckDBPyRelation) -> list[str]:
    """Restituisce i nomi delle colonne di una relazione."""
    return [desc[0] for desc in rel.description]


# ── Keyword → famiglia per fallback ────────────────────────────────────
# Se il match esatto fallisce, prova per keyword nella colonna
KEYWORD_FALLBACK: dict[str, str] = {
    "fiscale": "partita_iva",
    "cf_": "partita_iva",
    "codice_fiscale": "partita_iva",
    "istat": "codice_istat",
    "catastale": "codice_catastale",
    "belfiore": "codice_catastale",
    "comune": "comune_nome",
    "denominazione": "comune_nome",
    "ipa": "codice_ipa",
    "provincia": "provincia",
    "prov": "provincia",
    "regione": "regione",
    "nuts": "nuts",
    # chiavi ente BDAP
    "ente_bdap": "id_ente",
    "id_ente": "id_ente",
    "codice_ente": "codice_ente_siope",  # SIOPE
    "ente_siope": "codice_ente_siope",
    "ente_miur": "codice_ente_miur",
    "ente_ssn": "codice_ente_ssn",
    "piva": "piva",
}


def match_column_to_family(col_name: str, synonyms: dict[str, list[str]]) -> list[tuple[str, str]]:
    """
    Data una colonna, trova le famiglie di chiave a cui potrebbe appartenere.
    Prima prova match esatto con i sinonimi, poi fallback per keyword.
    Restituisce lista di (family_name, matched_synonym_o_keyword).
    """
    col_lower = col_name.lower()
    matches = []

    # Passo 1: match esatto con sinonimi
    for family, aliases in synonyms.items():
        for alias in aliases:
            if alias.lower() == col_lower:
                matches.append((family, alias))
                break

    # Passo 2: se non c'è match esatto, prova per keyword
    if not matches:
        for keyword, family in KEYWORD_FALLBACK.items():
            if keyword in col_lower:
                matches.append((family, f"keyword:{keyword}"))
                break  # una sola famiglia per colonna in fallback

    return matches


def try_join(
    ds_view: str,
    hub_view: str,
    ds_col: str,
    hub_col: str,
    normalizer_sql: str,
    con: duckdb.DuckDBConnection,
) -> tuple[int, int, int]:
    """
    Prova un JOIN tra dataset_col (con normalizer) e hub_col.
    `ds_view` e `hub_view` sono nomi di viste temporanee registrate in con.
    Restituisce (totale, match, no_match).
    """
    ds_expr = normalizer_sql.replace("{col}", f"d.{ds_col}")
    sql = f"""
    SELECT
        COUNT(*) AS totale,
        COUNT(h.{hub_col}) AS match,
        COUNT(*) - COUNT(h.{hub_col}) AS no_match
    FROM {ds_view} d
    LEFT JOIN {hub_view} h ON {ds_expr} = h.{hub_col}
    """
    try:
        result = con.execute(sql).fetchone()
        return int(result[0]), int(result[1]), int(result[2])
    except Exception:
        # Errore SQL (tipo incompatibile, colonna inesistente, ecc.)
        return 0, 0, 0


def scan(slug: str, year: int | None = None) -> None:
    """Esegue la scansione delle chiavi di join per un dataset su tutti gli hub configurati."""

    synonyms = load_synonyms()
    catalog = load_catalog()
    catalog_ds = find_dataset_in_catalog(slug, catalog)

    if year is None:
        year = probe_year(slug, catalog_ds)

    if year is None:
        print(f"❌ Impossibile determinare l'anno per {slug}. Usa --year.")
        return

    # Carica dataset
    ds_url = resolve_gcs_url(slug, year)

    print(f"Dataset: {slug}")
    print(f"Anno:    {year}")
    print(f"URL:     {ds_url}")
    print()

    con = duckdb.connect()

    try:
        ds_rel = load_parquet(ds_url, con)
    except Exception as e:
        print(f"❌ Impossibile caricare {ds_url}: {e}")
        con.close()
        return

    ds_columns = get_columns(ds_rel)
    con.register("ds_view_tmp", ds_rel)

    print(
        f"Colonne dataset ({len(ds_columns)}): {', '.join(ds_columns[:15])}{'...' if len(ds_columns) > 15 else ''}"
    )
    print()

    # Scan su ogni hub
    all_results: list[dict] = []

    for hub_info in HUBS:
        hub_slug = hub_info["slug"]
        hub_url = hub_info["url"]
        hub_label = hub_info["label"]
        key_map = hub_info["key_map"]

        print(f"── Scan su {hub_label} ──")

        try:
            hub_rel = load_parquet(hub_url, con)
        except Exception as e:
            print(f"  ❌ Impossibile caricare {hub_url}: {e}")
            continue

        con.register("hub_view_tmp", hub_rel)
        hub_columns = get_columns(hub_rel)
        print(f"  Hub: {len(hub_columns)} colonne")

        for col in ds_columns:
            matches = match_column_to_family(col, synonyms)

            for family, synonym in matches:
                if family not in key_map:
                    continue

                key_info = key_map[family]
                hub_col = key_info["hub_column"]

                for norm_name, norm_expr in key_info["normalizers"]:
                    total, match, no_match = try_join(
                        "ds_view_tmp", "hub_view_tmp", col, hub_col, norm_expr, con
                    )

                    if total == 0:
                        continue

                    rate = (match / total * 100) if total > 0 else 0

                    all_results.append(
                        {
                            "hub": hub_slug,
                            "hub_label": hub_label,
                            "colonna": col,
                            "famiglia": family,
                            "synonym": synonym,
                            "hub_col": hub_col,
                            "normalizer": norm_name,
                            "totale": total,
                            "match": match,
                            "no_match": no_match,
                            "rate": rate,
                        }
                    )

        hub_matched = [r for r in all_results if r["hub"] == hub_slug and r["match"] > 0]
        if hub_matched:
            print(f"  ✅ {len(hub_matched)} combinazioni con match > 0")
        else:
            print("  ⚠️  Nessun match su questo hub")
        print()

    con.close()

    # ── Report ─────────────────────────────────────────────────────────
    if not all_results:
        print("❌ Nessun join candidate trovato per questo dataset.")
        return

    # Tabella risultati
    matched = [r for r in all_results if r["match"] > 0]
    failed = [r for r in all_results if r["match"] == 0]

    print(
        f"{'Hub':<28} {'Colonna':<32} {'Famiglia':<18} {'Hub key':<14} {'Normalizer':<22} {'Match':>8} {'Su':>8} {'Rate':>8}"
    )
    print("-" * 140)
    for r in matched:
        rate_str = f"{r['rate']:.1f}%"
        print(
            f"{r['hub_label']:<28} {r['colonna']:<32} {r['famiglia']:<18} {r['hub_col']:<14} {r['normalizer']:<22} {r['match']:>8} {r['totale']:>8} {rate_str:>8}"
        )

    if failed and not matched:
        print("--- Tentativi falliti (match=0) ---")
        for r in failed[:5]:
            print(
                f"  {r['hub_label']}: {r['colonna']} → {r['hub_col']} via {r['normalizer']}: {r['match']}/{r['totale']}"
            )

    # Raccomandazione
    if matched:
        matched.sort(key=lambda r: r["rate"], reverse=True)
        best = matched[0]
        print()
        print(
            f"🏆 Miglior chiave: [{best['hub_label']}] {best['colonna']} → {best['hub_col']} (via {best['normalizer']}: {best['rate']:.1f}%)"
        )
        print(f"   Totale: {best['match']}/{best['totale']} (no-match: {best['no_match']})")

        bridge_note = ""
        for hub_info in HUBS:
            if hub_info["slug"] == best["hub"] and hub_info.get("bridge_to_hub"):
                bt = hub_info["bridge_to_hub"]
                bridge_note = f" → risale a {bt['hub_slug']} via {bt['via']}"

        print()
        print("Suggerimento join_map.yaml:")
        print(f"  hub: {best['hub']}{bridge_note}")
        print("  comuni_key:")
        print(f"    column: {best['colonna']}")
        print(f"  hub_key: {best['hub_col']}")
        print(f"  normalizer: ... (scegli in base al normalizer '{best['normalizer']}')")
    else:
        print()
        print("⚠️  Nessuna chiave matcha con gli hub configurati.")
        print("   Possibili cause:")
        print("   - Il dataset usa un bridge esterno (es. Sogei, codice meccanografico)")
        print("   - Encoding diverso (apostrofi, accenti) non coperto dai normalizer")
        print("   - Granularità diversa (provincia/regione/NUTS, non comune/ente)")
        print("   - Servono normalizer o hub aggiuntivi")


def main():
    parser = argparse.ArgumentParser(description="Scopri chiavi di join territoriali di un dataset")
    parser.add_argument("slug", help="Slug del dataset (es. mim_anagrafica_scuole_statali)")
    parser.add_argument("--year", type=int, default=None, help="Anno (default: auto-detect)")
    args = parser.parse_args()

    scan(args.slug, args.year)


if __name__ == "__main__":
    main()
