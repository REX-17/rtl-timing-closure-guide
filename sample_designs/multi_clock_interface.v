module medium_risk_design (
    input clk,
    input rst,
    input [7:0] a,
    input [7:0] b,
    output reg [7:0] y,
    output reg fanout_sig
);

reg [7:0] s1;
reg [7:0] s2;
reg [7:0] s3;
reg [7:0] s4;
reg [7:0] s5;
reg [7:0] s6;

// Deep combinational chain
always @(*) begin
    s1 = a + b;
    s2 = s1 ^ 8'hAA;
    s3 = s2 + 8'h55;
    s4 = s3 ^ 8'h0F;
    s5 = s4 + 8'h33;
    s6 = s5 ^ 8'hF0;
end

always @(posedge clk or posedge rst) begin
    if (rst)
        y <= 8'd0;
    else
        y <= s6;
end

// Artificial high fanout source
always @(posedge clk or posedge rst) begin
    if (rst)
        fanout_sig <= 1'b0;
    else
        fanout_sig <= y[0];
end

wire f1  = fanout_sig;
wire f2  = fanout_sig;
wire f3  = fanout_sig;
wire f4  = fanout_sig;
wire f5  = fanout_sig;
wire f6  = fanout_sig;
wire f7  = fanout_sig;
wire f8  = fanout_sig;
wire f9  = fanout_sig;
wire f10 = fanout_sig;
wire f11 = fanout_sig;
wire f12 = fanout_sig;

endmodule