"""batch_by_source.py — orchestrazione preflight/run per fonte.

Esegue ``toolkit run preflight`` (default) o ``toolkit run`` su tutti i
dataset.yml di dataset-incubator, raggruppati per ``source_id``, con report
aggregato.

Sostituisce:
- il loop inline Python dei workflow CI (smoke-weekly.yml) — stesso pattern,
  riusabile in locale;
- i ``batches/*.txt`` obsoleti (raggruppavano per protocollo e citavano il CLI
  deprecato ``toolkit batch``).

Contratto: la fonte di verità per il raggruppamento è ``dataset.source_id`` in
``dataset.yml`` (già obbligatorio nello standard candidate). Nessun file batch
da mantenere: i gruppi sono derivati a ogni run.

Prova del fuoco: se il raggruppamento per fonte o il criterio di successo del
preflight cambiano, smoke-weekly e chi usa questo script rischiano di validare
candidate con fonti non raggiungibili.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ("candidates", "support_datasets", "compose")
UNKNOWN_SOURCE = "__unknown__"


@dataclass(frozen=True)
class DatasetEntry:
    """Un dataset.yml con il suo source_id."""

    path: Path
    source_id: str
    dataset_name: str


def load_source_id(yml_path: Path) -> str:
    """Legge ``dataset.source_id`` via ``load_dataset_manifest`` (contratto toolkit).

    Riusa il parser condiviso del toolkit invece di un YAML parse locale:
    stesso comportamento di validate_candidate_structure e della CI.
    """
    from toolkit.core.dataset_loader import load_dataset_manifest

    manifest = load_dataset_manifest(yml_path)
    sid = manifest.get("source_id")
    return str(sid).strip() if sid else ""


def scan_dataset_ymls(root: Path | None = None) -> list[DatasetEntry]:
    """Scansiona candidates/, support_datasets/, compose/ per i dataset.yml.

    I dataset senza ``source_id`` vengono marcati con ``UNKNOWN_SOURCE``
    (non esclusi: restano processabili, ma segnalati nel report).
    """
    root = root or ROOT
    entries: list[DatasetEntry] = []
    for section in SECTIONS:
        base = root / section
        if not base.is_dir():
            continue
        for entry_dir in sorted(base.iterdir()):
            yml = entry_dir / "dataset.yml"
            if not yml.is_file():
                continue
            sid = load_source_id(yml)
            entries.append(
                DatasetEntry(
                    path=yml,
                    source_id=sid or UNKNOWN_SOURCE,
                    dataset_name=sid or f"{section}/{entry_dir.name}",
                )
            )
    return entries


def group_by_source(entries: list[DatasetEntry]) -> dict[str, list[DatasetEntry]]:
    """Raggruppa i dataset per source_id (ordinati per path)."""
    groups: dict[str, list[DatasetEntry]] = {}
    for entry in sorted(entries, key=lambda e: (e.source_id, str(e.path))):
        groups.setdefault(entry.source_id, []).append(entry)
    return groups


def evaluate_preflight(result: dict) -> tuple[bool, str]:
    """Criterio di successo per un report preflight.

    Ok se ``status == "passed"`` e le fonti probe-effettive sono tutte
    raggiungibili. Le fonti ``skipped`` non contano (es. type: script).
    Un candidate senza fonti remote (local_file, 0 sources) è ok se passed —
    corrige il pattern CI (smoke-weekly) dove ``len(srcs) > 0`` faceva
    fallire proprio i local_file.

    Returns:
        (ok, reachable_str) — es. (True, "2/2"), (True, "-") per 0 fonti.
    """
    ok_status = result.get("status") == "passed"
    sources = result.get("sources") or []
    active = [s for s in sources if s.get("status") != "skipped"]
    n_reach = sum(1 for s in active if s.get("reachable"))
    reachable_str = f"{n_reach}/{len(active)}" if active else "-"
    ok = ok_status and (not active or n_reach == len(active))
    return ok, reachable_str


def run_preflight(config: Path, timeout: int = 90) -> dict:
    """Esegue ``toolkit run preflight --json`` su un config.

    Il comando stampa il JSON su stdout anche quando lo status è ``failed``
    (esce con codice 1 dopo l'echo): il JSON si parsa comunque da stdout,
    con fallback su stderr se la risposta non è JSON.
    """
    try:
        r = subprocess.run(
            ["toolkit", "run", "preflight", "--config", str(config), "--json"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"status": "failed", "dataset": config.parent.name, "error": "timeout"}
    except FileNotFoundError:
        return {
            "status": "failed",
            "dataset": config.parent.name,
            "error": "toolkit non trovato nel PATH",
        }

    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {
            "status": "failed",
            "dataset": config.parent.name,
            "error": (r.stderr or r.stdout)[:300],
        }


def format_report(rows: list[dict], groups: dict[str, list[DatasetEntry]]) -> str:
    """Rappresentazione testuale compatta del report."""
    lines = []
    for source_id in sorted(groups):
        lines.append(f"[{source_id}] ({len(groups[source_id])})")
        for row in rows:
            if row["source_id"] != source_id:
                continue
            icon = "✅" if row["ok"] else "🔴"
            err = f" — {row.get('error', '')[:80]}" if row.get("error") else ""
            warn = ""
            if row.get("warnings"):
                warn = " ⚠ " + "; ".join(row["warnings"])[:70]
            lines.append(f"  {icon} {row['dataset']:30s} {row['reachable']}{warn}{err}")
    lines.append("")
    passed = sum(1 for r in rows if r["ok"])
    lines.append(f"Summary: {passed}/{len(rows)} OK")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Preflight/run per fonte su tutti i dataset di dataset-incubator"
    )
    parser.add_argument(
        "--fonte", "-f", default=None, help="Filtra per source_id (default: tutte le fonti)"
    )
    parser.add_argument(
        "--step", choices=("preflight", "run"), default="preflight", help="Azione da eseguire"
    )
    parser.add_argument("--smoke", action="store_true", help="Con --step run: sample-rows/bytes")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    parser.add_argument("--timeout", type=int, default=90, help="Timeout per dataset (s)")
    args = parser.parse_args(argv)

    entries = scan_dataset_ymls()
    groups = group_by_source(entries)
    if not groups:
        print("Nessun dataset.yml trovato", file=sys.stderr)
        return 1

    if args.fonte:
        if args.fonte not in groups:
            available = ", ".join(sorted(groups))
            print(f"Fonte '{args.fonte}' non trovata. Disponibili: {available}", file=sys.stderr)
            return 1
        groups = {args.fonte: groups[args.fonte]}

    unknown = [e for e in entries if e.source_id == UNKNOWN_SOURCE]

    rows: list[dict] = []
    for source_id in sorted(groups):
        for entry in groups[source_id]:
            if args.step == "preflight":
                result = run_preflight(entry.path, timeout=args.timeout)
                ok, reachable = evaluate_preflight(result)
                # Warning del config check (es. source_id mancante) dal toolkit:
                # validate_config li produce già — li esponiamo nel report bulk.
                warnings = (result.get("config_check") or {}).get("warnings") or []
                rows.append(
                    {
                        "source_id": source_id,
                        "dataset": result.get("dataset", entry.dataset_name),
                        "ok": ok,
                        "reachable": reachable,
                        "error": result.get("error"),
                        "warnings": warnings,
                    }
                )
            else:
                cmd = ["toolkit", "run", "--config", str(entry.path)]
                if args.smoke:
                    cmd.append("--smoke")
                try:
                    r = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout)
                    ok = r.returncode == 0
                    rows.append(
                        {
                            "source_id": source_id,
                            "dataset": entry.dataset_name,
                            "ok": ok,
                            "reachable": "-",
                            "error": (r.stderr or r.stdout)[:200] if not ok else None,
                        }
                    )
                except subprocess.TimeoutExpired:
                    rows.append(
                        {
                            "source_id": source_id,
                            "dataset": entry.dataset_name,
                            "ok": False,
                            "reachable": "-",
                            "error": "timeout",
                        }
                    )

    if args.json:
        report = {
            "summary": {
                "total": len(rows),
                "passed": sum(1 for r in rows if r["ok"]),
                "failed": sum(1 for r in rows if not r["ok"]),
            },
            "unknown_source": [str(e.path) for e in unknown],
            "rows": rows,
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_report(rows, groups))
        if unknown:
            print(
                f"\n⚠ {len(unknown)} dataset senza source_id (gruppo '{UNKNOWN_SOURCE}'): "
                "aggiungere dataset.source_id — vedi docs/candidate-standard.md",
                file=sys.stderr,
            )

    return 1 if any(not r["ok"] for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
