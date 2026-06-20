#!/usr/bin/env python3
"""Download PNRR Progetti CSV from Italia Domani.

Il server AEM blocca python-requests ma accetta wget.
Prova wget prima, fallback a urllib (potrebbe fallire con 403).
Rimuove il BOM (UTF-8-SIG) dal file scaricato.
"""

import subprocess
import sys
import os

url = "https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Progetti.csv"
output = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

# Try wget first (works with AEM WAF)
try:
    subprocess.run(
        ["wget", "-q", "--user-agent=" + ua, "-O", output, url],
        check=True,
        timeout=300,
    )
    print("Downloaded via wget")
except (subprocess.CalledProcessError, FileNotFoundError):
    # Fallback: python-requests (may get 403 on AEM)
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = resp.read()
    # Strip BOM if present
    if data[:3] == b"\xef\xbb\xbf":
        data = data[3:]
    with open(output, "wb") as f:
        f.write(data)
    print("Downloaded via urllib")

# Strip BOM from wget-downloaded file
if os.path.getsize(output) > 0:
    with open(output, "rb") as f:
        data = f.read()
    if data[:3] == b"\xef\xbb\xbf":
        data = data[3:]
        with open(output, "wb") as f:
            f.write(data)
        print("BOM stripped")
