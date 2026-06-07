#!/usr/bin/env python3
"""Esegue toolkit run full per un compose, prima i support dataset in sequenza.

Uso:
    python scripts/run_compose_with_support.py <dataset.yml> [extra_opts...]
"""

import subprocess
import sys
from pathlib import Path

import yaml


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: run_compose_with_support.py <dataset.yml> [extra_opts...]")
        sys.exit(1)

    config_path = Path(sys.argv[1])
    extra_opts = sys.argv[2:]

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    # Esegue i support dataset in sequenza
    supports = cfg.get("support", [])
    if supports:
        print(f"📦 Compose: eseguo {len(supports)} support dataset in sequenza...")
        for s in supports:
            scfg = s.get("config", "")
            syears = s.get("years", [])
            if not scfg or not Path(scfg).exists():
                print(f"  ⏭️  Support config non trovata: {scfg}")
                continue
            print(f"  ▶ Support: {scfg} years={syears}")
            for y in syears:
                cmd = ["toolkit", "run", "full", "--config", scfg, "--year", str(y)] + extra_opts
                print(f"    toolkit run full --year {y}...")
                r = subprocess.run(cmd, capture_output=True, text=True)
                if r.returncode != 0:
                    print(f"    ❌ Support {scfg} year {y} FAILED")
                    print(r.stderr)
                    sys.exit(1)
                print("    ✅ OK")
        print("  ✅ Support completati")

    # Esegue il compose stesso
    print(f"📦 Eseguo compose: {config_path}")
    cmd = ["toolkit", "run", "full", "--config", str(config_path)] + extra_opts
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("❌ Compose FAILED")
        print(r.stderr)
    else:
        print("✅ Compose OK")
    # Stampa stdout del compose (contiene JSON)
    print(r.stdout)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
