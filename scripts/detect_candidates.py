#!/usr/bin/env python3
"""Detect changed candidate/support_dataset configs from a git diff.

Replaces the inline Python logic previously duplicated in:
  - .github/workflows/pr-toolkit-check.yml (detect step)
  - .github/workflows/post-merge-candidate.yml (detect step)

Usage:
    # From CI (PR diff):
    python scripts/detect_candidates.py --base-sha $BASE_SHA --head-sha $HEAD_SHA

    # From local (all candidates):
    python scripts/detect_candidates.py

    # From local (specific slug):
    python scripts/detect_candidates.py --slug ispra-ru-costi-kg

Output JSON:
    {
      "has_items": true,
      "has_configs": true,
      "items": [{"kind": "candidate", "slug": "...", "root": "candidates/..."}],
      "configs": [
        {
          "kind": "candidate",
          "slug": "...",
          "config_path": "candidates/.../dataset.yml",
          "config_exists": true,
          "artifact_name": "...",
          "is_nested": false,
          "push_slug": "..."
        }
      ]
    }
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from toolkit.core.dataset_loader import load_dataset_manifest

ROOT = Path(__file__).resolve().parents[1]


def _resolve_year(cfg_path: Path) -> int:
    """Resolve the sample year from a dataset.yml — last year in list."""
    try:
        manifest = load_dataset_manifest(cfg_path)
        years = manifest.get("years", [])
        return int(years[-1]) if years else 0
    except Exception:
        return 0


def _dataset_name(cfg_path: Path) -> str | None:
    """Read dataset.name from a dataset.yml — None if missing/unreadable."""
    try:
        manifest = load_dataset_manifest(cfg_path)
        return manifest.get("name")
    except Exception:
        return None


def _git_diff_files(base_sha: str | None, head_sha: str) -> list[str]:
    """Return list of file paths changed between base and head."""
    if base_sha:
        result = subprocess.run(
            ["git", "diff", "--name-only", base_sha, head_sha],
            capture_output=True, text=True, cwd=ROOT,
        )
    else:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            capture_output=True, text=True, cwd=ROOT,
        )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, result.args, result.stdout, result.stderr
        )
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]


def _read_stdin_files() -> list[str]:
    """Read newline-separated file paths from stdin."""
    return [line.strip() for line in sys.stdin if line.strip()]


def _detect_from_files(files: list[str]) -> tuple[list[dict], list[dict]]:
    """Detect candidate/support roots and configs from file list."""
    seen: dict[tuple[str, str], dict] = {}
    for file_name in files:
        path = Path(file_name)
        parts = path.parts
        if len(parts) < 2:
            continue
        if parts[0] == "candidates":
            seen[("candidates", parts[1])] = {
                "kind": "candidate",
                "slug": parts[1],
                "root": f"candidates/{parts[1]}",
            }
        elif parts[0] == "support_datasets":
            seen[("support_datasets", parts[1])] = {
                "kind": "support_dataset",
                "slug": parts[1],
                "root": f"support_datasets/{parts[1]}",
            }
        elif parts[0] == "compose":
            seen[("compose", parts[1])] = {
                "kind": "compose",
                "slug": parts[1],
                "root": f"compose/{parts[1]}",
            }

    items = sorted(seen.values(), key=lambda item: (item["kind"], item["slug"]))
    configs: list[dict[str, Any]] = []

    for item in items:
        root = Path(item["root"])
        sources_root = root / "sources"
        if sources_root.is_dir():
            for source_dir in sorted(sources_root.iterdir()):
                if not source_dir.is_dir():
                    continue
                config_path = source_dir / "dataset.yml"
                if not config_path.exists():
                    continue
                configs.append({
                    **item,
                    "config_path": config_path.as_posix(),
                    "config_exists": True,
                    "push_slug": f"{item['slug']}_{source_dir.name}",
                    "artifact_name": f"{item['slug']}-{source_dir.name}",
                    "year": _resolve_year(config_path),
                    "is_nested": True,
                })
        else:
            config_path = root / "dataset.yml"
            if not config_path.exists():
                continue
            ds_name = _dataset_name(config_path)
            configs.append({
                **item,
                "config_path": config_path.as_posix(),
                "config_exists": True,
                "push_slug": ds_name or item["slug"],
                "artifact_name": item["slug"],
                "year": _resolve_year(config_path),
                "is_nested": False,
            })

    return items, configs


def detect_candidates(
    base_sha: str | None = None,
    head_sha: str | None = None,
    slug: str | None = None,
    files: list[str] | None = None,
) -> dict[str, Any]:
    """Main detection function. Returns dict with items and configs.

    Supports three modes:
      - git diff (base_sha + head_sha)
      - stdin file list (files param, from 'gh pr view --json files')
      - local slug filter (slug param)
    """
    if files is not None:
        # Called from post-merge with gh pr view files
        items, configs = _detect_from_files(files)
    elif slug:
        # Detect only a specific slug (local use)
        root_candidates = ROOT / "candidates" / slug
        root_support = ROOT / "support_datasets" / slug
        items = []
        configs = []

        if root_candidates.exists():
            kind = "candidate"
            root = f"candidates/{slug}"
            items.append({"kind": kind, "slug": slug, "root": root})
            sources_root = root_candidates / "sources"
            if sources_root.is_dir():
                for source_dir in sorted(sources_root.iterdir()):
                    if not source_dir.is_dir():
                        continue
                    cfg = source_dir / "dataset.yml"
                    configs.append({
                        "kind": kind, "slug": slug, "config_path": cfg.as_posix(),
                        "config_exists": cfg.exists(),
                        "push_slug": f"{slug}_{source_dir.name}",
                        "artifact_name": f"{slug}-{source_dir.name}",
                        "year": _resolve_year(cfg) if cfg.exists() else 0,
                        "is_nested": True,
                    })
            else:
                cfg = root_candidates / "dataset.yml"
                cfg_exists = cfg.exists()
                ds_name = _dataset_name(cfg) if cfg_exists else None
                configs.append({
                    "kind": kind, "slug": slug, "config_path": cfg.as_posix(),
                    "config_exists": cfg_exists,
                    "push_slug": ds_name or slug,
                    "artifact_name": slug,
                    "year": _resolve_year(cfg) if cfg_exists else 0,
                    "is_nested": False,
                })
        root_compose = ROOT / "compose" / slug
        if root_compose.exists():
            kind = "compose"
            root = f"compose/{slug}"
            items.append({"kind": kind, "slug": slug, "root": root})
            cfg = root_compose / "dataset.yml"
            configs.append({
                "kind": kind, "slug": slug, "config_path": cfg.as_posix(),
                "config_exists": cfg.exists(),
                "push_slug": slug, "artifact_name": slug,
                "year": _resolve_year(cfg) if cfg.exists() else 0,
                "is_nested": False,
            })
        elif root_support.exists():
            kind = "support_dataset"
            root = f"support_datasets/{slug}"
            items.append({"kind": kind, "slug": slug, "root": root})
            cfg = root_support / "dataset.yml"
            configs.append({
                "kind": kind, "slug": slug, "config_path": cfg.as_posix(),
                "config_exists": cfg.exists(),
                "push_slug": slug, "artifact_name": slug,
                "year": _resolve_year(cfg) if cfg.exists() else 0,
                "is_nested": False,
            })
    else:
        # Git diff mode
        if head_sha is None:
            head_sha = "HEAD"
        files = _git_diff_files(base_sha, head_sha)
        items, configs = _detect_from_files(files)

    return {
        "has_items": bool(items),
        "has_configs": bool(configs),
        "items": items,
        "configs": configs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-sha", help="Base commit SHA for git diff")
    parser.add_argument("--head-sha", help="Head commit SHA for git diff (default: HEAD)")
    parser.add_argument("--slug", help="Detect only a specific slug (local use)")
    parser.add_argument("--files", action="store_true", help="Read file list from stdin (gh pr view mode)")
    parser.add_argument("--json", action="store_true", help="Output JSON (default: text summary)")

    args = parser.parse_args()

    base = args.base_sha or None
    head = args.head_sha or "HEAD"

    files_input = None
    if args.files:
        files_input = _read_stdin_files()

    result = detect_candidates(
        base_sha=base,
        head_sha=head,
        slug=args.slug,
        files=files_input,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    # Human-readable output
    print(f"items: {len(result['items'])} | configs: {len(result['configs'])}")
    for item in result["items"]:
        print(f"  [{item['kind']}] {item['slug']} @ {item['root']}")
    for cfg in result["configs"]:
        nested = " [nested]" if cfg["is_nested"] else ""
        print(f"  → {cfg['config_path']}{nested} (artifact: {cfg['artifact_name']})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
