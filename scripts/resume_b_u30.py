"""Resume B30 from its latest preserved routed snapshot, or post-CTS state.

Use a new run directory: preserve the interrupted run and its synthesis evidence.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess

ROOT=Path(__file__).resolve().parents[1]
source='B_p100_u30_v2_20261102T035316Z'
env=ROOT/'results/environment'
tag='B_p100_u30_v2_resume_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
checkpoint=ROOT/'asic/configs/runs'/source/'37-openroad-resizertimingpostcts/state_out.json'
state=json.loads(checkpoint.read_text())
start='OpenROAD.STAMidPNR-2'
previous=json.loads((env/'B_u30_candidate.json').read_text()) if (env/'B_u30_candidate.json').exists() else {}
previous_run=ROOT/'asic/configs/runs'/previous.get('run','__absent__')
snapshots=list(previous_run.rglob('drt_iter*.odb'))
if snapshots:
    # Iteration numbers restart after antenna repair. Use write time, not the
    # largest iteration number, which could belong to an earlier routing pass.
    # Leave the newest file aside in case a pause interrupted its write.
    ordered=sorted(snapshots,key=lambda p:p.stat().st_mtime_ns)
    snapshot=ordered[-2] if len(ordered)>1 else ordered[-1]
    step=next(p for p in snapshot.parents if p.name.endswith('openroad-detailedrouting'))
    state=json.loads((step/'state_in.json').read_text())
    state['odb']=str(snapshot.resolve())
    checkpoint=env/f'{tag}_state.json'
    checkpoint.write_text(json.dumps(state,indent=2)+'\n')
    start='OpenROAD.DetailedRouting'
odb=Path(state['odb'])
assert odb.is_file(),odb
registry_path=env/'resume_registry.json'
registry=json.loads(registry_path.read_text())
registry[tag]=source
registry_path.write_text(json.dumps(registry,indent=2)+'\n')
candidate=dict(run=tag,config='asic/configs/B_p100_u30.json',
               a_comparison_run='A_p100_u30_v2_resume',
               synthesis_source_run=source,input_state=str(checkpoint.relative_to(ROOT)),
               predecessor_run=previous.get('run'),from_step=start,
               input_odb=str(odb.relative_to(ROOT)),
               odb_sha256=hashlib.sha256(odb.read_bytes()).hexdigest(),
               console=f'results/environment/{tag}_console.log',
               purpose='Resume after user pause; unchanged 100 ns/30%, default routing, six threads; router reloads wires and reinitializes optimization')
(env/'B_u30_candidate.json').write_text(json.dumps(candidate,indent=2)+'\n')
(env/f'{tag}_resume.json').write_text(json.dumps(candidate,indent=2)+'\n')
print(json.dumps(candidate,indent=2),flush=True)
with (ROOT/candidate['console']).open('w') as log:
    result=subprocess.run(['bash','scripts/run_flow.sh',candidate['config'],tag,
                           '--from',start,'-i',str(checkpoint)],
                          cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
raise SystemExit(result.returncode)
