#!/usr/bin/env python3
"""Scarica Unità Locali ASIA da DBnomics API (parallelo).

Uso: python preprocess.py {year} {output.csv}

Dataset: ISTAT/183_1163_DF_DICA_ASIAULP_TERRIFDATA_3
Dati a livello comunale, anni 2018-2020.
"""

import csv
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

DATASET = "ISTAT/183_1163_DF_DICA_ASIAULP_TERRIFDATA_3"
PAGE_SIZE = 1000

ATECO = [
    "0010",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
]

DATA_TYPE = "LU"
SIZE_CLASS = "TOTAL"
FREQ = "A"


def api_request(data_type: str, ateco: str, offset: int = 0) -> dict:
    dims = json.dumps(
        {
            "FREQ": [FREQ],
            "PERS_EMPL_SIZE_CLASS": [SIZE_CLASS],
            "DATA_TYPE": [data_type],
            "ECON_ACTIVITY_NACE_2007": [ateco],
        }
    )
    params = urllib.parse.urlencode(
        {
            "dimensions": dims,
            "observations": "1",
            "limit": str(PAGE_SIZE),
            "offset": str(offset),
        }
    )
    url = f"https://api.db.nomics.world/v22/series/{DATASET}?{params}"
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req, timeout=120)
    return json.loads(resp.read())


def fetch_ateco(ateco: str) -> list[list]:
    """Scarica tutte le pagine per un singolo ATECO, restituisce righe."""
    rows = []
    try:
        resp = api_request(DATA_TYPE, ateco, 0)
    except Exception as e:
        print(f"  {ateco}: ERR {e}", flush=True)
        return rows

    num_found = resp["series"]["num_found"]
    if num_found == 0:
        return rows

    print(f"  {ateco}: {num_found} series", flush=True)
    offset = 0
    while offset < num_found:
        if offset > 0:
            try:
                resp = api_request(DATA_TYPE, ateco, offset)
            except Exception as e:
                print(f"    {ateco} offset={offset}: ERR {e}", flush=True)
                break
        docs = resp["series"].get("docs", [])
        for d in docs:
            dims_info = d.get("dimensions", {})
            ref_area = dims_info.get("REF_AREA", "")
            period_list = d.get("period", [])
            value_list = d.get("value", [])
            for p, v in zip(period_list, value_list):
                if v is not None:
                    rows.append([ref_area, int(p), ateco, float(v)])
        if len(docs) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
    return rows


def main():
    if len(sys.argv) < 3:
        print("Uso: python preprocess.py <year> <output.csv>", file=sys.stderr)
        sys.exit(1)
    output_path = sys.argv[2]

    all_rows = []
    print("Download ASIA UL (parallelo)...", flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        futuri = {pool.submit(fetch_ateco, a): a for a in ATECO}
        for f in as_completed(futuri):
            all_rows.extend(f.result())

    if not all_rows:
        print("ERRORE: nessun dato scaricato", flush=True)
        sys.exit(1)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ref_area", "anno", "ateco_sezione", "valore"])
        w.writerows(all_rows)

    print(f"\nFatto: {len(all_rows)} righe scritte in {output_path}", flush=True)


if __name__ == "__main__":
    main()
