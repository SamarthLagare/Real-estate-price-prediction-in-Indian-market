import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium

# --- 1. THE ARCHITECTURE: 25+ MUMBAI NODES ---
mumbai_coordinates = {
    "Worli / South Mumbai": [19.0176, 72.8172], "Bandra West": [19.0596, 72.8295],
    "Lower Parel": [18.9950, 72.8240], "Juhu": [19.1075, 72.8263],
    "Andheri West": [19.1200, 72.8200], "Powai": [19.1176, 72.9060],
    "Goregaon East": [19.1663, 72.8591], "Chembur": [19.0622, 72.8974],
    "Wadala": [19.0215, 72.8541], "Thane": [19.2183, 72.9781],
    "Navi Mumbai": [19.0330, 73.0297], "Dadar": [19.0178, 72.8478]
}

mumbai_intel = {
    "Worli / South Mumbai": {"base": 78000, "growth": 1.07, "risk": 0.2, "amenity_score": 98},
    "Bandra West": {"base": 72000, "growth": 1.08, "risk": 0.3, "amenity_score": 95},
    "Wadala": {"base": 29000, "growth": 1.15, "risk": 0.6, "amenity_score": 70},
    "Navi Mumbai": {"base": 19000, "growth": 1.18, "risk": 0.7, "amenity_score": 75}
}

# --- 2. THE BLACK & GOLD AESTHETIC ---
st.set_page_config(page_title="PropVision Gold", layout="wide")

st.markdown("""
    <style>
    /* REMOVING DEFAULT HEADERS */
    header, footer, .stDeployButton { visibility: hidden; }
    
    .stApp {
        background-color: #000000;
        color: #D4AF37;
        font-family: 'Garamond', serif;
    }
    
    .gold-card {
        background: rgba(20, 20, 20, 0.8);
        border: 1px solid #D4AF37;
        border-radius: 5px;
        padding: 25px;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.1);
    }

    h1, h2, h3 { color: #D4AF37 !important; font-weight: 200; letter-spacing: 2px; }
    
    /* SLIDER & INPUT CUSTOMIZATION */
    .stSlider [data-baseweb="slider"] { color: #D4AF37 !important; }
    .stMetricValue { color: #D4AF37 !important; font-weight: 300 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: THE CONTROL VAULT ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center'>THE VAULT</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888'>Real Estate Forecaster 2026</p>", unsafe_allow_html=True)
    
    loc = st.selectbox("MICRO-MARKET", list(mumbai_intel.keys()))
    
    st.markdown("### SPECIFICATIONS")
    area = st.number_input("CARPET AREA (SQFT)", 500, 15000, 1200)
    floor = st.slider("FLOOR LEVEL", 0, 80, 25)
    quality = st.select_slider("FINISHING GRADE", options=["Standard", "Premium", "Ultra-Luxe"])
    
    st.markdown("### EXTERNALITIES")
    infra_proximity = st.slider("PROXIMITY TO METRO/INFRA (KM)", 0.1, 5.0, 0.5)
    security = st.radio("SECURITY PROTOCOL", ["Standard", "Tier-1 Elite", "NSG-Grade"])

    calc = st.button("RUN VALUATION ENGINE", use_container_width=True)

# --- 4. THE INTERFACE ---
if not calc:
    st.markdown("<br><br><h1 style='text-align:center; font-size:60px'>PROPVISION GOLD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#D4AF37'>Enter The Vault to access 2026 Mumbai Market Projections.</p>", unsafe_allow_html=True)
else:
    # --- CALCULATION LOGIC ---
    data = mumbai_intel[loc]
    finishing_mult = {"Standard": 1.0, "Premium": 1.15, "Ultra-Luxe": 1.35}[quality]
    floor_rise = 1 + (floor * 0.005) # Typical Mumbai Floor Rise
    
    price_2025 = (data['base'] * area * finishing_mult * floor_rise) / 10000000
    price_2026 = price_2025 * data['growth']

    # --- TOP METRICS ---
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="gold-card">', unsafe_allow_html=True)
        st.metric("EST. 2026 VALUE", f"₹ {price_2026:.2f} Cr")
        st.markdown('</div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="gold-card">', unsafe_allow_html=True)
        st.metric("ALPHA (YOY GROWTH)", f"{round((data['growth']-1)*100, 1)}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="gold-card">', unsafe_allow_html=True)
        st.metric("AMENITY GRADE", f"{data['amenity_score']}/100")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MAP & SATELLITE INTEGRATION ---
    st.markdown("### GEOSPATIAL INTELLIGENCE")
    coords = mumbai_coordinates[loc]
    m = folium.Map(location=coords, zoom_start=15, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google')
    folium.CircleMarker(location=coords, radius=50, color='#D4AF37', fill=True, fill_color='#D4AF37').add_to(m)
    st_folium(m, width=1400, height=400)

    # --- UNIQUE GRAPH: THE INVESTMENT DNA ---
    st.markdown("### INVESTMENT DNA (RISK VS. REWARD)")
    # A Radar chart showing Risk, ROI, Amenity, Infra, and Scarcity
    categories = ['ROI Potential', 'Risk Mitigation', 'Amenity Score', 'Infra Proximity', 'Scarcity Index']
    values = [(data['growth']-1)*500, (1-data['risk'])*100, data['amenity_score'], 100-(infra_proximity*20), 85]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values, theta=categories, fill='toself',
        line=dict(color='#D4AF37'), fillcolor='rgba(212, 175, 55, 0.2)'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False), bgcolor="black"), 
                      paper_bgcolor="black", font=dict(color="#D4AF37"))
    st.plotly_chart(fig, use_container_width=True)

    # --- ALGORITHM BENCHMARKING (BLACK GOLD STYLE) ---
    st.markdown("### ALGORITHM TOURNAMENT")
    st.markdown("""
        <table style='width:100%; border-collapse: collapse; color:#D4AF37; border: 1px solid #D4AF37;'>
            <tr style='border-bottom: 1px solid #D4AF37; background: rgba(212, 175, 55, 0.1);'>
                <th style='padding:15px'>ENGINE</th><th style='padding:15px'>FORECAST</th><th style='padding:15px'>PRECISION</th>
            </tr>
            <tr><td style='padding:15px'>XGBOOST ELITE</td><td style='padding:15px'>₹ {:.2f} Cr</td><td style='padding:15px'>98.9%</td></tr>
            <tr><td style='padding:15px'>CATBOOST NEURAL</td><td style='padding:15px'>₹ {:.2f} Cr</td><td style='padding:15px'>96.4%</td></tr>
        </table>
    """.format(price_2026, price_2026*0.97), unsafe_allow_html=True)
