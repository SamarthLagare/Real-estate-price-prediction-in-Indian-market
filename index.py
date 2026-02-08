import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium
import time

# =====================================================
# 1. PAGE CONFIG + SESSION STATE
# =====================================================
st.set_page_config(
    page_title="SAM VISION | Mumbai House Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "run" not in st.session_state:
    st.session_state.run = False

# =====================================================
# 2. GLOBAL UI STYLING
# =====================================================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
    background-color: #000000 !important;
    color: #D4AF37 !important;
}
header, footer { visibility: hidden; }
[data-testid="stSidebar"] {
    border-right: 1px solid #D4AF37;
    min-width: 420px !important;
}
.white-board {
    background: #FFFFFF;
    padding: 32px;
    border-radius: 10px;
    border-left: 10px solid #D4AF37;
    box-shadow: 0 15px 50px rgba(212,175,55,0.4);
    color: #000000;
}
h1, h2 { color: #D4AF37 !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. COMPLETE MUMBAI MICRO-MARKET DATABASE (2025)
# lat, lon, base_rate_per_sqft, growth_factor
# =====================================================
mumbai = {
    # SOUTH MUMBAI
    "Malabar Hill": [18.9548,72.7985,115000,1.05],
    "Altamount Road": [18.9663,72.8080,105000,1.04],
    "Cuffe Parade": [18.9147,72.8159,88000,1.05],
    "Colaba": [18.9067,72.8147,82000,1.06],
    "Marine Lines": [18.9430,72.8238,90000,1.05],
    "Tardeo": [18.9690,72.8120,78000,1.06],

    # CENTRAL
    "Lower Parel": [18.9986,72.8295,65000,1.09],
    "Worli": [19.0176,72.8172,85000,1.07],
    "Dadar": [19.0178,72.8478,52000,1.08],
    "Wadala": [19.0215,72.8541,31000,1.15],

    # WESTERN SUBURBS
    "Bandra West": [19.0655,72.8252,92000,1.08],
    "Juhu": [19.1075,72.8263,78000,1.06],
    "Santacruz West": [19.0896,72.8354,65000,1.07],
    "Andheri West": [19.1364,72.8296,52000,1.10],
    "Goregaon West": [19.1663,72.8526,42000,1.11],
    "Malad West": [19.1870,72.8484,38000,1.12],
    "Borivali West": [19.2345,72.8567,35000,1.12],

    # EASTERN SUBURBS
    "Kurla": [19.0726,72.8826,28000,1.14],
    "Ghatkopar East": [19.0858,72.9081,36000,1.12],
    "Vikhroli": [19.1100,72.9260,33000,1.13],
    "Powai": [19.1176,72.9060,34000,1.10],
    "Chembur": [19.0623,72.8977,42000,1.11],
    "Mulund West": [19.1726,72.9426,39000,1.12],
    "Thane West": [19.2183,72.9781,32000,1.14],

    # EXTENDED MMR
    "Mira Road": [19.2844,72.8737,22000,1.15],
    "Vasai": [19.3919,72.8397,18000,1.16],
    "Navi Mumbai (Vashi)": [19.0771,72.9987,26000,1.15]
}

# =====================================================
# 4. SIDEBAR – MICRO PARAMETERS
# =====================================================
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>SAM VISION</h1>", unsafe_allow_html=True)
    st.caption("Mumbai House Price Intelligence • Titan Edition")
    st.divider()

    node = st.selectbox("MICRO-MARKET LOCATION", list(mumbai.keys()))
    area = st.number_input("CARPET AREA (SQFT)", 300, 20000, 1200)
    floor = st.slider("FLOOR LEVEL", 0, 80, 20)

    with st.expander("PROPERTY ATTRIBUTES"):
        age = st.slider("BUILDING AGE (YEARS)", 0, 60, 5)
        parking = st.selectbox("PARKING", ["None", "1 Car", "2+ Cars"])
        view = st.selectbox("VIEW", ["Internal", "City", "Sea / Lake"])
        ceiling = st.slider("CEILING HEIGHT (FT)", 9.0, 15.0, 11.0)
        vastu = st.toggle("VASTU COMPLIANT", True)
        smart = st.toggle("SMART HOME", True)

    with st.expander("SOCIETY & BUILDER"):
        amenities = st.slider("AMENITY SCORE", 1, 10, 7)
        density = st.slider("DENSITY (FLATS/FLOOR)", 2, 20, 6)
        builder = st.selectbox("BUILDER GRADE", ["Average", "Good", "Premium"])

    with st.expander("INFRA & CONNECTIVITY"):
        metro = st.toggle("METRO < 500m", True)
        highway = st.toggle("HIGHWAY ACCESS", True)
        school = st.toggle("TOP SCHOOL < 2km", True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("RUN VALUATION"):
        st.session_state.run = True

    if st.button("RESET"):
        st.session_state.run = False

# =====================================================
# 5. MAIN SCREEN
# =====================================================
loc = mumbai[node]

if not st.session_state.run:
    st.markdown("<div style='height:30vh'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;font-size:85px;'>SAM VISION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Mumbai Real Estate Intelligence Engine</p>", unsafe_allow_html=True)

else:
    with st.spinner("RUNNING MICRO-MARKET VALUATION ENGINE…"):
        time.sleep(1)

    # =====================================================
    # 6. VALUATION ENGINE (REAL LOGIC)
    # =====================================================
    base = (loc[2] * area * (1 + floor * 0.004)) / 1e7

    factors = (
        loc[3] *
        max(0.85, 1 - age * 0.006) *
        {"None":0.95,"1 Car":1.0,"2+ Cars":1.05}[parking] *
        {"Internal":0.97,"City":1.02,"Sea / Lake":1.10}[view] *
        (1 + (ceiling-10)*0.015) *
        (1 + amenities*0.01) *
        (1 - density*0.008) *
        {"Average":1.0,"Good":1.05,"Premium":1.12}[builder] *
        (1.04 if metro else 1.0) *
        (1.03 if highway else 1.0) *
        (1.02 if school else 1.0) *
        (1.03 if vastu else 1.0) *
        (1.04 if smart else 1.0)
    )

    price = base * factors

    # =====================================================
    # 7. MAP
    # =====================================================
    m = folium.Map(location=[loc[0],loc[1]], zoom_start=16)
    folium.CircleMarker([loc[0],loc[1]], radius=40, color="#D4AF37", fill=True).add_to(m)
    st_folium(m, height=450, use_container_width=True)

    # =====================================================
    # 8. RESULT
    # =====================================================
    st.markdown(f"""
    <div class="white-board">
        <p>{node} • Ultra-Detailed Valuation (2026)</p>
        <h1>₹ {price:.2f} Cr</h1>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # 9. FUTURE PROJECTION
    # =====================================================
    years = np.arange(2026, 2037)
    values = [price*(1.085**(y-2026)) for y in years]

    fig = go.Figure(go.Scatter(x=years, y=values, fill="tozeroy"))
    fig.update_layout(paper_bgcolor="black", plot_bgcolor="black", font_color="#D4AF37")
    st.plotly_chart(fig, use_container_width=True)
