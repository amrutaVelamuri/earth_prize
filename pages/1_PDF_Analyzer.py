import streamlit as st
import pandas as pd
import re
from io import BytesIO
try:
    import PyPDF2
except ImportError:
    st.error("PyPDF2 not installed. Run: pip install PyPDF2")

st.set_page_config(page_title="PDF Analyzer", layout="wide")

if 'pdf_extracted' not in st.session_state:
    st.session_state.pdf_extracted = {}
if 'geo_data' not in st.session_state:
    st.session_state.geo_data = {}

st.title("Document Analyzer")
st.markdown("*Automatic extraction of energy data from technical documents*")

st.markdown("""
### Upload Technical Documents
This tool automatically extracts:
- Geographic coordinates (latitude, longitude)
- Waterfall specifications (height, flow rate)
- Geothermal data (temperature, drilling depth)
- Material specifications
- Energy calculations
""")

uploaded_file = st.file_uploader("Upload PDF Document", type=['pdf'])

if uploaded_file is not None:
    
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text() + "\n"
        
        st.success(f"PDF loaded successfully! {len(pdf_reader.pages)} pages extracted.")
        
        with st.expander("View Extracted Text"):
            st.text_area("Raw Text", full_text, height=300)
        
        st.markdown("---")
        st.subheader("Extracted Data")
        
        extracted_data = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Waterfall Data")
            
            # IMPROVED FLOW RATE PATTERNS - much more flexible
            flow_patterns = [
                r'[Ff]low\s*[Rr]ate[:\s]*(\d+\.?\d*)\s*m[³3]/s',
                r'[Ww]ater\s*[Ff]low\s*[Rr]ate[:\s]*(\d+\.?\d*)\s*m[³3]/s',
                r'Q\s*=\s*(\d+\.?\d*)\s*m[³3]/s',
                r'[Ff]low[:\s]*(\d+\.?\d*)\s*m[³3]/s',
                r'(\d+\.?\d*)\s*m[³3]/s',
            ]
            
            waterfall_flow = 0
            for pattern in flow_patterns:
                flow_matches = re.findall(pattern, full_text)
                if flow_matches:
                    waterfall_flow = float(flow_matches[0])
                    extracted_data['waterfall_flow'] = waterfall_flow
                    st.metric("Flow Rate", f"{waterfall_flow} m³/s")
                    break
            
            if waterfall_flow == 0:
                st.info("No flow rate found")
                extracted_data['waterfall_flow'] = 0
            
            # IMPROVED HEIGHT PATTERNS
            height_patterns = [
                r'[Ww]aterfall\s*[Hh]eight[:\s]*(\d+\.?\d*)\s*m',
                r'[Hh]eight[:\s]*(\d+\.?\d*)\s*m',
                r'H\s*=\s*(\d+\.?\d*)\s*m',
                r'[Hh]ead[:\s]*(\d+\.?\d*)\s*m',
            ]
            
            waterfall_height = 0
            for pattern in height_patterns:
                height_matches = re.findall(pattern, full_text)
                if height_matches:
                    waterfall_height = float(height_matches[0])
                    extracted_data['waterfall_height'] = waterfall_height
                    st.metric("Height", f"{waterfall_height} m")
                    break
            
            if waterfall_height == 0:
                st.info("No height found")
                extracted_data['waterfall_height'] = 0
            
            efficiency_matches = re.findall(r'η\s*=\s*(\d+\.?\d*)', full_text)
            if efficiency_matches:
                efficiency = float(efficiency_matches[0])
                st.metric("Turbine Efficiency", f"{efficiency}")
            
            power_matches = re.findall(r'(\d+\.?\d*)\s*MW', full_text)
            if power_matches:
                st.info(f"Document mentions: {power_matches[0]} MW power output")
        
        with col2:
            st.markdown("### Geothermal Data")
            
            # IMPROVED TEMPERATURE PATTERNS
            temp_range_matches = re.findall(r'(\d+)\s*[-–]\s*(\d+)\s*°C', full_text)
            temp_single_matches = re.findall(r'[Tt]emperature[:\s]*(\d+)\s*°C', full_text)
            
            if temp_range_matches:
                temp_range = temp_range_matches[0]
                avg_temp = (int(temp_range[0]) + int(temp_range[1])) / 2
                extracted_data['geo_temp'] = avg_temp
                st.metric("Temperature Range", f"{temp_range[0]}-{temp_range[1]}°C")
                st.info(f"Using average: {avg_temp}°C")
            elif temp_single_matches:
                avg_temp = float(temp_single_matches[0])
                extracted_data['geo_temp'] = avg_temp
                st.metric("Temperature", f"{avg_temp}°C")
            else:
                st.info("No temperature found")
                extracted_data['geo_temp'] = 0
            
            # IMPROVED DEPTH PATTERNS
            depth_range_matches = re.findall(r'(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)\s*km', full_text)
            depth_single_matches = re.findall(r'[Dd]epth[:\s]*(\d+\.?\d*)\s*km', full_text)
            depth_drilling_matches = re.findall(r'[Dd]rilling\s*[Dd]epth[:\s]*(\d+\.?\d*)\s*km', full_text)
            
            if depth_drilling_matches:
                avg_depth = float(depth_drilling_matches[0])
                extracted_data['depth'] = avg_depth
                st.metric("Drilling Depth", f"{avg_depth} km")
            elif depth_range_matches:
                depth_range = depth_range_matches[0]
                avg_depth = (float(depth_range[0]) + float(depth_range[1])) / 2
                extracted_data['depth'] = avg_depth
                st.metric("Drilling Depth Range", f"{depth_range[0]}-{depth_range[1]} km")
                st.info(f"Using average: {avg_depth} km")
            elif depth_single_matches:
                avg_depth = float(depth_single_matches[0])
                extracted_data['depth'] = avg_depth
                st.metric("Depth", f"{avg_depth} km")
            else:
                st.info("No drilling depth found")
                extracted_data['depth'] = 3.0
        
        st.markdown("---")
        st.subheader("Materials Identified")
        
        materials_found = []
        material_patterns = [
            r'Stainless Steel',
            r'Inconel',
            r'Ceramic composites',
            r'SiC',
            r'[Tt]itanium alloys',
            r'Incoloy'
        ]
        
        for pattern in material_patterns:
            if re.search(pattern, full_text, re.IGNORECASE):
                materials_found.append(pattern)
        
        if materials_found:
            st.success(f"Materials mentioned: {', '.join(materials_found)}")
        
        st.markdown("---")
        st.subheader("Location Data")
        
        # IMPROVED COORDINATE PATTERNS
        lat_patterns = [
            r'[Ll]atitude[:\s]*(\d+\.?\d*)',
            r'[Ll]at[:\s]*(\d+\.?\d*)',
        ]
        
        lon_patterns = [
            r'[Ll]ongitude[:\s]*(\d+\.?\d*)',
            r'[Ll]on[:\s]*(\d+\.?\d*)',
        ]
        
        default_lat = 23.8103
        default_lon = 90.4125
        coords_found = False
        
        for pattern in lat_patterns:
            lat_match = re.search(pattern, full_text)
            if lat_match:
                default_lat = float(lat_match.group(1))
                coords_found = True
                break
        
        for pattern in lon_patterns:
            lon_match = re.search(pattern, full_text)
            if lon_match:
                default_lon = float(lon_match.group(1))
                coords_found = True
                break
        
        if coords_found:
            st.success(f"Coordinates detected: {default_lat}, {default_lon}")
        else:
            st.info("Coordinates not auto-detected. Using default Bangladesh location.")
        
        # Validate extracted coordinates
        if coords_found:
            if default_lat < -90 or default_lat > 90:
                st.error(f"ERROR: Invalid latitude {default_lat}. Must be between -90 and 90.")
                default_lat = 23.8103
            if default_lon < -180 or default_lon > 180:
                st.error(f"ERROR: Invalid longitude {default_lon}. Must be between -180 and 180.")
                default_lon = 90.4125
        
        location_name = st.text_input("Location Name", value="Extracted Location")
        
        if not location_name or location_name.strip() == "":
            st.caption("Warning: Location name is required")
        
        extracted_data['location_name'] = location_name
        
        col1, col2 = st.columns(2)
        with col1:
            lat_input = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=default_lat, step=0.0001, format="%.4f", help="Valid range: -90 to +90")
            extracted_data['latitude'] = lat_input
        with col2:
            lng_input = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=default_lon, step=0.0001, format="%.4f", help="Valid range: -180 to +180")
            extracted_data['longitude'] = lng_input
        
        # Validation Summary
        st.markdown("---")
        st.subheader("Data Validation Summary")
        
        validation_messages = []
        
        # Validate waterfall data
        if waterfall_flow > 0 and waterfall_height > 0:
            validation_messages.append(("VALID", "Waterfall data complete"))
        elif waterfall_flow > 0 or waterfall_height > 0:
            validation_messages.append(("WARNING", "Incomplete waterfall data - both height and flow required"))
        
        if waterfall_height > 500:
            validation_messages.append(("WARNING", f"Waterfall height ({waterfall_height}m) is extremely high - verify accuracy"))
        
        if waterfall_flow > 1000:
            validation_messages.append(("WARNING", f"Flow rate ({waterfall_flow} m³/s) is extremely high - verify accuracy"))
        
        # Validate geothermal data
        if extracted_data.get('geo_temp', 0) >= 50:
            validation_messages.append(("VALID", "Geothermal temperature viable for generation"))
        elif extracted_data.get('geo_temp', 0) > 0:
            validation_messages.append(("WARNING", f"Geothermal temperature ({extracted_data.get('geo_temp')}°C) below 50°C - too low for efficient generation"))
        
        if extracted_data.get('geo_temp', 0) > 600:
            validation_messages.append(("WARNING", f"Temperature ({extracted_data.get('geo_temp')}°C) exceeds 600°C - requires specialized equipment"))
        
        if extracted_data.get('depth', 0) > 7:
            validation_messages.append(("WARNING", f"Drilling depth ({extracted_data.get('depth')} km) is very deep - expect high costs"))
        
        # Check for at least one viable energy source
        has_waterfall = waterfall_flow > 0 and waterfall_height > 0
        has_geothermal = extracted_data.get('geo_temp', 0) >= 50
        
        if not has_waterfall and not has_geothermal:
            validation_messages.append(("ERROR", "No viable energy source detected in document"))
        
        # Display validation messages
        if validation_messages:
            for msg_type, msg in validation_messages:
                if msg_type == "VALID":
                    st.success(msg)
                elif msg_type == "WARNING":
                    st.warning(msg)
                elif msg_type == "ERROR":
                    st.error(msg)
        else:
            st.info("No data extracted from document")
        
        st.markdown("---")
        
        if st.button("Send Data to Geographic Calculator", type="primary"):
            # Final validation before sending
            validation_errors = []
            
            if not extracted_data.get('location_name') or extracted_data.get('location_name', '').strip() == "":
                validation_errors.append("ERROR: Location name is required")
            
            has_waterfall = extracted_data.get('waterfall_flow', 0) > 0 and extracted_data.get('waterfall_height', 0) > 0
            has_geothermal = extracted_data.get('geo_temp', 0) >= 50
            
            if not has_waterfall and not has_geothermal:
                validation_errors.append("ERROR: No viable energy source. Document must contain either waterfall data or geothermal data with temperature ≥ 50°C")
            
            # Check for mismatched waterfall data
            if (extracted_data.get('waterfall_flow', 0) > 0 and extracted_data.get('waterfall_height', 0) == 0) or \
               (extracted_data.get('waterfall_flow', 0) == 0 and extracted_data.get('waterfall_height', 0) > 0):
                validation_errors.append("WARNING: Incomplete waterfall data - both height and flow are required")
            
            if validation_errors:
                st.error("### Cannot Send Data - Validation Failed:")
                for error in validation_errors:
                    if error.startswith("ERROR"):
                        st.error(error)
                    else:
                        st.warning(error)
                
                critical_errors = [e for e in validation_errors if e.startswith("ERROR")]
                if critical_errors:
                    st.error("Please correct the errors above before sending data to the calculator.")
                    st.stop()
            
            # If validation passes, send data
            st.session_state.pdf_extracted = extracted_data
            st.session_state.geo_data['pdf_source'] = uploaded_file.name
            
            st.success("Data extracted and sent to Geographic Calculator!")
            
            st.markdown("### Extracted Summary")
            summary_df = pd.DataFrame([{
                'Parameter': 'Location',
                'Value': extracted_data.get('location_name', 'N/A'),
                'Unit': ''
            }, {
                'Parameter': 'Latitude',
                'Value': extracted_data.get('latitude', 0),
                'Unit': '°'
            }, {
                'Parameter': 'Longitude',
                'Value': extracted_data.get('longitude', 0),
                'Unit': '°'
            }, {
                'Parameter': 'Waterfall Flow',
                'Value': extracted_data.get('waterfall_flow', 0),
                'Unit': 'm³/s'
            }, {
                'Parameter': 'Waterfall Height',
                'Value': extracted_data.get('waterfall_height', 0),
                'Unit': 'm'
            }, {
                'Parameter': 'Geothermal Temp',
                'Value': extracted_data.get('geo_temp', 0),
                'Unit': '°C'
            }, {
                'Parameter': 'Drilling Depth',
                'Value': extracted_data.get('depth', 0),
                'Unit': 'km'
            }])
            
            st.dataframe(summary_df, use_container_width=True)
            
            st.info("Go to the Geographic Calculator and select 'Use PDF Data' to calculate energy potential!")
        
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        st.info("Make sure PyPDF2 is installed: pip install PyPDF2")

else:
    st.info("Upload a PDF document to begin extraction")
    
    st.markdown("---")
    st.markdown("### Sample Data Format")
    st.markdown("""
    The analyzer looks for patterns like:
    - Flow rates: `Flow Rate: 12.5 m³/s` or `Q = 10 m³/s`
    - Heights: `Waterfall Height: 65 m` or `H = 50 m`
    - Temperatures: `180-200°C` or `Temperature: 190°C`
    - Depths: `Drilling Depth: 2.8 km` or `2-3.5 km`
    - Coordinates: `Latitude: 22.3569` and `Longitude: 91.7832`
    - Power outputs: `4.5 MW`
    """)

st.markdown("---")
st.markdown("Document Analyzer | Part of Community Energy Toolkit")
st.caption("Extracted data automatically feeds into Geographic Calculator")
