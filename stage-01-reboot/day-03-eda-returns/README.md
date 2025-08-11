# Day 03 – S&P 500 Returns & Volatility EDA

**Author**: Brian  
**Date**: 2025-08-06  
**Input**: `sp500_clean.parquet` (Day 01)  
**Outputs**:
- `top_performers.csv` – best/worst 1-yr performers
- `rolling_vol.parquet` – return & vol columns added
- `risk_return.png` – scatter of vol vs. mean return
- `aapl_vol.png` – AAPL rolling vol

## Key Insights
- Top 1-yr performer: NVDA ≈ 189 % total return  
- Median volatility across tickers: 24 % annualized  
- Risk-return scatter shows classic positive relationship (R² ≈ 0.28)

## Run Notebook
```bash
jupyter notebook day03_returns_vol.ipynb