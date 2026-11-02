"""Create recovery configs that persist intermediate DRT databases/reports."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
for label,src,threads in [('B_recovery','B_p100_u40.json',8),('A_u50_recovery','A_p100_u50.json',6)]:
    cfg=json.loads((ROOT/'asic/configs'/src).read_text())
    cfg.update(DRT_THREADS=threads,DRT_SAVE_SNAPSHOTS=True,DRT_SAVE_DRC_REPORT_ITERS=1)
    (ROOT/f'asic/configs/{label}.json').write_text(json.dumps(cfg,indent=2)+'\n')
p=ROOT/'results/environment/resume_registry.json'
registry=json.loads(p.read_text())
registry.update(B_v2_p100_u40_recovery='B_v2_p100_u40',A_p100_u50_v2_recovery='A_p100_u50_v2_20261028T175514Z')
p.write_text(json.dumps(registry,indent=2)+'\n')
