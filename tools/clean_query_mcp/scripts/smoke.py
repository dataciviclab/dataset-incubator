from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.clean_query_mcp import server  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smoke test clean-query MCP catalog and GCS parquet access."
    )
    parser.add_argument("--dataset", help="Limit smoke test to one dataset slug.")
    args = parser.parse_args()

    catalog = server.find("")
    datasets = catalog.get("datasets", [])
    if args.dataset:
        datasets = [item for item in datasets if item["slug"] == args.dataset]
        if not datasets:
            print(f"Dataset non trovato: {args.dataset}", file=sys.stderr)
            return 2

    failures = 0
    for item in datasets:
        slug = item["slug"]
        details = server.dataset_overview(slug, limit=0)
        year = details.get("period", {}).get("end")
        result = server.run_query(
            "SELECT COUNT(*) AS rows FROM clean_input",
            dataset=slug,
            year=year,
            max_rows=1,
        )
        if "error" in result:
            failures += 1
            print(f"FAIL {slug}: {result['error']}")
            continue
        rows = result.get("rows", [])
        count = rows[0][0] if rows else None
        print(f"OK {slug}: rows={count} year={year}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
