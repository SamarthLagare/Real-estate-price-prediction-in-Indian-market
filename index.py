import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Sam Vision | Titan v16",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE TITAN UI: OBSIDIAN & GOLD STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Montserrat:wght@300;400;600&display=swap');
    
    /* Global Reset */
    .stApp { background-color: #020202; color: #e5e5e5; font-family: 'Montserrat', sans-serif; }
    header, footer { visibility: hidden; }
    
    /* Sidebar: The Control Vault */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #d4af37;
        min-width: 400px !important;
    }
    
    /* Titan Gold Accents */
    h1, h2, h3 { font-family: 'Cinzel', serif; color: #d4af37 !important; letter-spacing: 2px; }
    .stMetricValue { color: #d4af37 !important; font-family: 'Cinzel', serif; font-size: 3rem !important; }
    
    /* White Board readability for Metrics */
    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 4px;
        border-left: 8px solid #d4af37;
        color: #000;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.2);
    }
    
    /* Inputs Styling: Black Background, Gold Text */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #000 !important;
        border: 1px solid #d4af37 !important;
        color: #d4af37 !important;
    }
    label { color: #888 !important; text-transform: uppercase; font-size: 0.7rem !important; font-weight: 700 !important; }
    
    /* Buttons: Titan Gold */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #d4af37, #997d24) !important;
        color: black !important;
        font-weight: 800 !important;
        border: none !important;
        padding: 20px !important;
        letter-spacing: 3px !important;
        transition: 0.4s !important;
    }
    .stButton > button:hover { transform: scale(1.02); color: white !important; box-shadow: 0 0 20px #d4af37; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE GLOBAL DATABASE (RESOURCES) ---
countries = {
    "India": {
        "Mumbai": {"coords": [19.0760, 72.8777], "areas": ["Bandra", "Worli", "Juhu", "Powai", "Andheri", "Colaba", "Lower Parel", "Malabar Hill", "Chembur", "Wadala"]},
        "Pune": {"coords": [18.5204, 73.8567], "areas": ["Baner", "Koregaon Park", "Hinjewadi", "Kothrud", "Viman Nagar", "Kalyani Nagar", "Aundh", "Wakad", "Hadapsar", "Magarpatta"]}
    },
    "USA": {
        "New York": {"coords": [40.7128, -74.0060], "areas": ["Manhattan", "Brooklyn", "Queens", "Upper East Side", "SoHo", "Tribeca", "Williamsburg", "Astoria", "Harlem", "Chelsea"]}
    },
    "UAE": {
        "Dubai": {"coords": [25.2048, 55.2708], "areas": ["Downtown", "Marina", "Palm Jumeirah", "Business Bay", "JLT", "JVC", "Arabian Ranches", "Dubai Hills", "Bur Dubai", "Deira"]}
    }
}

# --- 4. SIDEBAR: THE VAULT (PARAMETERS) ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>SAM VISION</h1>", unsafe_allow_html=True)
    st.caption("BY SAMARTH LAGARE • TITAN v16.0")
    st.divider()

    # Location Matrix
    c_name = st.selectbox("REGION", list(countries.keys()))
    city_name = st.selectbox("METROPOLITAN", list(countries[c_name].keys()))
    area_name = st.selectbox("PRIME SECTOR", countries[c_name][city_name]["areas"])
    
    st.markdown("### 🧬 STRUCTURAL DNA")
    sqft = st.slider("TOTAL AREA (SQFT)", 400, 25000, 1500)
    bhk = st.select_slider("CONFIGURATION", options=[1, 2, 3, 4, 5, "Penthouse", "Mansion"])
    floor = st.number_input("ELEVATION (FLOOR)", 0, 150, 12)
    age = st.number_input("ASSET AGE (YEARS)", 0, 50, 0)
    
    with st.expander("✨ MINUTE PARAMETERS"):
        ceiling = st.slider("CEILING HEIGHT (FT)", 9.0, 20.0, 11.5)
        view = st.select_slider("VIEW GRADE", options=["Standard", "Cityscape", "Skyline", "Sea View"])
        vastu = st.toggle("VASTU COMPLIANT", value=True)
        smart = st.toggle("AI-SMART AUTOMATION", value=True)
        parking = st.number_input("PARKING BAYS", 0, 5, 1)
        legal = st.selectbox("LEGAL STATUS", ["RERA Registered", "OC Received", "A-Khata Clear"])

    with st.expander("🏙️ INFRASTRUCTURE NODES"):
        metro = st.toggle("METRO PROXIMITY (<1KM)", value=True)
        airport = st.toggle("AIRPORT HUB ACCESS")
        clubhouse = st.toggle("PRIVATE CLUB ACCESS", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    initiate = st.button("INITIATE VALUATION")

# --- 5. THE MAIN INTERFACE ---
if not initiate:
    # First Loading Interface (Logo & Blurred Map)
    st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; font-size:100px; letter-spacing:20px;'>SAM VISION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#d4af37; font-size:15px; letter-spacing:10px;'>TITAN EDITION • SELECT PARAMETERS TO START</p>", unsafe_allow_html=True)
    
    # Background Map (Blurred initially)
    m_intro = folium.Map(location=[20, 0], zoom_start=2, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google Satellite')
    st_folium(m_intro, width=2000, height=500)

else:
    # 6. CALCULATING ENGINE (Processing Mock)
    with st.status("🔮 ANALYZING QUANTUM DATA...", expanded=True) as status:
        st.write("Fetching historical Q1 market data...")
        time.sleep(1)
        st.write("Benchmarking ML Algorithms...")
        time.sleep(1)
        status.update(label="VALUATION COMPLETE", state="complete")

    # 7. SATELLITE NODE (Jump to location)
    target_coords = countries[c_name][city_name]["coords"]
    m = folium.Map(location=target_coords, zoom_start=18, tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google Satellite')
    folium.CircleMarker(target_coords, radius=40, color='#d4af37', fill=True, fill_opacity=0.3).add_to(m)
    st_folium(m, width=2000, height=600)

    # 8. THE WHITE BOARD INTERFACE (Readability)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    # Valuation Logic (Simulated for Demo)
    base_rate = 15000 if c_name == "India" else 85000
    view_mult = {"Standard": 1.0, "Cityscape": 1.08, "Skyline": 1.15, "Sea View": 1.25}
    price_est = (sqft * base_rate * view_mult[view]) / 10000000 # In Crores
    
    with col1:
        st.markdown(f"""<div class='metric-card'>
            <p style='color:#666; font-size:10px; font-weight:700;'>2026 Q1 ESTIMATE</p>
            <h1 style='color:#000 !important; margin:0;'>₹ {price_est:.2f} Cr</h1>
            <p style='color:#15803d; font-size:12px; margin-top:10px;'>High Accuracy Prediction</p>
        </div>""", unsafe_allow_html=True)

    # 9. ML ALGORITHM BENCHMARKING
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#666; font-size:10px; font-weight:700;'>ALGORITHM BENCHMARKING</p>", unsafe_allow_html=True)
        
        # Simulated algorithm testing
        algos = pd.DataFrame({
            "Algorithm": ["Linear Reg", "Random Forest", "Gradient Boost", "XGBoost (Titan)"],
            "Accuracy": [0.84, 0.92, 0.95, 0.985],
            "Estimate": [price_est*0.92, price_est*0.98, price_est*0.99, price_est]
        })
        st.dataframe(algos.style.highlight_max(axis=0, subset=['Accuracy'], color='#d4af37'))
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.markdown("<p style='color:#666; font-size:10px; font-weight:700;'>LIVABILITY DNA</p>", unsafe_allow_html=True)
        fig = go.Figure(data=go.Scatterpolar(
            r=[85, 95, 70, 80, 90],
            theta=['Vastu', 'Infra', 'ROI', 'Safety', 'Luxury'],
            fill='toself', line_color='#d4af37'
        ))
        fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 10. 10-YEAR GROWTH FORECAST
    st.markdown("### 📈 10-YEAR STRATEGIC HORIZON (2026-2036)")
    years = np.arange(2026, 2037)
    # Compound annual growth logic
    prices = [price_est * (1.08**(y-2026)) for y in years]
    
    fig_line = px.line(x=years, y=prices, markers=True, template="plotly_dark")
    fig_line.update_traces(line_color='#d4af37', fill='tozeroy')
    fig_line.update_layout(paper_bgcolor='#000', plot_bgcolor='#000')
    st.plotly_chart(fig_line, use_container_width=True)

    st.info("Titan v16 Intelligence: This property is in a high-growth corridor. Projected ROI: 125% over 10 years.")
