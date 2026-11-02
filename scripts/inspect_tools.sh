#!/usr/bin/env bash
set -eu
python3 - <<'PY'
import inspect
from librelane.steps import Yosys
for v in Yosys.Synthesis.config_vars:
    if any(s in v.name for s in ['HIER','PARAM','FLAT','CLOCK']): print(v.name,v.default,v.description)
PY
find /opt/proyecto3-tools/pdks -path '*/librelane/config.tcl' | head
