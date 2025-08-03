import numpy as np
import pandas as pd

class VolatilityEstimator:
    @staticmethod
    def estimate_annual_vol(price_series: pd.Series) -> float:
        log_rets = np.log(price_series / price_series.shift(1)).dropna()
        return float(log_rets.std(ddof=1) * np.sqrt(252))
