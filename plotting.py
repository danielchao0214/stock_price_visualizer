# plotting.py (Simplified)
import pandas as pd
import plotly.graph_objects as go

def create_stock_chart(
    df: pd.DataFrame,
    ticker: str,
    show_sma: bool,
    show_ema: bool,
    sma_window: int,
    ema_window: int
) -> go.Figure:
    """Creates a Plotly figure for stock price and selected indicators."""

    plot_data = df.copy()

    # Define columns to check for NaNs based on calculated indicators
    cols_to_check_na = ['Close']
    if show_sma and sma_window > 0 and 'SMA' in plot_data.columns:
         cols_to_check_na.append('SMA')
    if show_ema and ema_window > 0 and 'EMA' in plot_data.columns:
         cols_to_check_na.append('EMA')

    # Drop rows with NaNs in essential columns for cleaner plotting
    # Removes initial period where indicators aren't available
    plot_data.dropna(subset=cols_to_check_na, how='any', inplace=True)

    # Initialize figure
    fig = go.Figure()

    # --- Add Traces ---
    # Price trace (always shown)
    fig.add_trace(go.Scatter(
        x=plot_data.index, y=plot_data['Close'], mode='lines', name='Price',
        line=dict(color='blue', width=1.5)
    ))

    # SMA trace (conditional)
    if show_sma and sma_window > 0 and 'SMA' in plot_data.columns:
        fig.add_trace(go.Scatter(
            x=plot_data.index, y=plot_data['SMA'], mode='lines', name=f'{sma_window}-Day SMA',
            line=dict(color='red', width=1.5, dash='dot') # Dotted line for SMA
        ))

    # EMA trace (conditional)
    if show_ema and ema_window > 0 and 'EMA' in plot_data.columns:
         fig.add_trace(go.Scatter(
            x=plot_data.index, y=plot_data['EMA'], mode='lines', name=f'{ema_window}-Day EMA',
            line=dict(color='green', width=1.5, dash='dash') # Dashed line for EMA
        ))

    # --- Layout Configuration ---
    fig.update_layout(
        title=f'{ticker} Stock Price & Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        hovermode='x unified', # Unified hover info
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), # Legend position top
        xaxis_rangeslider_visible=False, # Hide rangeslider
        template="plotly_white" # Clean theme
        # margin=dict(l=50, r=50, t=50, b=50) # Optional: Adjust margins
    )

    return fig