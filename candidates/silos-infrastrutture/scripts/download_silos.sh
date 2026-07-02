#!/bin/bash
# Download rapporto SILOS (Camera dei Deputati) attraverso il proxy VM.
# Necessario perché l'IP di GitHub Actions è bloccato da dati.camera.it.
# Il proxy VM (BLOCKED_SOURCE_PROXY) fa da tramite.
set -euo pipefail

OUTPUT="${1:-PISRapportoCSV2024.zip}"
ZIP_URL="https://dati.camera.it/ocd/dump/silos/PISRapportoCSV2024.zip"
UA="Mozilla/5.0 (compatible; DataCivicLab/1.0; +https://dataciviclab.github.io)"
PROXY="${BLOCKED_SOURCE_PROXY:-}"

CURL_ARGS=(-sSL --fail --retry 3 --retry-delay 5 -H "User-Agent: $UA")

if [ -n "$PROXY" ]; then
    CURL_ARGS+=(-x "$PROXY")
fi

curl "${CURL_ARGS[@]}" "$ZIP_URL" -o "$OUTPUT"
echo "Scaricato: $OUTPUT ($(wc -c < "$OUTPUT") bytes)" >&2
