
"""
ETL - Stock Performance Dashboard
Main entry point
"""
from pathlib import Path
import sys

# allow running as script
sys.path.append(str(Path(__file__).parent.parent))

from src.config import TICKERS, START_DATE, END_DATE, RAW_DIR, PROCESSED_DIR
from src.extract import extract_quotes
from src.transform import transform_data
from src.dimensions import create_dim_asset, create_dim_calendar
from src.load import export_data
from src.quality import data_quality_report
from src.logger import get_logger

log = get_logger(__name__)

def main():
    log.info("="*60)
    log.info("Stock Performance Dashboard - ETL Pipeline v2.0")
    log.info("="*60)
    try:
        raw = extract_quotes(TICKERS, START_DATE, END_DATE)
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        raw.to_csv(RAW_DIR / "quotes_raw.csv", index=False)

        fact = transform_data(raw)
        dim_asset = create_dim_asset(fact)
        dim_cal = create_dim_calendar(fact)

        data_quality_report(fact)
        export_data(fact, dim_asset, dim_cal)

    except Exception as exc:
        log.critical("Pipeline failed: %s", exc, exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
