"""Audit preserved sources against effective run configurations after execution."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
for run in (ROOT/'asic/configs/runs').iterdir():
    config=run/'resolved.json'
    if not config.exists():continue
    cfg=json.loads(config.read_text())
    paths=[Path(p) for p in cfg.get('VERILOG_FILES',[])]
    for directory in cfg.get('VERILOG_INCLUDE_DIRS',[]):paths+=list(Path(directory).glob('*.vh'))
    files={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
    dest=ROOT/'results/runs'/run.name;dest.mkdir(parents=True,exist_ok=True)
    (dest/'input_hashes_audited.json').write_text(json.dumps(dict(capture='post-run audit of preserved input files',files=files),indent=2)+'\n')
