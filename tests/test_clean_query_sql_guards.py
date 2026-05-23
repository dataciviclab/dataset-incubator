from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

import pytest

import server

pytestmark = pytest.mark.contract


class CleanQuerySqlGuardTest(unittest.TestCase):
    def assert_allowed(self, sql: str) -> None:
        server._validate_scope(sql)
        server._validate_select_sql(sql)

    def assert_blocked(self, sql: str) -> None:
        with self.assertRaises(server.DuckdbClientError):
            server._validate_scope(sql)
            server._validate_select_sql(sql)

    def test_allows_clean_input_select(self) -> None:
        self.assert_allowed("SELECT COUNT(*) FROM clean_input")

    def test_allows_cte(self) -> None:
        self.assert_allowed(
            "WITH t AS (SELECT * FROM clean_input) SELECT COUNT(*) FROM t"
        )

    def test_blocks_direct_parquet_read(self) -> None:
        self.assert_blocked("SELECT * FROM read_parquet('gs://bucket/file.parquet')")

    def test_blocks_unknown_from_table(self) -> None:
        self.assert_blocked("SELECT * FROM other_table")

    def test_blocks_unknown_join_table(self) -> None:
        self.assert_blocked("SELECT * FROM clean_input JOIN other_table USING (id)")

    def test_blocks_multiple_statements(self) -> None:
        self.assert_blocked("SELECT * FROM clean_input; DROP TABLE clean_input")

    def test_blocks_dml_keyword(self) -> None:
        self.assert_blocked("DELETE FROM clean_input")

    def test_blocks_non_positive_max_rows(self) -> None:
        with self.assertRaises(server.DuckdbClientError):
            server._guard_max_rows(0)

    def test_blocks_above_hard_cap(self) -> None:
        with self.assertRaises(server.DuckdbClientError):
            server._guard_max_rows(server.MAX_ROWS_HARD_CAP + 1)


# ─── Contract: year → WHERE anno = year in count / preview / time_series ─────


def _make_mock_conn() -> MagicMock:
    """Build a mock DuckDB connection that captures execute SQL."""
    conn = MagicMock()
    conn.execute.return_value.description = [("col",)]
    conn.execute.return_value.fetchone.return_value = (0,)
    conn.execute.return_value.fetchall.return_value = []
    return conn


_SLUG = "giustizia_penale_indicatori"  # single-file, multi-year (2014-2024)


class CleanQueryYearFilterContractTest(unittest.TestCase):
    """Verifica che year=... inietti WHERE <year_col> = <year> nella SQL.

    Copre i tre tool che il fix ha modificato: count, preview (via _duckdb_read), time_series.
    """

    @patch("lab_connectors.duckdb.safe_connect")
    @patch.object(server, "resolve_parquet_path")
    def test_count_injects_year_filter(
        self, mock_resolve: MagicMock, mock_sc: MagicMock
    ) -> None:
        mock_resolve.return_value = ["gs://fake/giustizia_penale_indicatori_2024.parquet"]
        conn = _make_mock_conn()
        mock_sc.return_value.__enter__.return_value = conn

        server.count(_SLUG, year=2024)

        sql = conn.execute.call_args[0][0]
        self.assertIn("WHERE anno = 2024", sql)

    @patch("lab_connectors.duckdb.safe_connect")
    @patch.object(server, "resolve_parquet_path")
    def test_count_no_year_no_filter(
        self, mock_resolve: MagicMock, mock_sc: MagicMock
    ) -> None:
        mock_resolve.return_value = ["gs://fake/giustizia_penale_indicatori_2024.parquet"]
        conn = _make_mock_conn()
        mock_sc.return_value.__enter__.return_value = conn

        server.count(_SLUG)

        sql = conn.execute.call_args[0][0]
        self.assertNotIn("WHERE", sql)

    @patch("lab_connectors.duckdb.safe_connect")
    @patch.object(server, "resolve_parquet_path")
    def test_preview_injects_year_filter(
        self, mock_resolve: MagicMock, mock_sc: MagicMock
    ) -> None:
        """preview usa _duckdb_read, che ora inietta il filtro anno."""
        mock_resolve.return_value = ["gs://fake/giustizia_penale_indicatori_2024.parquet"]
        conn = _make_mock_conn()
        mock_sc.return_value.__enter__.return_value = conn

        server.preview(_SLUG, year=2024)

        sql = conn.execute.call_args[0][0]
        self.assertIn("WHERE anno = 2024", sql)

    @patch("lab_connectors.duckdb.safe_connect")
    @patch.object(server, "resolve_parquet_path")
    def test_time_series_injects_year_filter(
        self, mock_resolve: MagicMock, mock_sc: MagicMock
    ) -> None:
        mock_resolve.return_value = ["gs://fake/giustizia_penale_indicatori_2024.parquet"]
        conn = _make_mock_conn()
        mock_sc.return_value.__enter__.return_value = conn

        server.time_series(_SLUG, "disposition_time_gg", "distretto", year=2024)

        sql = conn.execute.call_args[0][0]
        self.assertIn("WHERE anno = 2024", sql)

    @patch("lab_connectors.duckdb.safe_connect")
    @patch.object(server, "resolve_parquet_path")
    def test_time_series_no_year_no_filter(
        self, mock_resolve: MagicMock, mock_sc: MagicMock
    ) -> None:
        mock_resolve.return_value = ["gs://fake/giustizia_penale_indicatori_2024.parquet"]
        conn = _make_mock_conn()
        mock_sc.return_value.__enter__.return_value = conn

        server.time_series(_SLUG, "disposition_time_gg", "distretto")

        sql = conn.execute.call_args[0][0]
        self.assertNotIn("WHERE", sql)


# ─── Unit: _inject_year_filter (pure function) ──────────────────────────────


class InjectYearFilterUnitTest(unittest.TestCase):
    """Test per _inject_year_filter come funzione pura (nessun I/O)."""

    @pytest.mark.pure_unit
    @pytest.mark.pure_unit
    def test_injects_where_after_from_cte(self) -> None:
        sql = (
            "WITH clean_input AS (SELECT * FROM read_parquet('fake.parquet')) "
            "SELECT COUNT(*) AS total FROM clean_input"
        )
        result = server._inject_year_filter(sql, "anno", 2024)
        self.assertIn("WHERE anno = 2024", result)
        # WHERE deve stare tra FROM clean_input e nient'altro
        self.assertRegex(result, r"FROM clean_input WHERE anno = 2024\s*$")

    @pytest.mark.pure_unit
    def test_injects_where_before_limit(self) -> None:
        sql = (
            "WITH clean_input AS (SELECT * FROM read_parquet('fake.parquet')) "
            "SELECT * FROM clean_input LIMIT 10"
        )
        result = server._inject_year_filter(sql, "anno", 2023)
        self.assertIn("WHERE anno = 2023", result)
        self.assertRegex(result, r"FROM clean_input WHERE anno = 2023\s+LIMIT")

    @pytest.mark.pure_unit
    def test_injects_where_before_group_by(self) -> None:
        sql = (
            "WITH clean_input AS (SELECT * FROM read_parquet('fake.parquet')) "
            "SELECT anno, tipo, SUM(val) AS tot FROM clean_input "
            "GROUP BY anno, tipo ORDER BY anno"
        )
        result = server._inject_year_filter(sql, "anno", 2022)
        self.assertIn("WHERE anno = 2022", result)
        self.assertRegex(result, r"FROM clean_input WHERE anno = 2022\s+GROUP BY")

    @pytest.mark.pure_unit
    def test_ignores_cte_inner_from(self) -> None:
        """Il filtro DEVE andare nel FROM esterno, non in quello della CTE."""
        sql = (
            "WITH clean_input AS (SELECT * FROM read_parquet('fake.parquet')) "
            "SELECT * FROM clean_input"
        )
        result = server._inject_year_filter(sql, "anno", 2024)
        # Conta quante volte compare FROM ... WHERE
        count = result.count("WHERE anno = 2024")
        self.assertEqual(count, 1, f"WHERE deve comparire una sola volta, non {count}")

    @pytest.mark.pure_unit
    def test_skips_when_year_col_none(self) -> None:
        sql = "SELECT COUNT(*) FROM clean_input"
        result = server._inject_year_filter(sql, None, 2024)
        self.assertEqual(result, sql)

    @pytest.mark.pure_unit
    def test_skips_when_year_none(self) -> None:
        sql = "SELECT COUNT(*) FROM clean_input"
        result = server._inject_year_filter(sql, "anno", None)
        self.assertEqual(result, sql)

    @pytest.mark.pure_unit
    def test_does_not_double_where(self) -> None:
        sql = (
            "WITH clean_input AS (SELECT * FROM read_parquet('fake.parquet')) "
            "SELECT COUNT(*) AS total FROM clean_input WHERE altro_col > 0"
        )
        result = server._inject_year_filter(sql, "anno", 2024)
        # Il WHERE esistente non deve essere duplicato
        self.assertIn("WHERE altro_col > 0", result)
        self.assertEqual(result.count("WHERE"), 1)


if __name__ == "__main__":
    unittest.main()
