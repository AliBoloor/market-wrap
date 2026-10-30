from copy import deepcopy
from datetime import datetime, timezone
import json
import pytest
from market_wrap.trade_ideas import validate_ideas, render_ideas, write_ideas
from market_wrap.site import build_site, load_report
from test_site import _report


def bundle():
    # Synthetic unit-test values; never published as market observations.
    return dict(trading_date='2026-10-22', next_session='2026-10-23',
        generated_at='2026-10-23T00:00:00+00:00', calendar_source='https://www.nyse.com/markets/hours-calendars',
        max_loss_cap=None, social_coverage='Unit fixture; no posts retrieved', shortfall_reason='Fixture only',
        candidates=[dict(id='test', symbol='TEST', instrument='Synthetic unit fixture',
            underlying_price=100, observed_at='2026-10-22T20:00:00+00:00',
            market_source='https://example.com/fixture', thesis='Conditional test',
            level_basis='Synthetic level', trigger='Reclaim', invalidation='Loss of level',
            no_trade='No confirmation', structure='Illustrative 100/101 call debit vertical',
            expiry='2026-10-26', strike_status='illustrative',
            payoff_profile=dict(kind='debit',option_type='call',long_strike=100,short_strike=101,
                expiry='2026-10-26',quantity=1,multiplier=100,premium=.5,fees=0,assumption_status='illustrative'))])


def test_ideas_render_cap_unset_and_separate_page(tmp_path):
    data = bundle(); text = render_ideas(data)
    assert 'UNSET' in text and 'NOT certified' not in text  # No numeric cap presumed.
    assert 'No candidate is certified' in text and '1/10' in text
    source = tmp_path / 'ideas.json'; source.write_text(json.dumps(data))
    path = write_ideas(source, tmp_path)
    assert load_report(path).family == 'trade-ideas'
    daily = tmp_path / 'content/reports/daily'; daily.mkdir()
    _report(daily / '2026-10-22.md', '2026-10-22', 'Daily')
    out = tmp_path / 'site'; build_site(tmp_path / 'content/reports', out)
    assert 'Illustrative 100/101' in (out / 'trade-ideas/index.html').read_text()
    assert 'href="/market-wrap/trade-ideas/"' in (out / 'index.html').read_text()
    assert (out / 'trade-ideas/archive/index.html').is_file()


@pytest.mark.parametrize('field,value', [('expiry','2026-10-23'),('expiry','2026-10-31'),
    ('observed_at','2026-10-21T20:00:00+00:00'), ('underlying_price',float('nan')),
    ('strike_status','verified listed'), ('premium',1.0), ('max_loss',500)])
def test_rejects_unsupported_candidate(field,value):
    data=bundle();data['candidates'][0][field]=value
    with pytest.raises(ValueError): validate_ideas(data)


def test_shortfall_and_performance_evidence():
    data=bundle();data['shortfall_reason']=''
    with pytest.raises(ValueError): validate_ideas(data)
    data=bundle();data['candidates'][0]['outside_commentary']=dict(
        post_url='https://x.com/test/status/123',posted_at='2026-10-22T16:00:00+00:00',
        author='Fixture',excerpt='Test',quote_or_paraphrase='paraphrase',credibility='unverified',
        own_assessment='No track record established',performance_claim='90% win rate')
    with pytest.raises(ValueError): validate_ideas(data)
    del data['candidates'][0]['outside_commentary']['performance_claim']
    text=render_ideas(data)
    assert 'Outside commentary:' in text and 'Own assessment:' in text


def test_truthful_zero_idea_edition():
    data=bundle();data['candidates']=[]
    assert 'supported: 0' in render_ideas(data)
    data['max_loss_cap']={'amount':100, 'currency':'USD'}
    assert '100 USD configured, NOT certified' in render_ideas(data)


def test_authorized_caps_render_and_validate():
    data=bundle();data['risk_caps']={'currency':'USD','spx':1000,'other':500}
    text=render_ideas(data)
    assert 'USD 1,000 per SPX' in text and 'USD 500' in text
    assert 'UNSET' not in text
    data['risk_caps']['other']=1000
    with pytest.raises(ValueError): validate_ideas(data)


def test_separate_eastern_and_closing_owners():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    closing=(root/'automation/DAILY_TASK_PROMPT.md').read_text()
    prompt=(root/'automation/TRADE_IDEAS_1500_TASK_PROMPT.md').read_text()
    assert 'git merge --ff-only origin/main' in closing
    assert 'validated Daily completion marker' in closing
    assert 'must never create, regenerate or' in closing
    assert '15:00 America/New_York' in prompt
    assert "Daily's marker is independent" in prompt
    assert 'future' in prompt and 'USER selects expiries' in prompt
