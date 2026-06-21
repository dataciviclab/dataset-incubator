"""
Helper condivisi per notebook candidate dataset-incubator.

Centralizza l'invocazione CLI del toolkit e utility di visualizzazione,
così che ogni notebook non replichi le stesse 15 righe di `tk()`, `tk_year()`,
`tk_schema()` e `show()`.

Uso nel notebook:

    from notebook_helpers import NotebookHelper, show

    SLUG = "my-dataset"
    cfg, anno = NotebookHelper.find_config()
    h = NotebookHelper(cfg, anno)

    paths = h.tk_year("inspect", "paths")
    schema = h.tk_schema("clean")
    show(df)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class NotebookHelper:
    """Helper per invocare il toolkit CLI da notebook candidate.

    Args:
        cfg_path: Path assoluto del dataset.yml del candidate.
        anno: Anno di run (ultimo anno della lista ``years`` in dataset.yml).
    """

    def __init__(self, cfg_path: Path, anno: int) -> None:
        self.cfg_path = cfg_path
        self.anno = anno

    # ── toolkit CLI wrappers ──────────────────────────────────────────────

    def tk(self, *args: str) -> dict[str, Any]:
        """Esegue un comando toolkit e restituisce il JSON di output.

        I comandi supportati includono: ``inspect config``, ``inspect summary``,
        ``inspect runs``, etc.

        Args:
            *args: Argomenti del comando (es. ``"inspect", "paths"``).

        Returns:
            Dict parsato dal JSON stdout del toolkit. Vuoto se stdout è vuoto.
        """
        cmd = ["toolkit", *args, "-c", str(self.cfg_path), "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            result.check_returncode()
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def tk_year(self, *args: str) -> dict[str, Any]:
        """Come :meth:`tk` ma aggiunge automaticamente ``--year <anno>``.

        Utile per comandi che richiedono l'anno (``inspect config``,
        ``inspect summary``).
        """
        return self.tk(*args, "--year", str(self.anno))

    def tk_schema(self, layer: str) -> dict[str, Any]:
        """Restituisce lo schema di un layer (raw/clean/mart).

        Args:
            layer: Nome del layer (``"raw"``, ``"clean"``, ``"mart"``).

        Returns:
            Dict con chiavi ``columns``, ``schema``, etc. In caso di errore
            restituisce ``{"columns": 0, "schema": []}``.
        """
        try:
            data = self.tk_year("inspect", "config", "-l", layer, "-m", "schema")
        except Exception:
            return {"columns": 0, "schema": []}
        if isinstance(data, dict) and "column_count" in data and "columns" in data:
            return {"columns": data["column_count"], "schema": data["columns"]}
        return data

    # ── ricerca dataset.yml ───────────────────────────────────────────────

    @staticmethod
    def find_config() -> tuple[Path, int]:
        """Cerca ``dataset.yml`` risalendo dalla CWD e restituisce
        ``(cfg_path, anno)``.

        L'anno è l'ultimo della lista ``dataset.years`` nel YAML.

        Returns:
            Tupla ``(Path al dataset.yml, anno intero)``.

        Raises:
            FileNotFoundError: Se ``dataset.yml`` non viene trovato risalendo
                dagli antenati della CWD.
        """
        import yaml

        start = Path.cwd().resolve()
        for probe in [start, *start.parents]:
            candidate = probe / "dataset.yml"
            if candidate.exists():
                cfg = yaml.safe_load(candidate.read_text())
                anno = cfg["dataset"]["years"][-1]
                return candidate, anno
        raise FileNotFoundError(f"dataset.yml non trovato risalendo da {start}")


# ── utility di visualizzazione ────────────────────────────────────────────


def show(df: Any) -> None:
    """Stampa un DataFrame: ``display()`` in Jupyter, ``print()`` altrove.

    Args:
        df: DataFrame pandas o oggetto con metodo ``to_string()``.
    """
    try:
        display(df)  # type: ignore[name-defined]  # noqa: F821
    except NameError:
        print(df.to_string())
