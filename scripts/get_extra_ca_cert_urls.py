import os
import sys
from pathlib import Path
import yaml

def get_urls(config_path: Path) -> list:
    """Estrae gli URL dei certificati CA extra dal file di configurazione."""
    if not config_path.is_file():
        return []
        
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    seen = []
    if data and isinstance(data, dict):
        # Cerca i certificati extra nella struttura del dataset
        candidates = data.get("candidates", {})
        for c_data in candidates.values():
            urls = c_data.get("extra_ca_cert_urls", [])
            if isinstance(urls, str):
                urls = [urls]
            for url in urls:
                if url and url not in seen:
                    seen.append(url)
    return seen


def main() -> int:
    """CLI entry point.

    Returns:
        0 on success,
        1 on usage error or file‑not‑found,
        2 on YAML parsing error.
    """
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])
    elif os.environ.get("CONFIG_PATH"):
        config_path = Path(os.environ["CONFIG_PATH"])
    else:
        print("Usage: get_extra_ca_cert_urls.py <dataset.yml path>", file=sys.stderr)
        return 1

    # Ritorna 1 se il file esplicitamente richiesto non esiste
    if not config_path.is_file():
        print(f"Error: File not found: {config_path}", file=sys.stderr)
        return 1

    try:
        urls = get_urls(config_path)
        for url in urls:
            print(url)
        return 0
    except yaml.YAMLError as e:
        print(f"YAML parsing error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
