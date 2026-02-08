import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium

# --- 1. CONFIG & SEAMLESS LUXURY STYLING ---
st.set_page_config(page_title="AURUM | Obsidian Terminal", layout="wide")

# Polished Sidebar & Global Theme
st.markdown("""
    <style>
    /* Global Reset */
    header, footer, .stDeployButton { visibility: hidden; }
    .stApp { background-color: #000000; color: #D4AF37; font-family: 'Inter', sans-serif; }
    
    /* Polished Sidebar Override */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #D4AF37;
        min-width: 350px !important;
    }
    [data-testid="stSidebarNav"] { background-image: none; }
    
    /* Elegant Navigation Buttons */
    .nav-btn {
        padding: 15px;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        color: #D4AF37;
        cursor: pointer;
    }
    
    /* Custom Slider & Input Glow */
    .stSlider [data-baseweb="slider"] { color: #D4AF37 !important; }
    div[data-baseweb="input"] { background-color: #111 !important; border: 1px solid #D4AF37 !important; color: white !important; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Playfair Display', serif; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE MARKET DATA (2025-2026 INTELLIGENCE) ---
mumbai_intel = {
    "Malabar Hill (The Ridge)": {"base": 115000, "growth": 1.05, "coords": [18.9548, 72.7985]},
    "Bandra West (Pali Hill)": {"base": 95000, "growth": 1.08, "coords": [19.0655, 72.8252]},
    "Worli (Coastal Node)": {"base": 82000, "growth": 1.07, "coords": [19.0176, 72.8172]},
    "Juhu (The Shore)": {"base": 75000, "growth": 1.06, "coords": [19.1075, 72.8263]},
    "Wadala (Smart City)": {"base": 32000, "growth": 1.16, "coords": [19.0215, 72.8541]},
    "Navi Mumbai (Airport Hub)": {"base": 21000, "growth": 1.22, "coords": [19.0330, 73.0297]}
}

# --- 3. POLISHED SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center; font-size:32px; letter-spacing:8px;'>AURUM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888; font-size:12px;'>QUANTUM TERMINAL v3.0</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation Tabs (Improved UI)
    nav = st.radio("WORKFLOW", ["Terminal", "Market Heatmap", "Portfolio Intelligence"], label_visibility="collapsed")
    
    st.markdown("<br>### 📍 MICRO-MARKET", unsafe_allow_html=True)
    loc = st.selectbox("Location Node", list(mumbai_intel.keys()), label_visibility="collapsed")
    
    with st.expander("🏗️ ARCHITECTURAL SPECS", expanded=True):
        area = st.number_input("Carpet Area (SqFt)", 500, 20000, 1500)
        ceiling = st.slider("Ceiling Height (Ft)", 9.0, 18.0, 11.0)
        floor = st.slider("Elevation (Floor)", 0, 120, 30)
        construction = st.select_slider("Build Quality", ["Grade B", "Grade A", "Ultra-Luxe"])

    with st.expander("💎 PREMIUM PARAMETERS"):
        khata = st.selectbox("Legal Status", ["A-Khata", "RERA Registered", "Occupancy Certificate (OC)"])
        ev_slots = st.number_input("EV Charging Bays", 0, 10, 2)
        vastu = st.toggle("Vastu Compliance", value=True)
        smart_home = st.toggle("AI-Integrated Automation", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    execute = st.button("RUN QUANTUM ANALYSIS", use_container_width=True)

# --- 4. TERMINAL INTERFACE ---
if not execute:
    # Centered Minimalist Welcome
    st.markdown("<div style='height: 25vh;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; font-size:72px; letter-spacing:15px;'>AURUM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px; color:rgba(212,175,55,0.6);'>MUMBAI REAL ESTATE QUANTUM FORECASTER 2026</p>", unsafe_allow_html=True)
else:
    # Logic Engine
    data = mumbai_intel[loc]
    build_mult = {"Grade B": 0.9, "Grade A": 1.0, "Ultra-Luxe": 1.3}[construction]
    floor_rise = 1 + (floor * 0.005)
    
    price_2025 = (data['base'] * area * build_mult * floor_rise * (1.1 if smart_home else 1.0)) / 10000000
    price_2026 = price_2025 * data['growth']

    # Satellite Map
    st.markdown("### 🛰️ SATELLITE NODE RECONNAISSANCE")
    m = folium.Map(location=data['coords'], zoom_start=18, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google')
    folium.CircleMarker(data['coords'], radius=30, color='#D4AF37', fill=True, weight=1).add_to(m)
    st_folium(m, width=1400, height=400)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🧬 INVESTMENT DNA")
        # Unique Radar/Spider Graph
        categories = ['ROI Alpha', 'Legal Tier', 'Luxury Index', 'Infra Score', 'Vastu Score']
        vals = [(data['growth']-1)*500, 95, (floor/1.2), 85, 95 if vastu else 10]
        
        fig = go.Figure(data=go.Scatterpolar(r=vals, theta=categories, fill='toself', line_color='#D4AF37'))
        fig.update_layout(polar=dict(bgcolor="black", radialaxis=dict(visible=False)), paper_bgcolor="black", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"### 💎 VALUATION")
        st.metric("2026 FORECAST", f"₹ {price_2026:.2f} Cr")
        st.metric("GROWTH YOY", f"{round((data['growth']-1)*100, 1)}%", "+ Alpha")
        st.markdown("---")
        st.write(f"**Elevation:** {floor}th Level")
        st.write(f"**Legal:** {khata}")
        st.write(f"**Automation:** {'Active' if smart_home else 'Inactive'}")
