import streamlit as st
import importlib.util, sys, os
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ============================================================================
# PAGE CONFIG — sidebar hidden entirely
# ============================================================================
st.set_page_config(
    page_title="EcoGrid — Community Energy Toolkit",
    layout="wide",
    page_icon="🌱",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# GLOBAL CSS
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

[data-testid="collapsedControl"]  { display: none !important; }
section[data-testid="stSidebar"]  { display: none !important; }

:root {
    --gd:#0d3b2e; --gm:#1a6b4a; --gb:#2ecc85; --gg:#4fffb0;
    --ea:#c8a96e; --cr:#f5f0e8; --dk:#0a1f17; --bd:rgba(46,204,133,.2);
}
html,body,[class*="css"]{ font-family:'DM Sans',sans-serif; }
.main { background: var(--dk); }
.block-container { padding: 1.5rem 2.5rem 4rem; }

.hero-wrap{background:linear-gradient(135deg,#0d3b2e 0%,#0a2a20 45%,#071a14 100%);
    border:1px solid var(--bd);border-radius:20px;padding:40px 50px;margin-bottom:32px;
    position:relative;overflow:hidden;
    display:flex;align-items:center;gap:36px;}
.hero-wrap::before{content:'';position:absolute;inset:0;
    background:radial-gradient(ellipse 60% 80% at 80% 50%,rgba(46,204,133,.13) 0%,transparent 70%);
    pointer-events:none;}
.hero-logo-img{
    width:140px;height:140px;object-fit:contain;flex-shrink:0;
    filter:drop-shadow(0 0 18px rgba(46,204,133,0.35)) brightness(1.1);
    position:relative;z-index:1;
    border-radius:50%;
    mix-blend-mode: lighten;
}
.hero-text{position:relative;z-index:1;}
.hero-logo{font-family:'Syne',sans-serif;font-size:4em;font-weight:800;
    color:var(--gb);letter-spacing:-2px;line-height:1;margin:0;}
.hero-logo span{color:var(--ea);}
.hero-tag{font-size:1.05em;color:rgba(245,240,232,.65);margin:8px 0 0;font-weight:300;}
.hero-badge{display:inline-block;background:rgba(46,204,133,.12);border:1px solid var(--gb);
    color:var(--gb);border-radius:100px;padding:4px 14px;
    font-size:.74em;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:14px;}

.stTabs [data-baseweb="tab-list"]{background:rgba(13,59,46,.6);border-radius:14px;padding:5px;
    gap:3px;border:1px solid var(--bd);backdrop-filter:blur(10px);}
.stTabs [data-baseweb="tab"]{border-radius:10px;padding:10px 20px;
    color:rgba(245,240,232,.48);font-family:'Syne',sans-serif;
    font-weight:600;font-size:.84em;transition:all .25s;
    border:none!important;background:transparent!important;}
.stTabs [aria-selected="true"]{background:var(--gb)!important;color:var(--dk)!important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:26px;min-height:500px;}

.sh{font-family:'Syne',sans-serif;font-size:1.85em;font-weight:800;
    color:var(--cr);letter-spacing:-1px;margin-bottom:3px;}
.ss{color:rgba(245,240,232,.43);font-size:.88em;margin-bottom:20px;}
.al{width:42px;height:3px;background:var(--gb);border-radius:2px;margin-bottom:16px;}

.stat-card{background:linear-gradient(145deg,rgba(26,107,74,.2),rgba(13,59,46,.35));
    border:1px solid var(--bd);border-radius:16px;padding:20px 14px;text-align:center;}
.sn{font-family:'Syne',sans-serif;font-size:2.1em;font-weight:800;color:var(--gb);line-height:1;}
.sl{font-size:.76em;color:rgba(245,240,232,.48);margin-top:5px;text-transform:uppercase;letter-spacing:.6px;}

.team-card{background:linear-gradient(145deg,rgba(26,107,74,.13),rgba(13,59,46,.26));
    border:1px solid var(--bd);border-radius:18px;padding:24px 16px;text-align:center;
    transition:transform .3s,border-color .3s;}
.team-card:hover{border-color:var(--gb);transform:translateY(-4px);}
.tav{width:88px;height:88px;border-radius:50%;margin:0 auto 13px;
    border:2px solid var(--gb);display:flex;align-items:center;justify-content:center;
    font-size:1.9em;font-weight:700;font-family:'Syne',sans-serif;}
.tn{font-family:'Syne',sans-serif;font-size:.97em;font-weight:700;color:var(--cr);margin-bottom:2px;}
.tr{font-size:.76em;color:var(--gb);text-transform:uppercase;letter-spacing:.8px;font-weight:600;}
.tb{font-size:.78em;color:rgba(245,240,232,.48);margin-top:6px;line-height:1.5;}

.hw-card{background:linear-gradient(145deg,rgba(26,107,74,.17),rgba(13,59,46,.28));
    border:1px solid var(--bd);border-radius:15px;padding:20px;text-align:center;}
.hi{font-size:2.1em;margin-bottom:6px;}
.hl{font-family:'Syne',sans-serif;font-size:.86em;font-weight:700;color:var(--cr);text-transform:uppercase;letter-spacing:.4px;}
.hon{color:var(--gb);font-size:.92em;font-weight:700;margin-top:5px;}
.hwn{color:var(--ea);font-size:.92em;font-weight:700;margin-top:5px;}

.ib{background:rgba(13,59,46,.4);border-left:3px solid var(--gb);
    border-radius:0 11px 11px 0;padding:13px 17px;margin:9px 0;
    color:rgba(245,240,232,.78);font-size:.88em;line-height:1.6;}
.fp{background:rgba(46,204,133,.09);border:1px solid rgba(46,204,133,.22);
    color:var(--gb);border-radius:100px;padding:4px 12px;
    font-size:.8em;font-weight:500;display:inline-block;margin:2px 2px;}

.sr{display:flex;align-items:flex-start;gap:13px;background:rgba(13,59,46,.28);
    border:1px solid var(--bd);border-radius:12px;padding:15px 17px;margin-bottom:9px;}
.snum{background:var(--gb);color:var(--dk);width:28px;height:28px;min-width:28px;
    border-radius:50%;display:flex;align-items:center;justify-content:center;
    font-family:'Syne',sans-serif;font-weight:800;font-size:.88em;}
.sbody h4{font-family:'Syne',sans-serif;color:var(--cr);margin:0 0 2px;font-size:.9em;}
.sbody p{color:rgba(245,240,232,.46);margin:0;font-size:.79em;line-height:1.5;}

div[data-testid="stMetricValue"]{color:var(--gb)!important;font-family:'Syne',sans-serif!important;}
div[data-testid="stMetricLabel"]{color:rgba(245,240,232,.52)!important;}
.stButton>button{background:var(--gb)!important;color:var(--dk)!important;
    font-family:'Syne',sans-serif!important;font-weight:700!important;
    border:none!important;border-radius:10px!important;padding:10px 22px!important;transition:all .2s!important;}
.stButton>button:hover{background:var(--gg)!important;transform:translateY(-2px);}
.stSelectbox label,.stNumberInput label,.stCheckbox label,.stSlider label{color:rgba(245,240,232,.75)!important;}

.footer{text-align:center;padding:26px 0 4px;color:rgba(245,240,232,.26);
    font-size:.78em;border-top:1px solid var(--bd);margin-top:38px;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER — run a page file inside the current tab context
# ============================================================================
def run_page(filepath: str):
    """Run a page file in-place. Catches st.stop() so tabs 4+5 still render."""
    abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
    if not os.path.exists(abs_path):
        st.error(f"File not found: {filepath}")
        return
    try:
        spec = importlib.util.spec_from_file_location("_pg", abs_path)
        mod  = importlib.util.module_from_spec(spec)
        mod.__file__ = abs_path
        sys.modules["_pg"] = mod
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    except Exception as e:
        st.error(f"Error in {filepath}: {e}")


# ============================================================================
# SESSION STATE
# ============================================================================
for k, v in {
    'geo_data': {}, 'pdf_extracted': {}, 'predictions': {},
    'linked_locations': [],
    'energy_history_v4': {'records':[],'usage_log':[],'recovered_log':[],'remaining_log':[]},
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================================
# LOGO — load and base64-encode once
# ============================================================================
def load_logo_b64(path="logo.png"):
    """Try to load logo from same directory as app.py. Returns base64 string or None."""
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = load_logo_b64()

# ============================================================================
# HERO — with logo if available, text-only fallback otherwise
# ============================================================================
if logo_b64:
    st.markdown(f"""
    <div class="hero-wrap">
      <img src="data:image/png;base64,{logo_b64}" class="hero-logo-img" alt="EcoGrid Logo" />
      <div class="hero-text">
        <div class="hero-badge">🌍 Community Energy Toolkit</div>
        <p class="hero-logo">Eco<span>Grid</span></p>
        <p class="hero-tag">Renewable energy analysis · Carbon impact measurement · AI-powered monitoring</p>
      </div>
    </div>""", unsafe_allow_html=True)
else:
    # Fallback: no logo file found
    st.markdown("""
    <div class="hero-wrap">
      <div class="hero-text">
        <div class="hero-badge">🌍 Community Energy Toolkit</div>
        <p class="hero-logo">Eco<span>Grid</span></p>
        <p class="hero-tag">Renewable energy analysis · Carbon impact measurement · AI-powered monitoring</p>
      </div>
    </div>""", unsafe_allow_html=True)
    st.info("💡 Tip: Place `logo.png` in the same folder as `app.py` to display the logo in the header.", icon="🖼️")

# ============================================================================
# MAIN TABS
# ============================================================================
t1, t2, t3, t4, t5 = st.tabs([
    "👥  Introduction",
    "📚  About & Education",
    "📊  Data & Calculation",
    "🔌  Verification Unit",
    "🏠  Household Energy Status",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — INTRODUCTION
# ══════════════════════════════════════════════════════════════════════════════
with t1:
    st.markdown('<p class="sh">Our Mission</p><div class="al"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ib">EcoGrid is a comprehensive platform that helps communities analyse renewable energy potential, measure environmental impact, and optimise energy consumption. Our toolkit combines AI with practical energy calculations to make clean energy accessible to everyone.</div>', unsafe_allow_html=True)

    for col,(n,l) in zip(st.columns(4),[("5","Modules"),("3","Energy Sources"),("122yrs","Training Data"),("CO₂","Tracked")]):
        col.markdown(f'<div class="stat-card"><div class="sn">{n}</div><div class="sl">{l}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Meet the Team</p><div class="al"></div><p class="ss">Replace names, roles and bios below — uncomment st.image() to add real photos.</p>', unsafe_allow_html=True)

    TEAM = [
        {"i":"TM1","g":"linear-gradient(135deg,#2ecc85,#0d3b2e)","n":"Team Member 1","r":"Project Lead","b":"Add a short bio here."},
        {"i":"TM2","g":"linear-gradient(135deg,#4fffb0,#1a6b4a)","n":"Team Member 2","r":"Energy Engineer","b":"Add a short bio here."},
        {"i":"TM3","g":"linear-gradient(135deg,#c8a96e,#6b4a1a)","n":"Team Member 3","r":"Data Scientist","b":"Add a short bio here."},
        {"i":"TM4","g":"linear-gradient(135deg,#85c8ff,#1a4a6b)","n":"Team Member 4","r":"Hardware Engineer","b":"Add a short bio here."},
    ]
    for col, m in zip(st.columns(4), TEAM):
        with col:
            st.markdown(f"""<div class="team-card">
              <div class="tav" style="background:{m['g']};">{m['i']}</div>
              <div class="tn">{m['n']}</div>
              <div class="tr">{m['r']}</div>
              <div class="tb">{m['b']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">What We Built</p><div class="al"></div>', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("""<div style="background:rgba(13,59,46,.33);border:1px solid rgba(46,204,133,.18);border-radius:15px;padding:20px;">
          <p style="font-family:'Syne',sans-serif;font-weight:700;color:#f5f0e8;margin-bottom:10px;">🔋 Energy Analysis</p>
          <span class="fp">Waterfall Hydro</span><span class="fp">Geothermal</span>
          <span class="fp">Waste Recovery</span><span class="fp">Multi-location Grid</span>
          <p style="font-family:'Syne',sans-serif;font-weight:700;color:#f5f0e8;margin:14px 0 10px;">🌱 Environmental</p>
          <span class="fp">CO₂ Tracking</span><span class="fp">Tree Equivalency</span><span class="fp">Fossil Comparison</span>
        </div>""", unsafe_allow_html=True)
    with f2:
        st.markdown("""<div style="background:rgba(13,59,46,.33);border:1px solid rgba(46,204,133,.18);border-radius:15px;padding:20px;">
          <p style="font-family:'Syne',sans-serif;font-weight:700;color:#f5f0e8;margin-bottom:10px;">🤖 AI & Forecasting</p>
          <span class="fp">Real-time Monitoring</span><span class="fp">Anomaly Detection</span>
          <span class="fp">LSTM Predictions</span><span class="fp">122-year Dataset</span>
          <p style="font-family:'Syne',sans-serif;font-weight:700;color:#f5f0e8;margin:14px 0 10px;">📄 Reporting</p>
          <span class="fp">PDF Extraction</span><span class="fp">AI Reports</span><span class="fp">CSV / JSON Export</span>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ABOUT & EDUCATION
# ══════════════════════════════════════════════════════════════════════════════
with t2:
    st.markdown('<p class="sh">About & Education</p><div class="al"></div><p class="ss">Learn how to get the most out of EcoGrid</p>', unsafe_allow_html=True)

    for i,(title,desc) in enumerate([
        ("PDF Analyzer","Upload a technical document. Auto-extracts coordinates, waterfall specs, geothermal temperatures and drilling depths."),
        ("Geographic Calculator","Enter or import location data. Adjust sliders and hit Calculate for power, energy and carbon figures."),
        ("Time-Series Predictor","With calculator data loaded, run the LSTM predictor trained on 122 years of Bangladesh weather data."),
        ("Household Energy Status","Enter real-time kWh readings for any sector. The AI engine flags anomalies and recommends actions."),
        ("Export & AI Reports","Download CSV / JSON or generate a full written report tailored to your audience."),
    ], 1):
        st.markdown(f'<div class="sr"><div class="snum">{i}</div><div class="sbody"><h4>{title}</h4><p>{desc}</p></div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Visual Guides</p><div class="al"></div><p class="ss">Add screenshots by uploading images to your project folder and calling st.image()</p>', unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    for col, lbl in zip([g1,g2], ["Platform Overview","Calculator Walkthrough"]):
        col.markdown(f'<div style="border:2px dashed rgba(46,204,133,.26);border-radius:13px;padding:54px 16px;text-align:center;background:rgba(13,59,46,.18);"><p style="color:rgba(245,240,232,.38);font-size:.96em;margin:0;">📷 {lbl}</p></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DATA & CALCULATION
# ══════════════════════════════════════════════════════════════════════════════
with t3:
    st.markdown('<p class="sh">Data & Calculation</p><div class="al"></div>', unsafe_allow_html=True)

    sub1, sub2, sub3 = st.tabs([
        "📄  PDF Analyzer",
        "🌍  Geographic Calculator",
        "📈  Time-Series Predictor",
    ])

    with sub1:
        run_page("pages/1_PDF_Analyzer.py")

    with sub2:
        run_page("pages/2_Geographic_Calculator.py")

    with sub3:
        run_page("pages/3_Time_Series_Predictor.py")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — VERIFICATION UNIT
# ══════════════════════════════════════════════════════════════════════════════
with t4:
    st.markdown('<p class="sh">Verification Unit</p><div class="al"></div><p class="ss">Hardware integration · Sensors · Physical verification</p>', unsafe_allow_html=True)

    for col,(icon,lbl,status,cls) in zip(st.columns(4),[
        ("⚡","Sensor Array","Online","hon"),
        ("📡","Data Link","Connected","hon"),
        ("🔋","Power Supply","Normal","hwn"),
        ("🛡️","Verification","Active","hon"),
    ]):
        col.markdown(f'<div class="hw-card"><div class="hi">{icon}</div><div class="hl">{lbl}</div><div class="{cls}">{status}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    hh1, hh2 = st.columns(2)
    with hh1:
        st.markdown('<p style="font-family:\'Syne\',sans-serif;font-weight:700;color:#f5f0e8;margin-bottom:11px;">🔧 Physical Equipment</p>', unsafe_allow_html=True)
        for n,d in [
            ("Energy meters & CTs","Real-time kWh per phase"),
            ("DAQ modules","Digitise analogue signals at 1 kHz"),
            ("IoT gateway / ESP32","Edge processing & MQTT"),
            ("Environmental sensors","Temp, humidity, irradiance"),
        ]:
            st.markdown(f'<div style="background:rgba(13,59,46,.28);border:1px solid rgba(46,204,133,.14);border-radius:10px;padding:11px 15px;margin-bottom:8px;"><p style="color:#f5f0e8;font-weight:600;margin:0 0 2px;font-size:.88em;">{n}</p><p style="color:rgba(245,240,232,.42);margin:0;font-size:.78em;">{d}</p></div>', unsafe_allow_html=True)
    with hh2:
        st.markdown('<p style="font-family:\'Syne\',sans-serif;font-weight:700;color:#f5f0e8;margin-bottom:11px;">📡 Data & Verification</p>', unsafe_allow_html=True)
        for n,d in [
            ("Calibration","Monthly zero-point & span vs. reference"),
            ("Protocol","MQTT over TLS every 5 s"),
            ("Quality control","3σ rejection + CRC checks"),
            ("Certification","IEC 62052 / ANSI C12.20"),
        ]:
            st.markdown(f'<div style="background:rgba(13,59,46,.28);border:1px solid rgba(46,204,133,.14);border-radius:10px;padding:11px 15px;margin-bottom:8px;"><p style="color:#f5f0e8;font-weight:600;margin:0 0 2px;font-size:.88em;">{n}</p><p style="color:rgba(245,240,232,.42);margin:0;font-size:.78em;">{d}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Setup Guide</p><div class="al"></div>', unsafe_allow_html=True)
    for i,(title,d) in enumerate([
        ("Wire sensors","Connect CTs around each phase conductor. Use shielded cable for runs > 1 m."),
        ("Flash firmware","Upload Arduino/ESP32 sketch. Set Wi-Fi SSID & MQTT broker in config.h."),
        ("Calibrate","Apply 1 kW reference load; adjust CT_RATIO until reading matches."),
        ("Verify transmission","Check MQTT dashboard — payloads every 5 s, CRC pass > 99.9%."),
        ("Connect to EcoGrid","Enter broker URL in Household Energy Status tab. Data flows automatically."),
    ], 1):
        st.markdown(f'<div class="sr"><div class="snum">{i}</div><div class="sbody"><h4>{title}</h4><p>{d}</p></div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    hw1, hw2 = st.columns(2)
    for col, lbl in zip([hw1,hw2], ["Wiring Diagram","Installed Unit Photo"]):
        col.markdown(f'<div style="border:2px dashed rgba(46,204,133,.25);border-radius:12px;padding:50px 14px;text-align:center;background:rgba(13,59,46,.16);"><p style="color:rgba(245,240,232,.35);font-size:.93em;margin:0;">📷 {lbl}</p></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — HOUSEHOLD ENERGY STATUS
# ══════════════════════════════════════════════════════════════════════════════
with t5:
    st.markdown('<p class="sh">Household Energy Status</p><div class="al"></div><p class="ss">EnergyGuard AI · Keen Edition V4 · Real-time monitoring & optimisation</p>', unsafe_allow_html=True)

    class ER:
        def __init__(self,u,e,s,t,sl,tmp):
            self.usage=u; self.expected=e; self.sector=s
            self.time_of_day=t; self.sunlight=sl; self.temperature=tmp

    def eg_ratio(r):   return r.usage/r.expected if r.expected else 0
    def eg_anomaly(h): return len(h['usage_log'])>=2 and h['usage_log'][-1]>h['usage_log'][-2]*1.25
    def eg_alert(rt,an): return "CRITICAL" if rt>=1.35 or an else ("WARNING" if rt>=1.15 else "NORMAL")
    def eg_score(rt):  return round(max(0,min(100,100-abs(rt-1)*75)),1)
    def eg_recovery(r): w=.3*r.usage; rec=.8*w; return round(rec,2),round(w-rec,2)

    def eg_ai(r,rt,an,al,rec):
        reasons,actions,conf=[],[],30
        reasons.append(f"Usage is {rt:.2f}× expected")
        if an:                reasons.append("Abnormal spike detected"); conf+=15
        if r.temperature>30:  reasons.append("High temp — cooling load increased"); conf+=10
        if r.sunlight and r.time_of_day.lower()=="day": reasons.append("Sunlight available but underutilised"); conf+=15
        if r.sector.lower() in ["factory","power plant"]: reasons.append("High recoverable industrial losses"); conf+=15
        actions.append(("HIGH",  f"Continuously recover wasted electricity (~{rec[0]} kWh)"))
        actions.append(("HIGH",  f"System stability reserve (~{rec[1]} kWh)"))
        if an:   actions.append(("IMMEDIATE","Activate Null Line — capture leakage"))
        if al=="CRITICAL":
            actions.append(("IMMEDIATE","Reduce non-essential loads"))
            actions.append(("HIGH","Shift base load to geothermal/renewable"))
            if r.sunlight: actions.append(("IMMEDIATE","Activate Smart Daylight-Mirroring System"))
        elif al=="WARNING": actions.append(("MEDIUM","Optimise operating schedule"))
        else:               actions.append(("LOW","System operating optimally"))
        return reasons, actions, min(100,conf)

    with st.form("hh_energy_form"):
        st.markdown('<p style="font-family:\'Syne\',sans-serif;font-weight:700;color:#f5f0e8;font-size:.94em;margin-bottom:13px;">📊 Enter Energy Reading</p>', unsafe_allow_html=True)
        fi1, fi2 = st.columns(2)
        with fi1:
            usage_v    = st.number_input("Energy usage (kWh)",   min_value=0.0,  step=0.1, value=5.0)
            expected_v = st.number_input("Expected usage (kWh)", min_value=0.01, step=0.1, value=4.0)
            sector_v   = st.selectbox("Sector", ["Home","Factory","Power Plant"])
        with fi2:
            tod_v      = st.selectbox("Time of Day", ["Day","Night"])
            sun_v      = st.checkbox("Sunlight available?", value=True)
            temp_v     = st.number_input("Temperature (°C)", step=0.1, value=25.0)
        sub = st.form_submit_button("🔍 Analyse Energy", use_container_width=True)

    if sub:
        rec_obj = ER(usage_v,expected_v,sector_v,tod_v,sun_v,temp_v)
        rt  = eg_ratio(rec_obj)
        an  = eg_anomaly(st.session_state.energy_history_v4)
        al  = eg_alert(rt,an)
        sc  = eg_score(rt)
        rv  = eg_recovery(rec_obj)

        h = st.session_state.energy_history_v4
        h['records'].append(rec_obj); h['usage_log'].append(usage_v)
        h['recovered_log'].append(rv[0]); h['remaining_log'].append(rv[1])

        if al=="CRITICAL":  st.error("🔴 CRITICAL — Immediate optimisation required!")
        elif al=="WARNING": st.warning("🟡 WARNING — Efficiency dropping")
        else:               st.success("🟢 NORMAL — System operating optimally")

        m1,m2,m3,m4 = st.columns(4)
        m1.metric("Usage Ratio",      f"{rt:.2f}×")
        m2.metric("Efficiency Score", f"{sc}/100")
        m3.metric("Recovered",        f"{rv[0]} kWh")
        m4.metric("Wasted",           f"{rv[1]} kWh")

        reasons,actions,conf = eg_ai(rec_obj,rt,an,al,rv)
        st.markdown('<p style="font-family:\'Syne\',sans-serif;font-weight:700;color:#2ecc85;margin:18px 0 7px;">🤖 AI Diagnosis</p>', unsafe_allow_html=True)
        for rr in reasons:
            st.markdown(f'<div class="ib">• {rr}</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:rgba(245,240,232,.44);font-size:.83em;">Confidence: <strong style="color:#2ecc85;">{conf}%</strong></p>', unsafe_allow_html=True)

        st.markdown('<p style="font-family:\'Syne\',sans-serif;font-weight:700;color:#2ecc85;margin:16px 0 7px;">🛠️ Recommended Actions</p>', unsafe_allow_html=True)
        for lvl,act in actions:
            if lvl=="IMMEDIATE": st.error(f"🚨 **[{lvl}]** {act}")
            elif lvl=="HIGH":    st.warning(f"⚠️ **[{lvl}]** {act}")
            elif lvl=="MEDIUM":  st.info(f"ℹ️ **[{lvl}]** {act}")
            else:                st.success(f"✅ **[{lvl}]** {act}")

        if len(h['usage_log']) >= 2:
            st.markdown('<p style="font-family:\'Syne\',sans-serif;font-weight:700;color:#f5f0e8;margin:20px 0 9px;">📈 Waste Recovery Performance</p>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10,4))
            fig.patch.set_facecolor('#0a1f17'); ax.set_facecolor('#0d3b2e')
            xs = range(len(h['usage_log']))
            ax.plot(xs, h['usage_log'],     label="Total Usage", color="#2ecc85",lw=2.5,marker='o',ms=6)
            ax.plot(xs, h['recovered_log'], label="Recovered",   color="#4fffb0",lw=2,  marker='s',ms=5)
            ax.plot(xs, h['remaining_log'], label="Wasted",      color="#c8a96e",lw=2,  marker='^',ms=5)
            ax.tick_params(colors='#f5f0e8',labelsize=9)
            ax.set_xlabel("Step",color='#f5f0e8'); ax.set_ylabel("kWh",color='#f5f0e8')
            for sp in ['top','right']: ax.spines[sp].set_visible(False)
            for sp in ['left','bottom']: ax.spines[sp].set_color('rgba(46,204,133,.22)')
            ax.grid(True,alpha=.11,color='#2ecc85')
            ax.legend(facecolor='#0d3b2e',edgecolor='rgba(46,204,133,.22)',labelcolor='#f5f0e8',fontsize=9)
            plt.tight_layout(); st.pyplot(fig); plt.close()
    else:
        st.markdown('<div style="text-align:center;padding:36px 14px;background:rgba(13,59,46,.18);border:1px dashed rgba(46,204,133,.2);border-radius:14px;"><p style="font-size:1.8em;margin-bottom:5px;">⚡</p><p style="color:rgba(245,240,232,.46);margin:0;">Enter data above and click <strong style="color:#2ecc85;">Analyse Energy</strong></p></div>', unsafe_allow_html=True)
        h = st.session_state.energy_history_v4
        if h['usage_log']:
            st.dataframe(pd.DataFrame({
                'Step':      range(1, len(h['usage_log'])+1),
                'Usage':     h['usage_log'],
                'Recovered': h['recovered_log'],
                'Wasted':    h['remaining_log'],
            }).tail(10), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="footer"><strong style="color:#2ecc85;">EcoGrid</strong> · Community Energy & Carbon Impact Toolkit<br>Empowering communities with clean energy solutions · © 2024 EcoGrid Team · Built with Streamlit</div>', unsafe_allow_html=True)
