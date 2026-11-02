"""Run in the KLayout GUI: klayout -r scripts/layout_capture.py.

Markers are OpenDB cell boxes selected by preserved hierarchical instance names.
No geometry is modified and no illustrative layout is generated.
"""
import pya,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
tag='final_A_v2_p100_u40'
run=ROOT/'asic/configs/runs'/tag
gds=run/'final/gds/asic_top.gds'
if not gds.exists():
    gds=next(p for p in (run/'final').rglob('*.gds') if 'klayout' in str(p).lower())
out=ROOT/'docs/figures';out.mkdir(parents=True,exist_ok=True)
app=pya.Application.instance()
win=app.main_window()
cv=win.load_layout(str(gds),0)
view=win.current_view()
palette=Path('/opt/proyecto3-tools/pdks/ciel/gf180mcu/versions/54435919abffb937387ec956209f9cf5fd2dfbee/gf180mcuD/libs.tech/klayout/tech/gf180mcu.lyp')
view.load_layer_props(str(palette))
layers=view.begin_layers()
while not layers.at_end():
    props=layers.current()
    props.visible=props.source_layer in [34,36,42,46,81]
    props.frame_color=0x526476
    props.fill_color=0x253443
    view.set_layer_properties(layers,props)
    layers.next()
view.set_config('background-color','#121923')
view.set_config('text-visible','false')
view.set_config('grid-visible','false')
view.resize(1600,1400)
view.max_hier()
view.zoom_fit()
view.save_image(str(out/'layout_real.png'),1600,1400)
locations=json.loads((ROOT/f'results/layout/{tag}/cell_locations.json').read_text())
colors={'register_file':0xff3333,'alu':0x00ffff,'cycle_counter':0xffff00}
for group,color in colors.items():
    view.clear_markers()
    cells=[c for c in locations if c['group']==group]
    for cell in cells:
        marker=pya.Marker()
        marker.set(pya.DBox(*cell['box']))
        marker.color=color
        marker.frame_color=color
        marker.line_width=2
        marker.dither_pattern=0
        view.add_marker(marker)
    label=pya.Marker()
    label.set(pya.DText(f'{group}: {len(cells)} instancias trazadas',20,650))
    label.color=color
    view.add_marker(label)
    view.save_image(str(out/f'layout_{group}.png'),1600,1400)
view.save_screenshot(str(out/'klayout_gui.png'))
print('KLayout GUI captures saved',gds)
