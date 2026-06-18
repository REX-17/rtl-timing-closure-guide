from analysis.optimization_assistant import (
    generate_optimization_suggestions,
    print_optimization_report
)



from analysis.risk_assessment import (
    assess_timing_risk,
    print_risk_report
)



from analysis.clock_domain import (
    analyze_clock_domains,
    print_clock_domain_report
)



from analysis.fanout_analyzer import (
    analyze_fanout,
    print_fanout_report
)



from analysis.critical_path import (
    identify_critical_paths,
    print_critical_path_report
)


from parser import parse_file

from analysis.path_extractor import extract_paths
from analysis.depth_analyzer import (
    analyze_depth,
    print_depth_report
)

parsed_data = parse_file("test_files/test.v")

path_data = extract_paths(
    "test_files/test.v",
    parsed_data
)

print(path_data)

depth_results = analyze_depth(path_data)

print_depth_report(depth_results)


critical_results = identify_critical_paths(
    depth_results
)

print_critical_path_report(
    critical_results
)


fanout_results = analyze_fanout(
    "test_files/test.v"
)

print_fanout_report(
    fanout_results
)


clock_results = analyze_clock_domains(
    parsed_data
)

print_clock_domain_report(
    clock_results
)



risk_results = assess_timing_risk(
    depth_results,
    fanout_results,
    clock_results
)

print_risk_report(
    risk_results
)


suggestions = generate_optimization_suggestions(
    depth_results,
    fanout_results,
    clock_results,
    risk_results
)

print_optimization_report(
    suggestions
)