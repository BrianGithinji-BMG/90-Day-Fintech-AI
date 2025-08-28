# Day 05 – Logistic Regression for Next-Day Direction

## Model
- Algorithm: Logistic Regression (balanced class weights)  
- Features: 5 lag returns, volatility MA, RSI, SMA ratio, Bollinger %B  
- Target: 1 if next-day return > 0 else 0  

## Performance (5-fold time-series CV)
- Precision: 0.54  
- Recall: 0.52  
- F1: 0.53  
- Brier score: 0.25  

## Usage
```bash
streamlit run app_v2.py