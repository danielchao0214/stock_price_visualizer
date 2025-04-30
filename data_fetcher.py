# data_fetcher.py (Simplified)
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

@st.cache_data # Cache the data fetch result
def load_data(ticker: str, start: date, end: date) -> pd.DataFrame | None:
    """Fetches historical stock data from Yahoo Finance."""
    try:
        # Download adjusted stock data
        data = yf.download(
            ticker,
            start=start,
            end=end,
            auto_adjust=True,   # Gets adjusted 'Close'
            progress=False,     # Hide yfinance progress bar
            multi_level_index=False # Ensure single-level columns
        )

        # Check if data was returned
        if data.empty:
            st.warning(f"No data found for {ticker} ({start} to {end}).")
            return None

        # Ensure index is datetime
        if not isinstance(data.index, pd.DatetimeIndex):
             data.index = pd.to_datetime(data.index)

        # Ensure 'Close' column exists
        if 'Close' not in data.columns:
            st.error(f"'Close' column missing for {ticker}.")
            return None

        return data

    except Exception as e:
        # Catch potential download errors
        st.error(f"Error fetching data for {ticker}: {e}")
        return None