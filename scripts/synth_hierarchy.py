"""Mapped hierarchical synthesis, preserving module area attribution and gate probes."""
import sys,subprocess,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from verify import sources,run
strategy=int(sys.argv[1]) if len(sys.argv)>1 else 0
sim='--sim' in sys.argv
image='sim/generated' if sim else 'asic/generated'
tag=f'{"A" if strategy==0 else "B"}_{"sim" if sim else "prod"}_hier'
if '--opt' in sys.argv: tag+='_opt'
out=ROOT/'results/synthesis'/tag;out.mkdir(parents=True,exist_ok=True)
pdk=Path('/opt/proyecto3-tools/pdks/ciel/gf180mcu/versions/54435919abffb937387ec956209f9cf5fd2dfbee/gf180mcuD')
lib=pdk/'libs.ref/gf180mcu_fd_sc_mcu7t5v0/lib/gf180mcu_fd_sc_mcu7t5v0__tt_025C_5v00.lib'
src=sources(image)
if '--opt' in sys.argv: src=[p.replace('asic/rtl/asic_memory.v','asic/variants/asic_memory_registered_addr.v') for p in src]
script=(f'read_verilog -I{image} '+' '.join(src)+'\n'+
        f'chparam -set MemoryStrategy {strategy} asic_top\n'+
        'hierarchy -top asic_top\n'+
        'synth -top asic_top\n'+
        f'dfflibmap -liberty {lib}\nabc -liberty {lib}\nclean\n'+
        f'tee -o {out}/stat.json stat -json -liberty {lib}\n'+
        f'write_verilog -noattr -noexpr {out}/netlist.v\nwrite_json {out}/netlist.json\n')
(out/'synthesis.ys').write_text(script)
run(['yosys','-s',str(out/'synthesis.ys')],out/'synthesis.log')
print(tag)
