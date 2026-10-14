#!/usr/bin/env python3
"""Fetch proiezioni demografiche ISTAT da demo.istat.it (RPCCerca.php).

Canale: SPA demo.istat.it — POST RPCCerca.php (JSON).
Sostituisce SDMX (flaky) con l'API interna della piattaforma Demo.

Usage: python preprocess.py <year> <output.csv>
  year: anno base delle proiezioni (default 2025)
  output: path CSV di output (raw_input.csv)
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://demo.istat.it/app"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"{BASE}/?i=PPR&l=it",
    "Origin": "https://demo.istat.it",
    "User-Agent": "DataCivicLab/1.0",
}

# regioni demo → (codice NUTS2, nome, ripartizione parent)
REGIONI = {
    "1": ("ITC1", "Piemonte", "27"),
    "2": ("ITC2", "Valle d'Aosta", "27"),
    "3": ("ITC4", "Lombardia", "27"),
    "5": ("ITH3", "Veneto", "28"),
    "6": ("ITH4", "Friuli-Venezia Giulia", "28"),
    "7": ("ITC3", "Liguria", "27"),
    "8": ("ITH5", "Emilia-Romagna", "28"),
    "9": ("ITI1", "Toscana", "24"),
    "10": ("ITI2", "Umbria", "24"),
    "11": ("ITI3", "Marche", "24"),
    "12": ("ITI4", "Lazio", "24"),
    "13": ("ITF1", "Abruzzo", "29"),
    "14": ("ITF2", "Molise", "29"),
    "15": ("ITF3", "Campania", "29"),
    "16": ("ITF4", "Puglia", "29"),
    "17": ("ITF5", "Basilicata", "29"),
    "18": ("ITF6", "Calabria", "29"),
    "19": ("ITG1", "Sicilia", "30"),
    "20": ("ITG2", "Sardegna", "30"),
    "21": ("ITH1", "P.A. Bolzano", "28"),
    "22": ("ITH2", "P.A. Trento", "28"),
}

# ripartizioni aggregate (codici custom, univoci — non NUTS)
RIPARTIZIONI = {
    "26": ("IT", "Italia"),
    "23": ("RIP_NORD", "Nord"),
    "27": ("RIP_NORD_OVEST", "Nord-ovest"),
    "28": ("RIP_NORD_EST", "Nord-est"),
    "24": ("RIP_CENTRO", "Centro"),
    "25": ("RIP_MEZZOGIORNO", "Mezzogiorno"),
}

YEARS = list(range(2025, 2081))
COMPONENTI = {
    "1": "popolazione_inizio_anno",
    "2": "nati",
    "3": "morti",
    "8": "saldo_naturale",
    "9": "saldo_migratorio_estero",
    "10": "saldo_migratorio_interno",
}


def rpc(form: dict) -> list[dict]:
    """POST a RPCCerca.php e restituisce le righe del datatable."""
    data = urllib.parse.urlencode(form).encode()
    req = urllib.request.Request(f"{BASE}/RPCCerca.php", data=data, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = json.loads(resp.read().decode())
    if payload.get("type") != "json" or not payload.get("Status"):
        raise RuntimeError(f"RPC error: {payload.get('Messaggio') or payload.get('message')}")
    return payload.get("datatable", {}).get("data") or []


def fetch_componenti(rip_code: str, comp_code: str, reg_code: str = "") -> list[dict]:
    """Fetch bilancio demografico per una ripartizione (o regione) e componente."""
    rows = rpc(
        {
            "componenti": comp_code,
            "annoda": str(YEARS[0]),
            "annoa": str(YEARS[-1]),
            "ripartizione": rip_code,
            "regione": reg_code,
            "hid-i": "PPR",
            "hid-a": "2025",
            "hid-l": "it",
            "hid-cat": "PPR",
            "hid-dati": "dati-form-1",
            "hid-tavola": "tavola-form-1",
            "btnricerca-1": "Cerca",
        }
    )
    return rows


def main() -> None:
    out_path = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
    fieldnames = [
        "territorio_codice",
        "territorio",
        "componente_codice",
        "componente",
        "anno",
        "valore",
    ]
    n = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        # ripartizioni aggregate (ripartizione=X, regione vuota)
        for rip_code, (nuts, nome) in RIPARTIZIONI.items():
            for comp_code, comp_name in COMPONENTI.items():
                try:
                    rows = fetch_componenti(rip_code, comp_code)
                except Exception as e:
                    print(f"  SKIP {nome}/{comp_name}: {e}", file=sys.stderr)
                    continue
                for r in rows:
                    anno = r.get("anno")
                    val = r.get("median")
                    if anno is None or val in (None, ""):
                        continue
                    w.writerow(
                        {
                            "territorio_codice": nuts,
                            "territorio": nome,
                            "componente_codice": comp_name,
                            "componente": comp_name.replace("_", " ").title(),
                            "anno": anno,
                            "valore": val,
                        }
                    )
                    n += 1
                time.sleep(0.3)
            print(f"  {nome} ({nuts}) ok", file=sys.stderr)
        # regioni (ripartizione=parent, regione=id)
        for reg_id, (nuts, nome, parent) in REGIONI.items():
            for comp_code, comp_name in COMPONENTI.items():
                try:
                    rows = fetch_componenti(parent, comp_code, reg_code=reg_id)
                except Exception as e:
                    print(f"  SKIP {nome}/{comp_name}: {e}", file=sys.stderr)
                    continue
                for r in rows:
                    anno = r.get("anno")
                    val = r.get("median")
                    if anno is None or val in (None, ""):
                        continue
                    w.writerow(
                        {
                            "territorio_codice": nuts,
                            "territorio": nome,
                            "componente_codice": comp_name,
                            "componente": comp_name.replace("_", " ").title(),
                            "anno": anno,
                            "valore": val,
                        }
                    )
                    n += 1
                time.sleep(0.3)
            print(f"  {nome} ({nuts}) ok", file=sys.stderr)
    print(f"raw written: {n} rows -> {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
