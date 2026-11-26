#!/usr/bin/env python3
"""Valida gli output di ``oneri_pensioni_pa``.

Controlli per ogni anno:
- nessun duplicato sulla chiave naturale, nessun nullo/negativo;
- `Importi TOTALE` >= arretrati + ratei + tredicesima (il totale non e' la
  somma dei tre componenti: e' un totale pubblicato dalla fonte);
- 95 RTS (uffici territoriali);
- i mart sommano al clean e hanno una riga per gruppo;
- cross-check con ``pensioni_pa_dag``: stesse partite (stesso stock DAG).

Uso (dopo un run, dalla root del repo):
    python candidates/oneri-pensioni-pa/scripts/check_oneri.py
    python candidates/oneri-pensioni-pa/scripts/check_oneri.py --data-dir out/data

Exit 0 se tutto torna, 1 se almeno un controllo fallisce. Se non ci sono
output del candidate, esce 0.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

KEY = "anno, mese, ministero, capitolo_bilancio, piano_gestione, rts"
EXPECTED_RTS = 95


def _q(path: Path) -> str:
    return str(path).replace("'", "''")


def check_year(
    con: duckdb.DuckDBPyConnection,
    year: str,
    clean: Path,
    mart_min: Path,
    mart_rts: Path,
    pensioni_clean: Path | None,
) -> list[str]:
    errors: list[str] = []
    c = _q(clean)

    total_partite, total_importi = con.execute(
        f"select sum(numero_partite), sum(importi_totale_eur) from read_parquet('{c}')"
    ).fetchone()
    if total_partite is None:
        return [f"{year}: clean senza righe"]

    dup = con.execute(
        f"select count(*) from (select {KEY}, count(*) n from read_parquet('{c}') "
        f"group by all having n > 1)"
    ).fetchone()[0]
    if dup:
        errors.append(f"{year}: {dup} chiavi duplicate")

    nulls, negativi = con.execute(
        f"""select sum(case when numero_partite is null or importi_totale_eur is null
                              or ministero is null or rts is null then 1 else 0 end),
                   sum(case when numero_partite < 0 or importi_totale_eur < 0 then 1 else 0 end)
            from read_parquet('{c}')"""
    ).fetchone()
    if nulls:
        errors.append(f"{year}: {nulls} righe con nulli su chiave/misura")
    if negativi:
        errors.append(f"{year}: {negativi} righe con valori negativi")

    sotto = con.execute(
        f"""select count(*) from read_parquet('{c}')
            where importi_totale_eur < importi_arretrati_eur + importi_ratei_eur + importi_tredicesima_eur"""
    ).fetchone()[0]
    if sotto:
        errors.append(f"{year}: {sotto} righe con totale < somma dei componenti")

    rts = con.execute(f"select count(distinct rts) from read_parquet('{c}')").fetchone()[0]
    if rts != EXPECTED_RTS:
        errors.append(f"{year}: {rts} RTS (attese {EXPECTED_RTS})")

    for mart, label in ((mart_min, "per_ministero"), (mart_rts, "per_rts")):
        if not mart.exists():
            errors.append(f"{year}: mart {label} mancante ({mart})")
            continue
        m = _q(mart)
        somma = con.execute(f"select sum(importi_totale_eur) from read_parquet('{m}')").fetchone()[
            0
        ]
        if somma is None or abs(somma - total_importi) > 0.01:
            errors.append(f"{year}: mart {label} {somma} != clean {total_importi}")

    combinazioni_min = con.execute(
        f"select count(*) from (select distinct ministero from read_parquet('{c}'))"
    ).fetchone()[0]
    combinazioni_rts = con.execute(
        f"select count(*) from (select distinct rts, descrizione_rts from read_parquet('{c}'))"
    ).fetchone()[0]
    righe_min = (
        con.execute(f"select count(*) from read_parquet('{_q(mart_min)}')").fetchone()[0]
        if mart_min.exists()
        else -1
    )
    righe_rts = (
        con.execute(f"select count(*) from read_parquet('{_q(mart_rts)}')").fetchone()[0]
        if mart_rts.exists()
        else -1
    )
    if righe_min != combinazioni_min:
        errors.append(f"{year}: mart per_ministero {righe_min} righe, attese {combinazioni_min}")
    if righe_rts != combinazioni_rts:
        errors.append(f"{year}: mart per_rts {righe_rts} righe, attese {combinazioni_rts}")

    cross = "saltato"
    if pensioni_clean is not None and pensioni_clean.exists():
        p = con.execute(
            f"select sum(numero_partite) from read_parquet('{_q(pensioni_clean)}')"
        ).fetchone()[0]
        diff = total_partite - p
        if diff == 0:
            cross = f"OK ({p} partite)"
        elif year == "2017" and diff == 10:
            # I due file 2017-12 hanno una revisione diversa: R1 +9, CT +1.
            # Dal 2018 i totali coincidono esattamente.
            cross = f"DIFF {diff:+d} (2017: revisione fonte, R1/CT)"
        else:
            errors.append(f"{year}: partite oneri {total_partite} != pensioni {p}")

    print(
        f"{year}: {total_partite} partite, {total_importi:.2f} EUR, {rts} RTS | "
        f"mart min {righe_min}, rts {righe_rts} | cross pensioni: {cross}"
    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida output oneri_pensioni_pa")
    parser.add_argument("--data-dir", default="out/data")
    args = parser.parse_args()

    root = Path(args.data_dir)
    clean_dir = root / "clean" / "oneri_pensioni_pa"
    mart_dir = root / "mart" / "oneri_pensioni_pa"
    pensioni_dir = root / "clean" / "pensioni_pa_dag"
    clean_files = sorted(clean_dir.glob("*/oneri_pensioni_pa_*_clean.parquet"))
    if not clean_files:
        print("oneri_pensioni_pa: nessun output clean, salto")
        return 0

    con = duckdb.connect()
    errors: list[str] = []
    for clean in clean_files:
        year = clean.parent.name
        pensioni_files = sorted(pensioni_dir.glob(f"{year}/*.parquet"))
        errors.extend(
            check_year(
                con,
                year,
                clean,
                mart_dir / year / "mart_oneri_per_ministero.parquet",
                mart_dir / year / "mart_oneri_per_rts.parquet",
                pensioni_files[0] if pensioni_files else None,
            )
        )

    if errors:
        print("\nValidazione FALLITA:", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 1
    print("\nValidazione OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
