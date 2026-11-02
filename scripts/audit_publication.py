"""Audit the Git-visible delivery without staging, committing or publishing it."""
from pathlib import Path
import hashlib, json, re, subprocess

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'results/environment/publication_audit.json'
paths = subprocess.check_output(
    ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT
).decode().split('\0')
patterns = [
    re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(rb'gh[pousr]_[A-Za-z0-9]{36,}'),
    re.compile(rb'github_pat_[A-Za-z0-9_]{60,}'),
    re.compile(rb'AKIA[0-9A-Z]{16}'),
]
files, findings = [], []
for name in sorted(set(paths)):
    p = ROOT / name
    if not name or not p.is_file() or p == out:
        continue
    data = p.read_bytes()
    assert len(data) < 100_000_000, f'File too large: {name}'
    assert not name.startswith(('asic/configs/runs/', 'work/')), name
    if p.suffix.lower() in {'.py','.sh','.v','.vh','.s','.md','.json','.txt','.log','.tcl','.yml','.yaml','.csv'}:
        if any(pattern.search(data) for pattern in patterns):
            findings.append(name)
    files.append(dict(path=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
record = dict(scope='Git-visible tracked and untracked files; no staging or publication',
              secret_check='Common private-key, GitHub token and AWS access-key formats; not an exhaustive guarantee',
              possible_secret_files=findings, file_count=len(files), total_bytes=sum(f['bytes'] for f in files),
              files=files)
out.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='files'},indent=2))
assert not findings, 'Review flagged file paths locally; secret values were not printed'
