#!/usr/bin/env python3
"""Scarica PNRR_Progetti.csv da Italia Domani (AEM/Akamai).

Akamai fa fingerprinting del client: nessun singolo client funziona ovunque.
- HttpClient di lab-connectors + header browser completi: funziona dal venv
  locale (requests recente), ma può dare 403 da GitHub Actions (IP runner).
- wget con User-Agent breve ("Mozilla/5.0"): funziona anche da CI.
- curl: ultima risorsa.

La catena prova in ordine: HttpClient -> wget -> curl. Il primo che risponde
HTTP 200 vince.

Uso: python preprocess.py <output.csv>
"""

import subprocess
import sys
from pathlib import Path

URL = "https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Progetti.csv"
UA_BROWSER = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
)
UA_SHORT = "Mozilla/5.0"


def _try_httpclient(output: Path) -> bool:
    """Tentativo con HttpClient di lab-connectors + header browser."""
    from lab_connectors.http import HttpClient

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
    }
    client = HttpClient(timeout=300, max_retries=1, user_agent=UA_BROWSER)
    result = client.get(URL, headers=headers)
    if result.response is not None and result.response.status_code == 200:
        content = result.response.content
        if content[:2] == b"\x1f\x8b":
            import gzip

            content = gzip.decompress(content)
        output.write_bytes(content)
        print(f"HttpClient: ok ({len(content)} bytes)")
        return True
    return False


def _try_wget(output: Path) -> bool:
    """Tentativo con wget + UA breve (funziona anche da CI)."""
    try:
        subprocess.run(
            ["wget", "-q", "--user-agent=" + UA_SHORT, "-O", str(output), URL],
            check=True,
            timeout=500,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    if output.exists() and output.stat().st_size > 0:
        print(f"wget: ok ({output.stat().st_size} bytes)")
        return True
    return False


def _try_curl(output: Path) -> bool:
    """Tentativo con curl + UA breve."""
    try:
        subprocess.run(
            ["curl", "-sS", "-A", UA_SHORT, "-o", str(output), URL],
            check=True,
            timeout=500,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    if output.exists() and output.stat().st_size > 0:
        print(f"curl: ok ({output.stat().st_size} bytes)")
        return True
    return False


def main() -> None:
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv")
    if _try_httpclient(output):
        return
    print("HttpClient fallito (403 o errore) — fallback wget")
    if _try_wget(output):
        return
    print("wget fallito — fallback curl")
    if _try_curl(output):
        return
    raise RuntimeError(f"Download fallito per {URL} (tutti i client)")


if __name__ == "__main__":
    main()
