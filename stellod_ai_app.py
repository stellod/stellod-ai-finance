
import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import gc
import talib
from datetime import datetime
import random
import time

st.title("🚀 Stellod AI - Intelligent Trading Assistant")

# Sidebar - User Inputs
st.sidebar.header("📈 User Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker", "RELIANCE.NS")
start_date = st.sidebar.date_input("Start Date", datetime(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Fetch data
def fetch_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, progress=False)
    return data

# Calculate Indicators
def calculate_indicators(data):
    data["RSI"] = talib.RSI(data["Close"], 14)
    data["MACD"], data["MACD_Signal"], _ = talib.MACD(data["Close"])
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
st.sidebar.info("© Stellod AI - Simplifying intelligent trading")
