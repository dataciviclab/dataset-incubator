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

# ── Mappa: famiglia di chiave → hub_key in comuni_master + normalizer ────
# Ogni entry ha:
#   hub_column: colonna in comuni_master per il JOIN
#   normalizers: lista di (nome, espressione_sql) da provare
#     L'espressione SQL ha {col} come placeholder per la colonna del dataset

KEY_MAP: dict[str, dict] = {
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
            ("lower + direct", "LOWER({col})"),
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
}


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
    """Esegue la scansione delle chiavi di join per un dataset."""

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
    hub_url = resolve_gcs_url("comuni_master", 2026)

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

    try:
        hub_rel = load_parquet(hub_url, con)
    except Exception as e:
        print(f"❌ Impossibile caricare comuni_master: {e}")
        con.close()
        return

    # Registra come viste DuckDB per poterle referenziare in SQL
    con.register("ds_view_tmp", ds_rel)
    con.register("hub_view_tmp", hub_rel)
    DS_VIEW = "ds_view_tmp"
    HUB_VIEW = "hub_view_tmp"

    ds_columns = get_columns(ds_rel)
    hub_columns = get_columns(hub_rel)

    print(
        f"Colonne dataset ({len(ds_columns)}): {', '.join(ds_columns[:15])}{'...' if len(ds_columns) > 15 else ''}"
    )
    print(f"Hub reference: comuni_master ({len(hub_columns)} colonne)")
    print()

    # Per ogni colonna, trova famiglia e prova join
    results: list[dict] = []

    for col in ds_columns:
        matches = match_column_to_family(col, synonyms)

        for family, synonym in matches:
            if family not in KEY_MAP:
                continue  # famiglia non mappata per JOIN territoriale

            key_info = KEY_MAP[family]
            hub_col = key_info["hub_column"]

            for norm_name, norm_expr in key_info["normalizers"]:
                total, match, no_match = try_join(DS_VIEW, HUB_VIEW, col, hub_col, norm_expr, con)

                if total == 0:
                    continue  # errore SQL o tipo incompatibile

                rate = (match / total * 100) if total > 0 else 0

                results.append(
                    {
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

    con.close()

    # ── Report ─────────────────────────────────────────────────────────
    if not results:
        print("❌ Nessun join candidate trovato per questo dataset.")
        return

    # Ordina per match rate decrescente
    results.sort(key=lambda r: r["rate"], reverse=True)

    # Ordina per match rate decrescente
    matched = [r for r in results if r["match"] > 0]
    failed = [r for r in results if r["match"] == 0]

    if not matched and not failed:
        print("⚠️  Nessun join candidate trovato per questo dataset.")
        return

    # Tabella risultati
    print(
        f"{'Colonna':<32} {'Famiglia':<18} {'Hub key':<14} {'Normalizer':<22} {'Match':>8} {'Su':>8} {'Rate':>8}"
    )
    print("-" * 110)
    for r in matched:
        rate_str = f"{r['rate']:.1f}%"
        print(
            f"{r['colonna']:<32} {r['famiglia']:<18} {r['hub_col']:<14} {r['normalizer']:<22} {r['match']:>8} {r['totale']:>8} {rate_str:>8}"
        )

    # Mostra tentativi falliti (max 5)
    if failed and not matched:
        print("--- Tentativi falliti (match=0) ---")
        for r in failed[:5]:
            print(
                f"  {r['colonna']} → {r['hub_col']} via {r['normalizer']}: {r['match']}/{r['totale']}"
            )

    # Raccomandazione
    if matched:
        print()
        best = matched[0]
        print(
            f"🏆 Miglior chiave: {best['colonna']} → comuni_master.{best['hub_col']} (via {best['normalizer']}: {best['rate']:.1f}%)"
        )
        print(f"   Totale: {best['match']}/{best['totale']} (no-match: {best['no_match']})")

        print()
        print("Suggerimento join_map.yaml:")
        print("  comuni_key:")
        print(f"    column: {best['colonna']}")
        print(f"  hub_key: {best['hub_col']}")
        print(f"  normalizer: ... (scegli in base al normalizer '{best['normalizer']}')")
    else:
        print()
        print("⚠️  Nessuna chiave matcha direttamente con comuni_master.")
        print("   Possibili cause:")
        print("   - Il dataset usa un bridge (es. codice Sogei, codice meccanografico)")
        print("   - La colonna territoriale ha encoding diverso (apostrofi, accenti)")
        print("   - Il dataset ha granularità diversa (provincia/regione/NUTS, non comune)")
        print("   - Servono normalizer non ancora implementati")


def main():
    parser = argparse.ArgumentParser(description="Scopri chiavi di join territoriali di un dataset")
    parser.add_argument("slug", help="Slug del dataset (es. mim_anagrafica_scuole_statali)")
    parser.add_argument("--year", type=int, default=None, help="Anno (default: auto-detect)")
    args = parser.parse_args()

    scan(args.slug, args.year)


if __name__ == "__main__":
    main()
