"""Freeze a post-antenna routing checkpoint for a fresh OpenROAD process."""
from pathlib import Path
import json,hashlib,re,shutil
ROOT=Path(__file__).resolve().parents[1]
run=ROOT/'asic/configs/runs/B_v2_p100_u40_snapshot_resume'
step=run/'01-openroad-detailedrouting'
reports=sorted((step/'drt-run-1').glob('*.rpt'),key=lambda p:int(re.search(r'drc-(\d+)',p.name).group(1)))
assert len(reports)>=2
# Use the preceding completed checkpoint, not a file currently being written.
index=int(re.search(r'drc-(\d+)',reports[-2].name).group(1))
snapshot=step/f'drt_iter{index}.odb'
if not snapshot.exists():snapshot=step/'drt-run-1'/snapshot.name
assert snapshot.is_file()
copy=ROOT/'work/B_postantenna_cold.odb'
shutil.copy2(snapshot,copy)
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(snapshot)==digest(copy)
state=json.loads((step/'state_in.json').read_text());state['odb']=str(copy)
(ROOT/'results/environment/B_cold_resume_state.json').write_text(json.dumps(state,indent=2)+'\n')
cfg=json.loads((ROOT/'asic/configs/B_recovery.json').read_text());cfg['DRT_THREADS']=4
(ROOT/'asic/configs/B_cold_resume.json').write_text(json.dumps(cfg,indent=2)+'\n')
p=ROOT/'results/environment/resume_registry.json';registry=json.loads(p.read_text())
registry['B_v2_p100_u40_cold_resume']='B_v2_p100_u40'
p.write_text(json.dumps(registry,indent=2)+'\n')
record=dict(source_snapshot=str(snapshot.relative_to(ROOT)),sha256=digest(copy),
            source_report=str(reports[-2].relative_to(ROOT)),
            restart='Fresh process after post-route antenna insertion; ROUTED wires retained; optimization state reset',
            threads=4,unchanged=['RTL','program','PDK','clock period 100 ns','core utilization 40 percent'])
(ROOT/'results/environment/B_cold_resume.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
