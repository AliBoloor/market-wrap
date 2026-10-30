"""Horizon-first technical short-condor maps; no expiry selection or pricing."""
from datetime import date
from html import escape
from zoneinfo import ZoneInfo
import math
import yaml
from .models import _parse_time

UNIVERSE = ('SPX','QQQ','IWM','TLT','GLD')
HORIZONS = ('next-session','one-week','one-month')


def eligibility(now, *, session, next_session, is_trading_day, completed):
    if now.tzinfo is None:raise ValueError('timezone-aware current time required')
    eastern=now.astimezone(ZoneInfo('America/New_York'))
    if eastern.date()!=session:return False,'current New York session only; no silent backfill'
    if not is_trading_day or session.weekday()>4:return False,'exchange closed'
    if (eastern.hour,eastern.minute,eastern.second)<(15,0,0):return False,'before 15:00 America/New_York'
    if next_session<=session:return False,'next verified exchange session required'
    if completed:return False,'Trade Ideas date already validated'
    return True,'15:00 Eastern refresh eligible; label actual session state'


def validate_bundle(b):
    session=date.fromisoformat(b['trading_date']);target=date.fromisoformat(b['next_session'])
    generated=_parse_time(b['generated_at']);cutoff=_parse_time(b['research_cutoff']).astimezone(ZoneInfo('America/New_York'));observed=_parse_time(b['data_observed_at'])
    hour=16 if b['publication_mode']=='close-initial' else 15
    if cutoff.date()!=session or (cutoff.hour,cutoff.minute,cutoff.second)!=(hour,0,0):raise ValueError('explicit close-initial or 15:00 Eastern cutoff required')
    if observed>cutoff or generated<cutoff or observed.astimezone(ZoneInfo('America/New_York')).date()!=session:raise ValueError('no future observations or closing lookahead')
    if target<=session or not b['calendar_source'].startswith('https://') or b.get('calendar_verified') is not True:raise ValueError('verified horizon calendar required')
    if b.get('risk_cap_usd')!=500:raise ValueError('conditional fee-inclusive USD 500 entry requirement')
    if [h['id'] for h in b['horizons']]!=list(HORIZONS):raise ValueError('day, week, month horizon definitions required')
    for h in b['horizons']:
        if date.fromisoformat(h['start'])!=target or date.fromisoformat(h['end'])<target or type(h['trading_sessions']) is not int or h['trading_sessions']<1:raise ValueError('explicit calendar/session horizon boundaries required')
    if [t['symbol'] for t in b['tickers']]!=list(UNIVERSE):raise ValueError('fixed five-ticker universe required')
    for t in b['tickers']:
        spot=t['spot']
        if isinstance(spot,bool) or not isinstance(spot,(float,int)) or not math.isfinite(spot) or spot<=0:raise ValueError('actual positive spot reference required')
        if not t['source'].startswith('https://'):raise ValueError('direct technical data source required')
        if [p['horizon'] for p in t['levels']]!=list(HORIZONS):raise ValueError('three per-ticker horizon rows required')
        pairs=[]
        for p in t['levels']:
            put,call=p['short_put'],p['short_call']
            if not all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in (put,call)) or not 5<put<spot<call:raise ValueError('short strikes must bracket spot with positive long put')
            if p.get('long_put')!=put-5 or p.get('long_call')!=call+5:raise ValueError('both wings exactly five points')
            for key in ('basis','support','resistance','upside','downside','range'):
                if not p.get(key):raise ValueError('missing technical scenario evidence '+key)
            if any(key in p for key in ('expiry','premium','max_profit','breakeven')):raise ValueError('technical horizons do not select expiry or invent pricing')
            pairs.append((put,call))
        if len(set(pairs))!=3:raise ValueError('do not copy the same bounds across horizons')


def intrinsic(p,price):
    return max(p['long_put']-price,0)-max(p['short_put']-price,0)-max(price-p['short_call'],0)+max(price-p['long_call'],0)


def conditional_loss(credit,fees):
    if not (math.isfinite(credit) and math.isfinite(fees) and 0<credit<5 and fees>=0):
        raise ValueError('actual positive credit below five and nonnegative fees required')
    return 500-100*credit+fees


def schematic(p,spot):
    """Intrinsic shape with unknown cash-flow offset, spot-centered x scale."""
    strikes=[p['long_put'],p['short_put'],p['short_call'],p['long_call']]
    radius=max(abs(k-spot) for k in strikes)*1.2
    lo=max(0,spot-radius);hi=spot+radius
    x=lambda v:35+430*(v-lo)/(hi-lo)
    y=lambda v:60-22*v
    points=[lo,*strikes,hi]
    path=' '.join(f'{x(s):.2f},{y(intrinsic(p,s)):.2f}' for s in points)
    marks=''.join(f'<line class="condor-strike" x1="{x(k):.2f}" x2="{x(k):.2f}" y1="42" y2="184"/><text class="condor-label" x="{x(k):.2f}" y="{202 if i%2==0 else 236}"><tspan x="{x(k):.2f}">{label}</tspan><tspan x="{x(k):.2f}" dy="14">{k:g}</tspan></text>' for i,(k,label) in enumerate(zip(strikes,['LONG PUT','SHORT PUT','SHORT CALL','LONG CALL'])))
    title=f"Short iron condor shape: long put {strikes[0]:g}, short put {strikes[1]:g}, short call {strikes[2]:g}, long call {strikes[3]:g}; spot {spot:.2f}"
    return f'''<svg class="condor-chart" viewBox="0 0 500 280" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><desc>Shape before unknown credit and fees. Four dashed strike lines and labeled axis ticks; blue center line marks the actual spot reference. Technical horizon is not option expiry.</desc><text x="35" y="20">Shape only · unknown credit shifts curve vertically</text><line class="condor-axis" x1="35" x2="465" y1="184" y2="184"/>{marks}<polyline class="condor-payoff" points="{path}"/><line class="condor-spot" x1="{x(spot):.2f}" x2="{x(spot):.2f}" y1="28" y2="184"/><circle class="condor-spot-dot" cx="{x(spot):.2f}" cy="60" r="4"/><text class="condor-spot-label" x="{x(spot):.2f}" y="34">SPOT {spot:.2f}</text><text x="170" y="276">Underlying price / strike</text></svg>'''


def render_bundle(b):
    validate_bundle(b)
    first=b['publication_mode']=='close-initial'
    meta=dict(report_family='trade-ideas',trading_date=b['trading_date'],title='Technical Iron Condors · Day / Week / Month',report_type='Trade Ideas',generated_at=b['generated_at'],data_observed_at=b['data_observed_at'],freshness='Completed-close first edition' if first else '15:00 Eastern intraday research',completeness='Five tickers · three technical horizons · unpriced schematic legs')
    out='---\n'+yaml.safe_dump(meta,sort_keys=False)+'---\n\n'
    out+=f"**Research session: {b['trading_date']} · Next session: {b['next_session']} · {'First edition: completed 16:00 New York close' if first else 'Recurring 15:00 America/New_York cutoff'}.**\n\nResearch cutoff: {b['research_cutoff']}. Generated: {b['generated_at']}. Latest baseline observation: {b['data_observed_at']}.\n\n"
    out+='**Short iron condors only · both wings five points · one standard 100-multiplier package.** These are technical level sets, not selected option expirations or verified listed contracts.\n\n'
    out+='| Technical horizon | Window | Trading sessions |\n|---|---|---:|\n'
    for h in b['horizons']:out+=f"| {h['label']} | {h['start']} → {h['end']} | {h['trading_sessions']} |\n"
    out+='\n'+b['calendar_note']+'\n\n'+b['research']+'\n\n'
    for t in b['tickers']:
        out+=f'<section class="condor-ticker"><header><h2>{t["symbol"]}</h2><p>Spot reference <strong>{t["spot"]:.2f}</strong> · <a href="{escape(t["source"],quote=True)}">Daily price inputs</a> · retrieved {escape(t["retrieved_at"])}</p></header>'
        out+=f'<p class="condor-trend">{escape(t["trend"])}</p>'
        for p in t['levels']:
            h=next(h for h in b['horizons'] if h['id']==p['horizon'])
            out+=f'''<div class="condor-row"><div class="condor-copy"><h3>{escape(h['label'])}</h3><p class="condor-window">{h['start']} → {h['end']}</p><p class="condor-legs"><strong>SHORT {p['short_call']:g} CALL</strong> / <strong>LONG {p['long_call']:g} CALL</strong><br><strong>SHORT {p['short_put']:g} PUT</strong> / <strong>LONG {p['long_put']:g} PUT</strong></p><p><b>Support:</b> {escape(p['support'])}<br><b>Resistance:</b> {escape(p['resistance'])}</p><p>{escape(p['basis'])}</p><details><summary>Upside, downside and range conditions</summary><p><b>Upside:</b> {escape(p['upside'])}</p><p><b>Downside:</b> {escape(p['downside'])}</p><p><b>Range:</b> {escape(p['range'])}</p></details></div><div class="condor-visual">{schematic(p,t['spot'])}</div></div>'''
        out+=f'<p class="condor-gamma"><b>Gamma context:</b> {escape(t["gamma_note"])}</p></section>\n\n'
    out+='''## Shared schematic and risk notes

The curve shows signed intrinsic shape before entry cash flow, shifted vertically
by the unknown credit and costs. It is an expiry-payoff schematic for whatever
same-expiry package you select—not a forecast of P&L on the technical horizon.
Pre-expiry value also depends on remaining time and implied volatility. No net
profit, exact breakeven or executable premium is invented. You select expiries;
all proposed technical strikes require a listing/deliverable/liquidity check.

With five-point wings, one 100-multiplier intact package has modeled maximum
expiry loss **500 − 100C + F**, where C is net credit in points and F is actual
all-in USD costs. The **$500 conditional entry requirement** needs 0<C<5 and
100C≥F. Unknown credit/fees means eligibility is unconfirmed, not a guaranteed
account-loss limit. ETF assignment/pin/after-hours residual-stock risk can exceed
the intact-package model; execute/manage the complete package. SPX requires
exact AM/PM settlement and contract verification. No naked legging or broker orders.

'''
    out+='## Evidence and methodology\n\n'+b['methods']+'\n\n'+b['sources']+'\n\n'+b['limitations']+'\n'
    return out
