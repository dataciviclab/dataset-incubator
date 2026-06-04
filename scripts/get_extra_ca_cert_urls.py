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

from toolkit.core.dataset_loader import load_dataset_manifest


def get_urls(cfg_path: Path) -> list[str]:
    """Extract deduplicated extra CA cert URLs from a dataset.yml."""
    if not cfg_path.exists():
        return []
    manifest = load_dataset_manifest(cfg_path)
    if "error" in manifest:
        raise ValueError(manifest["error"])
    # Deduplica mantenendo l'ordine
    seen: set[str] = set()
    result: list[str] = []
    for url in manifest.get("extra_ca_cert_urls", []):
        if url and url not in seen:
            seen.add(url)
            result.append(url)
    return result


def main() -> int:
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    elif os.environ.get("CONFIG_PATH"):
        config_path = Path(os.environ["CONFIG_PATH"])
    else:
        print("Usage: get_extra_ca_cert_urls.py <dataset.yml path>", file=sys.stderr)
        return 1

    for url in get_urls(config_path):
        print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
