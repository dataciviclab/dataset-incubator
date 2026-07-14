#!/usr/bin/env python3
"""Scarica immatricolati MUR via CKAN DataStore API.

Usa lab_connectors.http.HttpClient con proxy esplicito
(BLOCKED_SOURCE_PROXY) per funzionare da GHA.
"""

import csv
import os
import sys
from pathlib import Path

from lab_connectors.http import HttpClient


def main():
    if len(sys.argv) < 3:
        print("Uso: python preprocess.py <year> <output.csv>", file=sys.stderr)
        sys.exit(1)

    output_path = Path(sys.argv[2])

    proxy_url = os.environ.get("BLOCKED_SOURCE_PROXY")
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    client = HttpClient(timeout=120, max_retries=2)

    # Scarica CSV via DataStore search (dump non disponibile su MUR CKAN)
    url = (
        "https://dati-ustat.mur.gov.it/api/3/action/datastore_search"
        "?resource_id=9bb0cf6d-1d4e-47f3-8ae9-0c665617b158&limit=5000"
    )
    print(f"Download {url} ...", flush=True)

    if proxies:
        print(f"  con proxy {proxy_url}", flush=True)

    result = client.get(url, proxies=proxies)
    if not result.is_ok or not result.response:
        print(f"ERRORE download: {result.err}", file=sys.stderr)
        sys.exit(1)

    # Scrivi output come CSV
    data = result.response.json()
    records = data.get("result", {}).get("records", [])
    if not records:
        print("ERRORE: nessun record nel risultato", file=sys.stderr)
        sys.exit(1)

    fieldnames = list(records[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(records)

    print(f"Fatto: {len(records)} righe scritte in {output_path}", flush=True)


if __name__ == "__main__":
    main()
