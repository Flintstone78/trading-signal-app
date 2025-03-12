import yfinance as yf
import pandas as pd
import numpy as np
import requests
import streamlit as st

# Define the indexes to analyze
TICKERS = ["^GSPC", "^IXIC", "^GDAXI"]  # S&P 500, Nasdaq, DAX

# Fetch historical data
def get_stock_data(ticker, period="6mo", interval="1d"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)
    df["Ticker"] = ticker  # Add ticker column for identification
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

# Send email alert
def send_email_alert(message):
    import smtplib
    from email.mime.text import MIMEText
    
    sender_email = artwaves.email@gmail.com
    receiver_email = fredrik.vindelalv@gmail.com
    password = Mauritius123?
    
    msg = MIMEText(message)
    msg["Subject"] = "Trading Signal Alert"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Streamlit Dashboard
def run_dashboard():
    st.title("Trading Signal Dashboard")
    st.write("Real-time detection of breakout signals using Kullamägi's strategy")
    
    breakout_signals = []
    
    for ticker in TICKERS:
        data = get_stock_data(ticker)
        signals = identify_breakout(data)
        if not signals.empty:
            breakout_signals.append(signals)
    
    if breakout_signals:
        breakout_df = pd.concat(breakout_signals)
        st.subheader("🚀 Breakout Signals Detected!")
        st.dataframe(breakout_df)
        
        message = f"🚀 Breakout Alert! Check {breakout_df['Ticker'].tolist()} for new highs!"
        send_email_alert(message)
    else:
        st.write("No breakouts detected at the moment.")
    
    for ticker in TICKERS:
        st.subheader(f"Price Chart for {ticker}")
        data = get_stock_data(ticker)
        st.line_chart(data["Close"])

# Run the scanner
def main():
    run_dashboard()

if __name__ == "__main__":
    main()