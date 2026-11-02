"""Curate compact signoff evidence and final views, preserving original run paths."""
from pathlib import Path
import shutil,json,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1]
selection=ROOT/'results/environment/selected_b_run.json'
selected_b=json.loads(selection.read_text())['run'] if selection.exists() else 'B_v2_p100_u40_snapshot_resume'
registry_path=ROOT/'results/environment/resume_registry.json'
registry=json.loads(registry_path.read_text()) if registry_path.exists() else {}
def copy_file(src,dst):
    src,dst=Path(src),Path(dst)
    if dst.exists() and src.stat().st_size==dst.stat().st_size and src.stat().st_mtime_ns==dst.stat().st_mtime_ns:return str(dst)
    return shutil.copy2(src,dst)
for run in (ROOT/'asic/configs/runs').glob('*'):
    if not (run/'final/metrics.json').exists():continue
    out=ROOT/'results/runs'/run.name;out.mkdir(parents=True,exist_ok=True)
    for name in ['resolved.json','flow.log','warning.log','error.log']:
        if (run/name).exists():copy_file(run/name,out/name)
    for step in run.iterdir():
        if step.is_dir() and any(s in step.name for s in ['verilator-lint','openroad-detailedrouting']):
            for f in step.iterdir():
                if f.is_file() and (f.suffix=='.log' or f.name=='state_out.json'):
                    dest=out/'evidence'/f.relative_to(run)
                    dest.parent.mkdir(parents=True,exist_ok=True);copy_file(f,dest)
        if step.is_dir() and any(s in step.name for s in ['stapostpnr','magic-drc','netgen-lvs','reportmanufacturability','checkantennas']):
            for f in step.rglob('*'):
                if f.is_file() and f.suffix in ['.rpt','.log','.json','.xml'] and f.stat().st_size<5_000_000:
                    dest=out/'evidence'/f.relative_to(run)
                    dest.parent.mkdir(parents=True,exist_ok=True);copy_file(f,dest)
    if run.name in ['A_v2_p100_u40',selected_b] or run.name.startswith('final_'):
        for sub in ['gds','lef','def','nl','sdc']:
            src=run/'final'/sub
            if src.exists():shutil.copytree(src,out/'views'/sub,dirs_exist_ok=True,copy_function=copy_file)
    (out/'origin.txt').write_text(str(run.relative_to(ROOT))+'\n')
    if run.name==selected_b and registry.get(run.name):
        precursor=ROOT/'asic/configs/runs'/registry[run.name]
        for step in precursor.glob('*verilator-lint'):
            for f in step.iterdir():
                if f.is_file() and (f.suffix=='.log' or f.name=='state_out.json'):
                    dest=out/'evidence/precursor'/f.relative_to(precursor)
                    dest.parent.mkdir(parents=True,exist_ok=True);copy_file(f,dest)
        for filename in ['resolved.json','flow.log','warning.log','error.log']:
            if (precursor/filename).is_file():
                dest=out/'evidence/precursor'/filename
                dest.parent.mkdir(parents=True,exist_ok=True);copy_file(precursor/filename,dest)
recovery_names={'B_v2_p100_u40','B_v2_p100_u40_recovery','B_v2_p100_u40_snapshot_resume','B_v2_p100_u40_cold_resume','B_v2_p100_u40_eco_resume','B_v2_p100_u40_ordered_resume'}
recovery_names.update(p.name for p in (ROOT/'asic/configs/runs').glob('B_p100_u30_v2*'))
recovery_names.update(p.name for p in (ROOT/'asic/configs/runs').glob('B_v2_p100_u40_detour_*'))
for name in sorted(recovery_names):
    run=ROOT/'asic/configs/runs'/name
    for step in run.glob('*openroad-detailedrouting'):
        out=ROOT/'results/incidents/routing_recovery'/name
        out.mkdir(parents=True,exist_ok=True)
        for filename in ['openroad-detailedrouting.log','config.json','state_in.json']:
            if (step/filename).is_file():copy_file(step/filename,out/filename)
        # Retain the last completed per-iteration DRC report of each routing pass.
        for routing_pass in step.glob('drt-run-*'):
            reports=list(routing_pass.glob('*.rpt'))
            if reports:
                latest=max(reports,key=lambda p:p.stat().st_mtime_ns)
                dest=out/routing_pass.name/latest.name
                dest.parent.mkdir(parents=True,exist_ok=True);copy_file(latest,dest)
out=ROOT/'results/functional/waves';out.mkdir(exist_ok=True)
for f in (ROOT/'work').glob('*.vcd'):
    # Store the compact selected-signal traces; old full-hierarchy debug dump excluded.
    if f.stat().st_size<10_000_000:
        with f.open('rb') as src,gzip.open(out/(f.name+'.gz'),'wb') as dst:shutil.copyfileobj(src,dst)
