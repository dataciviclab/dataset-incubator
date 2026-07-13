#!/usr/bin/env python3
"""Parsifica file XLS/XLSX del personale SSN da Ministero Salute.

Output CSV unico con dati TAB1 (ruoli) e MEDICI_E_INFERMIERI.
3 file sorgente:
  2010-2019: C_17_dataset_65_0_upFile.xls  (multi-sheet)
  2020:      C_17_dataset_120_0_upFile.xlsx
  2021:      C_17_dataset_191_0_upFile.xlsx

Uso: python preprocess.py {year} {output.csv}
"""

import csv
import sys
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

URLS = {
    2019: "https://www.dati.salute.gov.it/sites/default/files/imported/C_17_dataset_65_0_upFile.xls",
    2020: "https://www.dati.salute.gov.it/sites/default/files/imported/C_17_dataset_120_0_upFile.xlsx",
    2021: "https://www.dati.salute.gov.it/sites/default/files/imported/C_17_dataset_191_0_upFile.xlsx",
}

FILES = {
    2019: "C_17_dataset_65_0_upFile.xls",
    2020: "C_17_dataset_120_0_upFile.xlsx",
    2021: "C_17_dataset_191_0_upFile.xlsx",
}

HEADERS = [
    "prospetto",
    "anno",
    "codice_regione",
    "denominazione_regione",
    "codice_azienda",
    "ruolo_categoria",
    "dotazioni_organiche",
    "tempo_pieno_u",
    "tempo_pieno_d",
    "part_time_inf_50_u",
    "part_time_inf_50_d",
    "part_time_sup_50_u",
    "part_time_sup_50_d",
    "pers_anno_rif_u",
    "pers_anno_rif_d",
]


def download(url: str, dest: Path) -> None:
    import shutil
    import ssl
    import subprocess
    import urllib.request

    # 1) Prova curl -k (gestisce SSL meglio, funziona con gov.it)
    curl = shutil.which("curl")
    if curl:
        print(f"Download {url} (via curl)...", flush=True)
        try:
            subprocess.run(
                [curl, "-k", "-sS", "-L", "--max-time", "120", "-o", str(dest), url],
                check=True,
                capture_output=True,
                timeout=120,
            )
            print(f"  -> {dest} ({dest.stat().st_size / 1e6:.1f} MB)", flush=True)
            return
        except Exception as e:
            print(f"  curl fallito: {e}", flush=True)

    # 2) Fallback: urllib con TLSv1.2 forzato (gov.it non supporta TLS 1.3)
    print(f"Download {url} (via urllib TLSv1.2)...", flush=True)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
        data = resp.read()
        dest.write_bytes(data)
    print(f"  -> {dest} ({dest.stat().st_size / 1e6:.1f} MB)", flush=True)


def ensure_file(year: int) -> Path:
    path = CACHE_DIR / FILES.get(year, FILES[2019])
    if not path.exists():
        url = URLS.get(year, URLS[2019])
        download(url, path)
    return path


def _xls_row_is_data(vals):
    return (
        vals
        and vals[0]
        and str(vals[0]).strip() != ""
        and str(vals[0]).strip() != "ANNO DI RIFERIMENTO"
    )


def parse_xls_tab1(workbook, year: int):
    sheet_name = f"TAB1_{year}"
    ws = workbook.sheet_by_name(sheet_name)
    rows = []
    for r in range(3, ws.nrows):
        vals = ws.row_values(r)
        if not _xls_row_is_data(vals):
            continue
        rows.append(
            [
                "TAB1",
                int(vals[0]),
                str(vals[1]).strip(),
                str(vals[2]).strip(),
                str(int(vals[3])) if isinstance(vals[3], float) else str(vals[3]).strip(),
                str(vals[4]).strip(),
                float(vals[5]) if vals[5] else None,
                float(vals[6]) if vals[6] else None,
                float(vals[7]) if vals[7] else None,
                float(vals[8]) if vals[8] else None,
                float(vals[9]) if vals[9] else None,
                float(vals[10]) if vals[10] else None,
                float(vals[11]) if vals[11] else None,
                float(vals[12]) if vals[12] else None,
                float(vals[13]) if vals[13] else None,
            ]
        )
    return rows


def _find_medinf_sheet(workbook, year: int):
    prefix = f"TAB1_{year}"
    for sn in workbook.sheet_names():
        if sn.startswith(prefix) and ("medici" in sn or "infermier" in sn):
            return sn
    raise ValueError(f"Nessun sheet medici/infermieri per {year} tra: {workbook.sheet_names()}")


def parse_xls_medinf(workbook, year: int):
    sheet_name = _find_medinf_sheet(workbook, year)
    ws = workbook.sheet_by_name(sheet_name)
    rows = []
    for r in range(3, ws.nrows):
        vals = ws.row_values(r)
        if not _xls_row_is_data(vals):
            continue
        rows.append(
            [
                "MEDICI_E_INFERMIERI",
                int(vals[0]),
                str(vals[1]).strip(),
                str(vals[2]).strip(),
                str(int(vals[3])) if isinstance(vals[3], float) else str(vals[3]).strip(),
                str(vals[4]).strip(),
                float(vals[5]) if vals[5] else None,
                float(vals[6]) if vals[6] else None,
                float(vals[7]) if vals[7] else None,
                float(vals[8]) if vals[8] else None,
                float(vals[9]) if vals[9] else None,
                float(vals[10]) if vals[10] else None,
                float(vals[11]) if vals[11] else None,
                float(vals[12]) if vals[12] else None,
                float(vals[13]) if vals[13] else None,
            ]
        )
    return rows


def _parse_xlsx_sheet(ws, year: int, prospetto: str):
    rows = []
    all_rows_list = list(ws.iter_rows(values_only=True))
    header_idx = None
    for r_idx, row in enumerate(all_rows_list):
        if row and len(row) > 1 and row[1] == "ANNO DI RIFERIMENTO":
            header_idx = r_idx
            break
    if header_idx is None:
        return rows
    for row in all_rows_list[header_idx + 1 :]:
        if len(row) < 15 or row[1] is None or str(row[1]).strip() == "":
            continue
        anno = int(row[1])
        rows.append(
            [
                prospetto,
                anno,
                str(row[2]).strip() if row[2] else None,
                str(row[3]).strip() if row[3] else None,
                str(row[4]).strip() if row[4] else None,
                str(row[5]).strip() if row[5] else None,
                float(row[6]) if row[6] is not None else None,
                float(row[7]) if row[7] is not None else None,
                float(row[8]) if row[8] is not None else None,
                float(row[9]) if row[9] is not None else None,
                float(row[10]) if row[10] is not None else None,
                float(row[11]) if row[11] is not None else None,
                float(row[12]) if row[12] is not None else None,
                float(row[13]) if row[13] is not None else None,
                float(row[14]) if row[14] is not None else None,
            ]
        )
    return rows


def parse_xlsx_tab1(workbook, year: int):
    sheet_name = f"TAB1 {year}"
    ws = workbook[sheet_name]
    return _parse_xlsx_sheet(ws, year, "TAB1")


def parse_xlsx_medinf(workbook, year: int):
    sheet_name = f"MED E INF_{year}"
    ws = workbook[sheet_name]
    return _parse_xlsx_sheet(ws, year, "MEDICI_E_INFERMIERI")


def main():
    if len(sys.argv) < 3:
        print("Uso: python preprocess.py <year> <output.csv>", file=sys.stderr)
        sys.exit(1)

    output_path = sys.argv[2]

    all_rows = []

    for year in range(2010, 2019 + 1):
        fpath = ensure_file(2019)
        import xlrd

        wb = xlrd.open_workbook(str(fpath))
        all_rows.extend(parse_xls_tab1(wb, year))
        all_rows.extend(parse_xls_medinf(wb, year))
        print(f"  {year}: {len(all_rows)} righe accumulate", flush=True)

    for year in [2020, 2021]:
        fpath = ensure_file(year)
        import openpyxl

        wb = openpyxl.load_workbook(str(fpath), read_only=True, data_only=True)
        all_rows.extend(parse_xlsx_tab1(wb, year))
        all_rows.extend(parse_xlsx_medinf(wb, year))
        print(f"  {year}: {len(all_rows)} righe accumulate", flush=True)

    if not all_rows:
        print("ERRORE: nessun dato estratto", flush=True)
        sys.exit(1)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        w.writerows(all_rows)

    print(f"\nFatto: {len(all_rows)} righe scritte in {output_path}", flush=True)


if __name__ == "__main__":
    main()
