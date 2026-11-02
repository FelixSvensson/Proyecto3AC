from pathlib import Path
import subprocess,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'assembler'))
from assembler import assemble_words
get=lambda p:subprocess.check_output(['git','show','HEAD:'+p],cwd=ROOT,text=True)
source=assemble_words(get('sw/game.s'))
hexwords=[int(line,16) for line in get('sw/game.hex').splitlines() if line.strip()]
def constant(words):
    high=words[8]&0xfffff000;low=words[9]>>20
    return high+(low-4096 if low&2048 else low)
result=dict(source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            source_instruction_words=len(source),hex_instruction_words=len(hexwords),
            source_wait_cycles=constant(source),hex_wait_cycles=constant(hexwords),
            differing_word_indices=[i for i,(a,b) in enumerate(zip(source,hexwords)) if a!=b])
(ROOT/'results/environment/original_program_consistency.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
