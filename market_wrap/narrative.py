from __future__ import annotations

from datetime import datetime

import pandas as pd

from .models import CalendarEvent, NewsItem


def _move_text(row: pd.Series) -> str:
    direction = "rose" if row["1D"] >= 0 else "fell"
    return f"{row['Asset']} {direction} {abs(row['1D']):.1%}"


def build_market_narrative(
    returns: pd.DataFrame,
    levels: pd.DataFrame,
    volatility: pd.DataFrame,
    events: list[CalendarEvent],
    news: list[NewsItem],
    now: datetime,
) -> list[str]:
    """Create a factual morning narrative without asserting unverified causality."""
    paragraphs: list[str] = []
    usable = returns.dropna(subset=["1D"]) if not returns.empty else returns
    if not usable.empty:
        strongest = usable.loc[usable["1D"].idxmax()]
        weakest = usable.loc[usable["1D"].idxmin()]
        equities = usable.loc[usable["Group"] == "Equities"]
        tone = "positive" if not equities.empty and equities["1D"].mean() > 0 else "defensive"
        paragraphs.append(
            f"The cross-asset tone is {tone} entering the session. {_move_text(strongest)}, "
            f"while {_move_text(weakest)}. These are the latest available daily closes, so the "
            "moves describe the setup rather than live pre-market trading."
        )

    level_rows = levels.set_index("Asset") if not levels.empty else levels
    equity_names = returns.loc[returns["Group"] == "Equities", "Asset"] if not returns.empty else []
    signals: list[str] = []
    for name in list(equity_names)[:3]:
        if name not in level_rows.index:
            continue
        row = level_rows.loc[name]
        ma50 = row.get("50D MA")
        ma200 = row.get("200D MA")
        if pd.notna(ma50) and pd.notna(ma200):
            position = "above" if row["Last"] > ma50 else "below"
            trend = "above" if ma50 > ma200 else "below"
            signals.append(f"{name} is {position} its 50-day average, with the 50-day {trend} the 200-day")
    if signals:
        vol_note = ""
        iv_rows = volatility.dropna(subset=["IV Proxy"]) if not volatility.empty else volatility
        if not iv_rows.empty:
            lead = iv_rows.iloc[0]
            relation = "above" if lead["IV-RV Spread"] >= 0 else "below"
            vol_note = (
                f" For {lead['Asset']}, the implied-volatility proxy is {lead['IV Proxy']:.1%}, "
                f"{relation} 20-day realized volatility of {lead['RV20']:.1%}."
            )
        paragraphs.append("Technically, " + "; ".join(signals) + "." + vol_note)

    if events:
        upcoming = events[:3]
        descriptions: list[str] = []
        for event in upcoming:
            local = event.when.astimezone(now.tzinfo)
            day = "today" if local.date() == now.date() else local.strftime("%A")
            descriptions.append(f"{event.title} {day} at {local:%H:%M %Z}")
        paragraphs.append(
            "The scheduled-event focus is " + ", followed by ".join(descriptions) +
            ". High-importance releases or policy events can change rates, volatility, and index direction quickly."
        )

    if news:
        themes = "; ".join(item.title for item in news[:3])
        paragraphs.append(
            f"The leading monitored headlines are: {themes}. They are included as the current news agenda; "
            "the report does not infer that a headline caused a market move without corroborating evidence."
        )

    if not paragraphs:
        paragraphs.append(
            "Market context is limited because current price, calendar, and headline inputs were unavailable. "
            "Review the data-quality flags below before relying on this report."
        )
    return paragraphs
