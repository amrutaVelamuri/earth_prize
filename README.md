Community Energy Toolkit
Open-source renewable energy analysis platform for sustainable community development.
Overview
The Community Energy Toolkit helps communities and organizations calculate and predict renewable energy potential from waterfall turbines, geothermal systems, and waste energy recovery.
Built for the Earthshot Prize Challenge to democratize renewable energy planning for underserved communities worldwide.
Features

PDF Analyzer: Automatically extracts technical data from engineering documents
Geographic Calculator: Interactive map-based energy potential analysis with batch processing
Time-Series Predictor: LSTM neural network forecasting using 122 years of climate data

Installation
bash# Clone repository
git clone https://github.com/amrutaVelamuri/earth_prize.git
cd earth_prize

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
Open browser to http://localhost:8501
Project Structure
earth_prize/
├── app.py                          # Main landing page
├── pages/
│   ├── 1_PDF_Analyzer.py          # Document extraction
│   ├── 2_Geographic_Calculator.py # Energy calculations
│   └── 3_Time_Series_Predictor.py # LSTM forecasting
├── validation.py                   # Input validation module
├── requirements.txt
├── README.md
└── tests/
    └── test_validation.py
Usage
Basic Workflow

PDF Analyzer (optional): Upload technical documents to auto-extract parameters
Geographic Calculator: Enter location data, calculate energy potential, export results
Time-Series Predictor: Generate seasonal forecasts based on climate scenarios

Batch Analysis CSV Format
csvlocation_name,latitude,longitude,waterfall_height_m,waterfall_flow_m3s,geo_temp_c,depth_km
Chittagong Hills,22.3569,91.7832,45,8.5,180,2.8
Sylhet Valley,24.8949,91.8687,30,12.0,150,2.5
Calculations
Waterfall Power
P = ρ × g × Q × h × η

ρ = 1000 kg/m³ (water density)
g = 9.81 m/s² (gravity)
Q = flow rate (m³/s)
h = height (m)
η = efficiency (0.85-0.95)

Geothermal Power
P = ṁ × Cp × ΔT × η / 1000

ṁ = 50 kg/s (mass flow rate)
Cp = 4.18 kJ/kg·°C (specific heat)
ΔT = temperature difference (°C)
η = conversion efficiency (0.10-0.25)

Waste Recovery
E_recovered = E_base × 0.30 × 0.80
Assumes 30% waste rate with 80% recovery efficiency.
Example Output
Input: Chittagong Hills - 45m waterfall at 8.5 m³/s, 180°C geothermal at 2.8km depth
Output:

Waterfall: 3.36 MW
Geothermal: 0.49 MW
Waste Recovery: 0.83 MW/year
Total: 3.85 MW powering 3,850 households

Testing
bashpip install pytest pytest-cov
pytest tests/
Impact
This toolkit enables communities to:

Calculate feasibility before expensive surveys
Compare multiple locations
Predict seasonal variations
Plan for climate scenarios
Make data-driven investment decisions

License
MIT License
Contact

Email: amvelamuri@gmail.com
GitHub: https://github.com/amrutaVelamuri/earth_prize
Issues: https://github.com/amrutaVelamuri/earth_prize/issues
