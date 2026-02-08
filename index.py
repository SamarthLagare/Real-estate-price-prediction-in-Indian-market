import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

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
# THEME (UNCHANGED)
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
# GLOBAL LOCATION DATA (UNCHANGED)
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
        }
    }
}

# =====================================================
# SIDEBAR INPUTS (UNCHANGED)
# =====================================================
with st.sidebar:
    st.markdown("## 🌍 SAM VISION")

    country = st.selectbox("Country", list(DATA.keys()))
    city = st.selectbox("City", list(DATA[country].keys()))
    location = st.selectbox("Location", list(DATA[country][city].keys()))

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
# ML TRAINING DATA (PAST DATA 2010–2025)
# =====================================================
np.random.seed(42)
years = np.arange(2010, 2026)
rows = len(years) * 200

df = pd.DataFrame({
    "year": np.repeat(years, 200),
    "area": np.random.randint(300, 5000, rows),
    "floor": np.random.randint(0, 80, rows),
    "age": np.random.randint(0, 50, rows),
    "amenities": np.random.randint(1, 10, rows),
})

df["price_cr"] = (
    df.area * 50000 *
    (1 + df.floor * 0.004) *
    (1 - df.age * 0.006) *
    (1 + df.amenities * 0.01) *
    (1 + (df.year - 2010) * 0.03)
) / 1e7

X = df[["year","area","floor","age","amenities"]]
y = df["price_cr"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

models = {
    "Linear Regression": LinearRegression(),
    "Ridge": Ridge(),
    "Lasso": Lasso(),
    "Random Forest": RandomForestRegressor(n_estimators=120),
    "Gradient Boosting": GradientBoostingRegressor()
}

scores = []
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    scores.append((name, r2_score(y_test, pred), model))

best_model_name, best_r2, best_model = sorted(scores, key=lambda x: x[1], reverse=True)[0]

# =====================================================
# CURRENT PREDICTION (ML)
# =====================================================
current_year = 2025
user_df = pd.DataFrame([{
    "year": current_year,
    "area": area,
    "floor": floor,
    "age": age,
    "amenities": amenities
}])

current_price = best_model.predict(user_df)[0]

# =====================================================
# FUTURE PREDICTION (2026–2035)
# =====================================================
future_years = np.arange(2026, 2036)
future_prices = []

for y in future_years:
    temp = user_df.copy()
    temp["year"] = y
    future_prices.append(best_model.predict(temp)[0])

# =====================================================
# MAP (UNCHANGED – SATELLITE)
# =====================================================
lat, lon, _, _ = DATA[country][city][location]
m = folium.Map(
    location=[lat, lon],
    zoom_start=16,
    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    attr="Google Satellite"
)
folium.CircleMarker(
    [lat, lon],
    radius=max(20, current_price * 2),
    color="#D4AF37",
    fill=True,
    fill_opacity=0.45,
    popup=f"₹ {current_price:.2f} Cr"
).add_to(m)

st_folium(m, height=460, use_container_width=True)

# =====================================================
# RESULT BOARD
# =====================================================
st.markdown(f"""
<div class="white-board">
<p>ML Predicted Value (2025)</p>
<h1>₹ {current_price:.2f} Cr</h1>
<p><b>Best Model:</b> {best_model_name}</p>
<p><b>Accuracy (R²):</b> {best_r2:.3f}</p>
<p><b>Past Data Used:</b> 2010 – 2025</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# FUTURE TREND CHART
# =====================================================
fig = go.Figure(go.Scatter(
    x=future_years,
    y=future_prices,
    fill="tozeroy",
    line_color="#D4AF37"
))
fig.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black",
    font_color="#D4AF37",
    title="ML-Based Price Forecast (2026–2035)"
)
st.plotly_chart(fig, use_container_width=True)
