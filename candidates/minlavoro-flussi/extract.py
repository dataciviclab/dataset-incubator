#!/usr/bin/env python3
"""MinLavoro flussi: normalizza Nota trimestrale + Rapporto Annuale → unico raw.csv long.

Fonte dati primaria: CSV in data/nota/ e data/ra/ (legacy fetch_minlavoro.py).
Se assenti, fa fetch OData con retry.

Schema output:

    fonte, tabella_id, tipo_flusso, anno, trimestre,
    geo_level, geo, genere, tipologia_contratto, settore,
    classe_eta, motivo_cessazione, durata_fascia, qualifica,
    indicatore, valore

Uso (toolkit raw source):
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
LOCAL_NOTA = HERE / "data" / "nota"
LOCAL_RA = HERE / "data" / "ra"

BASE_URL = "https://dati.lavoro.gov.it"
CATALOG_URL = f"{BASE_URL}/api/core/Nodes/1/Catalog"
NODE_ID = 1
HEADERS = {"Accept": "application/json", "User-Agent": "DataCivicLab/1.0"}

GROUP_PREFIXES = ("Nota trimestrale", "Rapporto Annuale")

FIELDNAMES = [
    "fonte",
    "tabella_id",
    "tipo_flusso",
    "anno",
    "trimestre",
    "geo_level",
    "geo",
    "genere",
    "tipologia_contratto",
    "settore",
    "classe_eta",
    "motivo_cessazione",
    "durata_fascia",
    "qualifica",
    "indicatore",
    "valore",
]

COL_MAP = {
    "anno": "anno",
    "trimestre": "trimestre",
    "ripartizione_geografica": "geo_rip",
    "regione": "geo_reg",
    "genere": "genere",
    "tipologia_contrattuale": "tipologia_contratto",
    "tipologia_di_contratto": "tipologia_contratto",
    "settore_attivita": "settore",
    "settore_di_attivita": "settore",
    "macro_settore_di_attivi_98f4d271": "macro_settore",
    "qualifica_professionale": "qualifica",
    "motivo_di_cessazione": "motivo_cessazione",
    "macro_motivo_di_cessazi_ad200df4": "macro_motivo",
    "indicatore": "indicatore",
    "osservazione": "valore",
}


def _norm_col(name: str) -> str:
    n = name.strip().lower()
    if n.startswith(
        ("classi_d_eta", "classi_d__eta", "classi_di_eta", "fasce_d_et", "classi_d_et")
    ):
        return "classe_eta"
    if n.startswith(
        (
            "fasce_di_durata_del_con",
            "dettaglio_delle_fasce",
            "classe_di_durata_effett",
            "fasce_di_durata_prima",
        )
    ):
        return "durata_fascia"
    return COL_MAP.get(n, n)


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


def _derive_tipo_flusso(title: str) -> str:
    t = title.lower()
    if "missioni" in t and "attivat" in t:
        return "missione_attivata"
    if "missioni" in t and "cessat" in t:
        return "missione_cessata"
    if "somministrazione" in t and "attivat" in t:
        return "somministrazione_attivata"
    if "somministrazione" in t and "cessat" in t:
        return "somministrazione_cessata"
    if "tirocini" in t and "cessat" in t:
        return "tirocinio_cessato"
    if "tirocini" in t and "attivat" in t:
        return "tirocinio_attivato"
    if "trasformat" in t:
        return "trasformazione"
    if "cessat" in t:
        return "cessazione"
    if "attivat" in t:
        return "attivazione"
    return "altro"


def _parse_geo(value: str | None) -> tuple[str | None, str | None]:
    if not value:
        return None, None
    v = value.strip()
    if not v or v in ("N.D.", "N.D"):
        return None, None
    if v in ("Nord", "Centro", "Mezzogiorno"):
        return "ripartizione", v
    if "-" in v and v.split("-", 1)[0].strip().isdigit():
        return "regione", v.split("-", 1)[1].strip().title()
    return "regione", v


def _title_to_tabella_id(title: str) -> str:
    parts = title.split(" - ", 2)
    prefix = parts[0].strip().lower()
    fonte_code = "nota" if prefix.startswith("nota") else "ra"
    if len(parts) >= 2:
        tab = parts[1].strip().lower().replace("tabella ", "")
        tab = tab.split()[0].rstrip(".")
        return f"{fonte_code}_{tab}"
    return fonte_code


def _filename_to_tabella_id(filename: str, fonte: str) -> str:
    """'tabella_01_-_rapporti_...' → 'nota_01' o 'ra_01.01'."""
    stem = Path(filename).stem.lower()
    fonte_code = "nota" if fonte == "nota_trimestrale" else "ra"
    # Estrai numero tabella: 'tabella_01' o 'tabella_01.01' o 'tabella_02.02_bis'
    if "tabella_" in stem:
        rest = stem.split("tabella_", 1)[1]
        num = rest.split("_")[0].rstrip(".")
        # gestisci '01.01' da 'tabella_01.01_-_...'
        if not num and rest:
            num = rest.split("-")[0].strip().rstrip(".")
        # per RA i numeri sono tipo 01.01, 02.02_bis → tieni solo la parte numerica iniziale
        num_clean = ""
        for ch in num:
            if ch.isdigit() or ch == ".":
                num_clean += ch
            else:
                break
        num_clean = num_clean.rstrip(".")
        if not num_clean:
            # fallback: prendi i primi token dopo tabella_
            num_clean = rest.replace("-", "_").split("_")[0]
        return f"{fonte_code}_{num_clean}"
    return fonte_code


def normalize_row(row: dict, fonte: str, tabella_id: str, tipo_flusso: str) -> dict | None:
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

    anno = _parse_anno(mapped.get("anno"))
    if anno is None:
        return None

    geo_level = None
    geo = None
    if mapped.get("geo_reg"):
        geo_level, geo = _parse_geo(mapped["geo_reg"])
    elif mapped.get("geo_rip"):
        geo_level, geo = _parse_geo(mapped["geo_rip"])

    return {
        "fonte": fonte,
        "tabella_id": tabella_id,
        "tipo_flusso": tipo_flusso,
        "anno": anno,
        "trimestre": mapped.get("trimestre"),
        "geo_level": geo_level,
        "geo": geo,
        "genere": mapped.get("genere"),
        "tipologia_contratto": mapped.get("tipologia_contratto"),
        "settore": mapped.get("settore") or mapped.get("macro_settore"),
        "classe_eta": mapped.get("classe_eta"),
        "motivo_cessazione": mapped.get("motivo_cessazione") or mapped.get("macro_motivo"),
        "durata_fascia": mapped.get("durata_fascia"),
        "qualifica": mapped.get("qualifica"),
        "indicatore": mapped.get("indicatore"),
        "valore": valore,
    }


def read_local_csvs(
    writer: csv.DictWriter, skip_nota: bool = False, skip_ra: bool = False
) -> tuple[int, int]:
    """Legge i CSV locali già scaricati. Restituisce (rows, skipped)."""
    n_rows = 0
    n_skipped = 0
    for fonte, local_dir, skip in (
        ("nota_trimestrale", LOCAL_NOTA, skip_nota),
        ("rapporto_annuale", LOCAL_RA, skip_ra),
    ):
        if skip:
            continue
        if not local_dir.is_dir():
            print(f"  WARN: directory locale assente: {local_dir}")
            continue
        files = sorted(local_dir.glob("*.csv"))
        print(f"  Fonte locale {fonte}: {len(files)} file da {local_dir.name}/")
        for f in files:
            tabella_id = _filename_to_tabella_id(f.name, fonte)
            # tipo_flusso dal nome file (i titoli locali sono troncati, ma bastano le keyword)
            tipo_flusso = _derive_tipo_flusso(f.name.replace("_", " "))
            try:
                with open(f, encoding="utf-8", errors="replace") as fh:
                    reader = csv.DictReader(fh)
                    for row in reader:
                        norm = normalize_row(row, fonte, tabella_id, tipo_flusso)
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


def fetch_odata(
    writer: csv.DictWriter, only_missing: tuple[bool, bool] = (False, False)
) -> tuple[int, int]:
    """Fetch OData con retry. only_missing=(nota_presente, ra_presente) salta le fonti già in cache."""
    skip_nota, skip_ra = only_missing
    catalog = fetch_json(CATALOG_URL)
    packages = catalog.get("packageMap", {})

    targets: list[tuple[str, str, str, str]] = []
    for pid, pkg in packages.items():
        title = pkg.get("title", pid)
        fonte = None
        for prefix in GROUP_PREFIXES:
            if title.startswith(prefix):
                fonte = "nota_trimestrale" if prefix.startswith("Nota") else "rapporto_annuale"
                break
        if fonte is None:
            continue
        if fonte == "nota_trimestrale" and skip_nota:
            continue
        if fonte == "rapporto_annuale" and skip_ra:
            continue
        odata_res = None
        for rid in pkg.get("resourceIdentifiers", []):
            if rid.startswith("ODATA_"):
                odata_res = rid.replace("ODATA_", "")
                break
        if odata_res is None:
            continue
        targets.append((title, pid, odata_res, fonte))

    n_rows = 0
    n_skipped = 0
    for title, pkg_id, res_id, fonte in sorted(targets, key=lambda x: x[0]):
        tabella_id = _title_to_tabella_id(title)
        tipo_flusso = _derive_tipo_flusso(title)
        try:
            rows = fetch_odata_rows(pkg_id, res_id)
        except Exception as e:
            print(f"  ERRORE: {title[:60]} → {e}")
            continue
        for row in rows:
            norm = normalize_row(row, fonte, tabella_id, tipo_flusso)
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

    # Legge indipendentemente ogni cartella locale presente;
    # fetch OData solo per le fonti mancanti.
    has_nota = LOCAL_NOTA.is_dir() and any(LOCAL_NOTA.glob("*.csv"))
    has_ra = LOCAL_RA.is_dir() and any(LOCAL_RA.glob("*.csv"))
    print(f"Cache locale: nota={'sì' if has_nota else 'no'} ra={'sì' if has_ra else 'no'}")

    n_rows = 0
    n_skipped = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        if has_nota or has_ra:
            n_rows, n_skipped = read_local_csvs(writer, skip_nota=not has_nota, skip_ra=not has_ra)
        if not has_nota or not has_ra:
            print("Fetch OData per fonti mancanti…")
            o_rows, o_skipped = fetch_odata(writer, only_missing=(has_nota, has_ra))
            n_rows += o_rows
            n_skipped += o_skipped

    print(f"Totale: {n_rows} righe → {out_path} ({n_skipped} scartate)")


if __name__ == "__main__":
    main()
