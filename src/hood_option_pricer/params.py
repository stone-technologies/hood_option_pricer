from dataclasses import dataclass
from datetime import datetime

@dataclass
class OptionParams:
    ticker: str
    expiry: datetime
    strike: float
    rate: float = 0.05
    volatility_window: int = 252
    binomial_steps: int = 200
    mc_paths: int = 200_000
    max_retries: int = 5
    backoff_factor: float = 1.5
