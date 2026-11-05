"""Distinguish validated local content from verified live publication.

A completion marker avoids repeated research; it does not prove Pages delivery.
Both latest and dated routes must identify the exact source bytes before a
scheduled retry may exit as already published.
"""
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import Request,urlopen
from .site import discover_reports


class _Identity(HTMLParser):
    def __init__(self):
        super().__init__();self.reports=[]

    def handle_starttag(self,tag,attrs):
        if tag=='article':
            attrs=dict(attrs)
            self.reports.append((attrs.get('data-report-family'),attrs.get('data-report-date'),attrs.get('data-source-sha256')))


def publication_status(root:Path,*,family='daily',base_url='https://aliboloor.github.io/market-wrap/',opener=urlopen):
    reports=[r for r in discover_reports(root/'content/reports') if r.family==family]
    if not reports:
        return dict(state='no_validated_content',family=family)
    report=reports[0];day=report.slug
    marker=root/'data'/family/day/'complete.json'
    if not marker.exists():
        return dict(state='no_validated_content',family=family,trading_date=day)
    saved=json.loads(marker.read_text())
    if any(saved.get(k)!=v for k,v in dict(status='validated',report_family=family,trading_date=day).items()):
        return dict(state='no_validated_content',family=family,trading_date=day)
    digest=sha256(report.source.read_bytes()).hexdigest()
    expected=(family,day,digest);evidence=[]
    for suffix in (f'{family}/',f'{family}/reports/{day}/'):
        url=base_url.rstrip('/')+'/'+suffix
        try:
            request=Request(url,headers={'User-Agent':'market-wrap-publication-check/1.0','Cache-Control':'no-cache'})
            with opener(request,timeout=20) as response:
                parser=_Identity();parser.feed(response.read().decode('utf-8'))
                evidence.append(dict(url=url,matches=expected in parser.reports))
        except (OSError,ValueError) as error:
            evidence.append(dict(url=url,matches=False,error=str(error)))
    return dict(state='published' if all(e['matches'] for e in evidence) else 'deployment_pending',
        family=family,trading_date=day,source_sha256=digest,evidence=evidence)
