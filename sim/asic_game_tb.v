`timescale 1ns/1ps
module asic_game_tb;
  parameter Strategy = 0;
  reg clk=0, rst=1;
  reg [3:0] buttons=0;
  wire [3:0] leds;
  always #50 clk=~clk;
`ifdef GATE
  asic_top dut (
`else
  asic_top #(.MemoryStrategy(Strategy)) dut (
`endif
    .i_Clk(clk), .rst_ni(rst), .i_Switch(buttons), .o_LED(leds),
    .i_SPI_SCLK(1'b0), .i_SPI_MOSI(1'b0), .i_SPI_CS_n(1'b1)
  );
  integer cycles=0, rounds=0, total=0, measured=0, attempt, target;
  integer prior_total, prior_rounds, expected, digit=0, data_accesses=0;
  integer stimulus_file;
  initial stimulus_file=$fopen("stimulus.csv","w");
  always @(negedge clk) begin
    #2;
    $fdisplay(stimulus_file,"%0d,%0d,%0d",cycles,rst,buttons);
  end
  always @(posedge clk) begin
    cycles=cycles+1;
    if (rst) begin
      if (dut.u_pochoco.data_req && !dut.u_pochoco.data_addr[31])
        data_accesses=data_accesses+1;
      if (dut.u_pochoco.u_core.rf_we) begin
        if(dut.u_pochoco.u_core.rf_waddr==2) rounds=dut.u_pochoco.u_core.rf_wdata;
        if(dut.u_pochoco.u_core.rf_waddr==3) total=dut.u_pochoco.u_core.rf_wdata;
        if(dut.u_pochoco.u_core.rf_waddr==10) begin
          measured=dut.u_pochoco.u_core.rf_wdata;
          $display("REACTION cycle=%0d value=%0d",cycles,measured);
        end
      end
      if (dut.u_pochoco.data_req && dut.u_pochoco.data_we) begin
        $display("STORE cycle=%0d addr=%08x value=%08x", cycles,dut.u_pochoco.data_addr,dut.u_pochoco.data_wdata);
        if(dut.u_pochoco.data_addr==32'h80000000) digit=dut.u_pochoco.data_wdata[7:0];
      end
    end
  end
  task respond;
    input integer wrong;
    begin
      wait(leds==15);
      wait(leds==1 || leds==2 || leds==4 || leds==8);
      target=leds;
      prior_rounds=rounds;
      prior_total=total;
      repeat(127) @(negedge clk);
      buttons=wrong ? (target==1 ? 2:1) : target;
      repeat(24) @(negedge clk);
      buttons=0;
      if(wrong) begin
        wait(digit==238);
        if(rounds!=prior_rounds || total!=prior_total) $fatal(1,"Wrong button lost previous rounds");
        $display("WRONG_PRESERVED rounds=%0d total=%0d",rounds,total);
      end else begin
        wait(rounds==prior_rounds+1);
        if(total!=prior_total+measured) $fatal(1,"Incorrect accumulation");
        $display("CORRECT rounds=%0d total=%0d measured=%0d",rounds,total,measured);
      end
    end
  endtask
  initial begin
    $dumpfile("game.vcd"); $dumpvars(1,asic_game_tb);
    #1 rst=0;
    repeat(6) @(negedge clk);
    rst=1;
    respond(0);
    respond(1);
    for(attempt=1;attempt<10;attempt=attempt+1) respond(0);
    wait(leds==0);
    repeat(300) @(negedge clk);
    expected=total/1000;
    if(expected>99) expected=99;
    expected=(expected/10)*16+(expected%10);
    if(digit!=expected) $fatal(1,"Average mismatch %0d vs %0d",digit,expected);
    if(data_accesses!=0) $fatal(1,"Game unexpectedly accessed RAM");
    $display("PASS GAME rounds=%0d total=%0d bcd=%02x RAM_accesses=%0d",rounds,total,digit,data_accesses);
    // Restart through button 4, then exercise external reset.
    buttons=8; repeat(30) @(negedge clk); buttons=0;
    wait(leds==15);
    if(rounds!=0 || total!=0) $fatal(1,"Restart failed");
    rst=0; repeat(6) @(negedge clk); rst=1;
    wait(leds==15);
    $display("PASS RESET_AND_RESTART");
    $finish;
  end
  initial begin #3000000; $fatal(1,"Timeout"); end
endmodule
