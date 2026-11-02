"""Rebuild one offending physical wire; preserve the complete logical graph.

Run with the pinned AppImage's `openroad -exit -python`.
The original checkpoint is read only. Full LibreLane signoff follows this ECO.
"""
from pathlib import Path
import hashlib,json,odb
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'work/B_postantenna_cold.odb'
dst=ROOT/'work/B_postantenna_eco.odb'
db=odb.dbDatabase.create();odb.read_db(db,str(src))
block=db.getChip().getBlock()
def connectivity_hash():
    graph=[]
    for net in block.getNets():
        pins=sorted((p.getInst().getName(),p.getMTerm().getName()) for p in net.getITerms())
        ports=sorted(p.getName() for p in net.getBTerms())
        graph.append((net.getName(),pins,ports))
    return hashlib.sha256(json.dumps(sorted(graph),separators=(',',':')).encode()).hexdigest()
before=connectivity_hash()
names=['u_pochoco.u_ram._07185_','u_pochoco.u_ram._08839_']
candidates=[block.findNet(n) for n in names]
assert all(n is not None for n in candidates)
net=min(candidates,key=lambda n:len(n.getITerms()))
wire=net.getWire();assert wire is not None
name=net.getName();pin_count=len(net.getITerms())
odb.dbWire.destroy(wire)
assert net.getWire() is None
assert before==connectivity_hash(),'Logical connectivity changed'
odb.write_db(db,str(dst))
cfg=json.loads((ROOT/'asic/configs/B_cold_resume.json').read_text());cfg['DRT_THREADS']=2
(ROOT/'asic/configs/B_eco_resume.json').write_text(json.dumps(cfg,indent=2)+'\n')
state=json.loads((ROOT/'results/environment/B_cold_resume_state.json').read_text())
state['odb']=str(dst)
(ROOT/'results/environment/B_eco_resume_state.json').write_text(json.dumps(state,indent=2)+'\n')
p=ROOT/'results/environment/resume_registry.json';registry=json.loads(p.read_text())
registry['B_v2_p100_u40_eco_resume']='B_v2_p100_u40'
p.write_text(json.dumps(registry,indent=2)+'\n')
record=dict(source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
            output_sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),
            removed_physical_wire_net=name,logical_pin_count=pin_count,
            logical_connectivity_sha256_before=before,
            logical_connectivity_sha256_after=connectivity_hash(),
            operation='Remove only the selected dbWire in a copy, then reconstruct it with DetailedRouting',
            threads=2,required_validation='Full DRC, LVS, antenna and nine-corner STA')
(ROOT/'results/environment/B_routing_eco.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
