"""Collect final metrics without replacing missing/failed checks by zero."""
from pathlib import Path
import json,csv,shutil,re
ROOT=Path(__file__).resolve().parents[1]
rows=[]
registry_path=ROOT/'results/environment/resume_registry.json'
registry=json.loads(registry_path.read_text()) if registry_path.exists() else {}
for run in sorted((ROOT/'asic/configs/runs').glob('*')):
    if run.name.startswith(('STA_fixed_','DEBUG_')): continue
    final=run/'final/metrics.json'
    if not final.exists(): continue
    m=json.loads(final.read_text())
    config=json.loads((run/'resolved.json').read_text()) if (run/'resolved.json').exists() else {}
    out=ROOT/'results/runs'/run.name;out.mkdir(parents=True,exist_ok=True)
    shutil.copy2(final,out/'metrics.json')
    if config:(out/'effective_config.json').write_text(json.dumps(config,indent=2)+'\n')
    sm={}
    synthesis_run=ROOT/'asic/configs/runs'/registry.get(run.name,run.name)
    for step in synthesis_run.glob('*yosys-synthesis'):
        sm=json.loads((step/'state_out.json').read_text())['metrics']
        (out/'synthesis_metrics.json').write_text(json.dumps(sm,indent=2)+'\n')
        shutil.copy2(step/'yosys-synthesis.log',out/'synthesis.log')
    routed_metrics={}
    # For resumed signoff, the routed predecessor remains in the source run.
    for candidate in [synthesis_run,run]:
        for step in candidate.glob('*openroad-detailedrouting'):
            if (step/'state_out.json').exists():routed_metrics=json.loads((step/'state_out.json').read_text())['metrics']
    checks=['magic__drc_error__count','design__lvs_error__count','antenna__violating__nets']
    corners=sorted(k.split('__corner:')[1] for k in m if k.startswith('timing__setup__wns__corner:'))
    timing=[m.get(f'timing__{kind}__{metric}__corner:{corner}') for corner in corners for kind in ['setup','hold'] for metric in ['wns','tns']]
    closed=bool(corners) and len(corners)==9 and all(v is not None and v>=0 for v in timing) and all(m.get(k) == 0 for k in checks)
    row=dict(run=run.name,period_ns=config.get('CLOCK_PERIOD'),util_pct=config.get('FP_CORE_UTIL'),
             synth_area_um2=sm.get('design__instance__area'),die_area_um2=m.get('design__die__area'),
             drc=m.get(checks[0]),lvs=m.get(checks[1]),antenna=m.get(checks[2]),corners=len(corners),closed=closed,
             worst_setup_slack_ns=min((m[f'timing__setup__ws__corner:{c}'] for c in corners),default=None),
             worst_hold_slack_ns=min((m[f'timing__hold__ws__corner:{c}'] for c in corners),default=None),
             route_initial_drc=None,
             route_iteration0_metric=m.get('route__drc_errors__iter:0'))
    # The metric's iteration index restarts during post-DRT antenna repair.
    # Read the first actual routing result from the full log instead.
    for candidate in [run,synthesis_run]:
        logs=list(candidate.glob('*openroad-detailedrouting/openroad-detailedrouting.log'))
        if logs:
            counts=re.findall(r'Number of violations\s*=\s*(\d+)',logs[0].read_text())
            if counts:
                row['route_initial_drc']=int(counts[0]);break
    row['routed_area_before_fill_um2']=routed_metrics.get('design__instance__area')
    util=routed_metrics.get('design__instance__utilization__stdcell')
    row['routed_util_before_fill_pct']=100*util if util is not None else None
    row['cost_usd']=row['die_area_um2']/1e6*23000 if row['die_area_um2'] is not None else None
    rows.append(row)
    with (out/'corners.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['corner','setup_wns_ns','setup_tns_ns','hold_wns_ns','hold_tns_ns','setup_slack_ns','hold_slack_ns'])
        for c in corners:writer.writerow([c]+[m.get(f'timing__{k}__{v}__corner:{c}') for k,v in [('setup','wns'),('setup','tns'),('hold','wns'),('hold','tns'),('setup','ws'),('hold','ws')]])
out=ROOT/'results';out.mkdir(exist_ok=True)
(out/'summary.json').write_text(json.dumps(rows,indent=2)+'\n')
if rows:
    with (out/'summary.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print(json.dumps(rows,indent=2))
