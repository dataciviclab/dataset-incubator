"""Genera l'artifact registry del repo: registry.json (fusion ADR).

Wrapper sottile sul builder condiviso ``toolkit.registry`` (il toolkit ospita la
logica di generazione, riusando config model/path resolver/run_state/parquet_schema):
qui solo layout, path contract e scrittura.

Fusion ADR (toolkit v1.49.0): il builder produce UNICO ``registry.json`` con le
sezioni datasets/marts/signals/codelists/entities. Le proiezioni legacy
(clean_catalog.json/pipeline_signals.json/entity_graph.json) sono state rimosse
dopo la migrazione di tutti i consumer a registry.json.

Layout dataset-incubator:
- dataset.yml in ``candidates/*/``, ``compose/*/`` e ``support_datasets/*/``;
- parquet e run records in ``out/data/`` (root dichiarato nei dataset.yml);
- GCS: ``gs://dataciviclab-{clean,mart}/{slug}/{year}/`` (layout year, default).

Il catalogo esistente (registry.json committato) preserva i metadata editoriali
e le entry dei dataset non runnati in questo run: il post-merge esegue solo i
dataset cambiati (pattern eurostat), il resto resta dal catalogo.

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
    """Carica existing dal registry.json unico (se presente).

    Returns:
        (existing_catalog, existing_signals): dict di sezioni (o None).
    """
    registry_path = out / "registry.json"
    if not registry_path.is_file():
        return None, None
    try:
        existing = json.loads(registry_path.read_text(encoding="utf-8"))
        return (
            {
                "datasets": existing.get("datasets", []),
                "marts": existing.get("marts", []),
            },
            {"signals": existing.get("signals", [])},
        )
    except json.JSONDecodeError:
        print(
            "WARN: registry.json esistente illeggibile — riparto da zero",
            file=sys.stderr,
        )
        return None, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--write",
        action="store_true",
        help="Scrive registry.json in registry/ (default: dry-run)",
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
        print("Artifact NON scritto: errori di validazione.", file=sys.stderr)
        return 1

    registry = result["registry"]
    if not args.write:
        s = registry["summary"]
        print(
            f"[dry-run] registry.json — datasets {s['datasets']}, "
            f"marts {s['marts']}, signals {s['signals']}"
        )
        print("Usa --write per scrivere il file.")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    out_path = args.out / "registry.json"
    out_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"scritto {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
