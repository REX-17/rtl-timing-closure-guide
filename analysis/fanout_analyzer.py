import re


def analyze_fanout(filenames, high_fanout_threshold=5):

    if isinstance(filenames, str):
        filenames = [filenames]

    fanout_map = {}

    for filename in filenames:

        with open(filename, "r") as f:
            code = f.read()

        # existing analysis logic goes here

    # Remove comments
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    fanout_map = {}

    # -----------------------------
    # Dataflow assignments
    # Example:
    # assign w2 = w1 | r1;
    # -----------------------------
    assign_matches = re.findall(
        r'assign\s+\w+\s*=\s*(.*?);',
        code
    )

    for expression in assign_matches:

        sources = re.findall(
            r'\b[a-zA-Z_]\w*\b',
            expression
        )

        for signal in sources:

            fanout_map[signal] = (
                fanout_map.get(signal, 0) + 1
            )

    # -----------------------------
    # Sequential assignments
    # Example:
    # r2 <= w2;
    # -----------------------------
    ff_matches = re.findall(
        r'\w+\s*<=\s*(.*?);',
        code
    )

    for expression in ff_matches:

        sources = re.findall(
            r'\b[a-zA-Z_]\w*\b',
            expression
        )

        for signal in sources:

            fanout_map[signal] = (
                fanout_map.get(signal, 0) + 1
            )

    if fanout_map:
        max_fanout = max(fanout_map.values())
    else:
        max_fanout = 0

    high_fanout_signals = []

    for signal, count in fanout_map.items():

        if count >= high_fanout_threshold:

            high_fanout_signals.append(
                {
                    "signal": signal,
                    "fanout": count
                }
            )

    return {

        "fanout_map": fanout_map,

        "max_fanout": max_fanout,

        "high_fanout_signals": high_fanout_signals

    }


def print_fanout_report(fanout_results):

    print("\n========== FANOUT ANALYSIS ==========")

    print("\nSignal Fanouts:")

    if len(fanout_results["fanout_map"]) == 0:

        print("No signals found.")

    else:

        for signal, count in sorted(
            fanout_results["fanout_map"].items()
        ):

            print(
                f"{signal} : {count}"
            )

    print(
        f"\nMaximum Fanout: "
        f"{fanout_results['max_fanout']}"
    )

    print("\nHigh Fanout Signals:")

    if len(
        fanout_results["high_fanout_signals"]
    ) == 0:

        print("None")

    else:

        for item in fanout_results[
            "high_fanout_signals"
        ]:

            print(
                f"{item['signal']} "
                f"(Fanout = {item['fanout']})"
            )

def analyze_multiple_fanouts(
    file_list,
    high_fanout_threshold=5
):
    """
    Analyze fanout across multiple RTL files.
    """

    combined_fanout = {}

    for filename in file_list:

        result = analyze_fanout(
            filename,
            high_fanout_threshold
        )

        for signal, count in result[
            "fanout_map"
        ].items():

            combined_fanout[signal] = (
                combined_fanout.get(
                    signal,
                    0
                )
                + count
            )

    if combined_fanout:

        max_fanout = max(
            combined_fanout.values()
        )

    else:

        max_fanout = 0

    high_fanout_signals = []

    for signal, count in combined_fanout.items():

        if count >= high_fanout_threshold:

            high_fanout_signals.append({

                "signal": signal,

                "fanout": count

            })

    return {

        "fanout_map":
            combined_fanout,

        "max_fanout":
            max_fanout,

        "high_fanout_signals":
            high_fanout_signals

    }