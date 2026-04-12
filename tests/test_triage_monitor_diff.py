from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from triage_monitor_diff import load_map, render_report, triage


# --- load_map ---

def test_load_map_returns_active_entries(tmp_path: Path) -> None:
    map_data = {
        "mappings": [
            {"source_id": "s1", "candidates": ["c1"], "active": True},
            {"source_id": "s2", "candidates": ["c2"], "active": False},
        ]
    }
    map_file = tmp_path / "map.yml"
    map_file.write_text(yaml.dump(map_data), encoding="utf-8")

    result = load_map(map_file)

    assert "s1" in result
    assert result["s1"] == ["c1"]
    assert "s2" not in result


def test_load_map_active_defaults_to_true(tmp_path: Path) -> None:
    map_data = {"mappings": [{"source_id": "s1", "candidates": ["c1"]}]}
    map_file = tmp_path / "map.yml"
    map_file.write_text(yaml.dump(map_data), encoding="utf-8")

    result = load_map(map_file)

    assert "s1" in result


def test_load_map_empty_mappings(tmp_path: Path) -> None:
    map_file = tmp_path / "map.yml"
    map_file.write_text(yaml.dump({"mappings": []}), encoding="utf-8")

    assert load_map(map_file) == {}


def test_load_map_invalid_root_type(tmp_path: Path) -> None:
    map_file = tmp_path / "map.yml"
    map_file.write_text("- just a list\n", encoding="utf-8")

    with pytest.raises(ValueError, match="non valido"):
        load_map(map_file)


def test_load_map_entry_missing_source_id(tmp_path: Path) -> None:
    map_data = {"mappings": [{"candidates": ["c1"], "active": True}]}
    map_file = tmp_path / "map.yml"
    map_file.write_text(yaml.dump(map_data), encoding="utf-8")

    with pytest.raises(ValueError, match="source_id"):
        load_map(map_file)


# --- triage ---

def _make_diff(
    sources_with_changes: list[str] | None = None,
    sources_with_errors: list[str] | None = None,
    per_source: dict | None = None,
) -> dict:
    return {
        "generated_at_utc": "2026-04-12T10:00:00Z",
        "sources_with_changes": sources_with_changes or [],
        "sources_with_errors": sources_with_errors or [],
        "per_source": per_source or {},
    }


def test_triage_no_changes() -> None:
    result = triage(_make_diff(), source_map={"s1": ["c1"]})

    assert result["impacted_count"] == 0
    assert result["impacted"] == []


def test_triage_source_in_map_with_changes() -> None:
    diff = _make_diff(
        sources_with_changes=["s1"],
        per_source={"s1": {"new": 0, "changed": 2, "removed": 0}},
    )
    result = triage(diff, source_map={"s1": ["c1", "c2"]})

    assert result["impacted_count"] == 1
    item = result["impacted"][0]
    assert item["source_id"] == "s1"
    assert item["candidates"] == ["c1", "c2"]
    assert item["changed"] == 2


def test_triage_missing_per_source_entry_degrades() -> None:
    """Se sources_with_changes elenca una fonte ma per_source e' incompleto, non crasha."""
    diff = _make_diff(
        sources_with_changes=["s1"],
        per_source={},  # chiave mancante
    )
    result = triage(diff, source_map={"s1": ["c1"]})

    assert result["impacted_count"] == 1
    item = result["impacted"][0]
    assert item["new"] == 0
    assert item["changed"] == 0
    assert item["removed"] == 0


def test_triage_missing_count_keys_degrades() -> None:
    """Se per_source ha la entry ma mancano le chiavi di conteggio, usa 0 come default."""
    diff = _make_diff(
        sources_with_changes=["s1"],
        per_source={"s1": {}},  # entry presente ma senza new/changed/removed
    )
    result = triage(diff, source_map={"s1": ["c1"]})

    assert result["impacted"][0]["changed"] == 0


def test_triage_unknown_source_ignored() -> None:
    diff = _make_diff(
        sources_with_changes=["unknown"],
        per_source={"unknown": {"new": 1, "changed": 0, "removed": 0}},
    )
    result = triage(diff, source_map={"s1": ["c1"]})

    assert result["impacted_count"] == 0


def test_triage_errors_in_map_reported() -> None:
    diff = _make_diff(sources_with_errors=["s1"])
    result = triage(diff, source_map={"s1": ["c1"]})

    assert "s1" in result["sources_with_errors_in_map"]


def test_triage_errors_not_in_map_ignored() -> None:
    diff = _make_diff(sources_with_errors=["other-source"])
    result = triage(diff, source_map={"s1": ["c1"]})

    assert result["sources_with_errors_in_map"] == []


# --- render_report ---

def test_render_report_no_action() -> None:
    result = {
        "generated_at": "2026-04-12T10:00:00Z",
        "impacted_count": 0,
        "impacted": [],
        "sources_with_errors_in_map": [],
    }
    report = render_report(result)

    assert "Nessuna azione" in report


def test_render_report_shows_impacted() -> None:
    result = {
        "generated_at": "2026-04-12T10:00:00Z",
        "impacted_count": 1,
        "impacted": [
            {"source_id": "s1", "candidates": ["c1"], "new": 0, "changed": 1, "removed": 0}
        ],
        "sources_with_errors_in_map": [],
    }
    report = render_report(result)

    assert "s1" in report
    assert "c1" in report
    assert "changed: 1" in report


def test_render_report_shows_errors() -> None:
    result = {
        "generated_at": "2026-04-12T10:00:00Z",
        "impacted_count": 0,
        "impacted": [],
        "sources_with_errors_in_map": ["s1"],
    }
    report = render_report(result)

    assert "s1" in report
    assert "errori" in report.lower()
