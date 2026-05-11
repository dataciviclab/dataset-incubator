"""Shared helpers for candidate/support-dataset introspection.

Centralizza logica di:
  - risoluzione anni (dataset.years)
  - risoluzione dipendenze support
  - estrazione slug da path
  - rilevamento nested config

Usato da:
  - resolve_sample_run.py
  - detect_candidates.py
  - pr-toolkit-check.yml (via resolve_sample_run.py)

Contratto: tutte le funzioni sono pure (input → output, niente I/O esterno
se non la lettura esplicita del dataset.yml in resolve_years).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def resolve_years(cfg_path: Path) -> list[int]:
    """Legge dataset.years da dataset.yml, ritorna lista ordinata di int.

    Ritorna lista vuota se il file non esiste, non ha la sezione dataset,
    o gli anni non sono validi.
    """
    try:
        with open(cfg_path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    except Exception:
        return []

    dataset = cfg.get("dataset", {})
    years = dataset.get("years", [])
    if not years:
        return []

    try:
        return sorted(int(y) for y in years)
    except (TypeError, ValueError):
        return []


def resolve_sample_year(cfg_path: Path) -> int:
    """Ritorna l'ultimo anno in dataset.years, o 0 se non determinabile.

    Utile per detect_candidates che usa un singolo anno nel matrix CI.
    """
    years = resolve_years(cfg_path)
    return years[-1] if years else 0


def resolve_support_entries(
    cfg: dict[str, Any],
    cfg_parent: Path,
    root: Path,
) -> list[dict[str, Any]]:
    """Legge le voci support[] da dataset.yml, supportando entrambi i pattern.

    Pattern supportati:
      - root level: support: [{name, config, years}]
      - inside dataset: dataset.support: [{name, config, years}]

    Args:
        cfg: dataset.yml parsato
        cfg_parent: directory che contiene dataset.yml
        root: ROOT del repository

    Returns:
        Lista di dict con chiavi name, config (path relativo a root), years
    """
    entries = []
    raw_support = cfg.get("support", []) or []
    dataset_support = cfg.get("dataset", {}).get("support", []) or []

    for entry in raw_support + dataset_support:
        rel_config = entry.get("config", "")
        if not rel_config:
            continue
        support_path = (cfg_parent / rel_config).resolve()
        try:
            support_rel = support_path.relative_to(root)
        except ValueError:
            support_rel = support_path
        entries.append({
            "name": entry.get("name", ""),
            "config": str(support_rel),
            "years": entry.get("years", []),
        })

    return entries


def candidate_slug_from_path(path: Path, root: Path) -> str | None:
    """Estrae lo slug di un candidate/support_dataset dal path.

    Cerca il primo segmento dopo candidates/ o support_datasets/ nel path
    relativo a root.

    Esempi:
      candidates/istat-housing-crowding/dataset.yml → "istat-housing-crowding"
      candidates/ispra-ru/sources/a_ru_base/dataset.yml → "ispra-ru"
      support_datasets/bdap-anagrafe-enti/dataset.yml → "bdap-anagrafe-enti"
    """
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path

    for i, part in enumerate(rel.parts):
        if part in ("candidates", "support_datasets"):
            if i + 1 < len(rel.parts):
                return rel.parts[i + 1]

    # Fallback: directory padre
    return path.parts[-2] if len(path.parts) >= 2 else None


def is_nested_config(path: Path) -> bool:
    """Un config è nested se il path contiene sources/ o compose/."""
    parts = path.parts
    return "sources" in parts or "compose" in parts
