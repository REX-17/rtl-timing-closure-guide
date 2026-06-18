def analyze_clock_domains(parsed_data):
    """
    Analyze clock domains for either a single parsed_data dict
    or a list of parsed_data dictionaries.
    """

    # Support multiple uploaded files
    if isinstance(parsed_data, list):

        clocks = []

        for design in parsed_data:
            clocks.extend(
                design.get("clocks", [])
            )

    else:
        clocks = parsed_data.get("clocks", [])

    unique_clocks = sorted(set(clocks))

    total_clock_domains = len(unique_clocks)

    if total_clock_domains == 0:
        status = "No clock detected"
    elif total_clock_domains == 1:
        status = "Single clock domain"
    else:
        status = "Multiple clock domains"

    return {
        "clock_domains": unique_clocks,
        "total_clock_domains": total_clock_domains,
        "status": status
    }

def print_clock_domain_report(clock_results):

    print("\n========== CLOCK DOMAIN ANALYSIS ==========")

    print(
        f"\nTotal Clock Domains: "
        f"{clock_results['total_clock_domains']}"
    )

    print("\nDetected Clock Domains:")

    if len(clock_results["clock_domains"]) == 0:

        print("None")

    else:

        for clk in clock_results["clock_domains"]:

            print(clk)

    print(
        f"\nStatus: "
        f"{clock_results['status']}"
    )

    if clock_results["total_clock_domains"] > 1:

        print(
            "\nRecommendation:"
        )

        print(
            "Multiple clock domains detected."
        )

        print(
            "Consider Clock Domain Crossing (CDC) verification."
        )

def analyze_multiple_clock_domains(
    parsed_data_list
):
    """
    Analyze clock domains across multiple
    parsed RTL files.
    """

    all_clocks = []

    for parsed_data in parsed_data_list:

        all_clocks.extend(
            parsed_data.get(
                "clocks",
                []
            )
        )

    unique_clocks = sorted(
        list(set(all_clocks))
    )

    total_clock_domains = len(
        unique_clocks
    )

    if total_clock_domains == 0:

        status = "No clock detected"

    elif total_clock_domains == 1:

        status = "Single clock domain"

    else:

        status = "Multiple clock domains"

    return {

        "clock_domains":
            unique_clocks,

        "total_clock_domains":
            total_clock_domains,

        "status":
            status

    }