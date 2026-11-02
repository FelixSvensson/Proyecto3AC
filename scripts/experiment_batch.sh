#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
for setting in "$@"; do
  tag="${setting}_v2_$(date -u +%Y%m%dT%H%M%SZ)"
  python3 scripts/snapshot.py "$tag"
  bash scripts/run_flow.sh "asic/configs/$setting.json" "$tag" > "results/environment/$tag.log" 2>&1
  code=$?
  printf '%s,%s\n' "$tag" "$code" >> results/environment/experiment_exitcodes.csv
  python3 scripts/collect_results.py > results/environment/collection.log
done
