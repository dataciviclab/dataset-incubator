#!/usr/bin/env python3
"""Scarica e normalizza il CSV adempimenti MEF per un anno.

Normalizza le differenze di encoding tra anni (latin-1 vs utf-8)
e unifica i nomi delle colonne tra anni diversi."""

import csv
import io
import sys
from pathlib import Path

from lab_connectors.http import download

URL_TEMPLATE = "https://www.de.mef.gov.it/modules/documenti_it/attivo_patrimonio/immobili_{year}/Dati_Adempimento_Anno_{year}.csv"

COLUMN_MAP = {
    "Settore Istituzionale": "Settore Istituzionale",
    "Macrocategoria Amministrazione": "Macrocategoria Amministrazione",
    "Tipologia Amministrazione": "Tipologia Amministrazione",
    "Amministrazione Denominazione": "Amministrazione Denominazione",
    "Amministrazione Codice Fiscale": "Amministrazione Codice Fiscale",
    "Regione (Amministrazione)": "Regione (Amministrazione)",
    "Provincia (Amministrazione)": "Provincia (Amministrazione)",
    "Comune (Amministrazione)": "Comune (Amministrazione)",
    "Cod. Comune (Amministrazione)": "Cod. Comune (Amministrazione)",
    "Numero beni in proprietà": "Numero beni in proprieta'",
    "Numero beni in proprieta'": "Numero beni in proprieta'",
    "Numero beni in detenzione": "Numero beni in detenzione",
    "Dichiarazione negativa": "Dichiarazione negativa",
    "Dich. di completezza dei dati": "Dich. di completezza dei dati",
    "Invio comunicazione": "Invio comunicazione",
    "Obbligo di comunicazione": "Obbligo di comunicazione",
    "Nome sezione": "Nome sezione",
    "Nome file Beni Immobili Dichiarati": "Nome file Beni Immobili Dichiarati",
    "Nome file Detenzioni a favore di terzi": "Nome file Detenzioni a favore di terzi",
}


def detect_encoding(data: bytes) -> str:
    try:
        data.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"


def _canonical_columns() -> list[str]:
    seen = set()
    result = []
    for v in COLUMN_MAP.values():
        if v not in seen:
            seen.add(v)
            result.append(v)
    return result


def main():
    if len(sys.argv) < 3:
        print("Usage: preprocess.py <year> <output_path>", file=sys.stderr)
        sys.exit(1)

    year = sys.argv[1]
    output_path = Path(sys.argv[2])

    url = URL_TEMPLATE.format(year=year)
    print(f"[preprocess enti] Download {url}", file=sys.stderr)
    raw = download(url)

    encoding = detect_encoding(raw)
    print(f"[preprocess enti] Encoding rilevato: {encoding}", file=sys.stderr)

    text = raw.decode(encoding)
    reader = csv.DictReader(io.StringIO(text), delimiter=";")

    out_columns = _canonical_columns()
    with open(output_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=out_columns, delimiter=";")
        writer.writeheader()

        for row in reader:
            out_row = {}
            for src_col, dst_col in COLUMN_MAP.items():
                if src_col in row and row[src_col].strip():
                    out_row[dst_col] = row[src_col]
                elif dst_col not in out_row or not out_row[dst_col]:
                    out_row.setdefault(dst_col, row.get(src_col, ""))
            writer.writerow(out_row)

    print(f"[preprocess enti] Fatto: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
