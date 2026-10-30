from copy import deepcopy
from datetime import datetime,date
from pathlib import Path
import json
import pytest
from market_wrap.condor import eligibility,validate_bundle,render_bundle,schematic,intrinsic,conditional_loss


def bundle():
    root=Path(__file__).resolve().parents[1]
    return json.loads((root/'data/trade-ideas/2026-10-29/ideas.json').read_text())


def test_five_wide_blocks_fifteen_rows_and_labeled_shapes():
    b=bundle();validate_bundle(b);s=render_bundle(b)
    assert s.count('class="condor-ticker"')==5
    assert s.count('class="condor-row"')==15
    assert s.count('class="condor-strike"')==60
    assert s.count('class="condor-spot"')==15
    assert s.count('<strong>SHORT ')==30 and s.count('<strong>LONG ')==30
    assert 'expiry-payoff schematic' in s and 'No net' in s
    for t in b['tickers']:
        for p in t['levels']:
            assert p['short_put']-p['long_put']==5 and p['long_call']-p['short_call']==5
            assert p['short_put']<t['spot']<p['short_call']
            assert intrinsic(p,p['long_put']-10)==-5
            assert intrinsic(p,t['spot'])==0
            assert intrinsic(p,p['long_call']+10)==-5
            svg=schematic(p,t['spot'])
            for k in ['long_put','short_put','short_call','long_call']:assert f'>{p[k]:g}</tspan>' in svg


def test_rejects_asymmetry_copied_horizons_expiry_and_lookahead():
    original=bundle()
    bad=deepcopy(original);bad['tickers'][0]['levels'][0]['long_put']-=5
    with pytest.raises(ValueError):validate_bundle(bad)
    bad=deepcopy(original);p=bad['tickers'][0]['levels'][0];p['expiry']='2026-10-30'
    with pytest.raises(ValueError):validate_bundle(bad)
    bad=deepcopy(original);bad['data_observed_at']='2026-10-29T20:00:01+00:00'
    with pytest.raises(ValueError):validate_bundle(bad)
    bad=deepcopy(original);t=bad['tickers'][0]
    for p in t['levels'][1:]:
        for k in ['short_put','long_put','short_call','long_call']:p[k]=t['levels'][0][k]
    with pytest.raises(ValueError):validate_bundle(bad)


def test_credit_fee_boundary():
    assert conditional_loss(.05,5)==500
    assert conditional_loss(.05,5.01)>500
    assert conditional_loss(1,10)==410
    with pytest.raises(ValueError):conditional_loss(0,0)


def test_eastern_schedule_tracks_new_york_dst():
    args=dict(session=date(2026,10,30),next_session=date(2026,11,2),is_trading_day=True,completed=False)
    assert not eligibility(datetime.fromisoformat('2026-10-30T18:59:59+00:00'),**args)[0]
    assert eligibility(datetime.fromisoformat('2026-10-30T19:00:00+00:00'),**args)[0]
    args.update(session=date(2026,11,27),next_session=date(2026,11,30))
    assert not eligibility(datetime.fromisoformat('2026-11-27T19:59:59+00:00'),**args)[0]
    assert eligibility(datetime.fromisoformat('2026-11-27T20:00:00+00:00'),**args)[0]
