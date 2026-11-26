#!/usr/bin/env python3
"""Scarica lo snapshot mensile degli oneri pensionistici DAG (MEF).

Stessa fonte e stesso protocollo di ``pensioni-pa-dag``, ma il file
``Dati_Amministrazione_YYYYMM.csv`` (categoria ``oneri``) espone il costo per
Ministero, capitolo di bilancio e RTS invece dello stock per tipo.

Uso:
    python scripts/download_dag_oneri.py --year 2025 --output dag_oneri_2025.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lab_connectors.http import HttpClient

URL = "https://datipensioni.mef.gov.it/datipensioni/downloadFile"
DATASET = "DOWNLOAD_RDF_MESE_ANNO_ONERI"


def download(year: int, month: int, output: Path) -> None:
    month_s = f"{month:02d}"
    filename = f"Dati_Amministrazione_{year}{month_s}.csv"
    payload = {
        "categoria": "oneri",
        "filename": filename,
        "dataset": DATASET,
        "mese": month_s,
        "anno": str(year),
    }

    client = HttpClient(timeout=120, max_retries=2)
    result = client.post(URL, data=payload, retries=2)
    if not result.is_ok or result.response is None:
        raise SystemExit(f"download fallito per {filename}: {result.err or 'no response'}")

    response = result.response
    if response.status_code != 200:
        raise SystemExit(f"HTTP {response.status_code} per {filename}")

    content = response.content
    head = content.lstrip()[:2048]
    if head[:1] == b"<" or b"NOME FILE NON CONSENTITO" in head:
        raise SystemExit(f"la fonte ha restituito HTML invece del CSV ({filename})")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content)
    print(f"scritto {output} ({len(content)} bytes)", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scarica lo snapshot mensile oneri DAG")
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", type=int, default=12)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    download(args.year, args.month, Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
