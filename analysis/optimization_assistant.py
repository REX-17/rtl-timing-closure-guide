def generate_optimization_suggestions(
    depth_results,
    fanout_results,
    clock_results,
    risk_results

    
):
    
    """
    Generates RTL-level timing optimization suggestions.
    """

    suggestions = []

    # -------------------------------------------------
    # Logic Depth
    # -------------------------------------------------

    if depth_results["max_depth"] >= 10:

        suggestions.append({

            "issue":
                f"Critical path depth is "
                f"{depth_results['max_depth']}",

            "what_if":
                "Insert a pipeline register "
                "near the middle of the path.",

            "expected_effect":
                "May reduce combinational "
                "logic depth and improve "
                "timing scalability.",

            "tradeoff":
                "Adds one clock cycle of "
                "latency."

        })

    elif depth_results["max_depth"] >= 5:

        suggestions.append({

            "issue":
                f"Moderately deep path "
                f"({depth_results['max_depth']})",

            "what_if":
                "Consider splitting the "
                "logic into multiple stages.",

            "expected_effect":
                "Potential reduction in "
                "timing risk.",

            "tradeoff":
                "May increase design "
                "complexity."

        })

    # -------------------------------------------------
    # Fanout
    # -------------------------------------------------

    for signal in fanout_results[
        "high_fanout_signals"
    ]:

        suggestions.append({

            "issue":
                f"High fanout on signal "
                f"{signal['signal']} "
                f"({signal['fanout']})",

            "what_if":
                "Introduce a buffer tree "
                "or duplicate the driver.",

            "expected_effect":
                "Reduced load per branch "
                "and improved signal "
                "distribution.",

            "tradeoff":
                "Additional hardware area."

        })

    # -------------------------------------------------
    # Clock Domains
    # -------------------------------------------
    if clock_results.get("total_clock_domains", 0) > 1:

        suggestions.append({
        "issue": "Multiple clock domains detected.",
        "what_if": "Insert CDC synchronizers and verify all clock crossings.",
        "expected_effect": "Reduces metastability risk and improves design reliability.",
        "tradeoff": "Adds latency and extra synchronization hardware."
    })

    if risk_results["status"] == "HIGH":

        suggestions.append({

        "issue":
            "Overall RTL timing risk is HIGH.",

        "what_if":
            "Review architecture for pipelining and logic partitioning.",

        "expected_effect":
            "Lower estimated timing risk.",

        "tradeoff":
            "May require RTL changes."

    })
        

    elif risk_results["status"] == "MEDIUM":

        suggestions.append({

        "issue":
            "Moderate RTL timing risk detected.",

        "what_if":
            "Consider pipelining long paths and reducing fanout.",

        "expected_effect":
            "Improved timing margin and easier timing closure.",

        "tradeoff":
            "May increase area or latency."

    })
    # -------------------------------------------------
    # Default suggestion if no issues are found
    # -------------------------------------------------

    if len(suggestions) == 0:

        suggestions.append({

            "issue":
                "No major RTL timing bottlenecks detected.",

            "what_if":
                "Proceed to synthesis and full STA for implementation-aware timing validation.",

            "expected_effect":
                "Current RTL structure appears timing-friendly.",

            "tradeoff":
                "Physical implementation may still introduce timing challenges."

        })

    return suggestions
