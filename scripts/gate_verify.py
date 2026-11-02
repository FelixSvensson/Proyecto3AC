"""Simulate the mapped GF180 standard-cell netlist with the RTL testbench."""
from pathlib import Path
import sys, json, re
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from verify import run
tag=sys.argv[1] if len(sys.argv)>1 else 'A_sim_hier'
out=ROOT/'results/synthesis'/tag
pdk=Path('/opt/proyecto3-tools/pdks/ciel/gf180mcu/versions/54435919abffb937387ec956209f9cf5fd2dfbee/gf180mcuD/libs.ref/gf180mcu_fd_sc_mcu7t5v0/verilog')
binary=f'work/{tag}_gate.vvp'
# Icarus rejects unsupported ifnone edge specify paths even without -gspecify.
# Remove ONLY specify/endspecify blocks for the required zero-delay simulation.
model=(pdk/'gf180mcu_fd_sc_mcu7t5v0.v').read_text()
model=re.sub(r'\bspecify\b.*?\bendspecify\b','',model,flags=re.S)
(ROOT/'work/gf180_functional.v').write_text(model)
run(['iverilog','-g2012','-DGATE','-s','asic_game_tb','-o',binary,'sim/asic_game_tb.v',str(out/'netlist.v'),str(pdk/'primitives.v'),'work/gf180_functional.v'],out/'gate_compile.log')
gate=run(['vvp',binary],out/'gate_sim.log')
(ROOT/'game.vcd').replace(ROOT/f'work/{tag}_gate.vcd')
(ROOT/'stimulus.csv').replace(out/'gate_stimulus.csv')
rtl=(ROOT/'results/functional/asic_game_tb_0.log').read_text()
clean=lambda text:[x for x in text.splitlines() if x.startswith(('STORE','REACTION','CORRECT','WRONG','PASS'))]
assert clean(gate)==clean(rtl),'Gate/RTL cycle trace mismatch'
assert (out/'gate_stimulus.csv').read_bytes()==(ROOT/'results/functional/stimulus_0.csv').read_bytes(), 'Stimuli differ'
(out/'gate_comparison.json').write_text(json.dumps(dict(equal=True,clock_period_ns=100,
    architecture=tag[0],
    accelerated=True,model='GF180MCU mapped standard cells, no SDF',reaction_cycles=136,
    correct_rounds=10,total_cycles=1360),indent=2)+'\n')
print('PASS GATE vs RTL: exact STORE/REACTION/round/reset traces')
