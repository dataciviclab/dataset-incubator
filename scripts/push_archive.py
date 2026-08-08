"""
push_archive.py — carica CLEAN e MART da DI/out/ su GCS

Struttura sorgente (toolkit):
  {DI_ROOT}/out/data/clean/{slug}/{year}/{slug}_{year}_clean.parquet
  {DI_ROOT}/out/data/mart/{slug}/{year}/mart_*.parquet

Struttura GCS:
  gs://dataciviclab-clean/{slug}/{year}/{slug}_{year}_clean.parquet  (pubblico)
  gs://dataciviclab-mart/{slug}/{year}/mart_*.parquet                (privato)

Uso:
  python push_archive.py --layer clean --slug ispra_ru_base --dry-run
  python push_archive.py --layer clean --slug ispra_ru_base
  python push_archive.py --layer mart  --slug ispra_ru_base
  python push_archive.py --layer mart  --slug ispra_ru_base --year 2024
  python push_archive.py --layer all                                   # tutti
  python push_archive.py --catalog-only --slug bdap_lea --update-catalog  # solo catalogo
"""

import argparse
import sys
import json
import datetime
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from lab_connectors.gcs import upload_file, upload_string

# Path contract canonico — vedere lab_connectors.gcs.paths per la documentazione
from lab_connectors.gcs.paths import (
    CLEAN_BUCKET,
    MART_BUCKET,
    catalog_manifest,
    gs_url,
    mart_parquet,
    pipeline_run,
)

from toolkit.contracts import layer_dataset_dir, run_record_dir as _run_record_dir

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DI_ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = DI_ROOT / "registry" / "clean_catalog.json"
OUT_ROOT = DI_ROOT / "out"


# Helper: directory radice di un layer (per scandire tutti gli slug).
# toolkit.contracts lavora per slug specifico; qui serve il contenitore.
def _layer_root(layer: str) -> Path:
    return OUT_ROOT / "data" / layer


# Helper per path canonici via toolkit.contracts
def _clean_dir(slug: str) -> Path:
    return layer_dataset_dir(OUT_ROOT, "clean", slug)


def _mart_dir(slug: str) -> Path:
    return layer_dataset_dir(OUT_ROOT, "mart", slug)


SKIP_DIRS = {"_validate", "_run"}
SKIP_SLUGS: set[str] = set()


# ---------------------------------------------------------------------------
# Helpers comuni
# ---------------------------------------------------------------------------
def get_slugs(root, slug_filter=None):
    if not root.exists():
        print(f"Directory non trovata: {root}", file=sys.stderr)
        sys.exit(1)
    slugs = [d.name for d in sorted(root.iterdir()) if d.is_dir() and d.name not in SKIP_SLUGS]
    if slug_filter:
        slugs = [s for s in slugs if s == slug_filter]
        if not slugs:
            # toolkit usa dataset.name (underscore), slugs hanno hyphens
            alt = slug_filter.replace("-", "_")
            slugs = [s for s in slugs if s == alt]
        if not slugs:
            print(f"Slug non trovato: {slug_filter}", file=sys.stderr)
            sys.exit(1)
    return slugs


def get_years(slug_dir, year_filter=None):
    years = [
        d.name
        for d in sorted(slug_dir.iterdir())
        if d.is_dir() and d.name not in SKIP_DIRS and d.name.isdigit()
    ]
    if year_filter:
        years = [y for y in years if y == str(year_filter)]
    return years


def get_parquets(year_dir):
    return sorted(year_dir.glob("*.parquet"))


def get_latest_run(slug, year):
    """Restituisce il JSON record dell'ultimo run, o None se non esiste."""
    run_dir = _run_record_dir(OUT_ROOT, slug, year)
    if not run_dir.exists():
        return None
    runs = sorted(run_dir.glob("*.json"))
    return runs[-1] if runs else None


# ---------------------------------------------------------------------------
# GCS — delegato a lab_connectors.gcs
# ---------------------------------------------------------------------------
def push_gcs(local_path, bucket_name, gcs_path, dry_run=False):
    if dry_run:
        print(f"  [dry] GCS: gs://{bucket_name}/{gcs_path}")
        return
    upload_file(str(local_path), bucket_name, gcs_path)
    print(f"  GCS: gs://{bucket_name}/{gcs_path}")


def upload_manifest(manifest, dry_run=False):
    manifest_path = catalog_manifest()
    manifest_gs = gs_url("clean", "catalog_manifest")
    if dry_run:
        print(f"  [dry] GCS: {manifest_gs}")
        return
    upload_string(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        CLEAN_BUCKET,
        manifest_path,
        content_type="application/json",
    )
    print(f"  GCS: {manifest_gs}")


# ---------------------------------------------------------------------------
# Catalog update
# ---------------------------------------------------------------------------
_PARQUET_TYPE_MAP = {
    "int8": "INTEGER",
    "int16": "INTEGER",
    "int32": "INTEGER",
    "int64": "INTEGER",
    "uint8": "INTEGER",
    "uint16": "INTEGER",
    "uint32": "INTEGER",
    "uint64": "INTEGER",
    "float": "DOUBLE",
    "double": "DOUBLE",
    "float32": "DOUBLE",
    "float64": "DOUBLE",
    "bool": "BOOLEAN",
    "boolean": "BOOLEAN",
    "date32[day]": "DATE",
    "date64[us]": "TIMESTAMP",
    "timestamp[us]": "TIMESTAMP",
    "timestamp[ms]": "TIMESTAMP",
}


def _parquet_columns(parquet_path: Path) -> list[dict]:
    schema = pq.read_schema(parquet_path)
    cols = []
    for i, name in enumerate(schema.names):
        raw_type = str(schema.field(name).type)
        bq_type = _PARQUET_TYPE_MAP.get(raw_type, "VARCHAR")
        cols.append({"name": name, "type": bq_type, "role": "", "description": ""})
    return cols


def update_catalog(slug: str, years: list[str], status: str, dry_run: bool = False) -> None:
    """Aggiorna clean_catalog.json per lo slug: upsert period, location e colonne."""
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    datasets = catalog.get("datasets", [])
    existing = next((d for d in datasets if d["slug"] == slug), None)

    int_years = sorted(int(y) for y in years)
    multi_file = len(int_years) > 1
    if multi_file:
        gcs_path = gs_url("clean", "clean_parquet", slug=slug, year="*")
    else:
        gcs_path = gs_url("clean", "clean_parquet", slug=slug, year=int_years[0])

    # Leggi schema dal parquet più recente disponibile
    latest_parquet = None
    for year in reversed(sorted(years)):
        candidates = list(_clean_dir(slug).glob(f"{year}/*_clean.parquet"))
        if candidates:
            latest_parquet = candidates[0]
            break

    if existing:
        existing["period"]["start"] = min(
            int_years[0], existing["period"].get("start", int_years[0])
        )
        existing["period"]["end"] = max(int_years[-1], existing["period"].get("end", int_years[-1]))
        existing["location"] = {"type": "gcs", "path": gcs_path, "multi_file": multi_file}
        if latest_parquet and not existing.get("columns"):
            existing["columns"] = _parquet_columns(latest_parquet)
        action = "aggiornato"
    else:
        cols = _parquet_columns(latest_parquet) if latest_parquet else []
        new_entry = {
            "slug": slug,
            "name": slug.replace("_", " ").title(),
            "description": "",
            "source": "",
            "source_id": "",
            "period": {"start": int_years[0], "end": int_years[-1]},
            "columns": cols,
            "location": {"type": "gcs", "path": gcs_path, "multi_file": multi_file},
            "stage": "published",
            "registry_source": "push_archive_auto",
        }
        datasets.append(new_entry)
        action = f"aggiunto ({status})"

    catalog["datasets"] = sorted(datasets, key=lambda d: d["slug"])
    catalog["updated_at"] = datetime.date.today().isoformat()

    if dry_run:
        print(f"  [dry] catalog: {slug} {action}")
        return

    CATALOG_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"  catalog: {slug} {action}")


# ---------------------------------------------------------------------------
# Layer: CLEAN
# ---------------------------------------------------------------------------
def push_clean(slug_filter=None, year_filter=None, dry_run=False):
    clean_root = _layer_root("clean")
    slugs = get_slugs(clean_root, slug_filter)
    print(f"[clean] slug: {slugs}\n")

    manifest = {
        "generated_at": pd.Timestamp.now("UTC").isoformat(),
        "bucket": CLEAN_BUCKET,
        "items": [],
    }

    for slug in slugs:
        slug_dir = _clean_dir(slug)
        years = get_years(slug_dir, year_filter)
        if not years:
            print(f"  [{slug}] nessun anno, salto.")
            continue

        print(f"[{slug}] anni: {years}")
        for year in years:
            for parq in get_parquets(slug_dir / year):
                gcs_path = f"{slug}/{year}/{parq.name}"
                push_gcs(parq, CLEAN_BUCKET, gcs_path, dry_run)
                if dry_run:
                    rows = None
                else:
                    try:
                        rows = len(pd.read_parquet(parq))
                    except Exception:
                        rows = None
                manifest["items"].append(
                    {
                        "slug": slug,
                        "year": int(year),
                        "file": parq.name,
                        "gcs_path": gcs_path,
                        "gcs_url": f"gs://{CLEAN_BUCKET}/{gcs_path}",
                        "updated_at": pd.Timestamp(parq.stat().st_mtime, unit="s").isoformat(),
                        "rows": rows,
                    }
                )

            run_record = get_latest_run(slug, year)
            if run_record is not None:
                run_gcs_path = pipeline_run(slug, year)
                push_gcs(run_record, CLEAN_BUCKET, run_gcs_path, dry_run)
            else:
                print(
                    f"  [{slug}/{year}] nessun run record trovato, pipeline_run.json non pushato."
                )
        print()

    if manifest["items"]:
        upload_manifest(manifest, dry_run)


# ---------------------------------------------------------------------------
# Layer: MART
# ---------------------------------------------------------------------------
def push_mart(slug_filter=None, year_filter=None, dry_run=False):
    mart_root = _layer_root("mart")
    slugs = get_slugs(mart_root, slug_filter)
    print(f"[mart] slug: {slugs}\n")

    for slug in slugs:
        slug_dir = _mart_dir(slug)
        years = get_years(slug_dir, year_filter)
        if not years:
            print(f"  [{slug}] nessun anno, salto.")
            continue

        print(f"[{slug}] anni: {years}")

        for year in years:
            for parq in get_parquets(slug_dir / year):
                gcs_path = mart_parquet(slug, year, parq.stem)
                push_gcs(parq, MART_BUCKET, gcs_path, dry_run)
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Push CLEAN/MART → GCS")
    parser.add_argument(
        "--layer",
        choices=["clean", "mart", "all"],
        default="all",
        help="Layer da pushare (default: all)",
    )
    parser.add_argument("--slug", help="Slug specifico (default: tutti)")
    parser.add_argument("--year", help="Anno specifico (default: tutti)")
    parser.add_argument("--dry-run", action="store_true", help="Simula senza caricare")
    parser.add_argument(
        "--update-catalog",
        action="store_true",
        help="Aggiorna registry/clean_catalog.json con period e location aggiornati",
    )
    parser.add_argument(
        "--status",
        default="candidate",
        choices=["candidate", "clean_ready", "public_catalog_ready"],
        help="Status da impostare nel catalog per i nuovi entry (default: candidate)",
    )
    parser.add_argument(
        "--catalog-only", action="store_true", help="Solo aggiornamento catalogo, senza push GCS"
    )
    args = parser.parse_args()

    # --catalog-only disabilita il push GCS, solo catalogo
    if args.catalog_only:
        args.layer = None

    if args.layer in ("clean", "all") and not args.catalog_only:
        push_clean(args.slug, args.year, args.dry_run)

    if args.update_catalog:
        clean_root = _layer_root("clean")
        slugs = get_slugs(clean_root, args.slug)
        for slug in slugs:
            years = get_years(_clean_dir(slug))
            update_catalog(slug, years, args.status, args.dry_run)

    if args.layer in ("mart", "all"):
        push_mart(args.slug, args.year, args.dry_run)

    print("Done.")


if __name__ == "__main__":
    main()
