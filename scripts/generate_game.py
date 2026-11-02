"""Build 10 MHz production image, or an explicitly accelerated simulation image."""
from pathlib import Path
import sys, re, json, hashlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'assembler'))
from assembler import assemble_words, emit_rom


def build(sim=False):
    source = (ROOT / 'sw/game.s').read_text(encoding='utf-8')
    values = [300 if sim else 30000000, 100 if sim else 1000000, 1000 if sim else 10000000]
    for reg, constants in [(6,values[:1]),(12,values[1:])]:
        remaining=iter(constants)
        def replace(match):
            value=next(remaining)
            hi=(value+2048)>>12
            lo=value-(hi<<12)
            return f'lui  x{reg}, 0x{hi:X}\n    addi x{reg}, x{reg}, {lo}'
        pattern=rf'lui\s+x{reg},\s*0x\w+\s*\n\s*addi\s+x{reg},\s*x{reg},\s*-?\d+'
        source,n=re.subn(pattern,replace,source)
        if n != len(constants): raise RuntimeError('Unexpected constant pairs')
    source = '# Generated from sw/game.s; clock=10 MHz; accelerated=' + str(sim) + '\n' + source
    # Correct legacy comments in the generated image only.
    source = source.replace('75000000',str(values[0])).replace('2500000',str(values[1]))
    path = ROOT / ('sim/generated' if sim else 'asic/generated')
    path.mkdir(parents=True,exist_ok=True)
    (path / 'game.s').write_text(source,encoding='utf-8')
    words = assemble_words(source)
    hextext = ''.join(f'{w:08x}\n' for w in words)
    (path / 'game.hex').write_text(hextext,encoding='utf-8')
    emit_rom(words,path)
    manifest = dict(clock_hz=10000000, accelerated=sim, wait_cycles=values[0],
                    tenth_cycles=values[1], average_divisor=values[2], instruction_words=len(words),
                    hex_sha256=hashlib.sha256(hextext.encode()).hexdigest())
    (path / 'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest))


if __name__ == '__main__':
    build('--sim' in sys.argv)
