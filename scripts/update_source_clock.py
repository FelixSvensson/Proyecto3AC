"""One-time production source migration; preserves the exact delivered source."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
original=ROOT/'sw/game_fpga_original.s'
if not original.exists():original.write_bytes((ROOT/'sw/game.s').read_bytes())
generated=(ROOT/'asic/generated/game.s').read_text()
assert generated.startswith('# Generated from')
(ROOT/'sw/game.s').write_text(generated.split('\n',1)[1],encoding='utf-8')
(ROOT/'sw/game.hex').write_bytes((ROOT/'asic/generated/game.hex').read_bytes())
