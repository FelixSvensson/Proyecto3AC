#!/usr/bin/env bash
set -eu
python3 - <<'PY'
from librelane.steps import Yosys,OpenROAD
for v in Yosys.Synthesis.config_vars:
    if any(x in v.name for x in ['SLANG','LIB','SYNTH_HIER']): print(v.name,v.default)
for cls in [OpenROAD.DetailedRouting,OpenROAD.GlobalPlacement]:
    for v in cls.config_vars:
        if any(x in v.name for x in ['THREAD','CORE']): print(v.name,v.default)
PY
find /opt/proyecto3-tools/pdks -path '*mcu7t5v0*' -name '*.v' | head
find /opt/proyecto3-tools/pdks -name '*tt*lib' | head
