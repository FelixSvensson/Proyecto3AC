"""Derive ASIC wrappers from the preserved FPGA sources. Run from any directory."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    out = ROOT / 'asic/rtl'
    out.mkdir(parents=True, exist_ok=True)
    soc = (ROOT / 'rtl/pochoco_soc.v').read_text(encoding='utf-8')
    soc = soc.replace('module pochoco_soc #(\n  parameter NumWords   = 512,\n  parameter MemFile    = "../sw/blink.hex"', 'module pochoco_soc_asic #(\n  parameter MemoryStrategy = 0')
    soc = soc.replace('input  wire       i_Clk,', 'input  wire       i_Clk,\n  input wire rst_ni,')
    start = soc.index('  // Power-on reset')
    end = soc.index('  // Core-memory wiring')
    soc = soc[:start] + soc[end:]
    soc = soc.replace('pochoco_ram #(.NumWords(NumWords), .MemFile(MemFile))', 'asic_memory #(.Strategy(MemoryStrategy))')
    soc = soc.replace('.clk_i     (clk),\n    .a_req_i', '.clk_i     (clk),\n    .rst_ni    (rst_ni),\n    .a_req_i')
    (out / 'pochoco_soc_asic.v').write_text(soc, encoding='utf-8')
    top = (ROOT / 'rtl/game_top.v').read_text(encoding='utf-8')
    top = top.replace('module game_top (', 'module asic_top #(parameter MemoryStrategy = 0) (')
    top = top.replace('input  wire       i_Clk,', 'input  wire       i_Clk,\n  input wire rst_ni,')
    top = top.replace('pochoco_soc #(\n    .MemFile("sw/game.hex")', 'pochoco_soc_asic #(\n    .MemoryStrategy(MemoryStrategy)')
    top = top.replace('.i_Clk        (i_Clk),', '.i_Clk        (i_Clk),\n    .rst_ni       (rst_ni),')
    (out / 'asic_top.v').write_text(top, encoding='utf-8')
    periph = (ROOT/'rtl/pochoco_periph.v').read_text(encoding='utf-8')
    periph = periph.replace('  reg [31:0] cycle_q;', '  wire [31:0] cycle_q;')
    start = periph.index('  always @(posedge clk_i or negedge rst_ni) begin')
    end = periph.index('  always @(posedge clk_i or negedge rst_ni) begin',start+1)
    periph = periph[:start] + '  cycle_counter u_cycle_counter (.clk_i(clk_i), .rst_ni(rst_ni), .count_o(cycle_q));\n\n' + periph[end:]
    (out/'pochoco_periph.v').write_text(periph,encoding='utf-8')


if __name__ == '__main__':
    main()
