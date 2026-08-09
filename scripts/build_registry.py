"""Genera gli artifact registry del repo: registry.json (fusion) + proiezioni legacy.

Wrapper sottile sul builder condiviso ``toolkit.registry`` (il toolkit ospita la
logica di generazione, riusando config model/path resolver/run_state/parquet_schema):
qui solo layout, path contract e scrittura.

Fusion ADR (toolkit v1.49.0): il builder produce un UNICO ``registry.json`` con le
sezioni datasets/marts/signals/codelists/entities. Per non rompere i consumer
attuali (data-explorer, agent-context-builder, smoke-weekly) il
wrapper scrive in aggiunta le proiezioni legacy ``clean_catalog.json``,
``pipeline_signals.json`` e ``entity_graph.json`` derivandole dalle stesse sezioni.
La rimozione delle proiezioni avviene dopo la migrazione dei consumer.

Layout dataset-incubator:
- dataset.yml in ``candidates/*/``, ``compose/*/`` e ``support_datasets/*/``;
- parquet e run records in ``out/data/`` (root dichiarato nei dataset.yml);
- GCS: ``gs://dataciviclab-{clean,mart}/{slug}/{year}/`` (layout year, default).

Il catalogo esistente (registry.json o clean_catalog.json committato) preserva i
metadata editoriali e le entry dei dataset non runnati in questo run: il post-merge
esegue solo i dataset cambiati (pattern eurostat), il resto resta dal catalogo.

Usage:
    python scripts/build_registry.py            # dry-run (stampa riepilogo)
    python scripts/build_registry.py --write    # scrive in registry/
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "registry"


def _load_existing(out: Path) -> tuple[dict | None, dict | None]:
    """Carica existing dal registry.json unico, con fallback legacy.

    Returns:
        (existing_catalog, existing_signals): dict di sezioni (o None).
    """
    registry_path = out / "registry.json"
    if registry_path.is_file():
        try:
            existing = json.loads(registry_path.read_text(encoding="utf-8"))
            return (
                {"datasets": existing.get("datasets", [])},
                {"signals": existing.get("signals", [])},
            )
        except json.JSONDecodeError:
            print(
                "WARN: registry.json esistente illeggibile — riparto da zero",
                file=sys.stderr,
            )

    # Fallback legacy: i vecchi artifact separati (repo non ancora migrati)
    existing_catalog = None
    legacy_catalog = out / "clean_catalog.json"
    if legacy_catalog.is_file():
        try:
            existing_catalog = json.loads(legacy_catalog.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(
                "WARN: clean_catalog.json esistente illeggibile — riparto da zero",
                file=sys.stderr,
            )

    existing_signals = None
    legacy_signals = out / "pipeline_signals.json"
    if legacy_signals.is_file():
        try:
            existing_signals = json.loads(legacy_signals.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(
                "WARN: pipeline_signals.json esistente illeggibile — riparto da zero",
                file=sys.stderr,
            )
    return existing_catalog, existing_signals


def _legacy_header(name: tuple[str, ...], path: Path, registry: dict) -> dict:
    """Header legacy per clean_catalog.json/pipeline_signals.json.

    Preserva i campi di presentazione dal file esistente (se presente),
    altrimenti default dal registry unico.
    """
    if path.is_file():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
            return {k: old.get(k) for k in name if k in old}
        except json.JSONDecodeError:
            pass
    return {}


def _project_clean_catalog(registry: dict, out: Path) -> dict:
    """Proiezione legacy clean_catalog.json dalla sezione datasets del registry."""
    path = out / "clean_catalog.json"
    header = _legacy_header(
        ("schema_version", "name", "description", "source_repo", "updated_at"), path, registry
    )
    return {
        "schema_version": header.get("schema_version", 1),
        "name": header.get("name", "Lab Clean Registry"),
        "description": header.get(
            "description",
            "Catalogo canonico dei clean parquet pubblici prodotti o adottati da dataset-incubator.",
        ),
        "source_repo": header.get("source_repo", registry.get("source_repo")),
        "updated_at": header.get("updated_at", registry.get("updated_at")),
        "datasets": registry.get("datasets", []),
    }


def _project_pipeline_signals(registry: dict, out: Path) -> dict:
    """Proiezione legacy pipeline_signals.json dalla sezione signals del registry."""
    path = out / "pipeline_signals.json"
    header = _legacy_header(("schema_version", "generated_at", "repo", "topic"), path, registry)
    signals = registry.get("signals", [])
    by_status = {"ok": 0, "warn": 0, "error": 0}
    for s in signals:
        by_status[s.get("status", "error")] = by_status.get(s.get("status", "error"), 0) + 1
    return {
        "schema_version": header.get("schema_version", "1"),
        "generated_at": header.get("generated_at", registry.get("updated_at")),
        "repo": header.get("repo", registry.get("repo")),
        "topic": header.get("topic", "pipeline_state"),
        "summary": {"total": len(signals), "by_status": by_status},
        "signals": signals,
    }


def _project_entity_graph(registry: dict) -> dict:
    """Proiezione legacy entity_graph.json dalla sezione entities del registry."""
    entities = registry.get("entities", {})
    return {
        "schema_version": 1,
        "generated_from": entities.get("generated_from", "registry.json"),
        "entities": entities.get("entities", {}),
        "bridges": entities.get("bridges", []),
        "summary": entities.get("summary", {}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--write",
        action="store_true",
        help="Scrive gli artifact in registry/ (default: dry-run)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Dir di output (default: {DEFAULT_OUT})",
    )
    args = parser.parse_args()

    try:
        from toolkit.registry import PathContract, RepoLayout
        from toolkit.registry.builders import build_registry
    except ImportError as exc:  # pragma: no cover
        print(
            f"ERRORE: toolkit.registry non disponibile ({exc}).\n"
            "Serve toolkit >= v1.49.0 (modulo registry su main, fusion ADR).",
            file=sys.stderr,
        )
        return 1

    layout = RepoLayout(
        repo_root=ROOT,
        dataset_dirs=("candidates", "compose", "support_datasets"),
        source_repo="dataciviclab/dataset-incubator",
    )
    contract = PathContract()  # default: layout year, nessun prefix

    existing_catalog, existing_signals = _load_existing(args.out)

    result = build_registry(
        layout,
        path_contract=contract,
        existing_catalog=existing_catalog,
        existing_signals=existing_signals,
    )

    # Errori già categorizzati dal builder: derive = warning (checkout
    # parziali), validation = bloccanti (artifact non conforme allo schema).
    all_warnings: list[str] = []
    all_real: list[str] = []
    for artifact, errors in result["errors"].items():
        all_warnings.extend(f"{artifact}: {e}" for e in errors["derive"])
        all_real.extend(f"{artifact}: {e}" for e in errors["validation"])

    for w in all_warnings:
        print(f"WARN: {w}", file=sys.stderr)

    if all_real:
        for e in all_real:
            print(f"ERROR: {e}", file=sys.stderr)
        print("Artifact NON scritti: errori di validazione.", file=sys.stderr)
        return 1

    registry = result["registry"]
    if not args.write:
        s = registry["summary"]
        print(
            f"[dry-run] registry.json — datasets {s['datasets']}, "
            f"marts {s['marts']}, signals {s['signals']} "
            f"(+ proiezioni legacy clean_catalog/pipeline_signals/entity_graph)"
        )
        print("Usa --write per scrivere i file.")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)

    # Artifact unico (fusion ADR)
    out_path = args.out / "registry.json"
    out_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"scritto {out_path}")

    # Proiezioni legacy per i consumer non ancora migrati
    for name, payload in (
        ("clean_catalog", _project_clean_catalog(registry, args.out)),
        ("pipeline_signals", _project_pipeline_signals(registry, args.out)),
        ("entity_graph", _project_entity_graph(registry)),
    ):
        legacy_path = args.out / f"{name}.json"
        legacy_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"scritto {legacy_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
