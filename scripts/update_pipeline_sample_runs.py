from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "registry" / "pipeline_signals.json"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Attach post-merge sample-run results to pipeline_signals.json."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument(
        "--samples-dir",
        type=Path,
        required=True,
        help="Directory containing sample_run_result.json artifacts.",
    )
    args = parser.parse_args()

    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    results = read_sample_results(args.samples_dir)
    if not results:
        print(f"no sample_run_result.json files found in {args.samples_dir}", file=sys.stderr)
        return 1

    errors = apply_sample_results(catalog, results)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    args.catalog.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"updated {args.catalog} with {len(results)} sample-run result(s)")
    return 0


def read_sample_results(samples_dir: Path) -> list[dict[str, Any]]:
    results = []
    for path in sorted(samples_dir.rglob("sample_run_result.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["_artifact_path"] = str(path)
        results.append(payload)
    return results


def apply_sample_results(
    catalog: dict[str, Any],
    results: list[dict[str, Any]],
) -> list[str]:
    signals = catalog.get("signals", [])
    by_id = {signal.get("id"): signal for signal in signals if isinstance(signal, dict)}
    grouped: dict[str, list[dict[str, Any]]] = {}
    errors = []

    for result in results:
        signal_id = result.get("id")
        if not signal_id:
            errors.append(f"{result.get('_artifact_path', '<unknown>')}: missing id")
            continue
        if signal_id not in by_id:
            errors.append(f"{signal_id}: no matching signal in catalog")
            continue
        grouped.setdefault(signal_id, []).append(result)

    if errors:
        return errors

    for signal_id, signal_results in grouped.items():
        by_id[signal_id]["sample_run"] = summarize_sample_results(signal_results)
    return []


def summarize_sample_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(results, key=lambda item: item.get("config_path", ""))
    failed = any(item.get("status") != "passed" for item in ordered)
    latest = ordered[-1]

    summary: dict[str, Any] = {
        "status": "failed" if failed else "passed",
        "run_id": str(latest.get("run_id", "")),
        "run_url": latest.get("run_url", ""),
        "checked_at": latest.get("checked_at", ""),
    }

    if len(ordered) == 1:
        only = ordered[0]
        years = only.get("years", [])
        if not years and only.get("year"):
            years = [only.get("year")]
        summary["years"] = years
        summary["config_path"] = only.get("config_path", "")
        if only.get("config_exists") is False:
            summary["config_exists"] = False
        return summary

    configs = []
    years = set()
    for item in ordered:
        year = item.get("year")
        if year is not None:
            years.add(int(year))
        config = {
            "status": item.get("status", "failed"),
            "year": year,
            "config_path": item.get("config_path", ""),
        }
        if item.get("config_exists") is False:
            config["config_exists"] = False
        configs.append(config)

    summary["years"] = sorted(years)
    summary["configs"] = configs
    return summary


if __name__ == "__main__":
    raise SystemExit(main())
