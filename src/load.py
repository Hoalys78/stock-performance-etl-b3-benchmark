
import sqlite3
from pathlib import Path
import pandas as pd
from .logger import get_logger
from .config import PROCESSED_DIR

log = get_logger(__name__)

def export_data(fact: pd.DataFrame, dim_asset: pd.DataFrame, dim_cal: pd.DataFrame) -> None:
    """
    Persist data in two formats:
      - CSV for Power BI direct consumption
      - SQLite for SQL analysis (EDA)
    In production this would be Snowflake/BigQuery/Delta Lake.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    tables = {
        "fact_prices": fact,
        "dim_asset": dim_asset,
        "dim_calendar": dim_cal,
    }
    for name, df in tables.items():
        path = PROCESSED_DIR / f"{name}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        log.info("CSV saved: %s (%d rows)", path, len(df))

    db_path = PROCESSED_DIR / "stocks.db"
    conn = sqlite3.connect(db_path)
    for name, df in tables.items():
        df.to_sql(name, conn, if_exists="replace", index=False)

    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_fact_ticker ON fact_prices(ticker)",
        "CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_prices(date)",
        "CREATE INDEX IF NOT EXISTS idx_fact_price_id ON fact_prices(price_id)",
        "CREATE INDEX IF NOT EXISTS idx_asset_ticker ON dim_asset(ticker)",
        "CREATE INDEX IF NOT EXISTS idx_cal_date ON dim_calendar(date)",
    ]
    for sql in indexes:
        conn.execute(sql)
    conn.commit()
    conn.close()
    log.info("SQLite saved: %s", db_path)
    log.info("\n%s\n  Pipeline completed\n  fact_prices    : %8d rows\n  dim_asset      : %8d assets\n  dim_calendar   : %8d days\n%s",
              "="*50, len(fact), len(dim_asset), len(dim_cal), "="*50)
