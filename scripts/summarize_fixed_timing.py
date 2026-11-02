"""Summarize adjacent measured pass/fail periods; never infer a bound from slack.

Keep richer characterization records already produced by the search script.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'results/timing'
groups={}
for path in folder.glob('STA_fixed_*.json'):
    sample=json.loads(path.read_text())
    corners=sample['corners']
    passed=len(corners)==9 and all(c[f'{kind}_{metric}']>=0 for c in corners.values() for kind in ['setup','hold'] for metric in ['wns','tns'])
    assert passed==sample['pass_timing'],path
    groups.setdefault(sample['source_run'],[]).append(sample)
for source,samples in groups.items():
    out=folder/f'frequency_{source}.json'
    if out.exists():continue
    passing=[x for x in samples if x['pass_timing']]
    if not passing:continue
    period=min(x['period_ns'] for x in passing)
    if period!=int(period):continue
    failing=next((x for x in samples if x['period_ns']==period-1 and not x['pass_timing']),None)
    if failing is None:continue
    record=dict(source_run=source,status='measured',
                method='Adjacent periods actually verified by nine-corner STA on a fixed layout; absolute IO constraints unchanged',
                resolution_ns=1,minimum_passing_period_ns=period,
                adjacent_failing_period_ns=period-1,frequency_mhz=1000/period,
                sampled_periods_ns=sorted(x['period_ns'] for x in samples))
    out.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record))
