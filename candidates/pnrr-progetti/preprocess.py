#!/usr/bin/env python3
"""Download PNRR Progetti CSV da Italia Domani.
Il server AEM blocca python-requests ma accetta wget.
"""

import subprocess
import sys

url = "https://www.italiadomani.gov.it/content/dam/sogei-ng/opendata/PNRR_Progetti.csv"
output = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

try:
    subprocess.run(
        ["wget", "-q", "--user-agent=" + ua, "-O", output, url],
        check=True,
        timeout=300,
    )
    print("Downloaded via wget")
except (subprocess.CalledProcessError, FileNotFoundError):
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=300) as resp:
        with open(output, "wb") as f:
            f.write(resp.read())
    print("Downloaded via urllib")
