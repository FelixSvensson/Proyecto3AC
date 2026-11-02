"""Native KLayout views of a real transient Metal2 short and the final region."""
import pya,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rawdir=ROOT/'asic/configs/runs/DEBUG_first_route/01-openroad-detailedrouting'
text=(rawdir/'asic_top.drc').read_text()
pattern=r'violation type: ([^\n]+)\n\s*srcs: ([^\n]+)\n\s*bbox = \(([\d.]+), ([\d.]+)\) - \(([\d.]+), ([\d.]+)\) on Layer ([^\n]+)'
records=re.findall(pattern,text)
chosen=next(x for x in records if 'u_rf' in x[1] and x[-1]=='Metal2')
box=[float(x) for x in chosen[2:6]]
out=ROOT/'results/incidents/drc_case';out.mkdir(parents=True,exist_ok=True)
for name in ['asic_top.drc','asic_top.drc.xml','config.json','openroad-detailedrouting.log']:
    shutil.copy2(rawdir/name,out/name)
m=json.loads((ROOT/'asic/configs/runs/DEBUG_first_route/final/metrics.json').read_text())
final=json.loads((ROOT/'asic/configs/runs/final_A_v2_p100_u40/final/metrics.json').read_text())
info=dict(type=chosen[0],sources=chosen[1],layer=chosen[-1],bbox_um=box,
          debug_purpose='Transient route retained with DRT_OPT_ITERS=0; not a signoff candidate',
          debug_drc=m['route__drc_errors'],final_drc=final['magic__drc_error__count'],
          correction='Allow the complete routing optimization; final_A_v2_p100_u40 has zero router and Magic DRC',
          final_iterations={k:v for k,v in final.items() if k.startswith('route__drc_errors__iter:')})
route_log=next((ROOT/'asic/configs/runs/final_A_v2_p100_u40').glob('*openroad-detailedrouting/openroad-detailedrouting.log'))
info['all_router_pass_violation_counts']=[int(x) for x in re.findall(r'Number of violations\s*=\s*(\d+)',route_log.read_text())]
info['iteration_metric_note']='Iteration keys restart and are overwritten on post-DRT antenna rerouting; use the full log for the first pass.'
(out/'case.json').write_text(json.dumps(info,indent=2)+'\n')
gds_before=ROOT/'asic/configs/runs/DEBUG_case_gds/final/gds/asic_top.gds'
if not gds_before.exists():gds_before=next((ROOT/'asic/configs/runs/DEBUG_case_gds').glob('*klayout-streamout/*.gds'))
win=pya.Application.instance().main_window()
for mode,gds in [('before',gds_before),('after',ROOT/'asic/configs/runs/final_A_v2_p100_u40/final/gds/asic_top.gds')]:
    win.load_layout(str(gds),0)
    view=win.current_view();view.max_hier()
    view.set_config('background-color','#121923');view.set_config('text-visible','false');view.set_config('grid-visible','false')
    layers=view.begin_layers()
    while not layers.at_end():
        lp=layers.current();lp.visible=lp.source_layer in [34,35,36]
        lp.frame_color=0x44bbff if lp.source_layer==36 else 0x586773
        lp.fill_color=lp.frame_color
        view.set_layer_properties(layers,lp);layers.next()
    marker=pya.Marker();marker.set(pya.DBox(*box));marker.frame_color=0xff3333;marker.color=0xff3333;marker.dither_pattern=1;marker.line_width=3;view.add_marker(marker)
    target=pya.DBox(box[0]-2,box[1]-2,box[2]+2,box[3]+2)
    view.zoom_box(target)
    view.save_image(str(ROOT/f'docs/figures/drc_{mode}.png'),1200,1000)
print(json.dumps(info,indent=2))
