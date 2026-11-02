"""Avoid the persistent Metal3 short with a small routing-only obstruction.

Operate on a copy, preserve all logical connections, and require full signoff.
Run with the pinned AppImage's openroad -exit -python.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,odb

ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'work/B_postantenna_cold.odb'
tag='B_v2_p100_u40_detour_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
dst=ROOT/'work'/f'{tag}.odb'
db=odb.dbDatabase.create();odb.read_db(db,str(src))
block=db.getChip().getBlock();scale=block.getDbUnitsPerMicron()
def graph_hash():
    graph=[]
    for net in block.getNets():
        graph.append((net.getName(),sorted((p.getInst().getName(),p.getMTerm().getName()) for p in net.getITerms()),sorted(p.getName() for p in net.getBTerms())))
    return hashlib.sha256(json.dumps(sorted(graph),separators=(',',':')).encode()).hexdigest()
before=graph_hash()
names=['u_pochoco.u_ram._07185_','u_pochoco.u_ram._08839_']
for name in names:
    net=block.findNet(name);assert net and net.getWire()
    odb.dbWire.destroy(net.getWire())
layer=db.getTech().findLayer('Metal3');assert layer
coordinates=[750.82,852.18,751.66,853.02]
obstruction=odb.dbObstruction.create(block,layer,*[round(x*scale) for x in coordinates])
assert obstruction is not None
assert before==graph_hash(),'Logical graph changed'
odb.write_db(db,str(dst))
cfg=json.loads((ROOT/'asic/configs/B_eco_resume.json').read_text())
config=ROOT/'asic/configs/B_detour_resume.json'
config.write_text(json.dumps(cfg,indent=2)+'\n')
state=json.loads((ROOT/'results/environment/B_cold_resume_state.json').read_text());state['odb']=str(dst)
state_path=ROOT/'results/environment'/f'{tag}_state.json'
state_path.write_text(json.dumps(state,indent=2)+'\n')
rp=ROOT/'results/environment/resume_registry.json';registry=json.loads(rp.read_text());registry[tag]='B_v2_p100_u40'
rp.write_text(json.dumps(registry,indent=2)+'\n')
record=dict(run=tag,config=str(config.relative_to(ROOT)),input_state=str(state_path.relative_to(ROOT)),
            a_comparison_run='A_v2_p100_u40',comparison_util_pct=40,
            source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),output_sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),
            removed_physical_wire_nets=names,logical_graph_sha256_before=before,logical_graph_sha256_after=graph_hash(),
            routing_obstruction=dict(layer='Metal3',bbox_um=coordinates),
            cause='Persistent post-antenna Metal3 short at (751.10,852.46)-(751.38,852.74) um',
            operation='Remove two physical dbWire objects in a copy and force a local routing detour; no logical connection or cell placement changed',
            required_validation='DRC Magic, LVS, antenna and nine-corner setup/hold; no closure claimed from this preparation')
(ROOT/'results/environment/B_detour_candidate.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2),flush=True)
