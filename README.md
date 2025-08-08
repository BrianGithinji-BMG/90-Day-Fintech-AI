# 90-Day-Fintech-AI
A 90 day intensive study to master AI-driven tools for finance

---

# Day 01 -S&P 500 Data Cleaning

**Author** : Brian Githinji
**Date**: 2025-08-08
**Stage**: 1 - Reboot

## Objective
Refresh core Pandas skills by ingesting and cleaning 5 years of daily OHLCV data for all S&P 500 tickers.

## Dataset
 - Source : Kaggle datasets mirror (CSV, 28 MB raw)
 - Rows : 619,040 | Columns: 7(data,open,high,low,close,volume,Name)

## Steps Performed
1. **Load** – `pd.read_csv(url)` directly from GitHub raw link.
2. **Parse dates** – `pd.to_datetime(df['date'])`.
3. **Check missing** – `df.isnull().sum()` → zero missing.
4. **Persist clean** – Saved as Parquet (`sp500_clean.parquet`) for faster I/O.



## How to Run
```bash
cd stage-01-reboot/day-01-pandas-cleaning
jupyter notebook Day1.ipynb


---
