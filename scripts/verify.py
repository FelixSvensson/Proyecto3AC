"""Run original and ASIC tests with logged commands, hashes and fail-fast results."""
import subprocess, sys, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def sources(image='sim/generated'):
    return ([str(p.relative_to(ROOT)) for p in (ROOT/'rtl/espino_core').glob('*.v') if p.name!='espino_register_file.v']+
            ['rtl/pochoco_spi_slave.v']+
            [str(p.relative_to(ROOT)) for p in (ROOT/'asic/rtl').glob('*.v')]+[f'{image}/program_rom.v'])


def run(args, logfile):
    result=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    logfile.parent.mkdir(parents=True,exist_ok=True)
    logfile.write_text('$ '+' '.join(args)+'\n'+result.stdout,encoding='utf-8')
    print(result.stdout[-2500:])
    if result.returncode: raise RuntimeError(f'Failed: {args}; see {logfile}')
    return result.stdout


def main():
    for script,args in [('prepare_asic.py',[]),('generate_game.py',[]),('generate_game.py',['--sim'])]:
        subprocess.run([sys.executable,str(ROOT/'scripts'/script)]+args,check=True,cwd=ROOT)
    work=ROOT/'work'; work.mkdir(exist_ok=True)
    logs=ROOT/'results/functional'; logs.mkdir(parents=True,exist_ok=True)
    run([sys.executable,'assembler/test_assembler.py'],logs/'original_assembler.log')
    for s in [0,1]:
        for name in ['asic_memory_tb','asic_game_tb']:
            binary=f'work/{name}_{s}.vvp'
            run(['iverilog','-g2012','-I','sim/generated','-s',name,'-P',f'{name}.Strategy={s}',
                 '-o',binary,f'sim/{name}.v']+sources(),logs/f'{name}_{s}_compile.log')
            output=run(['vvp',binary],logs/f'{name}_{s}.log')
            if 'PASS' not in output: raise RuntimeError('No PASS marker')
            if name=='asic_game_tb':
                (ROOT/'game.vcd').replace(work/f'game_{s}.vcd')
                (ROOT/'stimulus.csv').replace(logs/f'stimulus_{s}.csv')
    a=(logs/'asic_game_tb_0.log').read_text().splitlines()[1:]
    b=(logs/'asic_game_tb_1.log').read_text().splitlines()[1:]
    assert a==b, 'Strategies differ in cycle trace'
    assert (logs/'stimulus_0.csv').read_bytes()==(logs/'stimulus_1.csv').read_bytes()
    (logs/'comparison.json').write_text(json.dumps(dict(strategies_equal=True,
        simulation_clock_ns=100,accelerated=True,gate_simulation=False,
        trace_sha256=hashlib.sha256('\n'.join(a).encode()).hexdigest()),indent=2)+'\n')
    print('PASS: strategies have identical cycle traces; gate simulation remains separate.')


if __name__=='__main__': main()
