from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "templates" / "candidate"
DEFAULT_CANDIDATES = ROOT / "candidates"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def build_replacements(args: argparse.Namespace) -> dict[str, str]:
    created_date = args.created_date or date.today().isoformat()
    source_url = args.source_url or "TODO"
    discussion_url = args.discussion_url or "TODO"
    issue_url = args.issue_url or "TODO"
    sql_slug = args.slug.replace("-", "_")

    return {
        "{slug}": args.slug,
        "{title}": args.title,
        "{discussion_url}": discussion_url,
        "{issue_url}": issue_url,
        "{source_url}": source_url,
        "{created_date}": created_date,
        "{{SLUG}}": args.slug,
        "{{TITLE}}": args.title,
        "{{DISCUSSION_URL}}": discussion_url,
        "{{ISSUE_URL}}": issue_url,
        "{{SOURCE_URL}}": source_url,
        "{{CREATED_DATE}}": created_date,
        "__slug__": args.slug,
        "__slug_sql__": sql_slug,
    }


def render_text(value: str, replacements: dict[str, str]) -> str:
    for needle, replacement in replacements.items():
        value = value.replace(needle, replacement)
    return value


def display_path(path: Path) -> str:
    if path.is_relative_to(ROOT):
        return path.relative_to(ROOT).as_posix()
    return path.as_posix()


def iter_template_files(template_dir: Path) -> list[Path]:
    return sorted(path for path in template_dir.rglob("*") if path.is_file())


def validate_args(args: argparse.Namespace) -> None:
    if not SLUG_RE.match(args.slug):
        raise SystemExit(
            "Slug non valido: usa solo minuscole, numeri e trattini, es. pensioni-pa-dag."
        )
    if not args.title.strip():
        raise SystemExit("Title obbligatorio.")
    if not args.template_dir.is_dir():
        raise SystemExit(f"Template non trovato: {args.template_dir}")


def plan_files(
    template_dir: Path,
    target_dir: Path,
    replacements: dict[str, str],
) -> list[tuple[Path, Path]]:
    planned: list[tuple[Path, Path]] = []
    for src in iter_template_files(template_dir):
        rel = src.relative_to(template_dir)
        rendered_parts = [render_text(part, replacements) for part in rel.parts]
        planned.append((src, target_dir.joinpath(*rendered_parts)))
    return planned


def write_file(src: Path, dst: Path, replacements: dict[str, str]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        text = src.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        shutil.copy2(src, dst)
        return
    dst.write_text(render_text(text, replacements), encoding="utf-8")


def scaffold(args: argparse.Namespace) -> int:
    validate_args(args)

    target_dir = args.candidates_dir / args.slug
    replacements = build_replacements(args)
    planned = plan_files(args.template_dir, target_dir, replacements)

    existing = [dst for _, dst in planned if dst.exists()]
    if target_dir.exists() and not args.force:
        raise SystemExit(f"Candidate gia' esistente: {target_dir}. Usa --force per sovrascrivere.")
    if existing and not args.force:
        listed = "\n".join(f"- {display_path(path)}" for path in existing)
        raise SystemExit(f"File gia' esistenti:\n{listed}\nUsa --force per sovrascrivere.")

    print(f"Candidate: {args.slug}")
    print(f"Target: {display_path(target_dir)}")
    print("File:")
    for _, dst in planned:
        print(f"- {display_path(dst)}")

    if not args.write:
        print("\nDry-run: nessun file scritto. Ripeti con --write per creare lo scaffold.")
        return 0

    for src, dst in planned:
        write_file(src, dst, replacements)

    print("\nCreato. Prossimi passi:")
    print(f"- completa {display_path(target_dir / 'dataset.yml')}")
    print(f"- completa {display_path(target_dir / 'README.md')} e notes.md")
    print("- esegui: python scripts/validate_candidate_structure.py")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copia templates/candidate in candidates/{slug} sostituendo placeholder minimi."
    )
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--discussion-url")
    parser.add_argument("--issue-url")
    parser.add_argument("--source-url")
    parser.add_argument("--created-date")
    parser.add_argument("--template-dir", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--candidates-dir", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--write", action="store_true", help="Scrive i file. Default: dry-run.")
    parser.add_argument("--force", action="store_true", help="Permette sovrascrittura del target.")
    return parser.parse_args()


def main() -> int:
    return scaffold(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
