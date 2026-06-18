module timing_stress_test (
    input  wire        clk,
    input  wire        rst,
    input  wire [7:0]  a,
    input  wire [7:0]  b,
    input  wire [7:0]  c,
    input  wire [7:0]  d,
    output reg  [7:0]  y
);

wire [7:0] s1;
wire [7:0] s2;
wire [7:0] s3;
wire [7:0] s4;
wire [7:0] s5;
wire [7:0] s6;
wire [7:0] s7;
wire [7:0] s8;

assign s1 = a + b;
assign s2 = s1 ^ c;
assign s3 = s2 + d;
assign s4 = (s3 & a) | b;
assign s5 = s4 + s1;
assign s6 = s5 ^ s2;
assign s7 = (s6 | s3) & s4;
assign s8 = s7 + s5;

always @(posedge clk or posedge rst) begin
    if (rst)
        y <= 8'd0;
    else
        y <= s8;
end

endmodule