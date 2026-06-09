#!/usr/bin/env python3
"""Scarica i dati SITUAS via opensituas e produce il CSV raw per la pipeline.

Prerequisiti:
    pip install opensituas

Uso:
    python scripts/download_data.py

Genera: raw/istat_elenco_comuni_raw.csv
"""

import csv
import subprocess
import sys
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "raw"
REPORTS = {"61": "codici", "74": "superficie", "73": "caratteristiche"}


def _fetch_report(pfun: str) -> list[dict]:
    """Chiama opensituas e restituisce le righe del report come lista di dict."""
    result = subprocess.run(
        ["opensituas", "-o", "csv", "get", pfun],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        print(f"ERROR: opensituas get {pfun} fallito:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    reader = csv.DictReader(result.stdout.splitlines())
    return list(reader)


def main():
    print("Download report SITUAS via opensituas...")

    # Scarica i tre report
    data = {}
    for pfun, name in REPORTS.items():
        print(f"  Report {pfun} ({name})...")
        data[pfun] = _fetch_report(pfun)

    # Indice per PRO_COM_T
    idx = {pfun: {r["PRO_COM_T"]: r for r in rows} for pfun, rows in data.items()}

    # Colonne output
    columns = [
        "codice_istat",
        "denominazione",
        "codice_catastale",
        "regione",
        "provincia",
        "sigla_provincia",
        "superficie_km2",
        "popolazione_residente",
        "popolazione_legale",
        "zona_altimetrica",
        "altitudine",
        "comune_litoraneo",
        "comune_isolano",
    ]

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RAW_DIR / "istat_elenco_comuni_raw.csv"

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)

        for pro_com_t, r61 in idx["61"].items():
            r74 = idx["74"].get(pro_com_t, {})
            r73 = idx["73"].get(pro_com_t, {})

            area_raw = r74.get("AREA_KMQ", "").replace(",", ".")
            writer.writerow(
                [
                    pro_com_t,
                    r61.get("COMUNE_IT", ""),
                    r61.get("COD_CATASTO", ""),
                    r61.get("DEN_REG", ""),
                    r61.get("DEN_UTS", ""),
                    r61.get("SIGLA_AUTOMOBILISTICA", ""),
                    area_raw,
                    r74.get("POP_RES", ""),
                    r74.get("POP_LEG", ""),
                    r73.get("ZONA_ALT", ""),
                    r73.get("ALT", ""),
                    r73.get("COM_LIT", ""),
                    r73.get("COM_ISO", ""),
                ]
            )

    count = len(idx["61"])
    print(f"\nFatto: {out_path} ({count} comuni)")


if __name__ == "__main__":
    main()
