## Setup Commands

```bash
poetry config virtualenvs.in-project true
poetry install

# Run script
poetry run python scripts/run_brent_call_pricer.py

# Run tests
poetry run pytest

## Overview

This project implements a stochastic modeling framework for financial assets, starting from real market data and building toward derivative pricing and simulation.

The current model:
- retrieves historical price data (e.g. Brent oil proxy)
- estimates volatility from log returns
- models asset dynamics using Geometric Brownian Motion (GBM)
- simulates price paths via Monte Carlo methods
- prices European call options under the risk-neutral measure
- benchmarks results against the Black–Scholes closed-form solution

The system is designed as a modular "stochastic engine", with clear separation between data, models, pricing, and execution layers, enabling future extensions toward strategy development and market microstructure modeling.