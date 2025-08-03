import pytest
from hood_option_pricer.pricers import BlackScholesPricer

def test_bs_zero_time():
    pricer = BlackScholesPricer()
    assert pricer.call_price(100, 100, 0, 0.05, 0.2) == 0
    assert pricer.put_price(100, 100, 0, 0.05, 0.2) == pytest.approx(0)
