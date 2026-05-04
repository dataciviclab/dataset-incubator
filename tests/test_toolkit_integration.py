"""Integration test: lancia toolkit su un candidate minimo e verifica output.

Richiede `toolkit` installato nel PATH e un candidato template valido.

Non fa parte del fast-test suite perche' chiama un eseguibile esterno.
"""

from __future__ import annotations

import csv
import json
import subprocess
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "templates" / "candidate"


def _write_csv(path: Path, rows: list[list[str]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(rows)


def test_toolkit_run_minimal_candidate() -> None:
    """Crea un candidate minimo con source locale, esegue toolkit run, verifica output."""
    with tempfile.TemporaryDirectory(prefix="di-intg-") as tmp:
        dst = Path(tmp) / "test_intg"
        dst.mkdir()
        (dst / "sql").mkdir()

        # CSV di test
        raw_dir = dst / "raw_data"
        raw_dir.mkdir()
        _write_csv(
            raw_dir / "dataset_2024.csv",
            [["anno", "valore"], ["2024", "100"], ["2024", "200"]],
        )

        # dataset.yml
        yml = dst / "dataset.yml"
        yml.write_text(
            f"""
root: "{dst / 'out'}"
dataset:
  name: test_intg
  years: [2024]
raw:
  sources:
    - name: fonte
      type: local_file
      args:
        path: "{raw_dir / 'dataset_2024.csv'}"
clean:
  sql: sql/clean.sql
  read:
    source: auto
    mode: latest
    header: true
mart:
  tables:
    - name: mart_intg
      sql: sql/mart.sql
  required_tables:
    - mart_intg
validation:
  fail_on_error: true
output:
  artifacts: minimal
""".strip(),
        )

        # SQL
        (dst / "sql" / "clean.sql").write_text("select * from raw_input")
        (dst / "sql" / "mart.sql").write_text("select * from clean_input")

        # Esegui toolkit
        result = subprocess.run(
            ["toolkit", "run", "all", "--config", str(yml), "--years", "2024"],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode != 0:
            pytest.fail(f"toolkit run all fallito:\nSTDOUT:{result.stdout}\nSTDERR:{result.stderr}")

        # Verifica output CLEAN
        clean_parquet = dst / "out" / "data" / "clean" / "test_intg" / "2024" / "test_intg_2024_clean.parquet"
        assert clean_parquet.exists(), f"Clean parquet non trovato: {clean_parquet}"

        # Verifica metadata CLEAN
        meta_path = clean_parquet.parent / "metadata.json"
        assert meta_path.exists(), f"metadata.json non trovato: {meta_path}"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        assert meta["layer"] == "clean"
        assert meta["dataset"] == "test_intg"

        # Verifica output MART
        mart_parquet = dst / "out" / "data" / "mart" / "test_intg" / "2024" / "mart_intg.parquet"
        assert mart_parquet.exists(), f"Mart parquet non trovato: {mart_parquet}"

        # Verifica manifest MART
        manifest_path = mart_parquet.parent / "manifest.json"
        assert manifest_path.exists()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest.get("summary", {}).get("ok") is True
