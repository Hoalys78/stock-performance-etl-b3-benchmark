
import pandas as pd
from .logger import get_logger

log = get_logger(__name__)

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean, standardize and validate raw DataFrame.

    Steps:
      - Rename columns to snake_case (English)
      - Normalize data types
      - Handle nulls with differentiated strategy
      - Remove exact duplicates
      - Validate price ranges (sanity check)
    """
    log.info("Starting data transformation...")
    df = df.copy()

    column_map = {
        "Date": "date",
        "Open": "open_price",
        "High": "high_price",
        "Low": "low_price",
        "Close": "close_price",
        "Volume": "volume",
        "date": "date",
        "open": "open_price",
        "high": "high_price",
        "low": "low_price",
        "close": "close_price",
        "volume": "volume",
        "Dividends": "dividends",
        "Stock Splits": "stock_splits",
    }
    df = df.rename(columns=column_map)

    keep_cols = {"date", "ticker", "company", "open_price", "high_price", "low_price", "close_price", "volume"}
    extra_cols = [c for c in df.columns if c not in keep_cols]
    if extra_cols:
        log.info("Dropping unused columns: %s", extra_cols)
        df = df.drop(columns=extra_cols, errors="ignore")

    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.normalize()
    for col in ("open_price", "high_price", "low_price", "close_price"):
        df[col] = pd.to_numeric(df[col], errors="coerce").round(4)
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0).astype("int64")

    # Critical field: close_price
    n_before = len(df)
    df = df.dropna(subset=["close_price"])
    if len(df) < n_before:
        log.warning("Removed %d rows without close_price (%.1f%%)", n_before - len(df), (n_before - len(df))/n_before*100)

    for col in ("open_price", "high_price", "low_price"):
        nulls = df[col].isna().sum()
        if nulls > 0:
            df[col] = df[col].fillna(df["close_price"])
            log.info("  %s: %d nulls filled with close_price", col, nulls)

    invalid = df[df["close_price"] <= 0]
    if not invalid.empty:
        log.warning("Found %d records with price <= 0 - removing", len(invalid))
        df = df[df["close_price"] > 0]

    n_dup = df.duplicated(subset=["date", "ticker"]).sum()
    if n_dup > 0:
        log.warning("Removing %d duplicate records (date + ticker)", n_dup)
        df = df.drop_duplicates(subset=["date", "ticker"], keep="last")

    df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    df.insert(0, "price_id", df.index + 1)

    log.info(
        "Transformation done: %d rows | %d assets | period: %s -> %s",
        len(df), df["ticker"].nunique(), df["date"].min().date(), df["date"].max().date()
    )
    return df
