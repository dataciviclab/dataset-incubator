#!/usr/bin/env python3
"""Scarica e normalizza i CSV delle elezioni europee da Eligendo.

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
    1979: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-19790610.zip", "1979-06-10", True)],
    1984: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-19840617.zip", "1984-06-17", True)],
    1989: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-19890618.zip", "1989-06-18", True)],
    1994: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-19940612.zip", "1994-06-12", True)],
    1999: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-19990613.zip", "1999-06-13", True)],
    2004: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-20040612.zip", "2004-06-13", True)],
    2009: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-20090607.zip", "2009-06-07", True)],
    2014: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-20140525.zip", "2014-05-25", True)],
    2019: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-20190526.zip", "2019-05-26", True)],
    2024: [("https://dait.interno.gov.it/documenti/opendata/europee/europee-20240609.zip", "2024-06-09", True)],
}

COL_MAP: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^(CIRC(OSCR(IZIONE)?)?|DESCRCIRC|DESCCIRCEUROPEA)$", re.I), "circoscrizione"),
    (re.compile(r"^(REG(IONE)?|DESCRREG|DESCREGIONE)$", re.I), "regione"),
    (re.compile(r"^(PROV(INCIA)?|DESCRPROV|DESCPROVINCIA)$", re.I), "provincia"),
    (re.compile(r"^(COMUNE|DESCRCOMUNE|DESCCOMUNE)$", re.I), "comune"),
    (re.compile(r"^SEZ(IONE)?$", re.I), "sezione"),
    (re.compile(r"^(NUM_LISTA|NUMERO_LISTA)$", re.I), "num_lista"),
    (re.compile(r"^(LISTA|DESCR_LISTA|DESCRLISTA|DESCLISTA)$", re.I), "lista"),
    (re.compile(r"^(VOTI_LISTA|VOTILISTA|NUMVOTI)$", re.I), "voti_lista"),
    (re.compile(r"^(ELETTORI(TOT)?|ELETTORITOTALI)$", re.I), "elettori"),
    (re.compile(r"^(ELETTORI_MASCHI|ELETTORIMASCHI|ELETTORI UOMINI|ELETTORI_M)$", re.I), "elettori_maschi"),
    (re.compile(r"^(VOTANTI(TOT)?|NUMVOTANTITOTALI)$", re.I), "votanti"),
    (re.compile(r"^(VOTANTI_MASCHI|VOTANTIMASCHI|VOTANTI UOMINI|VOTANTI_M)$", re.I), "votanti_maschi"),
    (re.compile(r"^(SCHEDEBIANCHE|SKBIANCHE|SCHEDE_BIANCHE|NUMSCHEDEBIANCHE)$", re.I), "schede_bianche"),
    (re.compile(r"^DATA_ELEZIONE$", re.I), "data_elezione_raw"),
    (re.compile(r"^TIPO_ELEZIONE$", re.I), "tipo_elezione"),
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


def extract_scrutini(zf: zipfile.ZipFile) -> list[list[str]]:
    candidates = []
    for name in zf.namelist():
        base = os.path.basename(name)
        if base.startswith("~") or base.startswith("."):
            continue
        if "preferenze" in base.lower() or "fuorisede" in base.lower() or "fuori" in base.lower():
            continue
        if base.lower().endswith(".xlsx") or base.lower().endswith(".xls"):
            continue
        if "votanti" in base.lower():
            continue
        candidates.append(name)
    # Prefer LivComune (comune-level) over SEZIONI (sezione-level)
    commune_files = [n for n in candidates if "livcomune" in n.lower() or "liv_comune" in n.lower()]
    if commune_files:
        name = commune_files[0]
    else:
        name = candidates[0] if candidates else None
    if name is None:
        return []
    content = zf.read(name)
    decoded = smart_decode(content)
    return parse_csv(decoded)


def process_url(url: str, election_date: str, is_zip: bool) -> list[dict]:
    raw = download(url)
    if is_zip:
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            raw_rows = extract_scrutini(zf)
    else:
        raw_rows = parse_csv(smart_decode(raw))

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
                if name in ("voti_lista", "elettori", "elettori_maschi",
                            "votanti", "votanti_maschi", "schede_bianche",
                            "num_lista", "sezione"):
                    val = normalize_number(val)
                rec[name] = val
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
        records = process_url(url, election_date, is_zip)
        print(f"    {len(records)} righe", file=sys.stderr)
        all_records.extend(records)

    if not all_records:
        print("Nessun dato estratto!", file=sys.stderr)
        sys.exit(1)

    canonical_cols = [
        "data_elezione", "data_elezione_raw", "tipo_elezione",
        "circoscrizione", "regione", "provincia", "comune", "sezione",
        "num_lista", "lista", "voti_lista",
        "elettori", "elettori_maschi", "votanti", "votanti_maschi",
        "schede_bianche",
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
