import pytest
from datetime import datetime, timedelta
from hood_option_pricer.engine import OptionPricingEngine
from hood_option_pricer.params import OptionParams

def test_engine_no_time():
    expiry = datetime.now() - timedelta(days=1)
    params = OptionParams(ticker="HOOD", expiry=expiry, strike=50)
    engine = OptionPricingEngine(params)
    df = engine.run()
    assert set(df["type"]) == {"call","put"}
    assert "Black–Scholes" in df["method"].values
