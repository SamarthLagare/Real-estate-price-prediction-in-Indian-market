import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium

# --- 1. LATEST MINIMALIST CONFIG ---
# Using initial_sidebar_state="collapsed" can sometimes prevent the "snap" 
# but "expanded" is better for a professional terminal look.
st.set_page_config(page_title="AURUM", layout="wide", initial_sidebar_state="expanded")

# --- 2. THE PREMIUM "BLACK & GOLD" CSS ---
st.markdown("""
    <style>
    /* NATIVE OVERRIDES */
    header, footer { visibility: hidden; }
    .stApp { background-color: #000000; color: #D4AF37; }
    
    /* SIDEBAR: Simple & Deep Black */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    /* MINIMALIST TEXT */
    h1, h2, h3 { font-family: 'serif'; font-weight: 200; letter-spacing: 2px; }
    .stMetricValue { color: #D4AF37 !important; font-weight: 300 !important; }
    
    /* CLEAN BUTTONS */
    .stButton > button {
        border: 1px solid #D4AF37 !important;
        background: transparent !important;
        color: #D4AF37 !important;
        border-radius: 2px;
        transition: 0.3s;
    }
    .stButton > button:hover { background: #D4AF37 !important; color: #000 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE REFINED DATASET (15 PRIME NODES) ---
mumbai_intel = {
    "Malabar Hill": {"base": 118000, "growth": 1.05, "coords": [18.9548, 72.7985]},
    "Pali Hill, Bandra": {"base": 98000, "growth": 1.08, "coords": [19.0655, 72.8252]},
    "Worli Sea Face": {"base": 85000, "growth": 1.07, "coords": [19.0176, 72.8172]},
    "Juhu Beach": {"base": 75000, "growth": 1.06, "coords": [19.1075, 72.8263]},
    "Hiranandani, Powai": {"base": 36000, "growth": 1.12, "coords": [19.1176, 72.9060]},
    "Palm Beach, Navi Mumbai": {"base": 24000, "growth": 1.25, "coords": [19.0330, 73.0297]}
}

# --- 4. THE CLEAN SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>AURUM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#555; font-size:10px;'>ESTATE QUANTUM</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Simple Navigation
    loc = st.selectbox("LOCATION NODE", list(mumbai_intel.keys()))
    
    st.markdown("---")
    area = st.number_input("AREA (SQFT)", 500, 20000, 1500)
    floor = st.slider("FLOOR", 0, 100, 25)
    
    with st.expander("REFINED SPECS"):
        ceiling = st.slider("CEILING (FT)", 9.0, 15.0, 11.0)
        vastu = st.toggle("VASTU", value=True)
        smart = st.toggle("AI-SMART", value=True)

    execute = st.button("RUN VALUATION")

# --- 5. THE TERMINAL INTERFACE ---
if not execute:
    st.markdown("<div style='height:30vh'></div><h1 style='text-align:center; font-size:80px; letter-spacing:20px;'>AURUM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#D4AF37; font-size:12px; letter-spacing:5px;'>MUMBAI 2026 FORECASTER</p>", unsafe_allow_html=True)
else:
    # Logic
    data = mumbai_intel[loc]
    price_2025 = (data['base'] * area * (1 + floor*0.005)) / 10000000
    price_2026 = price_2025 * data['growth']

    # Satellite Map
    m = folium.Map(location=data['coords'], zoom_start=18, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google')
    folium.CircleMarker(data['coords'], radius=25, color='#D4AF37', fill=True).add_to(m)
    st_folium(m, width=1500, height=400)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Elegant Metric Grid
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("2026 FORECAST", f"₹ {price_2026:.2f} Cr")
    with c2: st.metric("YOY ALPHA", f"+{round((data['growth']-1)*100, 1)}%")
    with c3:
        # Mini Radar Graph
        fig = go.Figure(data=go.Scatterpolar(
            r=[80, 90, 70, 85, 90],
            theta=['ROI', 'Scarcity', 'Legal', 'Infra', 'Luxury'],
            fill='toself', line_color='#D4AF37'
        ))
        fig.update_layout(polar=dict(bgcolor="black", radialaxis=dict(visible=False)), paper_bgcolor="black", showlegend=False, height=200, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
