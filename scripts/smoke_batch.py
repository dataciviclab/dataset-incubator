#!/usr/bin/env python3
"""Esegue smoke test batch su una lista di candidate.

Legge un file batch (es. batches/http.txt), per ogni config risolve
l'ultimo anno via resolve_sample_run.py, ed esegue toolkit run all
con --smoke. Produce report JSON e riepilogo a schermo.

Usage:
    python scripts/smoke_batch.py batches/http.txt
    python scripts/smoke_batch.py batches/http.txt --parallel 4
    python scripts/smoke_batch.py batches/green.txt --json report.json
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parent


def resolve_year(config_path: str) -> dict | None:
    """Run resolve_sample_run.py for a config and return result."""
    try:
        r = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "resolve_sample_run.py"), config_path],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode == 0:
            return json.loads(r.stdout)
        return None
    except Exception:
        return None


def run_one(config_path: str, year: int) -> dict:
    """Run toolkit on one candidate for one year with --smoke."""
    slug = Path(config_path).parent.name
    start = time.time()
    try:
        r = subprocess.run(
            [sys.executable, "-m", "toolkit.cli.app", "run", "all",
             "-c", config_path, "-y", str(year), "--smoke"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        ok = r.returncode == 0
        duration = round(time.time() - start, 1)
        output = (r.stdout + r.stderr).strip()
        return {
            "slug": slug,
            "config": config_path,
            "year": year,
            "status": "PASSED" if ok else "FAILED",
            "duration": duration,
            "output": output[-200:] if not ok else "",
        }
    except subprocess.TimeoutExpired:
        return {
            "slug": slug, "config": config_path, "year": year,
            "status": "TIMEOUT", "duration": round(time.time() - start, 1),
            "output": "timeout 120s",
        }
    except Exception as e:
        return {
            "slug": slug, "config": config_path, "year": year,
            "status": "ERROR", "duration": round(time.time() - start, 1),
            "output": str(e),
        }


def load_configs(batch_file: str) -> list[str]:
    """Load config paths from a batch file (skip comments/empty)."""
    path = Path(batch_file)
    if not path.exists():
        print(f"ERROR: file non trovato: {batch_file}", file=sys.stderr)
        sys.exit(1)
    configs = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        configs.append(line)
    return configs


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Smoke batch per candidate DI")
    parser.add_argument("batch_file", help="Path a batches/*.txt")
    parser.add_argument("--parallel", type=int, default=1, help="Run paralleli (default: 1)")
    parser.add_argument("--json", type=str, help="Path per output JSON")
    args = parser.parse_args()

    configs = load_configs(args.batch_file)
    if not configs:
        print("ERROR: nessun config trovato", file=sys.stderr)
        return 1
    print(f"Batch: {Path(args.batch_file).name}")
    print(f"Configs: {len(configs)}")
    print(f"Parallel: {args.parallel}")
    print()

    tasks = []
    for cfg in configs:
        resolved = resolve_year(cfg)
        if resolved and resolved.get("sample_year"):
            tasks.append((cfg, resolved["sample_year"]))
        else:
            print(f"  ❌ {cfg} — impossibile risolvere anno")
            tasks.append((cfg, None))

    results = []
    start_total = time.time()

    # Add SKIPPED entries before parallel execution (year could not be resolved)
    for cfg, year in tasks:
        if year is None:
            results.append({
                "slug": Path(cfg).parent.name, "config": cfg,
                "year": None, "status": "SKIPPED",
                "duration": 0, "output": "anno non risolto",
            })
            print(f"  ⏭️ {Path(cfg).parent.name:35s} — SKIPPED (no year)")

    if args.parallel > 1:
        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            futures = {
                ex.submit(run_one, cfg, year): (cfg, year)
                for cfg, year in tasks if year
            }
            for future in as_completed(futures):
                r = future.result()
                results.append(r)
                icon = "✅" if r["status"] == "PASSED" else "❌"
                print(f"  {icon} {r['slug']:35s} year={r['year']}  {r['duration']:>5.1f}s  {r['status']}")
    else:
        for cfg, year in tasks:
            if year is None:
                results.append({
                    "slug": Path(cfg).parent.name, "config": cfg,
                    "year": None, "status": "SKIPPED",
                    "duration": 0, "output": "anno non risolto",
                })
                print(f"  ⏭️ {Path(cfg).parent.name:35s} — SKIPPED (no year)")
                continue
            r = run_one(cfg, year)
            results.append(r)
            icon = "✅" if r["status"] == "PASSED" else "❌"
            print(f"  {icon} {r['slug']:35s} year={r['year']}  {r['duration']:>5.1f}s  {r['status']}")

    total_time = round(time.time() - start_total, 1)
    passed = sum(1 for r in results if r["status"] == "PASSED")
    failed = sum(1 for r in results if r["status"] != "PASSED")

    print()
    print("=" * 60)
    print(f"  RISULTATI: {passed}/{len(results)} passed  |  {total_time}s totali")
    print("=" * 60)
    for r in results:
        if r["status"] != "PASSED":
            print(f"  ❌ {r['slug']} ({r['status']}): {r.get('output','')[:120]}")

    report = {
        "batch_file": args.batch_file,
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "duration_seconds": total_time,
        "results": results,
    }
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2))
        print(f"\nReport salvato: {args.json}")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
