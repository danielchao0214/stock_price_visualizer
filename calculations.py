import pandas as pd

def add_indicators(df: pd.DataFrame, sma_window: int, ema_window: int) -> pd.DataFrame:
    """
    Calculates and adds SMA and EMA columns to the DataFrame.
    """
    # Work on a copy to avoid modifying the original DataFrame
    df_processed = df.copy()

    # Calculate SMA if window size is valid and 'Close' exists
    if sma_window > 0 and 'Close' in df_processed.columns:
        df_processed['SMA'] = df_processed['Close'].rolling(window=sma_window).mean()
    else:
        df_processed['SMA'] = pd.NA # Use pandas NA if SMA not calculated

    # Calculate EMA if window size is valid and 'Close' exists
    if ema_window > 0 and 'Close' in df_processed.columns:
        # adjust=True is standard for span-based EMA
        df_processed['EMA'] = df_processed['Close'].ewm(span=ema_window, adjust=True).mean()
    else:
        df_processed['EMA'] = pd.NA # Use pandas NA if EMA not calculated

    return df_processed