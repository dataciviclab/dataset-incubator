"""
push_archive.py — carica CLEAN e MART da DI/out/ su GCS + BigQuery

Struttura sorgente (toolkit):
  {DI_ROOT}/out/data/clean/{slug}/{year}/{slug}_{year}_clean.parquet
  {DI_ROOT}/out/data/mart/{slug}/{year}/mart_*.parquet

Struttura GCS:
  gs://dataciviclab-clean/{slug}/{year}/{slug}_{year}_clean.parquet  (pubblico)
  gs://dataciviclab-mart/{slug}/{year}/mart_*.parquet                (privato)

Struttura BigQuery (solo mart):
  project: dataciviclab
  dataset: {slug}        (auto-creato se non esiste, location EU)
  table:   {parquet_stem}

Uso:
  python push_archive.py --layer clean --slug ispra_ru_base --dry-run
  python push_archive.py --layer clean --slug ispra_ru_base
  python push_archive.py --layer mart  --slug ispra_ru_base
  python push_archive.py --layer mart  --slug ispra_ru_base --year 2024
  python push_archive.py --layer all                                   # tutti
"""

import argparse
import sys
import json
from pathlib import Path

import pandas as pd
from google.cloud import bigquery, storage
from google.api_core.exceptions import Conflict

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
GCP_PROJECT = "dataciviclab"
GCS_CLEAN_BUCKET = "dataciviclab-clean"
GCS_MART_BUCKET = "dataciviclab-mart"
BQ_LOCATION = "EU"
CATALOG_MANIFEST_PATH = "catalog/manifest.json"

DI_ROOT = Path(__file__).resolve().parents[1]
CLEAN_ROOT = DI_ROOT / "out" / "data" / "clean"
MART_ROOT = DI_ROOT / "out" / "data" / "mart"

SKIP_DIRS = {"_validate", "_run"}
SKIP_SLUGS = {"malasanita_struttura_mortalita_source_d_test"}  # slug da escludere dal push


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
            print(f"Slug non trovato: {slug_filter}", file=sys.stderr)
            sys.exit(1)
    return slugs


def get_years(slug_dir, year_filter=None):
    years = [
        d.name for d in sorted(slug_dir.iterdir())
        if d.is_dir() and d.name not in SKIP_DIRS and d.name.isdigit()
    ]
    if year_filter:
        years = [y for y in years if y == str(year_filter)]
    return years


def get_parquets(year_dir):
    return sorted(year_dir.glob("*.parquet"))


# ---------------------------------------------------------------------------
# GCS
# ---------------------------------------------------------------------------
def push_gcs(gcs_client, local_path, bucket_name, gcs_path, dry_run=False):
    if dry_run:
        print(f"  [dry] GCS: gs://{bucket_name}/{gcs_path}")
        return
    bucket = gcs_client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(str(local_path))
    print(f"  GCS: gs://{bucket_name}/{gcs_path}")


def upload_manifest(gcs_client, manifest, dry_run=False):
    if dry_run:
        print(f"  [dry] GCS: gs://{GCS_CLEAN_BUCKET}/{CATALOG_MANIFEST_PATH}")
        return
    bucket = gcs_client.bucket(GCS_CLEAN_BUCKET)
    blob = bucket.blob(CATALOG_MANIFEST_PATH)
    blob.upload_from_string(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        content_type="application/json",
    )
    print(f"  GCS: gs://{GCS_CLEAN_BUCKET}/{CATALOG_MANIFEST_PATH}")


# ---------------------------------------------------------------------------
# BigQuery
# ---------------------------------------------------------------------------
def ensure_bq_dataset(bq_client, dataset_id, dry_run=False):
    full_id = f"{GCP_PROJECT}.{dataset_id}"
    if dry_run:
        print(f"  [dry] BQ dataset: {full_id}")
        return
    dataset = bigquery.Dataset(full_id)
    dataset.location = BQ_LOCATION
    try:
        bq_client.create_dataset(dataset)
        print(f"  BQ dataset creato: {full_id}")
    except Conflict:
        pass


def push_bq(bq_client, local_path, slug, year, dry_run=False):
    df = pd.read_parquet(local_path)
    table_name = local_path.stem
    table_id = f"{GCP_PROJECT}.{slug}.{table_name}"

    if dry_run:
        print(f"  [dry] BQ: {table_id} ({len(df)} righe, cols: {list(df.columns)})")
        return

    if "anno" not in df.columns:
        df["anno"] = int(year)

    # Converti anno in DATE (1 gennaio dell'anno) per partizione BQ e Looker Studio
    df["data_anno"] = pd.to_datetime(df["anno"].astype(str) + "-01-01").dt.date

    # Elimina righe esistenti per questo anno prima di ricaricare
    try:
        bq_client.query(f"DELETE FROM `{table_id}` WHERE anno = {year}").result()
    except Exception:
        pass  # tabella non esiste ancora — ok

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
        autodetect=True,
    )
    job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"  BQ: {table_id} ({len(df)} righe)")


# ---------------------------------------------------------------------------
# Layer: CLEAN
# ---------------------------------------------------------------------------
def push_clean(gcs_client, slug_filter=None, year_filter=None, dry_run=False):
    slugs = get_slugs(CLEAN_ROOT, slug_filter)
    print(f"[clean] slug: {slugs}\n")

    manifest = {
        "generated_at": pd.Timestamp.utcnow().isoformat(),
        "bucket": GCS_CLEAN_BUCKET,
        "items": [],
    }

    for slug in slugs:
        slug_dir = CLEAN_ROOT / slug
        years = get_years(slug_dir, year_filter)
        if not years:
            print(f"  [{slug}] nessun anno, salto.")
            continue

        print(f"[{slug}] anni: {years}")
        for year in years:
            for pq in get_parquets(slug_dir / year):
                gcs_path = f"{slug}/{year}/{pq.name}"
                push_gcs(gcs_client, pq, GCS_CLEAN_BUCKET, gcs_path, dry_run)
                if dry_run:
                    rows = None
                else:
                    try:
                        rows = len(pd.read_parquet(pq))
                    except Exception:
                        rows = None
                manifest["items"].append(
                    {
                        "slug": slug,
                        "year": int(year),
                        "file": pq.name,
                        "gcs_path": gcs_path,
                        "gcs_url": f"gs://{GCS_CLEAN_BUCKET}/{gcs_path}",
                        "updated_at": pd.Timestamp(pq.stat().st_mtime, unit="s").isoformat(),
                        "rows": rows,
                    }
                )
        print()

    if manifest["items"]:
        upload_manifest(gcs_client, manifest, dry_run)


# ---------------------------------------------------------------------------
# Layer: MART
# ---------------------------------------------------------------------------
def push_mart(gcs_client, bq_client, slug_filter=None, year_filter=None, dry_run=False):
    slugs = get_slugs(MART_ROOT, slug_filter)
    print(f"[mart] slug: {slugs}\n")

    for slug in slugs:
        slug_dir = MART_ROOT / slug
        years = get_years(slug_dir, year_filter)
        if not years:
            print(f"  [{slug}] nessun anno, salto.")
            continue

        print(f"[{slug}] anni: {years}")
        if bq_client:
            ensure_bq_dataset(bq_client, slug, dry_run)

        for year in years:
            for pq in get_parquets(slug_dir / year):
                gcs_path = f"{slug}/{year}/{pq.name}"
                push_gcs(gcs_client, pq, GCS_MART_BUCKET, gcs_path, dry_run)
                if bq_client:
                    push_bq(bq_client, pq, slug, year, dry_run)
        print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Push CLEAN/MART → GCS + BigQuery")
    parser.add_argument("--layer", choices=["clean", "mart", "all"], default="all",
                        help="Layer da pushare (default: all)")
    parser.add_argument("--slug", help="Slug specifico (default: tutti)")
    parser.add_argument("--year", help="Anno specifico (default: tutti)")
    parser.add_argument("--dry-run", action="store_true", help="Simula senza caricare")
    parser.add_argument("--no-bq", action="store_true", help="Salta BigQuery (solo GCS)")
    args = parser.parse_args()

    gcs_client = storage.Client(project=GCP_PROJECT)
    bq_client = bigquery.Client(project=GCP_PROJECT) if not args.no_bq else None

    if args.layer in ("clean", "all"):
        push_clean(gcs_client, args.slug, args.year, args.dry_run)

    if args.layer in ("mart", "all"):
        push_mart(gcs_client, bq_client, args.slug, args.year, args.dry_run)

    print("Done.")


if __name__ == "__main__":
    main()
