# RTL Timing Closure Guide

An interactive RTL timing analysis platform built with Python and Streamlit for exploring timing-critical structures in Verilog/SystemVerilog designs.

The tool provides early-stage RTL timing exploration by identifying timing paths, measuring logic depth, analyzing fanout, assessing timing risk, and generating optimization guidance before synthesis and signoff STA.



##  Features

### Path Extraction
- Identifies FF-to-FF timing paths
- Displays path traversal details
- Calculates logic depth across combinational stages

### Logic Depth Analysis
- Detects deep combinational pipelines
- Highlights potentially critical timing paths
- Reports maximum logic depth

### Fanout Analysis
- Identifies high-fanout signals
- Reports fanout counts
- Flags potential timing bottlenecks

### Timing Risk Assessment
- Generates timing risk scores
- Classifies designs as:
  - Low Risk
  - Moderate Risk
  - High Risk
- Provides explanations for risk classification

### Optimization Assistant
- Suggests timing-closure improvements
- Provides what-if optimization guidance
- Discusses expected impact and tradeoffs

### Interactive Dashboard
- Modern Streamlit-based interface
- Upload custom Verilog/SystemVerilog files
- Analyze included sample RTL designs
- Visualize extracted timing information



##  Project Architecture

```
RTL Source
     │
     ▼
 Verilog Parser
     │
     ▼
 Connectivity Graph
     │
     ▼
 Path Extraction
     │
     ├── Logic Depth Analysis
     ├── Fanout Analysis
     ├── Risk Assessment
     └── Optimization Assistant
     │
     ▼
 Streamlit Dashboard
```

---

##  Project Structure

```
rtl-timing-closure-guide/
│
├── analysis/
│   ├── critical_path.py
│   ├── depth_analyzer.py
│   ├── fanout_analyzer.py
│   ├── clock_domain.py
│   ├── risk_assessment.py
│   └── optimization_assistant.py
│
├── sample_designs/
│   ├── simple_register_bank.v
│   ├── deep_pipeline.v
│   ├── high_fanout_controller.v
│   ├── multi_clock_interface.v
│   └── timing_stress_test.v
│
├── visualization/
│   ├── path_viewer.py
│   ├── charts.py
│   └── risk_dashboard.py
│
├── reports/
├── outputs/
├── parser.py
├── app.py
└── path_extractor.py
```

---

##  Technologies Used

- Python
- Streamlit
- Verilog/SystemVerilog Parsing
- Graph-Based Path Analysis
- Static Timing Exploration Concepts

---

##  Running the Project

### Clone Repository

```bash
git clone https://github.com/REX-17/rtl-timing-closure-guide.git
cd rtl-timing-closure-guide
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Application

```bash
streamlit run app.py
```

---

##  Example Analyses

### Deep Combinational Pipeline
- Long FF-to-FF path extraction
- High logic depth detection
- Timing risk evaluation

### High Fanout Controller
- Fanout hotspot identification
- Driver load analysis
- Optimization recommendations

### Multi-Clock Interface
- Clock domain awareness
- Timing path inspection

---

##  Current Scope

This project focuses on RTL-level timing exploration and timing-closure guidance.

It is **not a replacement for signoff Static Timing Analysis (STA)** tools such as PrimeTime or Tempus.

The current implementation does not perform:
- Gate-level delay calculation
- Setup timing checks
- Hold timing checks
- Clock uncertainty analysis
- Physical parasitic extraction

Instead, it provides early-stage visibility into RTL structures that may impact timing closure later in the design flow.

---

##  Future Improvements

- Graph visualization of timing paths
- Clock domain crossing (CDC) analysis
- Setup/Hold estimation models
- Timing path ranking
- Path filtering and search
- RTL optimization recommendations using AI
- Enhanced timing reports and export options

---

##  Author

Shubham Rane

RTL Timing Closure Guide was developed as an educational EDA-style project to explore RTL timing analysis concepts, critical path identification, fanout analysis, and timing-closure strategies through an interactive dashboard.

---
