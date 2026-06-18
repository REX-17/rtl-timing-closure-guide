def analyze_depth(path_data):

    paths = path_data.get("paths", [])

    if not paths:

        return {
            "max_depth": 0,
            "min_depth": 0,
            "avg_depth": 0,
            "total_paths": 0,
            "depth_distribution": [],
            "deepest_paths": []
        }

    depths = []

    for path in paths:

        depths.append(
            path["logic_depth"]
        )

    max_depth = max(depths)

    min_depth = min(depths)

    avg_depth = round(
        sum(depths) / len(depths),
        2
    )

    deepest_paths = []

    for path in paths:

        if path["logic_depth"] == max_depth:

            deepest_paths.append(path)

    return {

        "max_depth": max_depth,

        "min_depth": min_depth,

        "avg_depth": avg_depth,

        "total_paths": len(paths),

        "depth_distribution": depths,

        "deepest_paths": deepest_paths

    }


def print_depth_report(depth_results):

    print("\n========== DEPTH ANALYSIS ==========")

    print(
        f"\nTotal Paths: "
        f"{depth_results['total_paths']}"
    )

    print(
        f"\nMaximum Depth: "
        f"{depth_results['max_depth']}"
    )

    print(
        f"\nMinimum Depth: "
        f"{depth_results['min_depth']}"
    )

    print(
        f"\nAverage Depth: "
        f"{depth_results['avg_depth']}"
    )

    print("\nDeepest Paths:")

    for path in depth_results["deepest_paths"]:

        print(
            f"\n{path['start_ff']} "
            f"-> "
            f"{path['end_ff']}"
        )

        print(
            f"Depth: "
            f"{path['logic_depth']}"
        )

        print(
            "Path: "
            +
            " -> ".join(
                path["path_nodes"]
            )
        )