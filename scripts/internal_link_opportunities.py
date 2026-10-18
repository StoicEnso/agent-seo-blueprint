#!/usr/bin/env python3
"""Offline, stdlib-only contextual-link discovery. No network and no site edits.

Input is a JSON array of saved HTML captures: url, final_url, status,
content_type, html_path (under the manifest directory), optional sha256 and
x_robots_tag. Review output; a keyword match is not publication approval.
"""
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
from urllib.parse import urljoin, urlsplit, urlunsplit

SKIP = {'head', 'script', 'style', 'noscript', 'template', 'nav', 'header',
        'footer', 'aside', 'form', 'button', 'svg'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}


def clean(text):
    return ' '.join(unicodedata.normalize('NFKC', text).split())


def url_key(url):
    p = urlsplit(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('absolute HTTP(S) URL required')
    if p.query:
        raise ValueError('query URLs require separate ownership review')
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/') or '/', '', ''))


class EditorialHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.blocks = []
        self.links = []
        self.canonicals = []
        self.noindex = False
        self.base_href = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'base':
            self.base_href = True
        if tag == 'link' and 'canonical' in a.get('rel', '').lower().split():
            self.canonicals.append(a.get('href', ''))
        if tag == 'meta' and a.get('name', '').lower() in ('robots', 'googlebot'):
            self.noindex |= bool(re.search(r'\b(noindex|none)\b', a.get('content', ''), re.I))
        hidden = 'hidden' in a or a.get('aria-hidden', '').lower() == 'true'
        hidden |= bool(re.search(r'(display\s*:\s*none|visibility\s*:\s*hidden)', a.get('style', ''), re.I))
        blocked = tag in SKIP or hidden or any(e['blocked'] for e in self.stack)
        scope = 'article' if tag == 'article' or any(e['tag'] == 'article' for e in self.stack) else 'main' if tag == 'main' or any(e['tag'] == 'main' for e in self.stack) else 'body_fallback'
        block = None
        if tag in ('p', 'li') and not blocked:
            block = {'scope': scope, 'parts': []}
            self.blocks.append(block)
        if tag == 'a' and not blocked:
            self.links.append({'href': a.get('href', ''), 'scope': scope})
        if tag not in VOID:
            self.stack.append({'tag': tag, 'blocked': blocked, 'block': block})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if any(e['blocked'] for e in self.stack):
            return
        block = next((e['block'] for e in reversed(self.stack) if e['block'] is not None), None)
        if block is not None:
            linked = any(e['tag'] == 'a' for e in self.stack)
            if block['parts'] and block['parts'][-1][0] == linked:
                block['parts'][-1][1] += data
            else:
                block['parts'].append([linked, data])


def inspect(row, target, keywords, base, excluded):
    source = url_key(row['url'])
    record = {'source_url': source, 'target_url': target, 'status': 'excluded', 'reason': ''}
    def stop(reason):
        record['reason'] = reason
        return record
    if source == target:
        return stop('self_link')
    if source in excluded:
        return stop('protected_or_excluded')
    if urlsplit(source).netloc != urlsplit(target).netloc or urlsplit(source).scheme != urlsplit(target).scheme:
        return stop('different_origin')
    if row.get('status') != 200 or 'html' not in row.get('content_type', '').lower():
        return stop('not_200_html')
    if url_key(row.get('final_url', row['url'])) != source:
        return stop('redirected_source')
    file = (base / row['html_path']).resolve()
    if not file.is_relative_to(base.resolve()):
        return stop('capture_outside_manifest_directory')
    if file.stat().st_size > 5_000_000:
        return stop('capture_too_large')
    payload = file.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if row.get('sha256') and row['sha256'] != digest:
        return stop('capture_hash_mismatch')
    record['source_sha256'] = digest
    p = EditorialHTML()
    p.feed(payload.decode('utf-8', errors='replace'))
    if p.base_href:
        return stop('base_element_needs_manual_review')
    if p.noindex or re.search(r'\b(noindex|none)\b', row.get('x_robots_tag', ''), re.I):
        return stop('noindex')
    if len(p.canonicals) != 1 or not p.canonicals[0]:
        return stop('missing_or_multiple_canonicals')
    if url_key(urljoin(source, p.canonicals[0])) != source:
        return stop('noncanonical_source')
    scopes = {b['scope'] for b in p.blocks}
    scope = 'article' if 'article' in scopes else 'main' if 'main' in scopes else 'body_fallback'
    record['extraction_scope'] = scope
    for link in p.links:
        if link['scope'] != scope or not link['href']:
            continue
        try:
            if url_key(urljoin(source, link['href'])) == target:
                return stop('already_links_to_target_in_selected_scope')
        except ValueError:
            continue
    for b in p.blocks:
        if b['scope'] != scope:
            continue
        # Never join across an existing anchor or across paragraphs to invent a phrase.
        for linked, text in b['parts']:
            if linked:
                continue
            text = clean(text)
            for keyword in keywords:
                match = re.search(r'(?<!\w)' + re.escape(clean(keyword)) + r'(?!\w)', text, re.I)
                if match:
                    record.update(status='candidate_review_only', reason='unlinked_phrase_in_saved_html',
                                  matched_phrase=match.group(0), keyword=keyword,
                                  excerpt=text[max(0, match.start()-100):match.end()+200],
                                  reader_reason='', approval='not_granted', live_link_verified=False)
                    return record
    return stop('no_unlinked_phrase')


def discover(rows, target, keywords, base, excluded=()):
    target = url_key(target)
    excluded = {url_key(u) for u in excluded}
    if not isinstance(keywords, list) or not keywords or not all(isinstance(k, str) and clean(k) for k in keywords):
        raise ValueError('keywords must be a nonempty list of nonempty strings')
    seen, results = set(), []
    for row in rows:
        try:
            key = url_key(row['url'])
            if key in seen:
                results.append({'source_url': key, 'status': 'excluded', 'reason': 'duplicate_source'})
                continue
            seen.add(key)
            results.append(inspect(row, target, keywords, Path(base), excluded))
        except (KeyError, ValueError, OSError, TypeError) as error:
            results.append({'source_url': row.get('url', '') if isinstance(row, dict) else '',
                            'status': 'error', 'reason': str(error)})
    return {'target_url': target, 'network_requests': 0, 'site_edits': 0,
            'limits': 'Saved-HTML sample only; not a crawl, indexation check, relevance verdict or approval. Body fallback requires manual boilerplate review. CSS/JS-hidden content and malformed HTML need rendered verification.',
            'candidates': [r for r in results if r['status'] == 'candidate_review_only'], 'pages': results}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--manifest', required=True, type=Path)
    ap.add_argument('--target', required=True)
    ap.add_argument('--keywords', required=True, type=Path, help='JSON array of phrases')
    ap.add_argument('--exclude-urls', type=Path, help='JSON array of protected source URLs')
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    rows = json.loads(a.manifest.read_text())
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        ap.error('manifest must be a JSON array of capture objects')
    protected = {a.manifest.resolve(), a.keywords.resolve()}
    if a.exclude_urls:
        protected.add(a.exclude_urls.resolve())
    protected.update((a.manifest.parent / r['html_path']).resolve() for r in rows if 'html_path' in r)
    if a.out.resolve() in protected:
        ap.error('output must not overwrite any input')
    result = discover(rows, a.target, json.loads(a.keywords.read_text()), a.manifest.parent,
                      json.loads(a.exclude_urls.read_text()) if a.exclude_urls else [])
    a.out.write_text(json.dumps(result, indent=2) + '\n')
    print(f"{len(result['candidates'])} review candidates; {len(result['pages'])} input rows; no network or site edits")


if __name__ == '__main__':
    main()
