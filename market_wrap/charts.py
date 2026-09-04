"""Publication-quality charts generated from committed observations."""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

from .analytics import simple_moving_average
from .models import MarketSeries


def render_price_chart(series: MarketSeries, output: Path, *, windows: tuple[int, ...] = (20, 50, 200)) -> Path:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("chart rendering requires matplotlib") from exc

    if len(series.observations) < min(windows):
        raise ValueError(f"{series.symbol} needs at least {min(windows)} observations for requested chart")
    dates = [datetime.fromisoformat(item.timestamp.replace("Z", "+00:00")) for item in series.observations]
    closes = [item.close for item in series.observations]
    fig, axis = plt.subplots(figsize=(12, 6.5), constrained_layout=True)
    axis.plot(dates, closes, color="#14213d", linewidth=2.0, label="Close")
    colors = ("#2a9d8f", "#e9c46a", "#e76f51")
    for window, color in zip(windows, colors):
        axis.plot(dates, simple_moving_average(closes, window), color=color, linewidth=1.35, label=f"{window}-day SMA")
    axis.set_title(f"{series.instrument} ({series.symbol}) — Daily Technical Structure", loc="left", fontweight="bold")
    axis.set_ylabel(f"Price ({series.currency})")
    axis.set_xlabel("Date")
    axis.grid(axis="y", alpha=0.22)
    axis.legend(frameon=False, ncol=4)
    axis.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=9))
    axis.text(0, -0.16, f"Source: {series.source_name} | Latest: {series.latest.timestamp}", transform=axis.transAxes, fontsize=8, color="#555555")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160, facecolor="white", metadata={"Title": f"{series.symbol} technical chart"})
    plt.close(fig)
    return output


def render_relative_chart(primary: MarketSeries, secondary: MarketSeries, output: Path) -> Path:
    """Plot rebased closes on common dates; never interpolate missing sessions."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("chart rendering requires matplotlib") from exc
    first = {item.timestamp[:10]: item.close for item in primary.observations}
    second = {item.timestamp[:10]: item.close for item in secondary.observations}
    common_dates = sorted(first.keys() & second.keys())
    if len(common_dates) < 2:
        raise ValueError("relative chart requires at least two common observations")
    dates = [datetime.fromisoformat(value) for value in common_dates]
    a0, b0 = first[common_dates[0]], second[common_dates[0]]
    a = [first[value] / a0 * 100 for value in common_dates]
    b = [second[value] / b0 * 100 for value in common_dates]
    fig, axis = plt.subplots(figsize=(12, 6.5), constrained_layout=True)
    axis.plot(dates, a, linewidth=2, label=primary.symbol)
    axis.plot(dates, b, linewidth=2, label=secondary.symbol)
    axis.axhline(100, color="#777", linewidth=.8, alpha=.5)
    axis.set_title(f"{primary.instrument} vs. {secondary.instrument} — Rebased Performance", loc="left", fontweight="bold")
    axis.set_ylabel("Index (first common observation = 100)")
    axis.set_xlabel("Date")
    axis.grid(axis="y", alpha=.22)
    axis.legend(frameon=False)
    axis.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=9))
    axis.xaxis.set_major_formatter(mdates.ConciseDateFormatter(axis.xaxis.get_major_locator()))
    axis.text(0, -0.16, f"Sources: {primary.source_name}; {secondary.source_name} | No interpolation", transform=axis.transAxes, fontsize=8, color="#555")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=160, facecolor="white")
    plt.close(fig)
    return output
