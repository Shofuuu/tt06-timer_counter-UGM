`default_nettype none

module tt_um_timer_counter_UGM (
    input wire [7:0] ui_in, // Dedicated inputs - connected to the 8-bit ADC parallel output
    input wire [7:0] uo_out, // Dedicated outputs - connected to adc convStart, adc rd_cs, and synchronous rectifier high and low
    input  wire [7:0] uio_in,   // IOs: Bidirectional Input path - one input connected to adc busy signal
    output wire [7:0] uio_out,  // IOs: Bidirectional Output path
    output wire [7:0] uio_oe,   // IOs: Bidirectional Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // will go high when the design is enabled
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
    
    assign uio_oe = {8{1'b0}};
    assign uio_out[7:4] = {4{1'b0}};
    // assign uo_out = {8{1'b0}};

    timer_counter t0(
        .clk(clk), .inv(uio_in[0]), .rst(rst_n),
        .mode(uio_in[1]), .start(uio_in[2]), .stop(uio_in[3]),
        .segment(uo_out), .digit(uio_out[3:0])
    );

endmodule



