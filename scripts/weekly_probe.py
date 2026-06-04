#!/usr/bin/env python3
"""Weekly probe: raggiungibilità fonti — un probe per candidate (solo ultimo anno).

Legge batches/http.txt, per ogni candidate risolve l'ultimo anno
tramite resolve_sample_run.py, estrae l'URL della fonte primaria
dal dataset.yml e chiama probe_url_routed (toolkit).

Produce /tmp/probe_report.json con UP/DOWN per candidate.
In CI scrive anche GITHUB_STEP_SUMMARY.

Usage:
    python scripts/weekly_probe.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import yaml

from toolkit.scout.probe import probe_url_routed

ROOT = Path(__file__).resolve().parent.parent
BATCH_FILE = ROOT / "batches" / "http.txt"
RESOLVE_SCRIPT = ROOT / "scripts" / "resolve_sample_run.py"
TIMEOUT = 10


def resolve_year(config_path: Path) -> int | None:
    """Usa resolve_sample_run.py per trovare l'ultimo anno del candidate."""
    try:
        r = subprocess.run(
            [sys.executable, str(RESOLVE_SCRIPT), str(config_path)],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode == 0:
            data = json.loads(r.stdout)
            return data.get("sample_year")
        return None
    except Exception:
        return None


def extract_primary_url(cfg: dict, year: int) -> str | None:
    """Estrae URL della fonte primaria dal dataset.yml."""
    sources = cfg.get("raw", {}).get("sources", [])
    if not sources:
        return None

    # Fonte primaria (primary=true) o la prima
    primary = None
    for s in sources:
        if s.get("primary", False):
            primary = s
            break
    if primary is None:
        primary = sources[0]

    stype = primary.get("type", "")
    args = primary.get("args", {})
    client = primary.get("client", {})

    if stype == "http_file":
        url = args.get("url", "")
    elif stype == "ckan":
        url = args.get("portal_url", "")
    elif stype == "sdmx":
        url = client.get("data_base_url", "")
    elif stype == "sparql":
        url = args.get("endpoint", "")
    else:
        url = args.get("url", "") or args.get("endpoint", "")

    if not url:
        return None

    url = url.replace("{year}", str(year))
    return url


def probe_one(slug: str, config_path: Path) -> dict:
    """Probe su un candidate, restituisce risultato."""
    start = time.time()

    year = resolve_year(config_path)
    if year is None:
        return {
            "slug": slug, "status": "SKIP",
            "error": "anno non risolto", "duration": round(time.time() - start, 1),
        }

    try:
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
    except Exception as e:
        return {
            "slug": slug, "status": "ERROR",
            "error": f"lettura YAML: {e}", "duration": round(time.time() - start, 1),
        }

    url = extract_primary_url(cfg, year)
    if not url:
        return {
            "slug": slug, "status": "SKIP",
            "error": "URL fonte primaria non trovato", "duration": round(time.time() - start, 1),
        }

    try:
        probe = probe_url_routed(url, timeout=TIMEOUT)
        sc = probe.get("status_code", 0)

        if sc == 0:
            status = "UNREACHABLE"
        elif 200 <= sc < 400:
            status = "UP"
        elif sc == 404:
            status = "NOT_FOUND"
        elif sc == 403:
            status = "FORBIDDEN"
        elif sc == 503:
            status = "UNAVAILABLE"
        else:
            status = f"HTTP_{sc}"

        return {
            "slug": slug, "url": url, "year": year,
            "source_type": probe.get("source_type", "?"),
            "status": status, "status_code": sc,
            "error": "",
            "duration": round(time.time() - start, 1),
        }
    except Exception as e:
        return {
            "slug": slug, "url": url, "year": year,
            "status": "ERROR", "error": str(e),
            "duration": round(time.time() - start, 1),
        }


def main() -> int:
    # Leggi batch
    if not BATCH_FILE.exists():
        print(f"ERROR: batch file non trovato: {BATCH_FILE}", file=sys.stderr)
        return 1

    configs = []
    for line in BATCH_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        configs.append(ROOT / line)

    if not configs:
        print("ERROR: nessun config trovato in batches/http.txt", file=sys.stderr)
        return 1

    print(f"Batch: http.txt ({len(configs)} candidate)")
    print()

    results = []
    start_total = time.time()

    for cfg_path in configs:
        slug = cfg_path.parent.name
        print(f"  {slug}... ", end="", flush=True)
        r = probe_one(slug, cfg_path)
        results.append(r)

        s = r["status"]
        if s == "UP":
            print(f"✅ {s} ({r.get('source_type','?')}, {r['duration']}s)")
        elif s == "SKIP":
            print(f"⏭️  {s} ({r.get('error','')})")
        else:
            print(f"❌ {s} ({r.get('status_code','')} {r.get('error','')})")

    total_time = round(time.time() - start_total, 1)
    up = sum(1 for r in results if r["status"] == "UP")
    down = sum(1 for r in results if r["status"] not in ("UP", "SKIP"))
    skip = sum(1 for r in results if r["status"] == "SKIP")

    print()
    print("=" * 60)
    print(f"  {up}/{len(results)} UP  |  {down} DOWN  |  {skip} SKIP  |  {total_time}s")
    print("=" * 60)

    report = {
        "summary": {
            "total": len(results), "passed": up, "failed": down, "skipped": skip,
            "duration_seconds": total_time,
        },
        "results": results,
    }

    # Scrivi report
    report_path = Path("/tmp/probe_report.json")
    report_path.write_text(json.dumps(report, indent=2))

    # GITHUB_STEP_SUMMARY se in CI
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        lines = [f"## Weekly probe — {up}/{len(results)} UP"]
        lines.append("")
        for r in results:
            s = r["status"]
            if s == "UP":
                icon = "✅"
            elif s == "SKIP":
                icon = "⏭️"
            else:
                icon = "❌"
            src = r.get("source_type", "")
            lines.append(f"{icon} {r['slug']:35s} {s:15s} {src}")
        lines.append("")
        lines.append(f"Durata: {total_time}s")
        if skip:
            lines.append(f"Skip: {skip} (candidate senza URL o anno)")
        Path(step_summary).write_text("\n".join(lines) + "\n")

    return 0 if down == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
