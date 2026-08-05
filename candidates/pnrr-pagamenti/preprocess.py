#!/usr/bin/env python3
"""Scarica PNRR_Gare.csv da Italia Domani (AEM/Akamai).

Akamai blocca gli IP di GitHub Actions (403) sia diretto che via fallback
automatico. Il pattern validato nel Lab (mur-immatricolati) è: HttpClient
di lab-connectors con **proxy esplicito** da BLOCKED_SOURCE_PROXY.

Catena: HttpClient (diretto) -> HttpClient (proxy esplicito) -> wget (proxy)
-> curl (proxy). Ogni tentativo verifica che il contenuto NON sia HTML
(pagina di errore).

Uso: python preprocess.py <output.csv>
"""

import os
import subprocess
import sys
from pathlib import Path

URL = "https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Pagamenti_di_Progetto.csv"
UA_BROWSER = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
)
UA_SHORT = "Mozilla/5.0"


def _is_html(content: bytes) -> bool:
    """True se il contenuto sembra una pagina HTML (errore/challenge)."""
    head = content[:512].lower()
    return b"<!doctype" in head or b"<html" in head or b"access denied" in head


def _proxy() -> dict[str, str] | None:
    url = os.environ.get("BLOCKED_SOURCE_PROXY")
    if not url:
        return None
    return {"http": url, "https": url}


def _try_httpclient(output: Path, proxies: dict | None) -> bool:
    """HttpClient di lab-connectors, opzionalmente con proxy esplicito."""
    from lab_connectors.http import HttpClient

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
    }
    client = HttpClient(timeout=300, max_retries=1, user_agent=UA_BROWSER)
    kwargs = {"headers": headers}
    if proxies:
        kwargs["proxies"] = proxies
    result = client.get(URL, **kwargs)
    if result.response is not None and result.response.status_code == 200:
        content = result.response.content
        if not _is_html(content):
            output.write_bytes(content)
            print(f"HttpClient{' (proxy)' if proxies else ''}: ok ({output.stat().st_size} bytes)")
            return True
        print(f"HttpClient{' (proxy)' if proxies else ''}: 200 ma HTML — scartato")
    return False


def _try_tool(output: Path, tool: str) -> bool:
    """wget o curl con UA breve e proxy (se configurato)."""
    proxies = _proxy()
    cmd = []
    if tool == "wget":
        cmd = ["wget", "-q", "--user-agent=" + UA_SHORT]
        if proxies:
            cmd += [
                "-e",
                "use_proxy=yes",
                "-e",
                f"http_proxy={proxies['http']}",
                "-e",
                f"https_proxy={proxies['https']}",
            ]
        cmd += ["-O", str(output), URL]
    else:  # curl
        cmd = ["curl", "-sS", "-A", UA_SHORT]
        if proxies:
            cmd += ["-x", proxies["https"]]
        cmd += ["-o", str(output), URL]
    try:
        subprocess.run(cmd, check=True, timeout=400)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    if output.exists() and output.stat().st_size > 0:
        content = output.read_bytes()
        if not _is_html(content):
            print(f"{tool}{' (proxy)' if proxies else ''}: ok ({output.stat().st_size} bytes)")
            return True
        print(f"{tool}: scaricato ma HTML — scartato")
    return False


def main() -> None:
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv")
    # 1. diretto
    if _try_httpclient(output, None):
        return
    # 2. proxy esplicito (pattern mur-immatricolati)
    if _proxy():
        print("tentativo diretto fallito — riprovo con proxy esplicito")
        if _try_httpclient(output, _proxy()):
            return
        if _try_tool(output, "wget"):
            return
        if _try_tool(output, "curl"):
            return
    raise RuntimeError(f"Download fallito per {URL} (tutti i client, con e senza proxy)")


if __name__ == "__main__":
    main()
