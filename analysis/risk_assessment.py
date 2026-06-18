def assess_timing_risk(
    depth_results,
    fanout_results,
    clock_results
):
    """
    Computes an RTL-level timing risk score.
    """

    risk_score = 0

    reasons = []

    # -----------------------------
    # Logic Depth Contribution
    # -----------------------------
    max_depth = depth_results["max_depth"]

    if max_depth >= 10:
        risk_score += 40
        reasons.append(
            f"Very deep logic path (Depth = {max_depth})"
        )

    elif max_depth >= 5:
        risk_score += 25
        reasons.append(
            f"Moderately deep logic path (Depth = {max_depth})"
        )

    elif max_depth > 0:
        risk_score += 10

    # -----------------------------
    # Fanout Contribution
    # -----------------------------
    max_fanout = fanout_results["max_fanout"]

    if max_fanout >= 20:
        risk_score += 30
        reasons.append(
            f"Very high fanout detected ({max_fanout})"
        )

    elif max_fanout >= 10:
        risk_score += 15
        reasons.append(
            f"Moderately high fanout detected ({max_fanout})"
        )

    # -----------------------------
    # Clock Domain Contribution
    # -----------------------------
    total_domains = clock_results[
        "total_clock_domains"
    ]

    if total_domains > 1:
        risk_score += 20
        reasons.append(
            "Multiple clock domains detected"
        )

    # -----------------------------
    # Clamp Score
    # -----------------------------
    if risk_score > 100:
        risk_score = 100

    # -----------------------------
    # Classification
    # -----------------------------
    if risk_score <= 30:
        status = "LOW"

    elif risk_score <= 60:
        status = "MEDIUM"

    else:
        status = "HIGH"

    return {

        "risk_score": risk_score,

        "status": status,

        "reasons": reasons

    }


def print_risk_report(risk_results):

    print(
        "\n========== TIMING RISK ASSESSMENT =========="
    )

    print(
        f"\nTiming Risk Score : "
        f"{risk_results['risk_score']}/100"
    )

    print(
        f"Risk Level        : "
        f"{risk_results['status']}"
    )

    print("\nReasons:")

    if len(risk_results["reasons"]) == 0:

        print(
            "No significant RTL timing risks detected."
        )

    else:

        for reason in risk_results["reasons"]:

            print(f"- {reason}")