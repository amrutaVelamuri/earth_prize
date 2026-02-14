import streamlit as st

st.set_page_config(page_title="EcoGrid Toolkit", layout="wide", page_icon="🌱")

# Initialize ALL session state variables
if 'geo_data' not in st.session_state:
    st.session_state.geo_data = {}
if 'pdf_extracted' not in st.session_state:
    st.session_state.pdf_extracted = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}
if 'linked_locations' not in st.session_state:
    st.session_state.linked_locations = []

st.title("🌱 EcoGrid Toolkit")
st.markdown("### Clean energy analysis & carbon impact assessment platform")

st.markdown("""
This toolkit helps communities calculate renewable energy potential and measure environmental impact:
- **Waterfall turbines** - Hydroelectric power generation
- **Geothermal systems** - Underground heat extraction
- **Waste energy recovery** - Continuous efficiency optimization
- **Carbon impact analysis** - Compare with fossil fuel emissions
- **Multi-location grid** - Link locations for distributed generation
""")

st.sidebar.success("Select a tool above")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("**Step 1: Upload Documents**")
    st.markdown("Go to **PDF Analyzer** to upload technical documents.")
with col2:
    st.success("**Step 2: Calculate Potential**")
    st.markdown("Go to **Geographic Calculator** to analyze energy & carbon savings.")
with col3:
    st.warning("**Step 3: Predict Future**")
    st.markdown("Use **Time-Series Predictor** to forecast seasonal output.")
with col4:
    st.error("**Step 4: Compare Impact**")
    st.markdown("View carbon emissions saved vs fossil fuel generation.")

st.markdown("---")
st.subheader("Current Data Status")

col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.pdf_extracted:
        st.success("✅ PDF Data Loaded")
        st.write(f"- Flow: {st.session_state.pdf_extracted.get('waterfall_flow', 0)} m³/s")
        st.write(f"- Height: {st.session_state.pdf_extracted.get('waterfall_height', 0)} m")
        st.write(f"- Temp: {st.session_state.pdf_extracted.get('geo_temp', 0)}°C")
        st.write(f"- Depth: {st.session_state.pdf_extracted.get('depth', 0)} km")
    else:
        st.info("No PDF data yet")
        st.caption("Upload document in PDF Analyzer")

with col2:
    if st.session_state.geo_data and 'P_total_MW' in st.session_state.geo_data:
        st.success("✅ Analysis Complete")
        st.write(f"- Power: {st.session_state.geo_data.get('P_total_MW', 0):.2f} MW")
        st.write(f"- Energy: {st.session_state.geo_data.get('E_total_year_MWh', 0):,.0f} MWh")
        st.write(f"- Households: {st.session_state.geo_data.get('households_total', 0):,}")
        if 'carbon_saved_tons' in st.session_state.geo_data:
            st.write(f"- CO₂ Saved: {st.session_state.geo_data.get('carbon_saved_tons', 0):,.0f} tons/yr")
    else:
        st.info("No calculations yet")
        st.caption("Run Geographic Calculator")

with col3:
    if st.session_state.predictions and 'total_annual_mwh' in st.session_state.predictions:
        st.success("✅ Predictions Generated")
        st.write(f"- Forecast: {st.session_state.predictions.get('total_annual_mwh', 0):,.0f} MWh")
    else:
        st.info("No predictions yet")
        st.caption("Run Time-Series Predictor")

st.markdown("---")

if st.session_state.linked_locations:
    st.subheader("🔗 Linked Location Network")
    total_power = sum([loc.get('P_total_MW', 0) for loc in st.session_state.linked_locations])
    total_energy = sum([loc.get('E_total_year_MWh', 0) for loc in st.session_state.linked_locations])
    total_households = sum([loc.get('households_total', 0) for loc in st.session_state.linked_locations])
    total_carbon_saved = sum([loc.get('carbon_saved_tons', 0) for loc in st.session_state.linked_locations])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Locations", len(st.session_state.linked_locations))
    with col2:
        st.metric("Combined Power", f"{total_power:.2f} MW")
    with col3:
        st.metric("Total Households", f"{total_households:,}")
    with col4:
        st.metric("Total CO₂ Saved", f"{total_carbon_saved:,.0f} tons/yr")
    
    with st.expander("View Linked Locations"):
        for i, loc in enumerate(st.session_state.linked_locations):
            st.write(f"{i+1}. **{loc.get('location_name', 'Unknown')}** - {loc.get('P_total_MW', 0):.2f} MW - {loc.get('carbon_saved_tons', 0):,.0f} tons CO₂/yr")
    st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Clear All Data"):
        st.session_state.geo_data = {}
        st.session_state.pdf_extracted = {}
        st.session_state.predictions = {}
        st.session_state.linked_locations = []
        st.rerun()

with col2:
    if st.session_state.linked_locations:
        if st.button("🔗 Clear Linked Locations"):
            st.session_state.linked_locations = []
            st.rerun()

st.markdown("---")
st.markdown("**EcoGrid Toolkit** - Open-Source Clean Energy Platform")
st.caption("Built for sustainable community development and climate action") 
