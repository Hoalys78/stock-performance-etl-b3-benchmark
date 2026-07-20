
from __future__ import annotations
from typing import Optional
import pandas as pd
import yfinance as yf
from .logger import get_logger

log = get_logger(__name__)

def _download_single_ticker(ticker: str, start: str, end: str) -> Optional[pd.DataFrame]:
    """
    Fallback method: download one ticker at a time using Ticker.history().
    Ticker.history() always returns flat columns (no MultiIndex), more robust.
    """
    try:
        t = yf.Ticker(ticker)
        df = t.history(start=start, end=end, auto_adjust=True)
        if df.empty:
            log.warning("No data returned for %s", ticker)
            return None
        df = df.reset_index()
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
        df["ticker"] = ticker
        log.info("  [fallback] %s -> %d rows", ticker, len(df))
        return df
    except Exception as exc:
        log.error("  Failed to download %s via fallback: %s", ticker, exc)
        return None

def extract_quotes(tickers: dict[str, str], start: str, end: str) -> pd.DataFrame:
    """
    Extract historical quotes from Yahoo Finance.

    Two-layer strategy:
      1. Batch download with yf.download() - faster
      2. Individual Ticker.history() fallback - more robust

    Returns consolidated DataFrame with standardized columns.
    """
    log.info("Starting extraction: %d assets | %s -> %s", len(tickers), start, end)
    ticker_list = list(tickers.keys())
    frames: list[pd.DataFrame] = []

    try:
        log.info("Attempting batch download...")
        raw = yf.download(
            tickers=" ".join(ticker_list),
            start=start,
            end=end,
            auto_adjust=True,
            progress=False,
            threads=True,
            multi_level_index=True,
        )
        if raw.empty:
            raise ValueError("yf.download() returned empty DataFrame")

        # Handle MultiIndex columns (Price, Ticker) in yfinance 1.x
        if isinstance(raw.columns, pd.MultiIndex):
            log.info("MultiIndex detected - stacking by ticker...")
            raw = raw.stack(level=1, future_stack=True).reset_index()
            raw.columns.name = None
            ticker_col = raw.columns[1]
            if ticker_col != "ticker":
                raw = raw.rename(columns={ticker_col: "ticker"})
        else:
            raw = raw.reset_index()
            raw["ticker"] = ticker_list[0]

        for date_col in ("Date", "Datetime", "date", "datetime"):
            if date_col in raw.columns:
                raw = raw.rename(columns={date_col: "Date"})
                break

        for ticker in ticker_list:
            df_ticker = raw[raw["ticker"] == ticker].copy()
            if df_ticker.empty:
                log.warning("No batch data for %s -> trying fallback", ticker)
                fb = _download_single_ticker(ticker, start, end)
                if fb is not None:
                    frames.append(fb)
            else:
                df_ticker["ticker"] = ticker
                log.info("  %s -> %d rows", ticker, len(df_ticker))
                frames.append(df_ticker)

    except Exception as exc:
        log.warning("Batch download failed (%s) - switching to individual fallback", exc)
        for ticker in ticker_list:
            df_ticker = _download_single_ticker(ticker, start, end)
            if df_ticker is not None:
                frames.append(df_ticker)

    if not frames:
        raise RuntimeError("No data extracted. Check connectivity and tickers.")

    consolidated = pd.concat(frames, ignore_index=True)
    consolidated["company"] = consolidated["ticker"].map(tickers)

    log.info(
        "Extraction completed: %d rows | %d unique assets",
        len(consolidated),
        consolidated["ticker"].nunique(),
    )
    return consolidated
