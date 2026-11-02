"""Verify that the deliverable views are byte-identical to the completed runs."""
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parents[1]
records=[]
selection=ROOT/'results/environment/selected_b_run.json'
selected=json.loads(selection.read_text()) if selection.exists() else {}
selected_b=selected.get('run','B_v2_p100_u40_snapshot_resume')
for tag in ['final_A_v2_p100_u40',selected_b]:
    raw=ROOT/'asic/configs/runs'/tag
    if not (raw/'final/metrics.json').exists():
        assert tag!='final_A_v2_p100_u40','Mandatory final run missing'
        continue
    curated=ROOT/'results/runs'/tag
    config=json.loads((raw/'resolved.json').read_text())
    metrics=json.loads((raw/'final/metrics.json').read_text())
    expected_util=40 if tag=='final_A_v2_p100_u40' else selected.get('comparison_util_pct',40)
    assert config['CLOCK_PERIOD']==100 and config['FP_CORE_UTIL']==expected_util
    if tag==selected_b and selected.get('a_comparison_run'):
        comparison=json.loads((ROOT/'asic/configs/runs'/selected['a_comparison_run']/'resolved.json').read_text())
        assert comparison['CLOCK_PERIOD']==config['CLOCK_PERIOD'] and comparison['FP_CORE_UTIL']==expected_util
    assert config['PDK']=='gf180mcuD'
    corners=sorted(k.split('__corner:')[1] for k in metrics if k.startswith('timing__setup__wns__corner:'))
    timing_ok=len(corners)==9 and all(metrics[f'timing__{kind}__{metric}__corner:{c}']==0
        for c in corners for kind in ['setup','hold'] for metric in ['wns','tns'])
    checks={k:metrics.get(k) for k in ['magic__drc_error__count','design__lvs_error__count','antenna__violating__nets']}
    closed=timing_ok and all(v==0 for v in checks.values())
    if tag=='final_A_v2_p100_u40':assert closed,'Mandatory final criteria failed'
    views=[]
    for directory in ['gds','lef','def','nl','sdc']:
        for src in (raw/'final'/directory).glob('*'):
            if not src.is_file():continue
            dst=curated/'views'/directory/src.name
            assert dst.is_file(),f'Missing curated view: {dst}'
            digest=hashlib.sha256(src.read_bytes()).hexdigest()
            assert digest==hashlib.sha256(dst.read_bytes()).hexdigest(),f'Stale view: {dst}'
            views.append(dict(file=str(dst.relative_to(ROOT)),sha256=digest,bytes=dst.stat().st_size))
    assert any(x['file'].endswith('.gds') for x in views),'No deliverable GDS'
    electrical={kind:max((v for k,v in metrics.items() if k.startswith(f'design__max_{kind}_violation__count__corner:')),default=None)
                for kind in ['slew','fanout','cap']}
    records.append(dict(run=tag,closed_explicit_rubric_criteria=closed,corners=corners,
                        checks=checks,electrical_worst_counts=electrical,views=views))
(ROOT/'results/environment/final_artifact_audit.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k!='views'} for r in records],indent=2))
