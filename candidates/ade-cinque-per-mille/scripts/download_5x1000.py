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

# URL per anno: lista di 7 URL (uno per parte).
# 2024: pattern guest con data. 2025: pattern Liferay document store.
_YEAR_URLS = {
    2022: [
        "https://www.agenziaentrate.gov.it/portale/documents/d/guest/"
        "5x1000-af-2022-elenco-destinatari-ammessi-al-contributo-{parte}-agg-12-06-2026",
    ],
    2023: [
        "https://www.agenziaentrate.gov.it/portale/documents/d/guest/"
        "5x1000-af-2023-elenco-destinatari-ammessi-al-contributo-{parte}-agg-16-06-2026",
    ],
    2024: [
        "https://www.agenziaentrate.gov.it/portale/documents/d/guest/"
        "5x1000-af2024-elenco-destinatari-ammessi-al-contributo-{parte}-agg-24-06-2025",
    ],
    2025: [
        # P01-P02
        "https://www.agenziaentrate.gov.it/portale/documents/20143/10038477/"
        "5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/"
        "2452a155-9501-dc03-0d5b-6c3efddf202f",
        "https://www.agenziaentrate.gov.it/portale/documents/20143/10038477/"
        "5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/"
        "d1e84ff0-0c1c-548b-3f39-f5a66f269ef4",
        # P03-P04
        "https://www.agenziaentrate.gov.it/portale/documents/20143/10038744/"
        "5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/"
        "63c00ea0-8e31-505c-2ca4-c7d0cf02bedb",
        "https://www.agenziaentrate.gov.it/portale/documents/20143/10038744/"
        "5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/"
        "0da4703a-0a2d-363d-c2f5-53faad87afeb",
        # P05-P07
        "https://www.agenziaentrate.gov.it/portale/documents/20143/10038972/"
        "5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/"
        "0d3b80ca-6d93-c2a5-c79b-720041a1e33b",
        "https://www.agenziaentrate.gov.it/portale/documents/20143/10038972/"
        "5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/"
        "dd781e8a-f882-219c-7583-a0a6a8e0ebde",
        "https://www.agenziaentrate.gov.it/portale/documents/20143/10038972/"
        "5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/"
        "a6d16ce2-1486-ed87-270f-f9dc87b13b12",
    ],
}

NUM_PARTS = 7


def download_part(year: int, parte: int) -> str | None:
    urls = _YEAR_URLS.get(year)
    if not urls:
        print(f"  Nessun URL configurato per anno {year}", file=sys.stderr)
        return None
    # Se c'è un solo URL con {parte}, è un template per tutte le parti
    # Altrimenti usa URL dedicato per parte
    if len(urls) == 1 and "{parte}" in urls[0]:
        url = urls[0].replace("{parte}", str(parte))
    else:
        if parte < 1 or parte > len(urls):
            print(f"  Nessun URL configurato per anno {year} parte {parte}", file=sys.stderr)
            return None
        url = urls[parte - 1]
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
    if year not in _YEAR_URLS:
        print(
            f"ERRORE: anno {year} non configurato. Anni noti: {list(_YEAR_URLS.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Download 5x1000 anno {year} — {len(_YEAR_URLS[year])} parti", file=sys.stderr)

    header: str | None = None
    rows: list[str] = []
    downloaded = 0

    for parte in range(1, NUM_PARTS + 1):
        content = download_part(year, parte)
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

    # Normalizza header: "ETS e ONLUS" → "ETS" (2024 vs 2025)
    header = header.replace("ETS e ONLUS", "ETS")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        f.write("\n".join(rows) + "\n")

    print(f"\n✅ Scritti {len(rows):,} records in {args.output}", file=sys.stderr)
    print(f"   ({downloaded}/{NUM_PARTS} parti scaricate)", file=sys.stderr)


if __name__ == "__main__":
    main()
