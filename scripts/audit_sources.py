"""Record code/ROM hashes against the pre-run source snapshot and publication sizes."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
prior=json.loads((ROOT/'results/snapshots/v2_hierarchical.json').read_text())
comparison={p:dict(expected=h,current=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p,h in prior.items()}
different=[p for p,x in comparison.items() if x['expected']!=x['current']]
# Sources used for hardware (including the byte-identical ROM) must remain unchanged.
hardware_differences=[p for p in different if p.endswith(('.v','.vh','.hex'))]
assert not hardware_differences,hardware_differences
listed=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).split(b'\0')
files=[ROOT/p.decode() for p in listed if p]
large=[dict(file=str(p.relative_to(ROOT)),bytes=p.stat().st_size) for p in files if p.is_file() and p.stat().st_size>10_000_000]
assert not any(x['bytes']>=100_000_000 for x in large),'File exceeds GitHub regular-file limit'
result=dict(hardware_hashes_match_pre_run_snapshot=True,nonhardware_differences=different,
            publication_file_count=len(files),publication_bytes=sum(p.stat().st_size for p in files if p.is_file()),files_over_10MB=large)
(ROOT/'results/environment/source_and_size_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
