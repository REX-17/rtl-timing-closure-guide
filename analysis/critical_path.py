def identify_critical_paths(depth_results, top_n=5):
    """
    Identifies and ranks the top N critical paths based on logic depth.
    """

    critical_paths = sorted(
        depth_results.get("deepest_paths", []),
        key=lambda x: x["logic_depth"],
        reverse=True
    )

    critical_paths = critical_paths[:top_n]

    return {
        "critical_paths": critical_paths,
        "critical_path_count": len(critical_paths)
    }


def print_critical_path_report(critical_results):
    """
    Prints a formatted report of the critical paths.
    """

    print("\n========== CRITICAL PATH ANALYSIS ==========")

    print(
        f"\nCritical Paths Found: "
        f"{critical_results['critical_path_count']}"
    )

    if critical_results["critical_path_count"] == 0:
        print("\nNo critical paths detected.")
        return

    for index, path in enumerate(
        critical_results["critical_paths"],
        start=1
    ):

        print(f"\nCritical Path #{index}")

        print(
            f"Start Flip-Flop : {path['start_ff']}"
        )

        print(
            f"End Flip-Flop   : {path['end_ff']}"
        )

        print(
            f"Logic Depth     : {path['logic_depth']}"
        )

        print(
            "Path            : "
            + " -> ".join(path["path_nodes"])
        )