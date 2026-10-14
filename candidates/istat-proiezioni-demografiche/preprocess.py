#!/usr/bin/env python3
"""Fetch proiezioni demografiche ISTAT base 2025 → 2080.

Due canali:
1. ZIP demo.istat.it → popolazione per età × sesso × regione (median + IC)
2. RPCCerca.php → componenti bilancio (nati, morti, saldi) per Italia + ripartizioni + regioni

Usage: python preprocess.py <output_dir>
  output_dir: directory per raw_input.csv e raw_eta_sesso.csv
"""

from __future__ import annotations

import csv
import io
import json
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

BASE = "https://demo.istat.it/app"
ZIP_URL = "https://demo.istat.it/data/previsioni/Previsioni-Popolazione_per_eta-Regioni.zip"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"{BASE}/?i=PPR&l=it",
    "Origin": "https://demo.istat.it",
    "User-Agent": "DataCivicLab/1.0",
}

# regioni demo → (codice NUTS2, nome, ripartizione parent per RPC)
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

# nome file ZIP → NUTS2
ZIP_MAP = {
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

SESSO_MAP = {"Maschi": "maschi", "Femmine": "femmine", "Totale": "totale"}


def rpc(form: dict) -> list[dict]:
    data = urllib.parse.urlencode(form).encode()
    req = urllib.request.Request(f"{BASE}/RPCCerca.php", data=data, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as resp:
        payload = json.loads(resp.read().decode())
    if payload.get("type") != "json" or not payload.get("Status"):
        raise RuntimeError(f"RPC error: {payload.get('Messaggio') or payload.get('message')}")
    return payload.get("datatable", {}).get("data") or []


def fetch_componenti(rip_code: str, comp_code: str, reg_code: str = "") -> list[dict]:
    return rpc(
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


def fetch_eta_sesso(fout) -> int:
    """Download ZIP e parse CSV regionali → raw_input.csv (grano=eta_sesso)."""
    print("download ZIP...", file=sys.stderr)
    with urllib.request.urlopen(
        urllib.request.Request(ZIP_URL, headers={"User-Agent": "DataCivicLab/1.0"}), timeout=120
    ) as r:
        zip_bytes = r.read()

    n = 0
    w = csv.writer(fout)
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        for name in sorted(zf.namelist()):
            if not name.endswith(".csv"):
                continue
            stem = Path(name).stem.replace("it-Popolazione_per_eta_-_Regione_", "")
            nuts = ZIP_MAP.get(stem)
            if not nuts:
                print(f"  SKIP {stem}: no NUTS mapping", file=sys.stderr)
                continue
            with zf.open(name) as fh:
                text = io.TextIOWrapper(fh, encoding="utf-8-sig")
                lines = text.readlines()
            reader = csv.DictReader(io.StringIO("".join(lines[2:])), delimiter=";")
            for r in reader:
                anno = r.get("Anno")
                sesso = SESSO_MAP.get(r.get("Sesso", ""), "")
                eta = r.get("Età", "")
                val = r.get("Scenario mediano", "")
                if not anno or not sesso or eta == "" or val == "":
                    continue
                w.writerow(["eta_sesso", nuts, "popolazione", anno, sesso, eta, val])
                n += 1
            print(f"  {stem} ({nuts}) ok", file=sys.stderr)
    return n


def fetch_componenti_all(fout) -> int:
    """RPC bilancio demografico per Italia + ripartizioni + regioni → raw_input.csv (grano=componenti)."""
    n = 0
    w = csv.writer(fout)
    for rip_code, (nuts, nome) in RIPARTIZIONI.items():
        for comp_code, comp_name in COMPONENTI.items():
            try:
                rows = fetch_componenti(rip_code, comp_code)
            except Exception as e:
                print(f"  SKIP {nome}/{comp_name}: {e}", file=sys.stderr)
                continue
            for r in rows:
                if r.get("anno") and r.get("median") not in (None, ""):
                    w.writerow(["componenti", nuts, comp_name, r["anno"], "", "", r["median"]])
                    n += 1
            time.sleep(0.3)
        print(f"  {nome} ({nuts}) ok", file=sys.stderr)
    for reg_id, (nuts, nome, parent) in REGIONI.items():
        for comp_code, comp_name in COMPONENTI.items():
            try:
                rows = fetch_componenti(parent, comp_code, reg_code=reg_id)
            except Exception as e:
                print(f"  SKIP {nome}/{comp_name}: {e}", file=sys.stderr)
                continue
            for r in rows:
                if r.get("anno") and r.get("median") not in (None, ""):
                    w.writerow(["componenti", nuts, comp_name, r["anno"], "", "", r["median"]])
                    n += 1
            time.sleep(0.3)
        print(f"  {nome} ({nuts}) ok", file=sys.stderr)
    return n


def main() -> None:
    # argv[1] può essere un file CSV (dal toolkit) o una directory
    arg = sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv"
    if arg.endswith(".csv"):
        raw_path = Path(arg)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        raw_path = Path(arg) / "raw_input.csv"
        raw_path.parent.mkdir(parents=True, exist_ok=True)

    with open(raw_path, "w", newline="", encoding="utf-8") as fout:
        w = csv.writer(fout)
        w.writerow(
            ["grano", "territorio_codice", "componente_codice", "anno", "sesso", "eta", "valore"]
        )

        print("=== età × sesso (ZIP) ===", file=sys.stderr)
        n_eta = fetch_eta_sesso(fout)
        print(f"eta_sesso: {n_eta} rows", file=sys.stderr)

        print("=== componenti bilancio (RPC) ===", file=sys.stderr)
        n_comp = fetch_componenti_all(fout)
        print(f"componenti: {n_comp} rows", file=sys.stderr)

    print(f"TOTAL raw: {n_eta + n_comp} rows -> {raw_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
