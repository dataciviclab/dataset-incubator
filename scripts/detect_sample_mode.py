#!/usr/bin/env python3
"""Detect sample mode per candidate.

Attualmente ritorna sempre "sample_rows" perche' sample_bytes tronca il file
a byte arbitrari, rompendo i CSV con campi quotati multilinea (comuni nei
dati pubblici italiani). Con sample_mode che skippa min_rows, sample_rows
e' safe per tutti i tipi di fonte.

Pronto per sample_bytes futuro: basta cambiare il return in fondo a
detect_sample_mode() quando il toolkit supporta troncamento a linea intera,
non a byte.
"""

import sys
import yaml
from pathlib import Path


def detect_sample_mode(config_path: str) -> str:
    cfg_path = Path(config_path)
    if not cfg_path.exists():
        print(f"Config non trovato: {config_path}", file=sys.stderr)
        return "sample_rows"

    with open(cfg_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    sources = (cfg.get("raw") or {}).get("sources") or []

    for src in sources:
        _ = src  # placeholder per futura logica di ispezione fonte

    # Sempre sample_rows: safe per CSV multilinea, ZIP, CKAN.
    # sample_bytes resta disattivato perche' tronca a byte e i CSV con
    # campi quotati multilinea rompono il parsing DuckDB strict mode.
    return "sample_rows"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: detect_sample_mode.py <dataset.yml>", file=sys.stderr)
        sys.exit(1)
    mode = detect_sample_mode(sys.argv[1])
    print(mode)
