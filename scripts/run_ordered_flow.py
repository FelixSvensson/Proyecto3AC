"""Run the normal Classic flow with an explicit DRT net-order repair heuristic.

Only this process uses the generated Tcl. Installed LibreLane files and every
checker remain unchanged. Run under the pinned AppImage's python3.
"""
from pathlib import Path
import hashlib,json,sys
from librelane.steps.openroad import DetailedRouting
ROOT=Path(__file__).resolve().parents[1]
original=Path(DetailedRouting.get_script_path(None))
text=original.read_text()
needle='lappend drt_args -or_seed 42'
assert text.count(needle)==1
modified=text.replace(needle,'lappend drt_args -or_seed 43\nlappend drt_args -or_k 1')
generated=ROOT/'work/drt_ordered.tcl';generated.parent.mkdir(exist_ok=True)
generated.write_text(modified)
record=dict(original_script=str(original),original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
            generated_sha256=hashlib.sha256(modified.encode()).hexdigest(),
            changes={'or_seed':43,'or_k':1},
            unchanged='Classic step sequence, all checkers, RTL, PDK, clock, utilization',arguments=sys.argv[1:])
(ROOT/'results/environment/B_ordered_routing.json').write_text(json.dumps(record,indent=2)+'\n')
DetailedRouting.get_script_path=lambda self:str(generated)
from librelane.__main__ import cli
cli.main(args=sys.argv[1:],prog_name='librelane-ordered')
