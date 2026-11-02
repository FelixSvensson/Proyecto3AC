"""Find the smallest passing integer-ns period on an unchanged routed layout.

Each decision executes nine-corner post-route STA; a slack-based estimate only
selects an initial bracket, never substitutes for a measured passing point.
Hold failures are reported instead of being disguised by changing the period.
"""
from pathlib import Path
import json, math, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
source=sys.argv[1]
measured={}

def run(period):
    if period not in measured:
        result=subprocess.run([sys.executable,'scripts/fixed_layout_sta.py',source,str(period)],cwd=ROOT)
        assert result.returncode==0, f'STA execution failed at {period} ns'
        path=ROOT/f'results/timing/STA_fixed_{source}_p{period}.json'
        measured[period]=json.loads(path.read_text())
    return measured[period]

initial=run(100)
hold_ok=all(c['hold_wns']>=0 and c['hold_tns']>=0 for c in initial['corners'].values())
record=dict(source_run=source,method='fixed routed layout; absolute IO delays unchanged; measured integer-ns bisection',resolution_ns=1)
if not hold_ok:
    record.update(status='hold failure at 100 ns; no closed frequency claimed')
else:
    ws=min(c['setup_ws'] for c in initial['corners'].values())
    high=max(2,math.ceil(100-ws)+2)
    while not run(high)['pass_timing']:
        high*=2
        assert high<=10000,'No passing bracket up to 10000 ns'
    low=0
    while high-low>1:
        midpoint=(high+low)//2
        if run(midpoint)['pass_timing']:high=midpoint
        else:low=midpoint
    record.update(status='measured',minimum_passing_period_ns=high,
                  adjacent_failing_period_ns=low if low else None,
                  frequency_mhz=1000/high)
record['sampled_periods_ns']=sorted(measured)
(ROOT/f'results/timing/frequency_{source}.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2),flush=True)
