`timescale 1ns/1ps
`include "program_meta.vh"
module asic_memory_tb;
  parameter Strategy=0;
  reg clk=0,rst=1,ar=0,br=0,bw=0;
  reg [31:0] aa=32'hffffffff,ba=0,wd=0;
  reg [3:0] be=15;
  wire [31:0] aq,bq,expected;
  always #5 clk=~clk;
  asic_memory #(.Strategy(Strategy)) dut(clk,rst,ar,aa,aq,br,bw,be,ba,wd,bq);
  program_rom rom(aa,expected);
  integer i;
  task tick; begin @(posedge clk); #1; @(negedge clk); end endtask
  initial begin
    #1 rst=0; tick; rst=1; ar=1;
    for(i=0;i<`PROGRAM_WORDS;i=i+1) begin
      aa=i*4; tick;
      if((^aq)===1'bx || (^expected)===1'bx || aq!==expected) $fatal(1,"Program reset word %0d actual=%08x expected=%08x",i,aq,expected);
    end
    ar=0; aa=0; tick;
    if((^aq)===1'bx) $fatal(1,"Unknown output");
    br=1; bw=1; ba=`PROGRAM_WORDS*4; wd=32'h12345678; tick;
    bw=0; tick; if(bq!==32'h12345678) $fatal(1,"Data write");
    bw=1; be=4'b0101; wd=32'haabbccdd; tick;
    if(bq!==32'h12345678) $fatal(1,"Not read-before-write");
    bw=0; tick; if(bq!==32'h12bb56dd) $fatal(1,"Byte enable");
    ba=32'h10000000; bw=1; be=15; wd=32'hffffffff; tick;
    ba=`PROGRAM_WORDS*4; bw=0; tick;
    if(bq!==32'h12bb56dd) $fatal(1,"Address alias");
    ba=0; bw=1; wd=32'habcdef01; tick;
    ar=1; aa=0; bw=0; tick;
    if(Strategy==1 && aq!==32'habcdef01) $fatal(1,"Unified code not writable");
    if(Strategy==0 && aq!==expected) $fatal(1,"ROM writable");
    rst=0; tick; rst=1; tick;
    if(aq!==expected) $fatal(1,"Reset did not restore program");
    ba=`PROGRAM_WORDS*4; tick; if(bq!==0) $fatal(1,"Reset data");
    $display("PASS MEMORY strategy=%0d words=%0d data=1",Strategy,`PROGRAM_WORDS);
    $finish;
  end
endmodule
