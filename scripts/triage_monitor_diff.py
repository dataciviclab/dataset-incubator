"""Triage candidate DI impattati da diff monitor source-observatory.

Legge un diff_summary.json prodotto da SO resource_monitor e un mapping
source_id -> candidate slug, e produce un report di triage (Markdown + JSON).

Nessun side effect: non apre issue, non avvia pipeline, non scrive nel repo.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


def load_map(map_path: Path) -> dict[str, list[str]]:
    """Carica il mapping source_id -> candidates. Restituisce solo le entry active."""
    data = yaml.safe_load(map_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"source_candidate_map.yml non valido: atteso dict, trovato {type(data).__name__}")
    result: dict[str, list[str]] = {}
    for i, entry in enumerate(data.get("mappings", [])):
        if not isinstance(entry, dict) or "source_id" not in entry:
            raise ValueError(f"mappings[{i}]: entry non valida, 'source_id' richiesto")
        if entry.get("active", True):
            result[entry["source_id"]] = entry.get("candidates", [])
    return result


def triage(diff: dict, source_map: dict[str, list[str]]) -> dict:
    """Calcola candidate impattati a partire dal diff_summary."""
    impacted: list[dict] = []
    for source_id in diff.get("sources_with_changes", []):
        candidates = source_map.get(source_id, [])
        if not candidates:
            continue
        source_diff = diff.get("per_source", {}).get(source_id, {})
        impacted.append({
            "source_id": source_id,
            "candidates": candidates,
            "new": source_diff.get("new", 0),
            "changed": source_diff.get("changed", 0),
            "removed": source_diff.get("removed", 0),
        })

    errors_in_map: list[str] = [
        source_id
        for source_id in diff.get("sources_with_errors", [])
        if source_id in source_map
    ]

    return {
        "generated_at": diff.get("generated_at_utc", diff.get("generated_at", "")),
        "impacted_count": len(impacted),
        "impacted": impacted,
        "sources_with_errors_in_map": errors_in_map,
    }


def render_report(result: dict) -> str:
    lines = ["# Monitor diff triage - candidate impattati", ""]
    lines.append(f"Diff generato: {result['generated_at']}")
    lines.append("")

    if result["impacted_count"] == 0:
        lines.append(
            "**Nessuna azione richiesta.** "
            "Nessun candidate DI impattato da cambi nelle fonti monitorate."
        )
    else:
        lines.append(
            f"**{result['impacted_count']} fonte/i con cambi che impattano candidate DI:**"
        )
        lines.append("")
        for item in result["impacted"]:
            cand_list = ", ".join(f"`{c}`" for c in item["candidates"])
            lines.append(f"- **{item['source_id']}** -> {cand_list}")
            lines.append(
                f"  new: {item['new']}, changed: {item['changed']}, removed: {item['removed']}"
            )

    if result["sources_with_errors_in_map"]:
        lines.append("")
        lines.append("**Fonti con errori (monitor) presenti nel mapping DI:**")
        for s in result["sources_with_errors_in_map"]:
            lines.append(f"- {s}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Triage candidate DI impattati da diff monitor SO."
    )
    parser.add_argument(
        "--diff", required=True, type=Path, help="Path al diff_summary.json di SO"
    )
    parser.add_argument(
        "--map", required=True, type=Path, help="Path al source_candidate_map.yml"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("."), help="Directory di output"
    )
    args = parser.parse_args()

    if not args.diff.exists():
        print(f"Errore: file diff non trovato: {args.diff}", file=sys.stderr)
        return 1
    if not args.map.exists():
        print(f"Errore: file map non trovato: {args.map}", file=sys.stderr)
        return 1

    diff = json.loads(args.diff.read_text(encoding="utf-8"))
    source_map = load_map(args.map)
    result = triage(diff, source_map)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    report_path = args.output_dir / "triage_report.md"
    result_path = args.output_dir / "triage_result.json"

    report_path.write_text(render_report(result), encoding="utf-8")
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Report:              {report_path}")
    print(f"Result:              {result_path}")
    print(f"Candidate impattati: {result['impacted_count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
