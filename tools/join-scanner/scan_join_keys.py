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
# Path ai parquet locali (se già processati)
LOCAL_CLEAN = DI_ROOT / "out" / "data" / "clean"
LOCAL_MART = DI_ROOT / "out" / "data" / "mart"

# ── Hubs: elenco di hub su cui fare scan, in ordine di priorità ────────
# Ogni hub ha:
#   slug: identificativo
#   year: anno di riferimento
#   label: nome leggibile
#   key_map: mappa famiglia di chiave → hub_column + normalizer
#     (stessa struttura del vecchio KEY_MAP)
#   bridge_to_hub: se presente, indica come risalire a comuni_master
# Il path viene risolto da resolve_parquet_path() — prima locale, mai GCS.

HUBS = [
    {
        "slug": "comuni_master",
        "year": 2026,
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
            # Cross-grano NUTS: chiave NUTS3 del dataset → comuni_master.nuts3_2021
            "nuts": {
                "hub_column": "nuts3_2021",
                "normalizers": [
                    ("direct", "{col}"),
                ],
                "cross_grano": True,
                "note": "1 provincia → N comuni. Il dato viene replicato.",
            },
        },
    },
    {
        "slug": "bdap_anagrafe_enti",
        "year": 2026,
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


def resolve_parquet_path(slug: str, year: int) -> str:
    """Cerca il parquet prima in locale, poi su GCS.

    Locale: out/data/clean/{slug}/{year}/{slug}_{year}_clean.parquet
    GCS:    gcs_base/{slug}/{year}/{slug}_{year}_clean.parquet
    """
    local = LOCAL_CLEAN / slug / str(year) / f"{slug}_{year}_clean.parquet"
    if local.exists():
        return str(local)
    # Fallback: prova mart (per support dataset)
    mart = LOCAL_MART / slug / str(year)
    if mart.exists():
        for f in mart.iterdir():
            if f.suffix == ".parquet":
                return str(f)
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

        url = f"{GCS_BASE}/{slug}/{year}/{slug}_{year}_clean.parquet"
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
    "nuts2": "nuts",
    "nuts3": "nuts",
    "nuts_code": "nuts",
    "geo": "nuts",  # Eurostat: colonna geo = codice NUTS
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


def scan(
    slug: str, year: int | None = None, json_output: bool = False, quiet: bool = False
) -> dict | None:
    """Esegue la scansione delle chiavi di join per un dataset su tutti gli hub configurati.

    Restituisce dict con risultati (o None se errore).
    Se json_output=True, stampa solo JSON su stdout.
    Se quiet=True, non stampa output testuale.
    """

    synonyms = load_synonyms()
    catalog = load_catalog()
    catalog_ds = find_dataset_in_catalog(slug, catalog)

    if year is None:
        year = probe_year(slug, catalog_ds)

    if year is None:
        if not quiet and not json_output:
            print(f"❌ Impossibile determinare l'anno per {slug}. Usa --year.")
        return None

    ds_url = f"{GCS_BASE}/{slug}/{year}/{slug}_{year}_clean.parquet"

    if not quiet and not json_output:
        print(f"Dataset: {slug}")
        print(f"Anno:    {year}")
        print()

    con = duckdb.connect()

    try:
        ds_rel = load_parquet(ds_url, con)
    except Exception as e:
        if not quiet and not json_output:
            print(f"  ❌ {e}")
        con.close()
        return None

    ds_columns = get_columns(ds_rel)
    con.register("ds_view_tmp", ds_rel)

    if not quiet and not json_output:
        print(f"  Colonne: {len(ds_columns)}")

    all_results: list[dict] = []

    for hub_info in HUBS:
        hub_slug = hub_info["slug"]
        hub_year = hub_info.get("year", 2026)
        hub_path = resolve_parquet_path(hub_slug, hub_year)
        key_map = hub_info["key_map"]

        if hub_path.startswith("http"):
            continue  # hub non in locale

        try:
            hub_rel = load_parquet(hub_path, con)
        except Exception:
            continue

        con.register("hub_view_tmp", hub_rel)

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
                            "colonna": col,
                            "famiglia": family,
                            "hub_col": hub_col,
                            "normalizer": norm_name,
                            "totale": total,
                            "match": match,
                            "no_match": no_match,
                            "rate": round(rate, 1),
                        }
                    )

    con.close()

    # Best result
    matched = [r for r in all_results if r["match"] > 0]
    best = None
    if matched:
        matched.sort(key=lambda r: r["rate"], reverse=True)
        best = matched[0]

    result = {
        "slug": slug,
        "year": year,
        "rows": len(ds_columns),
        "best": best,
        "all": all_results,
    }

    if json_output:
        # Solo JSON, niente testo
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif not quiet:
        print(f"  Colonne: {len(ds_columns)}")
        if best:
            print(
                f"  ✅ {best['colonna']} → {best['hub_col']} [{best['hub']}] via {best['normalizer']}: {best['rate']:.1f}% ({best['match']}/{best['totale']})"
            )
        else:
            print("  ⚠️  Nessuna chiave trovata")

    return result


def scan_batch(slugs: list[str], json_output: bool = False):
    """Scansiona una lista di slug IN UNA SOLA CONNESSIONE.

    Gli hub (comuni_master, bdap) vengono caricati UNA VOLTA SOLA
    e riusati per tutti i dataset. Molto più veloce.
    """
    synonyms = load_synonyms()

    con = duckdb.connect()

    # Carica hub una volta sola — solo da locale
    hub_views = {}
    for hub_info in HUBS:
        hub_slug = hub_info["slug"]
        hub_year = hub_info.get("year", 2026)
        hub_path = resolve_parquet_path(hub_slug, hub_year)
        view_name = f"hub_{hub_slug}"

        # Verifica che sia locale
        if hub_path.startswith("http"):
            print(f"  ❌ Hub {hub_slug} non disponibile in locale. Buildalo prima con toolkit run.")
            continue

        try:
            hub_rel = load_parquet(hub_path, con)
            con.register(view_name, hub_rel)
            hub_views[hub_slug] = {
                "view": view_name,
                "label": hub_info["label"],
                "key_map": hub_info["key_map"],
                "bridge": hub_info.get("bridge_to_hub"),
            }
        except Exception as e:
            print(f"  ❌ Hub {hub_slug} non caricabile: {e}")

    print()
    results = []

    for slug in slugs:
        # Determina anno dal catalogo o fallback
        catalog = load_catalog()
        catalog_ds = find_dataset_in_catalog(slug, catalog)
        year = probe_year(slug, catalog_ds)

        if year is None:
            print(f"  ⚠️  {slug:<35} anno sconosciuto")
            continue

        # Legge da GCS via DuckDB (HTTP range request, solo colonne serve)
        ds_path = resolve_parquet_path(slug, year)

        try:
            ds_rel = load_parquet(ds_path, con)
        except Exception as e:
            print(f"  ❌  {slug:<35} {e}")
            continue

        ds_columns = get_columns(ds_rel)
        con.register("ds_view", ds_rel)

        all_hub_results = []

        for hub_slug, hub_view in hub_views.items():
            key_map = hub_view["key_map"]

            for col in ds_columns:
                matches = match_column_to_family(col, synonyms)

                for family, synonym in matches:
                    if family not in key_map:
                        continue

                    key_info = key_map[family]
                    hub_col = key_info["hub_column"]

                    for norm_name, norm_expr in key_info["normalizers"]:
                        total, match, no_match = try_join(
                            "ds_view", hub_view["view"], col, hub_col, norm_expr, con
                        )

                        if total == 0:
                            continue

                        rate = (match / total * 100) if total > 0 else 0
                        all_hub_results.append(
                            {
                                "hub": hub_slug,
                                "colonna": col,
                                "famiglia": family,
                                "hub_col": hub_col,
                                "normalizer": norm_name,
                                "totale": total,
                                "match": match,
                                "no_match": no_match,
                                "rate": round(rate, 1),
                            }
                        )

        con.execute("DROP VIEW IF EXISTS ds_view")

        matched = [r for r in all_hub_results if r["match"] > 0]
        best = None
        if matched:
            matched.sort(key=lambda r: r["rate"], reverse=True)
            best = matched[0]

        result = {
            "slug": slug,
            "year": year,
            "best": best,
            "all": all_hub_results,
        }
        results.append(result)

        if best:
            print(
                f"  ✅ {slug:<35} {best['colonna']:<30} → {best['hub_col']:<20} [{best['hub']}] {best['rate']:>5.1f}%"
            )
        else:
            print(f"  ⚠️  {slug:<35} nessuna chiave")

    con.close()

    if json_output:
        print(json.dumps(results, indent=2, ensure_ascii=False))


def _list_catalog_slugs() -> list[str]:
    """Restituisce gli slug dei dataset nel catalogo (con colonne territoriali candidate)."""
    datasets = load_catalog()
    skip = {
        "comuni_master",
        "bdap_anagrafe_enti",
        "istat_elenco_comuni",
        "costituzione_master",
        "opencivitas_glossario",
        "opencivitas_indicatori",
    }
    candidates = []
    for d in datasets:
        slug = d["slug"]
        if slug in skip:
            continue
        cols = [c["name"] for c in d.get("columns", [])]
        col_str = " ".join(cols).lower()
        keywords = [
            "codice_istat",
            "codice_catastale",
            "codice_fiscale",
            "codice_comune",
            "pro_com",
            "cod_comune",
            "codice_ente",
            "id_ente",
            "comune",
            "provincia",
            "regione",
            "sigla_provincia",
            "codice_ipa",
            "cf_soggetto",
            "codice_scuola",
        ]
        if any(k in col_str for k in keywords):
            candidates.append(slug)
    return sorted(candidates)

    # Salta hub e support
    skip = {
        "comuni_master",
        "bdap_anagrafe_enti",
        "istat_elenco_comuni",
        "costituzione_master",
        "opencivitas_glossario",
        "opencivitas_indicatori",
    }

    candidates = []
    for d in datasets:
        slug = d["slug"]
        if slug in skip:
            continue
        cols = [c["name"] for c in d.get("columns", [])]
        col_str = " ".join(cols).lower()

        # Ha almeno una colonna candidate?
        keywords = [
            "codice_istat",
            "codice_catastale",
            "codice_fiscale",
            "codice_comune",
            "pro_com",
            "cod_comune",
            "codice_ente",
            "id_ente",
            "comune",
            "provincia",
            "regione",
            "sigla_provincia",
            "codice_ipa",
            "cf_soggetto",
            "codice_scuola",
        ]
        if any(k in col_str for k in keywords):
            candidates.append(slug)

    return sorted(candidates)


def main():
    parser = argparse.ArgumentParser(description="Scopri chiavi di join territoriali di un dataset")
    parser.add_argument(
        "slug", nargs="?", help="Slug del dataset (es. mim_anagrafica_scuole_statali)"
    )
    parser.add_argument("--year", type=int, default=None, help="Anno (default: auto-detect)")
    parser.add_argument("--json", action="store_true", help="Output JSON invece di testo")
    parser.add_argument("--all", action="store_true", help="Scansiona tutti i dataset del catalogo")
    parser.add_argument("--batch", nargs="*", help="Lista di slug da scansionare")
    args = parser.parse_args()

    if args.all:
        slugs = _list_catalog_slugs()
        print(f"Scanning {len(slugs)} dataset...")
        print(
            "Hub caricati una volta: comuni_master (locale) + bdap_anagrafe_enti (se disponibile)"
        )
        print("Dati letti da GCS via DuckDB (range request, solo colonne serve)")
        print()
        scan_batch(slugs, json_output=args.json)
    elif args.batch is not None:
        scan_batch(args.batch, json_output=args.json)
    elif args.slug:
        scan(args.slug, args.year, json_output=args.json)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
