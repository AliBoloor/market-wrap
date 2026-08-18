from __future__ import annotations

import numpy as np
import pandas as pd

from .models import Asset, MarketData, QualityFlag


RETURN_WINDOWS = {"1D": 1, "5D": 5, "1M": 21, "3M": 63, "YTD": None}


def close_series(frame: pd.DataFrame) -> pd.Series:
    column = "adj_close" if "adj_close" in frame and frame["adj_close"].notna().any() else "close"
    series = frame[column].dropna().astype(float)
    return series[~series.index.duplicated(keep="last")].sort_index()


def moving_average(close: pd.Series, window: int) -> pd.Series:
    """Return a full-history simple moving average for table/chart consistency."""
    return close.rolling(window=window, min_periods=window).mean()


def asset_summary(assets: tuple[Asset, ...], data: MarketData) -> pd.DataFrame:
    rows: list[dict] = []
    for asset in assets:
        frame = data.prices.get(asset.symbol)
        if frame is None or frame.empty:
            continue
        close = close_series(frame)
        row = {"Group": asset.group, "Asset": asset.name, "Symbol": asset.symbol, "Last": close.iloc[-1]}
        for label, periods in RETURN_WINDOWS.items():
            if label == "YTD":
                current_year = close.index[-1].year
                base = close[close.index.year == current_year]
                row[label] = close.iloc[-1] / base.iloc[0] - 1 if len(base) > 1 else np.nan
            else:
                row[label] = close.iloc[-1] / close.iloc[-periods - 1] - 1 if len(close) > periods else np.nan
        returns = np.log(close / close.shift(1)).dropna()
        row["RV20"] = returns.tail(20).std(ddof=1) * np.sqrt(252) if len(returns) >= 10 else np.nan
        row["RV60"] = returns.tail(60).std(ddof=1) * np.sqrt(252) if len(returns) >= 20 else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def technical_levels(assets: tuple[Asset, ...], data: MarketData) -> pd.DataFrame:
    rows: list[dict] = []
    for asset in assets:
        frame = data.prices.get(asset.symbol)
        if frame is None or frame.empty:
            continue
        close = close_series(frame)
        rows.append({
            "Asset": asset.name,
            "Last": close.iloc[-1],
            "20D MA": moving_average(close, 20).iloc[-1],
            "50D MA": moving_average(close, 50).iloc[-1],
            "200D MA": moving_average(close, 200).iloc[-1],
            "20D Low": close.tail(20).min(),
            "20D High": close.tail(20).max(),
            "52W Low": close.tail(252).min(),
            "52W High": close.tail(252).max(),
        })
    return pd.DataFrame(rows)


def volatility_summary(assets: tuple[Asset, ...], data: MarketData) -> pd.DataFrame:
    summary = asset_summary(assets, data)
    if summary.empty:
        return summary
    rows: list[dict] = []
    for asset in assets:
        base = summary.loc[summary["Symbol"] == asset.symbol]
        if base.empty:
            continue
        iv = np.nan
        if asset.implied_vol_symbol and asset.implied_vol_symbol in data.prices:
            iv_close = close_series(data.prices[asset.implied_vol_symbol])
            iv = iv_close.iloc[-1] / 100.0
        rv20 = base.iloc[0]["RV20"]
        rows.append({
            "Asset": asset.name, "RV20": rv20, "RV60": base.iloc[0]["RV60"],
            "IV Proxy": iv, "IV-RV Spread": iv - rv20 if pd.notna(iv) and pd.notna(rv20) else np.nan,
        })
    return pd.DataFrame(rows)


def validate_market_data(assets: tuple[Asset, ...], data: MarketData) -> list[QualityFlag]:
    flags: list[QualityFlag] = []
    for asset in assets:
        frame = data.prices.get(asset.symbol)
        if frame is None:
            flags.append(QualityFlag("error", asset.symbol, "Required asset is missing"))
            continue
        close = close_series(frame)
        daily = close.pct_change().dropna()
        if close.index.duplicated().any():
            flags.append(QualityFlag("warning", asset.symbol, "Duplicate timestamps detected"))
        if (close <= 0).any():
            flags.append(QualityFlag("error", asset.symbol, "Non-positive price detected"))
        if (daily.abs() > 0.35).any():
            flags.append(QualityFlag("warning", asset.symbol, "Daily move above 35%; verify adjustment"))
    return flags
