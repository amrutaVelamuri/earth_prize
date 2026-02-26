import streamlit as st
import importlib.util, sys, os
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import streamlit.components.v1 as components

# ============================================================================
# PAGE CONFIG — sidebar hidden entirely
# ============================================================================
st.set_page_config(
    page_title="EcoGrid Toolkit",
    layout="wide",
    page_icon="🌱",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# GLOBAL CSS
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

[data-testid="collapsedControl"]  { display: none !important; }
section[data-testid="stSidebar"]  { display: none !important; }

:root {
    --gd:#0d3b2e; --gm:#1a6b4a; --gb:#2ecc85; --gg:#4fffb0;
    --ea:#c8a96e; --cr:#f0ede8; --dk:#080f0c; --bd:rgba(46,204,133,.18);
    --font-head: 'Plus Jakarta Sans', sans-serif;
    --font-body: 'Inter', sans-serif;
}
html, body, [class*="css"] {
    font-family: var(--font-body);
    -webkit-font-smoothing: antialiased;
    letter-spacing: -0.01em;
}
.main { background: var(--dk); }
.block-container { padding: 1.5rem 2.5rem 4rem; }

.hero-wrap {
    background: linear-gradient(135deg, #0a2e22 0%, #071f17 50%, #040f0b 100%);
    border: 1px solid var(--bd); border-radius: 24px;
    padding: 52px 60px; margin-bottom: 36px;
    position: relative; overflow: hidden;
    display: flex; align-items: center; gap: 40px;
}
.hero-wrap::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 55% 75% at 85% 50%, rgba(46,204,133,.10) 0%, transparent 70%);
    pointer-events: none;
}
.hero-logo-img {
    width: 130px; height: 130px; object-fit: contain; flex-shrink: 0;
    filter: drop-shadow(0 0 20px rgba(46,204,133,0.3)) brightness(1.05);
    position: relative; z-index: 1; border-radius: 16px;
}
.hero-text { position: relative; z-index: 1; }
.hero-logo {
    font-family: var(--font-head); font-size: 5.5em; font-weight: 800;
    color: var(--gb); letter-spacing: -3px; line-height: 1; margin: 0;
}
.hero-logo span { color: var(--ea); }
.hero-tag {
    font-family: var(--font-body); font-size: 1.15em; font-weight: 400;
    color: rgba(240,237,232,.55); margin: 10px 0 0; line-height: 1.5;
}
.hero-badge {
    display: inline-block;
    background: rgba(46,204,133,.10); border: 1px solid rgba(46,204,133,.35);
    color: var(--gb); border-radius: 6px; padding: 4px 12px;
    font-family: var(--font-body); font-size: .72em; font-weight: 600;
    letter-spacing: .08em; text-transform: uppercase; margin-bottom: 16px;
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10,35,25,.7); border-radius: 12px; padding: 4px;
    gap: 2px; border: 1px solid var(--bd); backdrop-filter: blur(12px);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px; padding: 9px 18px; color: rgba(240,237,232,.40);
    font-family: var(--font-body); font-weight: 500; font-size: .83em;
    letter-spacing: .01em; transition: all .2s;
    border: none !important; background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: var(--gb) !important; color: #061a11 !important; font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 28px; min-height: 500px; }
.sh {
    font-family: var(--font-head); font-size: 1.75em; font-weight: 700;
    color: var(--cr); letter-spacing: -0.5px; margin-bottom: 4px; line-height: 1.2;
}
.ss {
    font-family: var(--font-body); color: rgba(240,237,232,.38);
    font-size: .85em; margin-bottom: 22px; font-weight: 400;
}
.al { width: 36px; height: 2px; background: var(--gb); border-radius: 2px; margin-bottom: 18px; }
.stat-card {
    background: linear-gradient(145deg, rgba(26,107,74,.18), rgba(10,35,25,.4));
    border: 1px solid var(--bd); border-radius: 16px; padding: 22px 14px; text-align: center;
}
.sn { font-family: var(--font-head); font-size: 2em; font-weight: 700; color: var(--gb); line-height: 1; }
.sl {
    font-family: var(--font-body); font-size: .72em; font-weight: 500;
    color: rgba(240,237,232,.40); margin-top: 6px; text-transform: uppercase; letter-spacing: .08em;
}
.team-card {
    background: linear-gradient(160deg, rgba(16,52,36,.5), rgba(8,20,14,.6));
    border: 1px solid rgba(46,204,133,.14); border-radius: 20px; padding: 28px 18px; text-align: center;
    transition: transform .25s, border-color .25s, box-shadow .25s;
}
.team-card:hover {
    border-color: rgba(46,204,133,.4); transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,.3);
}
.tav {
    width: 72px; height: 72px; border-radius: 50%; margin: 0 auto 14px;
    border: 1.5px solid rgba(46,204,133,.5);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-head); font-size: 1.3em; font-weight: 700; color: var(--gb);
}
.tn { font-family: var(--font-head); font-size: .95em; font-weight: 600; color: var(--cr); margin-bottom: 4px; }
.tr { font-family: var(--font-body); font-size: .7em; font-weight: 500; color: var(--gb); text-transform: uppercase; letter-spacing: .1em; margin-bottom: 10px; }
.tb { font-family: var(--font-body); font-size: .78em; color: rgba(240,237,232,.42); line-height: 1.6; }
.hw-card {
    background: linear-gradient(145deg, rgba(16,52,36,.4), rgba(8,20,14,.5));
    border: 1px solid var(--bd); border-radius: 14px; padding: 20px; text-align: center;
}
.hi { font-size: 1.9em; margin-bottom: 8px; }
.hl { font-family: var(--font-body); font-size: .78em; font-weight: 600; color: rgba(240,237,232,.7); text-transform: uppercase; letter-spacing: .08em; }
.hon { color: var(--gb); font-size: .88em; font-weight: 600; margin-top: 6px; }
.hwn { color: var(--ea); font-size: .88em; font-weight: 600; margin-top: 6px; }
.hof { color: rgba(240,237,232,.3); font-size: .88em; font-weight: 600; margin-top: 6px; }
.ib {
    background: rgba(10,35,25,.5); border-left: 2px solid var(--gb);
    border-radius: 0 10px 10px 0; padding: 14px 18px; margin: 8px 0;
    color: rgba(240,237,232,.72); font-family: var(--font-body); font-size: .875em; line-height: 1.7;
}
.fp {
    background: rgba(46,204,133,.08); border: 1px solid rgba(46,204,133,.2);
    color: rgba(46,204,133,.9); border-radius: 6px; padding: 4px 11px;
    font-family: var(--font-body); font-size: .76em; font-weight: 500; display: inline-block; margin: 3px 3px;
}
.sr {
    display: flex; align-items: flex-start; gap: 14px;
    background: rgba(10,35,25,.4); border: 1px solid rgba(46,204,133,.12);
    border-radius: 12px; padding: 16px 18px; margin-bottom: 10px;
}
.snum {
    background: var(--gb); color: #061a11; width: 26px; height: 26px; min-width: 26px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-family: var(--font-head); font-weight: 700; font-size: .82em;
}
.sbody h4 { font-family: var(--font-head); color: var(--cr); margin: 0 0 3px; font-size: .88em; font-weight: 600; }
.sbody p { font-family: var(--font-body); color: rgba(240,237,232,.42); margin: 0; font-size: .78em; line-height: 1.6; }
div[data-testid="stMetricValue"] { color: var(--gb) !important; font-family: var(--font-head) !important; font-weight: 700 !important; }
div[data-testid="stMetricLabel"] { color: rgba(240,237,232,.45) !important; font-family: var(--font-body) !important; }
.stButton > button {
    background: var(--gb) !important; color: #061a11 !important;
    font-family: var(--font-body) !important; font-weight: 600 !important; font-size: .88em !important;
    border: none !important; border-radius: 9px !important; padding: 10px 22px !important; transition: all .18s !important;
}
.stButton > button:hover { background: var(--gg) !important; transform: translateY(-2px); }
.stSelectbox label, .stNumberInput label, .stCheckbox label, .stSlider label {
    color: rgba(240,237,232,.65) !important; font-family: var(--font-body) !important; font-size: .85em !important;
}
.footer {
    text-align: center; padding: 28px 0 4px; color: rgba(240,237,232,.22);
    font-family: var(--font-body); font-size: .76em;
    border-top: 1px solid rgba(46,204,133,.1); margin-top: 42px;
}
.pdf-container {
    background: rgba(10,35,25,.4); border: 1px solid rgba(46,204,133,.18);
    border-radius: 16px; padding: 20px; margin-top: 24px;
}
.pdf-header {
    display: flex; align-items: center; gap: 12px; margin-bottom: 16px;
}
.pdf-title {
    font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1em;
    font-weight: 700; color: #f0ede8; margin: 0;
}
.pdf-subtitle {
    font-family: 'Inter', sans-serif; font-size: .78em;
    color: rgba(240,237,232,.42); margin: 2px 0 0;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER — run a page file inside the current tab context
# ============================================================================
def run_page(filepath: str):
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
        err_name = type(e).__name__
        if "StopException" in err_name or "RerunException" in err_name:
            pass
        else:
            st.error(f"Error loading {os.path.basename(filepath)}: {e}")


# ============================================================================
# SESSION STATE
# ============================================================================
_defaults = {
    'geo_data': {},
    'pdf_extracted': {},
    'predictions': {},
    'linked_locations': [],
    'energy_history_v4': {
        'records': [],
        'usage_log': [],
        'recovered_log': [],
        'remaining_log': []
    },
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================================
# LOGO
# ============================================================================
def load_file_b64(path):
    abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    if os.path.exists(abs_path):
        with open(abs_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64     = load_file_b64("logo.png")
textbook_b64 = load_file_b64("EcoGrid Toolkit Textbook.pdf")

# ============================================================================
# HERO
# ============================================================================
if logo_b64:
    st.markdown(f"""
    <div class="hero-wrap">
      <img src="data:image/png;base64,{logo_b64}" class="hero-logo-img" alt="EcoGrid Logo" />
      <div class="hero-text">
        <div class="hero-badge">🌍 EcoGrid Toolkit</div>
        <p class="hero-logo">Eco<span>Grid</span></p>
        <p class="hero-tag">Renewable energy analysis · Carbon impact · Wasted energy recovery · AI-powered monitoring</p>
      </div>
    </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="hero-wrap">
      <div class="hero-text">
        <div class="hero-badge">🌍 EcoGrid Toolkit</div>
        <p class="hero-logo">Eco<span>Grid</span></p>
        <p class="hero-tag">Renewable energy analysis · Carbon impact · Wasted energy recovery · AI-powered monitoring</p>
      </div>
    </div>""", unsafe_allow_html=True)
    st.info("💡 Tip: Place `logo.png` in the same folder as `app.py` to display the logo.", icon="🖼️")

# ============================================================================
# MAIN TABS
# ============================================================================
t1, t2, t3, t4, t5, t6 = st.tabs([
    "👥  Introduction",
    "📚  About & Education",
    "📊  Data & Calculation",
    "🔌  Verification Unit",
    "🏠  Household Energy Status",
    "🔬  System Design",
])
# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — INTRODUCTION
# ══════════════════════════════════════════════════════════════════════════════
with t1:
    st.markdown('<p class="sh">Our Mission</p><div class="al"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ib">EcoGrid is a comprehensive platform that helps communities analyse renewable energy potential, measure environmental impact, and optimise energy consumption. Our toolkit combines AI with practical energy calculations to make clean energy accessible to everyone.</div>', unsafe_allow_html=True)

    for col, (n, l) in zip(st.columns(4), [("5","Modules"), ("3","Energy Sources"), ("122yrs","Training Data"), ("CO₂","Tracked")]):
        col.markdown(f'<div class="stat-card"><div class="sn">{n}</div><div class="sl">{l}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Meet the Team</p><div class="al"></div><p class="ss">Four co-founders united by a mission to make clean energy accessible to every community.</p>', unsafe_allow_html=True)

    TEAM = [
        {"n":"Retina Majumder","r":"Co-Founder · NGGHS '28 · Bangladesh","b":"NGGHS '28 · Bangladesh","img":"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"},
        {"n":"Siyeong Park","r":"Co-Founder · SASPX '28 · China","b":"SASPX '28 · China","img":"/9j/4AAQSkZJRgABAQAAAQABAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAHIAAAAAAQwAABtbnRyUkdCIFhZWiAH4AABAAEAAAAAAABhY3NwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAA9tYAAQAAAADTLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlkZXNjAAAA8AAAACRyWFlaAAABFAAAABRnWFlaAAABKAAAABRiWFlaAAABPAAAABR3dHB0AAABUAAAABRyVFJDAAABZAAAAChnVFJDAAABZAAAAChiVFJDAAABZAAAAChjcHJ0AAABjAAAADxtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEJYWVogAAAAAAAAb6IAADj1AAADkFhZWiAAAAAAAABimQAAt4UAABjaWFlaIAAAAAAAACSgAAAPhAAAts9YWVogAAAAAAAA9tYAAQAAAADTLXBhcmEAAAAAAAQAAAACZmYAAPKnAAANWQAAE9AAAApbAAAAAAAAAABtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACAAAAAcAEcAbwBvAGcAbABlACAASQBuAGMALgAgADIAMAAxADb/2wBDAAUDBAQEAwUEBAQFBQUGBwwIBwcHBw8LCwkMEQ8SEhEPERETFhwXExQaFRERGCEYGh0dHx8fExciJCIeJBweHx7/2wBDAQUFBQcGBw4ICA4eFBEUHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh7/wAARCALoAvQDASIAAhEBAxEB/8QAHQABAAEFAQEBAAAAAAAAAAAAAAIBAwQFBgcICf/EAEsQAAEDAwMCBAQEBAQEBAMGBwEAAhEDBCEFEjEGQSJRYXEHE4GRCDKhsRRCwdEVI1LwM2Jy4SRDgvEWkrI0RHOiwtIXGCZUY4OT/8QAGwEBAQEBAQEBAQAAAAAAAAAAAAECAwQFBgf/xAAwEQEBAAIBBAEEAQMCBgMAAAAAAQIRAwQSITFBBRMiUTIjYXGBoQYUM1KRsTRCYv/aAAwDAQACEQMRAD8A+lkRF5XUREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBFRzg0SjXNcYBkjkIKohcAYJAPqoGtSAneDBiG5P2CC4qLSar1XoemML7y/oUGh21z6roa0+q1lX4ndB0ajKVXqKzFR5hu125px5jgZ7q6qbdci4i8+LXQFpdG3ra2wvaYJptLm+4PcLrdL1TTdVs23mmX1vdW7xLalKoHD9OE1VZSKgc2dsjd5SqgyFAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEUg3uYA8ytde65o1kSK96Hkcikxz9vuQIHuYVGwR5bTpmrVe1lNolznGAPqvKeo/jt07p9StQ0rTbjUKtM7S91RlOmD5zPC8g+I3xwOqUDTvheUXw407a1qMFIH+WXA7j5n9FZjUtfSes9Y6dp9U0WUXVHAbi6o8UmEeYLuR6rnL34nW9EAi1Dg7cJYQ4CP+aYK+Q6fUnTt1YUv8Wv8AVH3D3k1vlnwtB4gHmOec+i5vU9WoUa4q2F5UfIO15pbCfQxiY91vtZ7n2ZdfGvQ7eu22uf4drzBllbeAPIkCJXN9Y/HW0s6j7axFCs5sGnVpgggT6/svju71M3NYuLiA7Dg4k/XzC11W8uA4tdVc4jEz2V7Id1fY+gfHzTLmjt1Jwp3mz/Lpup76dUGfzHlv9FxHWf4gL+1qFmmUfksdTc15pVTk5iDDXQDnnsvnKlfuYWvbMiQZyMq3c3b6lE0nOLgTJP7KzGJuusuviDe3urHUL+lb31QvDyLhm9rjM5B7FaHVNbvby8ddNZSpDktot2tHsFpCAgd4SD9FrURuTqdxdtDa9zUL2D/LqTkeh9F0OhdddUdJ3VC60nXa7A5sH5LnNx/pPErhmuIESVd+aXsDdrSfNTQ+oOhvj5ogpUzrtTWG1y2H1mPa8tcO4wP1n6rv9A/El0k68/hLxt/Xpk+Cv8oNqEf8zRg/RfDzHVKTtzSR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"},
        {"n":"Amruta Velamuri","r":"Co-Founder · RHS '27 · United States","b":"RHS '27 · United States","img":"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"},
        {"n":"Advika Balaji","r":"Co-Founder · WWPHSN '27 · United States","b":"WWPHSN '27 · United States","img":"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"},
    ]
    cols = st.columns(4)
    for col, m in zip(cols, TEAM):
        with col:
            if m["img"]:
                photo_html = '<img src="data:image/png;base64,' + m["img"] + '" style="width:110px;height:110px;border-radius:50%;object-fit:cover;object-position:top;border:2px solid rgba(46,204,133,.5);margin:0 auto 16px;display:block;">'
            else:
                photo_html = '<div style="width:110px;height:110px;border-radius:50%;border:2px solid rgba(46,204,133,.3);margin:0 auto 16px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,rgba(46,204,133,.15),rgba(8,20,14,.8));font-size:2em;">👤</div>'
            st.markdown(
                '<div class="team-card" style="min-height:220px;">' +
                photo_html +
                '<div class="tn">' + m["n"] + '</div>' +
                '<div class="tr">' + m["r"] + '</div>' +
                '</div>',
                unsafe_allow_html=True
            )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">What We Built</p><div class="al"></div>', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1:
        st.markdown("""<div style="background:rgba(13,59,46,.33);border:1px solid rgba(46,204,133,.18);border-radius:15px;padding:20px;">
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;color:#f5f0e8;margin-bottom:10px;">🔋 Energy Analysis</p>
          <span class="fp">Waterfall Hydro</span><span class="fp">Geothermal</span>
          <span class="fp">Waste Recovery</span><span class="fp">Multi-location Grid</span>
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;color:#f5f0e8;margin:14px 0 10px;">🌱 Environmental</p>
          <span class="fp">CO₂ Tracking</span><span class="fp">Tree Equivalency</span><span class="fp">Fossil Comparison</span>
        </div>""", unsafe_allow_html=True)
    with f2:
        st.markdown("""<div style="background:rgba(13,59,46,.33);border:1px solid rgba(46,204,133,.18);border-radius:15px;padding:20px;">
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;color:#f5f0e8;margin-bottom:10px;">🤖 AI & Forecasting</p>
          <span class="fp">Real-time Monitoring</span><span class="fp">Anomaly Detection</span>
          <span class="fp">LSTM Predictions</span><span class="fp">122-year Dataset</span>
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;color:#f5f0e8;margin:14px 0 10px;">📄 Reporting</p>
          <span class="fp">PDF Extraction</span><span class="fp">AI Reports</span><span class="fp">CSV / JSON Export</span>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ABOUT & EDUCATION
# ══════════════════════════════════════════════════════════════════════════════
with t2:
    st.markdown('<p class="sh">How to Use EcoGrid</p><div class="al"></div><p class="ss">Follow the steps below — each module feeds into the next</p>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(200,169,110,.08);border:1px solid rgba(200,169,110,.3);
                border-radius:12px;padding:14px 20px;margin-bottom:24px;">
      <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                color:#c8a96e;font-size:.85em;margin:0 0 10px;
                text-transform:uppercase;letter-spacing:.08em;">⚡ Before You Start — You'll Need</p>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <span style="background:rgba(200,169,110,.12);border:1px solid rgba(200,169,110,.25);
                     color:#c8a96e;border-radius:6px;padding:4px 12px;
                     font-family:Inter,sans-serif;font-size:.78em;font-weight:500;">📍 Location coordinates</span>
        <span style="background:rgba(200,169,110,.12);border:1px solid rgba(200,169,110,.25);
                     color:#c8a96e;border-radius:6px;padding:4px 12px;
                     font-family:Inter,sans-serif;font-size:.78em;font-weight:500;">💧 Waterfall height &amp; flow rate (m³/s)</span>
        <span style="background:rgba(200,169,110,.12);border:1px solid rgba(200,169,110,.25);
                     color:#c8a96e;border-radius:6px;padding:4px 12px;
                     font-family:Inter,sans-serif;font-size:.78em;font-weight:500;">🌡️ Geothermal temp (°C) &amp; depth (km)</span>
        <span style="background:rgba(200,169,110,.12);border:1px solid rgba(200,169,110,.25);
                     color:#c8a96e;border-radius:6px;padding:4px 12px;
                     font-family:Inter,sans-serif;font-size:.78em;font-weight:500;">📄 Technical PDF (optional)</span>
        <span style="background:rgba(200,169,110,.12);border:1px solid rgba(200,169,110,.25);
                     color:#c8a96e;border-radius:6px;padding:4px 12px;
                     font-family:Inter,sans-serif;font-size:.78em;font-weight:500;">🏠 Real-time kWh readings (optional)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    STEPS = [
        {"num":"01","icon":"📄","title":"PDF Analyzer","tab":"Tab 3 → PDF Analyzer","color":"#818cf8",
         "what":"Upload a technical site document",
         "gets":["Auto-extracts coordinates","Pulls waterfall height & flow","Reads geothermal temp & depth"],
         "tip":"Skip this if you already have your specs — go straight to Step 2",
         "unlocks":"Sends data directly to the Calculator"},
        {"num":"02","icon":"🌍","title":"Geographic Calculator","tab":"Tab 3 → Geographic Calculator","color":"#2ecc85",
         "what":"Enter or import your location specs",
         "gets":["Power output (MW)","Annual energy (MWh/yr)","CO₂ saved & homes powered","Waste energy recovered"],
         "tip":"This is the core step — everything else depends on running this first",
         "unlocks":"Populates live map, carbon charts & Verification Unit"},
        {"num":"03","icon":"📈","title":"Time-Series Predictor","tab":"Tab 3 → Time-Series Predictor","color":"#38bdf8",
         "what":"Run the LSTM AI forecast",
         "gets":["Monthly energy predictions","Seasonal climate adjustments","Confidence intervals","Up to 24-month forecast"],
         "tip":"Must run the Calculator first — LSTM uses that data as its base",
         "unlocks":"Exportable CSV / JSON forecast report"},
        {"num":"04","icon":"🔌","title":"Verification Unit","tab":"Tab 4","color":"#f97316",
         "what":"Verify hardware against software output",
         "gets":["Live stats on prototype diagram","Clickable hotspots per component","Component status cards","Real vs calculated comparison"],
         "tip":"Click any component on the diagram to see its live data popup",
         "unlocks":"Visual proof that hardware & software match"},
        {"num":"05","icon":"🏠","title":"Household Energy Monitor","tab":"Tab 5","color":"#c8a96e",
         "what":"Enter real-time kWh readings",
         "gets":["Anomaly detection","AI diagnosis & confidence score","Recovery recommendations","Usage trend chart"],
         "tip":"Works independently — no need to run the Calculator first",
         "unlocks":"Actionable efficiency recommendations"},
    ]

    for s in STEPS:
        gets_html = "".join([
            f'<span style="background:rgba(46,204,133,.08);border:1px solid rgba(46,204,133,.2);'
            f'color:rgba(46,204,133,.9);border-radius:5px;padding:3px 9px;'
            f'font-family:Inter,sans-serif;font-size:.74em;font-weight:500;'
            f'display:inline-block;margin:2px 3px;">{g}</span>'
            for g in s["gets"]
        ])
        st.markdown(f"""
        <div style="background:rgba(13,59,46,.25);border:1px solid rgba(46,204,133,.12);
                    border-left:3px solid {s['color']};border-radius:0 14px 14px 0;
                    padding:18px 20px;margin-bottom:12px;">
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
            <div style="background:linear-gradient(135deg,rgba(46,204,133,.2),rgba(8,20,14,.8));
                        border:1px solid {s['color']}44;border-radius:10px;
                        width:46px;height:46px;display:flex;align-items:center;
                        justify-content:center;font-size:1.3em;flex-shrink:0;">{s['icon']}</div>
            <div style="flex:1;">
              <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                <span style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                             color:#f0ede8;font-size:.95em;">Step {s['num']} · {s['title']}</span>
                <span style="background:{s['color']}22;border:1px solid {s['color']}44;
                             color:{s['color']};border-radius:5px;padding:2px 9px;
                             font-family:Inter,sans-serif;font-size:.7em;font-weight:600;
                             text-transform:uppercase;letter-spacing:.07em;">{s['tab']}</span>
              </div>
              <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.45);
                        font-size:.78em;margin:3px 0 0;">{s['what']}</p>
            </div>
          </div>
          <div style="margin-bottom:10px;">{gets_html}</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start;">
            <div style="background:rgba(200,169,110,.08);border:1px solid rgba(200,169,110,.2);
                        border-radius:7px;padding:5px 10px;flex:1;min-width:180px;">
              <span style="font-family:Inter,sans-serif;font-size:.73em;
                           color:rgba(200,169,110,.8);">💡 {s['tip']}</span>
            </div>
            <div style="background:rgba(46,204,133,.06);border:1px solid rgba(46,204,133,.18);
                        border-radius:7px;padding:5px 10px;flex:1;min-width:180px;">
              <span style="font-family:Inter,sans-serif;font-size:.73em;
                           color:rgba(46,204,133,.7);">🔓 {s['unlocks']}</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:14px;margin:8px 0 24px;">
      <span style="font-family:Inter,sans-serif;font-size:.8em;color:rgba(240,237,232,.3);
                   letter-spacing:.05em;">RECOMMENDED FLOW &nbsp;·&nbsp;</span>
      <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:.82em;
                   color:rgba(46,204,133,.6);font-weight:600;">
        PDF Analyzer → Calculator → LSTM Predictor → Verification Unit → Household Monitor
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<p class="sh">EcoGrid Textbook</p><div class="al"></div><p class="ss">Our full educational reference — read it right here or download below</p>', unsafe_allow_html=True)

    if textbook_b64:
        st.markdown("""
        <div class="pdf-container">
          <div class="pdf-header">
            <span style="font-size:1.6em;">📖</span>
            <div>
              <p class="pdf-title">EcoGrid Toolkit Textbook</p>
              <p class="pdf-subtitle">Scroll inside the viewer · Use the toolbar to zoom or go full-screen</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        pdf_js_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8"/>
          <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ background: #1a1a1a; font-family: Inter, sans-serif; }}
            #controls {{
              display: flex; align-items: center; gap: 10px;
              background: #0d3b2e; padding: 8px 14px;
              border-top: 1px solid rgba(46,204,133,.25);
            }}
            #controls button {{
              background: #2ecc85; color: #061a11; border: none;
              border-radius: 6px; padding: 5px 12px; font-size: 13px;
              font-weight: 600; cursor: pointer;
            }}
            #controls button:hover {{ background: #4fffb0; }}
            #controls span {{ color: rgba(240,237,232,.6); font-size: 13px; }}
            #page-num {{ color: #2ecc85; font-weight: 600; font-size: 13px; min-width: 80px; text-align:center; }}
            #canvas-container {{
              overflow-y: auto; height: 780px;
              display: flex; flex-direction: column; align-items: center;
              gap: 12px; padding: 16px 8px; background: #222;
            }}
            canvas {{
              box-shadow: 0 4px 20px rgba(0,0,0,.5);
              border-radius: 4px; background: white;
              max-width: 100%;
            }}
            #loading {{
              color: #2ecc85; font-size: 15px; padding: 40px;
              text-align: center;
            }}
          </style>
        </head>
        <body>
          <div id="canvas-container">
            <div id="loading">⏳ Loading textbook…</div>
          </div>
          <div id="controls">
            <button onclick="prevPage()">◀ Prev</button>
            <span id="page-num">Loading…</span>
            <button onclick="nextPage()">Next ▶</button>
            <div style="margin-left:auto; display:flex; align-items:center; gap:8px;">
              <button onclick="zoomOut()" title="Zoom out">−</button>
              <span id="zoom-level" style="color:rgba(240,237,232,.6); font-size:12px; min-width:40px; text-align:center;">160%</span>
              <button onclick="zoomIn()" title="Zoom in">+</button>
            </div>
          </div>

          <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
          <script>
            pdfjsLib.GlobalWorkerOptions.workerSrc =
              'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

            const b64 = `{textbook_b64}`;
            const binary = atob(b64);
            const bytes = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);

            let pdfDoc = null;
            let currentPage = 1;
            let currentScale = 1.6;
            const container = document.getElementById('canvas-container');
            const pageNum   = document.getElementById('page-num');
            const zoomLabel = document.getElementById('zoom-level');

            async function renderPage(num) {{
              const page = await pdfDoc.getPage(num);
              const viewport = page.getViewport({{ scale: currentScale }});
              const canvas = document.createElement('canvas');
              canvas.width  = viewport.width;
              canvas.height = viewport.height;
              const ctx = canvas.getContext('2d');
              await page.render({{ canvasContext: ctx, viewport }}).promise;
              return canvas;
            }}

            function zoomIn() {{
              if (currentScale >= 3.0) return;
              currentScale = Math.round((currentScale + 0.2) * 10) / 10;
              zoomLabel.textContent = Math.round(currentScale / 1.6 * 100) + '%';
              rerenderCurrent();
            }}

            function zoomOut() {{
              if (currentScale <= 0.6) return;
              currentScale = Math.round((currentScale - 0.2) * 10) / 10;
              zoomLabel.textContent = Math.round(currentScale / 1.6 * 100) + '%';
              rerenderCurrent();
            }}

            async function rerenderCurrent() {{
              container.innerHTML = '<div id="loading">⏳ Re-rendering…</div>';
              const canvas = await renderPage(currentPage);
              container.innerHTML = '';
              container.appendChild(canvas);
            }}

            async function loadPDF() {{
              try {{
                pdfDoc = await pdfjsLib.getDocument({{ data: bytes }}).promise;
                container.innerHTML = '';
                pageNum.textContent = `Page ${{currentPage}} / ${{pdfDoc.numPages}}`;
                const canvas = await renderPage(currentPage);
                container.appendChild(canvas);
              }} catch(e) {{
                container.innerHTML = `<div id="loading" style="color:#f87171;">❌ Error loading PDF: ${{e.message}}</div>`;
              }}
            }}

            async function prevPage() {{
              if (currentPage <= 1) return;
              currentPage--;
              container.innerHTML = '<div id="loading">⏳ Loading…</div>';
              pageNum.textContent = `Page ${{currentPage}} / ${{pdfDoc.numPages}}`;
              const canvas = await renderPage(currentPage);
              container.innerHTML = '';
              container.appendChild(canvas);
            }}

            async function nextPage() {{
              if (currentPage >= pdfDoc.numPages) return;
              currentPage++;
              container.innerHTML = '<div id="loading">⏳ Loading…</div>';
              pageNum.textContent = `Page ${{currentPage}} / ${{pdfDoc.numPages}}`;
              const canvas = await renderPage(currentPage);
              container.innerHTML = '';
              container.appendChild(canvas);
            }}

            loadPDF();
          </script>
        </body>
        </html>
        """

        components.html(pdf_js_html, height=870, scrolling=False)

        pdf_bytes = base64.b64decode(textbook_b64)
        st.download_button(
            label="⬇️  Download Textbook PDF",
            data=pdf_bytes,
            file_name="EcoGrid Toolkit Textbook.pdf",
            mime="application/pdf",
            use_container_width=False,
        )
    else:
        st.markdown("""
        <div style="border:2px dashed rgba(46,204,133,.26);border-radius:13px;padding:54px 16px;
                    text-align:center;background:rgba(13,59,46,.18);">
          <p style="font-size:2em;margin-bottom:8px;">📄</p>
          <p style="color:rgba(245,240,232,.55);font-size:.95em;margin:0 0 6px;">
            <strong style="color:#2ecc85;">EcoGrid Toolkit Textbook.pdf</strong> not found
          </p>
          <p style="color:rgba(245,240,232,.35);font-size:.82em;margin:0;">
            Place the file in the same folder as <code>app.py</code> and restart the app.
          </p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DATA & CALCULATION
# ══════════════════════════════════════════════════════════════════════════════
with t3:
    st.markdown('<p class="sh">Data & Calculation</p><div class="al"></div>', unsafe_allow_html=True)

    selected_tool = st.radio(
        "Select Tool",
        ["📄  PDF Analyzer", "🌍  Geographic Calculator", "📈  Time-Series Predictor"],
        horizontal=True,
        key="data_calc_tool_selector",
        label_visibility="collapsed"
    )

    st.markdown("---")

    if selected_tool == "📄  PDF Analyzer":
        run_page("pages/1_PDF_Analyzer.py")
    elif selected_tool == "🌍  Geographic Calculator":
        run_page("pages/2_Geographic_Calculator.py")
    elif selected_tool == "📈  Time-Series Predictor":
        run_page("pages/3_Time_Series_Predictor.py")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — VERIFICATION UNIT
# ══════════════════════════════════════════════════════════════════════════════
with t4:
    st.markdown('<p class="sh">Verification Unit</p><div class="al"></div>'
                '<p class="ss">Physical prototype · Live data overlay · Real-time component status</p>',
                unsafe_allow_html=True)

    gd           = st.session_state.get('geo_data', {})
    has_calc     = bool(gd.get('P_total_MW'))
    has_hydro    = bool(gd.get('has_waterfall'))
    has_geo      = bool(gd.get('has_geothermal'))
    has_orc      = has_hydro or has_geo

    p_hydro_mw   = gd.get('P_waterfall_MW', 0)
    p_geo_mw     = gd.get('P_geo_MW', 0)
    p_total_mw   = gd.get('P_total_MW', 0)
    e_orc_mwh    = gd.get('E_waste_recovered_MWh', 0)
    p_orc_mw     = e_orc_mwh / 8760 if e_orc_mwh else 0
    geo_temp     = gd.get('geo_temp', 0)
    depth_km     = gd.get('depth', 0)
    flow_rate    = gd.get('waterfall_flow', 0)
    fall_height  = gd.get('waterfall_height', 0)
    carbon_saved = gd.get('carbon_saved_tons', 0)
    households   = gd.get('households_total', 0)
    loc_name     = gd.get('location_name', '—')
    pipe_mat     = gd.get('pipe_material', '—')

    def hw_card(icon, label, active, val_line, status_txt):
        if active:
            dot_cls = "live-dot"; val_col = "#2ecc85"; stat_cls = "hon"
        elif has_calc:
            dot_cls = "live-dot live-dot-warn"; val_col = "#c8a96e"; stat_cls = "hwn"
        else:
            dot_cls = "live-dot live-dot-off"; val_col = "rgba(240,237,232,.28)"; stat_cls = "hof"
        dot_style = "display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:4px;vertical-align:middle;"
        if "warn" in dot_cls:
            dot_style += "background:#c8a96e;"
        elif "off" in dot_cls:
            dot_style += "background:rgba(240,237,232,.22);"
        else:
            dot_style += "background:#2ecc85;"
        return f"""<div class="hw-card">
          <div class="hi">{icon}</div>
          <div class="hl">{label}</div>
          <div style="font-family:'Inter',sans-serif;font-size:.82em;font-weight:700;
                      color:{val_col};margin-top:5px;">{val_line}</div>
          <div class="{stat_cls}"><span style="{dot_style}"></span>{status_txt}</div>
        </div>"""

    if has_calc:
        hyd_val  = f"{p_hydro_mw:.2f} MW" if has_hydro else "—"
        geo_val  = f"{p_geo_mw:.2f} MW · {geo_temp:.0f}°C" if has_geo else "—"
        orc_val  = f"{p_orc_mw:.3f} MW" if has_orc else "—"
        grd_val  = f"{p_total_mw:.2f} MW total"
        day_val  = "Passive · active"
        hyd_st   = "Active · generating" if has_hydro else "No hydro data"
        geo_st   = "Active · generating" if has_geo   else "No geo data"
        orc_st   = "Capturing waste"     if has_orc   else "No source data"
        grd_st   = "Routing power"
        day_st   = "Sunlight harvesting"
    else:
        hyd_val = geo_val = orc_val = grd_val = day_val = "Run calculator →"
        hyd_st  = geo_st  = orc_st  = grd_st  = day_st  = "Awaiting data"

    c5 = st.columns(5)
    c5[0].markdown(hw_card("💧","Hydro System",   has_hydro, hyd_val, hyd_st), unsafe_allow_html=True)
    c5[1].markdown(hw_card("🌋","Geothermal",     has_geo,   geo_val, geo_st), unsafe_allow_html=True)
    c5[2].markdown(hw_card("♻️","ORC Recovery",   has_orc,   orc_val, orc_st), unsafe_allow_html=True)
    c5[3].markdown(hw_card("⚡","Grid Control",   has_calc,  grd_val, grd_st), unsafe_allow_html=True)
    c5[4].markdown(hw_card("☀️","Daylight Tower", has_calc,  day_val, day_st), unsafe_allow_html=True)

    if not has_calc:
        st.info("💡 Run the **Geographic Calculator** in Tab 3 — live values will populate the diagram and cards above automatically.", icon="📊")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<p class="sh">Physical Prototype</p><div class="al"></div>'
                '<p class="ss">Autodesk Fusion 360 CAD model · Colour-coded by energy type · '
                'Live data from your calculations overlaid below</p>', unsafe_allow_html=True)

    hw_img_b64 = load_file_b64('hardware_diagram.png')

    if hw_img_b64:
        # ── Build overlay labels as plain Python strings (no HTML comments, no CSS classes) ──
        if has_calc:
            # Hydro label
            hydro_border = "rgba(200,169,110,0.55)" if not has_hydro else "rgba(46,204,133,0.55)"
            hydro_dot_bg = "#c8a96e" if not has_hydro else "#2ecc85"
            hydro_val_color = "#c8a96e" if not has_hydro else "#2ecc85"

            # Geo label
            geo_border = "rgba(200,169,110,0.55)" if not has_geo else "rgba(46,204,133,0.55)"
            geo_dot_bg = "#c8a96e" if not has_geo else "#2ecc85"
            geo_val_color = "#c8a96e" if not has_geo else "#2ecc85"

            overlay_html = f"""
            <div style="position:absolute;top:6%;left:2%;
                        background:rgba(6,26,17,0.88);border:1px solid {hydro_border};
                        border-radius:8px;padding:5px 10px;font-family:Inter,sans-serif;
                        font-size:.76em;color:#f0ede8;backdrop-filter:blur(4px);
                        box-shadow:0 2px 12px rgba(0,0,0,.4);white-space:nowrap;z-index:10;line-height:1.5;">
              <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
                           background:{hydro_dot_bg};margin-right:4px;vertical-align:middle;"></span>
              <span style="color:rgba(240,237,232,.45);">Hydro Turbine</span><br>
              <span style="color:{hydro_val_color};font-weight:700;">{p_hydro_mw:.2f} MW</span>
              <span style="color:rgba(240,237,232,.45);"> &middot; {flow_rate} m&sup3;/s &middot; {fall_height} m head</span>
            </div>

            <div style="position:absolute;bottom:20%;left:2%;
                        background:rgba(6,26,17,0.88);border:1px solid {geo_border};
                        border-radius:8px;padding:5px 10px;font-family:Inter,sans-serif;
                        font-size:.76em;color:#f0ede8;backdrop-filter:blur(4px);
                        box-shadow:0 2px 12px rgba(0,0,0,.4);white-space:nowrap;z-index:10;line-height:1.5;">
              <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
                           background:{geo_dot_bg};margin-right:4px;vertical-align:middle;"></span>
              <span style="color:rgba(240,237,232,.45);">Geothermal Well</span><br>
              <span style="color:{geo_val_color};font-weight:700;">{p_geo_mw:.2f} MW</span>
              <span style="color:rgba(240,237,232,.45);"> &middot; {geo_temp:.0f}&deg;C &middot; {depth_km} km &middot; {pipe_mat}</span>
            </div>

            <div style="position:absolute;top:6%;left:50%;transform:translateX(-50%);
                        background:rgba(6,26,17,0.88);border:1px solid rgba(46,204,133,0.55);
                        border-radius:8px;padding:5px 10px;font-family:Inter,sans-serif;
                        font-size:.76em;color:#f0ede8;backdrop-filter:blur(4px);
                        box-shadow:0 2px 12px rgba(0,0,0,.4);white-space:nowrap;z-index:10;line-height:1.5;">
              <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
                           background:#2ecc85;margin-right:4px;vertical-align:middle;"></span>
              <span style="color:rgba(240,237,232,.45);">ORC Recovery</span><br>
              <span style="color:#2ecc85;font-weight:700;">+{p_orc_mw:.3f} MW</span>
              <span style="color:rgba(240,237,232,.45);"> &middot; {e_orc_mwh:,.0f} MWh/yr captured</span>
            </div>

            <div style="position:absolute;top:6%;right:2%;
                        background:rgba(6,26,17,0.88);border:1px solid rgba(46,204,133,0.55);
                        border-radius:8px;padding:5px 10px;font-family:Inter,sans-serif;
                        font-size:.76em;color:#f0ede8;backdrop-filter:blur(4px);
                        box-shadow:0 2px 12px rgba(0,0,0,.4);white-space:nowrap;z-index:10;line-height:1.5;">
              <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
                           background:#2ecc85;margin-right:4px;vertical-align:middle;"></span>
              <span style="color:rgba(240,237,232,.45);">Grid Output</span><br>
              <span style="color:#2ecc85;font-weight:700;">{p_total_mw:.2f} MW</span>
              <span style="color:rgba(240,237,232,.45);"> total dispatched</span>
            </div>

            <div style="position:absolute;bottom:20%;right:2%;
                        background:rgba(6,26,17,0.88);border:1px solid rgba(46,204,133,0.55);
                        border-radius:8px;padding:5px 10px;font-family:Inter,sans-serif;
                        font-size:.76em;color:#f0ede8;backdrop-filter:blur(4px);
                        box-shadow:0 2px 12px rgba(0,0,0,.4);white-space:nowrap;z-index:10;line-height:1.5;">
              <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
                           background:#2ecc85;margin-right:4px;vertical-align:middle;"></span>
              <span style="color:rgba(240,237,232,.45);">Community &middot; {loc_name}</span><br>
              <span style="color:#2ecc85;font-weight:700;">{households:,} homes powered</span><br>
              <span style="color:rgba(240,237,232,.45);">{carbon_saved:,.0f} t CO&sup2;/yr avoided</span>
            </div>
            """
        else:
            overlay_html = """
            <div style="position:absolute;inset:0;display:flex;align-items:center;
                        justify-content:center;pointer-events:none;">
              <div style="background:rgba(6,26,17,0.78);border:1px solid rgba(46,204,133,.25);
                          border-radius:12px;padding:12px 28px;backdrop-filter:blur(4px);text-align:center;">
                <p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:.88em;
                           color:rgba(240,237,232,.4);margin:0;">
                  📊 Run the Geographic Calculator to activate live data overlays
                </p>
              </div>
            </div>"""

        # ── Render using components.html() — image constrained by height so it never clips ──
        IMG_H = 560
        IFRAME_H = IMG_H + 100

        hw_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8"/>
        <style>
          * {{ margin:0; padding:0; box-sizing:border-box; }}
          html, body {{ background:transparent; font-family:Inter,sans-serif; width:100%; }}
          .wrap {{
            background:rgba(10,35,25,.4);
            border:1px solid rgba(46,204,133,.2);
            border-radius:16px;
            padding:16px;
          }}
          .img-container {{
            position:relative;
            height:{IMG_H}px;
            display:flex;
            justify-content:center;
          }}
          .img-container img {{
            height:{IMG_H}px;
            width:auto;
            border-radius:10px;
            display:block;
          }}
          .legend {{
            display:flex; gap:14px; flex-wrap:wrap; margin-top:12px;
          }}
          .legend span {{
            font-family:Inter,sans-serif; font-size:.78em;
            color:rgba(240,237,232,.5); display:flex; align-items:center; gap:5px;
          }}
          .dot {{
            display:inline-block; width:11px; height:11px;
            border-radius:2px; flex-shrink:0;
          }}
          .caption {{
            font-family:Inter,sans-serif; font-size:.73em;
            color:rgba(240,237,232,.28); margin:8px 0 0;
          }}
          .hotspot {{
            position:absolute;
            cursor:pointer;
            border-radius:8px;
            transition: background 0.2s;
          }}
          .hotspot:hover {{
            background:rgba(46,204,133,0.10);
            outline: 2px solid rgba(46,204,133,0.4);
          }}
          .popup {{
            display:none;
            position:absolute;
            top:50%; left:50%;
            transform:translate(-50%,-50%);
            background:rgba(6,26,17,0.97);
            border:1px solid rgba(46,204,133,0.6);
            border-radius:12px;
            padding:16px 20px;
            z-index:100;
            min-width:250px;
            max-width:300px;
            box-shadow:0 8px 32px rgba(0,0,0,0.7);
            font-family:Inter,sans-serif;
          }}
          .popup-title {{
            font-family:'Plus Jakarta Sans',Inter,sans-serif;
            font-size:.95em; font-weight:700; color:#f0ede8;
            margin:0 0 6px; padding-right:20px;
          }}
          .popup-role {{
            font-size:.7em; font-weight:600; text-transform:uppercase;
            letter-spacing:.08em; margin:0 0 10px;
          }}
          .popup-stat {{
            font-size:.8em; color:rgba(240,237,232,.6);
            margin:4px 0; display:flex; justify-content:space-between;
          }}
          .popup-stat span {{ color:#2ecc85; font-weight:600; }}
          .popup-close {{
            position:absolute; top:8px; right:10px;
            background:none; border:none;
            color:rgba(240,237,232,.4); font-size:1em; cursor:pointer;
          }}
          .popup-close:hover {{ color:#f0ede8; }}
          .hint {{
            text-align:center; font-family:Inter,sans-serif;
            font-size:.74em; color:rgba(240,237,232,.3);
            margin-top:8px; letter-spacing:.03em;
          }}
        </style>
        </head>
        <body>
          <div class="wrap">
            <div class="img-container" id="imgContainer">
              <img src="data:image/png;base64,{hw_img_b64}" alt="EcoGrid Hardware Prototype Diagram"/>
              {overlay_html}

              <div class="hotspot" style="top:2%;left:5%;width:38%;height:28%;"
                   onclick="showInfo('hydro')"></div>
              <div class="hotspot" style="top:35%;left:14%;width:16%;height:20%;"
                   onclick="showInfo('geo')"></div>
              <div class="hotspot" style="top:60%;left:8%;width:18%;height:22%;"
                   onclick="showInfo('orc')"></div>
              <div class="hotspot" style="top:40%;left:2%;width:13%;height:18%;"
                   onclick="showInfo('grid')"></div>
              <div class="hotspot" style="top:58%;left:37%;width:16%;height:30%;"
                   onclick="showInfo('daylight')"></div>
              <div class="hotspot" style="top:28%;left:52%;width:42%;height:20%;"
                   onclick="showInfo('dashboard')"></div>
              <div class="hotspot" style="top:48%;left:60%;width:34%;height:40%;"
                   onclick="showInfo('residential')"></div>

              <div class="popup" id="popup">
                <button class="popup-close" onclick="closePopup()">✕</button>
                <div id="popup-content"></div>
              </div>
            </div>
            <p class="hint">💡 Click any component on the diagram to learn more</p>
            <div class="legend">
              <span><span class="dot" style="background:#3b82f6;"></span>Blue = Hydro Power</span>
              <span><span class="dot" style="background:#f97316;"></span>Orange = Geothermal</span>
              <span><span class="dot" style="background:#22c55e;"></span>Green = ORC Recovery</span>
              <span><span class="dot" style="background:#eab308;"></span>Yellow = Main Grid</span>
              <span><span class="dot" style="background:#ef4444;"></span>Red = Safety System</span>
            </div>
            <p class="caption">CAD model built in Autodesk Fusion 360 · Physical prototype by EcoGrid Team</p>
          </div>

          <script>
            const DATA = {{
              hydro: {{
                title: "💧 Hydro System",
                role: "Primary Generation",
                color: "#3b82f6",
                stats: [
                  ["Power Output", "{p_hydro_mw:.2f} MW"],
                  ["Flow Rate", "{flow_rate} m³/s"],
                  ["Head Height", "{fall_height} m"],
                  ["Status", "{('Active' if has_hydro else 'No data')}"]
                ],
                desc: "Waterfall-driven turbines convert kinetic energy of falling water into electricity continuously."
              }},
              geo: {{
                title: "🌋 Geothermal Plant",
                role: "Primary Generation",
                color: "#f97316",
                stats: [
                  ["Power Output", "{p_geo_mw:.2f} MW"],
                  ["Temperature", "{geo_temp:.0f}°C"],
                  ["Depth", "{depth_km} km"],
                  ["Pipe Material", "{pipe_mat}"]
                ],
                desc: "Extracts Earth's internal heat via deep wells. Runs 24/7 regardless of weather."
              }},
              orc: {{
                title: "♻️ ORC Recovery",
                role: "Waste Heat Capture",
                color: "#22c55e",
                stats: [
                  ["Recovered", "{p_orc_mw:.3f} MW"],
                  ["Annual Capture", "{e_orc_mwh:,.0f} MWh/yr"],
                  ["Efficiency", "80% of waste heat"],
                  ["Status", "Always ON"]
                ],
                desc: "Organic Rankine Cycle unit captures thermal losses from Hydro & Geothermal, converting them back into electricity."
              }},
              grid: {{
                title: "⚡ Grid Control Center",
                role: "Power Distribution",
                color: "#eab308",
                stats: [
                  ["Total Routed", "{p_total_mw:.2f} MW"],
                  ["Homes Powered", "{households:,}"],
                  ["CO₂ Avoided", "{carbon_saved:,.0f} t/yr"],
                  ["Location", "{loc_name}"]
                ],
                desc: "Central hub routing electricity from all sources to consumers. Manages load balancing and stability."
              }},
              daylight: {{
                title: "☀️ Daylight Tower",
                role: "Passive Energy Saving",
                color: "#2ecc85",
                stats: [
                  ["Type", "Passive mirror system"],
                  ["Function", "Sunlight redirection"],
                  ["Benefit", "Cuts lighting demand"],
                  ["Status", "Weather dependent"]
                ],
                desc: "Redirects natural sunlight into buildings, reducing artificial lighting load and overall electricity consumption."
              }},
              dashboard: {{
                title: "📊 City Energy Dashboard",
                role: "Monitoring & Display",
                color: "#818cf8",
                stats: [
                  ["Tracks", "Real-time generation"],
                  ["Alerts", "Anomaly detection"],
                  ["Data", "Live kWh readings"],
                  ["Link", "Tab 5 in app"]
                ],
                desc: "Displays real-time generation and consumption across the city grid so operators can track system health."
              }},
              residential: {{
                title: "🏘️ Residential Area",
                role: "Energy Consumer",
                color: "#d97706",
                stats: [
                  ["Homes Powered", "{households:,}"],
                  ["People Served", "{households * 4:,}"],
                  ["Energy Source", "100% renewable"],
                  ["Location", "{loc_name}"]
                ],
                desc: "End users receiving clean renewable electricity from the grid — homes and buildings in the community."
              }}
            }};

            function showInfo(key) {{
              const d = DATA[key];
              if (!d) return;
              let statsHtml = d.stats.map(([k, v]) =>
                `<div class="popup-stat">${{k}}<span>${{v}}</span></div>`
              ).join('');
              document.getElementById('popup-content').innerHTML = `
                <p class="popup-title">${{d.title}}</p>
                <p class="popup-role" style="color:${{d.color}}">${{d.role}}</p>
                ${{statsHtml}}
                <p style="font-size:.75em;color:rgba(240,237,232,.4);margin-top:10px;line-height:1.5;">${{d.desc}}</p>
              `;
              document.getElementById('popup').style.display = 'block';
            }}

            function closePopup() {{
              document.getElementById('popup').style.display = 'none';
            }}

            // Close popup if clicking outside
            document.getElementById('imgContainer').addEventListener('click', function(e) {{
              if (!e.target.classList.contains('hotspot') && e.target.id !== 'popup' && !e.target.closest('#popup')) {{
                closePopup();
              }}
            }});
          </script>
        </body>
        </html>
        """

        components.html(hw_html, height=IFRAME_H, scrolling=False)

    else:
        st.info("Place hardware_diagram.png in the same folder as app.py")

    # ── Live summary metrics ──────────────────────────────────────────────────
    if has_calc:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="sh" style="font-size:1.2em;">📡 Live Calculation Summary</p><div class="al"></div>', unsafe_allow_html=True)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Hydro Output",   f"{p_hydro_mw:.2f} MW",      delta="Active" if has_hydro else "No data")
        m2.metric("Geo Output",     f"{p_geo_mw:.2f} MW",        delta="Active" if has_geo   else "No data")
        m3.metric("ORC Recovered",  f"{p_orc_mw:.3f} MW",        delta="Always ON")
        m4.metric("Total to Grid",  f"{p_total_mw:.2f} MW",      delta=f"{households:,} homes")
        m5.metric("CO₂ Avoided",    f"{carbon_saved:,.0f} t/yr", delta="vs fossil fuel")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Component breakdown ───────────────────────────────────────────────────
    st.markdown('<p class="sh">Component Breakdown</p><div class="al"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        for name, colour, role, detail in [
            ("💧 Hydro System",         "#3b82f6", "Primary Generation",    "Waterfall-driven turbines generate the bulk of electricity. Water flow rate and height determine output power."),
            ("🌋 Geothermal Plant",      "#f97316", "Primary Generation",    "Extracts heat from deep underground. Temperature differential drives a generator via steam turbine."),
            ("♻️ ORC Recovery",          "#22c55e", "Waste Heat Capture",    "Organic Rankine Cycle unit captures thermal losses from both Hydro and Geothermal that would otherwise be wasted, converting them back into electricity."),
        ]:
            live = ""
            if has_calc:
                if "Hydro" in name and has_hydro:
                    live = f' <span style="color:#2ecc85;font-size:.73em;">· {p_hydro_mw:.2f} MW · {flow_rate} m³/s · {fall_height} m</span>'
                elif "Geo" in name and has_geo:
                    live = f' <span style="color:#2ecc85;font-size:.73em;">· {p_geo_mw:.2f} MW · {geo_temp:.0f}°C · {depth_km} km</span>'
                elif "ORC" in name and has_orc:
                    live = f' <span style="color:#2ecc85;font-size:.73em;">· +{p_orc_mw:.3f} MW · {e_orc_mwh:,.0f} MWh/yr</span>'
            st.markdown(f'''<div style="background:rgba(13,59,46,.25);border-left:3px solid {colour};border-radius:0 10px 10px 0;padding:13px 16px;margin-bottom:10px;">
              <p style="color:#f5f0e8;font-weight:700;font-size:.9em;margin:0 0 2px;">{name}{live}</p>
              <p style="color:{colour};font-size:.72em;font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin:0 0 5px;">{role}</p>
              <p style="color:rgba(245,240,232,.48);font-size:.8em;margin:0;line-height:1.6;">{detail}</p>
            </div>''', unsafe_allow_html=True)
    with c2:
        for name, colour, role, detail in [
            ("⚡ Grid Control Center",  "#eab308", "Power Distribution",    "The central hub that receives electricity from all sources and intelligently routes it to consumers and the city dashboard."),
            ("📊 City Energy Dashboard","#818cf8", "Monitoring & Display",  "Displays real-time generation and consumption data across the city grid, enabling operators to track system health."),
            ("🏘️ Residential Area",     "#d97706", "Energy Consumer",       "Represents the end users — homes and buildings that receive clean renewable electricity from the grid."),
            ("☀️ Daylight Tower",        "#2ecc85", "Passive Energy Saving", "Mirrors and redirects natural sunlight into buildings, cutting artificial lighting demand and reducing overall electricity consumption."),
        ]:
            live = ""
            if has_calc:
                if "Grid Control" in name:
                    live = f' <span style="color:#2ecc85;font-size:.73em;">· {p_total_mw:.2f} MW routed</span>'
                elif "Residential" in name:
                    live = f' <span style="color:#2ecc85;font-size:.73em;">· {households:,} homes · {loc_name}</span>'
            st.markdown(f'''<div style="background:rgba(13,59,46,.25);border-left:3px solid {colour};border-radius:0 10px 10px 0;padding:13px 16px;margin-bottom:10px;">
              <p style="color:#f5f0e8;font-weight:700;font-size:.9em;margin:0 0 2px;">{name}{live}</p>
              <p style="color:{colour};font-size:.72em;font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin:0 0 5px;">{role}</p>
              <p style="color:rgba(245,240,232,.48);font-size:.8em;margin:0;line-height:1.6;">{detail}</p>
            </div>''', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — HOUSEHOLD ENERGY STATUS
# ══════════════════════════════════════════════════════════════════════════════
with t5:
    st.markdown('<p class="sh">Household Energy Status</p><div class="al"></div><p class="ss">EnergyGuard AI · Keen Edition V4 · Real-time monitoring & optimisation</p>', unsafe_allow_html=True)

    class EnergyRecord:
        def __init__(self, u, e, s, t, sl, tmp):
            self.usage        = u
            self.expected     = e
            self.sector       = s
            self.time_of_day  = t
            self.sunlight     = sl
            self.temperature  = tmp

    def eg_ratio(r):
        return r.usage / r.expected if r.expected else 0

    def eg_anomaly(h):
        return len(h['usage_log']) >= 2 and h['usage_log'][-1] > h['usage_log'][-2] * 1.25

    def eg_alert(rt, an):
        if rt >= 1.35 or an:
            return "CRITICAL"
        elif rt >= 1.15:
            return "WARNING"
        return "NORMAL"

    def eg_score(rt):
        return round(max(0, min(100, 100 - abs(rt - 1) * 75)), 1)

    def eg_recovery(r):
        w   = 0.3 * r.usage
        rec = 0.8 * w
        return round(rec, 2), round(w - rec, 2)

    def eg_ai(r, rt, an, al, rec):
        reasons, actions, conf = [], [], 30
        reasons.append(f"Usage is {rt:.2f}× expected")
        if an:
            reasons.append("Abnormal spike detected"); conf += 15
        if r.temperature > 30:
            reasons.append("High temp — cooling load increased"); conf += 10
        if r.sunlight and r.time_of_day.lower() == "day":
            reasons.append("Sunlight available but underutilised"); conf += 15
        if r.sector.lower() in ["factory", "power plant"]:
            reasons.append("High recoverable industrial losses"); conf += 15

        actions.append(("HIGH",  f"Continuously recover wasted electricity (~{rec[0]} kWh)"))
        actions.append(("HIGH",  f"System stability reserve (~{rec[1]} kWh)"))
        if an:
            actions.append(("IMMEDIATE", "Activate Null Line — capture leakage"))
        if al == "CRITICAL":
            actions.append(("IMMEDIATE", "Reduce non-essential loads"))
            actions.append(("HIGH",      "Shift base load to geothermal/renewable"))
            if r.sunlight:
                actions.append(("IMMEDIATE", "Activate Smart Daylight-Mirroring System"))
        elif al == "WARNING":
            actions.append(("MEDIUM", "Optimise operating schedule"))
        else:
            actions.append(("LOW", "System operating optimally"))

        return reasons, actions, min(100, conf)

    with st.form("hh_energy_form"):
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f5f0e8;font-size:.94em;margin-bottom:13px;">📊 Enter Energy Reading</p>', unsafe_allow_html=True)
        fi1, fi2 = st.columns(2)
        with fi1:
            usage_v    = st.number_input("Energy usage (kWh)",   min_value=0.0,  step=0.1, value=5.0)
            expected_v = st.number_input("Expected usage (kWh)", min_value=0.01, step=0.1, value=4.0)
            sector_v   = st.selectbox("Sector", ["Home", "Factory", "Power Plant"])
        with fi2:
            tod_v  = st.selectbox("Time of Day", ["Day", "Night"])
            sun_v  = st.checkbox("Sunlight available?", value=True)
            temp_v = st.number_input("Temperature (°C)", step=0.1, value=25.0)
        sub = st.form_submit_button("🔍 Analyse Energy", use_container_width=True)

    if sub:
        rec_obj = EnergyRecord(usage_v, expected_v, sector_v, tod_v, sun_v, temp_v)
        rt  = eg_ratio(rec_obj)
        an  = eg_anomaly(st.session_state.energy_history_v4)
        al  = eg_alert(rt, an)
        sc  = eg_score(rt)
        rv  = eg_recovery(rec_obj)

        h = st.session_state.energy_history_v4
        h['records'].append(rec_obj)
        h['usage_log'].append(usage_v)
        h['recovered_log'].append(rv[0])
        h['remaining_log'].append(rv[1])

        if al == "CRITICAL":
            st.error("🔴 CRITICAL — Immediate optimisation required!")
        elif al == "WARNING":
            st.warning("🟡 WARNING — Efficiency dropping")
        else:
            st.success("🟢 NORMAL — System operating optimally")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Usage Ratio",      f"{rt:.2f}×")
        m2.metric("Efficiency Score", f"{sc}/100")
        m3.metric("Recovered",        f"{rv[0]} kWh")
        m4.metric("Wasted",           f"{rv[1]} kWh")

        reasons, actions, conf = eg_ai(rec_obj, rt, an, al, rv)

        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#2ecc85;margin:18px 0 7px;">🤖 AI Diagnosis</p>', unsafe_allow_html=True)
        for rr in reasons:
            st.markdown(f'<div class="ib">• {rr}</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:rgba(245,240,232,.44);font-size:.83em;">Confidence: <strong style="color:#2ecc85;">{conf}%</strong></p>', unsafe_allow_html=True)

        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#2ecc85;margin:16px 0 7px;">🛠️ Recommended Actions</p>', unsafe_allow_html=True)
        for lvl, act in actions:
            if lvl == "IMMEDIATE":
                st.error(f"🚨 **[{lvl}]** {act}")
            elif lvl == "HIGH":
                st.warning(f"⚠️ **[{lvl}]** {act}")
            elif lvl == "MEDIUM":
                st.info(f"ℹ️ **[{lvl}]** {act}")
            else:
                st.success(f"✅ **[{lvl}]** {act}")

        if len(h['usage_log']) >= 2:
            st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f5f0e8;margin:20px 0 9px;">📈 Waste Recovery Performance</p>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(10, 4))
            fig.patch.set_facecolor('#0a1f17')
            ax.set_facecolor('#0d3b2e')
            xs = range(len(h['usage_log']))
            ax.plot(xs, h['usage_log'],     label="Total Usage", color="#2ecc85", lw=2.5, marker='o', ms=6)
            ax.plot(xs, h['recovered_log'], label="Recovered",   color="#4fffb0", lw=2,   marker='s', ms=5)
            ax.plot(xs, h['remaining_log'], label="Wasted",      color="#c8a96e", lw=2,   marker='^', ms=5)
            ax.tick_params(colors='#f5f0e8', labelsize=9)
            ax.set_xlabel("Step",  color='#f5f0e8')
            ax.set_ylabel("kWh",   color='#f5f0e8')
            for sp in ['top', 'right']:
                ax.spines[sp].set_visible(False)
            for sp in ['left', 'bottom']:
                ax.spines[sp].set_color((46/255, 204/255, 133/255, 0.22))
            ax.grid(True, alpha=.11, color='#2ecc85')
            ax.legend(facecolor='#0d3b2e', edgecolor=(46/255, 204/255, 133/255, 0.22), labelcolor='#f5f0e8', fontsize=9)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

    else:
        st.markdown('<div style="text-align:center;padding:36px 14px;background:rgba(13,59,46,.18);border:1px dashed rgba(46,204,133,.2);border-radius:14px;"><p style="font-size:1.8em;margin-bottom:5px;">⚡</p><p style="color:rgba(245,240,232,.46);margin:0;">Enter data above and click <strong style="color:#2ecc85;">Analyse Energy</strong></p></div>', unsafe_allow_html=True)

        h = st.session_state.energy_history_v4
        if h['usage_log']:
            st.dataframe(pd.DataFrame({
                'Step':      range(1, len(h['usage_log']) + 1),
                'Usage':     h['usage_log'],
                'Recovered': h['recovered_log'],
                'Wasted':    h['remaining_log'],
            }).tail(10), use_container_width=True)
# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — SYSTEM DESIGN
# ══════════════════════════════════════════════════════════════════════════════
with t6:
    st.markdown('<p class="sh">Green Energy Systems: Detailed Design</p><div class="al"></div><p class="ss">The science, engineering, and AI integration behind each of the four EcoGrid technologies</p>', unsafe_allow_html=True)

    sys_tab1, sys_tab2, sys_tab3, sys_tab4, sys_tab5, sys_tab6 = st.tabs([
        "🌋 Geothermal",
        "💧 Waterfall Turbines",
        "♻️ Waste Recovery",
        "☀️ Daylight Mirroring",
        "🏭 Integrated Center",
        "🌍 SDG Alignment",
    ])

    # ── GEOTHERMAL ────────────────────────────────────────────────────────────
    with sys_tab1:
        st.markdown("""
        <div style="background:rgba(249,115,22,.07);border:1px solid rgba(249,115,22,.25);
                    border-radius:14px;padding:20px 24px;margin-bottom:20px;">
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                    color:#f97316;font-size:1.05em;margin:0 0 8px;">Core Concept</p>
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.7);
                    font-size:.88em;line-height:1.7;margin:0;">
            Deep boreholes 3–10 km into the Earth reach hot dry rock zones where temperatures 
            range from 150°C to 900°C. A dual-loop heat transfer system extracts this energy 
            continuously — day and night, regardless of weather — and converts it to electricity 
            via a turbine-generator. AI monitors every stage in real time.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.95em;margin-bottom:12px;">⚙️ System Steps</p>', unsafe_allow_html=True)

        steps = [
            ("01", "Deep Borehole Drilling", "Boreholes reach hot dry rock zones or underground reservoirs. Pipe material is selected based on temperature to minimise heat loss and prevent failure. AI monitors temperature, pressure, and stress continuously, predicting failures before they occur."),
            ("02", "Heat Transfer Loop — Primary (Downhole Circuit)", "Cold water or specialised working fluid (CO₂ or ammonia-water mixtures) is injected down the borehole. As it travels through hot rocks it absorbs heat and rises as superheated fluid or steam through the production well."),
            ("03", "Heat Transfer Loop — Secondary (Surface Plant Circuit)", "Superheated fluid passes through a heat exchanger, transferring energy to a secondary closed-loop working fluid that boils at a lower temperature, creating high-pressure steam. This dual-loop design prevents contamination and mineral scaling by keeping underground water separate from the turbine system."),
            ("04", "Steam to Electricity", "High-pressure steam drives a turbine-generator converting heat → mechanical energy → electricity. AI-controlled valves continuously adjust flow to maintain optimal turbine efficiency and match geothermal output with waste recovery, storage, and national grid demands."),
            ("05", "Re-Injection", "Cooled water is pumped back underground, maintaining reservoir pressure and preserving the resource so the system can run sustainably for decades."),
            ("06", "AI Integration", "AI optimises temperature, pressure, and fluid flow; monitors pipe stress and predicts replacements; balances energy demand matching across systems; activates automatic shutoff valves and fail-safes for overheating, leaks, or earthquakes."),
        ]

        for num, title, desc in steps:
            st.markdown(f"""
            <div style="display:flex;gap:14px;align-items:flex-start;
                        background:rgba(13,59,46,.25);border:1px solid rgba(249,115,22,.12);
                        border-radius:12px;padding:14px 18px;margin-bottom:10px;">
              <div style="background:#f97316;color:#061a11;width:28px;height:28px;min-width:28px;
                          border-radius:50%;display:flex;align-items:center;justify-content:center;
                          font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;font-size:.8em;">
                {num}
              </div>
              <div>
                <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                          color:#f0ede8;font-size:.88em;margin:0 0 4px;">{title}</p>
                <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.5);
                          font-size:.8em;margin:0;line-height:1.6;">{desc}</p>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.95em;margin-bottom:12px;">🌡️ Pipe Material by Temperature</p>', unsafe_allow_html=True)

        import pandas as pd
        pipe_df = pd.DataFrame({
            "Temperature Range": ["150–300°C", "300–600°C", "600–900°C"],
            "Material": ["Stainless Steel / Incoloy", "Inconel / Nickel-Chromium Composites", "Ceramic Composites / SiC / Titanium Alloys"],
            "Specification": ["Durable and corrosion-resistant", "High thermal and mechanical stability", "Resistant to extreme heat and pressure"],
        })
        st.dataframe(pipe_df, use_container_width=True, hide_index=True)

        st.markdown("""
        <div style="background:rgba(46,204,133,.07);border:1px solid rgba(46,204,133,.2);
                    border-radius:10px;padding:14px 18px;margin-top:16px;">
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.6);font-size:.82em;margin:0;line-height:1.7;">
            <strong style="color:#2ecc85;">Why it matters:</strong> Wrong pipe material at high temperatures 
            causes rapid corrosion and catastrophic failure within months. The correct material — automatically 
            recommended by the EcoGrid calculator — signals engineering credibility to development banks and 
            climate finance institutions reviewing funding applications.
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── WATERFALL TURBINES ────────────────────────────────────────────────────
    with sys_tab2:
        st.markdown("""
        <div style="background:rgba(59,130,246,.07);border:1px solid rgba(59,130,246,.25);
                    border-radius:14px;padding:20px 24px;margin-bottom:20px;">
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                    color:#3b82f6;font-size:1.05em;margin:0 0 8px;">Core Concept</p>
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.7);
                    font-size:.88em;line-height:1.7;margin:0;">
            Turbines attach directly to mountain slopes at the base of natural waterfalls — no dam, 
            no reservoir, no river diversion. AI-controlled adjustable blades continuously optimise 
            energy capture as flow varies across seasons. Water passes through and returns to the 
            river immediately downstream, leaving the ecosystem intact.
          </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">📐 Power Formula</p>', unsafe_allow_html=True)
            st.markdown("""
            <div style="background:rgba(13,59,46,.4);border:1px solid rgba(59,130,246,.2);
                        border-radius:12px;padding:18px;text-align:center;">
              <p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.3em;
                        font-weight:700;color:#3b82f6;margin:0 0 12px;">P = ρ · g · Q · H · η</p>
              <div style="font-family:Inter,sans-serif;font-size:.78em;color:rgba(240,237,232,.5);text-align:left;">
                <p style="margin:3px 0;">ρ = 1000 kg/m³ — water density</p>
                <p style="margin:3px 0;">g = 9.81 m/s²</p>
                <p style="margin:3px 0;">Q = flow rate (m³/s)</p>
                <p style="margin:3px 0;">H = waterfall height (m)</p>
                <p style="margin:3px 0;">η = turbine + generator efficiency</p>
              </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">📊 Example Calculation</p>', unsafe_allow_html=True)
            st.markdown("""
            <div style="background:rgba(13,59,46,.4);border:1px solid rgba(59,130,246,.2);
                        border-radius:12px;padding:18px;">
              <p style="font-family:Inter,sans-serif;font-size:.8em;color:rgba(240,237,232,.4);margin:0 0 10px;">
                Q = 10 m³/s · H = 50 m · η = 0.9
              </p>
              <p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.15em;
                        font-weight:700;color:#2ecc85;margin:0 0 5px;">P ≈ 4.41 MW</p>
              <p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.05em;
                        font-weight:700;color:#2ecc85;margin:0 0 5px;">38,630 MWh/year</p>
              <p style="font-family:Inter,sans-serif;font-size:.78em;
                        color:rgba(240,237,232,.4);margin:0;">≈ 5,370 families powered annually</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">🔧 Component Materials</p>', unsafe_allow_html=True)

        materials_df = pd.DataFrame({
            "Component": ["Turbine Blades", "Turbine Housing", "Sensor Casings", "Mounting Anchors"],
            "Material / Specification": [
                "Stainless steel, Inconel, coated alloys",
                "Reinforced steel with anti-corrosion coating",
                "Waterproof polymer / stainless steel",
                "Rock anchors / concrete and steel foundations",
            ],
            "Efficiency Advantage": [
                "Minimal wear, high energy capture",
                "Reduces mechanical losses",
                "Reliable, continuous monitoring",
                "Stable energy conversion",
            ],
        })
        st.dataframe(materials_df, use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">🤖 AI Functions</p>', unsafe_allow_html=True)

        ai_funcs = [
            ("Real-Time Flow Analysis", "Ultrasonic and pitot sensors feed live data. AI calculates optimal blade pitch for maximum energy capture at any flow rate."),
            ("Predictive Maintenance", "Monitors wear, vibration, and corrosion trends. Predicts blade, bearing, and housing replacements before failures occur, saving costs and reducing downtime."),
            ("Adaptive Efficiency", "Continuously adjusts blade angles and generator load to maintain peak output as waterfall conditions change — even during floods or low flow."),
            ("Safety Monitoring", "Tracks rainfall, debris flow, and vibration. Activates emergency stops automatically if dangerous conditions are detected. Acts instantly to override delays."),
            ("Remote Operations", "Engineers receive real-time AI diagnostics and recommendations, enabling safe adjustments from anywhere in the world. Guides robotic or rope-based maintenance interventions."),
        ]

        for title, desc in ai_funcs:
            st.markdown(f"""
            <div class="ib" style="margin-bottom:8px;">
              <strong style="color:#3b82f6;">{title}:</strong> {desc}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">⚠️ Technical Challenges & AI Solutions</p>', unsafe_allow_html=True)

        challenges_df = pd.DataFrame({
            "Challenge": [
                "Structural anchoring",
                "Corrosion & wear",
                "Flow variability",
                "Sensing & communication",
                "Control latency & safety",
                "Maintenance access",
            ],
            "AI-Integrated Solution": [
                "AI monitors stress and load on anchors; alerts for reinforcement before failure",
                "Predictive AI schedules modular blade replacement before failures occur",
                "AI adjusts blade angles in real time for optimum capture under any conditions",
                "AI integrates data from ultrasonic/pitot sensors, solar-powered IoT devices, LoRa/satellite",
                "AI acts instantly, overriding latency delays to prevent accidents",
                "AI predicts maintenance needs and guides robotic or rope-based interventions remotely",
            ],
        })
        st.dataframe(challenges_df, use_container_width=True, hide_index=True)

        st.markdown("""
        <div style="background:rgba(46,204,133,.07);border:1px solid rgba(46,204,133,.2);
                    border-radius:10px;padding:14px 18px;margin-top:16px;">
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.6);font-size:.82em;margin:0;line-height:1.7;">
            <strong style="color:#2ecc85;">No dam advantage:</strong> Traditional dam projects displace communities, 
            flood ecosystems, and take 5–10 years to build. Run-of-river turbines are operational in 18–24 months, 
            require no land flooding, and can be fully removed at end of life — leaving the site in its natural state.
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── WASTE RECOVERY ────────────────────────────────────────────────────────
    with sys_tab3:
        st.markdown("""
        <div style="background:rgba(34,197,94,.07);border:1px solid rgba(34,197,94,.25);
                    border-radius:14px;padding:20px 24px;margin-bottom:20px;">
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                    color:#22c55e;font-size:1.05em;margin:0 0 8px;">Core Concept</p>
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.7);
                    font-size:.88em;line-height:1.7;margin:0;">
            Every electricity network loses a portion of energy as heat — this is unavoidable under 
            the laws of thermodynamics. This multi-line recovery network intercepts that wasted 
            electricity and heat, converts it via an Organic Rankine Cycle unit, and feeds it back 
            into the grid — producing additional electricity from what the primary systems would 
            otherwise discard.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:12px;">🔌 The Four-Line System</p>', unsafe_allow_html=True)

        lines = [
            ("#3b82f6", "First Line — Electricity Supply", "Main supply line delivering power to homes, factories, and consumers. Acts as the source from which recoverable energy is detected and diverted."),
            ("#22c55e", "Second Line — Wasted Electricity Recovery", "At the junction between lines 1 and 2, an automated door with an ultrasonic mini-calculator detects recoverable energy and opens to divert it. A resistive heater inside converts the collected electricity into stored thermal energy."),
            ("#f97316", "Third Line — Heat Transfer to ORC", "Transfers heat from the resistive heater to an Organic Rankine Cycle system where it is converted back into usable electricity and returned to the grid."),
            ("#a855f7", "Multi-Faced Null Line — Leak Recovery", "Inactive until sensors detect voltage leakage anywhere in the network. Activates automatically to route leaked electricity back into the second line, ensuring zero waste from unexpected losses."),
        ]

        for colour, title, desc in lines:
            st.markdown(f"""
            <div style="border-left:3px solid {colour};background:rgba(13,59,46,.25);
                        border-radius:0 12px 12px 0;padding:14px 18px;margin-bottom:10px;">
              <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                        color:#f0ede8;font-size:.88em;margin:0 0 4px;">{title}</p>
              <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.5);
                        font-size:.8em;margin:0;line-height:1.6;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">🌡️ Thermal Recovery at Turbines & Generators</p>', unsafe_allow_html=True)

        st.markdown("""
        <div class="ib">
          The largest energy losses in the entire system occur at turbines and industrial generators. 
          To capture these, <strong style="color:#2ecc85;">ORC Thermal Recovery Lines</strong> are added 
          directly at points of thermal loss — heat is collected and converted into electricity, then returned 
          to the Second Line, forming a fully integrated, AI-controlled energy optimisation loop. This means 
          the biggest source of waste in the system becomes an additional generation source.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style="background:rgba(13,59,46,.4);border:1px solid rgba(34,197,94,.2);
                        border-radius:12px;padding:16px;text-align:center;">
              <p style="font-family:Inter,sans-serif;font-size:.73em;color:rgba(240,237,232,.4);margin:0 0 6px;">
                Waste from primary systems
              </p>
              <p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.5em;
                        font-weight:700;color:#22c55e;margin:0;">~30%</p>
              <p style="font-family:Inter,sans-serif;font-size:.73em;color:rgba(240,237,232,.4);margin:4px 0 0;">
                of gross output lost as heat
              </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background:rgba(13,59,46,.4);border:1px solid rgba(34,197,94,.2);
                        border-radius:12px;padding:16px;text-align:center;">
              <p style="font-family:Inter,sans-serif;font-size:.73em;color:rgba(240,237,232,.4);margin:0 0 6px;">
                Captured by ORC recovery
              </p>
              <p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.5em;
                        font-weight:700;color:#2ecc85;margin:0;">80%</p>
              <p style="font-family:Inter,sans-serif;font-size:.73em;color:rgba(240,237,232,.4);margin:4px 0 0;">
                of that waste converted back
              </p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background:rgba(13,59,46,.4);border:1px solid rgba(34,197,94,.2);
                        border-radius:12px;padding:16px;text-align:center;">
              <p style="font-family:Inter,sans-serif;font-size:.73em;color:rgba(240,237,232,.4);margin:0 0 6px;">
                Effective additional output
              </p>
              <p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.5em;
                        font-weight:700;color:#2ecc85;margin:0;">+24%</p>
              <p style="font-family:Inter,sans-serif;font-size:.73em;color:rgba(240,237,232,.4);margin:4px 0 0;">
                from same infrastructure
              </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">🤖 AI Functions</p>', unsafe_allow_html=True)

        ai_waste = [
            ("Flow Detection", "Interprets real-time data from ultrasonic calculators to identify recoverable energy instantaneously."),
            ("Energy Conversion", "Determines when to divert electricity to resistive heaters and ORC units based on live grid conditions."),
            ("Leak Management", "Activates the null line automatically upon detection of voltage leakage anywhere in the network."),
            ("System Safety", "Monitors second and third lines; shuts them down immediately if abnormal conditions are detected."),
            ("Energy Optimisation", "Integrates with geothermal and waterfall outputs to balance supply, storage, and demand across the entire grid."),
            ("Predictive Maintenance", "Anticipates failures, schedules repairs, and ensures continuous operation with minimal downtime."),
        ]

        for title, desc in ai_waste:
            st.markdown(f'<div class="ib" style="margin-bottom:8px;"><strong style="color:#22c55e;">{title}:</strong> {desc}</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background:rgba(46,204,133,.07);border:1px solid rgba(46,204,133,.2);
                    border-radius:10px;padding:14px 18px;margin-top:16px;">
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.6);font-size:.82em;margin:0;line-height:1.7;">
            <strong style="color:#2ecc85;">Real-world impact:</strong> A 4 MW combined system recovers an additional 
            0.3–0.5 MW from waste heat. Over a 30-year operational lifetime that represents hundreds of thousands 
            of MWh of clean electricity produced at zero additional infrastructure cost — free electricity from 
            what the system was already throwing away.
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── DAYLIGHT MIRRORING ────────────────────────────────────────────────────
    with sys_tab4:
        st.markdown("""
        <div style="background:rgba(234,179,8,.07);border:1px solid rgba(234,179,8,.25);
                    border-radius:14px;padding:20px 24px;margin-bottom:20px;">
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                    color:#eab308;font-size:1.05em;margin:0 0 8px;">Core Concept</p>
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.7);
                    font-size:.88em;line-height:1.7;margin:0;">
            Polygonal building architecture combined with blur mirrors and AI-controlled shutters 
            redirects natural sunlight deep into interior spaces, eliminating the need for electrical 
            lighting during daytime hours entirely. The building shape acts as a natural light amplifier — 
            each angled surface bounces sunlight further inward, reaching corners that rectangular 
            buildings leave in shadow. Blur mirrors are used instead of conventional mirrors because 
            they diffuse light, preventing glare that could distract or harm occupants.
          </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">🏗️ System Components</p>', unsafe_allow_html=True)
            components_list = [
                ("Blur Mirrors & Polygonal Design", "Mirrors installed along polygonal walls and ceilings. AI calculates optimal reflection paths continuously. Polygonal facets enable multi-directional light reflection reaching even hidden corners."),
                ("AI-Controlled Shutters", "Multi-speed mechanical, liquid crystal, and micro-louver layers modulate sunlight entry in real time. AI ensures smooth openings and ultra-fast closings, adapting to sun position and cloud cover."),
                ("Light Sensors", "Monitor illuminance at multiple interior points and feed data to AI for dynamic mirror and shutter adjustment, ensuring uniform brightness throughout the building."),
                ("Weather Sensors", "Measure sunlight intensity, cloud cover, and temperature. AI predicts sunlight fluctuations and proactively adjusts the system before changes reach the interior."),
            ]
            for name, desc in components_list:
                st.markdown(f"""
                <div style="background:rgba(13,59,46,.3);border:1px solid rgba(234,179,8,.15);
                            border-radius:10px;padding:12px 14px;margin-bottom:8px;">
                  <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                            color:#eab308;font-size:.82em;margin:0 0 3px;">{name}</p>
                  <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.5);
                            font-size:.78em;margin:0;line-height:1.6;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">📦 Materials & Specifications</p>', unsafe_allow_html=True)

            mat_df = pd.DataFrame({
                "Component": ["Mirrors", "Shutters", "Sensor Casings", "AI Control Unit"],
                "Material / Specification": [
                    "Blur-coated glass or polymer",
                    "Mechanical louvers, LC layers, micro-louvers",
                    "Weatherproof polymer or stainless steel",
                    "Embedded processor or small computer",
                ],
            })
            st.dataframe(mat_df, use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">🌍 Impact Stats</p>', unsafe_allow_html=True)
            impacts = [
                ("15%", "of global electricity consumed by artificial lighting — eliminated during daylight hours"),
                ("40%+", "of electricity in tropical commercial buildings can be lighting — biggest single saving"),
                ("Healthier", "Natural light improves student performance, patient recovery, and worker productivity"),
                ("Zero cost", "Once installed, daylight mirroring produces its saving at no ongoing energy cost"),
                ("Replicable", "Works in homes, schools, clinics, factories, offices — the model scales everywhere"),
            ]
            for stat, desc in impacts:
                st.markdown(f"""
                <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:8px;">
                  <div style="background:rgba(234,179,8,.15);border:1px solid rgba(234,179,8,.3);
                              border-radius:7px;padding:4px 9px;white-space:nowrap;">
                    <span style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                                 color:#eab308;font-size:.82em;">{stat}</span>
                  </div>
                  <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.5);
                            font-size:.78em;margin:0;line-height:1.6;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.9em;margin-bottom:10px;">🤖 AI Functionality</p>', unsafe_allow_html=True)

        ai_day = [
            ("Optimal Reflection Paths", "Calculates best angles for polygonal mirrors to direct sunlight efficiently to every part of the interior."),
            ("Real-Time Shutter Control", "Maintains consistent indoor brightness by opening and closing shutters dynamically as sun position and cloud cover change."),
            ("Seasonal & Geographic Adjustment", "Accounts for seasonal changes in sun angle and building orientation to maintain performance year-round."),
            ("Emergency & Manual Override", "Fully automated but allows human intervention at any time if needed."),
            ("Energy Optimisation", "Minimises electricity usage while maximising natural light capture across the full building."),
        ]
        for title, desc in ai_day:
            st.markdown(f'<div class="ib" style="margin-bottom:8px;"><strong style="color:#eab308;">{title}:</strong> {desc}</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background:rgba(46,204,133,.07);border:1px solid rgba(46,204,133,.2);
                    border-radius:10px;padding:14px 18px;margin-top:16px;">
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.6);font-size:.82em;margin:0;line-height:1.7;">
            <strong style="color:#2ecc85;">The key insight:</strong> It is always cheaper and more efficient 
            to not use energy than to generate it. A community that reduces building energy demand by 20% 
            through daylight mirroring effectively gets 20% more capacity from its generation infrastructure 
            at no additional cost — the same plant now serves more households.
          </p>
        </div>
        """, unsafe_allow_html=True)

    # ── INTEGRATED CENTER ─────────────────────────────────────────────────────
    with sys_tab5:
        st.markdown("""
        <div style="background:rgba(46,204,133,.07);border:1px solid rgba(46,204,133,.25);
                    border-radius:14px;padding:20px 24px;margin-bottom:20px;">
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                    color:#2ecc85;font-size:1.05em;margin:0 0 8px;">The Integrated Vision</p>
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.7);
                    font-size:.88em;line-height:1.7;margin:0;">
            The Renewable Energy Generation Center brings all four technologies together into a single 
            AI-managed ecosystem. Each system feeds into the others — geothermal provides the baseload, 
            waterfall handles seasonal peaks, waste recovery captures what both systems lose, and daylight 
            mirroring reduces what the community needs in the first place. The result is a self-optimising 
            energy loop that maximises output while minimising waste.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.95em;margin-bottom:14px;">🏭 Center Sections</p>', unsafe_allow_html=True)

        sections = [
            ("#f97316", "1", "Geothermal Energy Section", "Harvests heat from deep underground reservoirs and converts it to electricity using the dual-loop system. AI monitors temperature, pressure, and turbine performance in real time, adjusting fluid flow to maintain peak output continuously."),
            ("#22c55e", "2", "Wasted Electricity Recovery Section", "Captures energy that would otherwise be lost in electrical grids, converting it to heat and subsequently to electricity via ORC. AI actively monitors energy flow, predicts leaks, and dynamically adjusts recovery operations across the entire distribution network."),
            ("#3b82f6", "3", "Mountain-Attached Waterfall Turbine Section", "Converts the kinetic energy of waterfalls into electricity without obstructing natural water flow. Adjustable AI-managed turbines and real-time control ensure maximum efficiency and safety under all seasonal and weather conditions."),
            ("#eab308", "4", "Nationwide Distribution Hub", "All electricity generated from the three primary sections is collected and stored here. This section is intelligently linked to the wasted electricity recovery system, enabling the capture and reuse of any losses during distribution — creating a self-optimising, highly efficient energy loop."),
        ]

        for colour, num, title, desc in sections:
            st.markdown(f"""
            <div style="display:flex;gap:16px;align-items:flex-start;
                        background:rgba(13,59,46,.25);border:1px solid {colour}33;
                        border-left:3px solid {colour};
                        border-radius:0 14px 14px 0;padding:16px 20px;margin-bottom:12px;">
              <div style="background:{colour};color:#061a11;width:32px;height:32px;min-width:32px;
                          border-radius:50%;display:flex;align-items:center;justify-content:center;
                          font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:.9em;">
                {num}
              </div>
              <div>
                <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                          color:#f0ede8;font-size:.9em;margin:0 0 5px;">{title}</p>
                <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.5);
                          font-size:.8em;margin:0;line-height:1.6;">{desc}</p>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.95em;margin-bottom:14px;">☀️ Smart Daylight-Mirroring in the Center</p>', unsafe_allow_html=True)

        st.markdown("""
        <div class="ib">
          The center itself adopts the Smart Daylight-Mirroring Polygonal Building design — 
          demonstrating the technology in the very facility that generates the electricity. 
          Polygonal walls and ceilings reflect sunlight deep into interior spaces. Blur mirrors 
          diffuse light and prevent glare. AI-controlled shutters and sensors continuously adjust 
          mirror angles and sunlight entry. This makes the center a <strong style="color:#2ecc85;">
          living model</strong> for how factories, homes, and offices can implement smart daylighting — 
          proving the concept works at scale before it reaches the community.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f0ede8;font-size:.95em;margin-bottom:14px;">✅ Efficiency Summary</p>', unsafe_allow_html=True)

        efficiency_points = [
            ("Full resource utilisation", "Geothermal heat, waterfall kinetic energy, sunlight, and recovered waste are all fully captured"),
            ("AI-driven optimisation", "Human monitoring combined with AI automation means almost no energy is wasted at any stage"),
            ("Predictive maintenance", "Reduces downtime across all four systems, keeping the entire center continuously operational"),
            ("Demand reduction", "Smart building design ensures energy savings at every stage, stretching generation capacity further"),
            ("Self-optimising loop", "All systems feed into each other — waste from one becomes input for another"),
        ]

        for title, desc in efficiency_points:
            st.markdown(f"""
            <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:8px;">
              <span style="color:#2ecc85;font-size:1em;margin-top:1px;">✓</span>
              <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.6);font-size:.83em;margin:0;line-height:1.6;">
                <strong style="color:#f0ede8;">{title}:</strong> {desc}
              </p>
            </div>
            """, unsafe_allow_html=True)

    # ── SDG ALIGNMENT ─────────────────────────────────────────────────────────
    with sys_tab6:
        st.markdown("""
        <div style="background:rgba(46,204,133,.07);border:1px solid rgba(46,204,133,.25);
                    border-radius:14px;padding:20px 24px;margin-bottom:24px;">
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                    color:#2ecc85;font-size:1.05em;margin:0 0 8px;">SDG Alignment Overview</p>
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.7);
                    font-size:.88em;line-height:1.7;margin:0;">
            The EcoGrid system is designed not only for technological efficiency but to directly advance 
            global sustainability objectives. Each of the four technologies contributes to multiple UN 
            Sustainable Development Goals, creating a holistic model of sustainable innovation that 
            addresses energy, climate, health, education, and economic development simultaneously.
          </p>
        </div>
        """, unsafe_allow_html=True)

        sdgs = [
            ("#f59e0b", "SDG 7", "Affordable and Clean Energy",
             "Produces clean, renewable electricity from geothermal heat, waterfalls, and recovered wasted energy. AI ensures maximum efficiency by balancing production with demand and minimising losses.",
             ["Consistent low-carbon energy for households and industries", "A 50m waterfall turbine section alone can power over 5,370 families annually", "Smart daylighting reduces reliance on electrical lighting entirely"]),

            ("#6366f1", "SDG 9", "Industry, Innovation and Infrastructure",
             "Represents a cutting-edge infrastructure model integrating AI, smart energy recovery, and adaptive building design.",
             ["AI-driven optimisation, predictive maintenance, and smart lighting", "Serves as a living lab for clean energy technologies and sustainable urban planning", "Scalable renewable solutions for national grids without disrupting ecosystems"]),

            ("#10b981", "SDG 11", "Sustainable Cities and Communities",
             "Smart daylight-mirroring polygonal buildings reduce energy consumption while improving indoor environmental quality.",
             ["Replicable in homes, factories, and offices", "Creates safe, energy-efficient community spaces", "Reduces urban energy costs, promoting livable future-ready cities"]),

            ("#ef4444", "SDG 13", "Climate Action",
             "Replaces fossil-fuel electricity with geothermal and hydro-kinetic power, recovering wasted energy to reduce greenhouse gas emissions.",
             ["Mitigates climate change by cutting CO₂ from conventional generation", "AI ensures optimal operation, avoiding energy waste", "Quantified carbon savings unlock international climate finance"]),

            ("#8b5cf6", "SDG 12", "Responsible Consumption and Production",
             "The wasted electricity recovery system ensures that energy is used responsibly, recycling losses that conventional systems discard.",
             ["Recycles energy lost in industrial systems via ORC technology", "Promotes efficient materials use with long-life alloys and modular components", "Closed-loop design means nothing is wasted"]),

            ("#22c55e", "SDG 15", "Life on Land",
             "Mountain-attached waterfall turbines generate power without blocking water flows or harming ecosystems.",
             ["Maintains river and mountain ecosystems while harnessing kinetic energy", "Supports biodiversity by minimising environmental disruption", "No land flooding, no permanent alteration of natural waterways"]),

            ("#0ea5e9", "SDG 17", "Partnerships for the Goals",
             "Demonstrates interdisciplinary and international collaboration through AI, engineering, and sustainable architecture integration.",
             ["Model for governments, universities, and industries to collaborate", "Encourages knowledge-sharing and technology transfer globally", "Open toolkit approach enables replication across regions"]),
        ]

        for colour, code, name, contribution, impacts in sdgs:
            impacts_html = "".join([
                f'<p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.5);font-size:.78em;margin:3px 0;line-height:1.5;">• {i}</p>'
                for i in impacts
            ])
            st.markdown(f"""
            <div style="background:rgba(13,59,46,.25);border:1px solid {colour}33;
                        border-left:3px solid {colour};border-radius:0 14px 14px 0;
                        padding:16px 20px;margin-bottom:12px;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;flex-wrap:wrap;">
                <span style="background:{colour}22;border:1px solid {colour}55;color:{colour};
                             border-radius:7px;padding:4px 12px;font-family:'Plus Jakarta Sans',sans-serif;
                             font-weight:700;font-size:.82em;">{code}</span>
                <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                          color:#f0ede8;font-size:.9em;margin:0;">{name}</p>
              </div>
              <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.6);
                        font-size:.82em;margin:0 0 8px;line-height:1.6;">{contribution}</p>
              {impacts_html}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:
        rgba(46,204,133,.08);border:1px solid rgba(46,204,133,.25);
                    border-radius:14px;padding:20px 24px;margin-top:8px;text-align:center;">
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                    color:#2ecc85;font-size:1em;margin:0 0 8px;">The Bottom Line</p>
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.6);
                    font-size:.85em;line-height:1.7;margin:0;">
            This integrated system does more than generate electricity — it models a sustainable, 
            AI-optimised ecosystem that ensures clean energy access, reduces carbon footprint, 
            preserves natural ecosystems, and demonstrates how technology and AI can align with 
            global sustainability goals. The EcoGrid Renewable Energy Center is the SDGs in action.
          </p>
        </div>
        """, unsafe_allow_html=True)
        # ── PDF DOWNLOAD ──────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(13,59,46,.4);border:1px solid rgba(46,204,133,.25);
                    border-radius:14px;padding:24px;text-align:center;">
          <p style="font-size:1.8em;margin-bottom:8px;">📄</p>
          <p style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:700;
                    color:#f0ede8;font-size:1em;margin:0 0 6px;">Want to go deeper?</p>
          <p style="font-family:Inter,sans-serif;color:rgba(240,237,232,.45);
                    font-size:.82em;margin:0 0 16px;">
            Download the full 32-page technical design document covering every system in detail.
          </p>
        </div>
        """, unsafe_allow_html=True)

        design_pdf_b64 = load_file_b64("EcoGrid_Science_and_Systems.pdf")
        if design_pdf_b64:
            pdf_bytes = base64.b64decode(design_pdf_b64)
            st.download_button(
                label="⬇️  Download Full System Design PDF",
                data=pdf_bytes,
                file_name="EcoGrid_Green_Energy_Systems_Design.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.warning("Place EcoGrid_Science_and_Systems.pdf in the same folder as app.py to enable download.")

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="footer"><strong style="color:#2ecc85;">EcoGrid Toolkit</strong><br>Empowering communities with clean energy solutions · © 2024 EcoGrid Toolkit · Built with Streamlit</div>', unsafe_allow_html=True)
