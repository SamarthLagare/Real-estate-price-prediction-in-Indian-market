import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium

# --- 1. IMMUTABLE CONFIG & CSS INJECTION ---
# Setting layout to 'wide' here is the first step to prevent snapping
st.set_page_config(page_title="AURUM | Obsidian Terminal", layout="wide", initial_sidebar_state="expanded")

# Injecting CSS at the very top to lock styles before rendering components
st.markdown("""
    <style>
    /* REMOVE PADDING & HEADERS TO PREVENT SHIFT */
    .block-container { padding-top: 0rem; padding-bottom: 0rem; }
    header, footer, .stDeployButton { visibility: hidden; }
    
    /* THE OBSIDIAN THEME */
    .stApp { background-color: #000000; color: #D4AF37; font-family: 'Inter', sans-serif; }
    
    /* SIDEBAR LOCK: Matches background to prevent "Gray Snap" */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #D4AF37;
        box-shadow: 10px 0px 30px rgba(212, 175, 55, 0.05);
    }
    
    /* REMOVE SIDEBAR TOP MARGIN */
    [data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }
    
    /* GOLD ACCENTS & INPUTS */
    .stMetricValue { color: #D4AF37 !important; font-family: 'Playfair Display', serif; text-shadow: 0 0 10px rgba(212, 175, 55, 0.3); }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #0a0a0a !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        color: #fff !important;
    }
    
    /* PREVENT BUTTON SNAP */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #111 0%, #000 100%);
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
        transition: all 0.4s ease;
    }
    .stButton > button:hover {
        background: #D4AF37 !important;
        color: #000 !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LUXURY DATA NODES (MUMBAI 2026) ---
mumbai_intel = {
    "Malabar Hill (The Ridge)": {"base": 118000, "growth": 1.05, "coords": [18.9548, 72.7985]},
    "Bandra West (Pali Hill)": {"base": 98000, "growth": 1.08, "coords": [19.0655, 72.8252]},
    "Worli (Sea Face)": {"base": 85000, "growth": 1.07, "coords": [19.0176, 72.8172]},
    "Powai (Lake Enclave)": {"base": 36000, "growth": 1.12, "coords": [19.1176, 72.9060]},
    "Navi Mumbai (Capital Node)": {"base": 24000, "growth": 1.25, "coords": [19.0330, 73.0297]}
}

# --- 3. THE CONTROL VAULT (POLISHED SIDEBAR) ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center; font-size:36px; letter-spacing:10px; color:#D4AF37;'>AURUM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#666; font-size:10px; margin-top:-15px;'>MUMBAI QUANTUM TERMINAL v3.5</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    loc = st.selectbox("MICRO-MARKET NODE", list(mumbai_intel.keys()))
    
    st.markdown("---")
    # Using columns for minute parameters to save space and look "Technical"
    col_a, col_b = st.columns(2)
    area = col_a.number_input("CARPET (SQFT)", 500, 25000, 2000)
    ceiling = col_b.number_input("CEILING (FT)", 9.0, 20.0, 12.0)
    
    floor = st.slider("ELEVATION (FLOOR)", 0, 120, 40)
    
    with st.expander("🛡️ LEGAL & INFRASTRUCTURE", expanded=False):
        status = st.selectbox("LEGAL GRADE", ["RERA Registered", "OC Received", "A-Khata Clear"])
        security = st.select_slider("SECURITY TIER", ["Standard", "Elite-24", "NSG Command"])
        ev_bays = st.number_input("EV BAYS", 0, 10, 2)

    with st.expander("✨ LIFESTYLE ASSETS", expanded=False):
        vastu = st.toggle("VASTU COMPLIANT", value=True)
        automation = st.toggle("AI-SMART INTEGRATION", value=True)
        terrace = st.toggle("PRIVATE SKY TERRACE")
    
    st.markdown("<br>", unsafe_allow_html=True)
    execute = st.button("RUN QUANTUM VALUATION")

# --- 4. THE TERMINAL INTERFACE ---
if not execute:
    # Centered Minimalist Welcome to hide components before run
    st.markdown("<div style='height: 35vh;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; font-size:100px; letter-spacing:20px; margin:0;'>AURUM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:14px; color:#D4AF37; letter-spacing:5px;'>INITIALIZING QUANTUM FORECASTS... SELECT NODE IN VAULT</p>", unsafe_allow_html=True)
else:
    # --- LOGIC ENGINE ---
    data = mumbai_intel[loc]
    # Detailed parameter impacts
    f_premium = 1 + (floor * 0.006) # Floor rise
    c_premium = 1 + ((ceiling - 9) * 0.03) # Ceiling premium
    asset_premium = (1.15 if terrace else 1.0) * (1.1 if automation else 1.0)
    
    price_2025 = (data['base'] * area * f_premium * c_premium * asset_premium) / 10000000
    price_2026 = price_2025 * data['growth']

    # --- TOP SATELLITE RECON ---
    m = folium.Map(location=data['coords'], zoom_start=18, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google')
    folium.CircleMarker(data['coords'], radius=40, color='#D4AF37', fill=True, weight=2).add_to(m)
    st_folium(m, width=1600, height=450, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- DATA DRAWER ---
    c1, c2, c3 = st.columns([1.5, 1, 1])
    
    with c1:
        st.markdown("### 🧬 INVESTMENT DNA")
        # Unique Radar Graph for Minute Parameters
        categories = ['ROI Alpha', 'Legal Safety', 'Luxury Tier', 'Infra Score', 'Vastu Score']
        vals = [(data['growth']-1)*500, 100 if "OC" in status else 70, (floor/1.2), 90, 95 if vastu else 10]
        fig = go.Figure(data=go.Scatterpolar(r=vals, theta=categories, fill='toself', line_color='#D4AF37'))
        fig.update_layout(polar=dict(bgcolor="black", radialaxis=dict(visible=False)), paper_bgcolor="black", showlegend=False, margin=dict(l=0,r=0,t=20,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### 💎 FORECAST")
        st.metric("2026 VALUATION", f"₹ {price_2026:.2f} Cr")
        st.metric("YOY ALPHA", f"+{round((data['growth']-1)*100, 1)}%")
        st.markdown("---")
        st.write(f"**Base 2025:** ₹ {price_2025:.2f} Cr")
        st.write(f"**Stamp Duty (6%):** ₹ {price_2026*0.06:.2f} Cr")

    with c3:
        st.markdown("### ⚙️ SPECIFICATIONS")
        st.write(f"**Legal:** {status}")
        st.write(f"**Security:** {security}")
        st.write(f"**Ceiling:** {ceiling} Ft")
        st.write(f"**EV Hub:** {ev_bays} Bays")
        st.write(f"**Automation:** {'Active' if automation else 'None'}")
