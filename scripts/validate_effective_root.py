from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def inspect_root(toolkit_dir: Path, config_path: Path) -> Path:
    cmd = [
        sys.executable,
        "-m",
        "toolkit.cli.app",
        "inspect",
        "paths",
        "--config",
        str(config_path),
        "--json",
    ]
    result = subprocess.run(
        cmd,
        cwd=toolkit_dir,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    if isinstance(payload, list):
        root = payload[0]["root"]
    else:
        root = payload["root"]
    return Path(root).resolve()


def main() -> int:
    if len(sys.argv) < 3:
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
        actual_root = inspect_root(toolkit_dir, config_path)
        print(f"{config_path.relative_to(repo_root)} -> {actual_root}")
        if actual_root != expected_root:
            failures.append(
                f"{config_path.relative_to(repo_root)} resolves root to {actual_root}, expected {expected_root}"
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
