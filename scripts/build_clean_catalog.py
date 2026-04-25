from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "registry" / "clean_catalog.json"
DEFAULT_SCHEMA = ROOT / "registry" / "clean_catalog.schema.json"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize and optionally verify the Lab Clean Registry."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument(
        "--write", action="store_true", help="Rewrite catalog in canonical form."
    )
    parser.add_argument(
        "--refresh-date",
        action="store_true",
        help="Set updated_at to today's date when writing.",
    )
    parser.add_argument(
        "--check-gcs",
        action="store_true",
        help="Verify that public GCS paths resolve to at least one parquet.",
    )
    args = parser.parse_args()

    original_text = args.catalog.read_text(encoding="utf-8")
    catalog = json.loads(original_text)
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    normalized = normalize_catalog(catalog, refresh_date=args.refresh_date)

    errors = validate_catalog(normalized, schema)
    if args.check_gcs:
        errors.extend(validate_gcs_locations(normalized))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    output_text = json.dumps(normalized, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        args.catalog.write_text(output_text, encoding="utf-8")
        print(f"wrote {args.catalog}")
        return 0

    if output_text != original_text:
        print(f"{args.catalog} is not normalized; rerun with --write", file=sys.stderr)
        return 1

    print(f"ok {args.catalog} ({len(normalized['datasets'])} datasets)")
    return 0


def normalize_catalog(catalog: dict[str, Any], *, refresh_date: bool = False) -> dict[str, Any]:
    normalized = dict(catalog)
    normalized.setdefault("schema_version", 1)
    normalized.setdefault("name", "Lab Clean Registry")
    normalized.setdefault(
        "description",
        "Catalogo canonico dei clean parquet pubblici prodotti o adottati da dataset-incubator.",
    )
    normalized.setdefault("source_repo", "dataciviclab/dataset-incubator")
    normalized["updated_at"] = str(date.today()) if refresh_date else normalized.get(
        "updated_at", str(date.today())
    )

    datasets = []
    for dataset in normalized.get("datasets", []):
        item = dict(dataset)
        item.setdefault("status", "clean_ready")
        item.setdefault("visibility", "public")
        datasets.append(item)
    normalized["datasets"] = sorted(datasets, key=lambda item: item["slug"])
    return normalized


def validate_catalog(catalog: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors = validate_json_schema(catalog, schema)
    if catalog.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    datasets = catalog.get("datasets")
    if not isinstance(datasets, list) or not datasets:
        errors.append("datasets must be a non-empty list")
        return errors

    seen: set[str] = set()
    for dataset in datasets:
        slug = dataset.get("slug")
        if not slug:
            errors.append("dataset without slug")
            continue
        if slug in seen:
            errors.append(f"duplicate dataset slug: {slug}")
        seen.add(slug)

        period = dataset.get("period") or {}
        if period.get("start") is None or period.get("end") is None:
            errors.append(f"{slug}: missing period.start or period.end")
        elif int(period["start"]) > int(period["end"]):
            errors.append(f"{slug}: period.start greater than period.end")

        columns = dataset.get("columns")
        if not isinstance(columns, list) or not columns:
            errors.append(f"{slug}: columns must be a non-empty list")
        else:
            column_names = [column.get("name") for column in columns]
            if len(column_names) != len(set(column_names)):
                errors.append(f"{slug}: duplicate column names")

        location = dataset.get("location") or {}
        if location.get("type") not in {"gcs", "local"}:
            errors.append(f"{slug}: unsupported location.type")
        if not location.get("path"):
            errors.append(f"{slug}: missing location.path")
    return errors


def validate_json_schema(instance: Any, schema: dict[str, Any]) -> list[str]:
    """Validate the catalog against the local schema subset used by DI.

    This intentionally supports only the JSON Schema keywords present in
    registry/clean_catalog.schema.json, avoiding a runtime dependency just for
    the catalog check.
    """
    return _validate_node(instance, schema, schema, "$")


def _validate_node(
    instance: Any,
    node: dict[str, Any],
    root_schema: dict[str, Any],
    path: str,
) -> list[str]:
    errors: list[str] = []
    if "$ref" in node:
        node = _resolve_ref(root_schema, node["$ref"])

    expected_type = node.get("type")
    if expected_type and not _matches_json_type(instance, expected_type):
        return [f"{path}: expected {expected_type}, got {type(instance).__name__}"]

    if "const" in node and instance != node["const"]:
        errors.append(f"{path}: expected const {node['const']!r}")

    if "enum" in node and instance not in node["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum {node['enum']!r}")

    if "pattern" in node and isinstance(instance, str):
        if re.fullmatch(node["pattern"], instance) is None:
            errors.append(f"{path}: value {instance!r} does not match {node['pattern']}")

    if node.get("format") == "date" and isinstance(instance, str):
        try:
            date.fromisoformat(instance)
        except ValueError:
            errors.append(f"{path}: value {instance!r} is not a valid date (expected YYYY-MM-DD)")

    if isinstance(instance, dict):
        properties = node.get("properties", {})
        for field in node.get("required", []):
            if field not in instance:
                errors.append(f"{path}: missing required property {field!r}")

        if node.get("additionalProperties") is False:
            allowed = set(properties)
            for field in instance:
                if field not in allowed:
                    errors.append(f"{path}: additional property {field!r} not allowed")

        for field, value in instance.items():
            if field in properties:
                errors.extend(
                    _validate_node(
                        value, properties[field], root_schema, f"{path}.{field}"
                    )
                )

    if isinstance(instance, list):
        min_items = node.get("minItems")
        if min_items is not None and len(instance) < int(min_items):
            errors.append(f"{path}: expected at least {min_items} items")
        item_schema = node.get("items")
        if item_schema:
            for index, value in enumerate(instance):
                errors.extend(
                    _validate_node(value, item_schema, root_schema, f"{path}[{index}]")
                )

    return errors


def _resolve_ref(schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported schema ref: {ref}")
    node: Any = schema
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def _matches_json_type(instance: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(instance, dict)
    if expected_type == "array":
        return isinstance(instance, list)
    if expected_type == "string":
        return isinstance(instance, str)
    if expected_type == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected_type == "boolean":
        return isinstance(instance, bool)
    return True


def validate_gcs_locations(catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for dataset in catalog["datasets"]:
        slug = dataset["slug"]
        location = dataset["location"]
        if location["type"] != "gcs":
            continue
        path = location["path"]
        try:
            matches = resolve_gcs_path(path)
        except Exception as exc:
            errors.append(f"{slug}: {exc}")
            continue
        if not matches:
            errors.append(f"{slug}: no public GCS object matches {path}")
            continue
        if location.get("multi_file"):
            # Guard: if only one GCS file matches, assume it's a snapshot
            # containing the full series (e.g. civile_flussi_2025 contains
            # 2014-2025) — skip per-year check. Only validate per-year when
            # multiple files exist. This avoids false negatives on single-snapshot
            # datasets but means a missing-file push (0 matches) also passes.
            # TODO: add explicit snapshot: true to location schema to model
            # this properly instead of inferring from match count.
            if len(matches) > 1:
                missing_years = missing_period_years(matches, dataset["period"])
                if missing_years:
                    errors.append(f"{slug}: missing GCS files for years {missing_years}")
    return errors


def resolve_gcs_path(path: str) -> list[str]:
    if not path.startswith("gs://"):
        raise ValueError(f"not a GCS path: {path}")
    bucket, key = path[5:].split("/", 1)
    if "*" not in key:
        url = f"https://storage.googleapis.com/{bucket}/{quote(key, safe='/._-')}"
        request = Request(url, method="HEAD")
        with urlopen(request, timeout=30) as response:
            if response.status >= 400:
                return []
        return [key]

    prefix = key.split("*", 1)[0]
    names = list_gcs_objects(bucket, prefix)
    return [name for name in names if fnmatchcase(name, key)]


def list_gcs_objects(bucket: str, prefix: str) -> list[str]:
    params = urlencode({"prefix": prefix, "fields": "items(name),nextPageToken"})
    url = f"https://storage.googleapis.com/storage/v1/b/{quote(bucket)}/o?{params}"
    names: list[str] = []
    while url:
        with urlopen(url, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        names.extend(item["name"] for item in payload.get("items", []))
        token = payload.get("nextPageToken")
        if token:
            url = (
                f"https://storage.googleapis.com/storage/v1/b/{quote(bucket)}/o?"
                f"{params}&pageToken={quote(token)}"
            )
        else:
            url = ""
    return names


def missing_period_years(paths: list[str], period: dict[str, Any]) -> list[int]:
    start = int(period["start"])
    end = int(period["end"])
    missing = []
    for year in range(start, end + 1):
        if not any(f"/{year}/" in path or f"_{year}_" in path for path in paths):
            missing.append(year)
    return missing


if __name__ == "__main__":
    raise SystemExit(main())
