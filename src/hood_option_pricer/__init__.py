"""
HOOD Option Pricer package
"""
from .cli import main
from datetime import datetime
from .engine import OptionPricingEngine
from .params import OptionParams
from .estimators import VolatilityEstimator
from .data_fetcher import DataFetcher
from .pricers import BlackScholesPricer, BinomialCRRPricer, MonteCarloPricer

def estimate(ticker: str, strike: float, expiry: str):
    expiry = datetime.fromisoformat(expiry)
    params = OptionParams(ticker=ticker, strike=strike, expiry=expiry)
    engine = OptionPricingEngine(params)
    return engine.run()
