"""Expiry vertical-spread mathematics and accessible what-if profiles.

Settlement payoff excludes entry cash flow and fees. P&L includes both. Inputs
are illustrative assumptions, never option-chain observations or fill quotes.
"""
from __future__ import annotations

import html
import json
import math


def validate_profile(p: dict) -> None:
    if p.get('option_type') not in ('call', 'put') or p.get('kind') not in ('debit', 'credit'):
        raise ValueError('profile requires call/put and debit/credit')
    for key in ('long_strike', 'short_strike', 'premium', 'fees', 'quantity', 'multiplier'):
        value=p.get(key)
        if isinstance(value, bool) or not isinstance(value, (int,float)) or not math.isfinite(value):
            raise ValueError(f'profile {key} must be finite')
    width=abs(p['long_strike']-p['short_strike'])
    if min(p['long_strike'],p['short_strike']) <= 0 or width == 0:
        raise ValueError('profile strikes must be distinct and positive')
    debit = p['long_strike'] < p['short_strike'] if p['option_type']=='call' else p['long_strike'] > p['short_strike']
    if debit != (p['kind']=='debit'):
        raise ValueError('profile leg ordering conflicts with debit/credit kind')
    if not 0 <= p['premium'] <= width or p['fees'] < 0:
        raise ValueError('premium must be within spread width; fees nonnegative')
    if any(p[k] < 1 or int(p[k]) != p[k] for k in ('quantity','multiplier')):
        raise ValueError('quantity and multiplier must be positive integers')
    if p.get('assumption_status') != 'illustrative':
        raise ValueError('this what-if renderer accepts illustrative assumptions only')


def expiry_payoff(p: dict, price: float) -> float:
    """Signed intrinsic settlement value for the two legs, before entry/fees."""
    sign=1 if p['option_type']=='call' else -1
    intrinsic=lambda strike: max(sign*(price-strike),0)
    return (intrinsic(p['long_strike'])-intrinsic(p['short_strike']))*p['quantity']*p['multiplier']


def expiry_pnl(p: dict, price: float) -> float:
    entry=p['premium']*p['quantity']*p['multiplier']*(1 if p['kind']=='credit' else -1)
    return expiry_payoff(p,price)+entry-p['fees']


def profile_summary(p: dict) -> dict:
    validate_profile(p)
    low,high=sorted((p['long_strike'],p['short_strike']))
    a,b=expiry_pnl(p,low),expiry_pnl(p,high)
    worst,best=min(a,b),max(a,b)
    zero=None
    if a*b < 0:
        zero={'type':'point','value':low-a*(high-low)/(b-a)}
    elif abs(a)<1e-9:
        zero={'type':'region','minimum':0,'maximum':low}
    elif abs(b)<1e-9:
        zero={'type':'region','minimum':high,'maximum':None}
    return dict(best=best,worst=worst,max_profit=max(0,best),max_loss=max(0,-worst),breakeven=zero)


def breakeven_text(zero: dict | None) -> str:
    if zero is None:
        return 'None under these assumptions'
    if zero['type']=='point':
        return f"{zero['value']:.2f}"
    if zero['maximum'] is None:
        return f"Underlying ≥ {zero['minimum']:.2f} (zero-P&L region)"
    return f"Underlying 0–{zero['maximum']:.2f} (zero-P&L region)"


def render_svg(p: dict) -> str:
    """Static fallback chart, also repainted by the browser after input changes."""
    summary=profile_summary(p)
    low,high=sorted((p['long_strike'],p['short_strike']))
    width=high-low
    xs=[max(0,low-width),low,high,high+width]
    values=[expiry_pnl(p,x) for x in xs]+[expiry_payoff(p,x) for x in xs]+[0]
    bottom,top=min(values),max(values)
    pad=max((top-bottom)*.15,1);bottom-=pad;top+=pad
    x=lambda v: 56+(v-xs[0])/(xs[-1]-xs[0])*370
    y=lambda v: 208-(v-bottom)/(top-bottom)*170
    path=lambda fn:' '.join(('M' if i==0 else 'L')+f'{x(v):.2f},{y(fn(p,v)):.2f}' for i,v in enumerate(xs))
    label=f"Expiry P&L and signed settlement payoff; illustrative {p['kind']} {p['option_type']} vertical"
    return f'''<svg class="pnl-chart" viewBox="0 0 480 270" role="img" aria-label="{label}">
<title>{label}</title><desc>Blue solid line includes entry premium and fees. Gray dashed line excludes both. Values are USD for the entire assumed position.</desc>
<line class="pnl-axis" x1="56" y1="{y(0):.2f}" x2="426" y2="{y(0):.2f}"/>
<path class="payoff-line" d="{path(expiry_payoff)}"/><path class="pnl-line" d="{path(expiry_pnl)}"/>
<text x="8" y="24">USD / position</text><text data-label="top" x="4" y="52">{top:.0f}</text><text data-label="bottom" x="4" y="210">{bottom:.0f}</text>
<text x="56" y="232">{xs[0]:.2f}</text><text x="379" y="232">{xs[-1]:.2f}</text>
<text x="168" y="258">Underlying at expiry</text></svg>'''


def render_profile(p: dict, *, expiry: str, cap: float | None) -> str:
    summary=profile_summary(p)
    payload=html.escape(json.dumps(dict(p,cap=cap)),quote=True)
    cap_text='Unset' if cap is None else f'USD {cap:,.0f}'
    comparison='Cap unset' if cap is None else ('Within model cap' if summary['max_loss']<=cap else 'Exceeds model cap')
    method_slug = 'bull-call-spread-debit-call-spread' if p['option_type']=='call' and p['kind']=='debit' else 'bear-call-spread-credit-call-spread' if p['option_type']=='call' else 'bear-put-spread' if p['kind']=='debit' else 'bull-put-spread-credit-put-spread'
    inputs=''.join(f'<label>{label}<input type="number" data-field="{key}" value="{p[key]:g}" min="{minimum}" step="{step}" inputmode="decimal"></label>' for key,label,minimum,step in (
        ('premium',f"Assumed {p['kind']} (points/share)",0,'.01'),('fees','Assumed total fees (USD)',0,'.01'),
        ('quantity','Spread quantity',1,'1'),('multiplier','Assumed multiplier',1,'1')))
    return f'''<section class="pnl-profile" data-profile="{payload}" aria-label="Illustrative expiry P&amp;L profile">
<h3>Expiry P&amp;L profile · what-if model</h3>
<p class="pnl-assumption"><strong>ILLUSTRATIVE — no entry quote or listed contracts verified.</strong> Initial premium is {p["premium"]:g} points/share, a chosen modeling assumption, not a market estimate. Initial total fees assume USD {p["fees"]:g}; actual fees are unknown. Change the inputs below; all results remain hypothetical.</p>
<p>Buy 1 {p['option_type']} at {p['long_strike']:g}; sell 1 {p['option_type']} at {p['short_strike']:g}, per spread. Both legs expire {html.escape(expiry)}. Premium is per underlying point/share; fees are the all-in USD total for the entire position, not per contract.</p>
<div class="pnl-inputs">{inputs}</div>
<p class="pnl-legend"><span class="pnl-key">Solid blue: expiry P&amp;L</span> · Dashed gray: signed settlement payoff before entry premium and fees</p>
<div class="pnl-plot">{render_svg(p)}</div>
<dl class="pnl-results" aria-live="polite">
<div><dt>Maximum model gain</dt><dd data-result="profit">USD {summary['max_profit']:.2f}</dd></div>
<div><dt>Maximum model loss</dt><dd data-result="loss">USD {summary['max_loss']:.2f}</dd></div>
<div><dt>Breakeven at expiry</dt><dd data-result="breakeven">{breakeven_text(summary['breakeven'])}</dd></div>
<div><dt>Configured per-trade cap</dt><dd>{cap_text}</dd></div></dl>
<p data-result="eligibility">{comparison} under assumed premium, quantity, multiplier and fees; <strong>executable eligibility UNVERIFIED.</strong></p>
<p data-result="regime">{"All modeled expiry outcomes lose money." if summary["best"]<0 else ""}</p>
<p data-result="error" role="alert"></p>
<details><summary>Payoff and P&amp;L calculation</summary><p>Signed payoff = quantity × multiplier × (long intrinsic − short intrinsic). Expiry P&amp;L = payoff {'+' if p['kind']=='credit' else '−'} quantity × multiplier × {p['kind']} premium − total fees. A debit vertical's loss is debit × quantity × multiplier + fees; a credit vertical's loss is (width − credit) × quantity × multiplier + fees. The chart does not model pre-expiry value, volatility, slippage, early exercise or assignment. ETF/single-name physical exercise can create exposure beyond this idealized paired-leg model; manage both legs together and verify contract terms.</p></details>
<p><a href="https://www.optionseducation.org/strategies/all-strategies/{method_slug}">Options Industry Council: strategy payoff reference</a></p>
<noscript>JavaScript is off: this static chart shows the labeled initial assumptions; inputs will not recalculate.</noscript></section>'''
