import yfinance as yf
import pandas as pd
import plotly.express as px

# --- Configuration ---
ticker_symbol = (
    "GOOGL"  # Change this to any ticker you want (e.g., "MSFT", "AMZN", "TSLA")
)
start_date = "2023-01-01"
end_date = "2024-01-01"

window_size_sma_long = 50  # Window size for long SMA
window_size_ema_short = 20  # Window size for short EMA

# --- Step 2: Getting Stock Data ---
print(f"Downloading data for {ticker_symbol} from {start_date} to {end_date}...")
try:
    stock_data = yf.download(
        ticker_symbol, start=start_date, end=end_date, auto_adjust=False, multi_level_index=False
    )
    if stock_data.empty:
        print(f"No data found for {ticker_symbol} in the specified date range.")
        exit()  # Exit if no data
    print("Data downloaded successfully.")
    # print(stock_data.head()) # Optional: inspect the first few rows
except Exception as e:
    print(f"Error downloading data: {e}")
    exit()  # Exit if download fails

# --- Step 3: Calculating Simple Technical Indicators ---
print("Calculating indicators...")

# Simple Moving Average (SMA)
# We use 'Adj Close' as it's adjusted for splits/dividends
stock_data["SMA_Long"] = (
    stock_data["Adj Close"].rolling(window=window_size_sma_long).mean()
)
print(f"Calculated {window_size_sma_long}-Day SMA.")

# Exponential Moving Average (EMA)
# EMA reacts faster to recent price changes
stock_data["EMA_Short"] = (
    stock_data["Adj Close"].ewm(span=window_size_ema_short, adjust=False).mean()
)
print(f"Calculated {window_size_ema_short}-Day EMA.")

# Drop rows where indicators couldn't be calculated (due to the rolling window)
# This makes the plot look cleaner at the beginning
stock_data.dropna(inplace=True)
print("Removed initial rows with NaN indicator values.")
# print(stock_data.head()) # Optional: inspect after adding indicators and dropping NaNs

# --- Step 4: Visualizing the Data ---
print("Generating plot...")

# Create a figure with Plotly
fig = px.line(
    stock_data,
    x=stock_data.index,
    y='Adj Close',
    title=f'{ticker_symbol} Price and Indicators ({start_date} to {end_date})',
    labels={'value': 'Price', 'variable': 'Metric'},  # Better axis labels
    template='plotly_white'  # Clean theme
)

# Add SMA and EMA traces
fig.add_scatter(
    x=stock_data.index,
    y=stock_data['SMA_Long'],
    mode='lines',
    name=f'SMA {window_size_sma_long}',
    line=dict(color='orange', dash='dot')
)

fig.add_scatter(
    x=stock_data.index,
    y=stock_data['EMA_Short'],
    mode='lines',
    name=f'EMA {window_size_ema_short}',
    line=dict(color='green', dash='dash')
)

# Add range slider and style layout
fig.update_layout(
    xaxis=dict(
        title='Date',
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    ),
    yaxis=dict(title='Price (USD)'),
    hovermode='x unified',
    height=600
)

# Show the plot
fig.show()
