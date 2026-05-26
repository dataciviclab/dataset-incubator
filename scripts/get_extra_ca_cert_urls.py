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
        raw = data.get("raw", {})
        if isinstance(raw, dict):
            sources = raw.get("sources", [])
            if isinstance(sources, list):
                for source in sources:
                    if isinstance(source, dict):
                        args = source.get("args", {})
                        if isinstance(args, dict):
                            # 1. Gestione chiave singola: extra_ca_cert_url
                            url = args.get("extra_ca_cert_url")
                            if url and isinstance(url, str) and url not in seen:
                                seen.append(url)
                            
                            # 2. Gestione chiave lista: extra_ca_cert_urls
                            urls = args.get("extra_ca_cert_urls", [])
                            if isinstance(urls, str):
                                urls = [urls]
                            if isinstance(urls, list):
                                for u in urls:
                                    if u and isinstance(u, str) and u not in seen:
                                        seen.append(u)
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

    if not config_path.is_file():
        print(f"Error: File not found: {config_path}", file=sys.stderr)
        return 1

    try:
        urls = get_urls(config_path)
        for url in urls:
            print(url)
        return 0
    except Exception as e:
        print(f"YAML parsing error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
