#!/usr/bin/env python3
"""MinLavoro deposito contratti: normalizza le agevolazioni → raw.csv long.

Fonte primaria: CSV in data/deposito/. Fallback OData.

Schema:
    tabella_id, tipo_agevolazione, regione, mese, settore,
    tipologia_contratto, categoria, indicatore, anno, valore

Uso:
    python3 extract.py <output.csv>
"""

from __future__ import annotations

import csv
import json
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCAL_DEP = HERE / "data" / "deposito"

BASE_URL = "https://dati.lavoro.gov.it"
CATALOG_URL = f"{BASE_URL}/api/core/Nodes/1/Catalog"
NODE_ID = 1
HEADERS = {"Accept": "application/json", "User-Agent": "DataCivicLab/1.0"}
GROUP_PREFIX = "Deposito contratti"

FIELDNAMES = [
    "tabella_id",
    "tipo_agevolazione",
    "regione",
    "mese",
    "settore",
    "tipologia_contratto",
    "categoria",
    "indicatore",
    "anno",
    "valore",
]


def _norm_col(name: str) -> str:
    n = name.strip().lower()
    mapping = {
        "regione": "regione",
        "mese": "mese",
        "settore": "settore",
        "ripartizione_geografica": "ripartizione",
        "tipologia_di_contratto": "tipologia_contratto",
        "altre_agevolazioni": "categoria",
        "detassazione": "categoria",
        "obiettivi": "categoria",
        "indicatore": "indicatore",
        "anno": "anno",
        "osservazione": "valore",
    }
    return mapping.get(n, n)


def _parse_anno(val: str | None) -> int | None:
    if not val:
        return None
    s = val.strip()
    if not s:
        return None
    try:
        return int(s[:4])
    except ValueError:
        return None


def _derive_tipo(text: str) -> str:
    t = text.lower().replace("_", " ")
    if "decontribuzione" in t and "detassazione" in t:
        return "decontribuzione_detassazione"
    if "decontribuzione" in t:
        return "decontribuzione"
    if "detassazione" in t:
        return "detassazione"
    if "altre" in t:
        return "altre_agevolazioni"
    return "altro"


def _filename_to_tabella_id(filename: str) -> str:
    stem = Path(filename).stem.lower()
    slug = (
        stem.replace("distribuzione_regionale_delle_dichiarazioni_di_", "")
        .replace("distribuzione_territoriale_dei_contratti_attivi_di_", "")
        .replace("numero_delle_dichiarazioni_di_", "")
        .replace("distribuzione_dei_contratti_attivi_di_", "")
        .replace("_ai_fini_della_detassazione", "")
        .replace("_per_obiettivi", "")
    )
    return slug[:60]


def normalize_row(row: dict, tabella_id: str, tipo: str) -> dict | None:
    mapped: dict[str, str | None] = {}
    for col, val in row.items():
        key = _norm_col(col)
        if val is not None and str(val).strip() != "":
            mapped[key] = str(val).strip()

    raw_val = mapped.get("valore")
    if raw_val is None:
        return None
    try:
        valore = float(raw_val.replace(",", "."))
    except ValueError:
        return None

    return {
        "tabella_id": tabella_id,
        "tipo_agevolazione": tipo,
        "regione": mapped.get("regione"),
        "mese": mapped.get("mese"),
        "settore": mapped.get("settore"),
        "tipologia_contratto": mapped.get("tipologia_contratto"),
        "categoria": mapped.get("categoria"),
        "indicatore": mapped.get("indicatore"),
        "anno": _parse_anno(mapped.get("anno")),
        "valore": valore,
    }


def read_local_csvs(writer: csv.DictWriter) -> tuple[int, int]:
    n_rows = 0
    n_skipped = 0
    files = sorted(LOCAL_DEP.glob("*.csv"))
    print(f"  Fonte locale: {len(files)} file")
    for f in files:
        tabella_id = _filename_to_tabella_id(f.name)
        tipo = _derive_tipo(f.name)
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    norm = normalize_row(row, tabella_id, tipo)
                    if norm is None:
                        n_skipped += 1
                        continue
                    writer.writerow(norm)
                    n_rows += 1
        except Exception as e:
            print(f"  ERRORE {f.name}: {e}")
    return n_rows, n_skipped


def fetch_json(url: str, retries: int = 3) -> dict:
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
    raise last_err  # type: ignore[misc]


def fetch_odata_rows(pkg_id: str, res_id: str, page_size: int = 100) -> list[dict]:
    all_rows: list[dict] = []
    skip = 0
    while True:
        url = (
            f"{BASE_URL}/api/odata/odata/{NODE_ID}/{pkg_id}/{res_id}/DataRows"
            f"?$top={page_size}&$skip={skip}&$format=json"
        )
        data = fetch_json(url)
        rows = data.get("value", [])
        all_rows.extend(rows)
        if len(rows) < page_size:
            break
        skip += page_size
    return all_rows


def fetch_odata(writer: csv.DictWriter) -> tuple[int, int]:
    catalog = fetch_json(CATALOG_URL)
    packages = catalog.get("packageMap", {})
    targets: list[tuple[str, str, str]] = []
    for pid, pkg in packages.items():
        title = pkg.get("title", pid)
        if not title.startswith(GROUP_PREFIX):
            continue
        odata_res = None
        for rid in pkg.get("resourceIdentifiers", []):
            if rid.startswith("ODATA_"):
                odata_res = rid.replace("ODATA_", "")
                break
        if odata_res is None:
            continue
        targets.append((title, pid, odata_res))

    n_rows = 0
    n_skipped = 0
    for title, pkg_id, res_id in sorted(targets, key=lambda x: x[0]):
        parts = title.split(" - ", 1)
        rest = parts[1] if len(parts) > 1 else title
        tabella_id = _filename_to_tabella_id(rest.lower().replace(" ", "_") + ".csv")
        tipo = _derive_tipo(title)
        try:
            rows = fetch_odata_rows(pkg_id, res_id)
        except Exception as e:
            print(f"  ERRORE: {title[:60]} → {e}")
            continue
        for row in rows:
            norm = normalize_row(row, tabella_id, tipo)
            if norm is None:
                n_skipped += 1
                continue
            writer.writerow(norm)
            n_rows += 1
    return n_rows, n_skipped


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python3 extract.py <output.csv>", file=sys.stderr)
        sys.exit(1)
    out_path = Path(sys.argv[1])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    use_local = LOCAL_DEP.is_dir() and any(LOCAL_DEP.glob("*.csv"))
    print(f"Sorgente: {'CSV locali' if use_local else 'OData API'}")

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        if use_local:
            n_rows, n_skipped = read_local_csvs(writer)
        else:
            n_rows, n_skipped = fetch_odata(writer)

    print(f"Totale: {n_rows} righe → {out_path} ({n_skipped} scartate)")


if __name__ == "__main__":
    main()
