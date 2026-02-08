import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG + STATE
# =====================================================
st.set_page_config(
    page_title="SAM VISION | Global Housing AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "run" not in st.session_state:
    st.session_state.run = False

# =====================================================
# THEME
# =====================================================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
    background:black; color:#D4AF37;
}
header, footer {visibility:hidden;}
[data-testid="stSidebar"] {border-right:2px solid #D4AF37;}
.white-board {
    background:white;
    color:black;
    padding:32px;
    border-left:10px solid #D4AF37;
    border-radius:10px;
    box-shadow:0 15px 50px rgba(212,175,55,.45);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# GLOBAL LOCATION DATABASE
# lat, lon, base_price_per_sqft, growth
# =====================================================
DATA = {
    "India": {
        "Mumbai": {
            "Malabar Hill":[18.9548,72.7985,115000,1.05],
            "Colaba":[18.9067,72.8147,82000,1.06],
            "Worli":[19.0176,72.8172,85000,1.07],
            "Lower Parel":[18.9986,72.8295,65000,1.09],
            "Bandra West":[19.0655,72.8252,92000,1.08],
            "Juhu":[19.1075,72.8263,78000,1.06],
            "Andheri West":[19.1364,72.8296,52000,1.10],
            "Powai":[19.1176,72.9060,34000,1.10],
            "Chembur":[19.0623,72.8977,42000,1.11],
            "Borivali West":[19.2345,72.8567,35000,1.12],
        },
        "Delhi": {
            "Lutyens":[28.6172,77.2080,90000,1.05],
            "Vasant Vihar":[28.5583,77.1606,42000,1.08],
            "GK-1":[28.5484,77.2377,38000,1.09],
            "Dwarka":[28.5921,77.0460,25000,1.12],
            "Rohini":[28.7380,77.0822,23000,1.13],
            "Saket":[28.5244,77.2066,36000,1.09],
            "Karol Bagh":[28.6517,77.1907,30000,1.10],
            "Pitampura":[28.6980,77.1310,32000,1.10],
            "Mayur Vihar":[28.6096,77.2926,27000,1.11],
            "Noida":[28.5355,77.3910,24000,1.13],
        }
    },
    "USA": {
        "New York": {
            "Manhattan":[40.7831,-73.9712,120000,1.05],
            "Brooklyn":[40.6782,-73.9442,85000,1.07],
            "Queens":[40.7282,-73.7949,78000,1.08],
            "Bronx":[40.8448,-73.8648,70000,1.09],
            "Harlem":[40.8116,-73.9465,82000,1.07],
            "SoHo":[40.7233,-74.0030,110000,1.05],
            "Chelsea":[40.7465,-74.0014,100000,1.06],
            "Tribeca":[40.7163,-74.0086,125000,1.04],
            "Upper East":[40.7736,-73.9566,115000,1.05],
            "Upper West":[40.7870,-73.9754,108000,1.06],
        }
    },
    "UK": {
        "London": {
            "Mayfair":[51.5090,-0.1470,110000,1.04],
            "Chelsea":[51.4875,-0.1687,98000,1.05],
            "Canary Wharf":[51.5054,-0.0235,75000,1.08],
            "Greenwich":[51.4826,-0.0077,68000,1.09],
            "Camden":[51.5416,-0.1433,82000,1.07],
            "Soho":[51.5138,-0.1316,90000,1.06],
            "Hackney":[51.5450,-0.0550,72000,1.09],
            "Islington":[51.5380,-0.0990,85000,1.07],
            "Wembley":[51.5588,-0.2817,65000,1.10],
            "Croydon":[51.3762,-0.0982,60000,1.11],
        }
    }
}

# =====================================================
# SIDEBAR – LOCATION SELECTION
# =====================================================
with st.sidebar:
    st.markdown("## 🌍 SAM VISION")

    country = st.selectbox("Country", list(DATA.keys()))
    city = st.selectbox("City", list(DATA[country].keys()))
    location = st.selectbox("Location", list(DATA[country][city].keys()))

    st.divider()

    with st.expander("🏠 PROPERTY DETAILS"):
        area = st.slider("Carpet Area (sqft)", 300, 5000, 1200)
        floor = st.slider("Floor Level", 0, 80, 20)
        age = st.slider("Building Age (yrs)", 0, 50, 5)
        ceiling = st.slider("Ceiling Height (ft)", 9.0, 15.0, 11.0)

    with st.expander("🏢 SOCIETY"):
        amenities = st.slider("Amenities Score", 1, 10, 7)
        density = st.slider("Flats per Floor", 2, 20, 6)
        elevators = st.slider("Elevators", 1, 8, 3)
        security = st.slider("Security Level", 1, 5, 4)

    with st.expander("🌿 ENVIRONMENT"):
        view = st.selectbox("View", ["Internal","City","Water","Park"])
        noise = st.slider("Noise Level", 1, 10, 4)
        pollution = st.slider("Pollution Index", 1, 10, 4)
        greenery = st.slider("Green Cover", 1, 10, 6)

    with st.expander("🚇 CONNECTIVITY"):
        metro = st.toggle("Metro Nearby", True)
        school = st.toggle("School < 2km", True)
        hospital = st.toggle("Hospital < 3km", True)
        cbd = st.slider("CBD Distance (km)", 1, 40, 8)

    with st.expander("✨ QUALITY"):
        builder = st.selectbox("Builder Grade", ["Average","Good","Premium"])
        smart = st.toggle("Smart Home", True)
        vastu = st.toggle("Vastu", True)

    if st.button("RUN VALUATION"):
        st.session_state.run = True

# =====================================================
# LANDING
# =====================================================
if not st.session_state.run:
    st.markdown("<h1 style='text-align:center;font-size:80px'>SAM VISION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Global Micro-Level Housing Intelligence</p>", unsafe_allow_html=True)
    st.stop()

# =====================================================
# VALUATION ENGINE (₹ CRORES)
# =====================================================
lat, lon, rate, growth = DATA[country][city][location]

base_price = (rate * area * (1 + floor*0.004)) / 1e7

price_cr = base_price * (
    growth *
    max(0.85, 1 - age*0.006) *
    (1 + (ceiling-10)*0.015) *
    (1 + amenities*0.01) *
    (1 - density*0.008) *
    (1 + elevators*0.02) *
    (1 + security*0.02) *
    {"Internal":0.97,"City":1.02,"Water":1.10,"Park":1.06}[view] *
    (1 - noise*0.01) *
    (1 - pollution*0.01) *
    (1 + greenery*0.01) *
    (1.04 if metro else 1) *
    (1.03 if school else 1) *
    (1.03 if hospital else 1) *
    (1 - cbd*0.005) *
    {"Average":1,"Good":1.05,"Premium":1.12}[builder] *
    (1.04 if smart else 1) *
    (1.03 if vastu else 1)
)

low, high = price_cr*0.95, price_cr*1.05

# =====================================================
# SATELLITE MAP
# =====================================================
m = folium.Map(
    location=[lat,lon],
    zoom_start=16,
    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    attr="Google Satellite"
)
folium.CircleMarker(
    [lat,lon],
    radius=max(20, price_cr*2),
    color="#D4AF37",
    fill=True,
    fill_opacity=0.45,
    popup=f"₹ {price_cr:.2f} Cr"
).add_to(m)

st_folium(m, height=460, use_container_width=True)

# =====================================================
# RESULT BOARD
# =====================================================
st.markdown(f"""
<div class="white-board">
<p>{location}, {city}, {country}</p>
<h1>₹ {price_cr:.2f} Cr</h1>
<p>Confidence Range: ₹ {low:.2f} – ₹ {high:.2f} Cr</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# FUTURE PROJECTION
# =====================================================
years = np.arange(2026, 2037)
values = [price_cr*(1.08**(y-2026)) for y in years]

fig = go.Figure(go.Scatter(x=years,y=values,fill="tozeroy",line_color="#D4AF37"))
fig.update_layout(paper_bgcolor="black",plot_bgcolor="black",font_color="#D4AF37")
st.plotly_chart(fig, use_container_width=True)
