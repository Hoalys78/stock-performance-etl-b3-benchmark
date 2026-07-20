
import pandas as pd
from .logger import get_logger

log = get_logger(__name__)

def data_quality_report(df: pd.DataFrame) -> None:
    """Print data quality summary for documentation."""
    log.info("\n-- DATA QUALITY REPORT --")
    log.info("Total records  : %d", len(df))
    log.info("Assets         : %s", df["ticker"].unique().tolist())
    log.info("Period         : %s -> %s", df["date"].min().date(), df["date"].max().date())
    nulls = df.isnull().sum()
    if (nulls > 0).any():
        log.info("Remaining nulls:\n%s", nulls[nulls>0])
    else:
        log.info("Remaining nulls  : 0")
    for ticker in df["ticker"].unique():
        sub = df[df["ticker"] == ticker]
        log.info(
            "  %-10s | %d trading days | close: min=%.2f max=%.2f avg=%.2f",
            ticker, len(sub), sub["close_price"].min(), sub["close_price"].max(), sub["close_price"].mean()
        )
