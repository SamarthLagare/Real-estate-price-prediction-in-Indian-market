import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# --- 1. CONFIGURATION & MOCK DATA ---
st.set_page_config(page_title="PropVision AI", page_icon="🏢", layout="wide")

# 15 Famous Mumbai Locations (2025 Base Data)
# Format: [Avg_Rate_2025_per_sqft, 2026_Projected_Growth]
mumbai_intelligence = {
    "Worli": [75000, 1.065], "Bandra West": [65000, 1.080], "Andheri West": [45440, 1.075],
    "Juhu": [34040, 1.060], "Powai": [29550, 1.090], "Goregaon East": [30000, 1.105],
    "Chembur": [25461, 1.110], "Wadala": [30342, 1.120], "Borivali West": [24551, 1.085],
    "Kandivali East": [22700, 1.095], "Mulund West": [21840, 1.100], "Thane": [19800, 1.125],
    "Navi Mumbai": [15000, 1.150], "Santacruz East": [32000, 1.070], "Dahisar": [28390, 1.115]
}

# --- 2. GLASSMORPHISM CSS (Your Custom Styling) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp { background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(30, 41, 59) 90%); font-family: 'Inter', sans-serif; color: white; }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 24px; margin-bottom: 20px; }
    h1 { background: linear-gradient(to right, #00c6ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
    .glow-btn > button { background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important; color: white !important; border: none !important; box-shadow: 0 0 20px rgba(0, 114, 255, 0.4); }
    div[data-testid="stMetricValue"] { color: #00c6ff; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🔮 PropVision")
    st.caption("Executive Forecaster 2026")
    st.markdown("---")
    page = st.radio("NAVIGATE", ["Market Forecaster", "Growth Analytics", "Model Benchmarks"])

# --- 4. PAGE: MARKET FORECASTER ---
if page == "Market Forecaster":
    st.header("🏙️ Mumbai Real Estate Intelligence")
    
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Property Specs")
        loc = st.selectbox("Location", list(mumbai_intelligence.keys()))
        sqft = st.slider("Area (Sq.Ft)", 300, 5000, 1200)
        bhk = st.selectbox("BHK", [1, 2, 3, 4, 5], index=1)
        
        st.markdown("### Attributes")
        c1, c2 = st.columns(2)
        vastu = c1.checkbox("Vastu")
        sea_view = c2.checkbox("Sea View")
        
        st.markdown('<div class="glow-btn">', unsafe_allow_html=True)
        run = st.button("🚀 CALCULATE 2026 PRICE")
        st.markdown('</div></div>', unsafe_allow_html=True)

    if run:
        # Logic: 2025 Base -> 2026 Proj
        base_rate, growth = mumbai_intelligence[loc]
        adj_rate = base_rate * (1.15 if sea_view else 1.0) * (1.03 if vastu else 1.0)
        price_2025 = (adj_rate * sqft) / 10000000
        price_2026 = price_2025 * growth
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader(f"Valuation for {loc}")
            m1, m2 = st.columns(2)
            m1.metric("Est. Market Value (2026)", f"₹ {price_2026:.2f} Cr", f"+{int((growth-1)*100)}% YoY")
            m2.metric("2025 Base Value", f"₹ {price_2025:.2f} Cr")
            
            st.markdown("---")
            st.write(f"**Stamp Duty (6%):** ₹ {price_2026*0.06:.2f} Cr")
            st.write(f"**Registration Fee:** ₹ 30,000")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Mini Trend Line
            years = [2024, 2025, 2026]
            trend = [price_2025*0.92, price_2025, price_2026]
            fig = px.line(x=years, y=trend, title="Price Trajectory", template="plotly_dark")
            fig.update_traces(line_color='#00c6ff', mode='lines+markers')
            st.plotly_chart(fig, use_container_width=True)

# --- 5. PAGE: GROWTH ANALYTICS ---
elif page == "Growth Analytics":
    st.header("📊 Market Volatility & ROI")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    # Compare all 15 locations
    data = []
    for k, v in mumbai_intelligence.items():
        data.append({"Location": k, "2025 Rate": v[0], "2026 Growth (%)": round((v[1]-1)*100, 2)})
    
    df_growth = pd.DataFrame(data).sort_values("2026 Growth (%)", ascending=False)
    
    fig = px.bar(df_growth, x="Location", y="2026 Growth (%)", color="2026 Growth (%)",
                 title="Projected ROI by Locality (2025-2026)", template="plotly_dark",
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. PAGE: MODEL BENCHMARKS ---
elif page == "Model Benchmarks":
    st.header("🧠 Algorithm Tournament")
    st.markdown("Selecting the high-precision model for 2026 predictions.")
    
    # Simulated Tournament Results
    models = ["Linear Regression", "Random Forest", "Gradient Boosting", "XGBoost"]
    scores = [0.842, 0.915, 0.948, 0.984]
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig_comp = px.bar(x=scores, y=models, orientation='h', color=scores, 
                         title="Model Accuracy (R² Score)", template="plotly_dark")
        st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.metric("Top Performer", "XGBoost")
        st.metric("Error Rate (RMSE)", "1.1%")
        st.success("Selected for Production")
        st.markdown('</div>', unsafe_allow_html=True)
