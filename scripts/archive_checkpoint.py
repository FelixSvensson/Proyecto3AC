"""Package only the input views needed to reproduce a selected resumed run.

No PDK or tool files are included. Run in WSL where state paths resolve.
"""
from pathlib import Path
import argparse,hashlib,json,zipfile

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('run');parser.add_argument('config')
parser.add_argument('--output')
args=parser.parse_args()
run=ROOT/'asic/configs/runs'/args.run
state_path=next(run.glob('*openroad-detailedrouting/state_in.json'))
state=json.loads(state_path.read_text())
files={}
def replace(value):
    if isinstance(value,dict):return {k:replace(v) for k,v in value.items()}
    if isinstance(value,list):return [replace(v) for v in value]
    if isinstance(value,str) and value.startswith(str(ROOT)+'/'):
        path=Path(value)
        assert path.is_file(),path
        if value not in files:
            entry=f'files/{len(files):03d}_{path.name}'
            files[value]=dict(entry=entry,origin=str(path.relative_to(ROOT)),
                              bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        return '__CHECKPOINT__/'+files[value]['entry']
    return value
portable=replace(state)
config=ROOT/args.config;assert config.is_file() and config.resolve().is_relative_to(ROOT)
record=dict(source_run=args.run,from_step='OpenROAD.DetailedRouting',
            config=args.config,config_sha256=hashlib.sha256(config.read_bytes()).hexdigest(),
            state_origin=str(state_path.relative_to(ROOT)),
            pdk='gf180mcuD',pdk_revision='54435919abffb937387ec956209f9cf5fd2dfbee',
            librelane_version='3.0.17',files=list(files.values()),
            scope='Selected restart input only; PDK, tools and other routing snapshots excluded')
out=ROOT/(args.output or f'results/checkpoints/{args.run}.zip')
out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.writestr('manifest.json',json.dumps(record,indent=2)+'\n')
    z.writestr('state_portable.json',json.dumps(portable,indent=2)+'\n')
    for path,info in files.items():z.write(path,info['entry'])
assert out.stat().st_size<100_000_000
print(json.dumps(dict(archive=str(out.relative_to(ROOT)),bytes=out.stat().st_size,
                      sha256=hashlib.sha256(out.read_bytes()).hexdigest(),views=len(files))))
