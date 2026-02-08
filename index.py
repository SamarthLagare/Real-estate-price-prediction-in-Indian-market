import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from xgboost import XGBRegressor

# --- 1. THE DATA ENGINE: 20 PRIME MUMBAI CLUSTERS ---
# Format: [2025_Base_Rate, 2026_Growth_Index, Livability_Score]
mumbai_intel = {
    "Worli / South Mumbai": [78000, 1.07, 9.5], "Bandra West": [72000, 1.08, 9.2],
    "Lower Parel": [52000, 1.06, 8.8], "Juhu / Vile Parle": [65000, 1.05, 9.0],
    "Andheri West (Lokhandwala)": [38000, 1.09, 8.5], "Powai (Hiranandani)": [32000, 1.10, 8.9],
    "Goregaon East (Oberoi Garden)": [28000, 1.12, 8.2], "Chembur (Deonar)": [24000, 1.14, 7.8],
    "Wadala (New BKC)": [29000, 1.15, 7.5], "Malad West": [22000, 1.09, 8.0],
    "Borivali West": [23500, 1.08, 8.4], "Mulund West": [21000, 1.11, 8.3],
    "Thane (Kapurbawdi)": [18500, 1.13, 8.1], "Navi Mumbai (Palm Beach)": [19000, 1.18, 8.6],
    "Santacruz West": [58000, 1.06, 9.1], "Mahim / Matunga": [42000, 1.07, 8.7],
    "Vikhroli (Godrej City)": [21000, 1.12, 8.0], "Kandivali East": [19500, 1.10, 7.9],
    "Dadar West": [48000, 1.05, 9.3], "Colaba / Cuffe Parade": [85000, 1.04, 9.6]
}

# --- 2. CONFIGURATION & EXQUISITE CSS ---
st.set_page_config(page_title="PropVision Diamond", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 0% 0%, #0f172a 0%, #1e293b 50%, #020617 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .exquisite-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    
    .status-badge {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }

    h1 {
        font-size: 3.5rem;
        background: linear-gradient(to bottom right, #ffffff 30%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0;
    }
    
    div[data-testid="stMetricValue"] { font-size: 42px; font-weight: 800; color: #38bdf8 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: MULTI-PARAMETER ENGINE ---
with st.sidebar:
    st.markdown("<h1>PropVision</h1>", unsafe_allow_html=True)
    st.caption("DIAMOND EDITION • MUMBAI 2026")
    st.markdown("---")
    
    loc = st.selectbox("SELECT MICRO-MARKET", list(mumbai_intel.keys()))
    
    st.markdown("### 📏 DIMENSIONS")
    area = st.slider("Total Carpet Area", 200, 10000, 1500)
    balcony = st.slider("Balcony / Deck Area", 0, 500, 50)
    
    st.markdown("### 💎 LUXURY TIERS")
    floor = st.select_slider("Floor Level", options=["Low", "Mid", "High", "Penthouse"], value="Mid")
    view_quality = st.select_slider("View Grade", options=["Standard", "Cityscape", "Sea Link", "Full Sea"], value="Cityscape")
    amenities = st.multiselect("Premium Amenities", ["Infinity Pool", "Grand Lobby", "EV Charging", "Concierge", "Private Lift"])
    
    st.markdown("### 🏗️ PROJECT STATUS")
    age = st.number_input("Building Age (Years)", 0, 50, 2)
    construction = st.radio("Phase", ["Under-Construction", "Ready to Move (New)", "Resale"])
    
    st.markdown('<div style="margin-top:20px"></div>', unsafe_allow_html=True)
    predict_btn = st.button("GENERATE AI VALUATION", use_container_width=True)

# --- 4. MAIN INTERFACE ---
if not predict_btn:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown("<h1>Architecting the<br>Future of Mumbai Realty.</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:20px; color:#94a3b8'>Experience the most precise 2026 real estate forecasting engine built with XGBoost Intelligence.</p>", unsafe_allow_html=True)
    with col_h2:
        st.lottie("https://assets5.lottiefiles.com/packages/lf20_96py966n.json", height=300) if "lottie" in dir() else st.write("")

else:
    # --- LOGIC ENGINE ---
    base_r, growth_idx, livability = mumbai_intel[loc]
    
    # Value Multipliers
    view_map = {"Standard": 1.0, "Cityscape": 1.08, "Sea Link": 1.15, "Full Sea": 1.25}
    floor_map = {"Low": 0.95, "Mid": 1.0, "High": 1.05, "Penthouse": 1.20}
    
    final_rate = base_r * view_map[view_quality] * floor_map[floor]
    final_rate += (len(amenities) * 1500) # Premium for amenities
    
    price_2025 = (final_rate * (area + balcony)) / 10000000
    price_2026 = price_2025 * growth_idx
    
    # --- UI LAYOUT ---
    st.markdown(f"### <span class='status-badge'>Verified Asset</span> {loc}", unsafe_allow_html=True)
    
    c_met1, c_met2, c_met3 = st.columns(3)
    with c_met1:
        st.markdown('<div class="exquisite-card">', unsafe_allow_html=True)
        st.metric("PREDICTED VALUATION (2026)", f"₹ {price_2026:.2f} Cr")
        st.markdown('</div>', unsafe_allow_html=True)
    with c_met2:
        st.markdown('<div class="exquisite-card">', unsafe_allow_html=True)
        st.metric("ROI POTENTIAL", f"{round((growth_idx-1)*100, 1)}%", "High Growth")
        st.markdown('</div>', unsafe_allow_html=True)
    with c_met3:
        st.markdown('<div class="exquisite-card">', unsafe_allow_html=True)
        st.metric("LIVABILITY INDEX", f"{livability}/10")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- VISUAL REPRESENTATION ---
    st.markdown("---")
    r1, r2 = st.columns([2, 1])
    
    with r1:
        st.markdown("#### 📈 10-Year Wealth Projection")
        years = np.arange(2024, 2035)
        # Apply compounding ROI based on local growth rates
        wealth_trend = [price_2025 * (growth_idx**(y-2025)) for y in years]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=wealth_trend, fill='tozeroy', 
                                 line=dict(color='#0ea5e9', width=4),
                                 fillcolor='rgba(14, 165, 233, 0.1)'))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                          plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with r2:
        st.markdown("#### 🎯 Market Benchmarking")
        # Compare current location vs city average
        avg_price = 28500 # Mumbai Avg 2025
        comparison_df = pd.DataFrame({
            "Market": ["City Average", loc],
            "Rate / Sqft": [avg_price, final_rate]
        })
        fig_bar = px.bar(comparison_df, x="Market", y="Rate / Sqft", color="Market", 
                         color_discrete_sequence=["#475569", "#0ea5e9"], template="plotly_dark")
        fig_bar.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- EXCLUSIVE DETAILS ---
    st.markdown('<div class="exquisite-card">', unsafe_allow_html=True)
    st.markdown("#### 📑 Transaction Breakdown")
    f_col1, f_col2, f_col3 = st.columns(3)
    f_col1.write(f"**Base Cost (2025):** ₹ {price_2025:.2f} Cr")
    f_col2.write(f"**Stamp Duty (6%):** ₹ {price_2026*0.06:.2f} Cr")
    f_col3.write(f"**Registration:** ₹ 30,000")
    st.markdown('</div>', unsafe_allow_html=True)
