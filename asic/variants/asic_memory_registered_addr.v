// Both strategies preserve the one-edge synchronous instruction/data interface.
// Full address checks prevent aliases. ROM is combinational behind the output FF.
// Strategy B initializes every program FF with an explicit asynchronous reset.
`include "program_meta.vh"
module asic_memory #(parameter Strategy=0, parameter DataWords=1) (
  input wire clk_i, rst_ni,
  input wire a_req_i,
  input wire [31:0] a_addr_i,
  output reg [31:0] a_rdata_o,
  input wire b_req_i, b_we_i,
  input wire [3:0] b_be_i,
  input wire [31:0] b_addr_i, b_wdata_i,
  output reg [31:0] b_rdata_o
);
  localparam ProgramWords = `PROGRAM_WORDS;
  localparam TotalWords = ProgramWords + DataWords;
  localparam AddrW = $clog2(TotalWords);
  wire [31:0] rom_a, rom_b;
  reg [31:0] b_rom_addr_q;
  program_rom u_rom_a (.addr_i(a_addr_i), .data_o(rom_a));
  program_rom u_rom_b (.addr_i(Strategy == 0 ? b_rom_addr_q : b_addr_i), .data_o(rom_b));
  wire a_ok = a_addr_i[1:0] == 0 && a_addr_i[31:2] < TotalWords;
  wire b_ok = b_addr_i[31:2] < TotalWords;
  generate if (Strategy == 0) begin: g_split
    reg [31:0] data_mem [0:DataWords-1];
    integer i, byte_lane;
    reg [1:0] b_select_q;
    reg [31:0] b_ram_q;
    always @* begin
      case (b_select_q)
        1: b_rdata_o = rom_b;
        2: b_rdata_o = b_ram_q;
        default: b_rdata_o = 0;
      endcase
    end
    always @(posedge clk_i or negedge rst_ni) begin
      if (!rst_ni) begin
        for (i=0; i<DataWords; i=i+1) data_mem[i] <= 0;
        a_rdata_o <= 0;
        b_select_q <= 0;
        b_ram_q <= 0;
        b_rom_addr_q <= 0;
      end else begin
        if (a_req_i) a_rdata_o <= a_ok && a_addr_i[31:2] < ProgramWords ? rom_a : 32'h00000013;
        if (b_req_i) begin
          b_rom_addr_q <= b_addr_i;
          b_select_q <= !b_ok ? 0 : b_addr_i[31:2] < ProgramWords ? 1 : 2;
          if (b_ok && b_addr_i[31:2] >= ProgramWords)
            b_ram_q <= data_mem[b_addr_i[31:2]-ProgramWords];
          if (b_we_i && b_ok && b_addr_i[31:2] >= ProgramWords)
            for (byte_lane=0; byte_lane<4; byte_lane=byte_lane+1)
              if (b_be_i[byte_lane]) data_mem[b_addr_i[31:2]-ProgramWords][8*byte_lane+:8] <= b_wdata_i[8*byte_lane+:8];
        end
      end
    end
  end else begin: g_unified
    reg [31:0] mem [0:TotalWords-1];
    // Generated case function supplies constants to reset pins; no initial/readmemh.
    `include "program_reset.vh"
    integer i, byte_lane;
    always @(posedge clk_i or negedge rst_ni) begin
      if (!rst_ni) begin
        for (i=0; i<TotalWords; i=i+1) mem[i] <= reset_word(i);
        a_rdata_o <= 0;
        b_rdata_o <= 0;
      end else begin
        if (a_req_i) a_rdata_o <= a_ok ? mem[a_addr_i[AddrW+1:2]] : 32'h00000013;
        if (b_req_i) begin
          b_rdata_o <= b_ok ? mem[b_addr_i[AddrW+1:2]] : 0;
          if (b_we_i && b_ok)
            for (byte_lane=0; byte_lane<4; byte_lane=byte_lane+1)
              if (b_be_i[byte_lane]) mem[b_addr_i[AddrW+1:2]][8*byte_lane+:8] <= b_wdata_i[8*byte_lane+:8];
        end
      end
    end
  end endgenerate
endmodule
