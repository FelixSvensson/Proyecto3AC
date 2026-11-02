#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
/opt/proyecto3-tools/librelane-3.0.17.AppImage python3 scripts/synth_hierarchy.py 0
/opt/proyecto3-tools/librelane-3.0.17.AppImage python3 scripts/synth_hierarchy.py 1
