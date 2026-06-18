import re
print("\nINSIDE EXTRACT PATHS")

def extract_paths(filename, parsed_data):

    with open(filename, "r") as f:
        code = f.read()

    # Remove comments
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    flip_flops = parsed_data.get("flip_flops", [])

    assign_connections = extract_assign_connections(code)

    comb_connections = extract_combinational_connections(code)

    ff_connections = extract_ff_connections(code)

    print("\nASSIGN CONNECTIONS")
    print(assign_connections)

    print("\nCOMB CONNECTIONS")
    print(comb_connections)

    print("\nFF CONNECTIONS")
    print(ff_connections)

    graph = build_graph(
    assign_connections + comb_connections,
    ff_connections
)
    print("GRAPH =", graph)
    for k, v in graph.items():
        print(k, "->", v)
    

    paths = find_ff_to_ff_paths(
        graph,
        flip_flops
    )

    return {
        "paths": paths
    }


def extract_assign_connections(code):

    connections = []

    assigns = re.findall(
        r'assign\s+(\w+)\s*=\s*(.*?);',
        code
    )

    for destination, expression in assigns:

        sources = re.findall(
            r'\b[a-zA-Z_]\w*\b',
            expression
        )

        keywords = {
            "and", "or", "not",
            "xor", "xnor"
        }

        sources = [
            s for s in sources
            if s.lower() not in keywords
        ]

        connections.append({
            "destination": destination,
            "sources": sources
        })

    return connections

def extract_combinational_connections(code):

    connections = []

    matches = re.findall(
        r'(\w+)\s*=\s*(.*?);',
        code
    )

    for destination, expression in matches:

        sources = re.findall(
            r'\b[a-zA-Z_]\w*\b',
            expression
        )

        connections.append({
            "destination": destination,
            "sources": sources
        })

    return connections



def extract_ff_connections(code):

    connections = []

    ff_assignments = re.findall(
        r'(\w+)\s*<=\s*(.*?);',
        code
    )

    for destination, expression in ff_assignments:

        sources = re.findall(
            r'\b[a-zA-Z_]\w*\b',
            expression
        )

        connections.append({
            "destination": destination,
            "sources": sources
        })

    return connections


def build_graph(assign_connections, ff_connections):

    graph = {}

    all_connections = (
        assign_connections +
        ff_connections
    )

    for connection in all_connections:

        destination = connection["destination"]

        graph[destination] = (
            connection["sources"]
        )

    return graph


def find_ff_to_ff_paths(graph, flip_flops):

    print("\nFLIP FLOPS =", flip_flops)

    paths = []

    for end_ff in flip_flops:

        visited = set()

        trace_path(
            current_node=end_ff,
            graph=graph,
            flip_flops=flip_flops,
            visited=visited,
            current_path=[end_ff],
            paths=paths
        )

    return paths

def trace_path(
    current_node,
    graph,
    flip_flops,
    visited,
    current_path,
    paths
):

    print("VISITING:", current_node)
    print("CURRENT PATH:", current_path)

    if current_node in visited:
        return

    visited.add(current_node)

    # Reached a leaf node
    if current_node not in graph:

        paths.append({
            "start_ff": current_path[0],
            "end_ff": current_node,
            "logic_depth": max(0, len(current_path) - 2),
            "path_nodes": list(current_path)
        })

        return

    # Continue traversing all predecessors
    for source in graph[current_node]:

        trace_path(
            source,
            graph,
            flip_flops,
            visited.copy(),
            current_path + [source],
            paths
        )