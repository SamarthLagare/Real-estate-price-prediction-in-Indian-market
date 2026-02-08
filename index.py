import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# =====================================================
# PAGE CONFIG + STATE
# =====================================================
st.set_page_config("SAM VISION | ML Housing Predictor", layout="wide")

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
# LOCATION DATA (Lat, Lon)
# =====================================================
LOCATIONS = {
    "Mumbai - Bandra West": [19.0655,72.8252],
    "Mumbai - Worli": [19.0176,72.8172],
    "Delhi - Vasant Vihar": [28.5583,77.1606],
    "Bengaluru - Indiranagar": [12.9719,77.6412],
    "London - Canary Wharf": [51.5054,-0.0235],
    "New York - Manhattan": [40.7831,-73.9712],
    "Dubai - Marina": [25.0800,55.1400],
    "Singapore - Orchard": [1.3048,103.8318],
    "Paris - La Défense": [48.8924,2.2369],
    "Tokyo - Minato": [35.6581,139.7516],
}

# =====================================================
# SIDEBAR INPUTS
# =====================================================
with st.sidebar:
    st.markdown("## 🏙️ SAM VISION")

    location = st.selectbox("Location", list(LOCATIONS.keys()))
    area = st.slider("Carpet Area (sqft)", 300, 5000, 1200)
    floor = st.slider("Floor Level", 0, 80, 20)
    age = st.slider("Building Age (years)", 0, 50, 5)
    amenities = st.slider("Amenities Score", 1, 10, 7)
    metro = st.toggle("Metro Nearby", True)
    premium_builder = st.toggle("Premium Builder", True)

    if st.button("RUN ML VALUATION"):
        st.session_state.run = True

# =====================================================
# LANDING
# =====================================================
if not st.session_state.run:
    st.markdown("<h1 style='text-align:center;font-size:80px'>SAM VISION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>ML-Powered Housing Price Prediction</p>", unsafe_allow_html=True)
    st.stop()

# =====================================================
# SYNTHETIC TRAINING DATA (REALISTIC)
# =====================================================
np.random.seed(42)
rows = 5000

df = pd.DataFrame({
    "area": np.random.randint(300, 5000, rows),
    "floor": np.random.randint(0, 80, rows),
    "age": np.random.randint(0, 50, rows),
    "amenities": np.random.randint(1, 10, rows),
    "metro": np.random.choice([0,1], rows),
    "premium_builder": np.random.choice([0,1], rows),
})

# True price generation (₹ Crores)
df["price_cr"] = (
    df["area"] * 60000 *
    (1 + df["floor"] * 0.004) *
    (1 - df["age"] * 0.006) *
    (1 + df["amenities"] * 0.015) *
    (1.05 ** df["metro"]) *
    (1.12 ** df["premium_builder"])
) / 1e7

X = df.drop("price_cr", axis=1)
y = df["price_cr"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# =====================================================
# ML MODELS
# =====================================================
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(),
    "Lasso Regression": Lasso(),
    "Random Forest": RandomForestRegressor(n_estimators=150, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42)
}

results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    r2 = r2_score(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    results.append((name, r2, rmse, model))

results_df = pd.DataFrame(results, columns=["Model", "R² Score", "RMSE", "model"])
best_row = results_df.sort_values("R² Score", ascending=False).iloc[0]
best_model = best_row["model"]

# =====================================================
# USER PREDICTION (₹ CRORES)
# =====================================================
user_input = pd.DataFrame([{
    "area": area,
    "floor": floor,
    "age": age,
    "amenities": amenities,
    "metro": int(metro),
    "premium_builder": int(premium_builder),
}])

predicted_price = best_model.predict(user_input)[0]

# =====================================================
# SATELLITE MAP
# =====================================================
lat, lon = LOCATIONS[location]

m = folium.Map(
    location=[lat, lon],
    zoom_start=16,
    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    attr="Google Satellite"
)

folium.CircleMarker(
    [lat, lon],
    radius=max(20, predicted_price * 2),
    color="#D4AF37",
    fill=True,
    fill_opacity=0.45,
    popup=f"₹ {predicted_price:.2f} Cr"
).add_to(m)

st_folium(m, height=450, use_container_width=True)

# =====================================================
# RESULT BOARD
# =====================================================
st.markdown(f"""
<div class="white-board">
<p>{location}</p>
<h1>₹ {predicted_price:.2f} Cr</h1>
<p><b>Best Model:</b> {best_row['Model']}</p>
<p><b>Accuracy (R²):</b> {best_row['R² Score']:.3f}</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# MODEL COMPARISON
# =====================================================
st.subheader("📊 Model Performance Comparison")
st.dataframe(results_df.drop(columns=["model"]).sort_values("R² Score", ascending=False))
