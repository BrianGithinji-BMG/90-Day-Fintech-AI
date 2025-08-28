# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# page config

st.set_page_config(
    page_title = "s&p 500 Mini-Dashboard",
    page_icon  = "📈",
    layout     = "centered"
)

# Load data with caching

@st.cache_data
def load_data():
    return pd.read_parquet("rolling_vol.parquet")

df = load_data()

# Sidebar
st.sidebar.title("controls")
tickers = sorted(df["Name"].unique())
ticker = st.sidebar.selectbox("Select Ticker", tickers)

lookback_days = st.sidebar.slider(
    "Lookback (days)", min_value =30, max_value = 252*5,
value = 252
)

ma_window = st.sidebar.slider("Moving Average (days)", 5,60,20)

# Filter
cutoff_date = df["date"].max() - timedelta(days = lookback_days)
sub = df[(df["Name"] == ticker) & (df["date"] >= cutoff_date)]

# KPIs
latest_close  = sub.iloc[-1]["close"]
first_close   = sub.iloc[0]["close"]
total_ret     = (latest_close / first_close - 1) * 100
latest_vol    = sub.iloc[-1]["Volatility_30d"]

# Display 
st.title(f"{ticker} - Quick Look")
col1, col2, col3 = st.columns(3)
col1.metric("Latest Close", f"${latest_close:.2f}")
col2.metric("Total Return (lookback)",f"{total_ret:.1f}%")
col3.metric("30d Volatility (ann.)", f"{latest_vol:.1%}")

# Price + MA
sub["MA"] = sub["close"].rolling(ma_window).mean()
fig = px.line(
    sub,
    x = "date",
    y = ["close", "MA"],
    labels = {"value": "Price ($)", "variable": "Series"},
    title = f"{ticker} Price & {ma_window}-day MA"
)
st.plotly_chart(fig,use_container_width = True)
# Rolling Vol
fig2 = px.line(
    sub,
    x = "date",
    y = "Volatility_30d",
    labels = {"Volatility_30d": "Annualized Vol (%)"},
    title = f"{ticker} 30-Day Rolling Volatility"
)
st.plotly_chart(fig2, use_container_width=True)

# Download button
csv = sub[["date", "close", "ret", "Volatility_30d"]].to_csv(index=False)
st.sidebar.download_button(
    label="Download CSV",
    data=csv,
    file_name=f"{ticker}_data.csv",
    mime="text/csv"
)
    
import streamlit as st
import joblib
import json
import pandas as pd
from features import build_features

# Load model & metrics once
@st.cache_resource
def load_model():
    return joblib.load("model.joblib")

@st.cache_resource
def load_metrics():
    with open("metrics.json") as f:
        return json.load(f)

MODEL = load_model()
METRICS = load_metrics()

# ---- Sidebar ----
st.sidebar.title("📈 Stock Predictor")
st.sidebar.markdown("Predict if a stock will go **up tomorrow** based on past features.")
st.sidebar.markdown("---")

# ---- Prediction ----
if st.sidebar.button("🔮 Predict Tomorrow for AAPL"):
    # Filter AAPL data
    aapl = df[df["Name"] == "AAPL"]

    if aapl.empty:
        st.error("⚠️ No AAPL data found in the dataframe.")
    else:
        # Use last 60 rows so rolling features can be calculated
        last_row = (
            aapl.tail(60)
            .pipe(build_features)
            .drop(columns=["close", "ret", "Volatility_30d", "target", "Name", "date"], errors="ignore")
            .tail(1)  # take the most recent usable row
        )

        if last_row.empty or last_row.isna().any().any():
            st.warning("⚠️ Not enough history to make a prediction.")
        else:
            prob_up = MODEL.predict_proba(last_row)[0, 1]

            st.subheader("📊 Prediction Result")
            st.metric("Predicted P(Up Tomorrow)", f"{prob_up:.1%}")
            st.caption(f"Model F1 ≈ {METRICS['f1']:.2f}")
