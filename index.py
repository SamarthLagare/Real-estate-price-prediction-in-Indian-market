import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# =====================================================
# 1. PAGE + STATE
# =====================================================
st.set_page_config("SAM VISION | Ultimate Mumbai Housing AI", layout="wide")

if "run" not in st.session_state:
    st.session_state.run = False

# =====================================================
# 2. STYLE
# =====================================================
st.markdown("""
<style>
html, body { background:#000; color:#D4AF37; }
.white { background:#fff; padding:30px; border-radius:12px; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. MUMBAI MICRO LOCATIONS (RATE BANDS)
# =====================================================
locations = {
    "South Mumbai": 90000,
    "Worli": 85000,
    "Lower Parel": 65000,
    "Bandra West": 92000,
    "Juhu": 78000,
    "Andheri West": 52000,
    "Powai": 34000,
    "Chembur": 42000,
    "Borivali West": 35000,
    "Thane West": 32000,
    "Navi Mumbai": 26000,
}

# =====================================================
# 4. SIDEBAR INPUTS (MICRO LEVEL)
# =====================================================
with st.sidebar:
    st.title("🏙️ SAM VISION AI")

    location = st.selectbox("Micro Location", list(locations.keys()))
    area = st.slider("Carpet Area (sqft)", 300, 3000, 1200)
    floor = st.slider("Floor Level", 0, 60, 15)
    total_floors = st.slider("Total Floors", 5, 80, 30)
    age = st.slider("Building Age", 0, 50, 5)
    ceiling = st.slider("Ceiling Height (ft)", 9.0, 15.0, 11.0)
    balcony = st.slider("Balconies", 0, 3, 1)

    amenities = st.slider("Amenities Score", 1, 10, 7)
    density = st.slider("Flats per Floor", 2, 20, 6)
    open_space = st.slider("Open Space %", 10, 60, 30)
    maintenance = st.slider("Monthly Maintenance (₹)", 2000, 20000, 6000)

    builder = st.slider("Builder Reputation", 1, 10, 7)
    vastu = st.checkbox("Vastu Compliant")
    smart = st.checkbox("Smart Home")
    sea_view = st.checkbox("Sea / Lake View")
    metro = st.slider("Metro Distance (km)", 0.1, 5.0, 1.2)
    flood = st.slider("Flood Risk (1=Low,10=High)", 1, 10, 3)

    if st.button("RUN AI VALUATION"):
        st.session_state.run = True

# =====================================================
# 5. SYNTHETIC TRAINING DATA
# =====================================================
np.random.seed(42)
rows = 4000

df = pd.DataFrame({
    "area": np.random.randint(300, 3000, rows),
    "floor": np.random.randint(0, 60, rows),
    "age": np.random.randint(0, 50, rows),
    "ceiling": np.random.uniform(9, 15, rows),
    "amenities": np.random.randint(1, 10, rows),
    "density": np.random.randint(2, 20, rows),
    "builder": np.random.randint(1, 10, rows),
    "metro": np.random.uniform(0.1, 5, rows),
    "flood": np.random.randint(1, 10, rows),
})

df["price"] = (
    df["area"] * 45000 *
    (1 + df["floor"]*0.004) *
    (1 - df["age"]*0.005) *
    (1 + df["amenities"]*0.01) *
    (1 - df["density"]*0.01) *
    (1 + df["builder"]*0.02) *
    (1 - df["metro"]*0.04) *
    (1 - df["flood"]*0.03)
) / 1e7

X = df.drop("price", axis=1)
y = df["price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# =====================================================
# 6. ML MODELS
# =====================================================
models = {
    "Linear": LinearRegression(),
    "Ridge": Ridge(),
    "Lasso": Lasso(),
    "Random Forest": RandomForestRegressor(n_estimators=200),
    "Gradient Boost": GradientBoostingRegressor(),
    "Extra Trees": ExtraTreesRegressor(n_estimators=200)
}

results = []

for name, model in models.items():
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", model)
    ])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    results.append((name, r2_score(y_test, pred), mean_absolute_error(y_test, pred)))

results_df = pd.DataFrame(results, columns=["Model", "R2 Score", "MAE"])
best_model_name = results_df.sort_values("R2 Score", ascending=False).iloc[0]["Model"]
best_model = models[best_model_name]

# =====================================================
# 7. PREDICTION
# =====================================================
input_data = pd.DataFrame([{
    "area": area,
    "floor": floor,
    "age": age,
    "ceiling": ceiling,
    "amenities": amenities,
    "density": density,
    "builder": builder,
    "metro": metro,
    "flood": flood
}])

best_model.fit(X, y)
prediction = best_model.predict(input_data)[0]

# =====================================================
# 8. OUTPUT
# =====================================================
if st.session_state.run:
    st.markdown(f"""
    <div class="white">
        <h1>₹ {prediction:.2f} Cr</h1>
        <p><b>Selected Model:</b> {best_model_name}</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Model Comparison")
    st.dataframe(results_df)

    fig = go.Figure(go.Bar(
        x=results_df["Model"],
        y=results_df["R2 Score"]
    ))
    st.plotly_chart(fig, use_container_width=True)
