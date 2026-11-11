#!/usr/bin/env python3
"""Preprocess: scarica l'XLSX ISPRA (emissioni GHG per settore) e lo converte in CSV.

Il file ISPRA e' un XLSX con due fogli:
- "Dati": riga 0 = header, riga 1 = unita' di misura, righe 2+ = dati (1990-ultimo anno)
- "Metadati": titolo e fonte

L'URL cambia a ogni rilascio (la data di pubblicazione sta nel path): va
aggiornato `RELEASE_URL` quando ISPRA pubblica il nuovo anno.

Uso: python preprocess.py [output_path]
Se output_path non specificato, scrive in stdout.
"""

import csv
import io
import os
import sys

from openpyxl import load_workbook

from lab_connectors.http import download

# Rilascio 2026 (dati 1990-2024), aggiornamento scheda 2026-06-30.
RELEASE_URL = (
    "https://indicatoriambientali.isprambiente.it/sites/default/files/"
    "indicatori_ambientali/2026-06-11/"
    "Tabella%201%20Emissioni_gas_serra_da_processi_energetici_1990_2024_0.xlsx"
)

# Colonne del foglio "Dati" (posizione 0..5). I nomi di output restano quelli
# storici usati da clean/mart, anche se ISPRA ha rinominato la terza colonna
# ("Residenziale e servizi" -> "Terziario e Residenziale + Agricoltura e Pesca").
HEADER = [
    "anno",
    "industrie_energetiche",
    "industrie_manifatturiere",
    "residenziale_e_servizi",
    "trasporti",
    "totale",
]
N_COLS = len(HEADER)
DATA_SHEET = "Dati"
DATA_START_ROW = 2  # 0 = header, 1 = unita' di misura


def _to_float(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def convert_xlsx_to_csv(data: bytes, output) -> int:
    workbook = load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    if DATA_SHEET not in workbook.sheetnames:
        raise ValueError(f"Foglio '{DATA_SHEET}' assente (trovati: {workbook.sheetnames})")
    sheet = workbook[DATA_SHEET]

    writer = csv.writer(output, delimiter=";")
    writer.writerow(HEADER)

    n_rows = 0
    for row in sheet.iter_rows(min_row=DATA_START_ROW + 1, max_col=N_COLS, values_only=True):
        anno = row[0]
        if not isinstance(anno, (int, float)) or isinstance(anno, bool):
            continue
        valori = [_to_float(v) for v in row[1:N_COLS]]
        if all(v is None for v in valori):
            continue
        writer.writerow([int(anno), *valori])
        n_rows += 1
    return n_rows


def main():
    print(f"Downloading XLSX from {RELEASE_URL}...", file=sys.stderr)
    data = download(RELEASE_URL, timeout=60, user_agent="Mozilla/5.0")
    print(f"  Got {len(data)} bytes", file=sys.stderr)

    if len(sys.argv) > 1:
        output_path = sys.argv[1]
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            n_rows = convert_xlsx_to_csv(data, f)
        print(f"CSV written to {output_path} ({n_rows} righe)", file=sys.stderr)
    else:
        n_rows = convert_xlsx_to_csv(data, sys.stdout)
        print(f"{n_rows} righe", file=sys.stderr)


if __name__ == "__main__":
    main()
