"""Preprocess MASE SISEN — gas naturale distribuito per provincia.

Scarica tutti i documenti della cartella CMIS `gas_naturale/consumi/provinciali`
e produce un unico `raw_input.csv` wide:
`anno,regione,provincia,industriale,termoelettrico,reti`.

Fonti: ``Gas_Distribuito_Province_YYYY.xls(x)`` (2004-2025), un file per anno.

Layout (stabile tra le ere, cambiano solo foglio e formato):
- riga titolo (``GAS NATURALE TOTALE DISTRIBUITO PER PROVINCIA`` / ``ANNO YYYY``)
- riga intestazione: ``REGIONE | PROVINCIA | INDUSTRIALE | <spacer> | TERMOELETTRICO |
  RETI DI DISTRIBUZIONE | TOTALE GENERALE``
- righe provincia (colonna REGIONE vuota)
- una riga ``TOTALE`` **per regione**, con il nome della regione in colonna 0:
  le province di una regione sono quelle che *precedono* la sua riga ``TOTALE``.
- la colonna spacer è sempre 0: scartata
- la riga finale di fonte/testo è ignorata

Unità: M Sm3 (milioni di Sm3).
"""

from __future__ import annotations

import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

API = "https://sisen.mase.gov.it/dgsaie/api/v1"
FOLDER = "/sg_dgsaie/gas_naturale/consumi/provinciali"
TIMEOUT = 180

YEAR_RE = re.compile(r"_(\d{4})\.xls[x]?$", re.IGNORECASE)
TOTALE_PREFIX = "TOTALE"
JUNK_PREFIXES = ("ELABORAZIONE", "FONTE", "MINISTERO", "*", "(*)")
COL_REGIONE, COL_PROVINCIA = 0, 1
COL_INDUSTRIALE, COL_TERMOELETTRICO, COL_RETI = 2, 4, 5


def _fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
        return response.read()


def _list_documents() -> list[dict]:
    url = f"{API}/cmis/documents?folder={urllib.parse.quote(FOLDER)}"
    payload = json.loads(_fetch(url).decode("utf-8"))
    return payload if isinstance(payload, list) else []


def _engine(file_name: str) -> str:
    return "xlrd" if file_name.lower().endswith(".xls") else "openpyxl"


def _to_float(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and not pd.isna(value):
        return float(value)
    return None


def _is_junk(label) -> bool:
    text = re.sub(r"\s+", " ", str(label)).strip().upper()
    return not text or text.startswith(JUNK_PREFIXES)


def _parse(data: bytes, file_name: str, anno: int) -> list[tuple]:
    sheets = pd.read_excel(
        io.BytesIO(data), sheet_name=None, header=None, engine=_engine(file_name)
    )
    rows: list[tuple] = []
    for frame in sheets.values():
        header_idx = None
        for i in range(min(15, len(frame))):
            labels = {str(v).strip().upper() for v in frame.iloc[i].tolist() if isinstance(v, str)}
            if "PROVINCIA" in labels and "REGIONE" in labels:
                header_idx = i
                break
        if header_idx is None:
            continue

        block: list[tuple] = []
        for r in range(header_idx + 1, len(frame)):
            provincia = frame.iat[r, COL_PROVINCIA]
            regione = frame.iat[r, COL_REGIONE]
            if not isinstance(provincia, str) or not provincia.strip():
                continue
            if _is_junk(provincia):
                # riga di fonte/testo a piè di foglio
                continue
            if provincia.strip().upper().startswith(TOTALE_PREFIX):
                nome_regione = str(regione).strip() if isinstance(regione, str) else None
                if _is_junk(nome_regione):
                    nome_regione = None
                rows.extend((anno, nome_regione, p, ind, ter, ret) for p, ind, ter, ret in block)
                block = []
                continue
            ind = _to_float(frame.iat[r, COL_INDUSTRIALE])
            ter = _to_float(frame.iat[r, COL_TERMOELETTRICO])
            ret = _to_float(frame.iat[r, COL_RETI])
            if ind is None and ter is None and ret is None:
                # riga senza dati (piè di foglio)
                continue
            block.append((provincia.strip(), ind, ter, ret))
        rows.extend((anno, None, p, ind, ter, ret) for p, ind, ter, ret in block)
    return rows


def main() -> None:
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv")
    documents = _list_documents()

    docs: list[tuple[int, dict]] = []
    for doc in documents:
        match = YEAR_RE.search(doc["fileName"])
        if match:
            docs.append((int(match.group(1)), doc))
    if not docs:
        raise SystemExit("nessun file provinciale trovato nella cartella CMIS")
    docs.sort(key=lambda item: item[0])

    rows: list[tuple] = []
    for anno, doc in docs:
        data = _fetch(f"{API}/cmis/documents/{doc['id']}")
        parsed = _parse(data, doc["fileName"], anno)
        rows.extend(parsed)
        regioni = len({r[1] for r in parsed if r[1]})
        print(
            f"  {doc['fileName']}: {len(parsed)} righe, {regioni} regioni",
            file=sys.stderr,
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        import csv

        writer = csv.writer(handle)
        writer.writerow(["anno", "regione", "provincia", "industriale", "termoelettrico", "reti"])
        for row in rows:
            writer.writerow(["" if v is None else v for v in row])

    anni = sorted({r[0] for r in rows})
    print(
        f"raw_input.csv: {len(rows)} righe, anni {anni[0]}-{anni[-1]}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
