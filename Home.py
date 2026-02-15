import streamlit as st
import sys
import importlib.util

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="EcoGrid - Community Energy Toolkit",
    layout="wide",
    page_icon="🌱",
    initial_sidebar_state="expanded"  # Changed from collapsed to expanded
)

# ============================================================================
# INITIALIZE ALL SESSION STATE (shared across all tabs)
# ============================================================================
if 'geo_data' not in st.session_state:
    st.session_state.geo_data = {}
if 'pdf_extracted' not in st.session_state:
    st.session_state.pdf_extracted = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}
if 'linked_locations' not in st.session_state:
    st.session_state.linked_locations = []
if 'energy_history' not in st.session_state:
    from collections import deque
    st.session_state.energy_history = {
        'usage_log': deque(maxlen=50),
        'recovered_log': deque(maxlen=50),
        'remaining_log': deque(maxlen=50),
        'timestamps': deque(maxlen=50),
        'records': []
    }

# ============================================================================
# HELPER FUNCTION TO LOAD AND RUN PAGE FILES
# ============================================================================
def run_page_file(file_path, page_name):
    """Load and execute a page file from the pages folder"""
    import os
    
    # Check if file exists
    if not os.path.exists(file_path):
        st.error(f"❌ File not found: {file_path}")
        st.info("Please make sure your page files are in the correct location")
        return
    
    try:
        # Show what we're loading
        st.info(f"Loading {page_name}...")
        
        spec = importlib.util.spec_from_file_location(page_name, file_path)
        if spec is None:
            st.error(f"Could not load specification for {page_name}")
            return
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[page_name] = module
        spec.loader.exec_module(module)
        
        st.success(f"✅ {page_name} loaded successfully!")
        
    except Exception as e:
        st.error(f"❌ Error loading {page_name}:")
        st.error(str(e))
        st.info("Check the terminal for detailed error messages")
        
        # Show detailed error in expander
        with st.expander("Show detailed error"):
            import traceback
            st.code(traceback.format_exc())

# ============================================================================
# TEAM LOGO & HEADER
# ============================================================================
st.markdown("""
<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 30px;'>
    <h1 style='color: white; font-size: 3em; margin: 0;'>🌱 EcoGrid</h1>
    <p style='color: white; font-size: 1.2em; margin: 10px 0 0 0;'>Community Energy & Carbon Impact Toolkit</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# CREATE 5 TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👥 Introduction",
    "📚 About & Education", 
    "📊 Data & Calculation",
    "🔌 Verification Unit",
    "🏠 Household Energy Status"
])

# ============================================================================
# TAB 1: INTRODUCTION
# ============================================================================
with tab1:
    st.header("Welcome to EcoGrid")
    
    # Project Description
    st.markdown("""
    ### 🌍 Our Mission
    
    EcoGrid is a comprehensive platform designed to help communities analyze renewable energy potential,
    measure environmental impact, and optimize energy consumption. Our toolkit combines cutting-edge AI
    with practical energy calculations to make clean energy accessible to everyone.
    
    ### 🎯 What We Do
    
    - **Renewable Energy Analysis**: Calculate power generation potential from waterfalls and geothermal sources
    - **Carbon Impact Assessment**: Measure CO₂ emissions saved compared to fossil fuels
    - **AI-Powered Monitoring**: Real-time energy usage optimization with intelligent recommendations
    - **Time-Series Forecasting**: Predict seasonal energy output using LSTM neural networks
    - **Community Planning**: Tools for city planners and community leaders
    """)
    
    st.markdown("---")
    
    # Team Members Section
    st.subheader("👥 Meet Our Team")
    
    st.info("📸 Replace with your team member photos and information")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;'>
            <div style='width: 150px; height: 150px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; 
                        justify-content: center; color: white; font-size: 3em; font-weight: bold;'>
                TM1
            </div>
            <h4>Team Member 1</h4>
            <p style='color: #666;'>Role/Position</p>
            <p style='font-size: 0.9em;'>Brief description</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;'>
            <div style='width: 150px; height: 150px; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; 
                        justify-content: center; color: white; font-size: 3em; font-weight: bold;'>
                TM2
            </div>
            <h4>Team Member 2</h4>
            <p style='color: #666;'>Role/Position</p>
            <p style='font-size: 0.9em;'>Brief description</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;'>
            <div style='width: 150px; height: 150px; background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%); 
                        border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; 
                        justify-content: center; color: white; font-size: 3em; font-weight: bold;'>
                TM3
            </div>
            <h4>Team Member 3</h4>
            <p style='color: #666;'>Role/Position</p>
            <p style='font-size: 0.9em;'>Brief description</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;'>
            <div style='width: 150px; height: 150px; background: linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%); 
                        border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; 
                        justify-content: center; color: white; font-size: 3em; font-weight: bold;'>
                TM4
            </div>
            <h4>Team Member 4</h4>
            <p style='color: #666;'>Role/Position</p>
            <p style='font-size: 0.9em;'>Brief description</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features
    st.subheader("✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🔋 Energy Analysis
        - Waterfall hydroelectric potential calculation
        - Geothermal energy assessment
        - Waste energy recovery optimization
        - Multi-location grid planning
        
        #### 🌱 Environmental Impact
        - CO₂ emissions reduction tracking
        - Fossil fuel comparison analytics
        - Tree planting equivalency metrics
        - Long-term environmental forecasting
        """)
    
    with col2:
        st.markdown("""
        #### 🤖 AI-Powered Insights
        - Real-time energy monitoring
        - Anomaly detection system
        - Intelligent optimization recommendations
        - LSTM-based seasonal forecasting
        
        #### 📄 Comprehensive Reporting
        - Automated PDF data extraction
        - AI-generated impact reports
        - Export capabilities (CSV, JSON, Markdown)
        - City planner implementation guides
        """)

# ============================================================================
# TAB 2: ABOUT & EDUCATION
# ============================================================================
with tab2:
    st.header("📚 About & Education")
    
    st.info("📖 Add your educational content and tutorials here")
    
    st.markdown("""
    ### How to Use This Platform
    
    **Step 1: Data Input**
    - Manual entry with coordinates
    - PDF upload for automatic extraction
    - CSV batch processing for multiple locations
    
    **Step 2: Calculate Energy Potential**
    - Power generation capacity (MW)
    - Annual energy output (MWh)
    - Households that can be powered
    - Carbon emissions saved
    
    **Step 3: Analyze Results**
    - Interactive maps with detailed popups
    - Carbon impact comparison charts
    - Energy flow Sankey diagrams
    - Sensitivity analysis
    
    **Step 4: Generate Reports**
    - AI-powered comprehensive reports
    - Custom data exports (CSV/JSON)
    - Professional visualizations
    """)
    
    st.markdown("---")
    
    st.subheader("📸 Educational Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 80px 20px; background: #f0f2f6; border-radius: 10px; text-align: center; border: 2px dashed #999;'>
            <p style='color: #666; font-size: 1.3em; margin: 0;'>📷 Image Placeholder</p>
            <p style='color: #999; margin-top: 10px;'>Add system overview diagram</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 80px 20px; background: #f0f2f6; border-radius: 10px; text-align: center; border: 2px dashed #999;'>
            <p style='color: #666; font-size: 1.3em; margin: 0;'>📷 Image Placeholder</p>
            <p style='color: #999; margin-top: 10px;'>Add step-by-step guide</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🎓 Learning Resources")
    st.markdown("""
    - Video Tutorial 1: Platform Introduction
    - Video Tutorial 2: Energy Calculations
    - Video Tutorial 3: Reading Results
    - PDF Guide: Complete Manual
    
    *(Add your resources here)*
    """)

# ============================================================================
# TAB 3: DATA & CALCULATION - RUNS YOUR PAGE FILES
# ============================================================================
with tab3:
    st.header("📊 Data & Calculation")
    
    # Create sub-tabs
    calc_tabs = st.tabs([
        "📄 PDF Analyzer",
        "🧮 Geographic Calculator",
        "📈 Time-Series Predictor"
    ])
    
    # ========================================
    # PDF ANALYZER - runs 1_PDF_Analyzer.py
    # ========================================
    with calc_tabs[0]:
        st.markdown("---")
        run_page_file("pages/1_PDF_Analyzer.py", "pdf_analyzer")
    
    # ========================================
    # GEOGRAPHIC CALCULATOR - runs 2_Geographic_Calculator.py
    # ========================================
    with calc_tabs[1]:
        st.markdown("---")
        run_page_file("pages/2_Geographic_Calculator.py", "geographic_calculator")
    
    # ========================================
    # TIME-SERIES PREDICTOR - runs 3_Time_Series_Predictor.py
    # ========================================
    with calc_tabs[2]:
        st.markdown("---")
        run_page_file("pages/3_Time_Series_Predictor.py", "time_series_predictor")

# ============================================================================
# TAB 4: VERIFICATION UNIT (HARDWARE)
# ============================================================================
with tab4:
    st.header("🔌 Verification Unit - Hardware Integration")
    
    st.info("🛠️ Add your hardware documentation here")
    
    st.markdown("""
    ### Hardware Components
    
    #### 🔧 Physical Equipment
    - Energy meters and sensors
    - Data acquisition systems
    - IoT integration modules
    - Real-time monitoring dashboards
    
    #### 📡 Data Collection
    - Sensor specifications
    - Installation guidelines
    - Calibration procedures
    - Data transmission protocols
    
    #### 🔐 Verification & Validation
    - Accuracy testing procedures
    - Quality control measures
    - Certification standards
    - Compliance documentation
    """)
    
    st.markdown("---")
    
    st.subheader("Hardware Status Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='padding: 40px; background: #e8f5e9; border-radius: 10px; text-align: center; border: 2px solid #4caf50;'>
            <h2 style='color: #2e7d32; margin: 0;'>⚡</h2>
            <h4 style='margin: 10px 0;'>Sensor Status</h4>
            <p style='color: #4caf50; font-weight: bold; font-size: 1.2em; margin: 0;'>Online</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 40px; background: #e3f2fd; border-radius: 10px; text-align: center; border: 2px solid #2196f3;'>
            <h2 style='color: #1565c0; margin: 0;'>📡</h2>
            <h4 style='margin: 10px 0;'>Data Link</h4>
            <p style='color: #2196f3; font-weight: bold; font-size: 1.2em; margin: 0;'>Connected</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='padding: 40px; background: #fff3e0; border-radius: 10px; text-align: center; border: 2px solid #ff9800;'>
            <h2 style='color: #e65100; margin: 0;'>🔋</h2>
            <h4 style='margin: 10px 0;'>Power Supply</h4>
            <p style='color: #ff9800; font-weight: bold; font-size: 1.2em; margin: 0;'>Normal</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 5: HOUSEHOLD ENERGY STATUS - COMPLETE ENERGY MONITORING SYSTEM
# ============================================================================
with tab5:
    import matplotlib.pyplot as plt
    
    # ---------------- ENERGY RECORD ----------------
    class EnergyRecord:
        def __init__(self, usage, expected, sector, time_of_day, sunlight, temperature):
            self.usage = usage              # kWh
            self.expected = expected        # kWh
            self.sector = sector            # Home / Factory / Power Plant
            self.time_of_day = time_of_day  # Day / Night
            self.sunlight = sunlight        # Boolean
            self.temperature = temperature  # Celsius

    # ---------------- HISTORY MODULE ----------------
    class EnergyHistory:
        def __init__(self):
            self.records = []
            self.usage_log = []
            self.recovered_log = []
            self.remaining_log = []

        def add(self, record, recovered, remaining):
            self.records.append(record)
            self.usage_log.append(record.usage)
            self.recovered_log.append(recovered)
            self.remaining_log.append(remaining)

        def last_usage(self):
            if not self.records:
                return None
            return self.records[-1].usage

    # ---------------- ANALYTICS MODULE ----------------
    class EnergyAnalytics:

        @staticmethod
        def usage_ratio(record):
            if record.expected == 0:
                return 0
            return record.usage / record.expected

        @staticmethod
        def detect_anomaly(record, history):
            last = history.last_usage()
            if last is None:
                return False
            return record.usage > last * 1.25  # 25% spike

        @staticmethod
        def alert_level(ratio, anomaly):
            if ratio >= 1.35 or anomaly:
                return "CRITICAL"
            elif ratio >= 1.15:
                return "WARNING"
            return "NORMAL"

        @staticmethod
        def efficiency_score(ratio):
            score = 100 - abs(ratio - 1) * 75
            return round(max(0, min(100, score)), 1)

        @staticmethod
        def waste_recovery(record):
            wasted = 0.30 * record.usage
            recovered = 0.80 * wasted          # Always ON
            remaining = wasted - recovered     # System efficiency
            return round(recovered, 2), round(remaining, 2)

    # ---------------- AI DECISION ENGINE ----------------
    class KeenAI:
        def analyze(self, record, ratio, anomaly, alert, recovered):
            reasons = []
            actions = []
            confidence = 30

            reasons.append(f"Energy usage is {ratio:.2f}× expected")

            if anomaly:
                reasons.append("Sudden abnormal spike detected")
                confidence += 15

            if record.temperature > 30:
                reasons.append("High temperature increased cooling demand")
                confidence += 10

            if record.sunlight and record.time_of_day.lower() == "day":
                reasons.append("Sunlight available but underutilized")
                confidence += 15

            if record.sector.lower() in ["factory", "power plant"]:
                reasons.append("High recoverable industrial losses")
                confidence += 15

            # Continuous recovery (Second Line)
            actions.append(("HIGH", f"Recover wasted electricity continuously (~{recovered[0]} kWh)"))
            actions.append(("HIGH", f"Reserved for system stability (~{recovered[1]} kWh)"))

            # Null Line (only on anomaly)
            if anomaly:
                actions.append(("IMMEDIATE", "Activate Null Line to capture leakage"))

            if alert == "CRITICAL":
                actions.append(("IMMEDIATE", "Reduce non-essential loads"))
                actions.append(("HIGH", "Shift base load to geothermal / renewable"))
                if record.sunlight:
                    actions.append(("IMMEDIATE", "Activate Smart Daylight-Mirroring System"))

            elif alert == "WARNING":
                actions.append(("MEDIUM", "Optimize operating schedule"))

            else:
                actions.append(("LOW", "System operating optimally"))

            return reasons, actions, min(100, confidence)

    # ---------------- STREAMLIT APP ----------------
    st.title("⚡ EnergyGuard AI – Keen Edition V4")
    st.write("Monitor and optimize energy usage with AI-driven insights.")

    # Persist history between entries
    if "history" not in st.session_state:
        st.session_state.history = EnergyHistory()

    analytics = EnergyAnalytics()
    ai = KeenAI()

    # ---------------- INPUT FORM ----------------
    with st.form("energy_input"):
        st.subheader("Enter Energy Data")
        usage = st.number_input("Energy usage (kWh):", min_value=0.0, step=0.1)
        expected = st.number_input("Expected usage (kWh):", min_value=0.0, step=0.1)
        sector = st.selectbox("Sector:", ["Home", "Factory", "Power Plant"])
        time_of_day = st.selectbox("Time of Day:", ["Day", "Night"])
        sunlight = st.checkbox("Sunlight available?")
        temperature = st.number_input("Temperature (°C):", step=0.1)
        submitted = st.form_submit_button("Analyze Energy")

    if submitted:
        record = EnergyRecord(usage, expected, sector, time_of_day, sunlight, temperature)

        ratio = analytics.usage_ratio(record)
        anomaly = analytics.detect_anomaly(record, st.session_state.history)
        alert = analytics.alert_level(ratio, anomaly)
        score = analytics.efficiency_score(ratio)
        recovered = analytics.waste_recovery(record)

        st.session_state.history.add(record, recovered[0], recovered[1])

        # ---------------- DISPLAY ALERT ----------------
        st.subheader("🔔 Energy Status")
        if alert == "CRITICAL":
            st.error("🔴 CRITICAL – Immediate optimization required")
        elif alert == "WARNING":
            st.warning("🟡 WARNING – Efficiency dropping")
        else:
            st.success("🟢 NORMAL – System balanced")

        st.write(f"⚡ Efficiency Score: {score}/100")

        # ---------------- AI DIAGNOSIS ----------------
        reasons, actions, confidence = ai.analyze(record, ratio, anomaly, alert, recovered)

        st.subheader("🤖 AI Diagnosis")
        for r in reasons:
            st.write("•", r)

        st.subheader("🛠️ AI Action Plan")
        for level, act in actions:
            st.write(f"[{level}] {act}")

        st.write(f"AI Confidence Level: {confidence}%")

        # ---------------- PLOT ----------------
        if len(st.session_state.history.usage_log) >= 2:
            st.subheader("📈 Continuous Waste Recovery Performance")
            fig, ax = plt.subplots()
            ax.plot(st.session_state.history.usage_log, label="Total Usage (kWh)")
            ax.plot(st.session_state.history.recovered_log, label="Recovered Energy (kWh)")
            ax.plot(st.session_state.history.remaining_log, label="Unrecovered Waste (kWh)")
            ax.set_xlabel("Monitoring Step")
            ax.set_ylabel("Energy (kWh)")
            ax.set_title("Continuous Waste Recovery Performance")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <p><strong>EcoGrid - Community Energy Toolkit</strong></p>
    <p>Empowering communities with clean energy solutions</p>
    <p style='font-size: 0.9em;'>© 2024 EcoGrid Team | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
