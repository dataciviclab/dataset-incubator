#!/usr/bin/env python3
"""Preprocess: scarica XLS ISPRA emissioni GHG e lo converte in CSV.

Lo script:
1. Scarica il file XLS dall'URL
2. Legge Sheet 0 (D03_027)
3. Salta riga 1 (sub-header con unità di misura)
4. Produce CSV pulito con header normalizzati

Uso: python preprocess.py [output_path]
Se output_path non specificato, scrive in stdout.
"""

import sys
import os
import csv
import requests
import xlrd

URL = "https://indicatoriambientali.isprambiente.it/sites/default/files/indicatori_ambientali/2025-07-01/Tabella%201%20Emissioni_gas_serra_da_processi_energetici%20%286%29.xls"

HEADER = [
    "anno",
    "industrie_energetiche",
    "industrie_manifatturiere",
    "residenziale_e_servizi",
    "trasporti",
    "totale",
]


def download_xls(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, timeout=30, headers=headers, verify=False)
    r.raise_for_status()
    return r.content


def convert_xls_to_csv(data, output):
    workbook = xlrd.open_workbook(file_contents=data)
    sheet = workbook.sheet_by_index(0)  # Sheet 0 = D03_027

    writer = csv.writer(output, delimiter=";")
    writer.writerow(HEADER)

    # Row 0 = header, Row 1 = sub-header (unità di misura), Row 2+ = dati
    for r_idx in range(2, sheet.nrows):
        row = [sheet.cell(r_idx, c_idx).value for c_idx in range(sheet.ncols)]
        writer.writerow(row)


def main():
    print(f"Downloading XLS from {URL}...", file=sys.stderr)
    data = download_xls(URL)
    print(f"  Got {len(data)} bytes", file=sys.stderr)

    if len(sys.argv) > 1:
        output_path = sys.argv[1]
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            convert_xls_to_csv(data, f)
        print(f"CSV written to {output_path}", file=sys.stderr)
    else:
        convert_xls_to_csv(data, sys.stdout)


if __name__ == "__main__":
    main()
