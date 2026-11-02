from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from verify import sources,run
out=ROOT/'results/optimization';out.mkdir(parents=True,exist_ok=True)
src=[p if p!='asic/rtl/asic_memory.v' else 'asic/variants/asic_memory_registered_addr.v' for p in sources()]
for name in ['asic_memory_tb','asic_game_tb']:
    binary=f'work/{name}_opt.vvp'
    run(['iverilog','-g2012','-I','sim/generated','-s',name,'-o',binary,f'sim/{name}.v']+src,out/f'{name}_compile.log')
    output=run(['vvp',binary],out/f'{name}.log')
    if name=='asic_game_tb':
        (ROOT/'game.vcd').replace(ROOT/'work/game_opt.vcd')
        (ROOT/'stimulus.csv').replace(out/'stimulus.csv')
        clean=lambda text:[x for x in text.splitlines() if x.startswith(('STORE','REACTION','CORRECT','WRONG','PASS'))]
        ref=(ROOT/'results/functional/asic_game_tb_0.log').read_text()
        assert clean(output)==clean(ref)
        assert (out/'stimulus.csv').read_bytes()==(ROOT/'results/functional/stimulus_0.csv').read_bytes()
(out/'functional_comparison.json').write_text(json.dumps(dict(equal=True,method='Identical game traces and stimuli; memory reset/byte-enable tests passed'),indent=2)+'\n')
variant=(ROOT/'asic/variants/asic_memory_registered_addr.v').read_text().replace('module asic_memory #','module asic_memory_opt #')
(ROOT/'work/asic_memory_opt.v').write_text(variant)
run(['iverilog','-g2012','-I','sim/generated','-s','memory_equivalence_tb','-o','work/mem_eq.vvp',
     'sim/memory_equivalence_tb.v','asic/rtl/asic_memory.v','work/asic_memory_opt.v','sim/generated/program_rom.v'],out/'equivalence_compile.log')
run(['vvp','work/mem_eq.vvp'],out/'memory_equivalence.log')
