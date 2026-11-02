###############################################################################
# Created by write_sdc
###############################################################################
current_design asic_top
###############################################################################
# Timing Constraints
###############################################################################
create_clock -name i_Clk -period 87.0000 [get_ports {i_Clk}]
set_clock_transition 0.1500 [get_clocks {i_Clk}]
set_clock_uncertainty 0.2500 i_Clk
set_propagated_clock [get_clocks {i_Clk}]
set_input_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {i_SPI_CS_n}]
set_input_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {i_SPI_MOSI}]
set_input_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {i_SPI_SCLK}]
set_input_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {i_Switch[0]}]
set_input_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {i_Switch[1]}]
set_input_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {i_Switch[2]}]
set_input_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {i_Switch[3]}]
set_input_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {rst_ni}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_LED[0]}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_LED[1]}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_LED[2]}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_LED[3]}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_SPI_MISO}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment1_A}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment1_B}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment1_C}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment1_D}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment1_E}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment1_F}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment1_G}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment2_A}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment2_B}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment2_C}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment2_D}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment2_E}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment2_F}]
set_output_delay 20.0000 -clock [get_clocks {i_Clk}] -add_delay [get_ports {o_Segment2_G}]
###############################################################################
# Environment
###############################################################################
set_load -pin_load 0.0729 [get_ports {o_SPI_MISO}]
set_load -pin_load 0.0729 [get_ports {o_Segment1_A}]
set_load -pin_load 0.0729 [get_ports {o_Segment1_B}]
set_load -pin_load 0.0729 [get_ports {o_Segment1_C}]
set_load -pin_load 0.0729 [get_ports {o_Segment1_D}]
set_load -pin_load 0.0729 [get_ports {o_Segment1_E}]
set_load -pin_load 0.0729 [get_ports {o_Segment1_F}]
set_load -pin_load 0.0729 [get_ports {o_Segment1_G}]
set_load -pin_load 0.0729 [get_ports {o_Segment2_A}]
set_load -pin_load 0.0729 [get_ports {o_Segment2_B}]
set_load -pin_load 0.0729 [get_ports {o_Segment2_C}]
set_load -pin_load 0.0729 [get_ports {o_Segment2_D}]
set_load -pin_load 0.0729 [get_ports {o_Segment2_E}]
set_load -pin_load 0.0729 [get_ports {o_Segment2_F}]
set_load -pin_load 0.0729 [get_ports {o_Segment2_G}]
set_load -pin_load 0.0729 [get_ports {o_LED[3]}]
set_load -pin_load 0.0729 [get_ports {o_LED[2]}]
set_load -pin_load 0.0729 [get_ports {o_LED[1]}]
set_load -pin_load 0.0729 [get_ports {o_LED[0]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_4 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_Clk}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_SPI_CS_n}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_SPI_MOSI}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_SPI_SCLK}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {rst_ni}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_Switch[3]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_Switch[2]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_Switch[1]}]
set_driving_cell -lib_cell gf180mcu_fd_sc_mcu7t5v0__inv_1 -pin {ZN} -input_transition_rise 0.0000 -input_transition_fall 0.0000 [get_ports {i_Switch[0]}]
set_timing_derate -early 0.9500
set_timing_derate -late 1.0500
###############################################################################
# Design Rules
###############################################################################
set_max_transition 3.0000 [current_design]
set_max_capacitance 0.2000 [current_design]
set_max_fanout 10.0000 [current_design]
