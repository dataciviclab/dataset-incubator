#!/usr/bin/env python3
"""Fetch proiezioni demografiche ISTAT da demo.istat.it.

Scarica il ZIP ufficiale (età × sesso × regione, base 1/1/2025 → 2080)
e lo normalizza in un singolo CSV lungo.

Usage: python preprocess.py raw_input.csv
"""

from __future__ import annotations

import csv
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

ZIP_URL = "https://demo.istat.it/data/previsioni/Previsioni-Popolazione_per_eta-Regioni.zip"

# nome file ZIP → codice NUTS2
NUTS = {
    "Abruzzo": "ITF1",
    "Basilicata": "ITF5",
    "Calabria": "ITF6",
    "Campania": "ITF3",
    "Emilia-Romagna": "ITH5",
    "Friuli-Venezia_Giulia": "ITH4",
    "Lazio": "ITI4",
    "Liguria": "ITC3",
    "Lombardia": "ITC4",
    "Marche": "ITI3",
    "Molise": "ITF2",
    "Piemonte": "ITC1",
    "Provincia_autonoma_di_Bolzano": "ITH1",
    "Provincia_autonoma_di_Trento": "ITH2",
    "Puglia": "ITF4",
    "Sardegna": "ITG2",
    "Sicilia": "ITG1",
    "Toscana": "ITI1",
    "Trentino-Alto_Adige": "ITH",
    "Umbria": "ITI2",
    "Valle_d_Aosta-Vallee_d_Aoste": "ITC2",
    "Veneto": "ITH3",
}

SESSO = {"Maschi": "maschi", "Femmine": "femmine", "Totale": "totale"}


def main() -> None:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv")
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"download {ZIP_URL}", file=sys.stderr)
    with urllib.request.urlopen(ZIP_URL, timeout=120) as r:
        buf = io.BytesIO(r.read())

    n = 0
    with zipfile.ZipFile(buf) as zf, open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["territorio_codice", "anno", "sesso", "eta", "popolazione"])
        for name in sorted(zf.namelist()):
            if not name.endswith(".csv"):
                continue
            stem = Path(name).stem.replace("it-Popolazione_per_eta_-_Regione_", "")
            nuts = NUTS.get(stem)
            if not nuts:
                print(f"SKIP {stem}", file=sys.stderr)
                continue
            with zf.open(name) as fh:
                lines = io.TextIOWrapper(fh, encoding="utf-8-sig").readlines()
            # L0 titolo, L1 regione, L2 header, L3+ dati
            reader = csv.DictReader(io.StringIO("".join(lines[2:])), delimiter=";")
            for row in reader:
                eta = row.get("Età", "")
                val = row.get("Scenario mediano", "")
                if not row.get("Anno") or eta == "" or val == "":
                    continue
                w.writerow(
                    [
                        nuts,
                        row["Anno"],
                        SESSO.get(row.get("Sesso", ""), row.get("Sesso", "")),
                        eta,
                        val,
                    ]
                )
                n += 1
            print(f"  {stem} ({nuts}) ok", file=sys.stderr)
    print(f"raw: {n} rows -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
