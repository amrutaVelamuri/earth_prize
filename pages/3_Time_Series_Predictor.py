import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pickle

# TensorFlow imports
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    st.error("TensorFlow not installed. Run: pip install tensorflow")

st.set_page_config(page_title="Time-Series Predictor", layout="wide")

# Initialize session state
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}
if 'geo_data' not in st.session_state:
    st.session_state.geo_data = {}
if 'pdf_extracted' not in st.session_state:
    st.session_state.pdf_extracted = {}

st.title("LSTM Time-Series Energy Predictor")
st.markdown("*AI-powered seasonal forecasting using real climate data*")

# Check if we have data from Agent 3
has_geo_data = bool(st.session_state.geo_data and 'P_total_MW' in st.session_state.geo_data)

if not has_geo_data:
    st.warning("No calculation data available from Geographic Calculator!")
    st.info("Please go to the Geographic Calculator and run calculations first.")
    st.markdown("---")
    st.markdown("### What This Tool Does:")
    st.markdown("""
    - Uses a trained LSTM neural network
    - Trained on 122 years of Bangladesh weather data (1901-2023)
    - Predicts monthly energy output based on seasonal climate patterns
    - Provides confidence intervals for predictions
    - Forecasts up to 24 months ahead
    """)
    st.stop()

# Load the trained model and scalers
@st.cache_resource
def load_lstm_model():
    try:
        # Load with compile=False to avoid metric issues
        model = load_model('energy_predictor.h5', compile=False)
        
        # Recompile with proper metrics
        model.compile(
            optimizer='adam',
            loss='mean_squared_error',
            metrics=['mean_absolute_error']
        )
        
        with open('scaler_X.pkl', 'rb') as f:
            scaler_X = pickle.load(f)
        with open('scaler_y.pkl', 'rb') as f:
            scaler_y = pickle.load(f)
        return model, scaler_X, scaler_y, None
    except Exception as e:
        return None, None, None, str(e)

if TENSORFLOW_AVAILABLE:
    with st.spinner("Loading LSTM model..."):
        model, scaler_X, scaler_y, error = load_lstm_model()
    
    if error:
        st.error(f"Could not load model: {error}")
        st.info("Make sure you've run train_lstm_model.py first!")
        st.stop()
    else:
        st.success("✅ LSTM model loaded successfully!")
else:
    st.stop()

# Sidebar controls
st.sidebar.header("Prediction Settings")

forecast_months = st.sidebar.slider("Forecast Period (months)", 3, 24, 12)
start_month = st.sidebar.selectbox("Starting Month", 
    ['January', 'February', 'March', 'April', 'May', 'June',
     'July', 'August', 'September', 'October', 'November', 'December'],
    index=datetime.now().month - 1
)

# Climate scenario (affects predictions)
st.sidebar.markdown("### Climate Scenario")
climate_scenario = st.sidebar.radio(
    "Select scenario:",
    ["Normal", "Wetter (More Monsoon)", "Drier (Less Rain)", "Hotter"]
)

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["LSTM Forecast", "Model Info", "Comparison", "Export"])

# TAB 1: LSTM FORECAST
with tab1:
    st.header("LSTM Energy Forecast")
    
    # Get base data from Geographic Calculator
    base_power_mw = st.session_state.geo_data.get('P_total_MW', 0)
    waterfall_mw = st.session_state.geo_data.get('P_waterfall_MW', 0)
    geo_mw = st.session_state.geo_data.get('P_geo_MW', 0)
    location_name = st.session_state.geo_data.get('location_name', 'Selected Location')
    
    st.markdown(f"### Forecasting for: **{location_name}**")
    st.markdown(f"Base Power Capacity: **{base_power_mw:.2f} MW**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Waterfall Component", f"{waterfall_mw:.2f} MW")
    with col2:
        st.metric("Geothermal Component", f"{geo_mw:.2f} MW")
    
    st.markdown("---")
    
    if st.button("Generate LSTM Forecast", type="primary"):
        
        with st.spinner("Running LSTM predictions..."):
            
            # Month mapping
            month_map = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4,
                'May': 5, 'June': 6, 'July': 7, 'August': 8,
                'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            
            start_month_num = month_map[start_month]
            
            # Typical Bangladesh climate patterns by month
            bangladesh_climate = {
                1: (19, 20),    # January: cool, dry
                2: (22, 25),    # February: warm, dry
                3: (26, 50),    # March: hot, some rain
                4: (28, 100),   # April: hot, pre-monsoon
                5: (28, 250),   # May: hot, monsoon starts
                6: (28, 350),   # June: monsoon peak
                7: (28, 400),   # July: monsoon peak
                8: (28, 350),   # August: monsoon
                9: (27, 300),   # September: monsoon ending
                10: (26, 150),  # October: post-monsoon
                11: (23, 30),   # November: cool, dry
                12: (20, 15)    # December: cool, dry
            }
            
            # Adjust climate based on scenario
            climate_adjustments = {
                "Normal": (1.0, 1.0),
                "Wetter (More Monsoon)": (1.0, 1.3),
                "Drier (Less Rain)": (1.0, 0.7),
                "Hotter": (1.1, 0.9)
            }
            
            temp_mult, rain_mult = climate_adjustments[climate_scenario]
            
            months = []
            temperatures = []
            rainfalls = []
            
            # Generate climate data for forecast period
            for i in range(forecast_months):
                month_num = (start_month_num + i - 1) % 12 + 1
                year_offset = (start_month_num + i - 1) // 12
                
                month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                month_label = f"{month_names[month_num-1]} Y{year_offset+1}"
                months.append(month_label)
                
                # Get typical climate for this month
                base_temp, base_rain = bangladesh_climate[month_num]
                
                # Apply scenario adjustments and some random variation
                np.random.seed(42 + i)
                temp = base_temp * temp_mult * np.random.normal(1.0, 0.05)
                rain = base_rain * rain_mult * np.random.normal(1.0, 0.1)
                
                temperatures.append(temp)
                rainfalls.append(rain)
            
            # Get last 12 months of climate data for LSTM
            historical_months = []
            for i in range(12, 0, -1):
                month_num = (start_month_num - i) % 12
                if month_num == 0:
                    month_num = 12
                base_temp, base_rain = bangladesh_climate[month_num]
                historical_months.append([base_temp, base_rain])
            
            # Make predictions month by month
            predictions_mwh = []
            confidence_lower = []
            confidence_upper = []
            
            current_sequence = np.array(historical_months)
            
            for i in range(forecast_months):
                # Normalize the sequence
                sequence_scaled = scaler_X.transform(current_sequence)
                sequence_scaled = sequence_scaled.reshape(1, 12, 2)
                
                # Predict with LSTM
                prediction_scaled = model.predict(sequence_scaled, verbose=0)
                prediction_mwh = scaler_y.inverse_transform(prediction_scaled)[0][0]
                
                # Scale prediction to match user's system capacity
                user_monthly_mwh = (base_power_mw * 730)
                scale_factor = user_monthly_mwh / 3500
                
                scaled_prediction = prediction_mwh * scale_factor
                
                predictions_mwh.append(scaled_prediction)
                
                # Confidence intervals (±15%)
                confidence_lower.append(scaled_prediction * 0.85)
                confidence_upper.append(scaled_prediction * 1.15)
                
                # Update sequence with new data point
                new_point = [temperatures[i], rainfalls[i]]
                current_sequence = np.vstack([current_sequence[1:], new_point])
            
            # Calculate power from energy
            hours_per_month = 730
            predictions_mw = [e / hours_per_month for e in predictions_mwh]
            
            # Breakdown by source
            waterfall_ratio = waterfall_mw / base_power_mw if base_power_mw > 0 else 0.5
            geo_ratio = geo_mw / base_power_mw if base_power_mw > 0 else 0.5
            
            waterfall_predictions = [p * waterfall_ratio for p in predictions_mwh]
            geo_predictions = [p * geo_ratio for p in predictions_mwh]
            
            # Store predictions
            st.session_state.predictions = {
                'months': months,
                'temperatures': temperatures,
                'rainfalls': rainfalls,
                'waterfall_mw': [w / hours_per_month for w in waterfall_predictions],
                'geo_mw': [g / hours_per_month for g in geo_predictions],
                'total_mw': predictions_mw,
                'waterfall_mwh': waterfall_predictions,
                'geo_mwh': geo_predictions,
                'total_mwh': predictions_mwh,
                'confidence_lower': confidence_lower,
                'confidence_upper': confidence_upper,
                'total_annual_mwh': sum(predictions_mwh),
                'location': location_name,
                'climate_scenario': climate_scenario
            }
        
        st.success("✅ LSTM forecast generated successfully!")
    
    # Display predictions if they exist
    if 'months' in st.session_state.predictions:
        
        months = st.session_state.predictions['months']
        predictions_mw = st.session_state.predictions['total_mw']
        predictions_mwh = st.session_state.predictions['total_mwh']
        confidence_lower = st.session_state.predictions['confidence_lower']
        confidence_upper = st.session_state.predictions['confidence_upper']
        temperatures = st.session_state.predictions['temperatures']
        rainfalls = st.session_state.predictions['rainfalls']
        
        st.markdown("### Monthly Energy Forecast (LSTM)")
        
        # Create interactive plot
        fig = go.Figure()
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=months + months[::-1],
            y=[c/730 for c in confidence_upper] + [c/730 for c in confidence_lower[::-1]],
            fill='toself',
            fillcolor='rgba(0,100,200,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval (±15%)',
            showlegend=True
        ))
        
        # Total prediction line
        fig.add_trace(go.Scatter(
            x=months,
            y=predictions_mw,
            mode='lines+markers',
            name='LSTM Prediction',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=f"LSTM Energy Forecast - {location_name} ({st.session_state.predictions['climate_scenario']} Scenario)",
            xaxis_title="Month",
            yaxis_title="Power Output (MW)",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary metrics
        st.markdown("### Forecast Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_power = np.mean(predictions_mw)
            st.metric("Average Power", f"{avg_power:.2f} MW")
        
        with col2:
            total_energy = sum(predictions_mwh)
            st.metric("Total Energy (Forecast Period)", f"{total_energy:,.0f} MWh")
        
        with col3:
            peak_month = months[np.argmax(predictions_mw)]
            peak_power = max(predictions_mw)
            st.metric("Peak Month", peak_month)
            st.caption(f"{peak_power:.2f} MW")
        
        with col4:
            households = int(total_energy * 1000 / 7.2)
            st.metric("Avg Households Powered", f"{households:,}")
        
        # Climate input visualization
        st.markdown("---")
        st.markdown("### Climate Inputs (LSTM Features)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=months,
                y=temperatures,
                mode='lines+markers',
                name='Temperature',
                line=dict(color='red')
            ))
            fig_temp.update_layout(
                title='Temperature Forecast',
                xaxis_title='Month',
                yaxis_title='Temperature (°C)',
                height=300
            )
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col2:
            fig_rain = go.Figure()
            fig_rain.add_trace(go.Bar(
                x=months,
                y=rainfalls,
                name='Rainfall',
                marker_color='lightblue'
            ))
            fig_rain.update_layout(
                title='Rainfall Forecast',
                xaxis_title='Month',
                yaxis_title='Rainfall (mm)',
                height=300
            )
            st.plotly_chart(fig_rain, use_container_width=True)
        
        # Monthly breakdown table
        with st.expander("View Detailed Monthly Predictions"):
            prediction_df = pd.DataFrame({
                'Month': months,
                'Temp (°C)': [f"{t:.1f}" for t in temperatures],
                'Rain (mm)': [f"{r:.0f}" for r in rainfalls],
                'Power (MW)': [f"{p:.2f}" for p in predictions_mw],
                'Energy (MWh)': [f"{e:,.0f}" for e in predictions_mwh],
                'Households': [int(e * 1000 / 7.2) for e in predictions_mwh]
            })
            st.dataframe(prediction_df, use_container_width=True)
    else:
        st.info("Click 'Generate LSTM Forecast' button above to create predictions")

# TAB 2: MODEL INFO
with tab2:
    st.header("LSTM Model Information")
    
    st.markdown("""
    ### About This Model
    
    This is a **Long Short-Term Memory (LSTM)** neural network trained to predict energy output 
    based on climate patterns.
    
    #### Training Data:
    - **Source:** Bangladesh Weather Dataset (Kaggle)
    - **Period:** 1901-2023 (122 years)
    - **Features:** Monthly temperature and rainfall
    - **Records:** 1,474 months of historical data
    
    #### Model Architecture:
    - **Type:** LSTM Recurrent Neural Network
    - **Layers:** 
      - LSTM Layer 1: 64 units
      - Dropout: 20%
      - LSTM Layer 2: 32 units
      - Dropout: 20%
      - Dense: 16 units
      - Output: 1 unit (energy prediction)
    - **Input:** 12-month sequences of temperature + rainfall
    - **Output:** Next month's energy output (MWh)
    
    #### How It Works:
    1. Takes historical climate data (temp + rainfall) for past 12 months
    2. LSTM learns seasonal patterns and trends
    3. Predicts energy output for next month
    4. Scales prediction to match your system capacity
    5. Repeats for each forecasted month
    
    #### Physical Basis:
    - **Rainfall → Waterfall Power:** More rain = higher water flow = more power
    - **Temperature → Geothermal:** Higher temp = better heat extraction
    - Model learns these relationships from 122 years of climate cycles
    """)
    
    if st.checkbox("Show Training History Graph"):
        try:
            from PIL import Image
            img = Image.open('training_history.png')
            st.image(img, caption='LSTM Training History', use_column_width=True)
        except:
            st.info("training_history.png not found. Run train_lstm_model.py to generate it.")

# TAB 3: COMPARISON
with tab3:
    st.header("LSTM vs Baseline Comparison")
    
    if 'total_annual_mwh' in st.session_state.predictions:
        
        predicted_annual = st.session_state.predictions['total_annual_mwh']
        actual_annual = st.session_state.geo_data.get('E_total_year_MWh', 0)
        
        st.markdown("### Predicted vs Baseline")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Baseline Annual Energy", f"{actual_annual:,.0f} MWh")
            st.caption("From Geographic Calculator (constant)")
        
        with col2:
            st.metric("LSTM Predicted Energy", f"{predicted_annual:,.0f} MWh")
            st.caption(f"Accounting for {st.session_state.predictions.get('climate_scenario', 'Normal')} climate")
        
        with col3:
            difference_pct = ((predicted_annual - actual_annual) / actual_annual * 100) if actual_annual > 0 else 0
            st.metric("Difference", f"{difference_pct:+.1f}%")
            st.caption("Due to seasonal/climate factors")
        
        # Comparison chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Baseline',
            x=['Annual Energy'],
            y=[actual_annual],
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='LSTM Prediction',
            x=['Annual Energy'],
            y=[predicted_annual],
            marker_color='darkblue'
        ))
        
        fig.update_layout(
            title='Annual Energy Comparison',
            yaxis_title='Energy (MWh)',
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Generate a forecast first!")

# TAB 4: EXPORT
with tab4:
    st.header("Export Predictions")
    
    if 'months' in st.session_state.predictions:
        
        export_df = pd.DataFrame({
            'Month': st.session_state.predictions['months'],
            'Temperature_C': st.session_state.predictions['temperatures'],
            'Rainfall_mm': st.session_state.predictions['rainfalls'],
            'Total_MW': st.session_state.predictions['total_mw'],
            'Monthly_Energy_MWh': st.session_state.predictions['total_mwh'],
            'Confidence_Lower_MWh': st.session_state.predictions['confidence_lower'],
            'Confidence_Upper_MWh': st.session_state.predictions['confidence_upper']
        })
        
        st.dataframe(export_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="Download LSTM Predictions (CSV)",
                data=csv,
                file_name=f"lstm_forecast_{st.session_state.predictions.get('location', 'location')}.csv",
                mime="text/csv"
            )
        
        with col2:
            import json
            summary = {
                'model': 'LSTM Neural Network',
                'location': st.session_state.predictions.get('location', 'N/A'),
                'climate_scenario': st.session_state.predictions.get('climate_scenario', 'Normal'),
                'forecast_period_months': len(st.session_state.predictions['months']),
                'total_predicted_energy_mwh': st.session_state.predictions['total_annual_mwh'],
                'average_monthly_mwh': np.mean(st.session_state.predictions['total_mwh']),
                'predictions': export_df.to_dict('records')
            }
            
            json_str = json.dumps(summary, indent=2)
            st.download_button(
                label="Download Report (JSON)",
                data=json_str,
                file_name=f"lstm_forecast_report_{st.session_state.predictions.get('location', 'location')}.json",
                mime="application/json"
            )
        
    else:
        st.warning("Generate a forecast first!")

st.markdown("---")
st.markdown("Community Energy Toolkit - LSTM Time-Series Predictor")
