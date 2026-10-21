#!/usr/bin/env python3
"""Harvest call aperte/in arrivo dal SEDIA Search API (EU Funding & Tenders Portal).

Usage:
    python scripts/extract_sedia.py --output eu_call_open.csv [--statuses open,forthcoming]

Endpoint pubblico (apiKey=SEDIA è letterale del frontend EC, non un secret).
Multipart obbligatorio: query (bool JSON) + languages + sort.
Solo stdlib. Documentazione e rischi: notes.md.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.request
import uuid
from pathlib import Path

BASE = "https://api.tech.ec.europa.eu/search-api/prod/rest"
API_KEY = "SEDIA"

STATUS_FORTHCOMING = "31094501"
STATUS_OPEN = "31094502"
STATUS_CLOSED = "31094503"
TYPE_TOPIC = "1"
PERIOD_2127 = "2021 - 2027"

STATUS_MAP = {
    "open": STATUS_OPEN,
    "forthcoming": STATUS_FORTHCOMING,
    "closed": STATUS_CLOSED,
}

FRAMEWORK_LABELS = {
    "43108390": "Horizon Europe",
    "31045243": "Horizon 2020",
    "43152860": "Digital Europe",
    "44181033": "European Defence Fund",
    "43251814": "Creative Europe",
    "43298916": "Euratom",
    "43254019": "ESF",
    "43252405": "LIFE",
    "43251589": "CERV",
    "43251567": "CEF",
    "43252476": "Single Market Programme",
    "43252386": "Justice",
    "43252368": "Internal Security Fund",
    "43353764": "Erasmus+",
    "43332642": "EU4Health",
    "43252449": "RFCS",
    "43392145": "EMFAF",
    "44416173": "I3",
    "44773066": "Just Transition Mechanism",
    "45532249": "EU Bodies and Agencies",
    "43251447": "AMIF",
    "43252517": "SOCPL",
    "43298203": "UCPM",
    "43254037": "European Solidarity Corps",
    "43089234": "Innovation Fund",
    "43637601": "PPPA",
    "43697167": "European Parliament",
    "45876777": "NDICI Global Europe",
    "43253967": "Renewable Energy Financing Mechanism",
    "43252433": "PERICLES IV",
}

CSV_COLUMNS = [
    "identifier",
    "call_identifier",
    "call_title",
    "title",
    "status",
    "status_label",
    "framework_programme",
    "framework_label",
    "programme_period",
    "types_of_action",
    "start_date",
    "deadline_date",
    "deadline_model",
    "budget_total_eur",
    "expected_grants",
    "url",
]


def sedia_search(
    query: dict,
    *,
    page: int = 1,
    page_size: int = 100,
    languages: list[str] | None = None,
    sort: dict | None = None,
    timeout: int = 90,
) -> dict:
    languages = languages or ["en"]
    sort = sort or {"field": "sortStatus", "order": "ASC"}
    url = (
        f"{BASE}/search?apiKey={API_KEY}&text=*"
        f"&pageNumber={page}&pageSize={page_size}"
        f"&isFirstCall={str(page == 1).lower()}"
    )
    boundary = "----sedia" + uuid.uuid4().hex
    parts: list[bytes] = []
    for name, obj in (("query", query), ("languages", languages), ("sort", sort)):
        payload = json.dumps(obj)
        parts.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{name}"\r\n'
                f"Content-Type: application/json\r\n\r\n"
                f"{payload}\r\n"
            ).encode()
        )
    parts.append(f"--{boundary}--\r\n".encode())
    req = urllib.request.Request(
        url,
        data=b"".join(parts),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def build_query(status_codes: list[str], period: str = PERIOD_2127) -> dict:
    return {
        "bool": {
            "must": [
                {"terms": {"type": [TYPE_TOPIC]}},
                {"terms": {"status": status_codes}},
                {"term": {"programmePeriod": period}},
            ]
        }
    }


def parse_budget_overview(raw) -> tuple[float | None, int | None]:
    if not isinstance(raw, str) or not raw.strip():
        return None, None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None, None
    action_map = data.get("budgetTopicActionMap") or {}
    total = 0.0
    grants = 0
    found_amount = False
    for actions in action_map.values():
        items = actions if isinstance(actions, list) else [actions]
        for action in items:
            if not isinstance(action, dict):
                continue
            year_map = action.get("budgetYearMap") or {}
            for value in year_map.values():
                try:
                    total += float(value)
                    found_amount = True
                except (TypeError, ValueError):
                    pass
            eg = action.get("expectedGrants")
            if isinstance(eg, (int, float)):
                grants += int(eg)
    return (total if found_amount else None), (grants if grants else None)


def first(metadata: dict, key: str):
    value = metadata.get(key)
    if isinstance(value, list) and value:
        return value[0]
    return None


def date_only(value) -> str:
    if not value or not isinstance(value, str):
        return ""
    return value[:10]


def normalize_item(item: dict) -> dict:
    md = item.get("metadata") or {}
    budget_total, expected_grants = parse_budget_overview(first(md, "budgetOverview"))
    framework = first(md, "frameworkProgramme")
    status = first(md, "status")
    types_of_action = md.get("typesOfAction")
    if isinstance(types_of_action, list):
        types_of_action = "; ".join(str(x) for x in types_of_action)
    return {
        "identifier": first(md, "identifier") or "",
        "call_identifier": first(md, "callIdentifier") or "",
        "call_title": first(md, "callTitle") or "",
        "title": item.get("summary") or first(md, "title") or "",
        "status": status or "",
        "status_label": "",  # filled after normalize via status_label()
        "framework_programme": framework or "",
        "framework_label": FRAMEWORK_LABELS.get(str(framework), ""),
        "programme_period": first(md, "programmePeriod") or "",
        "types_of_action": types_of_action or "",
        "start_date": date_only(first(md, "startDate")),
        "deadline_date": date_only(first(md, "deadlineDate")),
        "deadline_model": first(md, "deadlineModel") or "",
        "budget_total_eur": "" if budget_total is None else f"{budget_total:.2f}",
        "expected_grants": "" if expected_grants is None else str(expected_grants),
        "url": first(md, "esST_URL") or item.get("url") or "",
    }


def status_label(code: str) -> str:
    for label, value in STATUS_MAP.items():
        if value == code:
            return label
    return code


def fetch_all(status_codes: list[str], *, max_pages: int = 30) -> list[dict]:
    query = build_query(status_codes)
    rows: list[dict] = []
    seen: set[str] = set()
    page = 1
    while page <= max_pages:
        data = sedia_search(query, page=page, page_size=100)
        results = data.get("results") or []
        if not results:
            break
        for item in results:
            row = normalize_item(item)
            row["status_label"] = status_label(row["status"])
            ident = row["identifier"]
            if ident and ident in seen:
                continue
            if ident:
                seen.add(ident)
            rows.append(row)
        total = int(data.get("totalResults") or 0)
        if len(seen) >= total:
            break
        page += 1
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Harvest EU open/forthcoming calls from SEDIA")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument(
        "--statuses",
        default="open,forthcoming",
        help="Comma-separated: open,forthcoming,closed (default: open,forthcoming)",
    )
    args = parser.parse_args()

    codes = []
    for part in args.statuses.split(","):
        key = part.strip().lower()
        if not key:
            continue
        if key not in STATUS_MAP:
            print(f"Unknown status: {key}", file=sys.stderr)
            return 2
        codes.append(STATUS_MAP[key])
    if not codes:
        print("No statuses given", file=sys.stderr)
        return 2

    print(f"Fetching SEDIA topics status={args.statuses} ...", file=sys.stderr)
    rows = fetch_all(codes)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    write_csv(out, rows)
    print(f"  {len(rows)} unique topics -> {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
