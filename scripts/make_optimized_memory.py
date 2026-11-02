"""Retiming the split data ROM mux across its synchronous output boundary.

The sampled address/selection and RAM read data produce the same edge response.
Only Strategy A changes; Strategy B is byte-for-byte the original branch.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/'asic/rtl/asic_memory.v').read_text()
text=text.replace('  wire [31:0] rom_a, rom_b;', '  wire [31:0] rom_a, rom_b;\n  reg [31:0] b_rom_addr_q;')
text=text.replace('u_rom_b (.addr_i(b_addr_i)', 'u_rom_b (.addr_i(Strategy == 0 ? b_rom_addr_q : b_addr_i)')
text=text.replace('    integer i, byte_lane;\n    always', '''    integer i, byte_lane;
    reg [1:0] b_select_q;
    reg [31:0] b_ram_q;
    always @* begin
      case (b_select_q)
        1: b_rdata_o = rom_b;
        2: b_rdata_o = b_ram_q;
        default: b_rdata_o = 0;
      endcase
    end
    always''',1)
text=text.replace('        b_rdata_o <= 0;','        b_select_q <= 0;\n        b_ram_q <= 0;\n        b_rom_addr_q <= 0;',1)
old='''          if (!b_ok) b_rdata_o <= 0;
          else if (b_addr_i[31:2] < ProgramWords) b_rdata_o <= rom_b;
          else b_rdata_o <= data_mem[b_addr_i[31:2]-ProgramWords];'''
new='''          b_rom_addr_q <= b_addr_i;
          b_select_q <= !b_ok ? 0 : b_addr_i[31:2] < ProgramWords ? 1 : 2;
          if (b_ok && b_addr_i[31:2] >= ProgramWords)
            b_ram_q <= data_mem[b_addr_i[31:2]-ProgramWords];'''
assert old in text
text=text.replace(old,new)
out=ROOT/'asic/variants';out.mkdir(exist_ok=True)
(out/'asic_memory_registered_addr.v').write_text(text)
