from __future__ import annotations

import sys
from pathlib import Path


def inspect_root(repo_root: Path, toolkit_dir: Path, config_path: Path) -> Path:
    toolkit_root = toolkit_dir.resolve()
    if str(toolkit_root) not in sys.path:
        sys.path.insert(0, str(toolkit_root))

    try:
        from toolkit.core.config import load_config
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Toolkit import failed. Install toolkit in the current Python environment first, "
            "for example: python -m pip install -e ./toolkit"
        ) from exc

    cfg = load_config(config_path, repo_root=repo_root)
    return cfg.root.resolve()


def main() -> int:
    if len(sys.argv) < 4:
        print(
            "Usage: validate_effective_root.py <repo_root> <toolkit_dir> <dataset.yml> [<dataset.yml> ...]",
            file=sys.stderr,
        )
        return 2

    repo_root = Path(sys.argv[1]).resolve()
    toolkit_dir = Path(sys.argv[2]).resolve()
    config_paths = [Path(arg).resolve() for arg in sys.argv[3:]]
    expected_root = (repo_root / "out").resolve()

    failures: list[str] = []

    for config_path in config_paths:
        rel_config = config_path.relative_to(repo_root)
        try:
            actual_root = inspect_root(repo_root, toolkit_dir, config_path)
        except Exception as exc:
            failures.append(
                f"{rel_config} failed root validation: {type(exc).__name__}: {exc}"
            )
            continue

        print(f"{rel_config} -> {actual_root}")
        if actual_root != expected_root:
            failures.append(
                f"{rel_config} resolves root to {actual_root}, expected {expected_root}"
            )

    if failures:
        print("\nEffective root validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"\nAll checked dataset.yml files resolve to {expected_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
