module deep_pipeline (
    input clk,
    input rst,
    input [7:0] a,
    output reg [7:0] y
);

reg [7:0] ff1;
reg [7:0] ff2;

wire [7:0] s1;
wire [7:0] s2;
wire [7:0] s3;
wire [7:0] s4;
wire [7:0] s5;
wire [7:0] s6;

// Launch FF
always @(posedge clk or posedge rst) begin
    if (rst)
        ff1 <= 8'd0;
    else
        ff1 <= a;
end

// Deep combinational chain
assign s1 = ff1 + 8'd1;
assign s2 = s1  + 8'd1;
assign s3 = s2  + 8'd1;
assign s4 = s3  + 8'd1;
assign s5 = s4  + 8'd1;
assign s6 = s5  + 8'd1;

// Capture FF
always @(posedge clk or posedge rst) begin
    if (rst)
        ff2 <= 8'd0;
    else
        ff2 <= s6;
end

always @(posedge clk or posedge rst) begin
    if (rst)
        y <= 8'd0;
    else
        y <= ff2;
end

endmodule