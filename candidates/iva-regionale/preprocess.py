#!/usr/bin/env python3
"""Scarica e normalizza il CSV IVA dal MEF per anno."""

import sys
import urllib.request
import csv
import io

year = sys.argv[1] if len(sys.argv) > 1 else "2024"
output = sys.argv[2] if len(sys.argv) > 2 else "raw_input.csv"

url = f"https://www1.finanze.gov.it/finanze/analisi_stat/public/index.php?tree={year}CIVATOT0201&export=3"

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=60) as resp:
    content = resp.read().decode("utf-8")

reader = csv.reader(io.StringIO(content), delimiter=";")
rows = list(reader)

# Trova header
header_idx = None
for i, row in enumerate(rows):
    if row and row[0].strip() == "Regione":
        header_idx = i
        break
if header_idx is None:
    header_idx = 7

header = rows[header_idx]
# Colonna numeriche (Ammontare, Media, Frequenza, Numero)
num_cols = {
    j
    for j, col in enumerate(header)
    if any(k in col for k in ["Ammontare", "Media", "Frequenza", "Numero"])
}


def normalize(val):
    val = val.strip()
    if not val or val == "***":
        return ""
    # Rimuovi punti migliaia, sostituisci virgola decimale
    if "," in val:
        val = val.replace(".", "").replace(",", ".")
    else:
        val = val.replace(".", "")
    return val


with open(output, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(header)
    for row in rows[header_idx + 1 :]:
        if not row or not row[0].strip():
            continue
        cleaned = [normalize(v) if j in num_cols else v.strip() for j, v in enumerate(row)]
        writer.writerow(cleaned)

print(f"Fatto: anno={year} righe={len(rows) - header_idx - 1}")
