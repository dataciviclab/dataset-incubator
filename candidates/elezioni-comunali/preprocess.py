#!/usr/bin/env python3
"""Scarica e normalizza i CSV delle elezioni comunali da Eligendo.

Uso: python preprocess.py <anno> <output.csv>
"""

import sys
import csv
import io
import os
import re
import zipfile
import urllib.request
from collections import defaultdict

SOURCES: dict[int, list[tuple[str, str, bool]]] = {
    2016: [("https://dait.interno.gov.it/documenti/opendata/comunali/comunali-20160605.zip", "2016-06-05", True)],
    2017: [("https://dait.interno.gov.it/documenti/opendata/comunali/comunali-20170611.zip", "2017-06-11", True)],
    2018: [("https://dait.interno.gov.it/documenti/opendata/comunali/comunali-20180610.zip", "2018-06-10", True)],
    2019: [("https://dait.interno.gov.it/documenti/opendata/comunali/comunali-20190526.zip", "2019-05-26", True)],
    2020: [("https://dait.interno.gov.it/documenti/opendata/comunali/comunali-20200920.zip", "2020-09-20", True)],
    2021: [("https://dait.interno.gov.it/documenti/opendata/comunali/comunali-20211003.zip", "2021-10-03", True)],
    2024: [("https://dait.interno.gov.it/documenti/opendata/comunali/comunali-20240609.zip", "2024-06-09", True)],
}

COL_MAP: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^DATAELEZIONE$", re.I), "data_elezione_raw"),
    (re.compile(r"^REG(IONE)?$", re.I), "regione"),
    (re.compile(r"^PROV(INCIA)?$", re.I), "provincia"),
    (re.compile(r"^COMUNE$", re.I), "comune"),
    (re.compile(r"^TURNO$", re.I), "turno"),
    (re.compile(r"^(ELETTORI(TOT)?|ELETTORITOTALI)$", re.I), "elettori"),
    (re.compile(r"^(ELETTORI_MASCHI|ELETTORIMASCHI)$", re.I), "elettori_maschi"),
    (re.compile(r"^(VOTANTI(TOT)?|NUMVOTANTITOTALI|VOTANTITOTALI)$", re.I), "votanti"),
    (re.compile(r"^(VOTANTI_MASCHI|VOTANTIMASCHI|NUMVOTANTIMASCHI)$", re.I), "votanti_maschi"),
    (re.compile(r"^(SCHEDE_BIANCHE|SKBIANCHE|SCHEDEBIANCHE)$", re.I), "schede_bianche"),
    (re.compile(r"^(COGNOME|COGNOME_CANDIDATO)$", re.I), "cognome"),
    (re.compile(r"^(NOME|NOME_CANDIDATO)$", re.I), "nome"),
    (re.compile(r"^(DATANASCITA|DATA_NASCITA)$", re.I), "data_nascita"),
    (re.compile(r"^(LUOGONASCITA|LUOGO_NASCITA)$", re.I), "luogo_nascita"),
    (re.compile(r"^SESSO$", re.I), "sesso"),
    (re.compile(r"^(CODTIPOELETTO|ELETTO)$", re.I), "cod_tipo_elettore"),
    (re.compile(r"^(VOTI_CANDIDATO|VOTICAND(IDATO)?|VOTICANDIDSINDACO)$", re.I), "voti_candidato"),
    (re.compile(r"^(LISTA|DESCR_LISTA|DESCRLISTA)$", re.I), "lista"),
    (re.compile(r"^(VOTI_LISTA|VOTILISTA)$", re.I), "voti_lista"),
    (re.compile(r"^(SEGGI_LISTA|SEGGILISTA|seggilista)$", re.I), "seggi_lista"),
    (re.compile(r"^votivalidiliste$", re.I), "voti_validi_liste"),
    (re.compile(r"^votivalidicandidsindaco$", re.I), "voti_validi_candidato"),
    (re.compile(r"^codtipoinvalidita$", re.I), "cod_tipo_invalidita"),
]


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def normalize_number(val: str) -> str:
    val = val.strip().strip('"')
    if not val or val in ("***", "-", "N.D."):
        return ""
    if "," in val:
        val = val.replace(".", "").replace(",", ".")
        if val.endswith(".0"):
            val = val[:-2]
    else:
        val = val.replace(".", "")
    return val


def smart_decode(data: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "iso-8859-1", "cp1252"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def parse_csv(content: str) -> list[list[str]]:
    reader = csv.reader(io.StringIO(content), delimiter=";")
    return [row for row in reader if any(cell.strip() for cell in row)]


def normalize_columns(header: list[str]) -> tuple[list[str], list[int]]:
    norm = []
    indices = []
    for i, col in enumerate(header):
        col = col.strip().strip('"')
        mapped = None
        for pattern, name in COL_MAP:
            if pattern.match(col):
                mapped = name
                break
        if mapped:
            norm.append(mapped)
            indices.append(i)
    return norm, indices


def extract_scrutini_from_txt(zf: zipfile.ZipFile) -> list[list[str]]:
    for name in zf.namelist():
        base = os.path.basename(name)
        if base.startswith("~") or base.startswith("."):
            continue
        if base.lower().endswith(".txt") or base.lower().endswith(".csv"):
            if "preferenze" in base.lower():
                continue
            content = zf.read(name)
            decoded = smart_decode(content)
            rows = parse_csv(decoded)
            if rows:
                return rows
    return []


def process_2016_2020(url: str, election_date: str) -> list[dict]:
    raw = download(url)
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        raw_rows = extract_scrutini_from_txt(zf)

    if not raw_rows:
        return []

    header = raw_rows[0]
    col_names, col_indices = normalize_columns(header)

    records = []
    for row in raw_rows[1:]:
        if not row or not any(cell.strip() for cell in row):
            continue
        rec = {"data_elezione": election_date}
        for name, idx in zip(col_names, col_indices):
            if idx < len(row):
                val = row[idx].strip().strip('"')
                if name in ("elettori", "elettori_maschi", "votanti", "votanti_maschi",
                            "schede_bianche", "voti_candidato", "voti_lista",
                            "seggi_lista", "turno"):
                    val = normalize_number(val)
                rec[name] = val
        if "cognome" in rec and "nome" in rec:
            rec["candidato"] = f"{rec.pop('cognome', '')} {rec.pop('nome', '')}".strip()
        records.append(rec)

    return records


def process_2021(url: str, election_date: str) -> list[dict]:
    raw = download(url)
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        raw_rows = extract_scrutini_from_txt(zf)

    if not raw_rows:
        return []

    header = raw_rows[0]
    col_names, col_indices = normalize_columns(header)

    records = []
    for row in raw_rows[1:]:
        if not row or not any(cell.strip() for cell in row):
            continue
        rec = {"data_elezione": election_date}
        for name, idx in zip(col_names, col_indices):
            if idx < len(row):
                val = row[idx].strip().strip('"')
                if name in ("elettori", "elettori_maschi", "votanti", "votanti_maschi",
                            "schede_bianche", "voti_candidato", "voti_lista",
                            "seggi_lista", "turno", "voti_validi_liste",
                            "voti_validi_candidato", "turno"):
                    val = normalize_number(val)
                rec[name] = val
        if "cognome" in rec and "nome" in rec:
            rec["candidato"] = f"{rec.pop('cognome', '')} {rec.pop('nome', '')}".strip()
        records.append(rec)

    return records


def process_2024(url: str, election_date: str) -> list[dict]:
    raw = download(url)

    scrutini = []
    liste = []

    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        for name in zf.namelist():
            base = os.path.basename(name)
            if base.startswith("~") or base.startswith("."):
                continue
            content = zf.read(name)
            decoded = smart_decode(content)
            rows = parse_csv(decoded)
            if not rows:
                continue
            if "scrutini" in base.lower():
                scrutini = rows
            elif "liste" in base.lower() or "candidati" in base.lower():
                liste = rows

    if not liste:
        return []

    # Parse scrutini into lookup: (regione, provincia, comune, turno) -> turnout
    turnout_lookup = {}
    if scrutini:
        s_header = scrutini[0]
        s_names, s_indices = normalize_columns(s_header)
        for row in scrutini[1:]:
            if not row or not any(cell.strip() for cell in row):
                continue
            key_parts = []
            vals = {}
            for name, idx in zip(s_names, s_indices):
                if idx < len(row):
                    val = row[idx].strip().strip('"')
                    if name in ("elettori", "elettori_maschi", "votanti",
                                "votanti_maschi", "schede_bianche", "turno"):
                        val = normalize_number(val)
                    vals[name] = val
            key = (vals.get("regione", ""), vals.get("provincia", ""),
                   vals.get("comune", ""), vals.get("turno", ""))
            turnout_lookup[key] = vals

    # Parse liste+candidati
    l_header = liste[0]
    l_names, l_indices = normalize_columns(l_header)

    records = []
    for row in liste[1:]:
        if not row or not any(cell.strip() for cell in row):
            continue
        rec = {"data_elezione": election_date}
        for name, idx in zip(l_names, l_indices):
            if idx < len(row):
                val = row[idx].strip().strip('"')
                if name in ("voti_candidato", "voti_lista", "seggi_lista", "turno"):
                    val = normalize_number(val)
                rec[name] = val
        if "cognome" in rec and "nome" in rec:
            rec["candidato"] = f"{rec.pop('cognome', '')} {rec.pop('nome', '')}".strip()

        # Merge turnout from scrutini
        tkey = (rec.get("regione", ""), rec.get("provincia", ""),
                rec.get("comune", ""), rec.get("turno", ""))
        if tkey in turnout_lookup:
            tv = turnout_lookup[tkey]
            rec["elettori"] = tv.get("elettori", "")
            rec["elettori_maschi"] = tv.get("elettori_maschi", "")
            rec["votanti"] = tv.get("votanti", "")
            rec["votanti_maschi"] = tv.get("votanti_maschi", "")
            rec["schede_bianche"] = tv.get("schede_bianche", "")

        records.append(rec)

    return records


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2024
    output = sys.argv[2] if len(sys.argv) > 2 else "raw_input.csv"

    sources = SOURCES.get(year)
    if not sources:
        print(f"Nessuna fonte configurata per l'anno {year}", file=sys.stderr)
        sys.exit(1)

    all_records: list[dict] = []
    for url, election_date, is_zip in sources:
        print(f"  {election_date} -> download...", file=sys.stderr)
        if year in (2016, 2017, 2018, 2019, 2020):
            records = process_2016_2020(url, election_date)
        elif year == 2021:
            records = process_2021(url, election_date)
        elif year == 2024:
            records = process_2024(url, election_date)
        else:
            records = []
        print(f"    {len(records)} righe", file=sys.stderr)
        all_records.extend(records)

    if not all_records:
        print("Nessun dato estratto!", file=sys.stderr)
        sys.exit(1)

    fieldnames = list(all_records[0].keys())

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(all_records)

    print(f"Fatto: anno={year} totale={len(all_records)} righe -> {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
