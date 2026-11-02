"""Prepare a new LibreLane input from the preserved B routing snapshot.

OpenROAD reloads ROUTED wires from ODB. Router iteration counters and workers
are initialized again; this is not a byte-for-byte continuation of the process.
Original run folders and snapshots are never overwritten.
"""
from pathlib import Path
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
run = ROOT / 'asic/configs/runs/B_v2_p100_u40_recovery'
snapshot = run / '01-openroad-detailedrouting/drt_iter2.odb'
state = json.loads((run / '01-openroad-detailedrouting/state_in.json').read_text())
assert snapshot.is_file()
state['odb'] = str(snapshot.resolve())
out = ROOT / 'results/environment/B_snapshot_resume_state.json'
out.write_text(json.dumps(state, indent=2) + '\n')
registry_path = ROOT / 'results/environment/resume_registry.json'
registry = json.loads(registry_path.read_text())
registry['B_v2_p100_u40_snapshot_resume'] = 'B_v2_p100_u40'
registry_path.write_text(json.dumps(registry, indent=2) + '\n')
record = dict(snapshot=str(snapshot.relative_to(ROOT)),
              sha256=hashlib.sha256(snapshot.read_bytes()).hexdigest(),
              input_state=str(out.relative_to(ROOT)),
              method='Reload routed wires; reinitialize router optimization state',
              openroad_commit='dcf36133a369abc8f3c5e5738cd4d82e4903c0e0',
              source='https://github.com/The-OpenROAD-Project/OpenROAD/blob/dcf36133a369abc8f3c5e5738cd4d82e4903c0e0/src/drt/src/io/io.cpp')
(ROOT / 'results/environment/B_snapshot_resume.json').write_text(json.dumps(record, indent=2)+'\n')
print(out)
