#!/usr/bin/env python3
"""Scarica e concatena le 7 parti del dataset 5x1000 dell'Agenzia delle Entrate.

Uso:
    python scripts/download_5x1000.py --year 2024 --output raw_input.csv

Ogni anno ha 7 file CSV (partizioni per iniziale/categoria).
L'URL segue il pattern:
    https://www.agenziaentrate.gov.it/portale/documents/d/guest/
    5x1000-af{year}-elenco-destinatari-ammessi-al-contributo-{parte}-...
"""

import argparse
import csv
import io
import sys
import urllib.request
import urllib.error

# URL di esempio verificato per il 2024:
#   .../5x1000-af2024-elenco-destinatari-ammessi-al-contributo-1-agg-24-06-2025
#
# Mappa: per ogni anno, la data di aggiornamento (parte finale dell'URL).
# La data è l'ultimo aggiornamento del dataset quell'anno.
_UPDATE_DATES = {
    2024: "24-06-2025",
    # 2025: da verificare — aggiungere dopo aver trovato l'URL reale
}

NUM_PARTS = 7

BASE_URL = (
    "https://www.agenziaentrate.gov.it/portale/documents/d/guest/"
    "5x1000-af{year}-elenco-destinatari-ammessi-al-contributo-{parte}-agg-{date}"
)


def download_part(year: int, parte: int, date: str) -> str | None:
    url = BASE_URL.format(year=year, parte=parte, date=date)
    print(f"  Downloading parte {parte}/7...", file=sys.stderr, end=" ")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        print(f"{len(data):,} bytes", file=sys.stderr)
        return data.decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr)
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Download 5x1000 dataset")
    parser.add_argument("--year", type=int, required=True, help="Anno (es. 2024)")
    parser.add_argument("--output", required=True, help="File CSV di output")
    args = parser.parse_args()

    year = args.year
    date = _UPDATE_DATES.get(year)
    if not date:
        print(f"ERRORE: anno {year} non configurato. Date note: {_UPDATE_DATES}", file=sys.stderr)
        sys.exit(1)

    print(f"Download 5x1000 anno {year} — {NUM_PARTS} parti", file=sys.stderr)

    header: str | None = None
    rows: list[str] = []
    downloaded = 0

    for parte in range(1, NUM_PARTS + 1):
        content = download_part(year, parte, date)
        if content is None:
            print(f"  ⚠ Parte {parte} non scaricata, continuo...", file=sys.stderr)
            continue

        # Legge le righe CSV
        reader = csv.reader(io.StringIO(content), delimiter=";")
        lines = list(reader)

        if not lines:
            continue

        # La prima parte ha header + 3 righe di intestazione
        # Salta le prime 3 righe (descrizione) e usa la quarta come header
        if header is None:
            # Trova l'header: riga che inizia con "Prog;"
            for i, row in enumerate(lines):
                if row and row[0].strip().startswith("Prog"):
                    header = ";".join(row)
                    lines = lines[i + 1 :]  # righe dopo l'header
                    break
            else:
                print(f"  ⚠ Header non trovato in parte {parte}", file=sys.stderr)
                continue
        else:
            # Parti successive: cerca l'header e salta
            for i, row in enumerate(lines):
                if row and row[0].strip().startswith("Prog"):
                    lines = lines[i + 1 :]
                    break
            else:
                # Se non trova header, salta le prime 3 (descrizione) e usa tutto
                if len(lines) > 3:
                    lines = lines[3:]

        for row in lines:
            if row and row[0].strip() and not row[0].strip().startswith("Prog"):
                rows.append(";".join(row))

        downloaded += 1

    if not header or not rows:
        print("ERRORE: nessun dato scaricato", file=sys.stderr)
        sys.exit(1)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        f.write("\n".join(rows) + "\n")

    print(f"\n✅ Scritti {len(rows):,} records in {args.output}", file=sys.stderr)
    print(f"   ({downloaded}/{NUM_PARTS} parti scaricate)", file=sys.stderr)


if __name__ == "__main__":
    main()
