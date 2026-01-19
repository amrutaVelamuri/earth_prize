import streamlit as st

st.set_page_config(page_title="Energy Toolkit", layout="wide")

# Initialize ALL session state variables at the top
if 'geo_data' not in st.session_state:
    st.session_state.geo_data = {}
if 'pdf_extracted' not in st.session_state:
    st.session_state.pdf_extracted = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}

st.title("Community Energy Toolkit")
st.markdown("### Open-source renewable energy analysis platform")

st.markdown("""
This toolkit helps communities calculate and predict renewable energy potential from:
- Waterfall turbines
- Geothermal systems
- Waste energy recovery
""")

st.sidebar.success("Select a tool above")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**Step 1: Upload Documents**")
    st.markdown("Go to **PDF Analyzer** to upload technical documents and extract data automatically.")

with col2:
    st.success("**Step 2: Calculate Potential**")
    st.markdown("Go to **Geographic Calculator** to analyze energy potential for your location.")

with col3:
    st.warning("**Step 3: Predict Future**")
    st.markdown("Time-Series Predictor (coming soon) will forecast seasonal energy output.")

st.markdown("---")
st.subheader("Current Data Status")

col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.pdf_extracted:
        st.success("PDF Data Loaded")
        st.write(f"- Waterfall Flow: {st.session_state.pdf_extracted.get('waterfall_flow', 0)} m³/s")
        st.write(f"- Waterfall Height: {st.session_state.pdf_extracted.get('waterfall_height', 0)} m")
        st.write(f"- Geo Temp: {st.session_state.pdf_extracted.get('geo_temp', 0)}°C")
        st.write(f"- Depth: {st.session_state.pdf_extracted.get('depth', 0)} km")
    else:
        st.info("No PDF data yet")
        st.caption("Upload a document in PDF Analyzer")

with col2:
    if st.session_state.geo_data and 'P_total_MW' in st.session_state.geo_data:
        st.success("Geographic Analysis Complete")
        st.write(f"- Total Power: {st.session_state.geo_data.get('P_total_MW', 0):.2f} MW")
        st.write(f"- Annual Energy: {st.session_state.geo_data.get('E_total_year_MWh', 0):,.0f} MWh")
        st.write(f"- Households: {st.session_state.geo_data.get('households_total', 0):,}")
    else:
        st.info("No calculations yet")
        st.caption("Run calculations in Geographic Calculator")

with col3:
    if st.session_state.predictions and 'total_annual_mwh' in st.session_state.predictions:
        st.success("Predictions Generated")
        st.write(f"- Predicted Output: {st.session_state.predictions.get('total_annual_mwh', 0):,.0f} MWh")
    else:
        st.info("No predictions yet")
        st.caption("Time-Series Predictor coming soon")

st.markdown("---")

if st.button("Clear All Data"):
    st.session_state.geo_data = {}
    st.session_state.pdf_extracted = {}
    st.session_state.predictions = {}
    st.rerun()

st.markdown("---")
st.markdown("Open-Source Community Energy Toolkit")
st.caption("Built for sustainable community development")