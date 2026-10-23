from datetime import date
from dataclasses import replace
from test_quantitative_core import make_series, FakeResponse
from market_wrap.preparation import spx_preparation
from market_wrap.data import YahooChartClient
from market_wrap.pipeline import collect_bundle, DEFAULT_INSTRUMENTS
import json


def test_map_uses_completed_session_and_rejects_proxy_or_stale():
    original = make_series(210)
    spx = replace(original, symbol='^GSPC', instrument='SPX cash index')
    day = date.fromisoformat(spx.latest.timestamp[:10])
    text = spx_preparation(spx, day)
    assert '| Completed-session high | 310.00 |' in text
    assert '| Completed-session low | 307.00 |' in text
    assert '| Completed-session close / gap reference | 309.00 |' in text
    assert all(term in text for term in ['Gap down', 'Gap up', 'Flat near', 'Invalidation', 'No trade', 'SET', 'pending official'])
    assert 'UNAVAILABLE' in spx_preparation(original, day)
    assert 'UNAVAILABLE' in spx_preparation(spx, date(2026, 1, 1))
    assert 'UNAVAILABLE' in spx_preparation(None, day)


def test_spx_volume_is_never_native_volume():
    payload = {'chart': {'result': [{'timestamp': [1700000000], 'indicators': {'quote': [dict(open=[10], high=[12], low=[9], close=[11], volume=[999])]}}]}}
    client = YahooChartClient(opener=lambda *a, **k: FakeResponse(json.dumps(payload).encode()))
    assert client.history('^GSPC', 'SPX').latest.volume is None
    assert client.history('SPY', 'ETF').latest.volume == 999


def test_stale_and_failed_collection_never_generates_fresh_levels(tmp_path, monkeypatch):
    monkeypatch.setattr(YahooChartClient, 'histories', lambda *a, **k: ({'^GSPC': replace(make_series(), symbol='^GSPC')}, []))
    data, failures = collect_bundle(tmp_path, date(2026, 1, 1))
    assert not data
    assert 'stale' in failures[0].reason
    assert 'UNAVAILABLE' in (tmp_path / 'data/daily/2026-01-01/spx-preparation.md').read_text()
    assert {'^GSPC', 'SPY', 'QQQ', 'IWM', 'XLV', 'XLK', 'XLF', 'XLE', 'XLI'} <= DEFAULT_INSTRUMENTS.keys()
