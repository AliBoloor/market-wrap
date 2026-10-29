from datetime import datetime,date,timedelta
from zoneinfo import ZoneInfo
from market_wrap.noon import eligibility


def gate(stamp,**kw):
    p=dict(session=date(2026,10,29),next_session=date(2026,10,30),is_trading_day=True,completed=False);p.update(kw)
    return eligibility(datetime.fromisoformat(stamp),**p)[0]


def test_exact_noon_dst_and_duplicate_gate():
    assert not gate('2026-10-29T18:59:59+00:00')
    assert gate('2026-10-29T19:00:00+00:00')
    assert not gate('2026-10-29T19:00:00+00:00',completed=True)
    assert not gate('2026-10-29T19:00:00+00:00',is_trading_day=False)
    assert not gate('2026-10-30T19:00:00+00:00')
    p=dict(session=date(2026,11,27),next_session=date(2026,11,30))
    noon=datetime(2026,11,27,12,tzinfo=ZoneInfo('America/Vancouver'))
    assert not gate((noon-timedelta(seconds=1)).isoformat(),**p)
    assert gate(noon.isoformat(),**p) # early close stays noon local, following IANA rules
