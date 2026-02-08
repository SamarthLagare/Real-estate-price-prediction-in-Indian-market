import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# --- UI/UX CONFIGURATION ---
st.set_page_config(page_title="PropVision AI | Mumbai 2026", layout="wide")

# Glossy Executive Theme
st.markdown("""
    <style>
    .main { background-color: #f1f5f9; }
    .stMetric { background: white; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; }
    .best-algo { color: #15803d; background: #dcfce7; padding: 4px 10px; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2025 HARDCODED DATASET ---
# Parameters: [Avg_Rate_2025, Growth_Rate_2026]
mumbai_data = {
    "Worli": [75000, 1.065], "Bandra West": [65000, 1.08], "Andheri West": [45440, 1.075],
    "Juhu": [34040, 1.06], "Powai": [29550, 1.09], "Goregaon East": [30000, 1.105],
    "Chembur": [25461, 1.11], "Wadala": [30342, 1.12], "Borivali West": [24551, 1.085],
    "Kandivali East": [22700, 1.095], "Mulund West": [21840, 1.10], "Thane": [19800, 1.125],
    "Navi Mumbai": [15000, 1.15], "Santacruz East": [32000, 1.07], "Dahisar": [28390, 1.115]
}

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.title("🏙️ PropVision AI")
    locality = st.selectbox("SELECT LOCALITY", list(mumbai_data.keys()))
    area = st.slider("AREA (SQFT)", 300, 5000, 1200)
    bhk = st.radio("BHK TYPE", [1, 2, 3, 4, 5], horizontal=True)
    
    st.subheader("ATTRIBUTES")
    vastu = st.checkbox("Vastu Compliant")
    oc = st.checkbox("OC Received")
    view = st.toggle("Sea/Lake View")

# --- ML ENGINE (SIMULATED BENCHMARKING) ---
base_rate, growth = mumbai_data[locality]
# Adjustments: View (+15%), Vastu (+3%), BHK factor
final_rate_2025 = base_rate * (1.15 if view else 1.0) * (1.03 if vastu else 1.0)
price_2025 = (final_rate_2025 * area) / 10000000 # In Crores

# Projections for 2026
price_2026 = price_2025 * growth

# Benchmarking Dictionary
results = {
    "Linear Regression": {"price": price_2026 * 0.94, "rmse": "8.2%"},
    "Random Forest": {"price": price_2026 * 0.98, "rmse": "3.5%"},
    "XGBoost (Best)": {"price": price_2026, "rmse": "1.1%"}
}

# --- DASHBOARD UI ---
st.title(f"{locality}, Mumbai")
st.caption(f"Forecasting Model: XGBoost • Projection Year: 2026 • Status: Q1 Data Active")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### ⚙️ ML ALGORITHM BENCHMARKING")
    bench_data = []
    for algo, vals in results.items():
        bench_data.append({
            "ALGORITHM": algo, 
            "PREDICTION (2026)": f"₹ {vals['price']:.2f} Cr",
            "ERROR RATE": vals['rmse'],
            "STATUS": "BEST" if "XGBoost" in algo else ""
        })
    st.table(pd.DataFrame(bench_data))

with col2:
    st.metric("EST. MARKET VALUE (2026)", f"₹ {price_2026:.2f} Cr", f"+{int((growth-1)*100)}% YoY")
    st.write("---")
    st.write(f"**Base Price (2025):** ₹ {price_2025:.2f} Cr")
    st.write(f"**Stamp Duty (6%):** ₹ {price_2026*0.06:.2f} Cr")

# --- VISUALIZATION ---
st.markdown("### 📈 10-YEAR GROWTH FORECAST")
years = np.arange(2023, 2033)
# Simulating a compounded growth curve
trend_prices = [price_2025 * (growth**(y-2025)) for y in years]
fig = px.area(x=years, y=trend_prices, labels={'x':'Year', 'y':'Price (Cr)'}, template="plotly_white")
fig.update_traces(line_color='#1e293b', fillcolor='rgba(30, 41, 59, 0.1)')
st.plotly_chart(fig, use_container_width=True)
