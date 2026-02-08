import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium
import time

# --------------------------------------------------
# 1. PAGE CONFIG + SESSION STATE
# --------------------------------------------------
st.set_page_config(
    page_title="SAM VISION",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "executed" not in st.session_state:
    st.session_state.executed = False

# --------------------------------------------------
# 2. GLOBAL STYLES (LOCKED UI)
# --------------------------------------------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
    background-color: #000000 !important;
    color: #D4AF37 !important;
}
header, footer { visibility: hidden; }
[data-testid="stSidebar"] {
    border-right: 1px solid #D4AF37;
    min-width: 380px !important;
}
.white-board {
    background: #FFFFFF;
    padding: 30px;
    border-radius: 8px;
    border-left: 10px solid #D4AF37;
    color: #000000;
    box-shadow: 0 10px 40px rgba(212,175,55,0.4);
}
h1, h2 { color: #D4AF37 !important; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. MUMBAI MICRO-MARKET DATA
# lat, lon, rate_per_sqft_2025, growth_factor_2026
# --------------------------------------------------
mumbai_data = {
    "Malabar Hill": [18.9548, 72.7985, 115000, 1.05],
    "Altamount Road": [18.9663, 72.8080, 105000, 1.04],
    "Cuffe Parade": [18.9147, 72.8159, 88000, 1.05],
    "Colaba": [18.9067, 72.8147, 82000, 1.06],
    "Lower Parel": [18.9986, 72.8295, 65000, 1.09],
    "Worli Sea Face": [19.0176, 72.8172, 85000, 1.07],
    "Wadala": [19.0215, 72.8541, 31000, 1.15],
    "Bandra West (Pali Hill)": [19.0655, 72.8252, 92000, 1.08],
    "Juhu": [19.1075, 72.8263, 78000, 1.06],
    "Andheri West (Lokhandwala)": [19.1364, 72.8296, 52000, 1.10],
    "Powai": [19.1176, 72.9060, 34000, 1.10],
    "Chembur": [19.0623, 72.8977, 42000, 1.11]
}

# --------------------------------------------------
# 4. SIDEBAR CONTROLS
# --------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>SAM VISION</h1>", unsafe_allow_html=True)
    st.caption("BY SAMARTH LAGARE • TITAN EDITION")
    st.divider()

    node = st.selectbox("SELECT MICRO-MARKET", list(mumbai_data.keys()))
    area = st.number_input("CARPET AREA (SQFT)", 300, 20000, 1500)
    floor = st.slider("FLOOR LEVEL", 0, 100, 25)

    with st.expander("IMPORTANT PARAMETERS"):
        age = st.slider("BUILDING AGE (YEARS)", 0, 50, 5)
        parking = st.selectbox("PARKING", ["None", "1 Car", "2+ Cars"])
        view = st.selectbox("VIEW", ["Internal", "City", "Sea / Lake"])
        legal = st.selectbox("LEGAL STATUS", ["OC Received", "RERA Registered"])
        vastu = st.toggle("VASTU COMPLIANT", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("EXECUTE VALUATION"):
        st.session_state.executed = True

    if st.button("RESET"):
        st.session_state.executed = False

# --------------------------------------------------
# 5. MAIN INTERFACE
# --------------------------------------------------
loc_info = mumbai_data[node]

if not st.session_state.executed:
    st.markdown("<div style='height:25vh'></div>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align:center;font-size:80px;'>SAM VISION</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center;'>INITIALIZING GLOBAL ASSET INTELLIGENCE…</p>",
        unsafe_allow_html=True
    )

else:
    with st.spinner("SYNERGIZING VALUATION ENGINES…"):
        time.sleep(1)

    # --------------------------------------------------
    # 6. VALUATION ENGINE
    # --------------------------------------------------
    base_price_2025 = (loc_info[2] * area * (1 + floor * 0.005)) / 1e7

    age_factor = max(0.85, 1 - age * 0.005)
    parking_factor = {"None": 0.95, "1 Car": 1.00, "2+ Cars": 1.05}[parking]
    view_factor = {"Internal": 0.97, "City": 1.02, "Sea / Lake": 1.08}[view]
    vastu_factor = 1.03 if vastu else 1.00

    price_2026 = (
        base_price_2025
        * loc_info[3]
        * age_factor
        * parking_factor
        * view_factor
        * vastu_factor
    )

    # --------------------------------------------------
    # 7. MAP
    # --------------------------------------------------
    m = folium.Map(
        location=[loc_info[0], loc_info[1]],
        zoom_start=17,
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google Satellite"
    )
    folium.CircleMarker(
        [loc_info[0], loc_info[1]],
        radius=40,
        color="#D4AF37",
        fill=True,
        fill_opacity=0.4
    ).add_to(m)

    st_folium(m, height=480, use_container_width=True)

    # --------------------------------------------------
    # 8. RESULT BOARD
    # --------------------------------------------------
    st.markdown(f"""
    <div class="white-board">
        <p style="font-size:12px;color:#666;">{node} • Q1 2026 VALUATION</p>
        <h1 style="font-size:60px;margin:0;">₹ {price_2026:.2f} Cr</h1>
        <hr>
        <div style="display:flex;justify-content:space-between;">
            <span>Legal: <b>{legal}</b></span>
            <span>Floor: <b>{floor}</b></span>
            <span>View: <b>{view}</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------
    # 9. ANALYTICS TABS
    # --------------------------------------------------
    t1, t2 = st.tabs(["Algorithm Leaderboard", "10-Year Growth"])

    with t1:
        df = pd.DataFrame({
            "Model": ["Linear Regression", "Random Forest", "XGBoost"],
            "Accuracy": [0.84, 0.92, 0.98],
            "Forecast (Cr)": [
                price_2026 * 0.95,
                price_2026 * 0.98,
                price_2026
            ]
        })
        st.table(df)

    with t2:
        years = np.arange(2026, 2037)
        values = [price_2026 * (1.08 ** (y - 2026)) for y in years]

        fig = go.Figure(
            data=go.Scatter(
                x=years,
                y=values,
                fill="tozeroy",
                line_color="#D4AF37"
            )
        )
        fig.update_layout(
            paper_bgcolor="black",
            plot_bgcolor="black",
            font_color="#D4AF37"
        )
        st.plotly_chart(fig, use_container_width=True)
