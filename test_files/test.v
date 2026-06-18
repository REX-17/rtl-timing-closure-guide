module test(
input clk,
input a,
input b,
input c
);

reg r1;
reg r2;
reg r3;

wire w1;
wire w2;

assign w1 = r1 & a;
assign w2 = w1 | b;

always @(posedge clk)
begin
    r1 <= c;
    r2 <= w2;
    r3 <= r2;
end

endmodule