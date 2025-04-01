
import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import gc
from datetime import datetime

st.title("🚀 Stellod AI - Intelligent Trading Assistant (No TA-Lib)")

# Sidebar - User Inputs
st.sidebar.header("📈 User Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker", "RELIANCE.NS")
start_date = st.sidebar.date_input("Start Date", datetime(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Fetch data
def fetch_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, progress=False)
    return data

# RSI (manual)
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# MACD (manual)
def compute_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

# Calculate Indicators
def calculate_indicators(data):
    data["RSI"] = compute_rsi(data["Close"])
    data["MACD"], data["MACD_Signal"] = compute_macd(data["Close"])
    return data

# Generate Signals
def generate_signals(data):
    data["Buy"] = (data["RSI"] < 30) & (data["MACD"] > data["MACD_Signal"])
    data["Sell"] = (data["RSI"] > 70) & (data["MACD"] < data["MACD_Signal"])
    return data

# Fetch and analyze data
if st.sidebar.button("Analyze"):
    with st.spinner("Analyzing stock..."):
        data = fetch_stock_data(ticker, start_date, end_date)
        data = calculate_indicators(data)
        data = generate_signals(data)
        st.success("Data loaded successfully!")

        # Display data
        st.subheader(f"Stock Data: {ticker}")
        st.dataframe(data.tail())

        # Plot signals
        fig, ax = plt.subplots()
        ax.plot(data.index, data["Close"], label="Close Price", color="blue")
        ax.scatter(data.index[data["Buy"]], data["Close"][data["Buy"]], color="green", marker="^", label="Buy")
        ax.scatter(data.index[data["Sell"]], data["Close"][data["Sell"]], color="red", marker="v", label="Sell")
        ax.set_title(f"Trading Signals - {ticker}")
        ax.legend()
        st.pyplot(fig)

# Optimize Memory
st.sidebar.button("Optimize Memory", on_click=gc.collect)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("© Stellod AI - No TA-Lib version")
