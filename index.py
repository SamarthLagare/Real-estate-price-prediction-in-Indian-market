import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import time

# ======================================================
# PAGE CONFIG + STATE
# ======================================================
st.set_page_config("SAM VISION | Ultimate Mumbai Housing AI", layout="wide")

if "run" not in st.session_state:
    st.session_state.run = False

# ======================================================
# UI THEME
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
    padding:30px;
    border-left:10px solid #D4AF37;
    border-radius:10px;
    box-shadow:0 15px 45px rgba(212,175,55,.45);
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# MUMBAI MICRO MARKETS (FULL)
# ======================================================
mumbai = {
    "Malabar Hill":[18.95,72.79,115000],
    "Colaba":[18.91,72.81,82000],
    "Cuffe Parade":[18.91,72.82,88000],
    "Lower Parel":[18.99,72.83,65000],
    "Worli":[19.01,72.81,85000],
    "Dadar":[19.01,72.84,52000],
    "Bandra West":[19.06,72.82,92000],
    "Juhu":[19.10,72.82,78000],
    "Andheri West":[19.13,72.83,52000],
    "Goregaon West":[19.16,72.85,42000],
    "Malad West":[19.18,72.84,38000],
    "Borivali West":[19.23,72.85,35000],
    "Powai":[19.11,72.90,34000],
    "Chembur":[19.06,72.89,42000],
    "Mulund":[19.17,72.94,39000],
    "Thane West":[19.21,72.97,32000],
    "Mira Road":[19.28,72.87,22000],
    "Navi Mumbai":[19.07,72.99,26000]
}

# ======================================================
# SIDEBAR INPUTS
# ======================================================
with st.sidebar:
    st.markdown("## 🏙️ SAM VISION")
    location = st.selectbox("Location", list(mumbai.keys()))
    area = st.slider("Carpet Area (sqft)", 300, 4000, 1200)
    floor = st.slider("Floor", 0, 60, 20)
    age = st.slider("Building Age", 0, 50, 5)
    amenities = st.slider("Amenities Score", 1, 10, 7)
    density = st.slider("Flats per Floor", 2, 20, 6)
    ceiling = st.slider("Ceiling Height (ft)", 9.0, 15.0, 11.0)
    builder = st.selectbox("Builder Quality", ["Average","Good","Premium"])
    view = st.selectbox("View", ["Internal","City","Sea"])
    metro = st.toggle("Metro Nearby", True)
    smart = st.toggle("Smart Home", True)
    vastu = st.toggle("Vastu", True)

    if st.button("RUN AI VALUATION"):
        st.session_state.run = True

# ======================================================
# LANDING
# ======================================================
if not st.session_state.run:
    st.markdown("<h1 style='text-align:center;font-size:80px'>SAM VISION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center'>Mumbai Housing Intelligence Engine</p>", unsafe_allow_html=True)
    st.stop()

# ======================================================
# SYNTHETIC TRAINING DATA
# ======================================================
np.random.seed(42)
rows = 4000

df = pd.DataFrame({
    "area": np.random.randint(300,4000,rows),
    "floor": np.random.randint(0,60,rows),
    "age": np.random.randint(0,40,rows),
    "amenities": np.random.randint(1,10,rows),
    "density": np.random.randint(2,20,rows),
    "ceiling": np.random.uniform(9,15,rows),
    "builder": np.random.choice([1,1.05,1.12], rows),
    "view": np.random.choice([0.97,1.02,1.1], rows),
    "metro": np.random.choice([1,1.04], rows),
    "smart": np.random.choice([1,1.04], rows),
    "vastu": np.random.choice([1,1.03], rows),
})

df["price"] = (
    df.area*55000*
    (1+df.floor*0.004)*
    (1-df.age*0.006)*
    (1+df.amenities*0.01)*
    (1-df.density*0.008)*
    df.builder*df.view*df.metro*df.smart*df.vastu
)/1e7

X = df.drop("price",axis=1)
y = df["price"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

# ======================================================
# ML MODELS
# ======================================================
models = {
    "Linear": LinearRegression(),
    "Ridge": Ridge(),
    "Lasso": Lasso(),
    "RandomForest": RandomForestRegressor(n_estimators=120),
    "GradientBoosting": GradientBoostingRegressor()
}

results = []

for name,model in models.items():
    model.fit(X_train,y_train)
    pred = model.predict(X_test)
    results.append((name,r2_score(y_test,pred),np.sqrt(mean_squared_error(y_test,pred)),model))

best = sorted(results,key=lambda x:x[1],reverse=True)[0]
best_model = best[3]

# ======================================================
# USER PREDICTION
# ======================================================
loc = mumbai[location]
user = pd.DataFrame([{
    "area":area,"floor":floor,"age":age,"amenities":amenities,
    "density":density,"ceiling":ceiling,
    "builder":{"Average":1,"Good":1.05,"Premium":1.12}[builder],
    "view":{"Internal":0.97,"City":1.02,"Sea":1.1}[view],
    "metro":1.04 if metro else 1,
    "smart":1.04 if smart else 1,
    "vastu":1.03 if vastu else 1
}])

price = best_model.predict(user)[0]

# ======================================================
# MAP (CUSTOM MIX)
# ======================================================
m = folium.Map(location=[loc[0],loc[1]], zoom_start=16, tiles="CartoDB dark_matter")
folium.CircleMarker([loc[0],loc[1]], radius=40, color="#D4AF37", fill=True).add_to(m)
st_folium(m, height=450, use_container_width=True)

# ======================================================
# RESULT
# ======================================================
st.markdown(f"""
<div class="white-board">
<p>{location} • AI Predicted Value</p>
<h1>₹ {price:.2f} Cr</h1>
<p>Best Model: <b>{best[0]}</b> | R²: {best[1]:.3f}</p>
</div>
""", unsafe_allow_html=True)

# ======================================================
# MODEL COMPARISON
# ======================================================
st.subheader("Model Performance")
perf = pd.DataFrame(results, columns=["Model","R2","RMSE","_"]).drop("_",axis=1)
st.dataframe(perf)

# ======================================================
# FUTURE PROJECTION
# ======================================================
years = np.arange(2026,2037)
values = [price*(1.085**(y-2026)) for y in years]

fig = go.Figure(go.Scatter(x=years,y=values,fill="tozeroy",line_color="#D4AF37"))
fig.update_layout(paper_bgcolor="black",plot_bgcolor="black",font_color="#D4AF37")
st.plotly_chart(fig,use_container_width=True)
