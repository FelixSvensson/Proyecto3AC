"""Run using openroad -python; emit cell boxes from the final OpenDB database."""
import odb,json,csv,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
tag=sys.argv[-1] if len(sys.argv)>1 else 'A_v2_p100_u40'
run=ROOT/'asic/configs/runs'/tag
files=list((run/'final').rglob('*.odb'))
assert files, 'Final OpenDB missing'
db=odb.dbDatabase.create()
odb.read_db(db,str(files[0]))
block=db.getChip().getBlock()
units=block.getDbUnitsPerMicron()
groups={'register_file':'u_rf.','alu':'u_alu.','cycle_counter':'u_cycle_counter.'}
cells=[]
for inst in block.getInsts():
    name=inst.getName()
    group=next((k for k,s in groups.items() if s in name),None)
    if group:
        b=inst.getBBox()
        cells.append(dict(group=group,instance=name,master=inst.getMaster().getName(),
                          box=[b.xMin()/units,b.yMin()/units,b.xMax()/units,b.yMax()/units]))
assert all(any(c['group']==g for c in cells) for g in groups), 'Missing hierarchy group'
out=ROOT/'results/layout'/tag;out.mkdir(parents=True,exist_ok=True)
(out/'cell_locations.json').write_text(json.dumps(cells,indent=2)+'\n')
pins=[]
for term in block.getBTerms():
    for pin in term.getBPins():
        for box in pin.getBoxes():
            pins.append(dict(name=term.getName(),layer=box.getTechLayer().getName(),
                             box=[box.xMin()/units,box.yMin()/units,box.xMax()/units,box.yMax()/units]))
(out/'pin_locations.json').write_text(json.dumps(pins,indent=2)+'\n')
print({g:sum(c['group']==g for c in cells) for g in groups})
