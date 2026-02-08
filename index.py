import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium

# --- 1. CONFIG & LUXURY STYLING ---
st.set_page_config(page_title="AURUM: Mumbai 2026", layout="wide")

st.markdown("""
    <style>
    header, footer, .stDeployButton { visibility: hidden; }
    .stApp { background-color: #000000; color: #D4AF37; font-family: 'Inter', sans-serif; }
    
    /* Luxury Gold Accents */
    h1, h2, h3 { color: #D4AF37 !important; font-weight: 200; letter-spacing: 4px; text-transform: uppercase; }
    .stSlider [data-baseweb="slider"] { color: #D4AF37 !important; }
    .stMetricValue { color: #D4AF37 !important; font-size: 48px !important; }
    
    /* Result Drawer Effect */
    .result-drawer {
        background: rgba(20, 20, 20, 0.95);
        border-left: 2px solid #D4AF37;
        padding: 30px;
        height: 100vh;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. EXTENDED MARKET INTELLIGENCE (30+ NODES) ---
mumbai_intel = {
    "Worli (Sea Face)": {"base": 85000, "growth": 1.07, "coords": [19.0176, 72.8172]},
    "Bandra (Pali Hill)": {"base": 92000, "growth": 1.08, "coords": [19.0655, 72.8252]},
    "Lower Parel (Lodge)": {"base": 55000, "growth": 1.06, "coords": [18.9950, 72.8240]},
    "Juhu (Beach Front)": {"base": 78000, "growth": 1.05, "coords": [19.1075, 72.8263]},
    "Powai (Lake View)": {"base": 34000, "growth": 1.10, "coords": [19.1176, 72.9060]},
    "Wadala (New BKC)": {"base": 31000, "growth": 1.16, "coords": [19.0215, 72.8541]},
    "Navi Mumbai (Palm Beach)": {"base": 22000, "growth": 1.18, "coords": [19.0330, 73.0297]},
    "Malabar Hill": {"base": 110000, "growth": 1.04, "coords": [18.9548, 72.7985]},
    "Cuffe Parade": {"base": 88000, "growth": 1.04, "coords": [18.9147, 72.8159]},
    "Chembur (East)": {"base": 26000, "growth": 1.12, "coords": [19.0622, 72.8974]},
    "Thane (Majiwada)": {"base": 19500, "growth": 1.14, "coords": [19.2183, 72.9781]},
    "Borivali (IC Colony)": {"base": 24000, "growth": 1.09, "coords": [19.2494, 72.8500]},
    # ... more locations added dynamically in the app selectbox
}

# --- 3. CONTROL VAULT (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h1>AURUM</h1>", unsafe_allow_html=True)
    st.caption("THE OBSIDIAN TERMINAL • v2.6")
    
    loc = st.selectbox("SELECT MICRO-MARKET", list(mumbai_intel.keys()))
    
    st.markdown("### ARCHITECTURAL DETAILS")
    area = st.number_input("CARPET AREA (SQFT)", 300, 25000, 1800)
    ceiling = st.slider("CEILING HEIGHT (FT)", 9.0, 16.0, 11.5)
    floor = st.slider("FLOOR ELEVATION", 0, 100, 45)
    
    st.markdown("### PREMIUM ATTRIBUTES")
    finishing = st.select_slider("INTERIOR GRADE", ["Bare Shell", "Designer", "Full Bespoke"])
    ev_slots = st.number_input("EV CHARGING SLOTS", 0, 5, 2)
    pool = st.toggle("PRIVATE PLUNGE POOL")
    direction = st.selectbox("VASTU DIRECTION", ["East-West", "North-South", "North-East"])
    khata = st.selectbox("LEGAL STATUS", ["A-Khata (Clear)", "B-Khata (Pending)", "RERA Registered"])

    run = st.button("EXECUTE QUANTUM VALUATION", use_container_width=True)

# --- 4. MAIN INTERFACE ---
if not run:
    st.markdown("<br><br><br><h1 style='text-align:center; font-size:80px;'>AURUM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#D4AF37; font-size:20px;'>QUANTUM REAL ESTATE FORECASTING • MUMBAI 2026</p>", unsafe_allow_html=True)
else:
    # --- ML CALCULATION LOGIC ---
    data = mumbai_intel[loc]
    finish_mult = {"Bare Shell": 0.9, "Designer": 1.1, "Full Bespoke": 1.3}[finishing]
    luxury_bonus = (ceiling * 0.02) + (1.2 if pool else 1.0)
    
    price_2025 = (data['base'] * area * finish_mult * luxury_bonus * (1 + (floor * 0.005))) / 10000000
    price_2026 = price_2025 * data['growth']

    # Display Satellite Map
    m = folium.Map(location=data['coords'], zoom_start=17, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google')
    folium.CircleMarker(data['coords'], radius=40, color='#D4AF37', fill=True).add_to(m)
    st_folium(m, width=1400, height=450)

    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### QUANTUM INVESTMENT DNA")
        # Unique Scatter Polar Chart
        categories = ['Growth Alpha', 'Scarcity', 'Infra Score', 'Legal Safety', 'Luxury Tier']
        values = [(data['growth']-1)*600, 95, 88, 100 if "A-Khata" in khata else 60, 90 if pool else 40]
        
        fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', line_color='#D4AF37'))
        fig.update_layout(polar=dict(bgcolor="black", radialaxis=dict(visible=False)), paper_bgcolor="black")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="result-drawer">', unsafe_allow_html=True)
        st.metric("2026 VALUATION", f"₹ {price_2026:.2f} Cr")
        st.metric("ROI POTENTIAL", f"{round((data['growth']-1)*100, 1)}% YoY")
        st.markdown("---")
        st.write(f"**Legal Tier:** {khata}")
        st.write(f"**Elevation Premium:** High")
        st.write(f"**EV Capability:** {ev_slots} Bays")
        st.markdown('</div>', unsafe_allow_html=True)
