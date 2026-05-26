"""Extract extra CA certificate URLs from a dataset.yml.

Legge la config, estrae extra_ca_cert_url e extra_ca_cert_urls
da raw.sources[].args, e stampa le URL deduplicate una per riga.

Usage:
    python scripts/get_extra_ca_cert_urls.py candidates/.../dataset.yml
    CONFIG_PATH=... python scripts/get_extra_ca_cert_urls.py

Exit code 0 anche se non trova URL (nessun output).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml


def get_urls(cfg_path: Path) -> list[str]:
    """Extract deduplicated extra CA cert URLs from a dataset.yml."""
    if not cfg_path.exists():
        return []

    try:
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        return []

    seen: list[str] = []
    for source in cfg.get("raw", {}).get("sources") or []:
        if not isinstance(source, dict):
            continue
        args = source.get("args") or {}
        for key in ("extra_ca_cert_url", "extra_ca_cert_urls"):
            value = args.get(key)
            if not value:
                continue
            if isinstance(value, str):
                urls = [value]
            elif isinstance(value, list):
                urls = [str(item) for item in value if item]
            else:
                continue
            for url in urls:
                if url and url not in seen:
                    seen.append(url)
    return seen


def main() -> int:
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    elif os.environ.get("CONFIG_PATH"):
        config_path = Path(os.environ["CONFIG_PATH"])
    else:
        print("Usage: get_extra_ca_cert_urls.py <dataset.yml path>", file=sys.stderr)
        return 1

    if not config_path.is_file():
        print(f"ERROR: Configuration file does not exist or is not a file: {config_path}", file=sys.stderr)
        return 1

    for url in get_urls(config_path):
        print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
