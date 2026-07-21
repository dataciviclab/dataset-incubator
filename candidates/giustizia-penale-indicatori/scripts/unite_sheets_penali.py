#!/usr/bin/env python3
"""
Unisce i 4 sheet del file Indicatori_Penali.xlsx in un unico CSV.

Sheet:
- Tribunali        (7 colonne)
- Corti d'Appello  (7 colonne)
- Giudici di Pace  (9 colonne — ultime 2 vuote, da scartare)
- Tribunale per i Minorenni (7 colonne)

Tutti hanno schema comune: Anno, Tipo ufficio, Distretto, Sede, Sezione,
Clearance rate, Disposition time.

Output: CSV con header standardizzato e colonne pulite.
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

COLUMNS_STANDARD = [
    "Anno",
    "Tipo ufficio",
    "Distretto",
    "Sede",
    "Sezione",
    "Clearance rate",
    "Disposition time",
]

INPUT = Path("raw_input.xlsx")
OUTPUT = Path("raw_input.csv")


def main():
    if not INPUT.exists():
        print(f"ERRORE: {INPUT} non trovato", file=sys.stderr)
        sys.exit(1)

    frames = []
    for sheet in SHEETS:
        try:
            df = pd.read_excel(INPUT, sheet_name=sheet)
            print(
                f"  LETTO {sheet}: {len(df)} righe × {len(df.columns)} colonne → {list(df.columns)}"
            )
            # Seleziona solo le colonne standard (scarta extra vuote)
            cols_presenti = [c for c in COLUMNS_STANDARD if c in df.columns]
            df = df[cols_presenti]
            # Forza Tipo ufficio dal nome sheet (alcuni sheet non lo hanno popolato)
            if "Tipo ufficio" not in df.columns or df["Tipo ufficio"].isna().all():
                df["Tipo ufficio"] = sheet
            # Tipizza Anno
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

    united.to_csv(OUTPUT, index=False)
    print(f"\nOutput: {OUTPUT} ({len(united)} righe, {len(united.columns)} colonne)")
    print(f"Colonne: {list(united.columns)}")
    print(f"Tipo ufficio distinti: {sorted(united['Tipo ufficio'].dropna().unique())}")


if __name__ == "__main__":
    main()
