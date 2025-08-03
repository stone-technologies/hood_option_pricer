# HOOD Option Pricer

Option pricer for little stone for any ticker, any expiration, any strike.

## Installation

```bash
pip install .
```

Or use:
```bash
pip install -r requirements.txt
```

## Usage

```python
from hood_option_pricer.cli import main
# CLI: hood-pricer --ticker HOOD --strike 35 --expiry 2025-12-19

from hood_option_pricer import estimate
import pandas as pd

df = estimate(ticker="HOOD", strike=35.0, expiry="2025-12-19")
print(df)
```

## Development

- Tests: `pytest`
- Lint: `flake8`
- Format: `black src tests`

## TODO:

Add volatility surface 
Add payoff graphs
Add proprietary volatility calculations (not sure if worth it for liquid options, maybe biotech or illiquid).
