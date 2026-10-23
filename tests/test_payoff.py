"""Known payoff boundaries, fees, break-even regions and browser math parity."""
from pathlib import Path
import json
import shutil
import subprocess
import pytest
from market_wrap.payoff import expiry_payoff, expiry_pnl, profile_summary, render_profile, validate_profile


def profile(option='call', kind='debit'):
    low_long=(option=='call')==(kind=='debit')
    return dict(option_type=option,kind=kind,long_strike=100 if low_long else 105,
        short_strike=105 if low_long else 100,premium=2,fees=5,quantity=1,multiplier=100,
        assumption_status='illustrative')


@pytest.mark.parametrize('option,kind,best,worst,be',[
    ('call','debit',295,-205,102.05),('put','debit',295,-205,102.95),
    ('call','credit',195,-305,101.95),('put','credit',195,-305,103.05)])
def test_known_vertical_bounds_and_breakeven(option,kind,best,worst,be):
    p=profile(option,kind);s=profile_summary(p)
    assert s['best']==best and s['worst']==worst
    assert s['breakeven']['value']==pytest.approx(be)
    assert expiry_pnl(p,be)==pytest.approx(0)
    for price in (0,90,100,102,105,110,10000):
        assert worst<=expiry_pnl(p,price)<=best
    assert expiry_payoff(p,110) != expiry_pnl(p,110)


def test_fees_and_quantity_do_not_get_conflated():
    p=profile();p.update(quantity=3,fees=7)
    s=profile_summary(p)
    assert s['max_loss']==607 and s['max_profit']==893
    assert s['breakeven']['value']==pytest.approx(102+7/300)
    p['fees']=2000
    assert profile_summary(p)['max_profit']==0
    assert profile_summary(p)['breakeven'] is None


def test_zero_regions_and_invalid_assumptions():
    p=profile();p.update(premium=0,fees=0)
    assert profile_summary(p)['breakeven']==dict(type='region',minimum=0,maximum=100)
    p['premium']=5
    assert profile_summary(p)['breakeven']==dict(type='region',minimum=105,maximum=None)
    for key,value in [('premium',6),('fees',-1),('quantity',1.5),('multiplier',0),('premium',float('nan'))]:
        bad=profile();bad[key]=value
        with pytest.raises(ValueError):validate_profile(bad)


def test_static_profile_is_accessible_and_explicitly_illustrative():
    text=render_profile(profile(),expiry='2026-10-30',cap=500)
    assert 'ILLUSTRATIVE' in text and 'UNVERIFIED' in text
    assert 'viewBox="0 0 480 270"' in text
    assert 'role="img"' in text and '<desc>' in text
    assert 'USD 205.00' in text and '102.05' in text
    assert 'noscript' in text and 'Assumed total fees' in text


def test_browser_math_and_chart_paths_match_python():
    node=shutil.which('node')
    if not node:pytest.skip('Node runtime unavailable for JS parity check')
    script=Path(__file__).resolve().parents[1]/'market_wrap/static/pnl.js'
    data=[profile(option,kind) for option in ('call','put') for kind in ('debit','credit')]
    data += [dict(profile(),quantity=12,fees=20),dict(profile(),premium=0,fees=0),dict(profile(),fees=600)]
    code="const fs=require('fs');const m=require(process.argv[1]);const data=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(data.map(p=>({summary:m.summary(p),chart:m.chart(p),samples:[0,100,102,105,110].map(x=>m.pnl(p,x))}))));"
    result=subprocess.run([node,'-e',code,str(script)],input=json.dumps(data),text=True,capture_output=True,check=True)
    for p,row in zip(data,json.loads(result.stdout)):
        s=profile_summary(p)
        assert row['summary']==s
        assert row['samples']==pytest.approx([expiry_pnl(p,x) for x in (0,100,102,105,110)])
        if p['premium'] or p['fees']:
            assert row['chart']['pnl_path'] != row['chart']['payoff_path']
        else:
            assert row['chart']['pnl_path'] == row['chart']['payoff_path']
        assert 'NaN' not in row['chart']['pnl_path']
