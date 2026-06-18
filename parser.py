import re
import os


def parse_file(filename):

    extension = os.path.splitext(filename)[1].lower()

    if extension == ".v":

        return parse_verilog(filename)

    elif extension == ".sv":

        return parse_systemverilog(filename)

    elif extension in [".vhd", ".vhdl"]:

        return parse_vhdl(filename)

    else:

        return None
    


def parse_verilog(filename):
    pass

def parse_systemverilog(filename):
    pass

def parse_vhdl(filename):
    pass


def parse_verilog(filename):

    print("\n========== VERILOG FILE ==========")

    with open(filename, "r") as f:
        code = f.read()

    # Remove comments
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    # Module Name
    module_match = re.search(
        r'\bmodule\s+(\w+)',
        code
    )

    module_name = (
        module_match.group(1)
        if module_match
        else "Not Found"
    )

    print("\nModule:")
    print(module_name)

    # Inputs
    inputs = re.findall(
        r'\binput\b(?:\s+reg|\s+wire)?(?:\s*\[\d+:\d+\])?\s+(\w+)',
        code
    )

    print("\nInputs:")
    for signal in inputs:
        print(signal)

    # Outputs
    outputs = re.findall(
        r'\boutput\b(?:\s+reg|\s+wire)?(?:\s*\[\d+:\d+\])?\s+(\w+)',
        code
    )

    print("\nOutputs:")
    for signal in outputs:
        print(signal)

    # Registers
    regs = re.findall(
        r'\breg\b(?:\s*\[\d+:\d+\])?\s+(\w+)',
        code
    )

    print("\nRegisters:")
    for reg in regs:
        print(reg)

    # Wires
    wires = re.findall(
        r'\bwire\b(?:\s*\[\d+:\d+\])?\s+(\w+)',
        code
    )

    print("\nWires:")
    for wire in wires:
        print(wire)

    # Parameters
    parameters = re.findall(
        r'\bparameter\b\s+(\w+)',
        code
    )

    print("\nParameters:")
    for param in parameters:
        print(param)

    # Behavioral Blocks
    behavioral_blocks = len(
        re.findall(
            r'\balways\b',
            code
        )
    )

    print("\nBehavioral Blocks:")
    print(behavioral_blocks)

    # Dataflow Assignments
    dataflow_assignments = len(
        re.findall(
            r'\bassign\b',
            code
        )
    )

    print("\nDataflow Assignments:")
    print(dataflow_assignments)

    # Structural Instances
    instances = re.findall(
        r'^\s*(?!module\b)(?!endmodule\b)(\w+)\s+(\w+)\s*\(',
        code,
        re.MULTILINE
    )

    print("\nStructural Instances:")

    for cell_type, inst_name in instances:

        print(
            f"{cell_type}  {inst_name}"
        )

    # Clock Detection
    clocks = []

    sensitivity_lists = re.findall(
        r'@\((.*?)\)',
        code
    )

    for sens in sensitivity_lists:

        signals = re.findall(
            r'(?:posedge|negedge)\s+(\w+)',
            sens
        )

        if len(signals) >= 1:

            clocks.append(signals[0])

    print("\nClocks:")

    for clk in set(clocks):
        print(clk)

    # Reset Detection
    resets = []

    for sens in sensitivity_lists:

        signals = re.findall(
            r'(?:posedge|negedge)\s+(\w+)',
            sens
        )

        if len(signals) >= 2:

            resets.append(signals[1])

    print("\nResets:")

    for rst in set(resets):
        print(rst)

    # Flip-Flop Detection
    assignments = re.findall(
        r'(\w+)\s*<=',
        code
    )

    flip_flops = []

    for reg in regs:

        if reg in assignments:

            flip_flops.append(reg)

    print("\nDetected Flip-Flops:")

    for ff in flip_flops:
        print(ff)

    print("\nTotal Flip-Flops:")
    print(len(flip_flops))

    netlist_info = detect_gate_netlist(code)

    print("\nGate Level Netlist:")
    print(netlist_info["is_gate_netlist"])

    print("\nNetlist DFF Cells:")
    print(netlist_info["total_dffs"])

    print("\nNetlist Scan Cells:")
    print(netlist_info["total_scan_cells"])


    return {

    "module": module_name,

    "inputs": inputs,

    "outputs": outputs,

    "registers": regs,

    "wires": wires,

    "parameters": parameters,

    "clocks": list(set(clocks)),

    "resets": list(set(resets)),

    "flip_flops": flip_flops,

    "total_flip_flops": len(flip_flops),

    "gate_netlist":
        netlist_info["is_gate_netlist"],

    "netlist_dffs":
        netlist_info["total_dffs"],

    "netlist_scan_cells":
        netlist_info["total_scan_cells"]

}




def parse_systemverilog(filename):

    print("\n========== SYSTEMVERILOG FILE ==========")

    with open(filename, "r") as f:
        code = f.read()

    # Remove comments
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    # Module Name
    module_match = re.search(
        r'\bmodule\s+(\w+)',
        code
    )

    module_name = (
        module_match.group(1)
        if module_match
        else "Not Found"
    )

    print("\nModule:")
    print(module_name)

    # Inputs
    inputs = re.findall(
        r'\binput\b(?:\s+logic)?(?:\s*\[\d+:\d+\])?\s+(\w+)',
        code
    )

    print("\nInputs:")
    for signal in inputs:
        print(signal)

    # Outputs
    outputs = re.findall(
        r'\boutput\b(?:\s+logic)?(?:\s*\[\d+:\d+\])?\s+(\w+)',
        code
    )

    print("\nOutputs:")
    for signal in outputs:
        print(signal)

    # Logic Signals
    logic_signals = re.findall(
        r'\blogic\b(?:\s*\[\d+:\d+\])?\s+(\w+)',
        code
    )

    print("\nLogic Signals:")
    for signal in logic_signals:
        print(signal)

    # always_ff
    always_ff_blocks = len(
        re.findall(
            r'\balways_ff\b',
            code
        )
    )

    print("\nalways_ff Blocks:")
    print(always_ff_blocks)

    # always_comb
    always_comb_blocks = len(
        re.findall(
            r'\balways_comb\b',
            code
        )
    )

    print("\nalways_comb Blocks:")
    print(always_comb_blocks)

    # FSM Detection
    fsm_states = []

    enum_match = re.search(
        r'typedef\s+enum.*?\{(.*?)\}',
        code,
        re.DOTALL
    )

    if enum_match:

        state_text = enum_match.group(1)

        fsm_states = [
            x.strip()
            for x in state_text.split(',')
            if x.strip()
        ]

    print("\nFSM States:")

    for state in fsm_states:
        print(state)

    print("\nFSM State Count:")
    print(len(fsm_states))

    # Clock Detection
    clocks = []

    sensitivity_lists = re.findall(
        r'@\((.*?)\)',
        code
    )

    for sens in sensitivity_lists:

        signals = re.findall(
            r'(?:posedge|negedge)\s+(\w+)',
            sens
        )

        if len(signals) >= 1:
            clocks.append(signals[0])

    print("\nClocks:")

    for clk in set(clocks):
        print(clk)

    # FF Detection
    assignments = re.findall(
        r'(\w+)\s*<=',
        code
    )

    flip_flops = []

    for signal in logic_signals:

        if signal in assignments:

            flip_flops.append(signal)

    print("\nDetected Flip-Flops:")

    for ff in flip_flops:
        print(ff)

    print("\nTotal Flip-Flops:")
    print(len(flip_flops))


    netlist_info = detect_gate_netlist(code)

    print("\nGate Level Netlist:")
    print(netlist_info["is_gate_netlist"])

    print("\nNetlist DFF Cells:")
    print(netlist_info["total_dffs"])

    print("\nNetlist Scan Cells:")
    print(netlist_info["total_scan_cells"])


    return {

    "module": module_name,

    "inputs": inputs,

    "outputs": outputs,

    "logic_signals": logic_signals,

    "fsm_states": fsm_states,

    "fsm_state_count":
        len(fsm_states),

    "clocks":
        list(set(clocks)),

    "flip_flops":
        flip_flops,

    "total_flip_flops":
        len(flip_flops),

    "gate_netlist":
        netlist_info["is_gate_netlist"],

    "netlist_dffs":
        netlist_info["total_dffs"],

    "netlist_scan_cells":
        netlist_info["total_scan_cells"]

}


def parse_vhdl(filename):

    print("\n========== VHDL FILE ==========")

    with open(filename, "r") as f:
        code = f.read()

    code_lower = code.lower()

    # Entity Name
    entity_match = re.search(
        r'entity\s+(\w+)\s+is',
        code_lower
    )

    entity_name = (
        entity_match.group(1)
        if entity_match
        else "Not Found"
    )

    print("\nEntity:")
    print(entity_name)

    # Architecture
    architecture_match = re.search(
        r'architecture\s+(\w+)\s+of',
        code_lower
    )

    architecture_name = (
        architecture_match.group(1)
        if architecture_match
        else "Not Found"
    )

    print("\nArchitecture:")
    print(architecture_name)

    # Signals
    signals = re.findall(
        r'signal\s+(\w+)',
        code_lower
    )

    print("\nSignals:")

    for signal in signals:
        print(signal)

    # Processes
    processes = len(
        re.findall(
            r'\bprocess\s*\(',
            code_lower
        )
    )

    print("\nProcess Blocks:")
    print(processes)

    # Clock Detection
    clocks = re.findall(
        r'rising_edge\s*\(\s*(\w+)\s*\)',
        code_lower
    )

    print("\nClocks:")

    for clk in set(clocks):
        print(clk)

    # FF Detection
    flip_flops = []

    if len(clocks) > 0:

        flip_flops = signals

    print("\nDetected Flip-Flops:")

    for ff in flip_flops:
        print(ff)

    print("\nTotal Flip-Flops:")
    print(len(flip_flops))


    return {

    "module": entity_name,

    "architecture":
        architecture_name,

    "signals":
        signals,

    "clocks":
        list(set(clocks)),

    "flip_flops":
        flip_flops,

    "total_flip_flops":
        len(flip_flops)

}



def detect_gate_netlist(code):

    dff_patterns = [

        r'\bDFF\b',
        r'\bDFFR\b',
        r'\bDFFRX1\b',
        r'\bDFFPOSX1\b',
        r'\bFDRE\b',
        r'\bFDCE\b'

    ]

    scan_patterns = [

        r'\bSDFF\b',
        r'\bSDFFRX1\b',
        r'\bSCAN_DFF\b'

    ]

    dff_cells = []
    scan_cells = []

    for pattern in dff_patterns:

        matches = re.findall(
            pattern,
            code,
            flags=re.IGNORECASE
        )

        dff_cells.extend(matches)

    for pattern in scan_patterns:

        matches = re.findall(
            pattern,
            code,
            flags=re.IGNORECASE
        )

        scan_cells.extend(matches)

    total_dffs = len(dff_cells)
    total_scan_cells = len(scan_cells)

    is_gate_netlist = (
        total_dffs > 0
        or
        total_scan_cells > 0
    )

    return {

        "is_gate_netlist":
            is_gate_netlist,

        "dff_cells":
            dff_cells,

        "scan_cells":
            scan_cells,

        "total_dffs":
            total_dffs,

        "total_scan_cells":
            total_scan_cells

    }


def parse_files(file_list):
    """
    Parse multiple RTL files and merge the results into a
    single project-level representation.

    Backward compatible:
        - parse_file(path)  -> single file
        - parse_files(list) -> multiple files
    """

    merged = {

        "modules": [],

        "inputs": [],

        "outputs": [],

        "registers": [],

        "logic_signals": [],

        "signals": [],

        "wires": [],

        "parameters": [],

        "clocks": [],

        "resets": [],

        "flip_flops": [],

        "total_flip_flops": 0,

        "gate_netlist": False,

        "netlist_dffs": 0,

        "netlist_scan_cells": 0

    }

    for filename in file_list:

        parsed = parse_file(filename)

        if parsed is None:
            continue

        if "module" in parsed:
            merged["modules"].append(
                parsed["module"]
            )

        merged["inputs"].extend(
            parsed.get("inputs", [])
        )

        merged["outputs"].extend(
            parsed.get("outputs", [])
        )

        merged["registers"].extend(
            parsed.get("registers", [])
        )

        merged["logic_signals"].extend(
            parsed.get("logic_signals", [])
        )

        merged["signals"].extend(
            parsed.get("signals", [])
        )

        merged["wires"].extend(
            parsed.get("wires", [])
        )

        merged["parameters"].extend(
            parsed.get("parameters", [])
        )

        merged["clocks"].extend(
            parsed.get("clocks", [])
        )

        merged["resets"].extend(
            parsed.get("resets", [])
        )

        merged["flip_flops"].extend(
            parsed.get("flip_flops", [])
        )

        merged["netlist_dffs"] += parsed.get(
            "netlist_dffs",
            0
        )

        merged["netlist_scan_cells"] += parsed.get(
            "netlist_scan_cells",
            0
        )

        merged["gate_netlist"] = (
            merged["gate_netlist"]
            or
            parsed.get("gate_netlist", False)
        )

    # Remove duplicates

    merged["modules"] = sorted(
        list(set(merged["modules"]))
    )

    merged["inputs"] = sorted(
        list(set(merged["inputs"]))
    )

    merged["outputs"] = sorted(
        list(set(merged["outputs"]))
    )

    merged["registers"] = sorted(
        list(set(merged["registers"]))
    )

    merged["logic_signals"] = sorted(
        list(set(merged["logic_signals"]))
    )

    merged["signals"] = sorted(
        list(set(merged["signals"]))
    )

    merged["wires"] = sorted(
        list(set(merged["wires"]))
    )

    merged["parameters"] = sorted(
        list(set(merged["parameters"]))
    )

    merged["clocks"] = sorted(
        list(set(merged["clocks"]))
    )

    merged["resets"] = sorted(
        list(set(merged["resets"]))
    )

    merged["flip_flops"] = sorted(
        list(set(merged["flip_flops"]))
    )

    merged["total_flip_flops"] = len(
        merged["flip_flops"]
    )

    return merged

if __name__ == "__main__":

    parse_file(
        "test_designs/parser_testing/dataflow.v"
    )