#!/usr/bin/env python3
"""Preprocess: anac_appalti_master — 8 dataset, anno per anno.

Usage: TOOLKIT_ALLOW_SCRIPT_SOURCE=1 toolkit run raw ...
   or: python preprocess.py <year> <output.parquet>
"""

import sys
import shutil
import duckdb
from pathlib import Path

GCS = "https://storage.googleapis.com/dataciviclab-clean"
BANDI_ANNI = list(range(2016, 2026))


def main():
    output_path = Path(sys.argv[2]).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    con.execute("SET memory_limit = '4GB'")
    con.execute("SET temp_directory = '/tmp/duckdb_tmp'")
    con.execute("SET threads = 2")
    con.execute("SET preserve_insertion_order = false")

    # Materializza tabelle dimensionali (una volta)
    print("Caricamento tabelle dimensionali...", flush=True)

    agg = {}
    for tbl, url, label in [
        (
            "agg",
            f"{GCS}/anac_aggiudicazioni/2026/anac_aggiudicazioni_2026_clean.parquet",
            "aggiudicazioni",
        ),
        (
            "aggte",
            f"{GCS}/anac_aggiudicatari/2026/anac_aggiudicatari_2026_clean.parquet",
            "aggiudicatari",
        ),
        ("coll", f"{GCS}/anac_collaudo/2026/anac_collaudo_2026_clean.parquet", "collaudo"),
        ("cup", f"{GCS}/anac_cup/2026/anac_cup_2026_clean.parquet", "cup"),
    ]:
        con.execute(f"CREATE TEMP TABLE {tbl} AS SELECT * FROM read_parquet('{url}')")
        r = con.execute(f"SELECT count(*) FROM {tbl}").fetchone()
        print(f"  {label}: {r[0]:,}", flush=True)
        agg[tbl] = r[0]

    for tbl, url, sql, label in [
        (
            "part_agg",
            f"{GCS}/anac_partecipanti/2026/anac_partecipanti_2026_clean.parquet",
            "SELECT cig, count(*) AS n, count(DISTINCT codice_fiscale) AS n_imprese FROM read_parquet('{}') WHERE cig IS NOT NULL GROUP BY cig",
            "partecipanti (agg)",
        ),
        (
            "sub_agg",
            f"{GCS}/anac_subappalti/2026/anac_subappalti_2026_clean.parquet",
            "SELECT cig, count(*) AS n, count(DISTINCT codice_fiscale) AS n_sub FROM read_parquet('{}') WHERE cig IS NOT NULL GROUP BY cig",
            "subappalti (agg)",
        ),
        (
            "sal_agg",
            f"{GCS}/anac_stati_avanzamento/2026/anac_stati_avanzamento_2026_clean.parquet",
            "SELECT cig, count(*) AS n_sal, sum(importo_sal) AS tot_sal, avg(n_giorni_scostamento) AS scost FROM read_parquet('{}') WHERE cig IS NOT NULL GROUP BY cig",
            "SAL (agg)",
        ),
    ]:
        con.execute(f"CREATE TEMP TABLE {tbl} AS {sql.format(url)}")
        r = con.execute(f"SELECT count(*) FROM {tbl}").fetchone()
        print(f"  {label}: {r[0]:,} gruppi", flush=True)

    # Crea tabella finale
    con.execute("""
        CREATE TEMP TABLE final (
            cig VARCHAR, anno INT, oggetto_gara VARCHAR,
            importo_complessivo_gara DOUBLE, oggetto_principale VARCHAR,
            stato VARCHAR, esito_bando VARCHAR, flag_pnrr BOOLEAN,
            cod_cpv VARCHAR, descr_cpv VARCHAR,
            amministrazione VARCHAR, provincia VARCHAR, sezione_regionale VARCHAR,
            importo_agg DOUBLE, data_agg DATE, ribasso DOUBLE,
            offerte_ammesse INT, flag_subappalto BOOLEAN, criterio_agg VARCHAR,
            operatore VARCHAR, cf VARCHAR, tipo_soggetto VARCHAR,
            n_partecipanti INT, n_imprese_partecipanti INT,
            n_subappalti INT, n_subappaltatori INT,
            esito_collaudo VARCHAR, data_collaudo DATE,
            riserve_avanzate DOUBLE, contenzioso DOUBLE,
            n_sal INT, importo_totale_sal DOUBLE, scostamento_medio DOUBLE,
            cup VARCHAR
        )
    """)

    # Processa un anno per volta
    print(f"Processo {len(BANDI_ANNI)} anni di bandi...", flush=True)
    for anno in BANDI_ANNI:
        print(f"  {anno}...", end=" ", flush=True)
        con.execute(f"""
            INSERT INTO final
            SELECT b.cig, {anno}, b.oggetto_gara, b.importo_complessivo_gara,
                b.oggetto_principale_contratto, b.stato, b.esito, b.flag_pnrr,
                b.cod_cpv, b.descrizione_cpv,
                b.denominazione_amministrazione_appaltante, b.provincia,
                b.sezione_regionale,
                a.importo_aggiudicazione, a.data_aggiudicazione_definitiva,
                a.ribasso_aggiudicazione, a.numero_offerte_ammesse,
                a.flag_subappalto, a.criterio_aggiudicazione,
                t.denominazione, t.codice_fiscale, t.tipo_soggetto,
                coalesce(p.n, 0), coalesce(p.n_imprese, 0),
                coalesce(s.n, 0), coalesce(s.n_sub, 0),
                col.esito_collaudo, col.data_delibera,
                col.riserve_avanzate, col.importo_contenz_risolto,
                coalesce(sa.n_sal, 0), coalesce(sa.tot_sal, 0), sa.scost,
                cu.cup
            FROM read_parquet('{GCS}/anac_bandi_gara/{anno}/anac_bandi_gara_{anno}_clean.parquet') b
            LEFT JOIN agg a ON b.cig = a.cig
            LEFT JOIN aggte t ON a.id_aggiudicazione = t.id_aggiudicazione
            LEFT JOIN part_agg p ON b.cig = p.cig
            LEFT JOIN sub_agg s ON b.cig = s.cig
            LEFT JOIN coll col ON b.cig = col.cig
            LEFT JOIN sal_agg sa ON b.cig = sa.cig
            LEFT JOIN cup cu ON b.cig = cu.cig
        """)
        r = con.execute("SELECT count(*) FROM final").fetchone()
        print(f"{r[0]:,}", flush=True)

    r = con.execute("SELECT count(*) FROM final").fetchone()
    print(f"\nScrittura {r[0]:,} righe → {output_path}", flush=True)
    con.execute(f"COPY final TO '{output_path}' (FORMAT PARQUET)")

    # Copia in clean (per validazione toolkit)
    clean_dir = output_path.parent.parent.parent / "clean" / output_path.parent.name
    clean_dir.mkdir(parents=True, exist_ok=True)
    clean_file = clean_dir / f"anac_appalti_master_{output_path.parent.name}_clean.parquet"
    shutil.copy2(output_path, clean_file)
    print(f"  Copiato in {clean_file}", flush=True)
    print("✅ Fatto!", flush=True)


if __name__ == "__main__":
    main()
