#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
config=${1:-asic/configs/A_p100_u40.json}
tag=${2:-$(basename "$config" .json)_$(date -u +%Y%m%dT%H%M%SZ)}
shift $(( $# > 1 ? 2 : $# ))
export PDK_ROOT=${PDK_ROOT:-/opt/proyecto3-tools/pdks}
exec /opt/proyecto3-tools/librelane-3.0.17.AppImage librelane --pdk gf180mcuD --pdk-root "$PDK_ROOT" --run-tag "$tag" --condensed -j 6 "$config" "$@"
