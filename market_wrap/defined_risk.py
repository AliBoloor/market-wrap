"""Version-two policy: three paired-leg families; parametric, not quoted, risk."""
from datetime import date
from html import escape
from zoneinfo import ZoneInfo
import math
import yaml
from .models import _parse_time

FAMILIES = ('call_vertical', 'put_vertical', 'iron_condor')
SYMBOLS = ('SPX', 'QQQ', 'IWM', 'GLD', 'TLT', 'XLK', 'XLF', 'XLE', 'XLI', 'XLV')


def legs(p):
    k=p['strikes']
    if p['family']=='iron_condor':
        # Long iron condor buys inner put/call, sells outer put/call (debit).
        # Short iron condor reverses every leg (credit).
        s=1 if p['kind']=='credit' else -1
        return [('put',k[0],s),('put',k[1],-s),('call',k[2],-s),('call',k[3],s)]
    option='call' if p['family']=='call_vertical' else 'put'
    low_long=(option=='call')==(p['kind']=='debit')
    return [(option,k[0],1 if low_long else -1),(option,k[1],-1 if low_long else 1)]


def validate_structure(p):
    if p.get('family') not in FAMILIES or p.get('kind') not in ('debit','credit'):
        raise ValueError('only call vertical, put vertical or iron condor; debit/credit required')
    k=p.get('strikes',[])
    if len(k)!=(4 if p['family']=='iron_condor' else 2) or any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<=0 for x in k) or any(a>=b for a,b in zip(k,k[1:])):
        raise ValueError('strikes must be positive, finite and strictly increasing')
    if p.get('multiplier')!=100 or type(p.get('quantity')) is not int or p['quantity']<1:
        raise ValueError('standard multiplier 100 and positive integer quantity required')
    if p['family']=='iron_condor' and not math.isclose(k[1]-k[0],k[3]-k[2]):
        raise ValueError('iron condor requires equal-width wings')


def intrinsic(p,price):
    return sum(sign*max((price-k) if option=='call' else (k-price),0) for option,k,sign in legs(p))


def pnl(p,price,premium,fees):
    validate_structure(p)
    if not 0<=premium<=width(p) or fees<0 or not all(math.isfinite(x) for x in (premium,fees)):
        raise ValueError('invalid hypothetical premium or fees')
    return 100*p['quantity']*(intrinsic(p,price)+(premium if p['kind']=='credit' else -premium))-fees


def width(p):
    return p['strikes'][1]-p['strikes'][0]


def bounds(p,premium,fees):
    values=[pnl(p,s,premium,fees) for s in [0,*p['strikes'],p['strikes'][-1]+width(p)]]
    return min(values),max(values)


def validate_bundle(b):
    session=date.fromisoformat(b['trading_date']); target=date.fromisoformat(b['next_session'])
    generated=_parse_time(b['generated_at'])
    observed=_parse_time(b['data_observed_at'])
    if observed>generated or observed.astimezone(ZoneInfo('America/New_York')).date()!=session:
        raise ValueError('current-session observation required; no future data')
    if b.get('publication_mode') == 'noon':
        from .noon import eligibility
        scheduled=_parse_time(b['scheduled_for']).astimezone(ZoneInfo('America/Vancouver'))
        allowed,reason=eligibility(generated,session=session,next_session=target,
            is_trading_day=b.get('calendar_verified') is True,completed=False)
        if not allowed or scheduled.date()!=session or scheduled.hour!=12 or scheduled.minute!=0 or scheduled.second!=0:
            raise ValueError('invalid noon timing/calendar: '+reason)
    if target<=session or not b['calendar_source'].startswith('https://'):
        raise ValueError('verified next-session calendar required')
    if b.get('risk_caps')!={'currency':'USD','spx':500,'other':500}:
        raise ValueError('all positions capped at USD 500 including explicit fees')
    if not b.get('research') or not b.get('social_coverage') or len(b['candidates'])>6:
        raise ValueError('research, coverage and compact candidate set required')
    ids=set()
    for c in b['candidates']:
        if c['id'] in ids or c['symbol'] not in SYMBOLS:
            raise ValueError('duplicate ID or unsupported symbol')
        ids.add(c['id']);validate_structure(c['model'])
        if not 0 <= (date.fromisoformat(c['expiry'])-target).days<=7:
            raise ValueError('expiration must be 0–7 calendar days from target session')
        for key in ('direction','volatility_view','level_basis','trigger','invalidation','alternative','listing_status','listing_source'):
            if not c.get(key):raise ValueError(f'missing {key}')
        if not c['listing_source'].startswith('https://'):raise ValueError('listing evidence source required')
        if c['listing_status'] not in ('desired; contracts unverified','verified listed'):
            raise ValueError('explicit listing status required')
        if c['listing_status']=='verified listed' and not c.get('contract_identifiers'):
            raise ValueError('exact contracts required for verified listing')
        if c.get('premium') is not None or c.get('fees') is not None:
            raise ValueError('v2 research uses UNKNOWN premium/fees; no invented entry risk')


def schematic(p):
    """Signed intrinsic-only diagram: no invented premium or breakeven."""
    k=p['strikes'];w=width(p);xs=[max(0,k[0]-w),*k,k[-1]+w]
    ys=[intrinsic(p,x)*100*p['quantity'] for x in xs]
    lo,hi=min(ys),max(ys);span=max(hi-lo,1)
    coords=' '.join(f'{45+390*(x-xs[0])/(xs[-1]-xs[0]):.2f},{190-140*(y-lo)/span:.2f}' for x,y in zip(xs,ys))
    return f'<svg viewBox="0 0 480 240" role="img" aria-label="Signed intrinsic payoff before unknown premium and fees"><title>Signed intrinsic payoff only; not net profit</title><polyline points="{coords}" fill="none" stroke="currentColor" stroke-width="3"/><text x="35" y="25">Intrinsic USD: {lo:g} to {hi:g}</text><text x="35" y="215">Underlying at expiry: {xs[0]:g} to {xs[-1]:g}</text></svg>'


def profile(p):
    q=p['quantity'];w=width(p);n=100*q
    legtext='; '.join(f'{"Buy" if sign==1 else "Sell"} {q} {option} {k:g}' for option,k,sign in legs(p))
    if p['kind']=='debit':
        formula=f'Max loss = {n}D + F; max profit = {n}({w:g} − D) − F. Admissible debit: 0 &lt; D &lt; {w:g}, D ≤ (500 − F)/{n}.'
    else:
        formula=f'Max loss = {n}({w:g} − C) + F; max profit = {n}C − F. Admissible credit: 0 &lt; C &lt; {w:g}, C ≥ {w:g} − (500 − F)/{n}.'
    if p['family']=='iron_condor':
        k=p['strikes'];be=f'{k[1]:g} − (C − F/{n}) and {k[2]:g} + (C − F/{n})' if p['kind']=='credit' else f'{k[0]:g} + (D + F/{n}) and {k[3]:g} − (D + F/{n})'
    else:
        k=p['strikes'];up=(p['family']=='call_vertical')==(p['kind']=='debit')
        base=k[0] if p['family']=='call_vertical' else k[1]
        effective=f'D + F/{n}' if p['kind']=='debit' else f'C − F/{n}'
        be=f'{base:g} {"+" if p["family"]=="call_vertical" else "−"} ({effective})'
    return f'''<section class="pnl-profile"><h3>{escape(p['kind'])} {escape(p['family'].replace('_',' '))} · schematic</h3><p>{legtext}. Same expiry; standard multiplier 100.</p><p><strong>Entry premium UNKNOWN. All-in fees UNKNOWN. Entry risk conditional; no executable eligibility confirmed.</strong></p>{schematic(p)}<p>D = net debit, C = net credit in points/share; F = actual all-position USD fees including expected closing/exercise costs. Quantity q = {q}. {formula} Require F &lt; 500 and a positive integer q satisfying the inequality; otherwise no trade.</p><p>Parametric breakeven: {be}, only if the result falls inside its sloping wing; sufficiently large fees can remove breakevens. No exact net profit, loss or breakeven is quoted. Intrinsic chart excludes entry cash flow and fees.</p></section>'''


def render_bundle(b):
    validate_bundle(b)
    meta=dict(report_family='trade-ideas',trading_date=b['trading_date'],title=f"Trade Ideas for {b['next_session']}",report_type='Trade Ideas',generated_at=b['generated_at'],data_observed_at=b['data_observed_at'],freshness='Intraday noon refresh; source delays explicit' if b.get('publication_mode')=='noon' else 'Completed close; post-close context separately timed',completeness='Conditional research; contracts and entry premiums unverified')
    out='---\n'+yaml.safe_dump(meta,sort_keys=False)+'---\n\n'
    baseline="Intraday baseline" if b.get("publication_mode")=="noon" else "Closing baseline"
    out+=f"**Target session: {b['next_session']} · {baseline}: {b['trading_date']} · All times New York unless stated.**\n\n"
    if b.get('publication_mode')=='noon':
        out+=f"Requested refresh start: **12:00 America/Vancouver**, scheduled {b['scheduled_for']}. Actual generation: {b['generated_at']}; latest observation: {b['data_observed_at']}. This is intraday research, not a completed-session close. Publication follows research and validation; timing can be delayed.\n\n"
    entry_label='Entry requirement: modeled loss of the intact package must be ≤ USD 500 including actual all-in fees. Eligibility is conditional until entry inputs are verified. Never naked options.' if b.get('publication_mode')=='noon' else 'USD 500 maximum loss per position including actual all-in fees. Never naked options.'
    out+=f'Only three families: **call vertical, put vertical, iron condor**. Each supports debit/credit variations. **{entry_label}** Candidates are alternatives, not a portfolio or orders.\n\n'
    out+=b['research']+'\n\n'
    out+='## Conditional next-session setups\n\n'
    for c in b['candidates']:
        out+=f"### {c['symbol']} · {c['direction']}\n\n"
        for key in ('volatility_view','level_basis','trigger','invalidation','alternative'):
            out+=f"**{key.replace('_',' ').title()}:** {c[key]}\n\n"
        out+=f"**Desired expiration:** {c['expiry']}. **Listing:** {c['listing_status']}. [Listing verification source]({c['listing_source']}). {c.get('listing_note','')}\n\n"
        out+=profile(c['model'])+'\n\n'
    out+='## Family selection and risk gates\n\nBullish + expansion: debit call vertical; bullish + stabilization/contraction: credit put vertical. Bearish + expansion: debit put vertical; bearish + rejection/contraction: credit call vertical. Range + contraction: short iron condor (credit: buy outer wings, sell inner put/call). Large move either direction + expansion: long iron condor (debit: buy inner put/call, sell outer wings). Equal wings, ordered put wing below call wing, one expiry and matched quantities; reversing every leg reverses signed intrinsic payoff. Unknown implied volatility means these are conditional volatility views, never claims that options are cheap or rich.\n\n'
    out+='No trade before confirmation, during unresolved release reaction, on a gap beyond the map without a new range, or without actual listed legs, liquidity, premium, fees and $500 sizing checks. Stops do not define maximum loss. Paired-leg expiry mathematics assumes both legs remain paired: ETF options are American exercise and physically settled; early assignment/pin risk can create stock exposure. Close/manage all legs together before expiry. SPXW is European/cash settled; select PM series explicitly and verify the last trading time, not AM-settled standard SPX. No broker connection or orders.\n\n'
    out+='## Public commentary and limitations\n\n'+b['social_coverage']+'\n\n'+b.get('limitations','')+'\n\n'
    out+='## Sources and observation record\n\n'+b['sources']+'\n'
    return out
