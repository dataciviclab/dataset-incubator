#!/bin/bash
set -euo pipefail
OUTPUT="${2:-input.csv}"
CSV_URL="https://dati-ustat.mur.gov.it/dataset/14aeb712-4665-4311-9e90-3e13639e8f50/resource/9bb0cf6d-1d4e-47f3-8ae9-0c665617b158/download/17_immatricolatixclasse.csv"
UA="Mozilla/5.0 (compatible; DataCivicLab/1.0; +https://dataciviclab.github.io)"
PROXY="${BLOCKED_SOURCE_PROXY:-http://152.70.15.192:8888}"
CURL_ARGS=(-sSL --fail --retry 3 --retry-delay 5 --tlsv1.2 -H "User-Agent: $UA")
[ -n "$PROXY" ] && CURL_ARGS+=(-x "$PROXY")
curl "${CURL_ARGS[@]}" "$CSV_URL" -o "$OUTPUT"
