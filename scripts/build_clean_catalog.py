from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any

import yaml
from lab_connectors.gcs import list_objects, object_exists
from lab_connectors.gcs.paths import gs_url
from toolkit.core.dataset_loader import load_dataset_manifest


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "registry" / "clean_catalog.json"
DEFAULT_SCHEMA = ROOT / "registry" / "clean_catalog.schema.json"
SEMTYPES_PATH = ROOT / "registry" / "semantic_types.yaml"


def _load_semantic_type_map() -> dict[str, str]:
    """Carica semantic_types.yaml e restituisce alias_map.

    alias_map: alias.lower() → semantic_type (match esatto).
    Niente partial/substring match — evita falsi positivi.
    Gli alias vanno tenuti specifici in semantic_types.yaml.
    """
    if not SEMTYPES_PATH.exists():
        return {}
    data = yaml.safe_load(SEMTYPES_PATH.read_text())
    types = data.get("types", {})
    alias_map: dict[str, str] = {}

    for stype, info in types.items():
        for alias in info.get("aliases", []):
            alias_lower = alias.lower()
            if alias_lower not in alias_map:
                alias_map[alias_lower] = stype

    return alias_map


def _assign_semantic_type(col_name: str, alias_map: dict[str, str]) -> str | None:
    """Assegna semantic_type a un nome colonna — solo match esatto."""
    col_lower = col_name.lower()
    return alias_map.get(col_lower)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize, derive, and optionally verify the Lab Clean Registry."
    )
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--write", action="store_true", help="Rewrite catalog in canonical form.")
    parser.add_argument(
        "--refresh-date",
        action="store_true",
        help="Set updated_at to today's date when writing.",
    )
    parser.add_argument(
        "--derive",
        action="store_true",
        help="Derive catalog from GCS: scan bucket, read parquet schemas, merge with editorial metadata. "
        "Usa --write per salvare (--derive senza --write è dry-run).",
    )
    parser.add_argument(
        "--slug",
        type=str,
        default=None,
        help="Limita il derive a un singolo slug (es. sbarchi_migranti_italia). "
        "Scansiona solo quel prefisso nel bucket — molto più veloce del derive completo.",
    )
    parser.add_argument(
        "--check-gcs",
        action="store_true",
        help="Verify that public GCS paths resolve to at least one parquet.",
    )
    args = parser.parse_args()

    # Normalizza lo slug a underscore: i nomi candidate usano trattini
    # (sbarchi-migranti-italia) ma GCS usa underscore (sbarchi_migranti_italia/)
    if args.slug:
        args.slug = args.slug.replace("-", "_")

    # Il catalogo di partenza: vuoto se --derive, altrimenti da file
    if args.derive:
        raw: dict[str, Any] = {"datasets": []}
        if args.catalog.exists():
            try:
                raw = json.loads(args.catalog.read_text(encoding="utf-8"))
                print(f"[derive] Caricati metadata editoriali da {args.catalog}", file=sys.stderr)
            except Exception:
                print(f"[derive] WARN: cannot read {args.catalog}, starting fresh", file=sys.stderr)
        catalog, derive_errors = derive_catalog_from_gcs(raw, args.refresh_date, slug=args.slug)
    else:
        original_text = args.catalog.read_text(encoding="utf-8")
        catalog = json.loads(original_text)
        derive_errors = []

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    normalized = normalize_catalog(catalog, refresh_date=args.refresh_date)

    errors = validate_catalog(normalized, schema)
    errors.extend(derive_errors)
    if args.check_gcs:
        errors.extend(validate_gcs_locations(normalized))

    if errors and not args.write:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    output_text = json.dumps(normalized, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        args.catalog.write_text(output_text, encoding="utf-8")
        print(f"wrote {args.catalog}")
        return 0

    # Dry-run: --derive senza --write
    if args.derive:
        print(f"ok (dry-run, {len(normalized['datasets'])} datasets)")
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
    normalized["updated_at"] = (
        str(date.today()) if refresh_date else normalized.get("updated_at", str(date.today()))
    )

    datasets = []
    for dataset in normalized.get("datasets", []):
        item = dict(dataset)
        item.pop("status", None)  # vecchio nome, rimosso
        item.pop("visibility", None)  # sempre public, rimosso
        item.setdefault("stage", "incubating")
        datasets.append(item)
    normalized["datasets"] = sorted(datasets, key=lambda item: item["slug"])

    # Arricchisci source_id dai dataset.yml dei candidati
    _enrich_source_ids(normalized, ROOT)
    # Popola period da time_coverage nei dataset.yml
    _enrich_period_from_coverage(normalized, ROOT)
    # Popola tags e category dai dataset.yml dei candidati
    _enrich_tags_and_category(normalized, ROOT)

    return normalized


def _iter_dataset_ymls(root: Path):
    """Itera i dataset.yml di candidates/, support_datasets/ e compose/.

    Allineato allo standard candidate: i metadati (source_id, tags, category)
    valgono per tutte e tre le sezioni, non solo per i candidate.
    """
    for section in ("candidates", "support_datasets", "compose"):
        section_dir = root / section
        if not section_dir.is_dir():
            continue
        for entry_dir in sorted(section_dir.iterdir()):
            yml_path = entry_dir / "dataset.yml"
            if yml_path.is_file():
                yield yml_path


def _manifest_key(manifest: dict[str, Any]) -> str:
    """Chiave di match col catalogo: dataset.name (underscore), con fallback slug.

    Il catalogo usa lo slug del nome dataset (es. inps_pensioni_trimestrale),
    non il nome directory del candidate (inps-pensioni): matchnare su name
    evita i falsi negativi dell'enrich.
    """
    key = manifest.get("name") or manifest.get("slug") or ""
    return key.replace("-", "_")


def _enrich_source_ids(catalog: dict[str, Any], root: Path) -> None:
    """Legge source_id dai dataset.yml e li fonde nel catalogo.

    Per ogni dataset nel catalogo, se esiste un dataset.yml (candidate,
    support o compose) con source_id, lo aggiunge al catalogo (non
    sovrascrive se già presente).
    """
    slug_to_source: dict[str, str] = {}
    for yml_path in _iter_dataset_ymls(root):
        try:
            manifest = load_dataset_manifest(yml_path)
        except Exception:
            continue
        sid = manifest.get("source_id")
        key = _manifest_key(manifest)
        if sid and key:
            slug_to_source[key] = sid

    if not slug_to_source:
        return

    updated = 0
    for ds in catalog.get("datasets", []):
        slug = ds.get("slug", "")
        sid = slug_to_source.get(slug)
        if sid and not ds.get("source_id"):
            ds["source_id"] = sid
            updated += 1

    if updated:
        print(f"[enrich] source_id aggiunto a {updated} dataset da dataset.yml")


def _enrich_period_from_coverage(catalog: dict[str, Any], root: Path) -> None:
    """Popola period.start/.end dal time_coverage nei dataset.yml dei candidati.

    time_coverage.start_year / end_year nel dataset.yml dichiara la copertura
    temporale reale della fonte. Questo override del period derivato da GCS
    evita che period rifletta solo gli anni di cui abbiamo un parquet su GCS,
    il che sarebbe fuorviante per dataset con file snapshot multi-anno.
    """
    slug_to_period: dict[str, dict[str, int]] = {}
    for yml_path in _iter_dataset_ymls(root):
        try:
            manifest = load_dataset_manifest(yml_path)
        except Exception:
            continue
        tc = manifest.get("time_coverage")
        key = _manifest_key(manifest)
        if tc and key and "start_year" in tc and "end_year" in tc:
            slug_to_period[key] = {
                "start": tc["start_year"],
                "end": tc["end_year"],
            }

    if not slug_to_period:
        return

    updated = 0
    for ds in catalog.get("datasets", []):
        slug = ds.get("slug", "")
        new_period = slug_to_period.get(slug)
        if new_period:
            ds["period"] = new_period
            updated += 1

    if updated:
        print(f"[enrich] period aggiornato da time_coverage per {updated} dataset")


def _enrich_tags_and_category(catalog: dict[str, Any], root: Path) -> None:
    """Popola tags e category dai dataset.yml dei candidati.

    Legge tags e category via load_dataset_manifest() e li aggiunge
    all'entry del catalogo, se presenti nel dataset.yml.
    Non sovrascrive se già presenti (l'editoriale ha precedenza).
    """
    slug_to_tags: dict[str, list[str]] = {}
    slug_to_category: dict[str, str | None] = {}
    for yml_path in _iter_dataset_ymls(root):
        try:
            manifest = load_dataset_manifest(yml_path)
        except Exception:
            continue
        key = _manifest_key(manifest)
        tags = manifest.get("tags") or []
        category = manifest.get("category")
        if tags and key:
            slug_to_tags[key] = tags
        if category and key:
            slug_to_category[key] = category

    if not slug_to_tags and not slug_to_category:
        return

    updated_tags = 0
    updated_category = 0
    for ds in catalog.get("datasets", []):
        slug = ds.get("slug", "")
        if slug in slug_to_tags and "tags" not in ds:
            ds["tags"] = slug_to_tags[slug]
            updated_tags += 1
        if slug in slug_to_category and "category" not in ds:
            ds["category"] = slug_to_category[slug]
            updated_category += 1

    if updated_tags:
        print(f"[enrich] tags aggiunto a {updated_tags} dataset da dataset.yml")
    if updated_category:
        print(f"[enrich] category aggiunta a {updated_category} dataset da dataset.yml")


def derive_catalog_from_gcs(
    existing: dict[str, Any],
    refresh_date: bool = False,
    slug: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """Deriva il catalogo scansionando GCS e leggendo schemi parquet.

    1. Scansiona ``gs://dataciviclab-clean/`` per scoprire slug + anni
       (se ``slug`` è dato, limita la scansione a quel prefisso)
    2. Per ogni slug, legge lo schema del parquet più recente
    3. Costruisce location usando il path contract
    4. Fonde con metadata editoriali dal catalogo esistente
    5. Ritorna (catalogo, errori)

    Gli errori di lettura schema fanno fallire lo script: meglio catalogo
    bloccante che parziale.
    Returns:
        Tuple (catalogo_dict, lista_errori).
    """
    import duckdb

    from lab_connectors.gcs.paths import https_url as _https

    errors: list[str] = []
    slug_index: dict[str, set[str]] = {}
    bucket = "dataciviclab-clean"

    # Se slug è dato, scansiona solo quel prefisso — evita la scansione
    # completa del bucket (decine di migliaia di oggetti).
    prefix = f"{slug}/" if slug else ""
    print(
        f"[derive] Scansione GCS bucket {bucket} (prefix={prefix or 'tutto'})...", file=sys.stderr
    )

    # 1. Scansiona bucket per scoprire slug + anni
    try:
        objects = list_objects(bucket, prefix=prefix, auth=False)
    except Exception as exc:
        print(f"[derive] ERRORE: impossibile leggere GCS: {exc}", file=sys.stderr)
        return existing, [f"GCS unreachable: {exc}"]

    for obj in objects:
        name: str = obj["name"]
        parts = name.split("/")
        if len(parts) == 3 and parts[2].endswith("_clean.parquet"):
            slug_found, year = parts[0], parts[1]
            slug_index.setdefault(slug_found, set()).add(year)

    if not slug_index:
        print(
            f"[derive] Nessun parquet pulito trovato in {bucket} (prefix={prefix or 'tutto'})",
            file=sys.stderr,
        )
        return existing, []

    print(f"[derive] Trovati {len(slug_index)} slug su GCS", file=sys.stderr)

    # 2. Filtra slug con pipeline_run.json (gate: solo da pipeline)
    piped_slug_years: dict[str, set[str]] = {}
    for slug, slug_years in slug_index.items():
        for y in slug_years:
            if object_exists(bucket, f"{slug}/{y}/pipeline_run.json"):
                piped_slug_years[slug] = slug_years
                break
    skipped = len(slug_index) - len(piped_slug_years)
    if skipped:
        print(f"[derive] Esclusi {skipped} slug senza pipeline_run.json", file=sys.stderr)

    if not piped_slug_years:
        print(f"[derive] Nessun slug con pipeline_run.json in {bucket}", file=sys.stderr)
        return existing, []

    # 3. Costruisci indice editoriali per merge
    editorial = {}
    for ds in existing.get("datasets", []):
        editorial[ds["slug"]] = ds

    # 4. Per ogni slug, deriva entry
    datasets: list[dict[str, Any]] = []
    for slug in sorted(piped_slug_years):
        years = sorted(piped_slug_years[slug])
        if not years:
            continue

        multi_file = len(years) > 1
        gcs_path = (
            gs_url("clean", "clean_parquet", slug=slug, year="*")
            if multi_file
            else gs_url("clean", "clean_parquet", slug=slug, year=years[0])
        )

        # Leggi schema dal parquet più recente su GCS (via DuckDB read_parquet)
        alias_map = _load_semantic_type_map()
        columns: list[dict[str, str]] = []
        latest_year = years[-1]
        parquet_url = _https("clean", "clean_parquet", slug=slug, year=latest_year)
        try:
            with duckdb.connect() as con:
                rows = con.sql(f"DESCRIBE SELECT * FROM read_parquet('{parquet_url}')").fetchall()
            for row in rows:
                col_name = row[0]
                raw_type = str(row[1]).lower()
                # Mappa tipo DuckDB → catalogo (preserva BIGINT vs INTEGER)
                duckdb_to_catalog = {
                    "integer": "INTEGER",
                    "int32": "INTEGER",
                    "int": "INTEGER",
                    "bigint": "BIGINT",
                    "int64": "BIGINT",
                    "smallint": "INTEGER",
                    "tinyint": "INTEGER",
                    "hugeint": "BIGINT",
                    "float": "DOUBLE",
                    "real": "DOUBLE",
                    "double": "DOUBLE",
                    "decimal": "DOUBLE",
                    "numeric": "DOUBLE",
                    "varchar": "VARCHAR",
                    "text": "VARCHAR",
                    "char": "VARCHAR",
                    "date": "DATE",
                    "timestamp": "TIMESTAMP",
                    "timestamp_s": "TIMESTAMP",
                    "timestamp_ms": "TIMESTAMP",
                    "timestamp_ns": "TIMESTAMP",
                    "time": "TIME",
                    "boolean": "BOOLEAN",
                    "bool": "BOOLEAN",
                }
                bq_type = duckdb_to_catalog.get(raw_type, "VARCHAR")
                # DATE e BOOLEAN sono sempre dimensioni; numeri sono metric di default
                # (il merge editoriale preserva i role corretti)
                role = "dimension" if bq_type in ("VARCHAR", "DATE", "BOOLEAN") else "metric"
                # Assegna tipo semantico se riconoscibile (solo match esatto)
                semantic_type = _assign_semantic_type(col_name, alias_map)
                col_entry = {"name": col_name, "type": bq_type, "role": role, "description": ""}
                if semantic_type:
                    col_entry["semantic_type"] = semantic_type
                columns.append(col_entry)
        except Exception as exc:
            errors.append(f"{slug}: cannot read schema from {parquet_url}: {exc}")
            continue

        # Entry derivata
        entry: dict[str, Any] = {
            "slug": slug,
            "name": slug.replace("_", " ").title(),
            "description": "",
            "source": "",
            "source_id": "",
            "period": {"start": int(years[0]), "end": int(years[-1])},
            "columns": columns,
            "location": {"type": "gcs", "path": gcs_path, "multi_file": multi_file},
            "stage": "published",
            "registry_source": "derive_auto",
        }

        # Merge con editoriali: preserva campi umani
        old = editorial.get(slug)
        if old:
            for field in ("name", "description", "source", "source_id", "stage", "period"):
                if old.get(field):
                    entry[field] = old[field]
            # Preserva descrizione, role e semantic_type delle colonne dall'editoriale
            old_cols = {c["name"]: c for c in old.get("columns", [])}
            for col in entry["columns"]:
                oc = old_cols.get(col["name"])
                if oc:
                    if oc.get("description"):
                        col["description"] = oc["description"]
                    if oc.get("role"):
                        col["role"] = oc["role"]
                    # Preserva semantic_type manuale se diverso da quello derivato
                    oc_st = oc.get("semantic_type")
                    if oc_st:
                        col["semantic_type"] = oc_st

        datasets.append(entry)

    # 4. Preserva dataset editoriali non trovati su GCS (es. compositi)
    derived_slugs = {d["slug"] for d in datasets}
    for slug, ds in editorial.items():
        if slug not in derived_slugs:
            datasets.append(ds)
            print(f"[derive] Preservato dataset editoriale non su GCS: {slug}", file=sys.stderr)

    # 5. Assembla catalogo
    catalog: dict[str, Any] = {
        "schema_version": 1,
        "name": "Lab Clean Registry",
        "description": "Catalogo canonico dei clean parquet pubblici prodotti o adottati da dataset-incubator.",
        "source_repo": "dataciviclab/dataset-incubator",
        "updated_at": str(date.today()),
        "datasets": sorted(datasets, key=lambda d: d["slug"]),
    }

    nuovi = sum(1 for d in datasets if d["slug"] not in editorial)
    agg = sum(1 for d in datasets if d["slug"] in editorial)
    print(
        f"[derive] Catalogo: {len(datasets)} dataset ({nuovi} nuovi, {agg} aggiornati)",
        file=sys.stderr,
    )
    if errors:
        for e in errors:
            print(f"[derive] ERROR: {e}", file=sys.stderr)

    return catalog, errors


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
                    _validate_node(value, properties[field], root_schema, f"{path}.{field}")
                )

    if isinstance(instance, list):
        min_items = node.get("minItems")
        if min_items is not None and len(instance) < int(min_items):
            errors.append(f"{path}: expected at least {min_items} items")
        item_schema = node.get("items")
        if item_schema:
            for index, value in enumerate(instance):
                errors.extend(_validate_node(value, item_schema, root_schema, f"{path}[{index}]"))

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
            missing_years = missing_period_years(matches, dataset["period"])
            if missing_years:
                print(
                    f"  WARN {slug}: GCS gap for years {missing_years} (period={dataset['period']})",
                    file=sys.stderr,
                )
    return errors


def resolve_gcs_path(path: str) -> list[str]:
    if not path.startswith("gs://"):
        raise ValueError(f"not a GCS path: {path}")
    bucket, key = path[5:].split("/", 1)
    if "*" not in key:
        if not object_exists(bucket, key):
            return []
        return [key]

    prefix = key.split("*", 1)[0]
    names = list_gcs_objects(bucket, prefix)
    return [name for name in names if fnmatchcase(name, key)]


def list_gcs_objects(bucket: str, prefix: str) -> list[str]:
    """Lista oggetti GCS per un bucket/prefix.

    Delega a lab_connectors.gcs.list_objects con auth=False (HTTP API pubblica).
    """
    results = list_objects(bucket, prefix=prefix, auth=False)
    return [r["name"] for r in results]


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
