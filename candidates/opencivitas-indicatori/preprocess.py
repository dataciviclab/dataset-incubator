#!/usr/bin/env python3
"""Scarica e unisce i CSV indicatori OpenCivitas per un anno.

Per ogni anno, scarica tutti i file ZIP `{year}_Ind_FC{prefix}{ambito}_{suffix}_csv.zip`
per i 7 ambiti tematici, estrae i CSV e li unisce in un unico file
con colonna aggiuntiva 'ambito'.

Usage: python preprocess.py <year> <output.csv>
"""

import csv
import os
import sys
import tempfile
import zipfile
from pathlib import Path

from lab_connectors.http.download import download


# Mappa anno → prefisso funzione e suffisso file
# Il pattern URL: https://docs.opencivitas.it/{year}_Ind_FC{prefix}{ambito}_{suffix}_csv.zip
YEAR_MAP = {
    # 2015: URL senza anno, suffisso 2 per tutti
    2015: {"prefix": "20", "suffix_default": "2", "tot_suffix": "2", "no_year": True},
    2016: {"prefix": "30", "suffix_default": "1", "tot_suffix": "1"},
    2017: {"prefix": "40", "suffix_default": "1", "tot_suffix": "1"},
    2018: {"prefix": "50", "suffix_default": "1", "tot_suffix": "1"},
    2019: {"prefix": "60", "suffix_default": "1", "tot_suffix": "2"},
    2021: {"prefix": "70", "suffix_default": "1", "tot_suffix": "1"},
    2022: {"prefix": "80", "suffix_default": "1", "tot_suffix": "2"},
}

# Ambiti: sigla_nell_URL → nome_descrittivo
AMBITI = [
    ("AMMIN", "amministrazione"),
    ("ISTRUZ", "istruzione"),
    ("POLIZIA", "polizia_locale"),
    ("RIFIUTI", "rifiuti"),
    ("SOCNID", "sociale_asili_nido"),
    ("TERRVIAB", "viabilita_territorio"),
    ("TOT", "servizi_totali"),
]

BASE_URL = "https://docs.opencivitas.it"


def download_and_extract_csv(url, tmp_dir):
    """Scarica un file ZIP e restituisce il path del CSV estratto."""
    zip_path = os.path.join(tmp_dir, "temp.zip")

    # Download con lab-connectors (SSL fallback, proxy, retry)
    try:
        data = download(url, timeout=60)
    except RuntimeError:
        return None  # File non disponibile, skip silenzioso

    try:
        with open(zip_path, "wb") as f:
            f.write(data)
        with zipfile.ZipFile(zip_path) as zf:
            csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
            if not csv_files:
                return None
            csv_name = csv_files[0]
            zf.extract(csv_name, tmp_dir)
            return os.path.join(tmp_dir, csv_name)
    except Exception:
        return None


def main():
    if len(sys.argv) < 3:
        print("Usage: python preprocess.py <year> <output.csv>", file=sys.stderr)
        sys.exit(1)

    year = int(sys.argv[1])
    output_path = Path(sys.argv[2])

    if year not in YEAR_MAP:
        print(
            f"ERRORE: anno {year} non configurato. Supportati: {list(YEAR_MAP.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    prefix = YEAR_MAP[year]["prefix"]

    with tempfile.TemporaryDirectory() as tmp_dir:
        all_rows = []
        downloaded = 0

        for sigla, ambito_nome in AMBITI:
            # Determina suffisso
            if sigla == "TOT":
                suffix = YEAR_MAP[year]["tot_suffix"]
            else:
                suffix = YEAR_MAP[year]["suffix_default"]

            if YEAR_MAP[year].get("no_year"):
                url = f"{BASE_URL}/Ind_FC{prefix}{sigla}_{suffix}_csv.zip"
            else:
                url = f"{BASE_URL}/{year}_Ind_FC{prefix}{sigla}_{suffix}_csv.zip"

            csv_path = download_and_extract_csv(url, tmp_dir)
            if csv_path is None:
                print(f"  SKIP {sigla} ({ambito_nome}) — non disponibile", flush=True)
                continue

            # Leggi il CSV (prova UTF-8, fallback Latin-1)
            def read_csv(path):
                for enc in ["utf-8-sig", "latin-1", "iso-8859-1"]:
                    try:
                        with open(path, encoding=enc) as f:
                            return list(csv.DictReader(f, delimiter=";"))
                    except (UnicodeDecodeError, UnicodeError):
                        continue
                return []

            rows_data = read_csv(csv_path)
            if not rows_data:
                print(f"  SKIP {sigla} — encoding non gestibile", flush=True)
                continue

            # Verifica header
            if not {"USERNAME", "Indicatore/Determinante", "Valore"}.issubset(
                set(rows_data[0].keys())
            ):
                print(f"  SKIP {sigla} — colonne inattese: {list(rows_data[0].keys())}", flush=True)
                continue

            for row in rows_data:
                username = (row.get("USERNAME") or "").strip()
                indicatore = (row.get("Indicatore/Determinante") or "").strip()
                valore_raw = (row.get("Valore") or "").strip()

                if not username or not indicatore:
                    continue

                all_rows.append(
                    {
                        "username": username,
                        "anno": str(year),
                        "ambito": ambito_nome,
                        "indicatore": indicatore,
                        "valore": valore_raw,
                    }
                )

            downloaded += 1
            print(f"  OK {sigla} ({ambito_nome}) — letto", flush=True)

        if not all_rows:
            print("ERRORE: nessun dato scaricato", file=sys.stderr)
            sys.exit(1)

        print(
            f"Scaricati {downloaded}/{len(AMBITI)} ambiti, {len(all_rows)} righe totali", flush=True
        )

        if downloaded < 5:
            print(
                f"ERRORE: solo {downloaded}/{len(AMBITI)} ambiti scaricati, soglia minima 5",
                file=sys.stderr,
            )
            sys.exit(1)

        # Scrivi output
        fieldnames = ["username", "anno", "ambito", "indicatore", "valore"]
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(all_rows)

        print(
            f"Output: {output_path} ({len(all_rows)} righe, {output_path.stat().st_size / 1e6:.1f} MB)",
            flush=True,
        )


if __name__ == "__main__":
    main()
