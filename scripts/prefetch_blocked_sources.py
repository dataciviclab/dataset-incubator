#!/usr/bin/env python3
"""Pre-download raw files from sources that block CI (e.g. dati.salute.gov.it).

Scarica il file raw via proxy e trasforma il dataset.yml da http_file a
local_file, così il toolkit salta probe HTTP (che fallirebbe) e usa il
file già presente.

Uso:
    HTTPS_PROXY=http://proxy:8888 python scripts/prefetch_blocked_sources.py \
        candidates/strutture-asl/dataset.yml

Variabili d'ambiente:
    HTTPS_PROXY / HTTP_PROXY : proxy da usare per lo scaricamento
    BLOCKED_SOURCE_PROXY     : proxy specifico per fonti bloccate (override)
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

# Espressioni regolari per identificare URL di fonti bloccate
BLOCKED_PATTERNS: list[re.Pattern] = [
    re.compile(r"https?://(www\.)?dati\.salute\.gov\.it"),
]


def _get_proxy() -> str | None:
    """Proxy da usare per fonti bloccate (env var o standard)."""
    return (
        os.environ.get("BLOCKED_SOURCE_PROXY")
        or os.environ.get("HTTPS_PROXY")
        or os.environ.get("https_proxy")
        or os.environ.get("HTTP_PROXY")
        or os.environ.get("http_proxy")
    )


def _is_blocked(url: str) -> bool:
    """True se l'URL appartiene a una fonte che blocca CI."""
    return any(p.search(url) for p in BLOCKED_PATTERNS)


def _download_with_curl(url: str, dest: Path, proxy: str) -> None:
    """Scarica file via proxy usando curl."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-x", proxy, "-sfL", url, "-o", str(dest)]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        size = dest.stat().st_size
        print(f"  ✅ scaricato {size} bytes -> {dest}")
    except subprocess.CalledProcessError as exc:
        print(f"  ❌ curl fallito (exit {exc.returncode}): {exc.stderr.strip()}")
        sys.exit(1)


def _patch_config(config_path: Path, raw_path: Path) -> None:
    """Modifica dataset.yml: http_file → local_file, url → path."""
    with open(config_path) as f:
        content = f.read()

    # Sostituisci tipo e URL
    content = content.replace('type: "http_file"', 'type: "local_file"')
    content = re.sub(
        r'url: "https?://[^"]+"',
        f'path: "{raw_path}"',
        content,
    )

    with open(config_path, "w") as f:
        f.write(content)
    print(f"  ✅ dataset.yml aggiornato: http_file → local_file")


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <dataset.yml> [dataset.yml ...]")
        sys.exit(1)

    proxy = _get_proxy()
    if not proxy:
        print("Nessun proxy configurato (HTTPS_PROXY / BLOCKED_SOURCE_PROXY). Skipping.")
        return

    config_paths = [Path(a) for a in sys.argv[1:]]

    for config_path in config_paths:
        if not config_path.exists():
            print(f"❌ Config non trovata: {config_path}")
            sys.exit(1)

        with open(config_path) as f:
            cfg = yaml.safe_load(f)

        # Cerca raw.sources con http_file
        raw_sources = (cfg or {}).get("raw", {}).get("sources", [])
        if not raw_sources:
            continue

        dataset_name = cfg.get("dataset", {}).get("name", config_path.stem)
        years = cfg.get("dataset", {}).get("years", [])
        root = Path(cfg.get("root", "../../out"))

        for source in raw_sources:
            if source.get("type") != "http_file":
                continue
            url = source.get("args", {}).get("url", "")
            if not _is_blocked(url):
                continue

            filename = source.get("args", {}).get(
                "filename",
                os.path.basename(url.split("?")[0]),
            )

            print(f"\n📦 {dataset_name} — {filename}")
            print(f"   URL: {url[:100]}…")

            # Determina path raw: root/data/raw/<slug>/<year>/<filename>
            # root è relativo alla dataset-incubator root
            # Il path assoluto: config_path.parent / root / data/raw/...
            base = (config_path.parent / root).resolve()
            for year in years:
                raw_dir = base / "data" / "raw" / dataset_name / str(year)
                dest = raw_dir / filename

                if dest.exists():
                    print(f"  ⏭️ già presente: {dest}")
                    continue

                _download_with_curl(url, dest, proxy)

            _patch_config(config_path, f"out/data/raw/{dataset_name}/{{year}}/{filename}")

    print("\n✅ Pre-download completato.")


if __name__ == "__main__":
    main()
