#!/usr/bin/env python3
"""Download resiliente con fallback multipli per siti che bloccano gli scraper.

Strategie (in ordine):
  1. requests + SSL verify=False → TLS 1.2 → proxy fallback
  2. curl -k (se disponibile)
  3. urllib + TLSv1.2 + User-Agent random

Uso come script:
  python download.py <url> [output_path]

Uso come modulo:
  from scripts.download import download
  data, path = download("https://...", "output.csv")
"""

from __future__ import annotations

import os
import random
import shutil
import ssl
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Literal

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/134.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/134.0.0.0",
]


def _rand_ua() -> str:
    return random.choice(_USER_AGENTS)


def _via_requests(url: str, dest: Path, timeout: int = 120) -> bool:
    """Tenta download con requests + SSL fallback + proxy."""
    try:
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.exceptions import InsecureRequestWarning
    except ImportError:
        return False

    import urllib3
    urllib3.disable_warnings(category=InsecureRequestWarning)

    # --- Tentativo 1: normale ---
    session = requests.Session()
    session.headers.update({"User-Agent": _rand_ua()})
    session.headers.update({"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
    session.headers.update({"Accept-Language": "it-IT,it;q=0.9,en;q=0.8"})

    proxy_url = os.environ.get("BLOCKED_SOURCE_PROXY")
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None

    strategies = [
        ("normale", {"verify": True}),
        ("verify=False", {"verify": False}),
    ]

    for name, kwargs in strategies:
        try:
            resp = session.get(url, timeout=timeout, proxies=proxies, **kwargs)
            resp.raise_for_status()
            dest.write_bytes(resp.content)
            session.close()
            return True
        except Exception as e:
            print(f"    requests ({name}): {e}", flush=True)

    # --- Proxy fallback ---
    if proxy_url:
        try:
            resp = session.get(url, timeout=timeout * 2, proxies=proxies, verify=False)
            resp.raise_for_status()
            dest.write_bytes(resp.content)
            session.close()
            return True
        except Exception as e:
            print(f"    requests (proxy): {e}", flush=True)

    session.close()
    return False


def _via_curl(url: str, dest: Path, timeout: int = 120) -> bool:
    """Tenta download con curl -k -L."""
    curl = shutil.which("curl")
    if not curl:
        return False
    try:
        ua = _rand_ua()
        subprocess.run(
            [curl, "-k", "-sS", "-L", "--max-time", str(timeout),
             "-H", f"User-Agent: {ua}",
             "-o", str(dest), url],
            check=True, capture_output=True, timeout=timeout + 10,
        )
        return dest.exists() and dest.stat().st_size > 0
    except Exception as e:
        print(f"    curl: {e}", flush=True)
        return False


def _via_urllib(url: str, dest: Path, timeout: int = 120) -> bool:
    """Tenta download con urllib + TLSv1.2 + User-Agent random."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": _rand_ua(),
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
            )
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                dest.write_bytes(r.read())
            return True
        except Exception as e:
            if attempt < 2:
                wait = (attempt + 1) * 3
                print(f"    urllib (tentativo {attempt + 1}): {e} — aspetto {wait}s", flush=True)
                time.sleep(wait)
            else:
                print(f"    urllib (esaurito): {e}", flush=True)
    return False


def download(
    url: str,
    dest: str | Path | None = None,
    timeout: int = 120,
    strategies: list[Literal["requests", "curl", "urllib"]] | None = None,
) -> tuple[bytes | None, Path | None]:
    """Scarica URL con fallback multipli.

    Args:
        url: URL da scaricare.
        dest: Path output (default: nome dal URL in cache/).
        timeout: Timeout secondi per tentativo.
        strategies: Ordine strategie. Default: [requests, curl, urllib].

    Returns:
        (contenuto_bytes, path_file) oppure (None, None) se tutto fallisce.
    """
    if dest is None:
        fname = url.split("/")[-1].split("?")[0] or "download.bin"
        dest = Path("cache") / fname
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)

    if strategies is None:
        strategies = ["requests", "curl", "urllib"]

    for strategy in strategies:
        print(f"  download [{strategy}]: {url}", flush=True)
        ok = False
        if strategy == "requests":
            ok = _via_requests(url, dest, timeout)
        elif strategy == "curl":
            ok = _via_curl(url, dest, timeout)
        elif strategy == "urllib":
            ok = _via_urllib(url, dest, timeout)

        if ok and dest.exists() and dest.stat().st_size > 0:
            size = dest.stat().st_size
            print(f"  OK ({size / 1e6:.1f} MB) — {dest}", flush=True)
            return (dest.read_bytes(), dest)

    print(f"  FALLITO: {url}", flush=True)
    return (None, None)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python download.py <url> [output_path]", file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    dest = sys.argv[2] if len(sys.argv) > 2 else None
    data, path = download(url, dest)
    if data is None:
        sys.exit(1)
