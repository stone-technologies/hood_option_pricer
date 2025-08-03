import logging
from datetime import datetime
from typing import List, Tuple
from time import sleep
import pandas as pd

from .data_fetcher import DataFetcher
from .estimators import VolatilityEstimator
from .params import OptionParams
from .pricers import BlackScholesPricer, BinomialCRRPricer, MonteCarloPricer

logger = logging.getLogger(__name__)

class OptionPricingEngine:
    def __init__(self, params: OptionParams):
        self.params = params
        self.fetcher = DataFetcher()
        self.vol_estimator = VolatilityEstimator()
        self.pricers: List[Tuple[str, object]] = [
            ("Black–Scholes", BlackScholesPricer()),
            ("Binomial CRR", BinomialCRRPricer(params.binomial_steps)),
            ("Monte Carlo", MonteCarloPricer(params.mc_paths))
        ]

    def _time_to_expiry(self) -> float:
        delta = max((self.params.expiry - datetime.now()).days, 0)
        return delta / 365.0

    def run(self) -> pd.DataFrame:
        logger.info("Fetching data for %s", self.params.ticker)
        prices = self.fetcher.fetch_close_prices(
            self.params.ticker,
            self.params.volatility_window,
            self.params.max_retries,
            self.params.backoff_factor
        )
        S0 = self.fetcher.fetch_spot_price(prices)
        sigma = self.vol_estimator.estimate_annual_vol(prices)
        T = self._time_to_expiry()

        rows = []
        for name, pricer in self.pricers:
            c = pricer.call_price(S0, self.params.strike, T, self.params.rate, sigma)
            p = pricer.put_price(S0, self.params.strike, T, self.params.rate, sigma)
            logger.info("%s Call=%.4f, Put=%.4f", name, c, p)
            rows.extend([
                {"method": name, "type": "call", "price": c},
                {"method": name, "type": "put",  "price": p},
            ])

        df = pd.DataFrame(rows)
        df.insert(0, "ticker", self.params.ticker)
        df["strike"] = self.params.strike
        df["expiry"] = self.params.expiry.isoformat()
        return df
