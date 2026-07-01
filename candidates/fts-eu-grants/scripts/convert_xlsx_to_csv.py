#!/usr/bin/env python3
"""Preprocess: scarica FTS XLSX dal portale UE e lo converte in CSV normalizzato.

Usage:
    python scripts/convert_xlsx_to_csv.py --year 2024 --output fts_2024.csv

Lo script:
1. Scarica il file XLSX dall'URL ufficiale FTS
2. Legge tutte le celle come stringhe (dtype=str)
3. Normalizza le colonne importi (rimuove virgole, gestisce trattini)
4. Produce CSV pulito con header in italiano e tipi numerici
"""

import argparse
import csv
import io
import sys

import pandas as pd
import requests

FTS_URL_TEMPLATE = (
    "https://ec.europa.eu/budget/financial-transparency-system/download/{year}_FTS_dataset_en.xlsx"
)

FTS_COLUMNS = [
    "anno",
    "budget",
    "rif_impegno_giuridico",
    "rif_bilancio",
    "beneficiario_nome",
    "beneficiario_partita_iva",
    "flag_no_profit",
    "flag_ong",
    "flag_coordinatore",
    "beneficiario_indirizzo",
    "beneficiario_citta",
    "beneficiario_cap",
    "paese_beneficiario",
    "nuts2",
    "zona_geografica",
    "luogo_azione",
    "importo_contrattato",
    "importo_contrattato_stimato",
    "importo_consumato_stimato",
    "impegno_importo_a",
    "importo_aggiuntivo_ridotto_b",
    "impegno_totale_a_plus_b",
    "impegno_consumato",
    "fonte_dettaglio",
    "tipo_spesa",
    "oggetto_contributo",
    "dipartimento_responsabile",
    "linea_bilancio_codice",
    "linea_bilancio_nome",
    "nome_programma",
    "tipo_finanziamento",
    "codice_gruppo_beneficiario",
    "tipo_beneficiario",
    "data_inizio_progetto",
    "data_fine_progetto",
    "tipo_contratto",
    "tipo_gestione",
    "paese_beneficiante",
]


def _normalize_amount(value) -> float | None:
    """Convert various amount formats to float or None."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        s = value.strip()
        if not s or s in ("-", ".", "", "nan", "NaN", "N/A"):
            return None
        # Remove commas used as thousands separators
        s = s.replace(",", "")
        try:
            return float(s)
        except (ValueError, TypeError):
            return None
    return None


def download_xlsx(url: str) -> bytes:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; DataCivicLab/1.0)"}
    r = requests.get(url, timeout=120, headers=headers)
    r.raise_for_status()
    return r.content


def convert_xlsx_to_csv(xlsx_data: bytes, output_path: str) -> dict:
    df = pd.read_excel(
        io.BytesIO(xlsx_data),
        sheet_name=0,
        header=0,
        dtype=str,
        engine="openpyxl",
    )

    n_rows = len(df)
    n_cols = len(df.columns)

    # Rename columns to canonical names
    if n_cols != len(FTS_COLUMNS):
        raise ValueError(f"Expected {len(FTS_COLUMNS)} columns, got {n_cols}")

    df.columns = FTS_COLUMNS

    # Normalize amount columns (16-22)
    for col_idx in range(16, 23):
        col_name = df.columns[col_idx]
        df[col_name] = df[col_name].apply(_normalize_amount)

    # Trim string columns
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.strip()

    # Write CSV
    df.to_csv(
        output_path,
        index=False,
        quoting=csv.QUOTE_ALL,
        encoding="utf-8",
    )

    return {"rows": n_rows, "cols": n_cols}


def main():
    parser = argparse.ArgumentParser(description="Download and convert FTS XLSX to CSV")
    parser.add_argument("--year", type=int, required=True, help="Year (e.g. 2024)")
    parser.add_argument("--output", type=str, required=True, help="Output CSV path")
    args = parser.parse_args()

    url = FTS_URL_TEMPLATE.format(year=args.year)

    print(f"Downloading {url} ...", file=sys.stderr)
    data = download_xlsx(url)
    print(f"  Got {len(data)} bytes", file=sys.stderr)

    print("Converting to CSV ...", file=sys.stderr)
    info = convert_xlsx_to_csv(data, args.output)
    print(
        f"  {info['rows']} rows, {info['cols']} columns written to {args.output}", file=sys.stderr
    )


if __name__ == "__main__":
    main()
