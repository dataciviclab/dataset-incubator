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
from collections import Counter
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

# Le etichette della fonte cambiano tra gli anni: senza normalizzazione la serie
# di una regione/provincia si spezza in due. Verificato sui dati 2004-2025.
REGION_ALIAS = {
    "ABBRUZZO": "ABRUZZO",  # refuso nella fonte, presente in 11 anni su 22
}
PROVINCE_ALIAS = {
    "MONZA-BRIANZA": "MONZA",  # 2010-2013; dal 2014 la fonte usa "MONZA"
}

# Conteggio province atteso per anno (riorganizzazioni amministrative). Guardia:
# una riga di testo dentro un blocco, o una variante non normalizzata, sposta il
# conteggio e fa fallire il run invece di entrare come provincia a 0,0,0.
EXPECTED_PROVINCES = [
    (2004, 2009, 104),
    (2010, 2013, 106),
    (2014, 2025, 110),
]

# Le 20 regioni attese dopo la normalizzazione. Guardia: se la fonte introduce
# una variante nuova, il run fallisce invece di pubblicare una serie spezzata.
EXPECTED_REGIONS = {
    "ABRUZZO",
    "BASILICATA",
    "CALABRIA",
    "CAMPANIA",
    "EMILIA ROMAGNA",
    "FRIULI VENEZIA GIULIA",
    "LAZIO",
    "LIGURIA",
    "LOMBARDIA",
    "MARCHE",
    "MOLISE",
    "PIEMONTE",
    "PUGLIA",
    "SARDEGNA",
    "SICILIA",
    "TOSCANA",
    "TRENTINO ALTO ADIGE",
    "UMBRIA",
    "VALLE D'AOSTA",
    "VENETO",
}


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


def _normalize_region(label) -> str | None:
    if not isinstance(label, str):
        return None
    text = re.sub(r"\s+", " ", label).strip().upper()
    if not text or text.startswith(JUNK_PREFIXES):
        return None
    return REGION_ALIAS.get(text, text)


def _normalize_province(label) -> str:
    text = re.sub(r"\s+", " ", str(label)).strip().upper()
    return PROVINCE_ALIAS.get(text, text)


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
                nome_regione = _normalize_region(regione)
                rows.extend((anno, nome_regione, p, ind, ter, ret) for p, ind, ter, ret in block)
                block = []
                continue
            # Nella fonte un componente vuoto vale 0: il TOTALE GENERALE della riga
            # è la somma dei componenti non nulli (es. RAGUSA 2013: 14,3 + NULL +
            # 43,2 = 57,5). Coercizione a 0, così le serie non hanno buchi.
            ind = _to_float(frame.iat[r, COL_INDUSTRIALE]) or 0.0
            ter = _to_float(frame.iat[r, COL_TERMOELETTRICO]) or 0.0
            ret = _to_float(frame.iat[r, COL_RETI]) or 0.0
            block.append((_normalize_province(provincia), ind, ter, ret))
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

    # Guardie: senza queste, una variante nuova nella fonte pubblicherebbe una
    # serie regionale spezzata (è successo con ABBRUZZO/ABRUZZO).
    regioni = {r[1] for r in rows}
    if regioni != EXPECTED_REGIONS:
        mancanti = sorted(EXPECTED_REGIONS - regioni)
        inattese = sorted(regioni - EXPECTED_REGIONS)
        raise SystemExit(
            "regioni inattese dopo la normalizzazione: "
            f"mancanti={mancanti} inattese={inattese}. "
            "Aggiungi la variante a REGION_ALIAS se è un refuso della fonte."
        )
    duplicati = sorted(coppia for coppia, n in Counter((r[0], r[2]) for r in rows).items() if n > 1)
    if duplicati:
        raise SystemExit(
            f"province duplicate per anno (variante non normalizzata?): {duplicati[:10]}"
        )

    attesi = {a: n for start, end, n in EXPECTED_PROVINCES for a in range(start, end + 1)}
    province_per_anno: dict[int, set[str]] = {}
    for anno, _, provincia, *_ in rows:
        province_per_anno.setdefault(anno, set()).add(provincia)
    for anno in sorted(province_per_anno):
        atteso = attesi.get(anno)
        if atteso is None:
            raise SystemExit(
                f"anno {anno} non previsto in EXPECTED_PROVINCES: "
                "aggiungi il conteggio atteso dopo aver verificato la fonte"
            )
        trovate = len(province_per_anno[anno])
        if trovate != atteso:
            raise SystemExit(
                f"{anno}: {trovate} province, attese {atteso} — "
                "riga estranea nel blocco o variante non normalizzata?"
            )

    with output.open("w", newline="", encoding="utf-8") as handle:
        import csv

        writer = csv.writer(handle)
        writer.writerow(["anno", "regione", "provincia", "industriale", "termoelettrico", "reti"])
        for row in rows:
            writer.writerow(["" if v is None else v for v in row])

    anni = sorted({r[0] for r in rows})
    print(
        f"raw_input.csv: {len(rows)} righe, anni {anni[0]}-{anni[-1]}, {len(regioni)} regioni",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
