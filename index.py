import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium

# --- 1. THE IMMUTABLE THEME (STOPS THE SNAP) ---
st.set_page_config(page_title="AURUM | Satellite Node", layout="wide", initial_sidebar_state="expanded")

# Inject CSS to remove all padding and force a dark canvas immediately
st.markdown("""
    <style>
    /* Force immediate black background to stop white/gray flickering */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #D4AF37 !important;
    }
    
    /* Remove padding around the map for a "Big Map" feel */
    .block-container { padding: 0rem !important; max-width: 100% !important; }
    header, footer { visibility: hidden; }

    /* Polished Sidebar - No Border to avoid visual 'jumps' */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid rgba(212, 175, 55, 0.1);
    }
    
    /* Elegant Metric Cards */
    .metric-box {
        background: rgba(10, 10, 10, 0.8);
        border: 1px solid #D4AF37;
        padding: 20px;
        border-radius: 4px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE GEOSPATIAL DATABASE ---
mumbai_nodes = {
    "Worli Sea Face": {"coords": [19.0176, 72.8172], "base": 85000, "growth": 1.07},
    "Pali Hill, Bandra": {"coords": [19.0655, 72.8252], "base": 98000, "growth": 1.08},
    "Malabar Hill": {"coords": [18.9548, 72.7985], "base": 118000, "growth": 1.05},
    "Hiranandani, Powai": {"coords": [19.1176, 72.9060], "base": 36000, "growth": 1.12},
    "Palm Beach Road": {"coords": [19.0330, 73.0297], "base": 24000, "growth": 1.25}
}

# --- 3. THE VAULT (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center; letter-spacing:10px;'>AURUM</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    loc_node = st.selectbox("SELECT NODE", list(mumbai_nodes.keys()))
    area = st.number_input("CARPET AREA", 500, 20000, 1500)
    floor = st.slider("FLOOR LEVEL", 0, 80, 20)
    
    st.markdown("### PARAMETERS")
    vastu = st.toggle("VASTU ALIGNMENT", value=True)
    automation = st.toggle("AI AUTOMATION", value=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    execute = st.button("RUN VALUATION", use_container_width=True)

# --- 4. THE MAIN SATELLITE INTERFACE ---
data = mumbai_nodes[loc_node]

# Centered Large Map
# Using a slightly higher zoom for that "Exquisite" detail
m = folium.Map(
    location=data['coords'], 
    zoom_start=18, 
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
    attr='Google Satellite'
)

# Custom Gold Pulsing Marker
folium.CircleMarker(
    location=data['coords'],
    radius=40,
    color='#D4AF37',
    fill=True,
    fill_color='#D4AF37',
    fill_opacity=0.2,
    popup=f"{loc_node} - Valuation Node"
).add_to(m)

# Centering the Map Widget
st_folium(m, width=2000, height=600, use_container_width=True)

# --- 5. VALUATION DRAWER (BELOW MAP) ---
if execute:
    # Logic Engine
    price_2025 = (data['base'] * area * (1 + floor * 0.006)) / 10000000
    price_2026 = price_2025 * data['growth']

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""<div class="metric-box">
            <p style='color:#888; font-size:12px;'>2026 VALUATION</p>
            <h2 style='margin:0;'>₹ {price_2026:.2f} Cr</h2>
        </div>""", unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""<div class="metric-box">
            <p style='color:#888; font-size:12px;'>YOY GROWTH</p>
            <h2 style='margin:0;'>+{round((data['growth']-1)*100, 1)}%</h2>
        </div>""", unsafe_allow_html=True)
        
    with col3:
        # Mini DNA Chart
        fig = go.Figure(data=go.Scatterpolar(
            r=[90, 85, 95, 70, 80],
            theta=['ROI', 'Legal', 'Vastu', 'Infra', 'Luxe'],
            fill='toself', line_color='#D4AF37'
        ))
        fig.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=False)),
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False, height=150, margin=dict(l=0,r=0,t=0,b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.markdown("<p style='text-align:center; color:#555;'>Adjust parameters in the Vault and click Execute to view intelligence.</p>", unsafe_allow_html=True)
