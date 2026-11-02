"""Restore a curated restart package, checking every file before use."""
from pathlib import Path
import argparse,hashlib,json,shlex,zipfile

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('archive');parser.add_argument('--destination')
args=parser.parse_args()
archive=Path(args.archive).resolve()
with zipfile.ZipFile(archive) as z:
    record=json.loads(z.read('manifest.json'))
    config=ROOT/record['config']
    assert hashlib.sha256(config.read_bytes()).hexdigest()==record['config_sha256'],'Config differs from the measured run'
    dest=(ROOT/(args.destination or f"work/restored_{record['source_run']}")).resolve()
    assert dest.is_relative_to(ROOT/'work'),'Restore destination must stay inside project work/'
    for info in record['files']:
        target=(dest/info['entry']).resolve()
        assert target.is_relative_to(dest),'Invalid archive path'
        data=z.read(info['entry'])
        assert len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256'],info['entry']
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    def replace(value):
        if isinstance(value,dict):return {k:replace(v) for k,v in value.items()}
        if isinstance(value,list):return [replace(v) for v in value]
        if isinstance(value,str) and value.startswith('__CHECKPOINT__/'):
            path=(dest/value.removeprefix('__CHECKPOINT__/')).resolve()
            assert path.is_relative_to(dest) and path.is_file()
            return str(path)
        return value
    state=replace(json.loads(z.read('state_portable.json')))
    output=dest/'state.json';output.write_text(json.dumps(state,indent=2)+'\n')
print('Verified and restored',len(record['files']),'views to',dest)
print('Run from the project directory in WSL, choosing a new tag:')
print(shlex.join(['bash','scripts/run_flow.sh',record['config'],'B_reproduction_NEW_TAG','--from',record['from_step'],'-i',str(output)]))
