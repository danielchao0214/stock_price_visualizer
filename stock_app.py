# stock_app.py (Simplified)
import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Import project modules
from data_fetcher import load_data
from calculations import add_indicators
from plotting import create_stock_chart

# --- Page Setup ---
st.set_page_config(
    page_title="Stock Visualizer",
    layout="wide" # Use full page width
)

# --- App Title ---
st.title("Stock Price Visualizer")

# --- Sidebar Inputs ---
st.sidebar.header("Configuration")

# Ticker symbol input
ticker_symbol = st.sidebar.text_input(
    "Stock Ticker:", "AAPL", help="e.g., AAPL, MSFT, GOOGL"
).upper()

# Date range selection
today = date.today()
start_date = st.sidebar.date_input(
    "Start Date:",
    value=today - timedelta(days=365), # Default: 1 year ago
    max_value=today - timedelta(days=1),
    help="Select start date."
)
end_date = st.sidebar.date_input(
    "End Date:",
    value=today, # Default: today
    max_value=today,
    min_value=start_date + timedelta(days=1), # Must be after start date
    help="Select end date."
)

# --- Indicator Settings ---
st.sidebar.header("Indicators")

# SMA controls
show_sma = st.sidebar.checkbox("Show SMA", True)
sma_window = st.sidebar.number_input(
    "SMA Window (Days):", 1, 250, 50, 1, disabled=not show_sma # min, max, default, step
)

# EMA controls
show_ema = st.sidebar.checkbox("Show EMA", True)
ema_window = st.sidebar.number_input(
    "EMA Window (Days):", 1, 250, 20, 1, disabled=not show_ema # min, max, default, step
)

# --- Raw Data Toggle ---
st.sidebar.header("Data Display")
show_raw_data = st.sidebar.checkbox("Show Data Table")

# --- Main Area ---

# Input validation
if not ticker_symbol:
    st.warning("Please enter a stock ticker.")
    st.stop() # Halt execution

if start_date >= end_date:
    st.error("Error: End date must fall after start date.")
    st.stop() # Halt execution

# Fetch data (uses cached function)
stock_data = load_data(ticker_symbol, start_date, end_date)

# Process and display if data is available
if stock_data is not None and not stock_data.empty:

    st.header(f"Analysis: {ticker_symbol}")

    # Calculate indicators
    stock_data_processed = add_indicators(
        stock_data,
        sma_window if show_sma else 0, # Pass 0 if not shown
        ema_window if show_ema else 0  # Pass 0 if not shown
    )

    # Create Plotly chart
    fig = create_stock_chart(
        stock_data_processed, ticker_symbol, show_sma, show_ema, sma_window, ema_window
    )

    # Display chart
    st.plotly_chart(fig, use_container_width=True)

    # Display raw data table if checked
    if show_raw_data:
        st.subheader("Stock Data")
        # Show processed data including indicators, rounded
        st.dataframe(stock_data_processed.round(2))

elif stock_data is None:
    # Fetching failed (error messages handled in load_data)
    st.info("Could not retrieve data. Check ticker symbol and date range.")

# --- Footer ---
st.markdown("---")
st.markdown("Use the sidebar to configure the analysis.")