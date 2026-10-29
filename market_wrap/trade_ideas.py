"""Evidence-first Trade Ideas rendering for the existing daily research task.

Inputs are researcher-supplied public observations, never a historical database
or generated pricing. No broker integration and no automatic contract selection.
"""
from __future__ import annotations

import json
import math
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from .models import _parse_time
from .payoff import validate_profile, render_profile


def _url(value: str) -> bool:
    return isinstance(value, str) and value.startswith('https://')


def validate_ideas(bundle: dict) -> None:
    if bundle.get('policy_version') == 2:
        from .defined_risk import validate_bundle
        return validate_bundle(bundle)
    session = date.fromisoformat(bundle['trading_date'])
    target = date.fromisoformat(bundle['next_session'])
    generated = _parse_time(bundle['generated_at'])
    if target <= session or not _url(bundle['calendar_source']):
        raise ValueError('verified next-session calendar date/source required')
    caps = bundle.get('risk_caps')
    if caps is not None and (caps.get('currency') != 'USD' or caps.get('spx') != 1000 or caps.get('other') != 500):
        raise ValueError('authorized risk caps are USD 1000 SPX / USD 500 others')
    cap = bundle.get('max_loss_cap')
    if cap is not None and (not isinstance(cap, dict) or not cap.get('currency')
            or not isinstance(cap.get('amount'), (float, int))
            or not math.isfinite(cap['amount']) or cap['amount'] <= 0):
        raise ValueError('cap requires a positive amount and explicit currency')
    ideas = bundle['candidates']
    if len(ideas) > 10 or (len(ideas) < 10 and not bundle.get('shortfall_reason')):
        raise ValueError('target ten; fewer require an explicit evidence shortfall')
    if not bundle.get('social_coverage'):
        raise ValueError('state X search coverage and access limitations')
    ids = set()
    for idea in ideas:
        if idea['id'] in ids:
            raise ValueError('duplicate candidate')
        ids.add(idea['id'])
        for field in ('symbol', 'instrument', 'thesis', 'trigger', 'invalidation', 'no_trade', 'structure', 'level_basis'):
            if not idea.get(field):
                raise ValueError(f'missing {field}')
        dte = (date.fromisoformat(idea['expiry']) - target).days
        if not 1 <= dte <= 7:
            raise ValueError('Trade Ideas requires 1–7 calendar DTE from next session; SPX 0DTE is separate')
        observed = _parse_time(idea['observed_at'])
        if observed.astimezone(ZoneInfo('America/New_York')).date() != session or observed > generated:
            raise ValueError('candidate needs current-session observation, no future or stale quote')
        price = idea['underlying_price']
        if not isinstance(price, (int, float)) or not math.isfinite(price) or price <= 0 or not _url(idea['market_source']):
            raise ValueError('actual positive underlying observation and direct market source required')
        if idea['strike_status'] not in ('illustrative', 'verified listed'):
            raise ValueError('strike status must distinguish illustrative from verified listed')
        if idea['strike_status'] == 'verified listed':
            if not _url(idea.get('chain_source', '')) or not idea.get('contract_identifiers'):
                raise ValueError('listed contracts require chain source and exact identifiers')
            chain_time = _parse_time(idea['chain_observed_at'])
            if chain_time > generated or chain_time.astimezone(ZoneInfo('America/New_York')).date() != session:
                raise ValueError('chain evidence must be current-session and not future')
        profile=idea.get('payoff_profile')
        if profile is None:
            raise ValueError('every candidate requires a structured expiry payoff profile')
        validate_profile(profile)
        if profile.get('expiry') != idea['expiry']:
            raise ValueError('profile legs must share the candidate expiry')
        social = idea.get('outside_commentary')
        if social:
            if not _url(social['post_url']) or not any(host in social['post_url'] for host in ('://x.com/', '://twitter.com/')):
                raise ValueError('outside commentary needs original X/Twitter post link')
            _parse_time(social['posted_at'])
            for field in ('author', 'excerpt', 'quote_or_paraphrase', 'credibility', 'own_assessment'):
                if not social.get(field):
                    raise ValueError(f'outside commentary missing {field}')
            if social.get('performance_claim') and not _url(social.get('independent_performance_source', '')):
                raise ValueError('performance claims need independent substantiation')
        # Pricing is not accepted as a casual prose field; exact risk requires a
        # reviewed contemporaneous chain/fees calculation beyond this renderer.
        if any(key in idea for key in ('premium', 'max_loss', 'cap_certified')):
            raise ValueError('no unverified pricing or cap certification; attach separate sourced risk analysis')


def render_ideas(bundle: dict) -> str:
    if bundle.get('policy_version') == 2:
        from .defined_risk import render_bundle
        return render_bundle(bundle)
    validate_ideas(bundle)
    day = bundle['trading_date']
    observed = max((i['observed_at'] for i in bundle['candidates']), default=bundle['generated_at'])
    count = len(bundle['candidates'])
    metadata = dict(report_family='trade-ideas', trading_date=day, title=f"Trade Ideas for {date.fromisoformat(bundle['next_session']).strftime('%B %d, %Y')}",
        report_type='Trade Ideas', generated_at=bundle['generated_at'], data_observed_at=observed,
        freshness='Current-session evidence' if count else 'No candidate observations',
        completeness=f'{count}/10 supported candidates')
    import yaml
    text = '---\n' + yaml.safe_dump(metadata, sort_keys=False) + '---\n\n'
    cap = bundle.get('max_loss_cap')
    cap_label = ('USD 1,000 per SPX trade; USD 500 per other ETF/single-name trade, including fees when known; NOT certified' if bundle.get('risk_caps') else None)
    if cap_label is None:
        cap_label = f"{cap['amount']} {cap['currency']} configured, NOT certified" if cap else 'UNSET — amount and currency pending clarification'
    text += f'''**Target trading session: {bundle['next_session']} (New York). Data session: {day}.**

Conditional research for {bundle['next_session']}; 1–7 calendar days to expiry from that session.
[Session calendar]({bundle['calendar_source']}). Generated: {bundle['generated_at']}.
Target: 10; supported: {count}. {bundle.get('shortfall_reason', '') or 'No numerical shortfall; chain and social coverage limitations below still apply.'}
Maximum-loss cap: **{cap_label}**. No candidate is certified within a cap.
Exact maximum loss needs actual premium, width, multiplier, quantity and all fees;
refresh opening prices and chains before evaluating any candidate. Illustrative
strikes are level-based hypotheses, not verified listed or executable contracts.
SPX 0DTE remains a separate Daily scenario feature. These are correlated watchlist alternatives, not instructions to hold all simultaneously. Avoid release windows and recheck issuer events/earnings before entry.

X/Twitter coverage: {bundle['social_coverage']}
Outside commentary is attributed opinion; independent assessment follows separately.
No track record is assumed from popularity or self-reported results.

'''
    if bundle.get('presentation_updated_at'):
        _parse_time(bundle['presentation_updated_at'])
        text += f"**P&L profile presentation updated:** {bundle['presentation_updated_at']}. Research observations retain their original dates; this is not a new market-data snapshot.\n\n"
    if bundle.get('catalysts'):
        text += '## Next-session catalysts and coverage\n\n' + bundle['catalysts'] + '\n\n'
    for idea in bundle['candidates']:
        text += f"## {idea['id']}: {idea['symbol']} — {idea['instrument']}\n\n"
        text += f"Observed underlying: {idea['underlying_price']:.2f} at {idea['observed_at']}. [Market source]({idea['market_source']}).\n\n"
        limit = 1000 if idea['symbol'] in ('SPX', '^GSPC') else 500
        if bundle.get('risk_caps'):
            text += f'**Risk eligibility:** USD {limit} maximum per trade. For quantity q and multiplier m, debit vertical requires q × m × actual debit + all fees ≤ {limit}; use no trade if fees/premium are unavailable. No cap certification from illustrative strikes.\n\n'
        for key in ('thesis', 'level_basis', 'trigger', 'invalidation', 'no_trade', 'structure', 'expiry', 'strike_status'):
            text += f"**{key.replace('_', ' ').title()}:** {idea[key]}\n\n"
        if idea['strike_status'] == 'verified listed':
            text += f"[Chain evidence]({idea['chain_source']}) at {idea['chain_observed_at']}; contracts: {idea['contract_identifiers']}. Prices require refresh.\n\n"
        text += render_profile(idea['payoff_profile'], expiry=idea['expiry'], cap=limit if bundle.get('risk_caps') else None) + '\n\n'
        social = idea.get('outside_commentary')
        if social:
            text += f"Outside commentary: {social['author']}, {social['posted_at']}, {social['quote_or_paraphrase']}: {social['excerpt']} [Original post]({social['post_url']}).\n\nCredibility: {social['credibility']}\n\nOwn assessment: {social['own_assessment']}\n\n"
            if social.get('performance_claim'):
                text += f"Performance claim: {social['performance_claim']} [Independent evidence]({social['independent_performance_source']}).\n\n"
        else:
            text += 'No independently usable outside post attached; this is own analysis.\n\n'
    return text.rstrip() + "\n"


def write_ideas(input_path: Path, output_root: Path) -> Path:
    bundle = json.loads(input_path.read_text())
    text = render_ideas(bundle)
    destination = output_root / 'content/reports/trade-ideas' / f"{bundle['trading_date']}.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding='utf-8')
    return destination
