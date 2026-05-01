"""Resolve sample run parameters from a dataset.yml.

Responsabilità (per issue #154):
  - leggere dataset.yml
  - determinare sample_year (ultimo anno in dataset.years)
  - validare gli input minimi
  - restituire JSON usabile dal workflow

Non deve:
  - eseguire la pipeline
  - duplicare logica di pipeline
  - supportare euristiche complesse per source/config

Usage:
  python scripts/resolve_sample_run.py candidates/istat-housing-crowding/dataset.yml
  python scripts/resolve_sample_run.py candidates/ispra-ru-costi-kg/sources/a_ru_base/dataset.yml

Output JSON:
  {
    "config_path": "candidates/istat-housing-crowding/dataset.yml",
    "slug": "istat-housing-crowding",
    "sample_year": 2024,
    "is_nested": false,
    "note": ""
  }

Errors exit with code 1 and JSON on stderr:
  {"error": "message"}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def resolve(config_path: str) -> dict:
    """Resolve sample run parameters for a dataset config."""
    path = Path(config_path)
    if not path.exists():
        return {"error": f"File not found: {config_path}"}

    try:
        with open(path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        return {"error": f"Invalid YAML: {e}"}

    # Validate it's a dataset.yml with required fields
    dataset = cfg.get("dataset", {})
    if not dataset:
        return {"error": f"No 'dataset' section in {config_path}"}

    name = dataset.get("name", "")
    if not name:
        return {"error": f"No 'dataset.name' in {config_path}"}

    years = dataset.get("years", [])
    if not years:
        return {
            "error": f"No 'dataset.years' in {config_path} — cannot determine sample year",
            "config_path": str(path),
            "slug": None,
        }

    # Sample year = last year in the list (most recent)
    try:
        years_int = sorted(int(y) for y in years)
    except (TypeError, ValueError):
        return {"error": f"Invalid years value in {config_path}: {years}"}

    sample_year = years_int[-1]

    # Compute slug from config path, NOT from YAML dataset.name
    # This avoids mismatch with pipeline_signals which uses directory names
    parts = path.parts
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        rel = path

    # Find slug: first segment after 'candidates/' or 'support_datasets/'
    slug = None
    for i, part in enumerate(rel.parts):
        if part in ("candidates", "support_datasets"):
            if i + 1 < len(rel.parts):
                slug = rel.parts[i + 1]
                break

    # Fallback: derive from directory if slug not found (should not happen
    # for valid candidates, but guards against malformed paths)
    if slug is None:
        slug = path.parts[-2] if len(path.parts) >= 2 else None

    # Nested config detection
    is_nested = "sources" in parts or "compose" in parts

    return {
        "config_path": str(rel),
        "slug": slug,
        "sample_year": sample_year,
        "all_years": years_int,
        "is_nested": is_nested,
        "note": (
            "nested config — run via source layer"
            if is_nested
            else ""
        ),
    }


def main() -> int:
    if len(sys.argv) < 2:
        print(
            json.dumps({"error": "Usage: python resolve_sample_run.py <dataset.yml path>"}),
            file=sys.stderr,
        )
        return 1

    config_path = sys.argv[1]
    result = resolve(config_path)

    if "error" in result:
        print(json.dumps(result), file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
