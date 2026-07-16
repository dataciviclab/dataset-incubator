#!/usr/bin/env python3
"""Scarica e unisce i metadati degli indicatori OpenCivitas per un anno.

Per ogni anno, scarica i file XLSX di metadati per tutti gli ambiti,
legge i fogli 'Indicatori', 'Determinanti' e 'Codici' e unisce in
un unico CSV.

Usage: python preprocess.py <year> <output.csv>
"""

import csv
import os
import sys
import tempfile
import zipfile
from pathlib import Path

from lab_connectors.http.download import download

BASE_URL = "https://docs.opencivitas.it"


# Mappa anno → prefisso funzione
YEAR_MAP = {
    2015: {"prefix": "20", "no_year": True, "suffix": "2"},
    2016: {"prefix": "30"},
    2017: {"prefix": "40"},
    2018: {"prefix": "50"},
    2019: {"prefix": "60"},
    2021: {"prefix": "70"},
    2022: {"prefix": "80"},
}

# Ambiti
AMBITI = [
    ("AMMIN", "amministrazione"),
    ("ISTRUZ", "istruzione"),
    ("POLIZIA", "polizia_locale"),
    ("RIFIUTI", "rifiuti"),
    ("SOCNID", "sociale_asili_nido"),
    ("TERRVIAB", "viabilita_territorio"),
    ("TOT", "servizi_totali"),
]


def download_and_read_metadata(url, tmp_dir, ambito_nome, year):
    """Scarica ZIP metadati, estrae XLSX, legge foglio Indicatori."""
    zip_path = os.path.join(tmp_dir, "meta.zip")

    try:
        data = download(url, timeout=30)
    except RuntimeError:
        return []

    try:
        with open(zip_path, "wb") as f:
            f.write(data)
        with zipfile.ZipFile(zip_path) as zf:
            xlsx_files = [f for f in zf.namelist() if f.endswith(".xlsx")]
            if not xlsx_files:
                return []
            zf.extract(xlsx_files[0], tmp_dir)
            xlsx_path = os.path.join(tmp_dir, xlsx_files[0])
    except Exception:
        return []

    # Leggi fogli Indicatori, Determinanti, Codici con pandas
    try:
        import pandas as pd

        xls = pd.ExcelFile(xlsx_path)
        rows = []

        # Foglio 1: Indicatori
        sheet_ind = None
        for s in xls.sheet_names:
            if s.upper().startswith("INDICATORI"):
                sheet_ind = s
                break
        if sheet_ind:
            df = pd.read_excel(xls, sheet_name=sheet_ind)
            if {"VAR_IND_COD", "VAR_IND_DES"}.issubset(set(df.columns)):
                for _, r in df.iterrows():
                    codice = str(r.get("VAR_IND_COD", "")).strip()
                    desc = str(r.get("VAR_IND_DES", "")).strip()
                    if codice and desc and codice != "nan":
                        rows.append(
                            {
                                "codice_indicatore": codice,
                                "descrizione": desc,
                                "tipo": "IND",
                                "categoria": str(r.get("VAR_IND_TIP", "")).strip(),
                                "funzione": str(r.get("VAR_IND_FUNZIONE", "")).strip(),
                                "ordine": str(r.get("VAR_IND_ORD", "")).strip(),
                                "anno": str(year),
                                "ambito": ambito_nome,
                            }
                        )

        # Foglio 2: Determinanti
        sheet_det = None
        for s in xls.sheet_names:
            if s.upper().startswith("DETERMINANTI"):
                sheet_det = s
                break
        if sheet_det:
            df = pd.read_excel(xls, sheet_name=sheet_det)
            if {"VAR_DET_COD", "VAR_DET_DES"}.issubset(set(df.columns)):
                for _, r in df.iterrows():
                    codice = str(r.get("VAR_DET_COD", "")).strip()
                    desc = str(r.get("VAR_DET_DES", "")).strip()
                    if codice and desc and codice != "nan":
                        rows.append(
                            {
                                "codice_indicatore": codice,
                                "descrizione": desc,
                                "tipo": "DET",
                                "categoria": str(r.get("VAR_DET_CAT_DES", "")).strip(),
                                "funzione": str(r.get("VAR_DET_FUNZIONE", "")).strip(),
                                "ordine": "",
                                "anno": str(year),
                                "ambito": ambito_nome,
                            }
                        )

        # Foglio 3: Codici anomalia
        sheet_cod = None
        for s in xls.sheet_names:
            if s.upper().startswith("CODICI"):
                sheet_cod = s
                break
        if sheet_cod:
            df = pd.read_excel(xls, sheet_name=sheet_cod)
            col_map = {c.upper().replace(" ", "_"): c for c in df.columns}
            cod_col = col_map.get("CODICE", "")
            des_col = col_map.get("DESCRIZIONE_CODICE", "")
            fun_col = col_map.get("FUNZIONE", "")
            if cod_col and des_col:
                for _, r in df.iterrows():
                    codice = str(r.get(cod_col, "")).strip()
                    desc = str(r.get(des_col, "")).strip()
                    if codice and desc and codice != "nan":
                        rows.append(
                            {
                                "codice_indicatore": codice,
                                "descrizione": desc,
                                "tipo": "COD",
                                "categoria": "",
                                "funzione": str(r.get(fun_col, "")).strip(),
                                "ordine": "",
                                "anno": str(year),
                                "ambito": ambito_nome,
                            }
                        )

        return rows
    except ImportError:
        print("ERRORE: pandas non installato", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"  ERRORE lettura XLSX: {e}", file=sys.stderr)
        return []


def main():
    if len(sys.argv) < 3:
        print("Usage: python preprocess.py <year> <output.csv>", file=sys.stderr)
        sys.exit(1)

    year = int(sys.argv[1])
    output_path = Path(sys.argv[2])

    if year not in YEAR_MAP:
        print(f"ERRORE: anno {year} non supportato. Usa: {list(YEAR_MAP.keys())}", file=sys.stderr)
        sys.exit(1)

    prefix = YEAR_MAP[year]["prefix"]

    with tempfile.TemporaryDirectory() as tmp_dir:
        all_rows = []
        total_downloaded = 0

        for sigla, ambito_nome in AMBITI:
            suffix = YEAR_MAP[year].get("suffix", "1")
            if YEAR_MAP[year].get("no_year"):
                url = f"{BASE_URL}/Metadati_Ind_FC{prefix}{sigla}_{suffix}_xlsx.zip"
            else:
                url = f"{BASE_URL}/{year}_Metadati_Ind_FC{prefix}{sigla}_{suffix}_xlsx.zip"
            rows = download_and_read_metadata(url, tmp_dir, ambito_nome, year)
            if rows:
                all_rows.extend(rows)
                total_downloaded += 1
                print(f"  OK {sigla} ({ambito_nome}) — {len(rows)} voci", flush=True)
            else:
                print(f"  SKIP {sigla} ({ambito_nome})", flush=True)

        if not all_rows:
            print("ERRORE: nessun metadato scaricato", file=sys.stderr)
            sys.exit(1)

        if total_downloaded < len(AMBITI):
            print(
                f"ERRORE: solo {total_downloaded}/{len(AMBITI)} ambiti scaricati, richiesti tutti e {len(AMBITI)}",
                file=sys.stderr,
            )
            sys.exit(1)

        fieldnames = [
            "codice_indicatore",
            "descrizione",
            "tipo",
            "categoria",
            "funzione",
            "ordine",
            "anno",
            "ambito",
        ]
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(all_rows)

        print(f"Output: {output_path} ({len(all_rows)} righe)", flush=True)


if __name__ == "__main__":
    main()
