import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px

# Carbon Emission Factors (Bangladesh specific - Source: BPDB & IEA)
CARBON_FACTORS = {
    'coal': 1.05,
    'natural_gas': 0.45,
    'diesel': 0.78,
    'furnace_oil': 0.85,
    'grid_average_bangladesh': 0.62
}

OTHER_EMISSIONS = {
    'SO2': 2.8,
    'NOx': 1.9,
    'PM2.5': 0.15,
    'CH4': 0.03,
    'mercury': 0.00001
}

st.set_page_config(page_title="Geographic Calculator - EcoGrid", layout="wide", page_icon="🌍")

# Initialize session state
if 'geo_data' not in st.session_state:
    st.session_state.geo_data = {}
if 'pdf_extracted' not in st.session_state:
    st.session_state.pdf_extracted = {}
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}
if 'linked_locations' not in st.session_state:
    st.session_state.linked_locations = []

st.title("🌍 Geographic Energy Calculator")
st.markdown("*Map-based renewable energy potential & carbon impact analysis*")

# Sidebar: Input Method
st.sidebar.header("Location Input")
input_method = st.sidebar.radio(
    "Choose input method:",
    ["Manual Entry", "Click on Map", "Use PDF Data", "Batch Analysis (CSV)"]
)

# Main Content
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Calculate", 
    "Map View", 
    "Carbon Impact",
    "Energy Flow",
    "Analysis", 
    "Export"
])

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
        carbon_saved = st.session_state.geo_data.get('carbon_saved_tons', 0)
        
        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4>{location_name}</h4>
            <b>Total Power:</b> {total_mw:.2f} MW<br>
            <b>Households:</b> {households:,}<br>
            <b>CO₂ Saved:</b> {carbon_saved:,.0f} tons/year<br>
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
    
    # Add linked location markers
    if st.session_state.linked_locations:
        for loc in st.session_state.linked_locations:
            loc_lat = loc.get('latitude', 0)
            loc_lng = loc.get('longitude', 0)
            loc_name = loc.get('location_name', 'Linked Location')
            loc_mw = loc.get('P_total_MW', 0)
            loc_carbon = loc.get('carbon_saved_tons', 0)
            
            popup_html = f"""
            <div style="font-family: Arial; width: 200px;">
                <h4>🔗 {loc_name}</h4>
                <b>Power:</b> {loc_mw:.2f} MW<br>
                <b>CO₂ Saved:</b> {loc_carbon:,.0f} tons/year
            </div>
            """
            
            folium.Marker(
                [loc_lat, loc_lng],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"🔗 {loc_name}",
                icon=folium.Icon(color='blue', icon='link', prefix='fa')
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
        
        st.success(f"New location selected: {clicked_lat:.4f}, {clicked_lng:.4f}")
        st.info("Go to the 'Calculate' tab and select 'Click on Map' input method to use these coordinates.")

# TAB 1: CALCULATE
with tab1:
    st.header("Energy Potential Calculator")
    
    # Alert user if map coordinates are available but not being used
    if 'clicked_lat' in st.session_state.geo_data and 'clicked_lng' in st.session_state.geo_data:
        if input_method != "Click on Map":
            st.warning(f"Map coordinates available: {st.session_state.geo_data['clicked_lat']:.4f}, {st.session_state.geo_data['clicked_lng']:.4f}. Change input method to 'Click on Map' in the sidebar to use them.")
    
    # Determine default values based on input method
    if input_method == "Use PDF Data" and st.session_state.pdf_extracted:
        st.success("Using data from PDF Analyzer")
        
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
        if 'clicked_lat' in st.session_state.geo_data and 'clicked_lng' in st.session_state.geo_data:
            st.success(f"Using map location: {st.session_state.geo_data['clicked_lat']:.4f}, {st.session_state.geo_data['clicked_lng']:.4f}")
            initial_latitude = float(st.session_state.geo_data['clicked_lat'])
            initial_longitude = float(st.session_state.geo_data['clicked_lng'])
        else:
            st.info("Go to the 'Map View' tab to click on a location first.")
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
    
    # Initialize form data in session state if not exists
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
    
    # Update coordinates when input method changes to "Click on Map"
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
    
    # Input fields
    location_name = st.text_input("Location Name", value=initial_location_name, help="Enter a descriptive name for this location")
    
    if not location_name or location_name.strip() == "":
        st.caption("Warning: Location name is required")
    
    col1, col2 = st.columns(2)
    
    with col1:
        latitude = st.number_input(
            "Latitude", 
            min_value=-90.0, 
            max_value=90.0, 
            value=st.session_state.form_latitude, 
            step=0.0001, 
            format="%.4f",
            key="latitude_input",
            help="Valid range: -90 to +90 (South to North)"
        )
        st.session_state.form_latitude = latitude
        
        waterfall_height = st.number_input(
            "Waterfall Height (m)", 
            min_value=0.0, 
            value=st.session_state.form_waterfall_height, 
            step=5.0,
            key="waterfall_height_input",
            help="Height of waterfall in meters. Leave at 0 if no waterfall."
        )
        st.session_state.form_waterfall_height = waterfall_height
        
        if waterfall_height > 500:
            st.caption("Warning: Very high waterfall - please verify")
        
        geo_temp = st.number_input(
            "Geothermal Temperature (°C)", 
            min_value=0.0, 
            max_value=900.0, 
            value=st.session_state.form_geo_temp, 
            step=10.0,
            key="geo_temp_input",
            help="Underground temperature in Celsius. Minimum 50°C for viable generation."
        )
        st.session_state.form_geo_temp = geo_temp
        
        if geo_temp > 0 and geo_temp < 50:
            st.caption("Warning: Temperature too low for efficient energy generation")
        elif geo_temp > 600:
            st.caption("Warning: Extremely high temperature - specialized equipment required")
    
    with col2:
        longitude = st.number_input(
            "Longitude", 
            min_value=-180.0, 
            max_value=180.0, 
            value=st.session_state.form_longitude, 
            step=0.0001, 
            format="%.4f",
            key="longitude_input",
            help="Valid range: -180 to +180 (West to East)"
        )
        st.session_state.form_longitude = longitude
        
        waterfall_flow = st.number_input(
            "Water Flow Rate (m³/s)", 
            min_value=0.0, 
            value=st.session_state.form_waterfall_flow, 
            step=0.5,
            key="waterfall_flow_input",
            help="Water flow in cubic meters per second. Leave at 0 if no waterfall."
        )
        st.session_state.form_waterfall_flow = waterfall_flow
        
        if waterfall_flow > 1000:
            st.caption("Warning: Very high flow rate - please verify")
        
        depth = st.number_input(
            "Drilling Depth (km)", 
            min_value=0.5, 
            max_value=10.0, 
            value=st.session_state.form_depth, 
            step=0.5,
            key="depth_input",
            help="Geothermal drilling depth in kilometers. Typical range: 1-5 km"
        )
        st.session_state.form_depth = depth
        
        if depth > 7:
            st.caption("Warning: Very deep drilling - higher costs expected")
    
    # Real-time validation summary
    st.markdown("---")
    
    validation_summary = []
    if waterfall_height > 0 or waterfall_flow > 0:
        if waterfall_height > 0 and waterfall_flow > 0:
            validation_summary.append("VALID: Waterfall data complete")
        else:
            validation_summary.append("WARNING: Waterfall data incomplete (need both height and flow)")
    
    if geo_temp >= 50:
        validation_summary.append("VALID: Geothermal data viable")
    elif geo_temp > 0:
        validation_summary.append("WARNING: Geothermal temperature too low")
    
    if not validation_summary:
        st.info("No energy source data entered yet")
    else:
        for summary in validation_summary:
            if summary.startswith("VALID"):
                st.success(summary)
            else:
                st.warning(summary)
    
    st.markdown("---")
    
    # Additional parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        turbine_efficiency = st.slider("Turbine Efficiency", 0.5, 0.95, 0.9, 0.01)
    with col2:
        geo_efficiency = st.slider("Geothermal Conversion Efficiency", 0.10, 0.25, 0.15, 0.01)
    with col3:
        capacity_factor = st.slider("Capacity Factor", 0.5, 0.95, 0.85, 0.01)
    
    # CALCULATIONS WITH VALIDATION
    if st.button("Calculate Energy Potential & Carbon Impact", type="primary"):
        
        # INPUT VALIDATION
        validation_errors = []
        
        if not location_name or location_name.strip() == "":
            validation_errors.append("ERROR: Location name cannot be empty")
        
        if latitude == 0 and longitude == 0:
            validation_errors.append("WARNING: Coordinates are at (0, 0). Please verify this is correct.")
        
        if waterfall_height > 0 and waterfall_flow == 0:
            validation_errors.append("ERROR: Waterfall height is set but flow rate is 0. Both must be greater than 0 for waterfall calculations.")
        
        if waterfall_flow > 0 and waterfall_height == 0:
            validation_errors.append("ERROR: Flow rate is set but waterfall height is 0. Both must be greater than 0 for waterfall calculations.")
        
        if waterfall_height > 500:
            validation_errors.append("WARNING: Waterfall height exceeds 500m. This is extremely high - please verify.")
        
        if waterfall_flow > 1000:
            validation_errors.append("WARNING: Flow rate exceeds 1000 m³/s. This is extremely high - please verify.")
        
        if geo_temp > 0 and geo_temp < 50:
            validation_errors.append("WARNING: Geothermal temperature below 50°C is too low for efficient energy generation.")
        
        if geo_temp > 600:
            validation_errors.append("WARNING: Temperature exceeds 600°C. This requires specialized equipment and safety measures.")
        
        if depth > 10:
            validation_errors.append("WARNING: Drilling depth exceeds 10 km. This is beyond typical geothermal project limits.")
        
        if depth < 1 and geo_temp > 100:
            validation_errors.append("WARNING: High temperature at shallow depth is unusual. Please verify data.")
        
        if waterfall_height == 0 and waterfall_flow == 0 and (geo_temp == 0 or geo_temp < 50):
            validation_errors.append("ERROR: No viable energy source detected. Please enter either waterfall data or geothermal data (temp > 50°C).")
        
        # Display validation errors/warnings
        if validation_errors:
            st.error("### Validation Issues Found:")
            for error in validation_errors:
                if error.startswith("ERROR"):
                    st.error(error)
                else:
                    st.warning(error)
            
            critical_errors = [e for e in validation_errors if e.startswith("ERROR")]
            if critical_errors:
                st.error("**Cannot proceed with calculation. Please fix the errors above.**")
                st.stop()
            else:
                if not st.checkbox("I acknowledge the warnings above and want to proceed with calculation"):
                    st.stop()
        
        with st.spinner("Calculating energy potential and environmental impact..."):
            
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
            
            # WASTE ENERGY RECOVERY (Continuous Second Line - Always ON)
            base_waste_sources = 0
            
            if has_waterfall:
                waterfall_waste = E_waterfall_year_MWh * 1000 * 0.30
                base_waste_sources += waterfall_waste
            
            if has_geothermal:
                geothermal_waste = E_geo_year_MWh * 1000 * 0.30
                base_waste_sources += geothermal_waste
            
            waste_recovered_kWh = base_waste_sources * 0.80
            waste_remaining_kWh = base_waste_sources * 0.20
            
            E_waste_recovered_MWh = waste_recovered_kWh / 1000
            E_waste_remaining_MWh = waste_remaining_kWh / 1000
            
            households_waste = int(E_waste_recovered_MWh * 1000 / 7.2)
            
            # TOTALS
            P_total_MW = P_waterfall_MW + P_geo_MW
            E_total_year_MWh = E_waterfall_year_MWh + E_geo_year_MWh + E_waste_recovered_MWh
            households_total = int(E_total_year_MWh * 1000 / 7.2)
            
            # CARBON EMISSIONS CALCULATIONS
            carbon_factor = CARBON_FACTORS['grid_average_bangladesh']
            carbon_saved_tons = E_total_year_MWh * carbon_factor
            
            SO2_saved = E_total_year_MWh * OTHER_EMISSIONS['SO2']
            NOx_saved = E_total_year_MWh * OTHER_EMISSIONS['NOx']
            PM25_saved = E_total_year_MWh * OTHER_EMISSIONS['PM2.5']
            CH4_saved = E_total_year_MWh * OTHER_EMISSIONS['CH4']
            mercury_saved = E_total_year_MWh * OTHER_EMISSIONS['mercury']
            
            trees_equivalent = int(carbon_saved_tons * 16.5)
            cars_off_road = int(carbon_saved_tons / 4.6)
            coal_avoided_tons = carbon_saved_tons / CARBON_FACTORS['coal']
            gas_avoided_tons = carbon_saved_tons / CARBON_FACTORS['natural_gas']
            
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
                'E_waste_remaining_MWh': E_waste_remaining_MWh,
                'base_waste_sources': base_waste_sources / 1000,
                'E_total_year_MWh': E_total_year_MWh,
                'households_total': households_total,
                'pipe_material': pipe_material,
                'has_waterfall': has_waterfall,
                'has_geothermal': has_geothermal,
                'carbon_saved_tons': carbon_saved_tons,
                'SO2_saved_kg': SO2_saved,
                'NOx_saved_kg': NOx_saved,
                'PM25_saved_kg': PM25_saved,
                'CH4_saved_kg': CH4_saved,
                'mercury_saved_kg': mercury_saved,
                'trees_equivalent': trees_equivalent,
                'cars_off_road': cars_off_road,
                'coal_avoided_tons': coal_avoided_tons,
                'gas_avoided_tons': gas_avoided_tons
            }
            
            st.session_state.predictions['waterfall_mw'] = P_waterfall_MW
            st.session_state.predictions['geo_mw'] = P_geo_MW
            st.session_state.predictions['total_annual_mwh'] = E_total_year_MWh
            st.session_state.predictions['location'] = location_name
        
        # DISPLAY RESULTS
        st.success("✅ Calculation Complete!")
        
        st.markdown("### Total System Output")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Power", f"{P_total_MW:.2f} MW")
        with col2:
            st.metric("Annual Energy", f"{E_total_year_MWh:,.0f} MWh")
        with col3:
            st.metric("Households Powered", f"{households_total:,}")
        with col4:
            st.metric("CO₂ Saved", f"{carbon_saved_tons:,.0f} tons/year", 
                     delta="vs fossil fuel", delta_color="normal")
        
        st.markdown("---")
        
        # Environmental Impact Summary
        st.markdown("### 🌱 Environmental Impact vs Fossil Fuel Generation")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Trees Equivalent", f"{trees_equivalent:,}", 
                     help="Number of trees needed to absorb this CO₂")
        with col2:
            st.metric("Cars Off Road", f"{cars_off_road:,}", 
                     help="Equivalent to removing this many cars from roads")
        with col3:
            st.metric("Coal Avoided", f"{coal_avoided_tons:,.0f} MWh", 
                     help="Equivalent coal generation avoided")
        with col4:
            st.metric("Gas Avoided", f"{gas_avoided_tons:,.0f} MWh", 
                     help="Equivalent natural gas generation avoided")
        
        st.markdown("---")
        
        # Breakdown
        st.markdown("### Energy Source Breakdown")
        
        st.info("**Waste Recovery System:** Operates continuously and independently from main generation systems, capturing 80% of thermal and mechanical losses.")
        
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
        
        st.markdown("---")
        
        # Add to Linked Locations button
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔗 Add to Linked Locations Network"):
                already_linked = any(
                    loc.get('location_name') == st.session_state.geo_data.get('location_name')
                    for loc in st.session_state.linked_locations
                )
                
                if already_linked:
                    st.warning("This location is already in the linked network!")
                else:
                    st.session_state.linked_locations.append(st.session_state.geo_data.copy())
                    st.success(f"✅ Added '{st.session_state.geo_data.get('location_name')}' to linked network!")
                    st.info(f"Total linked locations: {len(st.session_state.linked_locations)}")
        
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
                st.markdown("#### Continuous Waste Energy Recovery (Second Line)")
                st.write("**System Type:** Always-ON independent recovery")
                st.write(f"- **Total Waste Available:** {base_waste_sources / 1000:,.2f} MWh/year (30% of main output)")
                st.write(f"- **Recovery Efficiency:** 80% continuous capture")
                st.write(f"- **Recovered Energy:** {E_waste_recovered_MWh:,.2f} MWh/year")
                st.write(f"- **System Reserve:** {E_waste_remaining_MWh:,.2f} MWh/year (20% for stability)")
                st.write(f"- **Additional Households Powered:** {households_waste:,}")
                st.info("**Note:** This recovery system operates continuously and independently, capturing waste heat, friction losses, and mechanical inefficiencies from the primary generation systems.")
        
        st.success("Data saved and sent to Time-Series Predictor")
# PART 2 - Continue from Part 1
# This contains: TAB 3 (Carbon Impact), TAB 4 (Energy Flow), TAB 5 (Analysis), TAB 6 (Export)

# TAB 3: CARBON IMPACT
with tab3:
    st.header("🌍 Carbon & Environmental Impact Analysis")
    
    if st.session_state.geo_data and 'carbon_saved_tons' in st.session_state.geo_data:
        
        carbon_saved = st.session_state.geo_data['carbon_saved_tons']
        energy_mwh = st.session_state.geo_data['E_total_year_MWh']
        
        st.markdown(f"### Location: {st.session_state.geo_data.get('location_name')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ♻️ Your Renewable System")
            st.success(f"**{energy_mwh:,.0f} MWh/year**")
            st.success(f"**0 tons CO₂** emissions")
            st.success("**Clean & Sustainable**")
        
        with col2:
            st.markdown("#### ⚫ Equivalent Fossil Fuel System")
            st.error(f"**{energy_mwh:,.0f} MWh/year**")
            st.error(f"**{carbon_saved:,.0f} tons CO₂** emissions")
            st.error("**Polluting & Harmful**")
        
        st.markdown("---")
        st.markdown("### Harmful Emissions Avoided (per year)")
        
        emissions_df = pd.DataFrame({
            'Pollutant': ['CO₂', 'SO₂', 'NOx', 'PM2.5', 'CH₄', 'Mercury'],
            'Amount Avoided': [
                f"{st.session_state.geo_data['carbon_saved_tons']:,.0f} tons",
                f"{st.session_state.geo_data['SO2_saved_kg']:,.1f} kg",
                f"{st.session_state.geo_data['NOx_saved_kg']:,.1f} kg",
                f"{st.session_state.geo_data['PM25_saved_kg']:,.2f} kg",
                f"{st.session_state.geo_data['CH4_saved_kg']:,.2f} kg",
                f"{st.session_state.geo_data['mercury_saved_kg']*1000:,.3f} g"
            ],
            'Health Impact': [
                'Climate change, global warming',
                'Acid rain, respiratory diseases',
                'Smog, lung damage',
                'Heart disease, premature death',
                'Greenhouse gas (25x worse than CO₂)',
                'Neurotoxin, brain damage'
            ]
        })
        
        st.dataframe(emissions_df, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("### Visual Impact Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fuel_comparison = pd.DataFrame({
                'Fuel Type': ['Your System', 'Coal', 'Natural Gas', 'Diesel', 'Furnace Oil'],
                'CO₂ Emissions (tons)': [
                    0,
                    energy_mwh * CARBON_FACTORS['coal'],
                    energy_mwh * CARBON_FACTORS['natural_gas'],
                    energy_mwh * CARBON_FACTORS['diesel'],
                    energy_mwh * CARBON_FACTORS['furnace_oil']
                ]
            })
            
            fig = px.bar(
                fuel_comparison, 
                x='Fuel Type', 
                y='CO₂ Emissions (tons)',
                title='CO₂ Emissions Comparison by Fuel Type',
                color='Fuel Type',
                color_discrete_map={
                    'Your System': 'green',
                    'Coal': 'black',
                    'Natural Gas': 'orange',
                    'Diesel': 'red',
                    'Furnace Oil': 'darkred'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            equivalencies = pd.DataFrame({
                'Equivalent': ['Trees Planted', 'Cars Removed', 'Homes Powered'],
                'Amount': [
                    st.session_state.geo_data['trees_equivalent'],
                    st.session_state.geo_data['cars_off_road'],
                    st.session_state.geo_data['households_total']
                ]
            })
            
            fig2 = px.bar(
                equivalencies,
                x='Equivalent',
                y='Amount',
                title='Environmental Impact Equivalencies',
                color='Equivalent',
                color_discrete_sequence=['green', 'blue', 'purple']
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📊 20-Year Environmental Impact Projection")
        
        years = list(range(1, 21))
        cumulative_co2 = [carbon_saved * year for year in years]
        cumulative_trees = [st.session_state.geo_data['trees_equivalent'] * year for year in years]
        
        from plotly.subplots import make_subplots
        
        fig_projection = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Cumulative CO₂ Saved', 'Equivalent Trees Planted')
        )
        
        fig_projection.add_trace(
            go.Scatter(x=years, y=cumulative_co2, mode='lines+markers', 
                      name='CO₂ Saved', line=dict(color='green', width=3)),
            row=1, col=1
        )
        
        fig_projection.add_trace(
            go.Scatter(x=years, y=cumulative_trees, mode='lines+markers',
                      name='Trees Equivalent', line=dict(color='darkgreen', width=3)),
            row=1, col=2
        )
        
        fig_projection.update_xaxes(title_text="Years", row=1, col=1)
        fig_projection.update_xaxes(title_text="Years", row=1, col=2)
        fig_projection.update_yaxes(title_text="CO₂ (tons)", row=1, col=1)
        fig_projection.update_yaxes(title_text="Trees", row=1, col=2)
        fig_projection.update_layout(height=400, showlegend=False)
        
        st.plotly_chart(fig_projection, use_container_width=True)
        
        st.success(f"**Over 20 years:** {cumulative_co2[-1]:,.0f} tons CO₂ saved = {cumulative_trees[-1]:,} trees planted!")
        
    else:
        st.warning("No calculation data available. Please run calculations in the 'Calculate' tab first!")

# TAB 4: ENERGY FLOW DIAGRAM
with tab4:
    st.header("⚡ Energy Flow Visualization")
    
    if st.session_state.geo_data and 'P_total_MW' in st.session_state.geo_data:
        
        st.markdown(f"### System: {st.session_state.geo_data.get('location_name')}")
        
        waterfall_mwh = st.session_state.geo_data.get('E_waterfall_year_MWh', 0)
        geo_mwh = st.session_state.geo_data.get('E_geo_year_MWh', 0)
        waste_recovered = st.session_state.geo_data.get('E_waste_recovered_MWh', 0)
        total_mwh = st.session_state.geo_data.get('E_total_year_MWh', 0)
        
        # Calculate waste
        waste_from_waterfall = waterfall_mwh * 0.30 if waterfall_mwh > 0 else 0
        waste_from_geo = geo_mwh * 0.30 if geo_mwh > 0 else 0
        total_waste = waste_from_waterfall + waste_from_geo
        waste_lost = total_waste * 0.20
        
        # Sankey diagram nodes
        nodes = ['Waterfall Turbine', 'Geothermal System', 'Primary Energy', 'Waste Heat', 
                'Recovery System', 'Grid Output', 'Lost Heat']
        
        # Sankey diagram links
        links = {
            'source': [],
            'target': [],
            'value': [],
            'label': []
        }
        
        if waterfall_mwh > 0:
            links['source'].append(0)
            links['target'].append(2)
            links['value'].append(waterfall_mwh)
            links['label'].append(f'{waterfall_mwh:,.0f} MWh')
            
            links['source'].append(0)
            links['target'].append(3)
            links['value'].append(waste_from_waterfall)
            links['label'].append(f'{waste_from_waterfall:,.0f} MWh waste')
        
        if geo_mwh > 0:
            links['source'].append(1)
            links['target'].append(2)
            links['value'].append(geo_mwh)
            links['label'].append(f'{geo_mwh:,.0f} MWh')
            
            links['source'].append(1)
            links['target'].append(3)
            links['value'].append(waste_from_geo)
            links['label'].append(f'{waste_from_geo:,.0f} MWh waste')
        
        if total_waste > 0:
            links['source'].append(3)
            links['target'].append(4)
            links['value'].append(waste_recovered)
            links['label'].append(f'{waste_recovered:,.0f} MWh recovered')
            
            links['source'].append(3)
            links['target'].append(6)
            links['value'].append(waste_lost)
            links['label'].append(f'{waste_lost:,.0f} MWh lost')
        
        # Primary to grid
        primary_total = waterfall_mwh + geo_mwh
        if primary_total > 0:
            links['source'].append(2)
            links['target'].append(5)
            links['value'].append(primary_total)
            links['label'].append(f'{primary_total:,.0f} MWh')
        
        # Recovery to grid
        if waste_recovered > 0:
            links['source'].append(4)
            links['target'].append(5)
            links['value'].append(waste_recovered)
            links['label'].append(f'{waste_recovered:,.0f} MWh')
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
                color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#17becf', '#8c564b']
            ),
            link=dict(
                source=links['source'],
                target=links['target'],
                value=links['value'],
                label=links['label']
            )
        )])
        
        fig.update_layout(
            title=f"Energy Flow Diagram - {st.session_state.geo_data.get('location_name')}",
            font_size=12,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### System Efficiency Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            primary_efficiency = (primary_total / (primary_total + total_waste)) * 100 if (primary_total + total_waste) > 0 else 0
            st.metric("Primary System Efficiency", f"{primary_efficiency:.1f}%")
        
        with col2:
            recovery_efficiency = (waste_recovered / total_waste) * 100 if total_waste > 0 else 0
            st.metric("Waste Recovery Efficiency", f"{recovery_efficiency:.1f}%")
        
        with col3:
            overall_efficiency = (total_mwh / (primary_total + total_waste)) * 100 if (primary_total + total_waste) > 0 else 0
            st.metric("Overall System Efficiency", f"{overall_efficiency:.1f}%")
        
        st.markdown("---")
        st.markdown("### Energy Component Breakdown")
        
        component_data = []
        
        if waterfall_mwh > 0:
            component_data.append({
                'Component': 'Waterfall Turbine',
                'Energy (MWh)': waterfall_mwh,
                'Percentage': (waterfall_mwh / total_mwh * 100) if total_mwh > 0 else 0,
                'Status': '✅ Active'
            })
        
        if geo_mwh > 0:
            component_data.append({
                'Component': 'Geothermal System',
                'Energy (MWh)': geo_mwh,
                'Percentage': (geo_mwh / total_mwh * 100) if total_mwh > 0 else 0,
                'Status': '✅ Active'
            })
        
        if waste_recovered > 0:
            component_data.append({
                'Component': 'Waste Recovery',
                'Energy (MWh)': waste_recovered,
                'Percentage': (waste_recovered / total_mwh * 100) if total_mwh > 0 else 0,
                'Status': '♻️ Continuous'
            })
        
        component_df = pd.DataFrame(component_data)
        st.dataframe(component_df, use_container_width=True)
        
    else:
        st.warning("No calculation data available. Please run calculations in the 'Calculate' tab first!")

# TAB 5: ANALYSIS
with tab5:
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

# TAB 6: EXPORT
with tab6:
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
            'CO₂ Saved (tons/year)': [st.session_state.geo_data.get('carbon_saved_tons', 0)],
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
                file_name=f"ecogrid_{st.session_state.geo_data.get('location_name', 'location').replace(' ', '_')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_str = export_df.to_json(orient='records', indent=2)
            st.download_button(
                label="Download as JSON",
                data=json_str,
                file_name=f"ecogrid_{st.session_state.geo_data.get('location_name', 'location').replace(' ', '_')}.json",
                mime="application/json"
            )
    
    # Linked locations export
    if st.session_state.linked_locations:
        st.markdown("---")
        st.subheader("🔗 Linked Location Network Export")
        
        network_data = []
        for loc in st.session_state.linked_locations:
            network_data.append({
                'Location': loc.get('location_name'),
                'Latitude': loc.get('latitude'),
                'Longitude': loc.get('longitude'),
                'Power (MW)': loc.get('P_total_MW'),
                'Energy (MWh/year)': loc.get('E_total_year_MWh'),
                'CO₂ Saved (tons)': loc.get('carbon_saved_tons'),
                'Households': loc.get('households_total')
            })
        
        network_df = pd.DataFrame(network_data)
        st.dataframe(network_df, use_container_width=True)
        
        # Network totals
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Locations", len(st.session_state.linked_locations))
        with col2:
            total_power = sum([loc.get('P_total_MW', 0) for loc in st.session_state.linked_locations])
            st.metric("Combined Power", f"{total_power:.2f} MW")
        with col3:
            total_carbon = sum([loc.get('carbon_saved_tons', 0) for loc in st.session_state.linked_locations])
            st.metric("Total CO₂ Saved", f"{total_carbon:,.0f} tons")
        with col4:
            total_households = sum([loc.get('households_total', 0) for loc in st.session_state.linked_locations])
            st.metric("Total Households", f"{total_households:,}")
        
        csv_network = network_df.to_csv(index=False)
        st.download_button(
            label="Download Linked Network Data",
            data=csv_network,
            file_name="ecogrid_linked_network.csv",
            mime="text/csv"
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
                        waterfall_waste = e_waterfall * 1000 * 0.30
                    else:
                        p_waterfall = 0
                        e_waterfall = 0
                        waterfall_waste = 0
                    
                    if temp > 50:
                        p_geo = (50 * 4.18 * (temp - 25) * 0.15) / 1000
                        e_geo = p_geo * 24 * 365 * 0.85
                        geothermal_waste = e_geo * 1000 * 0.30
                    else:
                        p_geo = 0
                        e_geo = 0
                        geothermal_waste = 0
                    
                    # Waste recovery
                    total_waste = waterfall_waste + geothermal_waste
                    e_waste_recovered = (total_waste * 0.80) / 1000
                    
                    total_annual = e_waterfall + e_geo + e_waste_recovered
                    households = int(total_annual * 1000 / 7.2)
                    
                    # Carbon calculations
                    carbon_saved = total_annual * CARBON_FACTORS['grid_average_bangladesh']
                    
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
                        'CO2_Saved_tons': round(carbon_saved, 0),
                        'Households': households,
                        'Pipe_Material': material if temp > 50 else 'N/A'
                    })
                    
                    progress_bar.progress((idx + 1) / len(batch_df))
                
                status_text.text("Processing complete!")
                
                results_df = pd.DataFrame(results)
                st.write("### Batch Analysis Results")
                st.dataframe(results_df, use_container_width=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Locations", len(results_df))
                with col2:
                    total_power = results_df['Waterfall_MW'].sum() + results_df['Geothermal_MW'].sum()
                    st.metric("Combined Power", f"{total_power:.2f} MW")
                with col3:
                    total_carbon = results_df['CO2_Saved_tons'].sum()
                    st.metric("Total CO₂ Saved", f"{total_carbon:,.0f} tons/yr")
                with col4:
                    total_households = results_df['Households'].sum()
                    st.metric("Total Households", f"{total_households:,}")
                
                fig = px.scatter_mapbox(
                    results_df,
                    lat='Latitude',
                    lon='Longitude',
                    size='Total_Annual_MWh',
                    color='Total_Annual_MWh',
                    hover_name='Location',
                    hover_data=['Households', 'Waterfall_MW', 'Geothermal_MW', 'CO2_Saved_tons'],
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
st.markdown("**EcoGrid Toolkit** - Geographic Calculator")
st.caption("Renewable energy analysis with environmental impact assessment")
