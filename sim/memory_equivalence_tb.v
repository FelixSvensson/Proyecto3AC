`timescale 1ns/1ps
module memory_equivalence_tb;
  reg clk=0,rst=1,ar=0,br=0,bw=0;
  reg [31:0] aa=0,ba=0,wd=0;
  reg [3:0] be=0;
  wire [31:0] aq0,aq1,bq0,bq1;
  asic_memory d0(clk,rst,ar,aa,aq0,br,bw,be,ba,wd,bq0);
  asic_memory_opt d1(clk,rst,ar,aa,aq1,br,bw,be,ba,wd,bq1);
  always #5 clk=~clk;
  integer i,j,seed=32'h32731;
  initial begin
    #1 rst=0;
    for(i=0;i<2000;i=i+1) begin
      @(negedge clk);
      rst=i%101!=0;
      ar=$random(seed)&1;
      br=$random(seed)&1;
      bw=$random(seed)&1;
      be=$random(seed);
      wd=$random(seed);
      aa=($random(seed)&127)*4;
      ba=($random(seed)&127)*4;
      if(i%3==0) ba=107*4;
      if(i%7==0) ba=32'h10000000;
      @(posedge clk); #1;
      if(aq0!==aq1 || bq0!==bq1) $fatal(1,"Memory mismatch step=%0d aq=%x/%x bq=%x/%x",i,aq0,aq1,bq0,bq1);
    end
    $display("PASS MEMORY_EQUIVALENCE 2000 deterministic randomized cycles");
    $finish;
  end
endmodule
