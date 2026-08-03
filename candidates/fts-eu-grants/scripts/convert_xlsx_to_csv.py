#!/usr/bin/env python3
"""Preprocess: scarica FTS XLSX dal portale UE e lo converte in CSV normalizzato.

Usage:
    python scripts/convert_xlsx_to_csv.py --year 2024 --output fts_2024.csv

Lo script:
1. Scarica il file XLSX dall'URL ufficiale FTS
2. Legge tutte le celle come stringhe (dtype=str)
3. Mappa le colonne per NOME (non posizionale — lo schema varia per anno:
   2020-2023 = 39 colonne con "Recipient main registration number" e
   "Call for proposals Reference"/"Project / Contract Reference"/"Acronym";
   2024 = 38 colonne con "Geographical Zone"/"Action location"/"Funding type")
4. Produce CSV con header italiano STABILE (38 colonne) — colonne assenti
   nell'anno vengono lasciate vuote
5. Normalizza le colonne importi
"""

import argparse
import csv
import io
import re
import sys

import pandas as pd
import requests

FTS_URL_TEMPLATE = (
    "https://ec.europa.eu/budget/financial-transparency-system/download/{year}_FTS_dataset_en.xlsx"
)

# Header inglese stabile (ordine di output, 38 colonne)
FTS_OUTPUT_COLUMNS = [
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

# Mappa nome inglese -> colonna italiana (per NOME, robusta al drift di schema)
FTS_COLUMN_MAP = {
    "Year": "anno",
    "Budget": "budget",
    "Reference of the Legal Commitment (LC)": "rif_impegno_giuridico",
    "Reference (Budget)": "rif_bilancio",
    "Name of beneficiary": "beneficiario_nome",
    "Recipient main registration number": "beneficiario_partita_iva",  # 2020-2023
    "Main registration number of beneficiary": "beneficiario_partita_iva",  # 2025
    "VAT number of beneficiary": "beneficiario_partita_iva",  # 2024 (sovrascrive se presente)
    "Not-for-profit organisation (NFPO)": "flag_no_profit",
    "Non-governmental organisation (NGO)": "flag_ong",
    "Coordinator": "flag_coordinatore",
    "Address": "beneficiario_indirizzo",
    "City": "beneficiario_citta",
    "Postal code": "beneficiario_cap",
    "Beneficiary country": "paese_beneficiario",
    "NUTS2": "nuts2",
    "Geographical Zone": "zona_geografica",  # solo 2024
    "Action location": "luogo_azione",  # solo 2024
    "Beneficiary’s contracted amount (EUR)": "importo_contrattato",
    "Beneficiary’s estimated contracted amount (EUR)": "importo_contrattato_stimato",
    "Beneficiary’s estimated consumed amount (EUR)": "importo_consumato_stimato",
    "Commitment contracted amount (EUR) (A)": "impegno_importo_a",
    "Additional/Reduced amount (EUR) (B)": "importo_aggiuntivo_ridotto_b",
    "Commitment  total amount (EUR) (A+B)": "impegno_totale_a_plus_b",
    "Commitment consumed amount (EUR)": "impegno_consumato",
    "Source of (estimated) detailed amount": "fonte_dettaglio",
    "Expense type": "tipo_spesa",
    "Subject of grant or contract": "oggetto_contributo",
    "Responsible department": "dipartimento_responsabile",
    "Budget line number": "linea_bilancio_codice",
    "Budget line name": "linea_bilancio_nome",
    "Programme name": "nome_programma",
    "Funding type": "tipo_finanziamento",  # solo 2024
    "Beneficiary Group Code": "codice_gruppo_beneficiario",
    "Beneficiary type": "tipo_beneficiario",
    "Project start date": "data_inizio_progetto",
    "Project end date": "data_fine_progetto",
    "Type of contract*": "tipo_contratto",
    "Management type": "tipo_gestione",
    "Benefiting country": "paese_beneficiante",
}

# Colonne importo (in formato internazionale: punto decimale, nessuna virgola)
AMOUNT_COLUMNS = {
    "importo_contrattato",
    "importo_contrattato_stimato",
    "importo_consumato_stimato",
    "impegno_importo_a",
    "importo_aggiuntivo_ridotto_b",
    "impegno_totale_a_plus_b",
    "impegno_consumato",
}

# Colonne data: "-" o valori non ISO -> vuoto (il clean fa TRY_CAST AS DATE)
DATE_COLUMNS = {
    "data_inizio_progetto",
    "data_fine_progetto",
}


def _normalize_amount(value) -> float | None:
    """Convert amount to float or None.

    I valori FTS sono GIÀ in formato internazionale (punto decimale,
    nessuna virgola migliaia) — verificato su 2020-2024. NESSUN replace:
    un replace('.','') moltiplicherebbe gli importi per ~1000.
    Gestisce solo i marker di assenza: '-', '', '.', 'N/A', 'nan'.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        s = value.strip()
        if not s or s in ("-", ".", "", "nan", "NaN", "N/A"):
            return None
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

    # Rinomina per NOME: ogni colonna inglese presente -> colonna italiana.
    # Se due colonne inglesi mappano alla stessa italiana (partita_iva),
    # l'ultima (VAT, 2024) sovrascrive — ordine di FTS_COLUMN_MAP.
    n_rows = len(df)
    renamed: dict[str, list] = {c: [None] * n_rows for c in FTS_OUTPUT_COLUMNS}
    for eng_col in df.columns:
        target = FTS_COLUMN_MAP.get(eng_col)
        if target is not None:
            renamed[target] = df[eng_col].tolist()

    out = pd.DataFrame(renamed, columns=FTS_OUTPUT_COLUMNS)

    # Normalizza importi (formato internazionale -> float)
    for col in AMOUNT_COLUMNS:
        out[col] = out[col].apply(_normalize_amount)

    # Normalizza date: "-" o non-ISO -> vuoto (evita ConversionError nel clean)
    for col in DATE_COLUMNS:
        out[col] = out[col].apply(
            lambda v: v if (isinstance(v, str) and re.match(r"^\d{4}-\d{2}-\d{2}", v)) else ""
        )

    # Trim stringhe
    for col in out.columns:
        if out[col].dtype == object:
            out[col] = out[col].str.strip()

    out.to_csv(
        output_path,
        index=False,
        quoting=csv.QUOTE_ALL,
        encoding="utf-8",
    )

    return {"rows": n_rows, "cols": n_cols, "output_cols": len(FTS_OUTPUT_COLUMNS)}


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
        f"  {info['rows']} rows, {info['cols']} xlsx columns -> "
        f"{info['output_cols']} output columns written to {args.output}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
