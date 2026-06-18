import streamlit as st
import json


from parser import parse_file

from analysis.path_extractor import extract_paths
from analysis.depth_analyzer import (
    analyze_depth,
)
from analysis.critical_path import (
    identify_critical_paths,
)
from analysis.fanout_analyzer import (
    analyze_fanout,
)
from analysis.clock_domain import (
    analyze_clock_domains,
)
from analysis.risk_assessment import (
    assess_timing_risk,
)
from analysis.optimization_assistant import (
    generate_optimization_suggestions,
)

import tempfile
import os

st.set_page_config(
    page_title="RTL Timing Closure Guide",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

/* ------------------------------
   Overall Page
------------------------------ */

.stApp {
    background: black;
}

.block-container {
    max-width: 1200px;
    margin: auto;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ------------------------------
   Titles
------------------------------ */

h1 {
    text-align: center;
    font-size: 3rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.2rem;
    color: #3B82F6 !important;
    text-shadow: 0 0 15px rgba(59,130,246,0.35);
  
}

h2, h3 {
    border-left: none !important;
    padding-left: 0 !important;
    color: #60A5FA !important;
    font-weight: 700 !important;
}

h1 {
    text-align: center;
}

/* Code / JSON containers */
        
div[data-testid="stCodeBlock"] {
    background: #07101F !important;
    border: 1px solid #1E3A8A !important;
    border-radius: 12px !important;
    box-shadow: 0 0 10px rgba(37,99,235,0.15);
}
            
div[data-testid="stCodeBlock"] pre,
div[data-testid="stCodeBlock"] code {
    color: #F8FAFC !important;
    font-size: 15px;
}

            
div[data-baseweb="select"] > div {
    background-color: #0B1120 !important;
    color: #E5E7EB !important;
    border: 1px solid #2563EB !important;
    border-radius: 12px !important;
}
            
div[role="listbox"] {
    background-color: #0B1120 !important;
    border: 1px solid #2563EB !important;
}

/* Dropdown popup background */
ul[role="listbox"] {
    background-color: #07101F !important;
    color: #E5E7EB !important;
}

/* Each option */
li[role="option"] {
    background-color: #07101F !important;
    color: #E5E7EB !important;
}

/* Hovered option */
li[role="option"]:hover {
    background-color: #1E3A8A !important;
    color: white !important;
}

/* Text inside options */
li[role="option"] * {
    color: #E5E7EB !important;
}

/* Entire JSON widget */
div[data-testid="stJson"] {
    background: #0B1120 !important;
    border: 1px solid #2563EB !important;
    border-radius: 18px !important;
    overflow: hidden !important;
}

/* Inner JSON container */
div[data-testid="stJson"] > div {
    background: #0B1120 !important;
}

/* Every nested JSON element */
div[data-testid="stJson"] * {
    background: #0B1120 !important;
}
            
/* PATH DATA JSON BOX */

div[data-testid="stJson"] {
    background: #0F172A !important;
    border: 1px solid #1E3A8A !important;
    border-radius: 18px !important;
    padding: 15px !important;
    box-shadow: 0 0 10px rgba(37,99,235,0.25);
}                
p,
span,
label,
li,
div {
    color: #E5E7EB;
}
               
/* ------------------------------
   Metric Cards
------------------------------ */

            
div[data-testid="metric-container"] {
    background: #07101F;
    border: 1px solid #1E3A8A;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 0 12px rgba(37,99,235,0.15);
}


div[data-testid="metric-container"] {
    text-align: center;
}

div[data-testid="metric-container"] label {
    display: block;
    text-align: center;
}

div[data-testid="metric-container"] > div {
    justify-content: center;
}

.stCodeBlock,
pre,
code {
    background-color: #0F172A !important;
    color: #E2E8F0 !important;
}

div[data-testid="stCode"] {
    background-color: #0F172A !important;
    color: #E2E8F0 !important;
    border-radius: 8px;
}


/* Expander container */
details {
    background-color: #16213E !important;
    border: 1px solid #2C3E50 !important;
    border-radius: 8px !important;
        
}

.stButton > button {
    background: #2563EB !important;
    color: blue !important;
    border-radius: 10px !important;
    border: none !important;
}

/* Expander title */
details summary {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    font-weight: 600 !important;
    padding: 10px !important;
}

/* Hover */
details summary:hover {
    background-color: #273449 !important;
    color: #F8FAFC !important;
}
            
details p,
details span,
details div {
    color: #F8FAFC !important;
}
            

/* Metric labels */
div[data-testid="metric-container"] label {
    color: #D1D5DB !important;
}

/* Metric values */
div[data-testid="metric-container"] div {
    color: #FFFFFF !important;
}

/* ------------------------------
   File Uploader
------------------------------ */

[data-testid="stFileUploader"] {
    background: #07101F;
    border: 1px solid #2563EB;
    border-radius: 16px;
    padding: 18px;
    color: #E2E8F0;
}
/* ------------------------------
   Tabs
------------------------------ */

[data-testid="stFileUploader"] button {
    background: linear-gradient(
        135deg,
        #2563EB,
        #1D4ED8
    ) !important;

    border: none !important;
    border-radius: 10px !important;
}
            
            
button[data-baseweb="tab"] {
    background: #334155 !important;
    color: white !important;
    border-radius: 999px !important;
    padding: 8px 22px !important;
    margin-right: 8px !important;
    border: none !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: #2563EB !important;
    color: white !important;
}
/* ------------------------------
   Expanders
------------------------------ */

details {
    background-color: #111827;
    border-radius: 4px;
    border: 1px solid #374151;
    padding: 8px;
}

details summary {
    color: white;
    font-weight: 600;
}

/* ------------------------------
   Alerts
------------------------------ */

div[data-testid="stAlert"] {
    border-radius: 6px;
}

/* ------------------------------
   Hide Streamlit Branding
------------------------------ */

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stButton > button {
    background: linear-gradient(
        90deg,
        #2563EB,
        #1D4ED8
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 12px !important;

    font-weight: 700 !important;
}
            
div[data-testid="metric-container"] {
    background: #1E293B;
    border-radius: 18px;
    border: none;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    padding: 18px;
}
div[data-baseweb="select"] {
    background: #07101F !important;
}

div[data-baseweb="select"] * {
    color: #E5E7EB !important;
}



</style>
""", unsafe_allow_html=True)

st.title("RTL Timing Closure Guide")

st.caption(
    "RTL-Level Static Timing Exploration and What-If Optimization Assistance"
)

uploaded_files = st.file_uploader(
    "Upload Verilog / SystemVerilog / VHDL Files",
    type=["v", "sv", "vhd", "vhdl"],
    accept_multiple_files=True
)

sample_files = {
    "None": None,
    "Simple Register Bank (Low Risk)": "sample_designs/simple_register_bank.v",
    "Deep Combinational Pipeline": "sample_designs/deep_pipeline.v",
    "High Fanout Controller": "sample_designs/high_fanout_controller.v",
    "Multi-Clock Interface": "sample_designs/multi_clock_interface.v",
    "Timing Stress Test": "sample_designs/timing_stress_test.v",
}

selected_sample = st.selectbox(
    "Try Sample RTL Design",
    list(sample_files.keys()),
    key="sample_selector"
)

analyze_clicked = st.button(
    "Analyze the Design",
    use_container_width=True

)
designs_to_analyze = []

# Add selected sample
if selected_sample != "None":
    designs_to_analyze.append({
        "name": selected_sample,
        "path": sample_files[selected_sample]
    })

# Add uploaded files
if uploaded_files:

    st.success(
        f"{len(uploaded_files)} file(s) uploaded successfully."
    )

    for uploaded_file in uploaded_files:

        suffix = os.path.splitext(uploaded_file.name)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp:

            tmp.write(uploaded_file.read())

            designs_to_analyze.append({
                "name": uploaded_file.name,
                "path": tmp.name
            })

            

# Analyze every selected design
if analyze_clicked:

    for design in designs_to_analyze:

        st.markdown("---")
        st.header(f" {design['name']}")

        temp_path = design["path"]

        parsed_data = parse_file(temp_path)

        path_data = extract_paths(
        temp_path,
        parsed_data
    )
        st.write("PATH DATA")
        st.write(path_data)

        depth_results = analyze_depth(
        path_data
    )

        critical_results = identify_critical_paths(
        depth_results
    )

        fanout_results = analyze_fanout(
        temp_path
    )

        clock_results = analyze_clock_domains(
        parsed_data
    )
        st.write("CLOCK RESULTS")
        st.write(clock_results)
       

        risk_results = assess_timing_risk(
        depth_results,
        fanout_results,
        clock_results
    )
        st.write("RISK RESULTS")
        st.write(risk_results)

        suggestions = generate_optimization_suggestions(
        depth_results,
        fanout_results,
        clock_results,
        risk_results
    )
        

        st.info(
        f"Analysis completed for {design['name']}"
    )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
        "Flip-Flops",
        len(parsed_data.get("flip_flops", []))
    )

        col2.metric(
        "Timing Paths",
        depth_results["total_paths"]
    )

        col3.metric(
        "Max Logic Depth",
        depth_results["max_depth"]
    )

        col4.metric(
        "Risk Score",
        f"{risk_results['risk_score']}/100"
    )

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Design",
        "Paths",
        "Fanout",
        "Risk",
        "Optimization Assistance"
    ])

        with tab1:

            st.subheader("Design Information")

            st.code(
            json.dumps(parsed_data, indent=4),
            language="json"
        )

        with tab2:

            st.subheader("Path Analysis")

            st.code(
            json.dumps(path_data, indent=4),
            language="json"
        )

            st.subheader("Depth Analysis")

            st.code(
            json.dumps(depth_results, indent=4),
            language="json"
        )

            st.subheader("Critical Paths")

            st.code(
            json.dumps(critical_results, indent=4),
            language="json"
        )

        with tab3:

            st.subheader("Fanout")

            st.code(
            json.dumps(fanout_results, indent=4),
            language="json"
        )

            st.subheader("Clock Domains")

            st.code(
            json.dumps(clock_results, indent=4),
            language="json"
        )

        with tab4:

            st.metric(
                "Timing Risk Score",
                f"{risk_results['risk_score']}/100"
            )

            if risk_results["status"] == "LOW":
                st.success("LOW TIMING RISK")
            elif risk_results["status"] == "MEDIUM":
                st.warning("MEDIUM TIMING RISK")
            else:
                st.error("HIGH TIMING RISK")

            st.write("Reasons:")

            if risk_results["reasons"]:
                for reason in risk_results["reasons"]:
                    st.markdown(f"- {reason}")
            else:
                st.success(
            "No significant RTL timing risks detected."
        )

        with tab5:

            if len(suggestions) > 0:

                for i, suggestion in enumerate(
                    suggestions,
                    start=1
                ):

                    with st.expander(
                        f"Suggestion {i}",
                        expanded=True
                    ):

                        st.markdown(
                            f"**Issue:** {suggestion['issue']}"
                        )

                        st.markdown(
                            f"**What-if:** {suggestion['what_if']}"
                        )

                        st.markdown(
                            f"**Expected Effect:** {suggestion['expected_effect']}"
                        )

                        st.markdown(
                            f"**Tradeoff:** {suggestion['tradeoff']}"
                        )

            else:

                st.success(
                    "No optimization suggestions."
                )