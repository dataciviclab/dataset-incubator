"""Preprocess MASE SISEN — import di gas naturale per paese di origine.

Scarica tutti i documenti della cartella CMIS `gas_naturale/importazioni` e
produce un unico `raw_input.csv` lungo: `anno,mese,paese_origine,import_msmc`.

Fonti (API CMIS pubblica, nessuna autenticazione):
- ``ImportazioniGasAnnualiPerPaeseDiOrigine_1990-2021.xlsx``  → anni come colonne
- ``ImportazioniGasMensiliPerPaeseDiOrigine_YYYY.xls(x)``     → mesi come colonne

Le due ere hanno layout e **lingua** diversi:
- ``.xls`` (2002-2015): foglio ``Importazioni Paese Origine``; il file 2002-2009
  contiene più blocchi-anno impilati, ciascuno con titolo e intestazione propri.
- ``.xlsx`` (2016+): foglio ``Foglio2``, un anno per file.
Il parser individua le righe-titolo (``IMPORTAZIONI DI GAS NATURALE ... ANNO YYYY``)
e legge da lì: titolo → ``MESE`` → nomi mesi → dati, fino alla riga ``Totale``.

Granularità: **mensile 2002-2024**; per il **1990-2001** (non coperto dai file
mensili) si usa la serie annuale con ``mese`` vuoto.

Unità: M Sm3 (milioni di Sm3).

**Anomalia di unità (2013-2014)**: quei due file hanno il titolo "Miliardi di
standard metri cubi" ma i valori sono in **Sm3 grezzi** (es. RUSSIA gen-2013 =
2.462.201.248, cioè 2,46 miliardi Sm3). Il titolo è errato nella fonte. Il parser
rileva il caso dalla magnitudine del blocco-anno (somma > 500.000) e riscala di
1e-6, loggando la correzione.
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
FOLDER = "/sg_dgsaie/gas_naturale/importazioni"
TIMEOUT = 180

# Etichette paese normalizzate (le ere usano italiano e inglese, con varianti).
ALIAS = {
    # inglese (serie annuale)
    "RUSSIAN FEDERATION": "RUSSIA",
    "NETHERLANDS": "OLANDA",
    "NORWAY": "NORVEGIA",
    "LIBYA": "LIBIA",
    "QATAR": "QATAR",
    "GERMANY": "GERMANIA",
    "CROATIA": "CROAZIA",
    "NIGERIA": "NIGERIA",
    "UNITED KINGDOM": "REGNO UNITO",
    "UNITED STATES": "U.S.A.",
    "TRINIDAD AND TOBAGO": "TRINIDAD",
    "EGYPT": "EGITTO",
    "FRANCE": "FRANCIA",
    "UZBEKISTAN": "UZBEKISTAN",
    "DENMARK": "DANIMARCA",
    "UNITED ARAB EMIRATES": "EMIRATI ARABI UNITI",
    "BELGIUM": "BELGIO",
    "EQUATORIAL GUINEA": "GUINEA EQUATORIALE",
    "PERU": "PERU",
    "ANGOLA": "ANGOLA",
    "CAMEROON": "CAMERUN",
    "SPAIN": "SPAGNA",
    "SLOVENIA": "SLOVENIA",
    "AZERBAIJAN": "AZERBAIGIAN",
    "NOT ELSEWHERE SPECIFIED": "NON SPECIFICATO",
    # varianti italiane storiche
    "QUATAR": "QATAR",
    "UK": "REGNO UNITO",
    "USA": "U.S.A.",
    "TRINIDAD TOBAGO": "TRINIDAD",
    "ALTRI UNIONE EUROPEA": "ALTRI UE",
    "ALRI UE": "ALTRI UE",  # refuso nella fonte
    "ALTRI NON UNIONE EUROPEA": "ALTRI NON UE",
    "ALTRO": "ALTRI NON UE",
    "ALTRI NON UE": "ALTRI NON UE",
    "ALTRI UE": "ALTRI UE",
}

# Soglia per rilevare i file in Sm3 grezzi (2013-2014): somma di un blocco-anno
# ben sopra il massimo storico (~80.000 M Sm3).
RAW_SM3_THRESHOLD = 500_000
RAW_SM3_SCALE = 1e-6

JUNK_PREFIXES = ("FONTE", "*", "(*)")
TOTALE_PREFIXES = ("TOTALE",)
TITLE_RE = re.compile(r"IMPORTAZIONI DI GAS NATURALE.*?ANNO\s+(\d{4})", re.IGNORECASE)


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


def _normalize_country(label) -> str | None:
    text = re.sub(r"\(\*+\)", "", str(label))
    text = re.sub(r"\s+", " ", text).strip().strip("'").strip()
    if not text:
        return None
    upper = text.upper()
    if upper.startswith(JUNK_PREFIXES) or upper.startswith(TOTALE_PREFIXES):
        return None
    return ALIAS.get(upper, upper)


def _scale_block(block: list[tuple[int, int, str, float]], label: str) -> float:
    """Rileva i blocchi-anno in Sm3 grezzi (2013-2014) e restituisce il fattore."""
    total = sum(value for _, _, _, value in block)
    if total > RAW_SM3_THRESHOLD:
        print(
            f"    unità Sm3 rilevata in {label}: somma blocco {total:,.0f} "
            f"-> riscalo x{RAW_SM3_SCALE}",
            file=sys.stderr,
        )
        return RAW_SM3_SCALE
    return 1.0


def _parse_monthly(data: bytes, file_name: str) -> list[tuple[int, int, str, float]]:
    sheets = pd.read_excel(
        io.BytesIO(data), sheet_name=None, header=None, engine=_engine(file_name)
    )
    rows: list[tuple[int, int, str, float]] = []
    for frame in sheets.values():
        titles = [
            i
            for i in range(len(frame))
            if isinstance(frame.iat[i, 0], str) and TITLE_RE.search(str(frame.iat[i, 0]))
        ]
        for title_idx in titles:
            match = TITLE_RE.search(str(frame.iat[title_idx, 0]))
            anno = int(match.group(1))
            block: list[tuple[int, int, str, float]] = []
            for r in range(title_idx + 3, len(frame)):
                label = frame.iat[r, 0]
                if not isinstance(label, str):
                    if r > title_idx + 3:
                        break
                    continue
                if label.strip().upper().startswith(TOTALE_PREFIXES):
                    break
                paese = _normalize_country(label)
                if not paese:
                    continue
                for mese in range(1, 13):
                    value = _to_float(frame.iat[r, mese])
                    if value is not None:
                        block.append((anno, mese, paese, value))
            if not block:
                continue
            scale = _scale_block(block, f"{file_name} ({anno})")
            rows.extend((a, m, p, v * scale) for a, m, p, v in block)
    return rows


def _parse_annual(data: bytes, file_name: str) -> list[tuple[int, None, str, float]]:
    frame = pd.read_excel(io.BytesIO(data), sheet_name=0, header=None, engine=_engine(file_name))
    year_row = None
    for i in range(min(10, len(frame))):
        years = [
            v for v in frame.iloc[i, 1:].tolist() if isinstance(v, (int, float)) and 1900 < v < 2100
        ]
        if len(years) >= 20:
            year_row = i
            break
    if year_row is None:
        raise ValueError(f"riga anni non trovata in {file_name}")

    years = [
        int(v)
        for v in frame.iloc[year_row, 1:].tolist()
        if isinstance(v, (int, float)) and 1900 < v < 2100
    ]
    rows: list[tuple[int, None, str, float]] = []
    for r in range(year_row + 1, len(frame)):
        label = frame.iat[r, 0]
        if not isinstance(label, str):
            continue
        paese = _normalize_country(label)
        if not paese:
            continue
        for offset, year in enumerate(years):
            value = _to_float(frame.iat[r, 1 + offset])
            if value is not None:
                rows.append((year, None, paese, value))
    return rows


def _pick_monthly(documents: list[dict]) -> list[dict]:
    """Un file per anno, preferendo la revisione `_rev1` quando presente."""
    by_year: dict[int, dict] = {}
    for doc in documents:
        name = doc["fileName"]
        match = re.match(r"ImportazioniGasMensiliPerPaeseDiOrigine_(\d{4})", name)
        if not match:
            continue
        year = int(match.group(1))
        current = by_year.get(year)
        if current is None or "_rev1" in name:
            by_year[year] = doc
    return [by_year[y] for y in sorted(by_year)]


def main() -> None:
    output = Path(sys.argv[1] if len(sys.argv) > 1 else "raw_input.csv")
    documents = _list_documents()

    monthly_docs = _pick_monthly(documents)
    annual_docs = [d for d in documents if d["fileName"].startswith("ImportazioniGasAnnuali")]
    if not monthly_docs:
        raise SystemExit("nessun file mensile trovato nella cartella CMIS")

    rows: list[tuple[int, int | None, str, float]] = []
    for doc in monthly_docs:
        data = _fetch(f"{API}/cmis/documents/{doc['id']}")
        rows.extend(_parse_monthly(data, doc["fileName"]))
        print(f"  mensile {doc['fileName']}", file=sys.stderr)

    min_monthly_year = min(r[0] for r in rows)
    for doc in annual_docs:
        data = _fetch(f"{API}/cmis/documents/{doc['id']}")
        annual_rows = _parse_annual(data, doc["fileName"])
        kept = [r for r in annual_rows if r[0] < min_monthly_year]
        rows.extend(kept)
        print(
            f"  annuale {doc['fileName']}: {len(kept)} righe (anni < {min_monthly_year})",
            file=sys.stderr,
        )

    rows.sort(key=lambda r: (r[0], r[1] or 0, r[2]))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        import csv

        writer = csv.writer(handle)
        writer.writerow(["anno", "mese", "paese_origine", "import_msmc"])
        for anno, mese, paese, value in rows:
            writer.writerow([anno, mese if mese is not None else "", paese, value])

    anni = sorted({r[0] for r in rows})
    print(
        f"raw_input.csv: {len(rows)} righe, anni {anni[0]}-{anni[-1]}, "
        f"{len({r[2] for r in rows})} paesi",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
