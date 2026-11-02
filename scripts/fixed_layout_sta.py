"""STA refinement on an unchanged routed layout and unchanged absolute IO delays.

This is separate from fresh synthesis/PnR target sweeps, explicitly labelled.
"""
from pathlib import Path
import json,re,subprocess,sys
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
source=sys.argv[1]
periods=[float(p) for p in sys.argv[2:]]
run=ROOT/'asic/configs/runs'/source
state=next(run.glob('*stapostpnr/state_out.json'))
sdcfile=run/'final/sdc/asic_top.sdc'
if not sdcfile.exists():sdcfile=Path(json.loads(state.read_text())['sdc'])
sdc=sdcfile.read_text()
base=json.loads((ROOT/('asic/configs/final.json' if source.startswith('final_') else 'asic/configs/A_p100_u40.json')).read_text())
if source.startswith('B_'):base=json.loads((ROOT/'asic/configs/B_p100_u40.json').read_text())
layout_config=json.loads((run/'resolved.json').read_text())
base['FP_CORE_UTIL']=layout_config['FP_CORE_UTIL']
out=ROOT/'results/timing';out.mkdir(exist_ok=True)
records=[]
for period in periods:
    label=f'{period:g}'
    sdcfile=ROOT/f'asic/constraints/{source}_fixed_p{label}.sdc'
    modified,n=re.subn(r'(create_clock -name i_Clk -period )\S+',rf'\g<1>{period:.4f}',sdc)
    assert n==1
    sdcfile.write_text(modified)
    cfg=dict(base,CLOCK_PERIOD=period,SIGNOFF_SDC_FILE=f'dir::../constraints/{sdcfile.name}')
    cfgpath=ROOT/f'asic/configs/STA_{source}_p{label}.json'
    cfgpath.write_text(json.dumps(cfg,indent=2)+'\n')
    canonical=f'STA_fixed_{source}_p{label}'
    tag=canonical+'_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    args=['bash','scripts/run_flow.sh',str(cfgpath.relative_to(ROOT)),tag,'--only','OpenROAD.STAPostPNR','-i',str(state)]
    result=subprocess.run(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (out/f'{canonical}.log').write_text(result.stdout)
    produced=ROOT/'asic/configs/runs'/tag
    final=produced/'final/metrics.json'
    assert result.returncode==0 and final.exists(),f'STA failed: {tag}'
    m=json.loads(final.read_text())
    corners=sorted(k.split('__corner:')[1] for k in m if k.startswith('timing__setup__wns__corner:'))
    data={c:{f'{kind}_{metric}':m[f'timing__{kind}__{metric}__corner:{c}'] for kind in ['setup','hold'] for metric in ['wns','tns','ws']} for c in corners}
    record=dict(source_run=source,sta_run=tag,period_ns=period,mode='fixed routed layout; absolute IO constraints unchanged',
                pass_timing=len(corners)==9 and all(x[f'{kind}_{metric}']>=0 for x in data.values() for kind in ['setup','hold'] for metric in ['wns','tns']),corners=data)
    records.append(record)
    (out/f'{canonical}.json').write_text(json.dumps(record,indent=2)+'\n')
    print(tag,record['pass_timing'],min(x['setup_ws'] for x in data.values()),flush=True)
