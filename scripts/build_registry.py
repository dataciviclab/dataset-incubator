"""Genera gli artifact registry del repo: clean_catalog, mart_catalog, pipeline_signals, codelists.

Wrapper sottile sul builder condiviso ``toolkit.registry`` (il toolkit ospita la
logica di generazione, riusando config model/path resolver/run_state/parquet_schema):
qui solo layout, path contract e scrittura.

Layout dataset-incubator:
- dataset.yml in ``candidates/*/``, ``compose/*/`` e ``support_datasets/*/``;
- parquet e run records in ``out/data/`` (root dichiarato nei dataset.yml);
- GCS: ``gs://dataciviclab-{clean,mart}/{slug}/{year}/`` (layout year, default).

Il catalogo esistente (registry/clean_catalog.json committato) preserva i metadata
editoriali e le entry dei dataset non runnati in questo run: il post-merge esegue
solo i dataset cambiati (pattern eurostat), il resto resta dal catalogo.

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
    parser.add_argument(
        "--check-gcs",
        action="store_true",
        help="Verifica che le location gs:// del clean_catalog risolvano a parquet "
        "pubblici (derive_mode='check-gcs'). Non scrive nulla.",
    )
    args = parser.parse_args()

    try:
        from toolkit.registry import PathContract, RepoLayout
        from toolkit.registry.builders import build_registry
    except ImportError as exc:  # pragma: no cover
        print(
            f"ERRORE: toolkit.registry non disponibile ({exc}).\n"
            "Serve toolkit con il modulo registry (PR #452, in attesa di merge su main).",
            file=sys.stderr,
        )
        return 1

    layout = RepoLayout(
        repo_root=ROOT,
        dataset_dirs=("candidates", "compose", "support_datasets"),
        source_repo="dataciviclab/dataset-incubator",
    )
    contract = PathContract()  # default: layout year, nessun prefix

    existing = None
    existing_path = args.out / "clean_catalog.json"
    if existing_path.is_file():
        try:
            existing = json.loads(existing_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(
                "WARN: clean_catalog.json esistente illeggibile — riparto da zero",
                file=sys.stderr,
            )

    existing_signals = None
    signals_path = args.out / "pipeline_signals.json"
    if signals_path.is_file():
        try:
            existing_signals = json.loads(signals_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(
                "WARN: pipeline_signals.json esistente illeggibile — riparto da zero",
                file=sys.stderr,
            )

    result = build_registry(
        layout,
        path_contract=contract,
        existing_catalog=existing,
        existing_signals=existing_signals,
        derive_mode="check-gcs" if args.check_gcs else "local",
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

    if not args.write:
        for name in ("clean_catalog", "mart_catalog", "pipeline_signals", "codelists"):
            payload = result[name]
            n = (
                len(payload["datasets"])
                if name == "clean_catalog"
                else (
                    len(payload["marts"])
                    if name == "mart_catalog"
                    else (
                        payload["summary"]["total"]
                        if name == "pipeline_signals"
                        else len(payload["codelists"])
                    )
                )
            )
            print(f"[dry-run] {name}.json — {n} entries")
        print("Usa --write per scrivere i file.")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    for name in ("clean_catalog", "mart_catalog", "pipeline_signals", "codelists"):
        payload = result[name]
        out_path = args.out / f"{name}.json"
        out_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"scritto {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
