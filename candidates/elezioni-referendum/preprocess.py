#!/usr/bin/env python3
"""Scarica e normalizza i CSV dei referendum da Eligendo.

Uso: python preprocess.py <anno> <output.csv>
"""

import sys
import csv
import io
import os
import re
import zipfile
import urllib.request

SOURCES: dict[int, list[tuple[str, str, bool]]] = {
    1995: [("https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19950611.zip", "1995-06-11", True)],
    1999: [("https://dait.interno.gov.it/documenti/opendata/referendum/referendum-19990418.zip", "1999-04-18", True)],
    2000: [("https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20000521.zip", "2000-05-21", True)],
    2003: [("https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20030615.zip", "2003-06-15", True)],
    2006: [("https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20060625.zip", "2006-06-25", True)],
    2016: [("https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20161204.zip", "2016-12-04", True)],
    2020: [("https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20200920.zip", "2020-09-20", True)],
    2022: [("https://dait.interno.gov.it/documenti/opendata/referendum/referendum-20220612.zip", "2022-06-12", True)],
}

COL_MAP: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^REGIONE$", re.I), "regione"),
    (re.compile(r"^PROV(INCIA)?$", re.I), "provincia"),
    (re.compile(r"^COMUNE$", re.I), "comune"),
    (re.compile(r"^(ELETTORI_UOMINI|ELETTORI_MASCHI|ELETTORIMASCHI|ELETTORI MASCHI)$", re.I), "elettori_uomini"),
    (re.compile(r"^(ELETTORI(TOT)?|ELETTORITOTALI)$", re.I), "elettori"),
    (re.compile(r"^(VOTANTI_UOMINI|VOTANTI_MASCHI|VOTANTIMASCHI|VOTANTI MASCHI)$", re.I), "votanti_uomini"),
    (re.compile(r"^(VOTANTI(TOT)?|NUMVOTANTITOTALI)$", re.I), "votanti"),
    (re.compile(r"^(VOTI_SI|VOTISI|NUMVOTISI)$", re.I), "voti_si"),
    (re.compile(r"^(VOTI_NO|VOTINO|NUMVOTINO)$", re.I), "voti_no"),
    (re.compile(r"^(SCHEDE_NULLE|SCHEDENULLE)$", re.I), "schede_nulle"),
    (re.compile(r"^(SCHEDE_BIANCHE|SKBIANCHE|SCHEDEBIANCHE)$", re.I), "schede_bianche"),
    (re.compile(r"^(SCHEDE_CONTESTATE|SCHEDECONTESTATE)$", re.I), "schede_contestate"),
    (re.compile(r"^(NUM_REFERENDUM|NUMREFERENDUM|N_QUESITO)$", re.I), "num_quesito"),
    (re.compile(r"^QUESITO$", re.I), "descrizione_quesito"),
    (re.compile(r"^DESCR_REFERENDUM$", re.I), "descrizione_quesito"),
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


def process_zip(url: str, election_date: str) -> list[dict]:
    raw = download(url)
    records = []
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        for name in zf.namelist():
            base = os.path.basename(name)
            if base.startswith("~") or base.startswith("."):
                continue
            if not base.lower().endswith(".csv") and not base.lower().endswith(".txt"):
                continue
            if "votanti" in base.lower():
                continue
            content = zf.read(name)
            decoded = smart_decode(content)
            rows = parse_csv(decoded)
            if not rows:
                continue
            header = rows[0]
            col_names, col_indices = normalize_columns(header)
            if not col_names:
                continue
            for row in rows[1:]:
                if not row or not any(cell.strip() for cell in row):
                    continue
                rec = {"data_elezione": election_date}
                for cname, idx in zip(col_names, col_indices):
                    if idx < len(row):
                        val = row[idx].strip().strip('"')
                        if cname in ("elettori", "elettori_uomini", "votanti", "votanti_uomini",
                                      "voti_si", "voti_no", "schede_nulle", "schede_bianche",
                                      "schede_contestate", "num_quesito"):
                            val = normalize_number(val)
                        rec[cname] = val
                records.append(rec)
    return records


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2022
    output = sys.argv[2] if len(sys.argv) > 2 else "raw_input.csv"

    sources = SOURCES.get(year)
    if not sources:
        print(f"Nessuna fonte configurata per l'anno {year}", file=sys.stderr)
        sys.exit(1)

    all_records: list[dict] = []
    for url, election_date, is_zip in sources:
        print(f"  {election_date} -> download...", file=sys.stderr)
        records = process_zip(url, election_date)
        print(f"    {len(records)} righe", file=sys.stderr)
        all_records.extend(records)

    if not all_records:
        print("Nessun dato estratto!", file=sys.stderr)
        sys.exit(1)

    canonical_cols = [
        "data_elezione", "data_elezione_raw", "tipo_elezione",
        "regione", "provincia", "comune", "sezione",
        "num_quesito", "quesito",
        "elettori", "elettori_uomini",
        "votanti", "votanti_uomini",
        "voti_si", "voti_no",
        "schede_nulle", "schede_bianche", "schede_contestate",
    ]
    for rec in all_records:
        for col in canonical_cols:
            rec.setdefault(col, "")

    seen = set()
    for rec in all_records:
        for k in rec:
            seen.add(k)
    fieldnames = sorted(seen)

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(all_records)

    print(f"Fatto: anno={year} totale={len(all_records)} righe -> {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
