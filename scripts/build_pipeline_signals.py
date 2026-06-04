"""Build registry/pipeline_signals.json for ACB consumption.

Scans active candidates in dataset-incubator and produces a signal file
following the repo-signals standard (see agent-context-builder/schemas/repo-signals.md).

Status logic:
  ok   — structure valid + mart SQL present
  warn — structure valid but no mart SQL yet
  error — structural issue (missing dataset.yml, clean.sql, or ambiguous layout)

Run:
  python scripts/build_pipeline_signals.py [--out registry/pipeline_signals.json]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import jsonschema

from toolkit.core.dataset_loader import (
    detect_candidate_layout,
    has_mart_sql,
    load_dataset_manifest,
)

ROOT = Path(__file__).resolve().parents[1]

_SCHEMA_DIR = ROOT / "registry"


def _validate_schema(instance: dict) -> None:
    """Validate a dict against registry/pipeline_signals.schema.json."""
    schema_path = _SCHEMA_DIR / "pipeline_signals.schema.json"
    if not schema_path.exists():
        print("⚠️  pipeline_signals.schema.json non trovato — skip validazione")
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(instance=instance, schema=schema)
    except jsonschema.ValidationError as exc:
        print(f"❌ Validazione fallita (pipeline_signals.schema.json): {exc.message}")
        raise

# ---------------------------------------------------------------------------
# Layout resolution — delegata a toolkit.core.dataset_loader
# ---------------------------------------------------------------------------

_SUPPORT_DATASETS_DIR = ROOT / "support_datasets"


def _resolve_layout_name(base_dir: Path) -> str:
    """Rileva il layout, con gestione DI-specifica per support-dataset."""
    # support-dataset: directory in support_datasets/ con dataset.yml
    if _SUPPORT_DATASETS_DIR in base_dir.parents:
        yml = base_dir / "dataset.yml"
        if yml.exists():
            return "support-dataset"

    return detect_candidate_layout(base_dir)


def _years_label(years: list) -> str:
    if not years:
        return "anni: ?"
    years = sorted(int(y) for y in years)
    if len(years) == 1:
        return f"anno {years[0]}"
    return f"anni {years[0]}-{years[-1]}"


def _source_names(sources: list[dict]) -> list[str]:
    return [s.get("name", "?") for s in sources if isinstance(s, dict)]


# ---------------------------------------------------------------------------
# Candidate introspection — reuses has_mart_sql and detect_candidate_layout
# from validate_candidate_structure, but does its own structure walk
# to avoid coupling with validate_entry() which is designed for CLI output.
# ---------------------------------------------------------------------------

def _inspect_single_source(base_dir: Path) -> dict:
    """Inspect a single-source candidate (root dataset.yml)."""
    yml_path = base_dir / "dataset.yml"
    sql_dir = base_dir / "sql"

    failures = []
    if not yml_path.exists():
        failures.append("missing dataset.yml")
    if not sql_dir.is_dir():
        failures.append("missing sql/")
    elif not (sql_dir / "clean.sql").exists():
        failures.append("missing sql/clean.sql")

    mart_ok = sql_dir.is_dir() and has_mart_sql(base_dir)

    manifest = load_dataset_manifest(yml_path) if yml_path.exists() else {}
    source_names = _source_names(manifest.get("sources", []))

    return {
        "pattern": "single-source",
        "years": manifest.get("years", []),
        "sources": source_names,
        "mart_ok": mart_ok,
        "failures": failures,
    }


def _inspect_compose(base_dir: Path) -> dict:
    """Inspect a compose dataset (mart-only, no raw/clean)."""
    yml_path = base_dir / "dataset.yml"
    sql_dir = base_dir / "sql"

    failures = []
    if not yml_path.exists():
        failures.append("missing dataset.yml")
    if not sql_dir.is_dir():
        failures.append("missing sql/")
    elif not has_mart_sql(base_dir):
        failures.append("missing mart*.sql under sql/")

    mart_ok = sql_dir.is_dir() and has_mart_sql(base_dir)

    manifest = load_dataset_manifest(yml_path) if yml_path.exists() else {}
    support_list = manifest.get("support", [])
    source_names = [s.get("name", "?") for s in support_list] if support_list else []

    return {
        "pattern": "compose",
        "years": manifest.get("years", []),
        "sources": source_names,
        "mart_ok": mart_ok,
        "failures": failures,
    }


def _inspect_multi_source(base_dir: Path) -> dict:
    """Inspect a multi-source candidate (sources/*/dataset.yml)."""
    sources_dir = base_dir / "sources"
    source_dirs = sorted(p for p in sources_dir.iterdir() if p.is_dir())

    failures = []
    all_years: list[int] = []
    all_sources: list[str] = []
    mart_ok = False

    for src_dir in source_dirs:
        yml_path = src_dir / "dataset.yml"
        sql_dir = src_dir / "sql"

        if not yml_path.exists():
            failures.append(f"missing {src_dir.name}/dataset.yml")
            continue
        if not sql_dir.is_dir():
            failures.append(f"missing {src_dir.name}/sql/")
            continue
        if not (sql_dir / "clean.sql").exists():
            failures.append(f"missing {src_dir.name}/sql/clean.sql")

        manifest = load_dataset_manifest(yml_path)
        years = [int(y) for y in manifest.get("years", [])]
        all_years.extend(years)
        all_sources.extend(_source_names(manifest.get("sources", [])))

        if has_mart_sql(src_dir):
            mart_ok = True

    # compose layer — if present, its mart overrides individual source mart
    compose_dir = base_dir / "compose"
    if compose_dir.is_dir():
        compose_sql = compose_dir / "sql"
        if compose_sql.is_dir() and has_mart_sql(compose_dir):
            mart_ok = True
        elif compose_sql.is_dir() and not has_mart_sql(compose_dir):
            failures.append("compose/sql/ present but missing mart SQL")

    return {
        "pattern": "multi-source",
        "years": sorted(set(all_years)),
        "sources": list(dict.fromkeys(all_sources)),  # deduplicated, order-preserving
        "mart_ok": mart_ok,
        "failures": failures,
    }


def _build_signal(slug: str, base_dir: Path) -> dict:
    """Build a single signal entry for a candidate."""
    from typing import Any

    # Leggi source_id dal dataset.yml se presente
    source_id = ""
    yml_path = base_dir / "dataset.yml"
    if yml_path.is_file():
        try:
            manifest = load_dataset_manifest(yml_path)
            source_id = manifest.get("source_id", "") or ""
        except Exception:
            pass

    layout_name = _resolve_layout_name(base_dir)

    info: dict[str, Any]
    if layout_name == "support-dataset":
        info = {
            "pattern": "support-dataset",
            "years": [],
            "sources": [],
            "mart_ok": (base_dir / "sql").is_dir() and has_mart_sql(base_dir),
            "failures": [],
        }
    elif layout_name == "single-source":
        info = _inspect_single_source(base_dir)
    elif layout_name == "compose":
        info = _inspect_compose(base_dir)
    elif layout_name == "multi-source":
        info = _inspect_multi_source(base_dir)
    else:
        info = {
            "pattern": "unknown",
            "years": [],
            "sources": [],
            "mart_ok": False,
            "failures": ["no dataset.yml and no sources/ directory"],
        }

    years_label = _years_label(info["years"])
    pattern = info["pattern"]
    sources = info["sources"]
    mart_label = "mart: sì" if info["mart_ok"] else "mart: no"

    if pattern == "multi-source":
        n = len(sources)
        src_label = f"multi-source ({n} {'fonte' if n == 1 else 'fonti'})"
    elif sources:
        src_label = f"fonte: {sources[0]}" if len(sources) == 1 else f"fonti: {', '.join(sources[:2])}"
    else:
        src_label = "fonte: ?"

    detail_parts = [years_label, src_label, mart_label]
    if info["failures"]:
        detail_parts.append("⚠ " + "; ".join(info["failures"]))
    detail = " — ".join(detail_parts)

    if info["failures"]:
        status = "error"
    elif not info["mart_ok"]:
        status = "warn"
    else:
        status = "ok"

    action = ""
    if status == "warn":
        action = "aggiungere mart SQL per completare il candidato"
    elif status == "error":
        if pattern == "ambiguous":
            action = "scegliere un layout: sources/ (multi-source) oppure solo dataset.yml root (single-source) — mai entrambi"
        else:
            action = "correggere la struttura del candidato"

    return {
        "id": slug,
        "source_id": source_id,
        "status": status,
        "label": slug,
        "detail": detail,
        "action": action,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_signals(out_path: Path) -> int:
    previous_sample_runs = load_previous_sample_runs(out_path)
    signals = []

    candidates_dir = ROOT / "candidates"
    if not candidates_dir.exists():
        print("No candidates/ directory found.", file=sys.stderr)
        return 1

    for entry in sorted(p for p in candidates_dir.iterdir() if p.is_dir()):
        slug = entry.name
        signal = _build_signal(slug, entry)
        if slug in previous_sample_runs:
            signal["sample_run"] = previous_sample_runs[slug]
        signals.append(signal)

    # support_datasets also use detect_candidate_layout and need to appear in signals
    support_dir = ROOT / "support_datasets"
    if support_dir.exists():
        for entry in sorted(p for p in support_dir.iterdir() if p.is_dir()):
            slug = entry.name
            signal = _build_signal(slug, entry)
            if slug in previous_sample_runs:
                signal["sample_run"] = previous_sample_runs[slug]
            signals.append(signal)

    # Compose datasets: mart-only, leggono output gia pubblicati via support:
    # ID prefissato con "compose:" per evitare collisioni con candidate omonimi.
    compose_dir = ROOT / "compose"
    if compose_dir.exists():
        for entry in sorted(p for p in compose_dir.iterdir() if p.is_dir()):
            slug = f"compose:{entry.name}"
            signal = _build_signal(slug, entry)
            # sample_run per compose usa ID senza prefisso (directory name)
            if entry.name in previous_sample_runs:
                signal["sample_run"] = previous_sample_runs[entry.name]
            signals.append(signal)

    by_status: dict[str, int] = {"ok": 0, "warn": 0, "error": 0}
    for s in signals:
        by_status[s["status"]] = by_status.get(s["status"], 0) + 1

    payload = {
        "schema_version": "1",
        "generated_at": date.today().isoformat(),
        "repo": "dataset-incubator",
        "topic": "pipeline_state",
        "summary": {
            "total": len(signals),
            "by_status": by_status,
        },
        "signals": signals,
    }

    _validate_schema(payload)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"pipeline_signals.json — {len(signals)} candidates ({by_status})")
    return 0


def load_previous_sample_runs(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    sample_runs = {}
    for signal in payload.get("signals", []):
        if not isinstance(signal, dict):
            continue
        signal_id = signal.get("id")
        sample_run = signal.get("sample_run")
        if signal_id and isinstance(sample_run, dict):
            sample_runs[signal_id] = sample_run
    return sample_runs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "registry" / "pipeline_signals.json",
        help="Output path (default: registry/pipeline_signals.json)",
    )
    args = parser.parse_args()
    return build_signals(args.out)


if __name__ == "__main__":
    raise SystemExit(main())
