#!/usr/bin/env python3
"""Preprocess: scarica i parquet da costituzione-italiana su GitHub e produce il CSV master.

Ogni riga = un articolo della Costituzione (1-139) con metriche aggregate.

Output: raw_input.csv (consumato dal toolkit per clean → mart)
"""

from __future__ import annotations

import argparse
import csv
import logging
from collections import Counter
from pathlib import Path
from urllib.request import urlopen

logger = logging.getLogger("costituzione-master")

# Repository pubblico su GitHub
BASE = "https://raw.githubusercontent.com/dataciviclab/costituzione-italiana/main/data"

NOMI = {
    "articoli": "articoli.parquet",
    "revisioni": "revisioni.parquet",
    "atti": "atti-promovimento.parquet",
    "indicatori": "indicatori-costituzionali.parquet",
}


def _leggi_file(nome: str) -> bytes:
    """Scarica un parquet dal repo pubblico costituzione-italiana."""
    url = f"{BASE}/{NOMI[nome]}"
    logger.info("Download %s", url)
    with urlopen(url, timeout=60) as resp:
        return resp.read()


def leggi_articoli(data: bytes) -> dict[int, dict]:
    """Legge articoli.parquet: art → {testo, parte, heading}."""
    import pyarrow.parquet as pq
    import io

    t = pq.read_table(io.BytesIO(data))
    result = {}
    for i in range(t.num_rows):
        a = t.column("articolo")[i].as_py()
        if a is not None:
            result[a] = {
                "testo": (t.column("testo")[i].as_py() or "")[:200],
                "parte": t.column("parte")[i].as_py() or "",
                "heading": t.column("heading")[i].as_py() or "",
            }
    return result


def leggi_revisioni(data: bytes) -> Counter:
    """Legge revisioni.parquet: art → numero modifiche."""
    import pyarrow.parquet as pq
    import io

    t = pq.read_table(io.BytesIO(data))
    c: Counter = Counter()
    for i in range(t.num_rows):
        if t.column("tipo")[i].as_py() == "modifica_costituzione":
            for a in t.column("articoli_modificati")[i].as_py() or []:
                c[a] += 1
    return c


def leggi_giudizi(data: bytes) -> Counter:
    """Legge atti-promovimento.parquet: art → numero giudizi."""
    import pyarrow.parquet as pq
    import io

    t = pq.read_table(io.BytesIO(data))
    c: Counter = Counter()
    for v in t.column("parametro_articolo").to_pylist():
        if v:
            c[v] += 1
    return c


def leggi_indicatori(data: bytes) -> dict[int, list[str]]:
    """Legge indicatori-costituzionali.parquet: art → [slug, ...]."""
    import pyarrow.parquet as pq
    import io

    t = pq.read_table(io.BytesIO(data))
    result: dict[int, list[str]] = {}
    for i in range(t.num_rows):
        a = t.column("articolo")[i].as_py()
        slug = t.column("dataset_slug")[i].as_py()
        if a is not None and slug:
            result.setdefault(a, []).append(slug)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="raw_input.csv")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    # Leggi (locale o remoto)
    raw = {}
    for key in NOMI:
        raw[key] = _leggi_file(key)

    # Parse
    articoli = leggi_articoli(raw["articoli"])
    revisioni = leggi_revisioni(raw["revisioni"])
    giudizi = leggi_giudizi(raw["atti"])
    indicatori = leggi_indicatori(raw["indicatori"])

    # Write
    campi = [
        "articolo",
        "parte",
        "heading",
        "testo_preview",
        "n_modifiche",
        "n_giudizi",
        "n_indicatori",
        "dataset_slugs",
    ]
    out_path = Path(args.output)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campi)
        w.writeheader()
        for a in sorted(articoli):
            info = articoli[a]
            w.writerow(
                {
                    "articolo": a,
                    "parte": info["parte"],
                    "heading": info["heading"],
                    "testo_preview": info["testo"],
                    "n_modifiche": revisioni.get(a, 0),
                    "n_giudizi": giudizi.get(a, 0),
                    "n_indicatori": len(indicatori.get(a, [])),
                    "dataset_slugs": ", ".join(indicatori.get(a, [])),
                }
            )

    logger.info("Scritto %s — %d articoli", out_path, len(articoli))


if __name__ == "__main__":
    main()
