"""Preprocess MASE SISEN — consumi petroliferi (dati definitivi).

Scarica tutti i documenti della cartella CMIS `consumi_petroliferi/definitivi`
e produce un unico `raw_input.csv` lungo:
`anno,prodotto,dettaglio,mese,consumo_kt`.

Fonti: ``Consumi_Petroliferi_Definitivi_YYYY.xls(x)`` (2002-2025), un file per anno.

Layout (stabile; variano foglio, formato e righe di titolo):
- riga titolo ``CONSUMI PETROLIFERI  ANNO YYYY``
- riga ``I° SEMESTRE`` / ``2°SEMESTRE``
- riga intestazione: ``PRODOTTO | <dettaglio> | GEN. | FEB. | GEN.FEB | …``
- due blocchi affiancati (I° a sinistra, II° a destra), ciascuno con la propria
  colonna PRODOTTO; le colonne **cumulative** (``GEN.FEB``, ``GEN.MAR``, …) sono ignorate
- il nome prodotto è solo sulla prima riga del blocco; le righe successive hanno
  celle vuote o i marcatori ``DI CUI:`` / ``=`` → forward-fill che li ignora

Colonne mese (0-based): 2,3,5,7,9,11 (GEN..GIU) e 15,17,19,21,23,25 (LUG..DIC).
Il parser individua la riga di intestazione invece di assumerne l'offset.

Unità: migliaia di tonnellate (,000 tonn.).
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

API = "https://sisen.mase.gov.it/dgsaie/api/v1"
FOLDER = "/sg_dgsaie/consumi_petroliferi/definitivi"
TIMEOUT = 180

YEAR_RE = re.compile(r"_(\d{4})\.xls[x]?$", re.IGNORECASE)
TITLE_YEAR_RE = re.compile(r"CONSUMI\s+PETROLIFERI\s+ANNO\s+(\d{4})", re.IGNORECASE)
MARKERS = ("DI CUI", "=")
MONTH_COLUMNS = [
    (1, 2),
    (2, 3),
    (3, 5),
    (4, 7),
    (5, 9),
    (6, 11),
    (7, 15),
    (8, 17),
    (9, 19),
    (10, 21),
    (11, 23),
    (12, 25),
]
JUNK_PREFIXES = ("FONTE", "MINISTERO", "ELABORAZIONE", "*", "(*)", "CONSUMI E PERDITE")

# Le etichette prodotto cambiano tra le ere (abbreviazioni, refusi, marcatori nota).
PRODUCT_ALIAS = {
    "BENZINA": "benzina",
    "CARBOT.": "carboturbo",
    "CARBOTURBO": "carboturbo",
    "GASOLIO": "gasolio",
    "OLIO COMB.": "olio combustibile",
    "OLIO COMB.LE": "olio combustibile",
    "OLIO COMBUSTIBILE": "olio combustibile",
    "G.P.L.": "gpl",
    "GPL": "gpl",
    "LUBRIFICANTI TOTALE": "lubrificanti",
    "BITUMI": "bitumi",
    "TOTALE PRODOTTI PRINCIPALI": "totale prodotti principali",
}
# Varianti della riga di totale per prodotto.
DETAIL_TOTALE = {"TOTALE", "TOTALE (A)", "TOTALE GASOLI", "T O T A L E"}


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


def _clean_label(value) -> str | None:
    if not isinstance(value, str):
        return None
    text = re.sub(r"\(\*+\)", "", value)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def _is_product(label: str) -> bool:
    upper = label.upper()
    if upper.startswith(JUNK_PREFIXES):
        return False
    return not any(upper.startswith(marker) for marker in MARKERS)


def _header_index(frame) -> int | None:
    for i in range(min(12, len(frame))):
        labels = [str(v).strip().upper() for v in frame.iloc[i].tolist() if isinstance(v, str)]
        if "PRODOTTO" in labels and any(label.startswith("GEN") for label in labels):
            return i
    return None


def _sheet_year(frame) -> int | None:
    for i in range(min(6, len(frame))):
        for value in frame.iloc[i].tolist():
            if isinstance(value, str):
                match = TITLE_YEAR_RE.search(value)
                if match:
                    return int(match.group(1))
    return None


def _parse(data: bytes, file_name: str) -> list[tuple]:
    sheets = pd.read_excel(
        io.BytesIO(data), sheet_name=None, header=None, engine=_engine(file_name)
    )
    rows: list[tuple] = []
    for frame in sheets.values():
        header_idx = _header_index(frame)
        if header_idx is None:
            continue
        anno = _sheet_year(frame)
        if anno is None:
            continue
        prodotto = None
        for r in range(header_idx + 1, len(frame)):
            label = _clean_label(frame.iat[r, 0])
            if label and _is_product(label):
                prodotto = PRODUCT_ALIAS.get(label.upper(), label.lower())
            if prodotto is None:
                continue
            dettaglio = _clean_label(frame.iat[r, 1])
            if dettaglio:
                if any(dettaglio.upper().startswith(marker) for marker in MARKERS):
                    dettaglio = None
                elif dettaglio.upper() in DETAIL_TOTALE:
                    dettaglio = "TOTALE"
            for mese, column in MONTH_COLUMNS:
                value = _to_float(frame.iat[r, column])
                if value is not None:
                    rows.append((anno, prodotto, dettaglio, mese, value))
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
        raise SystemExit("nessun file dei consumi petroliferi trovato")
    docs.sort(key=lambda item: item[0])

    rows: list[tuple] = []
    for anno_file, doc in docs:
        data = _fetch(f"{API}/cmis/documents/{doc['id']}")
        parsed = _parse(data, doc["fileName"])
        # Alcuni file contengono più anni in fogli diversi (es. 2023 → 2021, 2022, 2023):
        # tengo solo le righe dell'anno del file, per non duplicare le serie.
        own = [r for r in parsed if r[0] == anno_file]
        kept = own or parsed
        rows.extend(kept)
        extra = sorted({r[0] for r in parsed} - {anno_file})
        note = f" (fogli extra: {extra} scartati)" if extra else ""
        print(
            f"  {doc['fileName']}: {len(kept)} righe, {len({r[1] for r in kept})} prodotti{note}",
            file=sys.stderr,
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["anno", "prodotto", "dettaglio", "mese", "consumo_kt"])
        for anno, prodotto, dettaglio, mese, value in rows:
            writer.writerow([anno, prodotto, dettaglio or "", mese, value])

    anni = sorted({r[0] for r in rows})
    print(
        f"raw_input.csv: {len(rows)} righe, anni {anni[0]}-{anni[-1]}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
