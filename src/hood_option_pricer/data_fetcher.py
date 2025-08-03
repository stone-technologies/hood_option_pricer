import time
import logging
from time import sleep
from typing import Any
import pandas as pd
import yfinance as yf
from curl_cffi import requests

logger = logging.getLogger(__name__)

class DataFetcher:
    @staticmethod
    def fetch_close_prices(
        ticker: str, hist_days: int,
        max_retries: int, backoff_factor: float
    ) -> pd.Series:
        attempt = 0
        while attempt < max_retries:
            try:
                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/136.0.0.0 Safari/537.36"
                    )
                }
                session = requests.Session(
                    impersonate="chrome", headers=headers, verify=False
                )
                sleep(1)
                logger.info('Wait, stone mode')
                tk = yf.Ticker(ticker, session=session)  # type: ignore
                df = tk.history(period=f"{hist_days+10}d")
                series = df["Close"].dropna().tail(hist_days)
                if series.empty:
                    raise ValueError("No close price data returned")
                return series
            except Exception as e:
                msg = str(e).lower()
                if "rate limited" in msg or "too many requests" in msg:
                    attempt += 1
                    wait = backoff_factor ** attempt
                    logger.warning(
                        "Rate limit for %s (attempt %d/%d), retrying in %.1f sec",
                        ticker, attempt, max_retries, wait
                    )
                    time.sleep(wait)
                    continue
                logger.error("Data fetch error for %s: %s", ticker, e)
                raise
        raise RuntimeError(
            f"Failed to fetch data for {ticker} after {max_retries} attempts"
        )

    @staticmethod
    def fetch_spot_price(close_prices: pd.Series) -> float:
        return float(close_prices.iloc[-1])
