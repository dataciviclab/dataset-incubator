from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.clean_query_mcp import server  # noqa: E402


# Dataset hub da testare sempre (verificano bridge e hub centrality)
HUB_SLUGS: set[str] = {
    "comuni_master",
    "bdap_anagrafe_enti",
    "unified_comuni",
    "anac_bandi_gara",
    "popolazione_istat_comunale_2019_2025",
    "opencivitas_fsc_2025_rso",
    "irpef_comunale",
    "pnrr_progetti",
    "mim_anagrafica_scuole_statali",
    "dipendenti_pubblici",
    "siope_bilancio_unificato",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smoke test clean-query MCP — testa hub + campione rappresentativo."
    )
    parser.add_argument("--dataset", help="Limit smoke test to one dataset slug.")
    parser.add_argument(
        "--max-datasets",
        type=int,
        default=25,
        help="Max dataset da testare (default 25, 0 = tutti).",
    )
    args = parser.parse_args()

    all_datasets = server.load_catalog()
    if args.dataset:
        all_datasets = [item for item in all_datasets if item["slug"] == args.dataset]
        if not all_datasets:
            print(f"Dataset non trovato: {args.dataset}", file=sys.stderr)
            return 2

    # Ordina: hub first, poi il resto (per priorità)
    hub_items = [d for d in all_datasets if d["slug"] in HUB_SLUGS]
    other_items = [d for d in all_datasets if d["slug"] not in HUB_SLUGS]

    max_ds = args.max_datasets
    if max_ds == 0:
        max_ds = len(all_datasets)

    datasets = hub_items[:]  # hub sempre inclusi
    remaining_slots = max_ds - len(datasets)
    if remaining_slots > 0:
        datasets.extend(other_items[:remaining_slots])

    print(
        f"Smoke test: {len(datasets)}/{len(all_datasets)} dataset "
        f"({len(hub_items)} hub + {max(0, remaining_slots)} altri)"
    )

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
