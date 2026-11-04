#!/usr/bin/env bash
set -euo pipefail
bash scripts/postgres-drill.sh healthy
for pair in 'missing:acknowledgement mismatch' 'stale:stale' 'schema:schema' 'corrupt:checksum'; do
  status=0
  output=$(bash scripts/postgres-drill.sh "${pair%%:*}") || status=$?
  [[ $status == 1 && $output == *"REFUSED ${pair#*:}"* ]] || { echo "$output"; exit 1; }
  echo "PASS ${pair%%:*} refused"
done
