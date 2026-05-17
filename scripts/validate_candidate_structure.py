from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]

LayoutType = Literal[
    "single-source", "multi-source", "ambiguous", "unknown",
    "support-dataset", "compose",
]


def detect_candidate_layout(base_dir: Path) -> dict:
    """Shared layout detection for candidate, support_dataset, and compose structures.

    Returns a dict with:
      layout: LayoutType — one of the six literal values
      has_root_dataset: bool
      has_sources: bool
    """
    if base_dir.parts[-2] == "support_datasets":
        return {
            "layout": "support-dataset",
            "has_root_dataset": (base_dir / "dataset.yml").exists(),
            "has_sources": False,
        }

    if base_dir.parts[-2] == "compose":
        return {
            "layout": "compose",
            "has_root_dataset": (base_dir / "dataset.yml").exists(),
            "has_sources": False,
        }

    has_root_dataset = (base_dir / "dataset.yml").exists()
    has_sources = (base_dir / "sources").is_dir()

    if has_root_dataset and has_sources:
        return {"layout": "ambiguous", "has_root_dataset": True, "has_sources": True}
    elif has_root_dataset:
        return {"layout": "single-source", "has_root_dataset": True, "has_sources": False}
    elif has_sources:
        return {"layout": "multi-source", "has_root_dataset": False, "has_sources": True}
    else:
        return {"layout": "unknown", "has_root_dataset": False, "has_sources": False}


def has_mart_sql(sql_dir: Path) -> bool:
    has_root_mart = any(
        path.name.startswith("mart") and path.suffix == ".sql"
        for path in sql_dir.glob("*.sql")
    )
    has_nested_mart = any(path.suffix == ".sql" for path in (sql_dir / "mart").glob("*.sql"))
    return has_root_mart or has_nested_mart


def validate_root_docs(base_dir: Path, failures: list[str]) -> None:
    if not (base_dir / "README.md").exists():
        failures.append(f"missing {base_dir.relative_to(ROOT) / 'README.md'}")
    if not (base_dir / "notes.md").exists():
        failures.append(f"missing {base_dir.relative_to(ROOT) / 'notes.md'}")


def validate_single_source(base_dir: Path, failures: list[str]) -> None:
    dataset_yml = base_dir / "dataset.yml"
    sql_dir = base_dir / "sql"

    if not dataset_yml.exists():
        failures.append(f"missing {dataset_yml.relative_to(ROOT)}")
    if not sql_dir.is_dir():
        failures.append(f"missing {sql_dir.relative_to(ROOT)}")
        return
    if not (sql_dir / "clean.sql").exists():
        failures.append(f"missing {(sql_dir / 'clean.sql').relative_to(ROOT)}")
    if not has_mart_sql(sql_dir):
        failures.append(f"missing mart*.sql under {sql_dir.relative_to(ROOT)}")


def validate_compose_root(base_dir: Path, failures: list[str]) -> None:
    """Validate a standalone compose dataset (mart-only, no raw/clean)."""
    dataset_yml = base_dir / "dataset.yml"
    sql_dir = base_dir / "sql"

    if not dataset_yml.exists():
        failures.append(f"missing {dataset_yml.relative_to(ROOT)}")
    if not sql_dir.is_dir():
        failures.append(f"missing {sql_dir.relative_to(ROOT)}")
        return
    if not has_mart_sql(sql_dir):
        failures.append(f"missing mart*.sql under {sql_dir.relative_to(ROOT)}")
    # Compose non ha raw/clean — e' mart-only.


def validate_compose(base_dir: Path, failures: list[str]) -> None:
    compose_dir = base_dir / "compose"
    if not compose_dir.exists():
        return

    dataset_yml = compose_dir / "dataset.yml"
    sql_dir = compose_dir / "sql"

    if not dataset_yml.exists():
        failures.append(f"missing {dataset_yml.relative_to(ROOT)}")
    if not sql_dir.is_dir():
        failures.append(f"missing {sql_dir.relative_to(ROOT)}")
        return
    if not has_mart_sql(sql_dir):
        failures.append(f"missing mart*.sql under {sql_dir.relative_to(ROOT)}")


def validate_multi_source(base_dir: Path, failures: list[str]) -> None:
    sources_dir = base_dir / "sources"
    source_dirs = sorted(path for path in sources_dir.iterdir() if path.is_dir())
    if not source_dirs:
        failures.append(f"missing source directories under {sources_dir.relative_to(ROOT)}")
        return

    for source_dir in source_dirs:
        dataset_yml = source_dir / "dataset.yml"
        sql_dir = source_dir / "sql"

        if not dataset_yml.exists():
            failures.append(f"missing {dataset_yml.relative_to(ROOT)}")
        if not sql_dir.is_dir():
            failures.append(f"missing {sql_dir.relative_to(ROOT)}")
            continue
        if not (sql_dir / "clean.sql").exists():
            failures.append(f"missing {(sql_dir / 'clean.sql').relative_to(ROOT)}")
        if not has_mart_sql(sql_dir):
            failures.append(f"missing mart*.sql under {sql_dir.relative_to(ROOT)}")

    validate_compose(base_dir, failures)


def validate_entry(base_dir: Path, failures: list[str]) -> None:
    rel_str = base_dir.relative_to(ROOT).as_posix()

    info = detect_candidate_layout(base_dir)
    layout = info["layout"]

    # Compose non richiede README/notes (e' mart-only, non ha candidate lifecycle)
    if layout != "compose":
        validate_root_docs(base_dir, failures)

    info = detect_candidate_layout(base_dir)
    layout = info["layout"]

    if layout == "support-dataset":
        validate_single_source(base_dir, failures)
        return

    if layout == "ambiguous":
        failures.append(
            f"{rel_str} has ambiguous structure: root dataset.yml and sources/ cannot coexist"
        )
        return

    if layout == "single-source":
        validate_single_source(base_dir, failures)
        return

    if layout == "compose":
        validate_compose_root(base_dir, failures)
        return

    if layout == "multi-source":
        validate_multi_source(base_dir, failures)
        return

    failures.append(
        f"{rel_str} has no valid structure: expected root dataset.yml or sources/"
    )


def main() -> int:
    failures: list[str] = []

    for section in ("compose", "candidates", "support_datasets"):
        base = ROOT / section
        if not base.exists():
            continue
        for entry in sorted(path for path in base.iterdir() if path.is_dir()):
            validate_entry(entry, failures)

    if failures:
        print("Candidate structure validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("Candidate structure validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
