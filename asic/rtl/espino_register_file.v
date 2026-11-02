// ASIC replacement for iCE40 BRAM: 15 writable registers, two synchronous reads.
// Read-before-write on a same-edge collision. x0 always returns zero.
module espino_register_file (
  input wire clk_i, rst_ni,
  input wire [3:0] raddr_a_i, raddr_b_i, waddr_i,
  input wire [31:0] wdata_i,
  input wire we_i,
  output reg [31:0] rdata_a_o, rdata_b_o
);
  reg [31:0] regs [1:15];
  integer i;
  always @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      for (i=1; i<16; i=i+1) regs[i] <= 32'b0;
      rdata_a_o <= 32'b0;
      rdata_b_o <= 32'b0;
    end else begin
      rdata_a_o <= raddr_a_i == 0 ? 32'b0 : regs[raddr_a_i];
      rdata_b_o <= raddr_b_i == 0 ? 32'b0 : regs[raddr_b_i];
      if (we_i && waddr_i != 0) regs[waddr_i] <= wdata_i;
    end
  end
endmodule
