#!/usr/bin/env python3
"""
Unisce i 4 sheet del file Indicatori_Penali.xlsx in un unico CSV.

Sheet:
- Tribunali
- Corti d'Appello
- Giudici di Pace
- Tribunale per i Minorenni

Tutti hanno lo stesso schema: Anno, Tipo ufficio, Distretto, Sede, Sezione,
Clearance rate, Disposition time.

Output: CSV con header e colonne standardizzate.
"""

import pandas as pd
import sys
from pathlib import Path

SHEETS = [
    "Tribunali",
    "Corti d'Appello",
    "Giudici di Pace",
    "Tribunale per i Minorenni",
]

INPUT = Path("raw_input.xlsx")  # fornito dal toolkit
OUTPUT = Path("raw_input.csv")


def main():
    if not INPUT.exists():
        print(f"ERRORE: {INPUT} non trovato", file=sys.stderr)
        sys.exit(1)

    frames = []
    for sheet in SHEETS:
        try:
            df = pd.read_excel(INPUT, sheet_name=sheet)
            # Tipizza colonne per uniformità tra sheet
            if "Anno" in df.columns:
                df["Anno"] = pd.to_numeric(df["Anno"], errors="coerce")
            df["Tipo ufficio"] = sheet
            frames.append(df)
            print(f"  OK  {sheet}: {len(df)} righe")
        except Exception as e:
            print(f"  ERR {sheet}: {e}", file=sys.stderr)

    if not frames:
        print("ERRORE: nessuno sheet letto", file=sys.stderr)
        sys.exit(1)

    united = pd.concat(frames, ignore_index=True)
    # Filtra righe senza Anno
    before = len(united)
    united = united.dropna(subset=["Anno"])
    print(f"  Filtrate {before - len(united)} righe senza Anno")

    united.to_csv(OUTPUT, index=False)
    print(f"\nOutput: {OUTPUT} ({len(united)} righe, {len(united.columns)} colonne)")


if __name__ == "__main__":
    main()
