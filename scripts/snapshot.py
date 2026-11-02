"""Archive exactly the sources and generated image used by a run."""
from pathlib import Path
import json,hashlib,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from verify import sources
tag=sys.argv[1]
image=sys.argv[2] if len(sys.argv)>2 else 'asic/generated'
files=sources(image)+[f'{image}/program_meta.vh',f'{image}/program_reset.vh',f'{image}/game.s',f'{image}/game.hex']
out=ROOT/'results/snapshots';out.mkdir(parents=True,exist_ok=True)
data={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}
(out/f'{tag}.json').write_text(json.dumps(data,indent=2)+'\n')
with zipfile.ZipFile(out/f'{tag}.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(ROOT/p,p)
