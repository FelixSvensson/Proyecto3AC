// Explicit hierarchy for measured area and placement traceability.
module cycle_counter(input wire clk_i, rst_ni, output reg [31:0] count_o);
  always @(posedge clk_i or negedge rst_ni)
    if (!rst_ni) count_o <= 32'b0;
    else count_o <= count_o + 32'd1;
endmodule
