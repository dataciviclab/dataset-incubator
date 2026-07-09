#!/usr/bin/env python3
"""Runner per il workflow post-merge-candidate.yml.

Estratto dalla logica inline Python nei job sample_run e build-and-pr
del workflow GHA post-merge-candidate.yml.

Subcommands:
    sample-run    Esegue toolkit run full + GCS push + catalog rebuild
                  per ogni config rilevato in detect_output.json.
                  Sostituisce il blocco inline 'Process each detected config'.

    build-pr-body  Genera il body markdown della PR registry.
                   Sostituisce il blocco inline 'Build draft PR body'.

Usage:
    python scripts/post_merge_runner.py sample-run [--detect-json PATH]
    python scripts/post_merge_runner.py build-pr-body [--detect-json PATH] \\
        --pr-number NUM --pr-title TITLE [--sample-result success|skipped] \\
        [--signals-changed true|false]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# sample-run
# ---------------------------------------------------------------------------


def _read_detect_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _ca_cert_setup(config_path: str, artifact_name: str, root: str) -> None:
    """Configure extra CA certificates if the config requires them."""
    r = subprocess.run(
        ["python", "scripts/get_extra_ca_cert_urls.py", config_path],
        capture_output=True,
        text=True,
        cwd=root,
    )
    urls = [u.strip() for u in r.stdout.strip().split("\n") if u.strip()]
    if not urls:
        return

    bundle = f"/tmp/extra-ca-{artifact_name}.pem"
    with open("/etc/ssl/certs/ca-certificates.crt") as src, open(bundle, "w") as dst:
        dst.write(src.read())

    for url in urls:
        try:
            data = urllib.request.urlopen(url).read()
            with open(bundle, "a") as dst:
                dst.write(data.decode() if isinstance(data, bytes) else data)
        except Exception as e:
            print(f"  WARN CA cert {url}: {e}")

    os.environ["REQUESTS_CA_BUNDLE"] = bundle
    os.environ["SSL_CERT_FILE"] = bundle


def _resolve_years(config_path: str, root: str) -> list[int]:
    """Resolve all_years from resolve_sample_run.py."""
    r = subprocess.run(
        ["python", "scripts/resolve_sample_run.py", config_path],
        capture_output=True,
        text=True,
        cwd=root,
    )
    if r.returncode != 0:
        raise RuntimeError(f"resolve fallito ({r.stderr.strip()})")
    params = json.loads(r.stdout)
    return params.get("all_years", [])


def _run_with_retry(cmd: list[str], cwd: str, attempts: int = 3) -> bool:
    for i in range(1, attempts + 1):
        r = subprocess.run(cmd, cwd=cwd)
        if r.returncode == 0:
            return True
        if i < attempts:
            wait = 20 * i
            print(f"    tentativo {i}/{attempts} fallito, riprovo tra {wait}s...")
            time.sleep(wait)
    return False


def _push_clean_to_gcs(slug: str, root: str) -> bool:
    """Push clean parquet to GCS. Returns True on success."""
    r = subprocess.run(
        ["python", "scripts/push_archive.py", "--layer", "clean", "--slug", slug, "--no-bq"],
        cwd=root,
    )
    return r.returncode == 0


def _rebuild_clean_catalog(root: str) -> None:
    """Rebuild clean_catalog.json after GCS push."""
    r = subprocess.run(
        ["python", "scripts/build_clean_catalog.py", "--derive", "--write"],
        cwd=root,
    )
    if r.returncode != 0:
        print(f"  WARN: build_clean_catalog --derive --write fallito (code {r.returncode})")

    r = subprocess.run(
        ["python", "scripts/build_clean_catalog.py", "--check-gcs"],
        cwd=root,
    )
    if r.returncode != 0:
        print(f"  WARN: build_clean_catalog --check-gcs ha trovato errori (code {r.returncode})")


def cmd_sample_run(args: argparse.Namespace) -> None:
    """Process each detected config: toolkit run, GCS push, catalog."""
    detect = _read_detect_json(args.detect_json)
    configs = detect.get("configs", [])
    if not configs:
        print("Nessun config da processare")
        return

    root = os.environ.get("GITHUB_WORKSPACE", ".")
    failed_configs: list[str] = []
    gcs_push_ok = False

    # Pre-install GCS lib se GCP auth disponibile
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        subprocess.run(
            ["python", "-m", "pip", "install", "google-cloud-storage", "-q"],
            capture_output=True,
        )

    for cfg in configs:
        config_path = cfg.get("config_path", "")
        slug = cfg.get("slug", "unknown")
        artifact_name = cfg.get("artifact_name", slug)
        config_exists = cfg.get("config_exists", False)

        print(f"\n=== Processing {slug} ({config_path}) ===")

        if not config_exists:
            print("  SKIP: config_path non esiste")
            continue

        # --- CA certs ---
        _ca_cert_setup(config_path, artifact_name, root)

        # --- Resolve ---
        try:
            all_years = _resolve_years(config_path, root)
        except RuntimeError as e:
            print(f"  FAIL: {e}")
            failed_configs.append(slug)
            continue

        years_str = ",".join(str(y) for y in all_years)

        # --- Toolkit run full (run + validate + readiness + support) ---
        # Se un candidate ha bisogno di proxy per raggiungere la fonte,
        # impostalo via os.environ nello script di download.
        print(f"  toolkit run full --years {years_str}")
        run_ok = _run_with_retry(
            ["toolkit", "run", "full", "--config", config_path, "--years", years_str, "--json"],
            cwd=root,
            attempts=args.retry,
        )

        status = "passed" if run_ok else "failed"
        if status == "failed":
            failed_configs.append(slug)

        run_id = os.environ.get("GITHUB_RUN_ID", "0")
        repo = os.environ.get("GITHUB_REPOSITORY", "")
        # Compose datasets usano prefisso "compose:" per allinearsi
        # a build_pipeline_signals.py che lo usa per evitare collisioni
        resolved_id = f"compose:{slug}" if config_path.startswith("compose/") else slug
        payload = {
            "id": resolved_id,
            "status": status,
            "years": all_years,
            "config_path": config_path,
            "config_exists": config_exists,
            "run_id": run_id,
            "run_url": f"https://github.com/{repo}/actions/runs/{run_id}",
            "checked_at": datetime.now(timezone.utc).date().isoformat(),
        }
        out_dir = f"sample_run_artifacts/{artifact_name}"
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        with open(f"{out_dir}/sample_run_result.json", "w") as pf:
            json.dump(payload, pf, indent=2)
        print(f"  {status}")

        # --- GCS push (solo per candidate, non per compose) ---
        is_compose = config_path.startswith("compose/")
        if status == "passed" and os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and not is_compose:
            print(f"  GCS push per {slug}...")
            push_slug = cfg.get("push_slug", slug)
            if _push_clean_to_gcs(push_slug, root):
                print(f"  GCS push completato per {slug} (push_slug={push_slug})")
                gcs_push_ok = True
            else:
                print(f"  GCS push FAILED for {slug}")
                failed_configs.append(slug)
        elif is_compose:
            print(f"  SKIP GCS push: compose dataset (solo mart, no clean)")

    # --- Clean catalog rebuild ---
    if gcs_push_ok:
        print("\n  Rebuilding clean catalog...")
        _rebuild_clean_catalog(root)
    else:
        print("\n  Skip clean catalog rebuild: nessun GCS push riuscito")

    if failed_configs:
        print("\nFAIL: one or more configs failed in post-merge full run:")
        for slug in failed_configs:
            print(f" - {slug}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# build-pr-body
# ---------------------------------------------------------------------------


def cmd_build_pr_body(args: argparse.Namespace) -> None:
    """Generate the PR body markdown for the registry PR."""
    detect = _read_detect_json(args.detect_json)
    items = detect.get("items", [])
    configs = detect.get("configs", [])

    gcp_available = (
        os.environ.get("GCP_WORKLOAD_IDENTITY_PROVIDER", "") != ""
        and os.environ.get("GCP_SERVICE_ACCOUNT", "") != ""
    )

    item_list = "\n".join(f"- `{i['slug']}` ({i['kind']}, `{i['root']}`)" for i in items)
    sample_list = (
        "\n".join(
            f"- `{c['config_path']}` -> artifact `sample-run-{c['artifact_name']}`" for c in configs
        )
        or "- No sample-run config detected"
    )

    body = "\n".join(
        [
            "## Post-merge registry handoff",
            "",
            f"Source PR: #{args.pr_number} — {args.pr_title}",
            "",
            "Changed candidate/support roots:",
            "",
            item_list,
            "",
            "## Cosa ha fatto CI",
            "",
            "- [x] Full run toolkit (tutti gli anni)",
            f"- [{'x' if gcp_available else ' '}] Clean parquet pushato su GCS",
            "- [x] `registry/pipeline_signals.json` aggiornato",
            f"- [{'x' if gcp_available else ' '}] `registry/clean_catalog.json` auto-derivato",
            "",
            "## Sample-run artifacts",
            "",
            sample_list,
            "",
            "## Cosa fare (solo per slug nuovi)",
            "",
            "1. Compilare `name`, `description`, `source`, `source_id`, e descrizioni/role delle colonne in `registry/clean_catalog.json`",
            "2. `python scripts/build_clean_catalog.py --check-gcs`",
            "3. Commit, push, mergiare la PR",
        ]
    )

    out_path = args.output
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(body + "\n")
    print(f"PR body scritto in {out_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Post-merge runner per dataset-incubator")
    sub = parser.add_subparsers(dest="command", required=True)

    # sample-run
    p_sample = sub.add_parser(
        "sample-run", help="Esegui toolkit run full + GCS push per ogni config"
    )
    p_sample.add_argument(
        "--detect-json",
        default="detect_output.json",
        help="Path a detect_output.json (default: detect_output.json)",
    )
    p_sample.add_argument(
        "--retry",
        type=int,
        default=3,
        help="Numero di tentativi per toolkit run (default: 3)",
    )

    # build-pr-body
    p_body = sub.add_parser("build-pr-body", help="Genera il body della PR registry")
    p_body.add_argument(
        "--detect-json",
        default="detect_output.json",
        help="Path a detect_output.json (default: detect_output.json)",
    )
    p_body.add_argument("--pr-number", required=True, help="Numero della PR sorgente")
    p_body.add_argument("--pr-title", required=True, help="Titolo della PR sorgente")
    p_body.add_argument(
        "--sample-result",
        default="skipped",
        choices=["success", "skipped", "failure"],
        help="Risultato del job sample_run (default: skipped)",
    )
    p_body.add_argument(
        "--signals-changed",
        default="false",
        choices=["true", "false"],
        help="Se pipeline_signals.json è cambiato (default: false)",
    )
    p_body.add_argument(
        "--output",
        default="post_merge_pr_body.md",
        help="Path di output per il body markdown (default: post_merge_pr_body.md)",
    )

    args = parser.parse_args()

    if args.command == "sample-run":
        cmd_sample_run(args)
    elif args.command == "build-pr-body":
        cmd_build_pr_body(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
