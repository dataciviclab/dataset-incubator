#!/usr/bin/env python3
"""Valida gli output di ``pensioni_pa_dag``.

Controlli per ogni anno:
- identita' del totale: regioni + Italia + Estero = totale;
- nessun duplicato sulla chiave naturale, nessun nullo/negativo;
- copertura stabile: 22 territori e 95 uffici;
- il mart somma al totale del clean e ha una riga per (anno, regione, tipo).

Uso (dopo un run, dalla root del repo):
    python candidates/pensioni-pa-dag/scripts/check_dag.py
    python candidates/pensioni-pa-dag/scripts/check_dag.py --data-dir out/data

Exit 0 se tutto torna, 1 se almeno un controllo fallisce. Se non ci sono
output del candidate (run di altri dataset), esce 0.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

KEY = (
    "anno, mese, regione, sigla_provincia, ufficio, tipo_pensione, "
    "codice_pensione, descrizione_microqualifica, codice_microqualifica, codice_titolo"
)
EXPECTED_TERRITORIES = 22
EXPECTED_OFFICES = 95


def _q(path: Path) -> str:
    """Path per read_parquet: single quote escaped."""
    return str(path).replace("'", "''")


def check_year(con: duckdb.DuckDBPyConnection, year: str, clean: Path, mart: Path) -> list[str]:
    errors: list[str] = []
    c = _q(clean)

    total, regioni, italia, estero = con.execute(
        f"""select sum(numero_partite),
                   sum(case when regione not in ('Italia','Estero') then numero_partite else 0 end),
                   sum(case when regione = 'Italia' then numero_partite else 0 end),
                   sum(case when regione = 'Estero' then numero_partite else 0 end)
            from read_parquet('{c}')"""
    ).fetchone()
    if total is None:
        return [f"{year}: clean senza righe"]
    if regioni + italia + estero != total:
        errors.append(f"{year}: identita' totale rotta: {regioni}+{italia}+{estero} != {total}")

    dup = con.execute(
        f"select count(*) from (select {KEY}, count(*) n from read_parquet('{c}') "
        f"group by all having n > 1)"
    ).fetchone()[0]
    if dup:
        errors.append(f"{year}: {dup} chiavi duplicate")

    nulls, negativi = con.execute(
        f"""select sum(case when numero_partite is null or importi_mensili_pagati_eur is null
                              or regione is null or ufficio is null then 1 else 0 end),
                   sum(case when numero_partite < 0 or importi_mensili_pagati_eur < 0 then 1 else 0 end)
            from read_parquet('{c}')"""
    ).fetchone()
    if nulls:
        errors.append(f"{year}: {nulls} righe con nulli su chiave/misura")
    if negativi:
        errors.append(f"{year}: {negativi} righe con valori negativi")

    territori, uffici = con.execute(
        f"select count(distinct regione), count(distinct ufficio) from read_parquet('{c}')"
    ).fetchone()
    if territori != EXPECTED_TERRITORIES:
        errors.append(f"{year}: {territori} territori (attesi {EXPECTED_TERRITORIES})")
    if uffici != EXPECTED_OFFICES:
        errors.append(f"{year}: {uffici} uffici (attesi {EXPECTED_OFFICES})")

    if not mart.exists():
        errors.append(f"{year}: mart mancante ({mart})")
        return errors

    m = _q(mart)
    total_mart, righe_mart = con.execute(
        f"select sum(numero_partite), count(*) from read_parquet('{m}')"
    ).fetchone()
    if total_mart != total:
        errors.append(f"{year}: mart {total_mart} != clean {total}")

    combinazioni = con.execute(
        f"select count(*) from (select distinct regione, tipo_pensione from read_parquet('{c}'))"
    ).fetchone()[0]
    if righe_mart != combinazioni:
        errors.append(f"{year}: mart {righe_mart} righe, attese {combinazioni}")

    print(
        f"{year}: clean {total} partite, {territori} territori, {uffici} uffici | "
        f"mart {total_mart} partite, {righe_mart} righe"
    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida output pensioni_pa_dag")
    parser.add_argument("--data-dir", default="out/data")
    args = parser.parse_args()

    root = Path(args.data_dir)
    clean_dir = root / "clean" / "pensioni_pa_dag"
    mart_dir = root / "mart" / "pensioni_pa_dag"
    clean_files = sorted(clean_dir.glob("*/pensioni_pa_dag_*_clean.parquet"))
    if not clean_files:
        print("pensioni_pa_dag: nessun output clean, salto")
        return 0

    con = duckdb.connect()
    errors: list[str] = []
    for clean in clean_files:
        year = clean.parent.name
        mart = mart_dir / year / "mart_territori_dicembre.parquet"
        errors.extend(check_year(con, year, clean, mart))

    if errors:
        print("\nValidazione FALLITA:", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 1
    print("\nValidazione OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
