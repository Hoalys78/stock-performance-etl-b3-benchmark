# Stock Performance Dashboard - ETL Pipeline (B3 + Benchmarks)

> Production-ready ETL pipeline extracting Brazilian stocks and benchmarks from Yahoo Finance, transforming into a Star Schema ready for Power BI / Tableau.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![yfinance](https://img.shields.io/badge/yfinance-1.x-green.svg)](https://pypi.org/project/yfinance/)

### Dashboard Preview
![Stock Performance](images/dashboard_preview.png)

## 1. Overview
This project implements a robust ETL pipeline to analyze a stock portfolio:
- **Brazilian stocks (B3):** PETR4, VALE3, ITUB4, WEGE3, MGLU3
- **Benchmarks:** IBOVESPA (^BVSP), S&P 500 (^GSPC), USD/BRL, IFIX

The pipeline handles yfinance 1.x breaking changes (MultiIndex), implements fallback extraction, data quality checks, and exports to both CSV and SQLite in Star Schema format.

## 2. Business Problem
How does a diversified Brazilian portfolio perform against market benchmarks? Investors need:
- Clean historical prices adjusted for splits/dividends
- Continuous calendar for time intelligence
- Sector-enriched asset dimension
- Ready-to-use model for BI tools

## 3. Architecture - Star Schema
```
fact_prices (price_id, date, ticker, open_price, high_price, low_price, close_price, volume)
     |
     |--- dim_asset (asset_id, ticker, company, sector, industry, asset_type)
     |
     |--- dim_calendar (date_id, date, year, month, year_month, is_weekday, etc.)
```

## 4. Tech Stack
- **Python:** Pandas, yfinance
- **Storage:** CSV (Power BI) + SQLite with indexes
- **BI Ready:** Optimized for Power BI / Tableau
- **Practices:** Logging, type hints, error handling, modular design

## 5. Project Structure
```
├── data/
│   ├── raw/              # Raw quotes (gitignored, kept for audit)
│   └── processed/        # Clean CSVs + SQLite DB
├── notebooks/
│   └── 01_etl_pipeline.ipynb  # Portfolio-friendly walkthrough
├── src/
│   ├── config.py         # Tickers, metadata, paths
│   ├── logger.py         # Centralized logging
│   ├── extract.py        # Yahoo Finance extraction with fallback
│   ├── transform.py      # Cleaning and validation
│   ├── dimensions.py     # dim_asset + dim_calendar
│   ├── load.py           # Export to CSV/SQLite
│   ├── quality.py        # Data quality report
│   └── main.py           # Entry point
├── sql/
│   └── analysis_queries.sql  # Example analytical queries
└── images/               # Charts for README
```

## 6. Key Features & Engineering Decisions

**1. yfinance 1.x compatibility:** Handles `multi_level_index=True` default. Stacks MultiIndex `(Price, Ticker)` into flat table. Fallback to `Ticker.history()` for robustness.

**2. Data Quality:** 
- Removes rows without close_price (critical)
- Fills open/high/low nulls with close (common for indices like ^BVSP)
- Removes price <= 0 and duplicates (date + ticker)
- Full quality report with min/max/avg per ticker

**3. Calendar Dimension:** Continuous calendar (all days, not just trading days) for Power BI DAX functions like `TOTALYTD`, `SAMEPERIODLASTYEAR`.

## 7. How to Run

```bash
# Clone
git clone https://github.com/your-username/stock-performance-etl.git
cd stock-performance-etl

# Create venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
pip install -r requirements.txt

# Run pipeline
python -m src.main

# Or run notebook
jupyter notebook notebooks/01_etl_pipeline.ipynb
```

Outputs in `data/processed/`:
- `fact_prices.csv`
- `dim_asset.csv`
- `dim_calendar.csv`
- `stocks.db` (SQLite with indexes)

## 8. Example Insights (from this dataset 2022-present)
- Petrobras (PETR4) shows highest volatility linked to commodity cycles
- WEG (WEGE3) consistently outperforms IBOVESPA in cumulative return
- IFIX provides lower volatility hedge vs pure equity

Add your charts in `images/` and link here.

## 9. SQL Analysis Examples
See `sql/analysis_queries.sql`:
- Last close per asset
- Monthly average
- Cumulative return vs benchmark
- Sector analysis

## 10. Future Improvements
- [ ] Add CDI rate from IPEA API
- [ ] Add technical indicators (SMA, RSI)
- [ ] Orchestrate with Airflow
- [ ] Deploy to BigQuery + dbt

## 11. Author
Oalis Anjos - Data Analyst
[LinkedIn](https://linkedin.com/in/your-profile) | [GitHub](https://github.com/your-username)

---
If this helped you, please give it a ⭐
