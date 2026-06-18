module high_fanout_controller (
    input clk,
    input rst,
    input enable,
    output reg q0,
    output reg q1,
    output reg q2,
    output reg q3,
    output reg q4,
    output reg q5,
    output reg q6,
    output reg q7,
    output reg q8,
    output reg q9,
    output reg q10,
    output reg q11
);

always @(posedge clk or posedge rst) begin
    if (rst) begin
        q0 <= 0;
        q1 <= 0;
        q2 <= 0;
        q3 <= 0;
        q4 <= 0;
        q5 <= 0;
        q6 <= 0;
        q7 <= 0;
        q8 <= 0;
        q9 <= 0;
        q10 <= 0;
        q11 <= 0;
    end
    else begin
        // One control signal drives many destinations
        q0 <= enable;
        q1 <= enable;
        q2 <= enable;
        q3 <= enable;
        q4 <= enable;
        q5 <= enable;
        q6 <= enable;
        q7 <= enable;
        q8 <= enable;
        q9 <= enable;
        q10 <= enable;
        q11 <= enable;
    end
end

endmodule