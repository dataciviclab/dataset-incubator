#!/usr/bin/env python3
"""Scarica e normalizza i CSV delle elezioni regionali da Eligendo.

Uso: python preprocess.py <anno> <output.csv>

Scarica ZIP/CSV da Eligendo per l'anno specificato, estrae il file scrutini,
normalizza colonne e numeri, e produce un CSV unico con schema standard.
"""

import sys
import csv
import io
import os
import re
import zipfile
import urllib.request

# ── mappa anni → lista di (url, data_elezione, is_zip) ──────────────────
SOURCES: dict[int, list[tuple[str, str, bool]]] = {
    2018: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20180304.zip",
            "2018-03-04",
            True,
        ),
    ],
    2019: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20190210.zip",
            "2019-02-10",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20190324.zip",
            "2019-03-24",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20190526.zip",
            "2019-05-26",
            True,
        ),
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20191027.zip",
            "2019-10-27",
            True,
        ),
    ],
    2020: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20200126.zip",
            "2020-01-26",
            True,
        ),
        # 2020-09-20 escluso: file XLSX non gestiti
    ],
    2021: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20211003.zip",
            "2021-10-03",
            True,
        ),
    ],
    2023: [
        (
            "https://dait.interno.gov.it/documenti/opendata/catalogoagid/regionali-20230212.csv",
            "2023-02-12",
            False,
        ),
    ],
    2024: [
        (
            "https://dait.interno.gov.it/documenti/opendata/regionali/regionali-20240609.zip",
            "2024-06-09",
            True,
        ),
    ],
}


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def normalize_number(val: str) -> str:
    """Normalizza numero: rimuovi punti migliaia, trasforma virgola in punto.
    Esempi: '1.234,56' → '1234.56', '5849,00' → '5849', '1234' → '1234'"""
    val = val.strip().strip('"')
    if not val or val in ("***", "-"):
        return ""
    if "," in val:
        val = val.replace(".", "").replace(",", ".")
        # Se era intero con virgola (.00), rimuovi la parte decimale
        if val.endswith(".0"):
            val = val[:-2]
    else:
        val = val.replace(".", "")
    return val


def smart_decode(data: bytes) -> str:
    """Decode bytes tentando UTF-8 prima, poi latin-1/ISO-8859-1."""
    for enc in ("utf-8-sig", "utf-8", "iso-8859-1", "cp1252"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def extract_scrutini_from_zip(raw: bytes, election_date: str) -> list[list[str]]:
    """Estrae il file scrutini da uno ZIP Eligendo.
    Cerca il file che NON si chiama 'Preferenze*' o 'CandidatiLista*'."""
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        # Trova il file scrutini (non preferenze)
        scrutini_name = None
        for name in zf.namelist():
            base = os.path.basename(name)
            if base.startswith("~") or base.startswith("."):
                continue
            if "preferenze" not in base.lower() and "candidatilista" not in base.lower():
                scrutini_name = name
                break
        if scrutini_name is None:
            # fallback: prendi il primo file non-directory
            for name in zf.namelist():
                if not name.endswith("/"):
                    scrutini_name = name
                    break
        if scrutini_name is None:
            raise ValueError(f"Nessun file trovato nello ZIP per {election_date}")

        content = zf.read(scrutini_name)
        decoded = smart_decode(content)
    return parse_csv(decoded)


def parse_csv(content: str) -> list[list[str]]:
    reader = csv.reader(io.StringIO(content), delimiter=";")
    return [row for row in reader if any(cell.strip() for cell in row)]


# ── Mappa normalizzazione colonne ───────────────────────────────────────
# (pattern nel nome colonna → nome normalizzato)
COL_MAP: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^REG(IONE)?$", re.I), "regione"),
    (re.compile(r"^CIRC(OSCR(IZIONE)?)?$", re.I), "circoscrizione"),
    (re.compile(r"^PROV(INCIA)?$", re.I), "provincia"),
    (re.compile(r"^COMUNE$", re.I), "comune"),
    (re.compile(r"^(ELETTORI(TOT)?)$", re.I), "elettori"),
    (re.compile(r"^(VOTANTI(TOT)?)$", re.I), "votanti"),
    (re.compile(r"^(SCHEDE_BIANCHE|SKBIANCHE)$", re.I), "schede_bianche"),
    (re.compile(r"^(COGNOME|COGNOME_CANDIDATO)$", re.I), "cognome"),
    (re.compile(r"^(NOME|NOME_CANDIDATO)$", re.I), "nome"),
    (re.compile(r"^(LISTA|DESCRLISTA)$", re.I), "lista"),
    (re.compile(r"^(VOTI_LISTA|VOTILISTA)$", re.I), "voti_lista"),
    (re.compile(r"^(VOTI_CAND(IDATO)?|VOTICAND(IDATO)?)$", re.I), "voti_candidato"),
]


def normalize_columns(header: list[str]) -> tuple[list[str], list[int]]:
    """Mappa le colonne raw ai nomi standard.
    Restituisce (nomi_normalizzati, indici_validi)."""
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


def process_url(url: str, election_date: str, is_zip: bool) -> list[dict]:
    """Scarica e normalizza un file da Eligendo. Restituisce lista di dict."""
    raw = download(url)
    if is_zip:
        raw_rows = extract_scrutini_from_zip(raw, election_date)
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
                # Normalizza campi numerici
                if name in (
                    "elettori",
                    "votanti",
                    "schede_bianche",
                    "voti_lista",
                    "voti_candidato",
                ):
                    val = normalize_number(val)
                rec[name] = val
        # Unisci cognome + nome in 'candidato'
        if "cognome" in rec and "nome" in rec:
            rec["candidato"] = f"{rec.pop('cognome', '')} {rec.pop('nome', '')}".strip()
        records.append(rec)

    return records


def main():
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2023
    output = sys.argv[2] if len(sys.argv) > 2 else "raw_input.csv"

    sources = SOURCES.get(year)
    if not sources:
        print(f"Nessuna fonte configurata per l'anno {year}", file=sys.stderr)
        sys.exit(1)

    all_records: list[dict] = []
    for url, election_date, is_zip in sources:
        print(f"  {election_date} → download...", file=sys.stderr)
        records = process_url(url, election_date, is_zip)
        print(f"    {len(records)} righe", file=sys.stderr)
        all_records.extend(records)

    if not all_records:
        print("Nessun dato estratto!", file=sys.stderr)
        sys.exit(1)

    # Ricava header da tutti i record
    fieldnames = list(all_records[0].keys())

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(all_records)

    print(f"✅ Fatto: anno={year} totale={len(all_records)} righe → {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
