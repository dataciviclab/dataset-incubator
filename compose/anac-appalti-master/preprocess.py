#!/usr/bin/env python3
"""Preprocess: anac_appalti_master — 8 dataset, anno per anno.

Grana: 1 riga per CIG. Aggiudicatari, collaudo e cup aggregati a livello CIG.
"""

import sys
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

    print("Caricamento tabelle dimensionali...", flush=True)

    # Aggiudicazioni: aggrega a 1 riga per CIG (ci sono ~13K CIG con più righe)
    con.execute(f"""
        CREATE TEMP TABLE agg AS
        SELECT cig,
            any_value(importo_aggiudicazione) AS importo_aggiudicazione,
            any_value(data_aggiudicazione_definitiva) AS data_aggiudicazione_definitiva,
            any_value(ribasso_aggiudicazione) AS ribasso_aggiudicazione,
            any_value(numero_offerte_ammesse) AS numero_offerte_ammesse,
            any_value(flag_subappalto) AS flag_subappalto,
            any_value(criterio_aggiudicazione) AS criterio_aggiudicazione,
            any_value(asta_elettronica) AS asta_elettronica,
            any_value(id_aggiudicazione) AS id_aggiudicazione,
            count(*) AS n_righe_agg
        FROM read_parquet('{GCS}/anac_aggiudicazioni/2026/anac_aggiudicazioni_2026_clean.parquet')
        WHERE cig IS NOT NULL
        GROUP BY cig
    """)
    r = con.execute("SELECT count(*) FROM agg").fetchone()
    print(f"  aggiudicazioni (agg): {r[0]:,} gruppi", flush=True)

    # Collaudo: aggrega a 1 riga per CIG (188 CIG con più righe)
    con.execute(f"""
        CREATE TEMP TABLE coll AS
        SELECT cig,
            any_value(esito_collaudo) AS esito_collaudo,
            any_value(data_delibera) AS data_delibera,
            any_value(riserve_avanzate) AS riserve_avanzate,
            any_value(importo_contenz_risolto) AS importo_contenz_risolto
        FROM read_parquet('{GCS}/anac_collaudo/2026/anac_collaudo_2026_clean.parquet')
        WHERE cig IS NOT NULL
        GROUP BY cig
    """)
    r = con.execute("SELECT count(*) FROM coll").fetchone()
    print(f"  collaudo (agg): {r[0]:,} gruppi", flush=True)

    # Aggiudicatari: aggrega a 1 riga per CIG (un CIG può avere più operatori ATI/RTI)
    con.execute(f"""
        CREATE TEMP TABLE aggte_agg AS
        SELECT cig,
            any_value(denominazione) AS operatore,
            any_value(codice_fiscale) AS cf,
            any_value(tipo_soggetto) AS tipo_soggetto,
            count(*) AS n_operatori
        FROM read_parquet('{GCS}/anac_aggiudicatari/2026/anac_aggiudicatari_2026_clean.parquet')
        WHERE cig IS NOT NULL
        GROUP BY cig
    """)
    r = con.execute("SELECT count(*) FROM aggte_agg").fetchone()
    print(f"  aggiudicatari (agg): {r[0]:,} gruppi", flush=True)

    # CUP: aggrega a 1 riga per CIG
    con.execute(f"""
        CREATE TEMP TABLE cup_agg AS
        SELECT cig, any_value(cup) AS cup
        FROM read_parquet('{GCS}/anac_cup/2026/anac_cup_2026_clean.parquet')
        WHERE cig IS NOT NULL
        GROUP BY cig
    """)
    r = con.execute("SELECT count(*) FROM cup_agg").fetchone()
    print(f"  cup (agg): {r[0]:,} gruppi", flush=True)

    # Tabelle aggregate (già pronte)
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

    # Crea tabella finale (1 riga per CIG)
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
            n_operatori INT,
            n_partecipanti INT, n_imprese_partecipanti INT,
            n_subappalti INT, n_subappaltatori INT,
            esito_collaudo VARCHAR, data_collaudo DATE,
            riserve_avanzate DOUBLE, contenzioso DOUBLE,
            n_sal INT, importo_totale_sal DOUBLE, scostamento_medio DOUBLE,
            cup VARCHAR
        )
    """)

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
                t.operatore, t.cf, t.tipo_soggetto,
                coalesce(t.n_operatori, 0) AS n_operatori,
                coalesce(p.n, 0), coalesce(p.n_imprese, 0),
                coalesce(s.n, 0), coalesce(s.n_sub, 0),
                col.esito_collaudo, col.data_delibera,
                col.riserve_avanzate, col.importo_contenz_risolto,
                coalesce(sa.n_sal, 0), coalesce(sa.tot_sal, 0), sa.scost,
                cu.cup
            FROM (
                SELECT * FROM read_parquet('{GCS}/anac_bandi_gara/{anno}/anac_bandi_gara_{anno}_clean.parquet')
                QUALIFY ROW_NUMBER() OVER (PARTITION BY cig ORDER BY importo_lotto DESC) = 1
            ) b
            LEFT JOIN agg a ON b.cig = a.cig
            LEFT JOIN aggte_agg t ON b.cig = t.cig
            LEFT JOIN part_agg p ON b.cig = p.cig
            LEFT JOIN sub_agg s ON b.cig = s.cig
            LEFT JOIN coll col ON b.cig = col.cig
            LEFT JOIN sal_agg sa ON b.cig = sa.cig
            LEFT JOIN cup_agg cu ON b.cig = cu.cig
        """)
        r = con.execute("SELECT count(*) FROM final").fetchone()
        print(f"{r[0]:,}", flush=True)

    r = con.execute("SELECT count(*) FROM final").fetchone()
    print(f"\nScrittura {r[0]:,} righe → {output_path}", flush=True)
    con.execute(f"COPY final TO '{output_path}' (FORMAT PARQUET)")
    print("✅ Fatto!", flush=True)


if __name__ == "__main__":
    main()
