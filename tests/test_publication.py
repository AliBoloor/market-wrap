from hashlib import sha256
from io import BytesIO
import json
from urllib.error import HTTPError
from pathlib import Path
from market_wrap.publication import publication_status
from market_wrap.site import build_site


def fixture(root):
    folder=root/'content/reports/daily';folder.mkdir(parents=True)
    report=folder/'2026-11-04.md'
    report.write_text('''---
report_family: daily
trading_date: 2026-11-04
title: November 4 close
report_type: Daily Market Wrap
generated_at: 2026-11-04T21:30:00Z
data_observed_at: 2026-11-04T21:00:00Z
freshness: Fresh
completeness: Complete
---
Validated closing report.
''')
    marker=root/'data/daily/2026-11-04';marker.mkdir(parents=True)
    (marker/'complete.json').write_text(json.dumps(dict(status='validated',report_family='daily',trading_date='2026-11-04')))
    return report


def test_validated_marker_alone_cannot_suppress_delivery(tmp_path):
    fixture(tmp_path)
    def missing(req,timeout):raise HTTPError(req.full_url,404,'Not found',None,None)
    result=publication_status(tmp_path,opener=missing)
    assert result['state']=='deployment_pending'
    assert all(not r['matches'] for r in result['evidence'])


def test_latest_and_dated_need_exact_source_not_just_http_success(tmp_path):
    report=fixture(tmp_path);build_site(tmp_path/'content/reports',tmp_path/'site')
    calls=[]
    def live(req,timeout):
        calls.append(req.full_url)
        suffix='daily/index.html' if req.full_url.endswith('/daily/') else 'daily/reports/2026-11-04/index.html'
        return BytesIO((tmp_path/'site'/suffix).read_bytes())
    assert publication_status(tmp_path,opener=live)['state']=='published'
    assert len(calls)==2
    report.write_text(report.read_text()+'\nMaterial correction.\n')
    assert publication_status(tmp_path,opener=live)['state']=='deployment_pending'
    def wrong_latest(req,timeout):
        if req.full_url.endswith('/daily/'):return BytesIO(b'<article data-report-date="2026-11-03"></article>')
        return live(req,timeout)
    assert publication_status(tmp_path,opener=wrong_latest)['state']=='deployment_pending'


def test_no_marker_does_not_claim_validated_or_published(tmp_path):
    fixture(tmp_path);(tmp_path/'data/daily/2026-11-04/complete.json').unlink()
    assert publication_status(tmp_path)['state']=='no_validated_content'


def test_daily_prompt_recovers_delivery_before_calendar_and_marker_exit():
    root=Path(__file__).resolve().parents[1]
    prompt=(root/'automation/DAILY_TASK_PROMPT.md').read_text()
    assert prompt.index('publication-status --root . --family daily') < prompt.index('Stop before broad web research')
    assert 'retry ONLY its failed jobs' in prompt
    assert 'must NEVER turn a failed deployment' in prompt
    assert 'Do NOT\nresearch, rewrite the report' in prompt
