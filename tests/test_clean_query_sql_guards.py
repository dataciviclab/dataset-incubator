from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "clean-query-mcp"))

import server  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
