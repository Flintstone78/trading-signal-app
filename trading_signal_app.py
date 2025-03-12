import yfinance as yf
import pandas as pd
import numpy as np
import requests
import streamlit as st

# Define the stock/index to analyze
TICKER = "^GSPC"  # S&P 500, change to preferred index

# Fetch historical data
def get_stock_data(ticker, period="6mo", interval="1d"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    return df

# Identify Kullamägi-style breakout setup
def identify_breakout(df, min_gain=0.3, max_gain=1.0, consolidation_days=20):
    df["High_rolling_max"] = df["High"].rolling(window=consolidation_days).max()
    df["Low_rolling_min"] = df["Low"].rolling(window=consolidation_days).min()
    df["Prev_High"] = df["High"].shift(1)
    
    # Detect strong price moves
    df["Price_Change"] = df["Close"].pct_change(consolidation_days)
    df["Strong_Move"] = (df["Price_Change"] >= min_gain) & (df["Price_Change"] <= max_gain)
    
    # Identify breakouts
    df["Breakout"] = (df["Close"] > df["High_rolling_max"]) & df["Strong_Move"]
    
    return df[df["Breakout"] == True]

# Streamlit Dashboard
def run_dashboard():
    st.title("Trading Signal Dashboard")
    st.write("Real-time detection of breakout signals using Kullamägi's strategy")
    
    data = get_stock_data(TICKER)
    breakout_signals = identify_breakout(data)
    
    if not breakout_signals.empty:
        st.subheader("🚀 Breakout Signals Detected!")
        st.dataframe(breakout_signals)
    else:
        st.write("No breakouts detected at the moment.")
    
    st.line_chart(data["Close"])

# Run the scanner
def main():
    run_dashboard()

if __name__ == "__main__":
    main()