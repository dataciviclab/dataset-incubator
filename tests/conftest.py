"""
Fixture condivise per i test di dataset-incubator.

Aggiunge scripts/ e tools/clean-query-mcp/ al path di default,
così nessun test deve ripetere sys.path.insert().
"""
import sys
from pathlib import Path
from typing import Any

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]

# Path setup — una volta sola
_SCRIPTS_PATH = str(_REPO_ROOT / "scripts")
_TOOLS_PATH = str(_REPO_ROOT / "tools" / "clean-query-mcp")

if _SCRIPTS_PATH not in sys.path:
    sys.path.insert(0, _SCRIPTS_PATH)
if _TOOLS_PATH not in sys.path:
    sys.path.insert(0, _TOOLS_PATH)
# Aggiunge anche ROOT per import via `scripts.xxx` (es. test_build_clean_catalog_derive)
_ROOT_PATH = str(_REPO_ROOT)
if _ROOT_PATH not in sys.path:
    sys.path.insert(0, _ROOT_PATH)


@pytest.fixture
def patch_root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Imposta ROOT a tmp_path per moduli che usano ROOT per path relativi."""
    # Patches validate_candidate_structure.ROOT
    monkeypatch.setattr("validate_candidate_structure.ROOT", tmp_path)
    monkeypatch.setattr("build_pipeline_signals.ROOT", tmp_path)
    monkeypatch.setattr("resolve_sample_run.ROOT", tmp_path)
    monkeypatch.setattr("detect_candidates.ROOT", tmp_path)
    return tmp_path


@pytest.fixture
def scripts_dir() -> Path:
    """Percorso assoluto a scripts/."""
    return _REPO_ROOT / "scripts"


@pytest.fixture
def fake_root(tmp_path: Path) -> Path:
    """Crea una directory temporanea che simula ROOT con candidates/ vuoto."""
    root = tmp_path / "dataset-incubator"
    (root / "candidates").mkdir(parents=True)
    (root / "registry").mkdir(parents=True)
    return root


def _make_yml(path: Path, content: dict[str, Any]) -> None:
    """Scrive un dataset.yml nella directory indicata."""
    import yaml
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(content, f, default_flow_style=False)


@pytest.fixture
def single_source_candidate(tmp_path: Path) -> Path:
    """Crea un candidate single-source in tmp_path/candidates/ok-ds."""
    base = tmp_path / "candidates" / "ok-ds"
    sql_dir = base / "sql"
    sql_dir.mkdir(parents=True)

    # clean.sql
    (sql_dir / "clean.sql").write_text("SELECT 1", encoding="utf-8")

    # mart.sql
    (sql_dir / "mart.sql").write_text("SELECT * FROM clean", encoding="utf-8")

    # dataset.yml
    _make_yml(base / "dataset.yml", {
        "dataset": {
            "name": "OK Dataset",
            "years": [2020, 2021, 2022],
            "source_id": "test-source-id",
        },
        "raw": {
            "sources": [{"name": "Fonte Test", "url": "https://example.com"}],
        },
    })

    return base


@pytest.fixture
def single_source_no_mart(tmp_path: Path) -> Path:
    """Candidate single-source senza mart SQL — stato warn."""
    base = tmp_path / "candidates" / "no-mart-ds"
    sql_dir = base / "sql"
    sql_dir.mkdir(parents=True)

    (sql_dir / "clean.sql").write_text("SELECT 1", encoding="utf-8")

    _make_yml(base / "dataset.yml", {
        "dataset": {"name": "No Mart", "years": [2021]},
        "raw": {"sources": [{"name": "Fonte"}]},
    })

    return base


@pytest.fixture
def single_source_broken(tmp_path: Path) -> Path:
    """Candidate single-source senza dataset.yml — stato error."""
    base = tmp_path / "candidates" / "broken-ds"
    base.mkdir(parents=True)
    # Nessun dataset.yml, nessun sql/
    return base


@pytest.fixture
def multi_source_candidate(tmp_path: Path) -> Path:
    """Candidate multi-source con due fonti + compose layer."""
    base = tmp_path / "candidates" / "multi-ds"
    sources_dir = base / "sources"
    compose_dir = base / "compose"

    # Fonte A
    src_a = sources_dir / "fonte-a"
    (src_a / "sql").mkdir(parents=True)
    (src_a / "sql" / "clean.sql").write_text("SELECT 1", encoding="utf-8")
    _make_yml(src_a / "dataset.yml", {
        "dataset": {"name": "Fonte A", "years": [2020]},
        "raw": {"sources": [{"name": "Fonte A Data"}]},
    })

    # Fonte B
    src_b = sources_dir / "fonte-b"
    (src_b / "sql").mkdir(parents=True)
    (src_b / "sql" / "clean.sql").write_text("SELECT 2", encoding="utf-8")
    _make_yml(src_b / "dataset.yml", {
        "dataset": {"name": "Fonte B", "years": [2021]},
        "raw": {"sources": [{"name": "Fonte B Data"}]},
    })

    # Compose layer con mart
    (compose_dir / "sql").mkdir(parents=True)
    (compose_dir / "sql" / "mart.sql").write_text("SELECT * FROM clean", encoding="utf-8")

    return base


@pytest.fixture
def compose_candidate(tmp_path: Path) -> Path:
    """Candidate compose (mart-only, no raw/clean)."""
    base = tmp_path / "compose" / "agg-ds"
    sql_dir = base / "sql"
    sql_dir.mkdir(parents=True)
    (sql_dir / "mart.sql").write_text("SELECT * FROM clean", encoding="utf-8")

    _make_yml(base / "dataset.yml", {
        "dataset": {"name": "Aggregato", "years": [2020, 2021]},
        "support": [{"name": "Dataset Base"}],
    })

    return base


@pytest.fixture
def support_dataset(tmp_path: Path) -> Path:
    """Support dataset (in support_datasets/)."""
    base = tmp_path / "support_datasets" / "support-ds"
    sql_dir = base / "sql"
    sql_dir.mkdir(parents=True)
    (sql_dir / "clean.sql").write_text("SELECT 1", encoding="utf-8")
    return base
