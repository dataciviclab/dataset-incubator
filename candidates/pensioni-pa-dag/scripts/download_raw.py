"""
DEPRECATED — il toolkit ora supporta http_post_file (toolkit#242).

Il candidate usa direttamente ``type: http_post_file`` in dataset.yml.
Questo script resta come riferimento storico per il pattern cookie
GET -> POST se l'endpoint dovesse richiederlo in futuro.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import requests


DEFAULT_URL = "https://datipensioni.mef.gov.it/datipensioni/downloadFile"
DEFAULT_PAGE_URL = "https://datipensioni.mef.gov.it/datipensioni/download"
DEFAULT_FILENAME = "Dati_Tipo_Pensione_totale.csv"
DEFAULT_CATEGORY = "pensioni"


def download_raw(
    output_path: Path,
    *,
    url: str = DEFAULT_URL,
    page_url: str = DEFAULT_PAGE_URL,
    filename: str = DEFAULT_FILENAME,
    category: str = DEFAULT_CATEGORY,
    timeout: int = 120,
    retries: int = 3,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    headers = {"User-Agent": "dataciviclab-dag-downloader/0.1"}

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = session.post(
                url,
                data={"filename": filename, "categoria": category},
                headers=headers,
                timeout=timeout,
            )
            if response.status_code == 200 and response.content:
                output_path.write_bytes(response.content)
                return output_path

            session.get(page_url, headers=headers, timeout=timeout)
            response = session.post(
                url,
                data={"filename": filename, "categoria": category},
                headers=headers,
                timeout=timeout,
            )
            response.raise_for_status()
            output_path.write_bytes(response.content)
            return output_path
        except Exception as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(5 * attempt, 15))

    raise RuntimeError(f"Download DAG fallito dopo {retries} tentativi: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scarica il CSV cumulativo pensioni DAG in inputs/.")
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parents[1] / "inputs" / DEFAULT_FILENAME),
        help="Path di output del CSV raw.",
    )
    parser.add_argument("--timeout", type=int, default=120, help="Timeout HTTP in secondi.")
    parser.add_argument("--retries", type=int, default=3, help="Numero di tentativi in caso di risposta instabile.")
    args = parser.parse_args()

    out = download_raw(Path(args.output), timeout=args.timeout, retries=args.retries)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
