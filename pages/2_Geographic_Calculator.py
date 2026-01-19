import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Geographic Calculator", layout="wide")

# Initialize session state
if 'geo_data' not in st.session_state:
    st.session_state.geo_data = {}
if 'pdf_extracted' not in st.session_state:
    st.session_state.pdf_extracted = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}

st.title("Geographic Energy Calculator")
st.markdown("*Map-based renewable energy potential analysis*")

# Sidebar: Input Method
st.sidebar.header("Location Input")
input_method = st.sidebar.radio(
    "Choose input method:",
    ["Manual Entry", "Click on Map", "Use PDF Data", "Batch Analysis (CSV)"]
)

# Main Content
tab1, tab2, tab3, tab4 = st.tabs(["Calculate", "Map View", "Analysis", "Export"])

# TAB 2: MAP VIEW (moved before Calculate tab to handle clicks first)
with tab2:
    st.header("Interactive Location Map")
    
    # Get current location for map center
    if st.session_state.geo_data:
        map_lat = st.session_state.geo_data.get('latitude', 23.8103)
        map_lng = st.session_state.geo_data.get('longitude', 90.4125)
    else:
        map_lat = 23.8103
        map_lng = 90.4125
    
    m = folium.Map(
        location=[map_lat, map_lng],
        zoom_start=8,
        tiles='OpenStreetMap'
    )
    
    if st.session_state.geo_data and 'location_name' in st.session_state.geo_data:
        location_name = st.session_state.geo_data.get('location_name', 'Selected Location')
        total_mw = st.session_state.geo_data.get('P_total_MW', 0)
        households = st.session_state.geo_data.get('households_total', 0)
        
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4>{location_name}</h4>
            <b>Total Power:</b> {total_mw:.2f} MW<br>
            <b>Households:</b> {households:,}<br>
            <b>Coordinates:</b><br>
            {map_lat:.4f}, {map_lng:.4f}
        </div>
        """
        
        if total_mw > 5:
            color = 'green'
        elif total_mw > 2:
            color = 'orange'
        else:
            color = 'red'
        
        folium.Marker(
            [map_lat, map_lng],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{location_name}: {total_mw:.2f} MW",
            icon=folium.Icon(color=color, icon='info-sign')
        ).add_to(m)
    
    st.markdown("**Click on the map to select a new location**")
    map_data = st_folium(m, width=700, height=500, key="main_map")
    
    # Handle map clicks
    if map_data and map_data.get('last_clicked'):
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lng = map_data['last_clicked']['lng']
        
        # Store clicked coordinates
        st.session_state.geo_data['clicked_lat'] = clicked_lat
        st.session_state.geo_data['clicked_lng'] = clicked_lng
        
        st.success(f"✅ New location selected: {clicked_lat:.4f}, {clicked_lng:.4f}")
        st.info("👈 Go to the 'Calculate' tab and select 'Click on Map' input method to use these coordinates!")

# TAB 1: CALCULATE
with tab1:
    st.header("Energy Potential Calculator")
    
    # Alert user if map coordinates are available but not being used
    if 'clicked_lat' in st.session_state.geo_data and 'clicked_lng' in st.session_state.geo_data:
        if input_method != "Click on Map":
            st.warning(f"📍 You have selected coordinates on the map ({st.session_state.geo_data['clicked_lat']:.4f}, {st.session_state.geo_data['clicked_lng']:.4f}). Change input method to 'Click on Map' in the sidebar to use them!")
    
    # Determine default values based on input method (only for initial setup)
    if input_method == "Use PDF Data" and st.session_state.pdf_extracted:
        st.success("📄 Using data from PDF Analyzer")
        
        # Pre-fill with PDF data
        initial_latitude = float(st.session_state.pdf_extracted.get('latitude', 23.8103))
        initial_longitude = float(st.session_state.pdf_extracted.get('longitude', 90.4125))
        initial_waterfall_height = float(st.session_state.pdf_extracted.get('waterfall_height', 0.0))
        initial_waterfall_flow = float(st.session_state.pdf_extracted.get('waterfall_flow', 0.0))
        initial_geo_temp = float(st.session_state.pdf_extracted.get('geo_temp', 0.0))
        initial_depth = float(st.session_state.pdf_extracted.get('depth', 3.0))
        initial_location_name = st.session_state.pdf_extracted.get('location_name', 'PDF Location')
        
    elif input_method == "Use PDF Data":
        st.warning("No PDF data available. Please use the PDF analyzer to upload and extract data first!")
        initial_latitude = 23.8103
        initial_longitude = 90.4125
        initial_waterfall_height = 0.0
        initial_waterfall_flow = 0.0
        initial_geo_temp = 0.0
        initial_depth = 3.0
        initial_location_name = "Default Location"
        
    elif input_method == "Click on Map":
        # Check if user has clicked on map
        if 'clicked_lat' in st.session_state.geo_data and 'clicked_lng' in st.session_state.geo_data:
            st.success(f"🗺️ Using map location: {st.session_state.geo_data['clicked_lat']:.4f}, {st.session_state.geo_data['clicked_lng']:.4f}")
            initial_latitude = float(st.session_state.geo_data['clicked_lat'])
            initial_longitude = float(st.session_state.geo_data['clicked_lng'])
        else:
            st.info("👉 Go to the 'Map View' tab to click on a location first!")
            initial_latitude = 23.8103
            initial_longitude = 90.4125
        
        initial_waterfall_height = 50.0
        initial_waterfall_flow = 10.0
        initial_geo_temp = 200.0
        initial_depth = 3.0
        initial_location_name = "Map Location"
        
    elif input_method == "Batch Analysis (CSV)":
        st.info("Upload CSV in the 'Export' tab for batch processing!")
        initial_latitude = 23.8103
        initial_longitude = 90.4125
        initial_waterfall_height = 50.0
        initial_waterfall_flow = 10.0
        initial_geo_temp = 200.0
        initial_depth = 3.0
        initial_location_name = "Batch Location"
        
    else:  # Manual Entry
        initial_latitude = 23.8103
        initial_longitude = 90.4125
        initial_waterfall_height = 50.0
        initial_waterfall_flow = 10.0
        initial_geo_temp = 200.0
        initial_depth = 3.0
        initial_location_name = "My Location"
    
    # Initialize form data in session state if not exists (use initial values only once)
    if 'form_latitude' not in st.session_state:
        st.session_state.form_latitude = initial_latitude
    if 'form_longitude' not in st.session_state:
        st.session_state.form_longitude = initial_longitude
    if 'form_waterfall_height' not in st.session_state:
        st.session_state.form_waterfall_height = initial_waterfall_height
    if 'form_waterfall_flow' not in st.session_state:
        st.session_state.form_waterfall_flow = initial_waterfall_flow
    if 'form_geo_temp' not in st.session_state:
        st.session_state.form_geo_temp = initial_geo_temp
    if 'form_depth' not in st.session_state:
        st.session_state.form_depth = initial_depth
    
    # Update ONLY coordinates when input method changes to "Click on Map"
    if input_method == "Click on Map" and 'clicked_lat' in st.session_state.geo_data:
        st.session_state.form_latitude = float(st.session_state.geo_data['clicked_lat'])
        st.session_state.form_longitude = float(st.session_state.geo_data['clicked_lng'])
    
    # Update ALL values when input method changes to "Use PDF Data"
    if input_method == "Use PDF Data" and st.session_state.pdf_extracted:
        st.session_state.form_latitude = initial_latitude
        st.session_state.form_longitude = initial_longitude
        st.session_state.form_waterfall_height = initial_waterfall_height
        st.session_state.form_waterfall_flow = initial_waterfall_flow
        st.session_state.form_geo_temp = initial_geo_temp
        st.session_state.form_depth = initial_depth
    
    # Input fields with session state
    location_name = st.text_input("Location Name", value=initial_location_name)
    
    col1, col2 = st.columns(2)
    
    with col1:
        latitude = st.number_input(
            "Latitude", 
            min_value=-90.0, 
            max_value=90.0, 
            value=st.session_state.form_latitude, 
            step=0.0001, 
            format="%.4f",
            key="latitude_input"
        )
        st.session_state.form_latitude = latitude
        
        waterfall_height = st.number_input(
            "Waterfall Height (m)", 
            min_value=0.0, 
            value=st.session_state.form_waterfall_height, 
            step=5.0,
            key="waterfall_height_input"
        )
        st.session_state.form_waterfall_height = waterfall_height
        
        geo_temp = st.number_input(
            "Geothermal Temperature (°C)", 
            min_value=0.0, 
            max_value=900.0, 
            value=st.session_state.form_geo_temp, 
            step=10.0,
            key="geo_temp_input"
        )
        st.session_state.form_geo_temp = geo_temp
    
    with col2:
        longitude = st.number_input(
            "Longitude", 
            min_value=-180.0, 
            max_value=180.0, 
            value=st.session_state.form_longitude, 
            step=0.0001, 
            format="%.4f",
            key="longitude_input"
        )
        st.session_state.form_longitude = longitude
        
        waterfall_flow = st.number_input(
            "Water Flow Rate (m³/s)", 
            min_value=0.0, 
            value=st.session_state.form_waterfall_flow, 
            step=0.5,
            key="waterfall_flow_input"
        )
        st.session_state.form_waterfall_flow = waterfall_flow
        
        depth = st.number_input(
            "Drilling Depth (km)", 
            min_value=0.5, 
            max_value=10.0, 
            value=st.session_state.form_depth, 
            step=0.5,
            key="depth_input"
        )
        st.session_state.form_depth = depth
    
    st.markdown("---")
    
    # Additional parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        turbine_efficiency = st.slider("Turbine Efficiency", 0.5, 0.95, 0.9, 0.01)
    with col2:
        geo_efficiency = st.slider("Geothermal Conversion Efficiency", 0.10, 0.25, 0.15, 0.01)
    with col3:
        capacity_factor = st.slider("Capacity Factor", 0.5, 0.95, 0.85, 0.01)
    
    # CALCULATIONS
    if st.button("Calculate Energy Potential", type="primary"):
        
        with st.spinner("Calculating..."):
            
            # Constants
            rho = 1000
            g = 9.81
            specific_heat = 4.18
            surface_temp = 25
            
            # WATERFALL CALCULATIONS
            if waterfall_height > 0 and waterfall_flow > 0:
                P_waterfall_watts = rho * g * waterfall_flow * waterfall_height * turbine_efficiency
                P_waterfall_MW = P_waterfall_watts / 1_000_000
                E_waterfall_year_MWh = P_waterfall_MW * 24 * 365
                households_waterfall = int(E_waterfall_year_MWh * 1000 / 7.2)
                has_waterfall = True
            else:
                P_waterfall_MW = 0
                E_waterfall_year_MWh = 0
                households_waterfall = 0
                has_waterfall = False
            
            # GEOTHERMAL CALCULATIONS
            if geo_temp > 50 and depth > 0:
                flow_rate_geo = 50.0
                temp_diff = geo_temp - surface_temp
                
                thermal_power_kW = flow_rate_geo * specific_heat * temp_diff
                P_geo_MW = (thermal_power_kW * geo_efficiency) / 1000
                E_geo_year_MWh = P_geo_MW * 24 * 365 * capacity_factor
                households_geo = int(E_geo_year_MWh * 1000 / 7.2)
                
                if geo_temp < 300:
                    pipe_material = "Stainless Steel / Incoloy"
                    relative_cost = 1.0
                elif geo_temp < 600:
                    pipe_material = "Inconel alloys / Nickel-chromium"
                    relative_cost = 2.5
                else:
                    pipe_material = "Ceramic composites / SiC / Titanium alloys"
                    relative_cost = 5.0
                
                has_geothermal = True
            else:
                P_geo_MW = 0
                E_geo_year_MWh = 0
                households_geo = 0
                pipe_material = "N/A"
                relative_cost = 0
                has_geothermal = False
            
            # WASTE ENERGY RECOVERY
            E_waste_recovered_MWh = (E_waterfall_year_MWh + E_geo_year_MWh) * 0.05
            households_waste = int(E_waste_recovered_MWh * 1000 / 7.2)
            
            # TOTALS
            P_total_MW = P_waterfall_MW + P_geo_MW
            E_total_year_MWh = E_waterfall_year_MWh + E_geo_year_MWh + E_waste_recovered_MWh
            households_total = int(E_total_year_MWh * 1000 / 7.2)
            
            # STORE IN SESSION STATE
            st.session_state.geo_data = {
                'location_name': location_name,
                'latitude': latitude,
                'longitude': longitude,
                'waterfall_height': waterfall_height,
                'waterfall_flow': waterfall_flow,
                'geo_temp': geo_temp,
                'depth': depth,
                'P_waterfall_MW': P_waterfall_MW,
                'P_geo_MW': P_geo_MW,
                'P_total_MW': P_total_MW,
                'E_waterfall_year_MWh': E_waterfall_year_MWh,
                'E_geo_year_MWh': E_geo_year_MWh,
                'E_waste_recovered_MWh': E_waste_recovered_MWh,
                'E_total_year_MWh': E_total_year_MWh,
                'households_total': households_total,
                'pipe_material': pipe_material,
                'has_waterfall': has_waterfall,
                'has_geothermal': has_geothermal
            }
            
            st.session_state.predictions['waterfall_mw'] = P_waterfall_MW
            st.session_state.predictions['geo_mw'] = P_geo_MW
            st.session_state.predictions['total_annual_mwh'] = E_total_year_MWh
            st.session_state.predictions['location'] = location_name
            
        # DISPLAY RESULTS
        st.success("Calculation Complete!")
        
        st.markdown("### Total System Output")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Power", f"{P_total_MW:.2f} MW")
        with col2:
            st.metric("Annual Energy", f"{E_total_year_MWh:,.0f} MWh")
        with col3:
            st.metric("Households Powered", f"{households_total:,}")
        with col4:
            revenue_estimate = E_total_year_MWh * 80
            st.metric("Est. Annual Revenue", f"${revenue_estimate:,.0f}")
        
        st.markdown("---")
        
        # Breakdown
        st.markdown("### Energy Source Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if has_waterfall or has_geothermal:
                labels = []
                values = []
                colors = []
                
                if has_waterfall:
                    labels.append('Waterfall')
                    values.append(E_waterfall_year_MWh)
                    colors.append('#1f77b4')
                
                if has_geothermal:
                    labels.append('Geothermal')
                    values.append(E_geo_year_MWh)
                    colors.append('#ff7f0e')
                
                if E_waste_recovered_MWh > 0:
                    labels.append('Waste Recovery')
                    values.append(E_waste_recovered_MWh)
                    colors.append('#2ca02c')
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    marker=dict(colors=colors),
                    hole=0.3
                )])
                fig_pie.update_layout(title="Energy Generation Mix")
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            sources = []
            power_values = []
            
            if has_waterfall:
                sources.append('Waterfall')
                power_values.append(P_waterfall_MW)
            
            if has_geothermal:
                sources.append('Geothermal')
                power_values.append(P_geo_MW)
            
            if E_waste_recovered_MWh > 0:
                sources.append('Waste Recovery')
                power_values.append(E_waste_recovered_MWh / (24 * 365))
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=sources,
                y=power_values,
                name='Power (MW)',
                marker_color='lightblue'
            ))
            fig_bar.update_layout(
                title="Power Output by Source",
                yaxis_title="Power (MW)",
                xaxis_title="Energy Source"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with st.expander("Detailed Calculations"):
            if has_waterfall:
                st.markdown("#### Waterfall Turbine System")
                st.write(f"- Flow Rate: {waterfall_flow} m³/s")
                st.write(f"- Height: {waterfall_height} m")
                st.write(f"- Efficiency: {turbine_efficiency*100}%")
                st.write(f"- **Power Output: {P_waterfall_MW:.2f} MW**")
                st.write(f"- **Annual Energy: {E_waterfall_year_MWh:,.0f} MWh**")
                st.write(f"- **Households: {households_waterfall:,}**")
                st.markdown("---")
            
            if has_geothermal:
                st.markdown("#### Geothermal System")
                st.write(f"- Depth: {depth} km")
                st.write(f"- Underground Temperature: {geo_temp}°C")
                st.write(f"- Temperature Differential: {geo_temp - surface_temp}°C")
                st.write(f"- Conversion Efficiency: {geo_efficiency*100}%")
                st.write(f"- Capacity Factor: {capacity_factor*100}%")
                st.write(f"- **Power Output: {P_geo_MW:.2f} MW**")
                st.write(f"- **Annual Energy: {E_geo_year_MWh:,.0f} MWh**")
                st.write(f"- **Households: {households_geo:,}**")
                st.write(f"- **Recommended Pipe Material:** {pipe_material}")
                st.write(f"- **Relative Cost Factor:** {relative_cost}x")
                st.markdown("---")
            
            if E_waste_recovered_MWh > 0:
                st.markdown("#### Waste Energy Recovery")
                st.write(f"- Estimated Recovery Rate: 5% of total generation")
                st.write(f"- **Recovered Energy: {E_waste_recovered_MWh:,.0f} MWh/year**")
                st.write(f"- **Additional Households: {households_waste:,}**")
        
        st.success("Data saved and sent to Time-Series Predictor")

# TAB 3: ANALYSIS
with tab3:
    st.header("Geographic Energy Analysis")
    
    if st.session_state.geo_data and 'P_total_MW' in st.session_state.geo_data:
        
        st.subheader("Optimal Placement Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.geo_data.get('has_waterfall'):
                st.success("Waterfall Turbine System")
                st.write("**Recommended Installation:**")
                st.write("- Install turbines at the base of waterfall")
                st.write("- Use adjustable blade systems for flow variation")
                st.write("- Implement AI-controlled flow monitoring")
                st.write("- Add modular blade replacement capability")
                
                height = st.session_state.geo_data.get('waterfall_height', 0)
                if height > 100:
                    st.warning("Very high waterfall - consider multiple turbine stages")
                elif height < 20:
                    st.info("Low head turbine recommended (Kaplan or Francis type)")
            else:
                st.info("No waterfall data - not applicable for this location")
        
        with col2:
            if st.session_state.geo_data.get('has_geothermal'):
                st.success("Geothermal System")
                st.write("**Recommended Installation:**")
                st.write(f"- Drill to {st.session_state.geo_data.get('depth', 0)} km depth")
                st.write(f"- Use {st.session_state.geo_data.get('pipe_material', 'N/A')}")
                st.write("- Implement closed-loop heat exchanger")
                st.write("- Add AI monitoring for pipe stress & temperature")
                
                temp = st.session_state.geo_data.get('geo_temp', 0)
                if temp > 300:
                    st.warning("High temperature - enhanced safety protocols required")
                if temp < 150:
                    st.info("Consider binary cycle system for low-temp geothermal")
            else:
                st.info("No geothermal data - not applicable for this location")
        
        st.markdown("---")
        
        st.subheader("Sensitivity Analysis")
        
        sensitivity_param = st.selectbox(
            "Select parameter to analyze:",
            ["Waterfall Flow Rate", "Waterfall Height", "Geothermal Temperature", "Drilling Depth"]
        )
        
        if sensitivity_param == "Waterfall Flow Rate":
            base_flow = st.session_state.geo_data.get('waterfall_flow', 10)
            base_height = st.session_state.geo_data.get('waterfall_height', 50)
            
            flow_range = np.linspace(base_flow * 0.5, base_flow * 1.5, 50)
            power_range = [1000 * 9.81 * f * base_height * 0.9 / 1_000_000 for f in flow_range]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=flow_range,
                y=power_range,
                mode='lines',
                name='Power Output',
                line=dict(color='blue', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[base_flow],
                y=[st.session_state.geo_data.get('P_waterfall_MW', 0)],
                mode='markers',
                name='Current Setup',
                marker=dict(size=15, color='red')
            ))
            fig.update_layout(
                title="Power Output vs Flow Rate",
                xaxis_title="Flow Rate (m³/s)",
                yaxis_title="Power (MW)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif sensitivity_param == "Waterfall Height":
            base_flow = st.session_state.geo_data.get('waterfall_flow', 10)
            base_height = st.session_state.geo_data.get('waterfall_height', 50)
            
            height_range = np.linspace(base_height * 0.5, base_height * 1.5, 50)
            power_range = [1000 * 9.81 * base_flow * h * 0.9 / 1_000_000 for h in height_range]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=height_range,
                y=power_range,
                mode='lines',
                name='Power Output',
                line=dict(color='green', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[base_height],
                y=[st.session_state.geo_data.get('P_waterfall_MW', 0)],
                mode='markers',
                name='Current Setup',
                marker=dict(size=15, color='red')
            ))
            fig.update_layout(
                title="Power Output vs Waterfall Height",
                xaxis_title="Height (m)",
                yaxis_title="Power (MW)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif sensitivity_param == "Geothermal Temperature":
            base_temp = st.session_state.geo_data.get('geo_temp', 200)
            
            temp_range = np.linspace(150, 400, 50)
            power_range = [(50 * 4.18 * (t - 25) * 0.15) / 1000 for t in temp_range]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=temp_range,
                y=power_range,
                mode='lines',
                name='Power Output',
                line=dict(color='orange', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[base_temp],
                y=[st.session_state.geo_data.get('P_geo_MW', 0)],
                mode='markers',
                name='Current Setup',
                marker=dict(size=15, color='red')
            ))
            fig.update_layout(
                title="Power Output vs Underground Temperature",
                xaxis_title="Temperature (°C)",
                yaxis_title="Power (MW)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        else:
            base_depth = st.session_state.geo_data.get('depth', 3.0)
            base_temp = st.session_state.geo_data.get('geo_temp', 200)
            
            surface_temp = 25
            gradient = (base_temp - surface_temp) / base_depth
            
            depth_range = np.linspace(1, 10, 50)
            temp_at_depth = [surface_temp + gradient * d for d in depth_range]
            power_range = [(50 * 4.18 * (t - surface_temp) * 0.15) / 1000 for t in temp_at_depth]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=depth_range,
                y=power_range,
                mode='lines',
                name='Power Output',
                line=dict(color='purple', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[base_depth],
                y=[st.session_state.geo_data.get('P_geo_MW', 0)],
                mode='markers',
                name='Current Setup',
                marker=dict(size=15, color='red')
            ))
            fig.update_layout(
                title="Power Output vs Drilling Depth",
                xaxis_title="Depth (km)",
                yaxis_title="Power (MW)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Comparison with Other Renewable Sources")
        
        total_mwh = st.session_state.geo_data.get('E_total_year_MWh', 0)
        
        solar_equiv_capacity = total_mwh / (8760 * 0.20)
        wind_equiv_capacity = total_mwh / (8760 * 0.35)
        
        comparison_df = pd.DataFrame({
            'Source': ['Your System', 'Equivalent Solar', 'Equivalent Wind'],
            'Capacity (MW)': [
                st.session_state.geo_data.get('P_total_MW', 0),
                solar_equiv_capacity,
                wind_equiv_capacity
            ],
            'Capacity Factor': ['85%', '20%', '35%'],
            'Annual MWh': [total_mwh, total_mwh, total_mwh]
        })
        
        st.dataframe(comparison_df, use_container_width=True)
        
        st.info("""
        **Why your system is better:**
        - Higher capacity factor (85% vs 20-35%)
        - More predictable output (not weather dependent)
        - Smaller land footprint
        - Lower intermittency
        """)
        
    else:
        st.warning("No calculation data available. Please go to the 'Calculate' tab first!")

# TAB 4: EXPORT
with tab4:
    st.header("Export & Batch Analysis")
    
    if st.session_state.geo_data and 'location_name' in st.session_state.geo_data:
        st.subheader("Download Current Calculation")
        
        export_data = {
            'Location Name': [st.session_state.geo_data.get('location_name', 'N/A')],
            'Latitude': [st.session_state.geo_data.get('latitude', 0)],
            'Longitude': [st.session_state.geo_data.get('longitude', 0)],
            'Waterfall Power (MW)': [st.session_state.geo_data.get('P_waterfall_MW', 0)],
            'Geothermal Power (MW)': [st.session_state.geo_data.get('P_geo_MW', 0)],
            'Total Power (MW)': [st.session_state.geo_data.get('P_total_MW', 0)],
            'Annual Energy (MWh)': [st.session_state.geo_data.get('E_total_year_MWh', 0)],
            'Households Powered': [st.session_state.geo_data.get('households_total', 0)],
            'Pipe Material': [st.session_state.geo_data.get('pipe_material', 'N/A')]
        }
        
        export_df = pd.DataFrame(export_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f"energy_calc_{st.session_state.geo_data.get('location_name', 'location').replace(' ', '_')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_str = export_df.to_json(orient='records', indent=2)
            st.download_button(
                label="Download as JSON",
                data=json_str,
                file_name=f"energy_calc_{st.session_state.geo_data.get('location_name', 'location').replace(' ', '_')}.json",
                mime="application/json"
            )
    
    st.markdown("---")
    
    st.subheader("Batch Analysis from CSV")
    
    st.markdown("""
    Upload a CSV file with multiple locations to analyze them all at once.
    
    **Required CSV format:**
    ```
    location_name,latitude,longitude,waterfall_height_m,waterfall_flow_m3s,geo_temp_c,depth_km
    Location 1,23.8103,90.4125,50,10,200,3.0
    Location 2,24.8949,91.8687,30,12,150,2.5
    ```
    """)
    
    sample_data = {
        'location_name': ['Chittagong Hills', 'Sylhet Valley', 'Khulna Region'],
        'latitude': [22.3569, 24.8949, 22.8456],
        'longitude': [91.7832, 91.8687, 89.5403],
        'waterfall_height_m': [45, 30, 0],
        'waterfall_flow_m3s': [8.5, 12.0, 0],
        'geo_temp_c': [180, 150, 200],
        'depth_km': [2.8, 2.5, 3.5]
    }
    sample_df = pd.DataFrame(sample_data)
    
    st.download_button(
        label="Download Sample CSV Template",
        data=sample_df.to_csv(index=False),
        file_name="sample_locations_template.csv",
        mime="text/csv"
    )
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            st.write("### Uploaded Data Preview")
            st.dataframe(batch_df.head(), use_container_width=True)
            
            if st.button("Process All Locations", type="primary"):
                
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, row in batch_df.iterrows():
                    status_text.text(f"Processing {row.get('location_name', f'Location {idx+1}')}...")
                    
                    lat = row.get('latitude', 0)
                    lng = row.get('longitude', 0)
                    h = row.get('waterfall_height_m', 0)
                    q = row.get('waterfall_flow_m3s', 0)
                    temp = row.get('geo_temp_c', 0)
                    depth = row.get('depth_km', 3.0)
                    
                    if h > 0 and q > 0:
                        p_waterfall = (1000 * 9.81 * q * h * 0.9) / 1_000_000
                        e_waterfall = p_waterfall * 24 * 365
                    else:
                        p_waterfall = 0
                        e_waterfall = 0
                    
                    if temp > 50:
                        p_geo = (50 * 4.18 * (temp - 25) * 0.15) / 1000
                        e_geo = p_geo * 24 * 365 * 0.85
                    else:
                        p_geo = 0
                        e_geo = 0
                    
                    e_waste = (e_waterfall + e_geo) * 0.05
                    total_annual = e_waterfall + e_geo + e_waste
                    households = int(total_annual * 1000 / 7.2)
                    
                    if temp < 300:
                        material = "Stainless Steel"
                    elif temp < 600:
                        material = "Inconel alloys"
                    else:
                        material = "Ceramic composites"
                    
                    results.append({
                        'Location': row.get('location_name', f'Location {idx+1}'),
                        'Latitude': lat,
                        'Longitude': lng,
                        'Waterfall_MW': round(p_waterfall, 2),
                        'Geothermal_MW': round(p_geo, 2),
                        'Total_Annual_MWh': round(total_annual, 0),
                        'Households': households,
                        'Pipe_Material': material if temp > 50 else 'N/A'
                    })
                    
                    progress_bar.progress((idx + 1) / len(batch_df))
                
                status_text.text("Processing complete!")
                
                results_df = pd.DataFrame(results)
                st.write("### Batch Analysis Results")
                st.dataframe(results_df, use_container_width=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Locations", len(results_df))
                with col2:
                    total_power = results_df['Waterfall_MW'].sum() + results_df['Geothermal_MW'].sum()
                    st.metric("Combined Power", f"{total_power:.2f} MW")
                with col3:
                    total_households = results_df['Households'].sum()
                    st.metric("Total Households", f"{total_households:,}")
                
                fig = px.scatter_mapbox(
                    results_df,
                    lat='Latitude',
                    lon='Longitude',
                    size='Total_Annual_MWh',
                    color='Total_Annual_MWh',
                    hover_name='Location',
                    hover_data=['Households', 'Waterfall_MW', 'Geothermal_MW'],
                    color_continuous_scale='Viridis',
                    size_max=20,
                    zoom=5
                )
                
                fig.update_layout(
                    mapbox_style="open-street-map",
                    title="Energy Potential Map - All Locations"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.download_button(
                    label="Download Batch Results",
                    data=results_df.to_csv(index=False),
                    file_name="batch_energy_analysis_results.csv",
                    mime="text/csv"
                )
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.info("Please make sure your CSV has the correct column names and format.")

st.markdown("---")
st.markdown("Community Energy Toolkit")
st.caption("Data ready for Time-Series Prediction and Energy Monitor")