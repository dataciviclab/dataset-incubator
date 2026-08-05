#!/usr/bin/env python3
"""Scarica PNRR_Gare.csv da Italia Domani (AEM/Akamai).

Akamai fa HTTP fingerprinting: blocca (403) i client HTTP con headers
incompleti e versioni vecchie di requests/urllib3. Serve il set di header
browser completo e un ambiente Python aggiornato (il venv del workspace).

Questo script va eseguito nel venv del workspace (come tutti gli script Lab).
Se gira in un ambiente senza lab_connectors, fallisce subito con un errore
chiaro: attivare il venv (source .venv/bin/activate).
"""

import sys

from lab_connectors.http import HttpClient

URL = "https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Gare.csv"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
)
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
}


def main() -> None:
    output = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
    client = HttpClient(timeout=300, max_retries=2, user_agent=UA)
    result = client.get(URL, headers=HEADERS)
    if result.response is None or result.response.status_code != 200:
        status = (
            result.response.status_code
            if result.response is not None
            else f"no response (is_ok={result.is_ok})"
        )
        raise RuntimeError(f"Download fallito per {URL}: HTTP {status}")
    with open(output, "wb") as fh:
        fh.write(result.response.content)
    print(f"Downloaded {len(result.response.content)} bytes -> {output}")


if __name__ == "__main__":
    main()
