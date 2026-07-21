#!/usr/bin/env python3
"""
Unisce i 4 sheet del file Indicatori_Penali.xlsx in un unico CSV.

Scarica il file XLSX dal portale del Ministero della Giustizia usando
lab_connectors.http.download (retry, SSL fallback, circuit breaker),
legge i 4 sheet (Tribunali, Corti d'Appello, Giudici di Pace, Minorenni)
e produce un CSV con schema unificato.

Sheet schema comune:
  Anno, Tipo ufficio, Distretto, Sede, Sezione, Clearance rate, Disposition time

Usage:
  python unite_sheets_penali.py [--url URL] [--output OUTPUT]
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
from lab_connectors.http import download as http_download

SHEETS = [
    "Tribunali",
    "Corti d'Appello",
    "Giudici di Pace",
    "Tribunale per i Minorenni",
]

COLUMNS_STANDARD = [
    "Anno",
    "Tipo ufficio",
    "Distretto",
    "Sede",
    "Sezione",
    "Clearance rate",
    "Disposition time",
]

DEFAULT_URL = (
    "https://datiestatistiche.giustizia.it/"
    "cmsresources/cms/documents/Indicatori_Penali.xlsx"
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--output", default="raw_input.csv")
    args = parser.parse_args()

    xlsx_path = Path("raw_input.xlsx")
    output_path = Path(args.output)

    # Scarica il file XLSX via lab_connectors (retry + SSL fallback automatici)
    print(f"Download {args.url} ...")
    data = http_download(args.url)
    xlsx_path.write_bytes(data)
    print(f"  OK ({len(data)} bytes)")

    # Leggi e unisci i 4 sheet
    frames = []
    for sheet in SHEETS:
        try:
            df = pd.read_excel(xlsx_path, sheet_name=sheet)
            print(
                f"  LETTO {sheet}: {len(df)} righe × {len(df.columns)} "
                f"colonne → {list(df.columns)}"
            )
            cols_presenti = [c for c in COLUMNS_STANDARD if c in df.columns]
            df = df[cols_presenti]
            if "Tipo ufficio" not in df.columns or df["Tipo ufficio"].isna().all():
                df["Tipo ufficio"] = sheet
            if "Anno" in df.columns:
                df["Anno"] = pd.to_numeric(df["Anno"], errors="coerce")
            frames.append(df)
            print(f"  OK  {sheet}: {len(df)} righe, {len(df.columns)} colonne")
        except Exception as e:
            print(f"  ERR {sheet}: {e}", file=sys.stderr)

    if not frames:
        print("ERRORE: nessuno sheet letto", file=sys.stderr)
        sys.exit(1)

    united = pd.concat(frames, ignore_index=True)
    before = len(united)
    united = united.dropna(subset=["Anno"])
    print(f"  Filtrate {before - len(united)} righe senza Anno")

    united.to_csv(output_path, index=False)
    print(f"\nOutput: {output_path} ({len(united)} righe, {len(united.columns)} colonne)")
    print(f"Colonne: {list(united.columns)}")
    tipo_uffici = sorted(united["Tipo ufficio"].dropna().unique())
    print(f"Tipo ufficio distinti: {tipo_uffici}")

    xlsx_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
