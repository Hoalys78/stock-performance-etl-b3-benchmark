
from datetime import datetime
from pathlib import Path

# Paths
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
DB_PATH = PROCESSED_DIR / "stocks.db"

# Period
START_DATE = "2022-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")

# Yahoo Finance tickers
TICKERS = {
    # Brazilian Stocks (B3)
    "PETR4.SA": "Petrobras",
    "VALE3.SA": "Vale",
    "ITUB4.SA": "Itau Unibanco",
    "WEGE3.SA": "WEG",
    "MGLU3.SA": "Magazine Luiza",
    # Benchmarks
    "^BVSP": "IBOVESPA",
    "^GSPC": "S&P 500",
    "BRL=X": "USD/BRL",
    "^IFIX": "IFIX",
}

ASSET_METADATA = {
    "PETR4.SA": {"sector": "Energy", "industry": "Oil & Gas", "type": "Stock"},
    "VALE3.SA": {"sector": "Materials", "industry": "Mining", "type": "Stock"},
    "ITUB4.SA": {"sector": "Financial", "industry": "Banking", "type": "Stock"},
    "WEGE3.SA": {"sector": "Industrials", "industry": "Machinery", "type": "Stock"},
    "MGLU3.SA": {"sector": "Consumer Cyclical", "industry": "E-commerce", "type": "Stock"},
    "^BVSP": {"sector": "Benchmark", "industry": "Brazilian Index", "type": "Benchmark"},
    "^IFIX": {"sector": "Benchmark", "industry": "REIT Index", "type": "Benchmark"},
    "^GSPC": {"sector": "Benchmark", "industry": "US Index", "type": "Benchmark"},
    "BRL=X": {"sector": "Benchmark", "industry": "FX Rate", "type": "Benchmark"},
    "CDI": {"sector": "Benchmark", "industry": "Fixed Income", "type": "Benchmark"},
}

EXPECTED_COLUMNS = {"Open", "High", "Low", "Close", "Volume"}
