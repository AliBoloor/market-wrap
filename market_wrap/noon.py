"""Deterministic timing/duplicate gate; researcher verifies exchange calendar."""
from datetime import datetime, date, time
from zoneinfo import ZoneInfo


def eligibility(now: datetime, *, session: date, next_session: date,
                is_trading_day: bool, completed: bool) -> tuple[bool, str]:
    if now.tzinfo is None:
        raise ValueError('timezone-aware current time required')
    pacific=now.astimezone(ZoneInfo('America/Vancouver'))
    if session!=pacific.date() or session!=now.astimezone(ZoneInfo('America/New_York')).date():
        return False,'only current session; no silent backfill'
    if not is_trading_day or session.weekday()>4:
        return False,'exchange closed'
    if pacific.time()<time(12):
        return False,'before noon Pacific'
    if next_session<=session:
        return False,'next verified session required'
    if completed:
        return False,'Trade Ideas date already validated'
    return True,'noon eligible; actual session state and observation times must be labeled'
