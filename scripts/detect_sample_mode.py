#!/usr/bin/env python3
"""Detect sample mode per candidate: sample_bytes (CSV/JSON) vs sample_rows (ZIP/CKAN).

Usato dal workflow pr-toolkit-check per scegliere il flag ottimale:
  - sample_bytes: scarica solo i primi N bytes (HTTP Range header) — efficiente, ma
    non funziona per ZIP (file troncato non decomprimibile) o CKAN (URL dinamici).
  - sample_rows: applica LIMIT N dopo il clean — funziona sempre, ma richiede
    lo scaricamento completo del raw.

Output: stampa "sample_rows" o "sample_bytes" su stdout.
"""

import sys
import yaml
from pathlib import Path


def _is_zip_source(src: dict) -> bool:
    """True se la fonte e' ZIP (sample_bytes non funziona)."""
    args = src.get("args") or {}
    url = (args.get("url") or "").lower()
    filename = (args.get("filename") or "").lower()
    return url.endswith(".zip") or ".zip" in url or filename.endswith(".zip")


def detect_sample_mode(config_path: str) -> str:
    cfg_path = Path(config_path)
    if not cfg_path.exists():
        print(f"Config non trovato: {config_path}", file=sys.stderr)
        return "sample_rows"  # default conservativo

    with open(cfg_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    sources = (cfg.get("raw") or {}).get("sources") or []

    for src in sources:
        stype = src.get("type", "http_file")

        # ZIP: sample_bytes tronca l'archivio, non decomprimibile
        if _is_zip_source(src):
            return "sample_rows"

        # CKAN: usa URL dinamici/redirect, Range header non affidabile
        if stype == "ckan":
            return "sample_rows"

        # http_post_file: potrebbe avere body complessi, meglio sample_rows
        if stype == "http_post_file":
            return "sample_rows"

    # Default: fonti HTTP semplici (CSV, JSON, XLSX) — sample_bytes OK
    return "sample_bytes"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: detect_sample_mode.py <dataset.yml>", file=sys.stderr)
        sys.exit(1)
    mode = detect_sample_mode(sys.argv[1])
    print(mode)
