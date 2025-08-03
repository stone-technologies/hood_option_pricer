import logging
import sys
from datetime import datetime

import click
import pandas as pd

from .engine import OptionPricingEngine
from .params import OptionParams

logger = logging.getLogger(__name__)

@click.command()
@click.option("--ticker", default="HOOD", help="Ticker symbol")
@click.option("--strike", type=float, required=True, help="Strike price")
@click.option("--expiry", required=True, help="Expiry YYYY-MM-DD")
@click.option("--rate", default=0.05, help="Risk-free rate")
def main(ticker, strike, expiry, rate):
    logging.basicConfig(level=logging.INFO)
    params = OptionParams(
        ticker=ticker,
        strike=strike,
        expiry=datetime.fromisoformat(expiry),
        rate=rate
    )
    engine = OptionPricingEngine(params)
    df: pd.DataFrame = engine.run()
    print(df.to_markdown(index=False))

if __name__ == "__main__":
    sys.exit(main())
