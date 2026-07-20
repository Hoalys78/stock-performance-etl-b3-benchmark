
import pandas as pd
from .logger import get_logger
from .config import ASSET_METADATA

log = get_logger(__name__)

def create_dim_asset(df: pd.DataFrame) -> pd.DataFrame:
    """Create enriched asset dimension with sector metadata."""
    log.info("Creating dim_asset...")
    assets = df[["ticker", "company"]].drop_duplicates().copy().sort_values("ticker").reset_index(drop=True)
    assets["sector"] = assets["ticker"].map(lambda x: ASSET_METADATA.get(x, {}).get("sector", "N/A"))
    assets["industry"] = assets["ticker"].map(lambda x: ASSET_METADATA.get(x, {}).get("industry", "N/A"))
    assets["asset_type"] = assets["ticker"].map(lambda x: ASSET_METADATA.get(x, {}).get("type", "Stock"))
    assets.insert(0, "asset_id", assets.index + 1)
    log.info("dim_asset: %d records", len(assets))
    return assets[["asset_id", "ticker", "company", "sector", "industry", "asset_type"]]

def create_dim_calendar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create continuous calendar dimension.
    Required for Power BI time intelligence (TOTALYTD, SAMEPERIODLASTYEAR).
    """
    log.info("Creating dim_calendar...")
    dates = pd.date_range(start=df["date"].min(), end=df["date"].max(), freq="D")
    cal = pd.DataFrame({"date": dates})
    cal["date_id"] = (cal.index + 1).astype("int32")
    cal["year"] = cal["date"].dt.year.astype("int16")
    cal["month"] = cal["date"].dt.month.astype("int8")
    cal["day"] = cal["date"].dt.day.astype("int8")
    cal["quarter"] = cal["date"].dt.quarter.astype("int8")
    cal["week_of_year"] = cal["date"].dt.isocalendar().week.astype("int8")
    cal["day_of_week_num"] = cal["date"].dt.dayofweek.astype("int8")
    cal["day_name"] = cal["date"].dt.strftime("%A")
    cal["month_name"] = cal["date"].dt.strftime("%B")
    cal["year_month"] = cal["date"].dt.strftime("%Y-%m")
    cal["year_quarter"] = cal["date"].dt.year.astype(str) + " Q" + cal["date"].dt.quarter.astype(str)
    cal["is_weekday"] = (cal["date"].dt.dayofweek < 5).astype(bool)
    log.info("dim_calendar: %d days | %d weekdays", len(cal), cal["is_weekday"].sum())
    return cal
