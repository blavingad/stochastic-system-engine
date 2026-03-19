from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import yfinance as yf

from stochastic_systems_engine.data.base import PriceDataLoader


@dataclass(slots=True)
class YahooFinanceLoader(PriceDataLoader):
    """Historical market data loader backed by Yahoo Finance."""

    auto_adjust: bool = False
    progress: bool = False

    def load_history(self, symbol: str, start: str, end: str) -> pd.DataFrame:
        """Download and standardize historical OHLCV data from Yahoo Finance."""
        self._validate_inputs(symbol=symbol, start=start, end=end)

        raw_data = yf.download(
            tickers=symbol,
            start=start,
            end=end,
            auto_adjust=self.auto_adjust,
            progress=self.progress,
        )

        print("\nRAW DATA HEAD:\n")
        print(raw_data.head())

        print("\nRAW COLUMNS:\n")
        print(raw_data.columns)

        if raw_data.empty:
            raise ValueError(
                f"No data returned for symbol='{symbol}' between '{start}' and '{end}'."
            )

        clean_data = self._standardize_dataframe(raw_data)

        if clean_data.empty:
            raise ValueError(
                f"Data for symbol='{symbol}' is empty after standardization."
            )

        return clean_data

    @staticmethod
    def _validate_inputs(symbol: str, start: str, end: str) -> None:
        """Validate user inputs before downloading data."""
        if not isinstance(symbol, str) or not symbol.strip():
            raise ValueError("Parameter 'symbol' must be a non-empty string.")

        if not isinstance(start, str) or not start.strip():
            raise ValueError("Parameter 'start' must be a non-empty string.")

        if not isinstance(end, str) or not end.strip():
            raise ValueError("Parameter 'end' must be a non-empty string.")

        try:
            start_ts = pd.to_datetime(start, format="%Y-%m-%d", errors="raise")
            end_ts = pd.to_datetime(end, format="%Y-%m-%d", errors="raise")
        except ValueError as exc:
            raise ValueError("Dates must be in YYYY-MM-DD format.") from exc

        if start_ts >= end_ts:
            raise ValueError(
                f"Expected start < end, but got start='{start}' and end='{end}'."
            )

    @staticmethod
    def _standardize_dataframe(raw_data: pd.DataFrame) -> pd.DataFrame:
        """Convert Yahoo Finance output into the project's standard schema."""
        data = raw_data.copy()

        print("\nSTANDARDIZE: incoming columns\n")
        print(data.columns)

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        print("\nSTANDARDIZE: flattened columns\n")
        print(data.columns)

        data = data.reset_index()

        print("\nSTANDARDIZE: after reset_index columns\n")
        print(data.columns)

        rename_map = {
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        }
        data = data.rename(columns=rename_map)

        print("\nSTANDARDIZE: after rename columns\n")
        print(data.columns)

        if "adj_close" not in data.columns and "close" in data.columns:
            data["adj_close"] = data["close"]

        required_columns = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]

        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise ValueError(
                f"Missing required columns after standardization: {missing_columns}. "
                f"Available columns: {list(data.columns)}"
            )

        data = data[required_columns].copy()

        data["date"] = pd.to_datetime(data["date"])

        numeric_columns = ["open", "high", "low", "close", "adj_close", "volume"]
        data[numeric_columns] = data[numeric_columns].apply(
            pd.to_numeric, errors="coerce"
        )

        data = data.dropna(subset=["date", "open", "high", "low", "close", "adj_close"])
        data = data.sort_values("date").reset_index(drop=True)

        return data