module timing_stress (
    input clk,
    input [7:0] a,
    input [7:0] b,
    input [7:0] c,
    input [7:0] d,
    output reg [7:0] y
);

reg [7:0] r1;
reg [7:0] r2;

wire [7:0] w1;
wire [7:0] w2;
wire [7:0] w3;
wire [7:0] w4;
wire [7:0] w5;

assign w1 = a + b;
assign w2 = w1 ^ c;
assign w3 = w2 + d;
assign w4 = w3 | r1;
assign w5 = w4 & r2;

always @(posedge clk) begin
    r1 <= w5;
    r2 <= r1;
    y <= r2;
end

endmodule