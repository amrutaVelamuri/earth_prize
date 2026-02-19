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
    padding: 44px 52px; margin-bottom: 36px;
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
    font-family: var(--font-head); font-size: 3.6em; font-weight: 800;
    color: var(--gb); letter-spacing: -2.5px; line-height: 1; margin: 0;
}
.hero-logo span { color: var(--ea); }
.hero-tag {
    font-family: var(--font-body); font-size: 1em; font-weight: 400;
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
    """Run a page file in-place. Fully isolated so failures never blank out later tabs."""
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
# SESSION STATE — initialise ALL keys up front
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
# LOGO — load and base64-encode once
# ============================================================================
def load_file_b64(path):
    abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    if os.path.exists(abs_path):
        with open(abs_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64    = load_file_b64("logo.png")
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

    for col, (n, l) in zip(st.columns(4), [("5","Modules"), ("3","Energy Sources"), ("122yrs","Training Data"), ("CO₂","Tracked")]):
        col.markdown(f'<div class="stat-card"><div class="sn">{n}</div><div class="sl">{l}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Meet the Team</p><div class="al"></div><p class="ss">Five co-founders united by a mission to make clean energy accessible to every community.</p>', unsafe_allow_html=True)

    TEAM = [
        {"i":"01","g":"linear-gradient(135deg,rgba(46,204,133,.2),rgba(8,20,14,.8))","n":"Retina","r":"Co-Founder","b":"Add a short bio here."},
        {"i":"02","g":"linear-gradient(135deg,rgba(46,204,133,.2),rgba(8,20,14,.8))","n":"Siyeong","r":"Co-Founder","b":"Add a short bio here."},
        {"i":"03","g":"linear-gradient(135deg,rgba(200,169,110,.2),rgba(8,20,14,.8))","n":"Amruta","r":"Co-Founder","b":"Add a short bio here."},
        {"i":"04","g":"linear-gradient(135deg,rgba(46,204,133,.2),rgba(8,20,14,.8))","n":"Shyam","r":"Co-Founder","b":"Add a short bio here."},
        {"i":"05","g":"linear-gradient(135deg,rgba(133,196,255,.2),rgba(8,20,14,.8))","n":"Advika","r":"Co-Founder","b":"Add a short bio here."},
    ]
    row1 = st.columns(3)
    row2_spacer1, row2_a, row2_b, row2_spacer2 = st.columns([0.5, 1, 1, 0.5])
    cols = list(row1) + [row2_a, row2_b]
    for col, m in zip(cols, TEAM):
        with col:
            st.markdown(f"""<div class="team-card">
              <div class="tav" style="background:{m['g']};">
                <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:.85em;font-weight:700;color:#2ecc85;">{m['i']}</span>
              </div>
              <div class="tn">{m['n']}</div>
              <div class="tr">{m['r']}</div>
              <div class="tb">{m['b']}</div>
            </div>""", unsafe_allow_html=True)

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
    st.markdown('<p class="sh">About & Education</p><div class="al"></div><p class="ss">Learn how to get the most out of EcoGrid</p>', unsafe_allow_html=True)

    for i, (title, desc) in enumerate([
        ("PDF Analyzer", "Upload a technical document. Auto-extracts coordinates, waterfall specs, geothermal temperatures and drilling depths."),
        ("Geographic Calculator", "Enter or import location data. Adjust sliders and hit Calculate for power, energy and carbon figures."),
        ("Time-Series Predictor", "With calculator data loaded, run the LSTM predictor trained on 122 years of Bangladesh weather data."),
        ("Household Energy Status", "Enter real-time kWh readings for any sector. The AI engine flags anomalies and recommends actions."),
        ("Export & AI Reports", "Download CSV / JSON or generate a full written report tailored to your audience."),
    ], 1):
        st.markdown(f'<div class="sr"><div class="snum">{i}</div><div class="sbody"><h4>{title}</h4><p>{desc}</p></div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── EcoGrid Textbook PDF Embed ────────────────────────────────────────────
    st.markdown('<p class="sh">EcoGrid Textbook</p><div class="al"></div><p class="ss">Our full educational reference — read it right here or download below</p>', unsafe_allow_html=True)

    if textbook_b64:
        import streamlit.components.v1 as components

        # Header card (pure markdown — no base64 in here)
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

        # Render PDF using PDF.js via CDN — works in all browsers on Streamlit Cloud
        # PDF.js fetches the file from a blob URL we build in JS, bypassing browser base64 blocks
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

            // Decode base64 → Uint8Array (avoids browser blob URL restrictions)
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

        # Download button — always available
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
    st.markdown('<p class="sh">Verification Unit</p><div class="al"></div><p class="ss">Hardware integration · Sensors · Physical verification</p>', unsafe_allow_html=True)

    for col, (icon, lbl, status, cls) in zip(st.columns(4), [
        ("⚡", "Sensor Array",  "Online",    "hon"),
        ("📡", "Data Link",     "Connected", "hon"),
        ("🔋", "Power Supply",  "Normal",    "hwn"),
        ("🛡️", "Verification",  "Active",    "hon"),
    ]):
        col.markdown(f'<div class="hw-card"><div class="hi">{icon}</div><div class="hl">{lbl}</div><div class="{cls}">{status}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    hh1, hh2 = st.columns(2)
    with hh1:
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f5f0e8;margin-bottom:11px;">🔧 Physical Equipment</p>', unsafe_allow_html=True)
        for n, d in [
            ("Energy meters & CTs",    "Real-time kWh per phase"),
            ("DAQ modules",            "Digitise analogue signals at 1 kHz"),
            ("IoT gateway / ESP32",    "Edge processing & MQTT"),
            ("Environmental sensors",  "Temp, humidity, irradiance"),
        ]:
            st.markdown(f'<div style="background:rgba(13,59,46,.28);border:1px solid rgba(46,204,133,.14);border-radius:10px;padding:11px 15px;margin-bottom:8px;"><p style="color:#f5f0e8;font-weight:600;margin:0 0 2px;font-size:.88em;">{n}</p><p style="color:rgba(245,240,232,.42);margin:0;font-size:.78em;">{d}</p></div>', unsafe_allow_html=True)
    with hh2:
        st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:700;color:#f5f0e8;margin-bottom:11px;">📡 Data & Verification</p>', unsafe_allow_html=True)
        for n, d in [
            ("Calibration",   "Monthly zero-point & span vs. reference"),
            ("Protocol",      "MQTT over TLS every 5 s"),
            ("Quality control","3σ rejection + CRC checks"),
            ("Certification", "IEC 62052 / ANSI C12.20"),
        ]:
            st.markdown(f'<div style="background:rgba(13,59,46,.28);border:1px solid rgba(46,204,133,.14);border-radius:10px;padding:11px 15px;margin-bottom:8px;"><p style="color:#f5f0e8;font-weight:600;margin:0 0 2px;font-size:.88em;">{n}</p><p style="color:rgba(245,240,232,.42);margin:0;font-size:.78em;">{d}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sh">Setup Guide</p><div class="al"></div>', unsafe_allow_html=True)
    for i, (title, d) in enumerate([
        ("Wire sensors",         "Connect CTs around each phase conductor. Use shielded cable for runs > 1 m."),
        ("Flash firmware",       "Upload Arduino/ESP32 sketch. Set Wi-Fi SSID & MQTT broker in config.h."),
        ("Calibrate",            "Apply 1 kW reference load; adjust CT_RATIO until reading matches."),
        ("Verify transmission",  "Check MQTT dashboard — payloads every 5 s, CRC pass > 99.9%."),
        ("Connect to EcoGrid",   "Enter broker URL in Household Energy Status tab. Data flows automatically."),
    ], 1):
        st.markdown(f'<div class="sr"><div class="snum">{i}</div><div class="sbody"><h4>{title}</h4><p>{d}</p></div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    hw1, hw2 = st.columns(2)
    for col, lbl in zip([hw1, hw2], ["Wiring Diagram", "Installed Unit Photo"]):
        col.markdown(f'<div style="border:2px dashed rgba(46,204,133,.25);border-radius:12px;padding:50px 14px;text-align:center;background:rgba(13,59,46,.16);"><p style="color:rgba(245,240,232,.35);font-size:.93em;margin:0;">📷 {lbl}</p></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — HOUSEHOLD ENERGY STATUS
# ══════════════════════════════════════════════════════════════════════════════
with t5:
    st.markdown('<p class="sh">Household Energy Status</p><div class="al"></div><p class="ss">EnergyGuard AI · Keen Edition V4 · Real-time monitoring & optimisation</p>', unsafe_allow_html=True)

    # ── Helper classes & functions ────────────────────────────────────────────

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

    # ── Form ─────────────────────────────────────────────────────────────────
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

    # ── Results ───────────────────────────────────────────────────────────────
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
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="footer"><strong style="color:#2ecc85;">EcoGrid Toolkit</strong><br>Empowering communities with clean energy solutions · © 2024 EcoGrid Toolkit · Built with Streamlit</div>', unsafe_allow_html=True)
