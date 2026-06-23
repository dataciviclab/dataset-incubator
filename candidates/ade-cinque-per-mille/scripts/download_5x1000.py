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
# Per anno: numero di parti e singolo URL template con {parte}
# 2023 ha 6 parti, 2024 e 2025 hanno 7 parti.
_ANNI = {
    2023: {
        "parti": 6,
        "url": "https://www.agenziaentrate.gov.it/portale/documents/d/guest/5x1000-af-2023-elenco-destinatari-ammessi-al-contributo-{parte}-agg-16-06-2026",
    },
    2024: {
        "parti": 7,
        "url": "https://www.agenziaentrate.gov.it/portale/documents/d/guest/5x1000-af2024-elenco-destinatari-ammessi-al-contributo-{parte}-agg-24-06-2025",
    },
    2025: {"parti": 7, "url": ""},  # 2025 ha URL dedicati sotto
}
# 2025: URL diversi per ogni parte (Liferay document store)
_2025_URLS = [
    "https://www.agenziaentrate.gov.it/portale/documents/20143/10038477/5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/2452a155-9501-dc03-0d5b-6c3efddf202f",
    "https://www.agenziaentrate.gov.it/portale/documents/20143/10038477/5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/d1e84ff0-0c1c-548b-3f39-f5a66f269ef4",
    "https://www.agenziaentrate.gov.it/portale/documents/20143/10038744/5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/63c00ea0-8e31-505c-2ca4-c7d0cf02bedb",
    "https://www.agenziaentrate.gov.it/portale/documents/20143/10038744/5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/0da4703a-0a2d-363d-c2f5-53faad87afeb",
    "https://www.agenziaentrate.gov.it/portale/documents/20143/10038972/5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/0d3b80ca-6d93-c2a5-c79b-720041a1e33b",
    "https://www.agenziaentrate.gov.it/portale/documents/20143/10038972/5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/dd781e8a-f882-219c-7583-a0a6a8e0ebde",
    "https://www.agenziaentrate.gov.it/portale/documents/20143/10038972/5X1000-AF2025+-+Elenco+destinatari+ammessi+al+contributo+-P{parte}.csv/a6d16ce2-1486-ed87-270f-f9dc87b13b12",
]


def download_part(year: int, parte: int, tot_parti: int) -> str:
    info = _ANNI.get(year)
    if not info:
        raise ValueError(f"Anno {year} non configurato")

    if info["url"]:
        url = info["url"].replace("{parte}", str(parte))
    elif year == 2025:
        if parte < 1 or parte > len(_2025_URLS):
            raise ValueError(f"Anno {year} parte {parte} non configurata")
        url = _2025_URLS[parte - 1].replace("{parte}", str(parte))
    else:
        raise ValueError(f"Anno {year} senza template URL")

    print(f"  Downloading parte {parte}/{tot_parti}...", file=sys.stderr, end=" ")
    # Retry: la fonte ADE può essere fragile in CI
    max_tentativi = 3
    for tentativo in range(1, max_tentativi + 1):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
            # Valida che sia CSV, non PDF
            if data.startswith(b"%PDF"):
                raise ValueError(f"parte {parte} è PDF, non CSV")
            text = data.decode("utf-8")
            print(f"{len(data):,} bytes ✅", file=sys.stderr)
            return text
        except urllib.error.URLError as e:
            if tentativo < max_tentativi:
                print(
                    f"tentativo {tentativo}/{max_tentativi} fallito ({e.reason}), riprovo...",
                    file=sys.stderr,
                )
                import time

                time.sleep(3)
                continue
            raise RuntimeError(
                f"rete: {e.reason} per parte {parte} dopo {max_tentativi} tentativi"
            ) from e
        except urllib.error.HTTPError as e:
            if tentativo < max_tentativi and e.code in (502, 503, 504, 429):
                print(f"HTTP {e.code}, riprovo...", file=sys.stderr)
                import time

                time.sleep(3)
                continue
            raise RuntimeError(f"HTTP {e.code} per parte {parte}") from e
        except UnicodeDecodeError:
            raise RuntimeError(f"parte {parte} non è testo UTF-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download 5x1000 dataset")
    parser.add_argument("--year", type=int, required=True, help="Anno (es. 2024)")
    parser.add_argument("--output", required=True, help="File CSV di output")
    args = parser.parse_args()

    year = args.year
    if year not in _ANNI:
        print(
            f"ERRORE: anno {year} non configurato. Anni noti: {list(_ANNI.keys())}", file=sys.stderr
        )
        sys.exit(1)

    tot_parti = _ANNI[year]["parti"]
    print(f"Download 5x1000 anno {year} — {tot_parti} parti", file=sys.stderr)

    header: str | None = None
    rows: list[str] = []
    falliti: list[int] = []

    for parte in range(1, tot_parti + 1):
        try:
            content = download_part(year, parte, tot_parti)
        except (RuntimeError, ValueError) as e:
            print(f"  ❌ {e}", file=sys.stderr)
            falliti.append(parte)
            continue

        reader = csv.reader(io.StringIO(content), delimiter=";")
        lines = list(reader)
        if not lines:
            falliti.append(parte)
            continue

        if header is None:
            for i, row in enumerate(lines):
                if row and row[0].strip().startswith("Prog"):
                    header = ";".join(row)
                    lines = lines[i + 1 :]
                    break
            else:
                print(f"  ⚠ Header non trovato in parte {parte}", file=sys.stderr)
                falliti.append(parte)
                continue
        else:
            for i, row in enumerate(lines):
                if row and row[0].strip().startswith("Prog"):
                    lines = lines[i + 1 :]
                    break
            else:
                if len(lines) > 3:
                    lines = lines[3:]

        for row in lines:
            if not row or not row[0].strip() or row[0].strip().startswith("Prog"):
                continue
            # Filtra righe non-dato: note legali, righe vuote, ecc.
            # Una riga valida ha un progressivo numerico in colonna 0
            # e un codice fiscale in colonna 1
            if not row[0].strip().isdigit():
                continue
            if len(row) < 2 or not row[1].strip():
                continue
            rows.append(";".join(row))

    if falliti:
        print(f"\n❌ ERRORE: {len(falliti)} parti non scaricate: {falliti}", file=sys.stderr)
        sys.exit(1)

    if not header or not rows:
        print("ERRORE: nessun dato scaricato", file=sys.stderr)
        sys.exit(1)

    # Normalizza header: "ETS e ONLUS" → "ETS" (2024 vs 2025)
    header = header.replace("ETS e ONLUS", "ETS")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        f.write("\n".join(rows) + "\n")

    print(f"\n✅ Scritti {len(rows):,} records in {args.output}", file=sys.stderr)
    print(f"   (tutte le {tot_parti} parti scaricate)", file=sys.stderr)


if __name__ == "__main__":
    main()
