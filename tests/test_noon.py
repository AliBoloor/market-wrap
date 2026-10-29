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


def test_cli_refuses_duplicate_noon_issue(tmp_path, monkeypatch):
    import json
    import market_wrap.trade_ideas as mod
    class Noon(datetime):
        @classmethod
        def now(cls,tz=None):
            return cls.fromisoformat('2026-10-29T19:00:00+00:00')
    monkeypatch.setattr(mod,'datetime',Noon)
    folder=tmp_path/'data/trade-ideas/2026-10-29';folder.mkdir(parents=True)
    (folder/'complete.json').write_text(json.dumps(dict(status='validated',report_family='trade-ideas',trading_date='2026-10-29')))
    evidence=tmp_path/'ideas.json';evidence.write_text(json.dumps(dict(publication_mode='noon',trading_date='2026-10-29',next_session='2026-10-30',calendar_verified=True)))
    import pytest
    with pytest.raises(ValueError,match='already validated'):
        mod.write_ideas(evidence,tmp_path)
