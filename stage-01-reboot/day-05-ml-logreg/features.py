import pandas as pd
import ta

def build_features(df_price):
    df = df_price.copy()
    # basic lags
    for lag in range(1, 6):
        df[f"ret_lag{lag}"] = df["ret"].shift(lag)
    # rolling volatility
    df["vol_ma_5"] = df["Volatility_30d"].rolling(5).mean()
    # technicals
    df["rsi_14"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    sma_20 = ta.trend.SMAIndicator(df["close"], window=20).sma_indicator()
    df["sma_ratio"] = df["close"] / sma_20
    bb = ta.volatility.BollingerBands(df["close"], window=20, window_dev=2)
    df["bb_position"] = (df["close"] - bb.bollinger_mavg()) / (bb.bollinger_hband() - bb.bollinger_lband())
    
    # target: next-day direction
    df["target"] = (df["ret"].shift(-1) > 0).astype(int)
    return df.dropna()

