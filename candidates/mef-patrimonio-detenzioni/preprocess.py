#!/usr/bin/env python3
"""Scarica, estrae e unisce tutti i 31 ZIP Det_* per un dato anno."""

import csv
import io
import sys
import zipfile
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

MEF_BASE = (
    "https://www.de.mef.gov.it/modules/documenti_it/attivo_patrimonio/immobili_{year}/opendata_det/"
)
ADEMPIMENTI_URL = "https://www.de.mef.gov.it/modules/documenti_it/attivo_patrimonio/immobili_{year}/Dati_Adempimento_Anno_{year}.csv"

COLUMNS = [
    "ID variazione",
    "Settore Istituzionale",
    "Macrocategoria Amministrazione",
    "Tipologia Amministrazione",
    "Amministrazione Denominazione",
    "Amministrazione Codice Fiscale",
    "Regione (Amministrazione)",
    "Provincia (Amministrazione)",
    "Comune (Amministrazione)",
    "Cod. Comune (Amministrazione)",
    "Tipo detenzione a terzi",
    "Detenzione Intera UI",
    "Superficie in detenzione",
    "Canone annuale",
    "Data decorrenza",
    "Data scadenza",
    "Sogg. ricevente (tipo)",
    "Sogg. ricevente (denominaz.)",
    "Sogg. ricevente (CF)",
    "Soggetto ricevente PA",
    "Finalità PF",
    "ID bene",
    "Natura del bene",
    "Tipologia Bene Immobile",
    "Superficie di Riferimento (mq)",
]


def _zip_variants(csv_name: str) -> list[str]:
    base = csv_name.replace(".csv", ".zip").replace(" ", "-")
    variants = [base]
    if "'" in base:
        variants.append(base.replace("'", "_"))
        variants.append(base.replace("'", ""))
    return variants


def _try_download(zip_name: str, year: str, dest: Path) -> bool:
    for variant in _zip_variants(zip_name.replace(".csv", ".zip")):
        url = MEF_BASE.format(year=year) + quote(variant)
        try:
            with urlopen(url, timeout=120) as resp:
                dest.write_bytes(resp.read())
            return True
        except Exception:
            continue
    return False


def main():
    if len(sys.argv) < 3:
        print("Usage: preprocess.py <year> <output_path>", file=sys.stderr)
        sys.exit(1)

    year = sys.argv[1]
    output_path = Path(sys.argv[2])
    cache_dir = Path(__file__).resolve().parent / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    ademp_url = ADEMPIMENTI_URL.format(year=year)
    print(f"[preprocess] Download adempimenti: {ademp_url}", file=sys.stderr)
    with urlopen(ademp_url) as resp:
        raw = resp.read()
    try:
        ademp_raw = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        ademp_raw = raw.decode("latin-1")

    reader = csv.DictReader(io.StringIO(ademp_raw), delimiter=";")
    csv_names = set()
    col_name = "Nome file Detenzioni a favore di terzi"
    for row in reader:
        fname = row.get(col_name, "").strip()
        if fname:
            csv_names.add(fname)

    print(f"[preprocess] Trovati {len(csv_names)} file ZIP da scaricare", file=sys.stderr)

    total_rows = 0
    with open(output_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=COLUMNS, delimiter=";")
        writer.writeheader()

        for csv_name in sorted(csv_names):
            base_zip = csv_name.replace(".csv", ".zip")
            zip_path = cache_dir / base_zip

            if not zip_path.exists():
                if not _try_download(base_zip, year, zip_path):
                    print(f"[preprocess] ERRORE download {base_zip}, skip", file=sys.stderr)
                    continue

            try:
                with zipfile.ZipFile(zip_path) as zf:
                    inner_csv = csv_name
                    if inner_csv not in zf.namelist():
                        inner_csv = next(n for n in zf.namelist() if n.endswith(".csv"))
                    with zf.open(inner_csv) as f:
                        raw = f.read()
                        try:
                            content = raw.decode("utf-8-sig")
                        except UnicodeDecodeError:
                            content = raw.decode("latin-1")
            except Exception as e:
                print(f"[preprocess] ERRORE lettura {base_zip}: {e}", file=sys.stderr)
                continue

            rows_this = 0
            reader = csv.DictReader(io.StringIO(content), delimiter=";")
            for row in reader:
                writer.writerow(row)
                rows_this += 1
            total_rows += rows_this
            print(
                f"[preprocess] {base_zip}: +{rows_this} righe (tot {total_rows})", file=sys.stderr
            )

    print(f"[preprocess] Fatto: {total_rows} righe scritte in {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
