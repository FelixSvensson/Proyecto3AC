from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from verify import sources


def main():
    for strategy in [0,1]:
        for period,util in [(100,40),(80,40),(60,40),(50,40),(100,30),(100,50)]:
            config=dict(DESIGN_NAME='asic_top',PDK='gf180mcuD',
                        VERILOG_FILES=['dir::../../'+p for p in sources('asic/generated')],
                        VERILOG_INCLUDE_DIRS=['dir::../../asic/generated'],
                        CLOCK_PORT='i_Clk',CLOCK_PERIOD=period,FP_CORE_UTIL=util,
                        SYNTH_PARAMETERS=[f'MemoryStrategy={strategy}'],
                        SYNTH_HIERARCHY_MODE='deferred_flatten',
                        DRT_THREADS=6,
                        ERROR_ON_LINTER_WARNINGS=False)
            if strategy==1 and period==100 and util==30:
                config.update(DRT_SAVE_SNAPSHOTS=True,DRT_SAVE_DRC_REPORT_ITERS=1)
            path=ROOT/f'asic/configs/{"A" if strategy==0 else "B"}_p{period}_u{util}.json'
            path.write_text(json.dumps(config,indent=2)+'\n')
            if strategy==0 and period==100 and util==40:
                final=dict(config)
                final['FP_PIN_ORDER_CFG']='dir::../constraints/pins.cfg'
                (ROOT/'asic/configs/final.json').write_text(json.dumps(final,indent=2)+'\n')
                optimized=dict(config)
                optimized['VERILOG_FILES']=[p.replace('asic/rtl/asic_memory.v','asic/variants/asic_memory_registered_addr.v') for p in config['VERILOG_FILES']]
                (ROOT/'asic/configs/A_opt_p100_u40.json').write_text(json.dumps(optimized,indent=2)+'\n')


if __name__=='__main__': main()
