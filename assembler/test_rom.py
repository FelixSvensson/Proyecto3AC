import sys, tempfile, unittest, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from assembler import assemble_words,emit_rom


class RomTests(unittest.TestCase):
    def test_all_generated_words_and_determinism(self):
        root=Path(__file__).resolve().parents[1]
        words=assemble_words((root/'asic/generated/game.s').read_text())
        self.assertEqual(len(words),107)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            emit_rom(words,path)
            before={p.name:p.read_bytes() for p in path.iterdir()}
            emit_rom(words,path)
            self.assertEqual(before,{p.name:p.read_bytes() for p in path.iterdir()})
            encoded=re.findall(r"data_o = 32'h([0-9a-f]{8});",(path/'program_rom.v').read_text())
            self.assertEqual([int(x,16) for x in encoded[:-1]],words)
    def test_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            for words in [[],[0]*257]:
                with self.assertRaises(ValueError): emit_rom(words,tmp)
    def test_constants(self):
        root=Path(__file__).resolve().parents[1]
        words=assemble_words((root/'asic/generated/game.s').read_text())
        pairs=[]
        for a,b in zip(words,words[1:]):
            if a&127==0x37 and b&0x707f==0x13 and (a>>7)&31==(b>>7)&31==(b>>15)&31:
                low=b>>20
                if low&2048: low-=4096
                pairs.append(((a&0xfffff000)+low)&0xffffffff)
        self.assertIn(30000000,pairs)
        self.assertIn(1000000,pairs)
        self.assertIn(10000000,pairs)


if __name__=='__main__': unittest.main(verbosity=2)
