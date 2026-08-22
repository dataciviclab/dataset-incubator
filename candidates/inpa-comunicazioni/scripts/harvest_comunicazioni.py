#!/usr/bin/env python3
"""Harvest comunicazioni di procedura dal Portale inPA.

Le comunicazioni sono il ciclo di vita dei concorsi: calendari prove, commissioni,
graduatorie finali, proroghe. Collegate al bando via ``concorsoId``.

Uso:
    python3 harvest_comunicazioni.py <output.csv>
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import time
from pathlib import Path

import requests

API_BASE = "https://portale.inpa.gov.it/concorsi-smart/api"
SEARCH_ENDPOINT = API_BASE + "/communication/user/public-area/search"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (DataCivicLab dataset-incubator)",
    "Accept": "application/json",
}

TAG_RE = re.compile(r"<[^>]+>")


def _clean_html(raw: str | None) -> str | None:
    if raw is None:
        return None
    text = TAG_RE.sub("", raw)
    text = html.unescape(text).strip()
    return text or None


def _flatten(item: dict) -> dict:
    return {
        "id": item.get("id"),
        "concorso_id": item.get("concorsoId"),
        "concorso_title": item.get("concorsoTitle"),
        "subject": item.get("subject"),
        "body": _clean_html(item.get("body")),
        "categoria": item.get("categoryName"),
        "data_pubblicazione": item.get("dateFirstPublish"),
        "ente": item.get("companyName"),
    }


def harvest(size: int, pause: float) -> list[dict]:
    body = {
        "subject": "",
        "concorsoId": None,
        "categoryId": None,
        "publishDateFrom": None,
        "publishDateTo": None,
        "effectiveDateFrom": None,
        "effectiveDateTo": None,
        "companyName": "",
    }
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    first = requests.post(SEARCH_ENDPOINT, params={"page": 0, "size": size}, json=body, timeout=60)
    first.raise_for_status()
    data = first.json()
    total_elements = data.get("totalElements", 0)
    total_pages = data.get("totalPages", 1)
    print(
        f"inPA comunicazioni: totalElements={total_elements} totalPages={total_pages}",
        file=sys.stderr,
    )

    rows = [_flatten(item) for item in data.get("content", [])]
    for page in range(1, total_pages):
        if pause:
            time.sleep(pause)
        r = requests.post(
            SEARCH_ENDPOINT, params={"page": page, "size": size}, json=body, timeout=60
        )
        r.raise_for_status()
        rows.extend(_flatten(item) for item in r.json().get("content", []))

    print(f"inPA comunicazioni: raccolte {len(rows)}", file=sys.stderr)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="path del CSV di output")
    parser.add_argument("--size", type=int, default=100, help="pagine per chiamata (default 100)")
    parser.add_argument("--pause", type=float, default=0.2, help="pausa tra pagine in secondi")
    args = parser.parse_args()

    out_path = Path(args.output)
    rows = harvest(args.size, args.pause)

    if not rows:
        print("inPA comunicazioni: nessuna comunicazione raccolta", file=sys.stderr)
        return 1

    fieldnames = sorted({k for r in rows for k in r})
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"inPA comunicazioni: scritto {out_path} ({len(rows)} righe)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
