#!/usr/bin/env python3
"""Scarica ASIA UL + Addetti dalla fonte ISTAT SDMX (parallelo, rate-limited).

Uso: python preprocess.py {year} {output.csv}

Dataflow: IT1 / 183_1163 (DICA_ASIAULP_TERRIFDATA), dimensioni
  FREQ, REF_AREA, DATA_TYPE, ECON_ACTIVITY_NACE_2007, PERS_EMPL_SIZE_CLASS
Key per sezione ATECO: A..<DATA_TYPE>.<ATECO>.TOTAL

Il mirror DBnomics (usato fino al 2020) non viene più aggiornato: la fonte
ISTAT espone ora la serie fino al 2024. Lo script interroga direttamente
l'SDMX live.

Volume: 2 tipi × 18 sezioni ATECO = 36 richieste. ISTAT limita a ~5 req/min:
un rate limiter condiviso spazia gli avvii, 4 worker scaricano in parallelo.
Le righe vengono scritte man mano (non si tengono in memoria ~1,7M righe).
"""

import csv
import io
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://esploradati.istat.it/SDMXWS/rest/data/IT1,183_1163,1.0"
START_YEAR = 2018
END_YEAR = 2024

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
DATA_TYPES = ["LU", "LUEMPDAA"]

# ~5 req/min condivise tra i worker.
MIN_INTERVAL = 12.0
MAX_WORKERS = 4
MAX_RETRIES = 4
REQUEST_TIMEOUT = 240

_rate_lock = threading.Lock()
_next_start = 0.0


def _throttle() -> None:
    """Spazia gli avvii delle richieste (rate limiter condiviso)."""
    global _next_start
    with _rate_lock:
        now = time.monotonic()
        wait = _next_start - now
        if wait > 0:
            time.sleep(wait)
            now = time.monotonic()
        _next_start = now + MIN_INTERVAL


def _url(data_type: str, ateco: str) -> str:
    key = f"A..{data_type}.{ateco}.TOTAL"
    return f"{BASE}/{key}/?startPeriod={START_YEAR}&endPeriod={END_YEAR}&format=csv"


def _download(url: str) -> bytes:
    req = urllib.request.Request(
        url, headers={"Accept": "text/csv", "User-Agent": "DataCivicLab/1.0"}
    )
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        return resp.read()


def _parse(raw: bytes, data_type: str, ateco: str) -> list[list]:
    text = raw.decode("utf-8")
    if "NoRecordsFound" in text:
        return []
    if not text.lstrip().startswith("DATAFLOW"):
        raise ValueError(f"risposta SDMX inattesa: {text[:120]!r}")

    rows: list[list] = []
    for row in csv.DictReader(io.StringIO(text)):
        ref_area = (row.get("REF_AREA") or "").strip()
        anno = (row.get("TIME_PERIOD") or "").strip()
        obs = (row.get("OBS_VALUE") or "").strip()
        if len(ref_area) != 6 or not ref_area.isdigit():
            continue
        if not anno.isdigit() or not obs:
            continue
        try:
            valore = float(obs)
        except ValueError:
            continue
        rows.append([data_type, ref_area, int(anno), ateco, valore])
    return rows


def fetch_one(data_type: str, ateco: str) -> list[list]:
    url = _url(data_type, ateco)
    for attempt in range(MAX_RETRIES):
        _throttle()
        try:
            raw = _download(url)
            rows = _parse(raw, data_type, ateco)
            print(f"  {data_type}/{ateco}: {len(rows)} righe", flush=True)
            return rows
        except urllib.error.HTTPError as e:
            if e.code == 404:
                body = e.read().decode("utf-8", "replace")
                if "NoRecordsFound" in body:
                    print(f"  {data_type}/{ateco}: nessun dato", flush=True)
                    return []
            last = e
        except Exception as e:  # timeout, connessione, body inatteso
            last = e

        if attempt < MAX_RETRIES - 1:
            wait = 10 * (attempt + 1)
            print(
                f"  {data_type}/{ateco}: {type(last).__name__} — retry tra {wait}s",
                flush=True,
            )
            time.sleep(wait)

    print(f"  {data_type}/{ateco}: FALLITO ({last})", file=sys.stderr, flush=True)
    return []


def main() -> None:
    if len(sys.argv) < 3:
        print("Uso: python preprocess.py <year> <output.csv>", file=sys.stderr)
        sys.exit(1)
    output_path = sys.argv[2]

    tasks = [(dt, a) for dt in DATA_TYPES for a in ATECO]
    print(
        f"Download ASIA UL+EM ({len(tasks)} richieste, {MAX_WORKERS} worker, ~5 req/min)...",
        flush=True,
    )

    write_lock = threading.Lock()
    written = 0

    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["data_type", "ref_area", "anno", "ateco_sezione", "valore"])

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = {pool.submit(fetch_one, dt, a): (dt, a) for dt, a in tasks}
            for future in as_completed(futures):
                rows = future.result()
                if not rows:
                    continue
                with write_lock:
                    writer.writerows(rows)
                    written += len(rows)

    if written == 0:
        print("ERRORE: nessun dato scaricato", file=sys.stderr)
        sys.exit(1)

    print(f"\nFatto: {written} righe scritte in {output_path}", flush=True)


if __name__ == "__main__":
    main()
