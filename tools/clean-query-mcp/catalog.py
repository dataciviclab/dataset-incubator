from __future__ import annotations

import os
import re
import threading
import time
import json
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode
from urllib.request import urlopen

DI_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG_PATH = DI_ROOT / "registry" / "clean_catalog.json"
CATALOG_PATH = Path(os.environ.get("CLEAN_QUERY_CATALOG_PATH", DEFAULT_CATALOG_PATH))
_cache: dict[str, Any] | None = None
_cache_lock = threading.Lock()

# GCS resolution cache: { (slug, year): (timestamp, [urls]) }
_gcs_res_cache: dict[tuple, tuple[float, list[str]]] = {}
_gcs_res_cache_ttl = int(
    os.environ.get("CLEAN_QUERY_GCS_CACHE_TTL", "300")
)  # 5 min default
_gcs_res_lock = threading.Lock()

# Lazy GCS client
_gcs_instance = None


def _get_gcs_client():
    global _gcs_instance
    if _gcs_instance is None:
        use_auth = os.environ.get("CLEAN_QUERY_GCS_AUTH", "").lower() in {
            "1",
            "true",
            "yes",
        }
        if use_auth:
            try:
                from google.cloud import storage

                _gcs_instance = storage.Client(project="dataciviclab")
            except Exception:
                _gcs_instance = False
        else:
            try:
                from google.cloud import storage

                _gcs_instance = storage.Client.create_anonymous_client()
            except Exception:
                _gcs_instance = False
    return _gcs_instance


def _load_catalog() -> list[dict[str, Any]]:
    global _cache
    with _cache_lock:
        if _cache is not None:
            return _cache
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        _cache = data.get("datasets", [])
        return _cache


def list_datasets() -> list[dict[str, Any]]:
    catalog = _load_catalog()
    return [
        {
            "slug": ds["slug"],
            "name": ds["name"],
            "description": ds["description"],
            "source": ds.get("source"),
            "period_start": ds["period"]["start"],
            "period_end": ds["period"]["end"],
        }
        for ds in catalog
    ]


def describe_dataset(slug: str) -> dict[str, Any]:
    catalog = _load_catalog()
    ds = next((d for d in catalog if d["slug"] == slug), None)
    if ds is None:
        slugs = [d["slug"] for d in catalog]
        return {
            "error": f"Dataset '{slug}' non trovato. Disponibili: {', '.join(slugs)}"
        }
    return {
        "slug": ds["slug"],
        "name": ds["name"],
        "description": ds["description"],
        "source": ds.get("source"),
        "period": ds["period"],
        "columns": ds["columns"],
        "location_type": ds["location"]["type"],
        "location_path": ds["location"]["path"],
    }


def resolve_parquet_path(slug: str, year: int | None = None) -> list[str]:
    """Resolve dataset location to a list of HTTPS URLs.

    For multi_file datasets, expands the glob by listing GCS blobs.
    Results are cached for _gcs_res_cache_ttl seconds.
    For single-file datasets, returns a list with one URL.
    If year is specified, filters to that specific year's file.
    """
    catalog = _load_catalog()
    ds = next((d for d in catalog if d["slug"] == slug), None)
    if ds is None:
        raise ValueError(f"Dataset '{slug}' non trovato nel catalogo")

    loc = ds["location"]
    cache_key = (slug, year)

    # Check GCS resolution cache for multi_file
    if loc["type"] == "gcs" and loc.get("multi_file"):
        with _gcs_res_lock:
            if cache_key in _gcs_res_cache:
                ts, urls = _gcs_res_cache[cache_key]
                if time.time() - ts < _gcs_res_cache_ttl:
                    return urls

    if loc["type"] == "local":
        path = loc["path"]
        full = (DI_ROOT / path).resolve()
        if not full.exists():
            raise FileNotFoundError(
                f"Parquet locale non trovato: {full}. "
                f"Esegui 'toolkit run' per {slug} oppure usa il dataset da GCS."
            )
        urls = [str(full)]
    elif loc["type"] == "gcs":
        raw = loc["path"]
        multi_file = loc.get("multi_file", False)
        bucket_and_key = raw[5:]
        bucket, key = bucket_and_key.split("/", 1)

        if multi_file and "*" in key:
            prefix = key.split("*")[0]
            blobs = _list_gcs_blobs(bucket, prefix=prefix)
            pattern = _glob_to_regex(key)
            urls = []
            for blob_name in sorted(blobs):
                if blob_name.endswith("_clean.parquet"):
                    if pattern.match(blob_name):
                        if year and f"/{year}/" not in blob_name:
                            continue
                        urls.append(
                            f"https://storage.googleapis.com/{bucket}/{quote(blob_name, safe='/._-')}"
                        )
            if not urls:
                raise FileNotFoundError(
                    f"Nessun file trovato per pattern '{raw}'"
                    + (f" anno={year}" if year else "")
                )
            # Cache the result
            with _gcs_res_lock:
                _gcs_res_cache[cache_key] = (time.time(), urls)
        else:
            urls = [
                f"https://storage.googleapis.com/{bucket}/{quote(key, safe='/._-')}"
            ]
    else:
        raise ValueError(f"Tipo location non supportato: {loc['type']}")

    return urls


def gcs_cache_stats() -> dict[str, Any]:
    """Return stats about the GCS resolution cache."""
    now = time.time()
    with _gcs_res_lock:
        total = len(_gcs_res_cache)
        valid = sum(
            1 for ts, _ in _gcs_res_cache.values() if now - ts < _gcs_res_cache_ttl
        )
        entries = []
        for (slug, year), (ts, urls) in sorted(
            _gcs_res_cache.items(), key=lambda item: (item[0][0], item[0][1] or 0)
        ):
            age = now - ts
            entries.append(
                {
                    "slug": slug,
                    "year": year,
                    "file_count": len(urls),
                    "age_sec": round(age, 1),
                    "fresh": age < _gcs_res_cache_ttl,
                }
            )
    return {
        "total_entries": total,
        "valid_entries": valid,
        "ttl_sec": _gcs_res_cache_ttl,
        "entries": entries,
    }


def gcs_cache_clear() -> None:
    """Clear the GCS resolution cache."""
    with _gcs_res_lock:
        _gcs_res_cache.clear()


def _list_gcs_blobs(bucket: str, prefix: str) -> list[str]:
    """List blob names from GCS bucket with given prefix."""
    client = _get_gcs_client()
    if client:
        blobs = client.list_blobs(bucket, prefix=prefix)
        return [b.name for b in blobs]

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


def _glob_to_regex(pattern: str) -> re.Pattern:
    """Convert a simple glob pattern (* only) to compiled regex."""
    escaped = ""
    for ch in pattern:
        if ch == "*":
            escaped += ".*"
        elif ch in r"\.+(){}^$|":
            escaped += "\\" + ch
        else:
            escaped += ch
    return re.compile("^" + escaped + "$")
