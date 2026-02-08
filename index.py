import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import time

# ======================================================
# PAGE CONFIG + STATE
# ======================================================
st.set_page_config("SAM VISION | Mumbai House AI", layout="wide")

if "run" not in st.session_state:
    st.session_state.run = False

# ======================================================
# THEME
# ======================================================
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

# ======================================================
# MUMBAI LOCATIONS
# ======================================================
mumbai = {
    "Malabar Hill":[18.95,72.79,115000],
    "Colaba":[18.91,72.81,82000],
    "Cuffe Parade":[18.91,72.82,88000],
    "Lower Parel":[18.99,72.83,65000],
    "Worli":[19.01,72.81,85000],
    "Bandra West":[19.06,72.82,92000],
    "Juhu":[19.10,72.82,78000],
    "Andheri West":[19.13,72.83,52000],
    "Goregaon West":[19.16,72.85,42000],
    "Borivali West":[19.23,72.85,35000],
    "Powai":[19.11,72.90,34000],
    "Chembur":[19.06,72.89,42000],
    "Mulund":[19.17,72.94,39000],
    "Thane West":[19.21,72.97,32000]
}

# ======================================================
# SIDEBAR INPUTS
# ======================================================
with st.sidebar:
    st.markdown("## 🏙️ SAM VISION")
    location = st.selectbox("Location", list(mumbai.keys()))
    area = st.slider("Carpet Area (sqft)", 300, 4000, 1200)
    floor = st.slider("Floor Level", 0, 60, 20)
    age = st.slider("Building Age (yrs)", 0, 40, 5)
    amenities = st.slider("Amenities Score", 1, 10, 7)
    view = st.selectbox("View", ["Internal","City","Sea"])
    metro = st.toggle("Metro Nearby", True)
    builder = st.selectbox("Builder Grade", ["Average","Good","Premium"])

    if st.button("RUN AI VALUATION"):
        st.session_state.run = True

# ======================================================
# LANDING
# ======================================================
if not st.session_state.run:
    st.markdown("<h1 style='text-align:center;font-size:80px'>SAM VISION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Mumbai Real Estate Intelligence</p>", unsafe_allow_html=True)
    st.stop()

# ======================================================
# SYNTHETIC TRAINING DATA
# ======================================================
np.random.seed(42)
rows = 3500

df = pd.DataFrame({
    "area": np.random.randint(300,4000,rows),
    "floor": np.random.randint(0,60,rows),
    "age": np.random.randint(0,40,rows),
    "amenities": np.random.randint(1,10,rows),
    "view": np.random.choice([0.97,1.02,1.1], rows),
    "metro": np.random.choice([1,1.04], rows),
    "builder": np.random.choice([1,1.05,1.12], rows)
})

df["price_cr"] = (
    df.area*55000*
    (1+df.floor*0.004)*
    (1-df.age*0.006)*
    (1+df.amenities*0.01)*
    df.view*df.metro*df.builder
)/1e7   # <-- CRORES

X = df.drop("price_cr",axis=1)
y = df["price_cr"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

# ======================================================
# ML MODELS
# ======================================================
models = {
    "Linear": LinearRegression(),
    "Ridge": Ridge(),
    "Random Forest": RandomForestRegressor(n_estimators=120),
    "Gradient Boosting": GradientBoostingRegressor()
}

scores = []
for name,model in models.items():
    model.fit(X_train,y_train)
    pred = model.predict(X_test)
    scores.append((name,r2_score(y_test,pred),model))

best = sorted(scores,key=lambda x:x[1],reverse=True)[0]
best_model = best[2]

# ======================================================
# USER PREDICTION (CRORES)
# ======================================================
user = pd.DataFrame([{
    "area":area,
    "floor":floor,
    "age":age,
    "amenities":amenities,
    "view":{"Internal":0.97,"City":1.02,"Sea":1.1}[view],
    "metro":1.04 if metro else 1,
    "builder":{"Average":1,"Good":1.05,"Premium":1.12}[builder]
}])

price_cr = best_model.predict(user)[0]

low = price_cr * 0.95
high = price_cr * 1.05

# ======================================================
# SATELLITE MAP (PREMIUM)
# ======================================================
lat,lon,_ = mumbai[location]
m = folium.Map(
    location=[lat,lon],
    zoom_start=16,
    tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    attr="Google Satellite"
)

folium.CircleMarker(
    [lat,lon],
    radius=price_cr*3,
    color="#D4AF37",
    fill=True,
    fill_opacity=0.45,
    popup=f"₹ {price_cr:.2f} Cr"
).add_to(m)

st_folium(m, height=460, use_container_width=True)

# ======================================================
# RESULT BOARD
# ======================================================
st.markdown(f"""
<div class="white-board">
<p>{location} • AI Predicted Value</p>
<h1>₹ {price_cr:.2f} Cr</h1>
<p>Confidence Range: ₹ {low:.2f} – ₹ {high:.2f} Cr</p>
<p>Best Model: <b>{best[0]}</b></p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# FUTURE PROJECTION
# ======================================================
years = np.arange(2026,2037)
values = [price_cr*(1.085**(y-2026)) for y in years]

fig = go.Figure(go.Scatter(x=years,y=values,fill="tozeroy",line_color="#D4AF37"))
fig.update_layout(paper_bgcolor="black",plot_bgcolor="black",font_color="#D4AF37")
st.plotly_chart(fig,use_container_width=True)
