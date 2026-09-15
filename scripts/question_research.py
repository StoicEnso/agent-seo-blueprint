#!/usr/bin/env python3
"""Offline observed-question banks and YouTube draft scaffolds. No network or writes."""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from urllib.parse import urlparse

SOURCES = {'paa', 'youtube_comment', 'youtube_transcript', 'review', 'gsc', 'support'}


def nonempty(v, field):
    if not isinstance(v, str) or not v.strip():
        raise ValueError(field + ': nonempty string required')
    if v.strip().upper().startswith(('REPLACE_', 'TODO:', 'TBD:')):
        raise ValueError(field + ': replace the template placeholder with evidence')
    return v.strip()


def date(v):
    v = nonempty(v, 'captured_at')
    d = datetime.fromisoformat(v.replace('Z', '+00:00').replace(' +', '+').replace(' -', '-'))
    if d.tzinfo is None:
        raise ValueError('captured_at: timezone required')
    return d.isoformat()


def url(v, field):
    v = nonempty(v, field)
    p = urlparse(v)
    if p.scheme not in {'http', 'https'} or not p.hostname or p.username or p.password:
        raise ValueError(field + ': HTTP(S) URL without credentials required')
    return v


def observation(row):
    if not isinstance(row, dict) or row.get('kind') != 'observed' or row.get('source_type') not in SOURCES:
        raise ValueError('only observed supported sources belong in the bank; keep hypotheses separate')
    r = dict(row)
    for f in ('exact_text', 'source_record_id', 'source_evidence', 'locale'):
        r[f] = nonempty(r.get(f), f)
    if not re.fullmatch(r'[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})+', r['locale']):
        raise ValueError('locale: language plus market required, e.g. en-US')
    r['locale'] = r['locale'].replace('_', '-').lower()
    r['captured_at'] = date(r.get('captured_at'))
    r['source_url'] = url(r.get('source_url'), 'source_url')
    identity = json.dumps([r['source_type'], r['source_url'], r['source_record_id'], r['locale']], ensure_ascii=False)
    r['id'] = 'q-' + hashlib.sha256(identity.encode()).hexdigest()[:20]
    if row.get('id') is not None and row['id'] != r['id']:
        raise ValueError('id does not match source identity')
    for f in ('seed_query', 'parent_question'):
        if r.get(f) is not None:
            nonempty(r[f], f)
    depth = r.get('expansion_depth')
    if depth is not None and (isinstance(depth, bool) or not isinstance(depth, int) or not 0 <= depth <= 2):
        raise ValueError('expansion_depth must be observed integer 0..2 or unknown/null')
    return r


def bank(packets, max_items=50):
    if isinstance(max_items, bool) or not isinstance(max_items, int) or not 1 <= max_items <= 500:
        raise ValueError('max-items must be 1..500')
    unique, limits = {}, []
    for p in packets:
        if not isinstance(p, dict) or not isinstance(p.get('observations'), list):
            raise ValueError('bank requires observations array')
        if p.get('hypotheses'):
            raise ValueError('keep hypotheses in a separate file')
        ll = p.get('limitations', [])
        if not isinstance(ll, list) or not all(isinstance(x, str) for x in ll):
            raise ValueError('limitations must be strings')
        limits.extend(ll)
        for row in p['observations']:
            r = observation(row)
            if r['id'] in unique and unique[r['id']] != r:
                raise ValueError('conflicting capture for source identity; keep versions separate: ' + r['id'])
            unique[r['id']] = r
            if len(unique) > max_items:
                raise ValueError('unique observation cap exceeded')
    rows = sorted(unique.values(), key=lambda x: x['id'])
    clusters = {}
    for r in rows:
        key = (r['locale'], ' '.join(r['exact_text'].casefold().split()))
        clusters.setdefault(key, []).append(r['id'])
    return {'schema_version': 1, 'observations': rows,
            'exact_text_clusters': [{'locale': k[0], 'normalized_text': k[1], 'observation_ids': v} for k, v in sorted(clusters.items())],
            'counts': {'captured_records': len(rows), 'exact_text_clusters': len(clusters)},
            'limitations': sorted(set(limits + ['Counts are captured records, not people or search volume.', 'Locators are not authenticity checks; semantic clustering needs review.']))}


def import_serp(p, evidence, locale, max_items=50):
    nonempty(evidence, 'evidence')
    if not isinstance(p, dict) or p.get('ok') is not True or not isinstance(p.get('serps'), list):
        raise ValueError('expected successful normalized DataForSEO serps JSON')
    rows = []
    for pi, pack in enumerate(p['serps']):
        if not isinstance(pack, dict) or not isinstance(pack.get('people_also_ask'), list):
            raise ValueError('PAA data unavailable: re-normalize the saved raw capture with updated client')
        captured = date(pack.get('captured_at'))
        seed = nonempty(pack.get('query'), 'query')
        source = url(pack.get('check_url'), 'check_url')
        for gi, group in enumerate(pack['people_also_ask']):
            if not isinstance(group, dict) or not isinstance(group.get('items'), list):
                raise ValueError('unsupported PAA group; inspect raw evidence')
            for qi, q in enumerate(group['items']):
                if not isinstance(q, dict):
                    raise ValueError('unsupported PAA question shape')
                question = nonempty(q.get('title'), 'PAA question title')
                record = f"{pack.get('task_id') or evidence}:{pi}:{gi}:{qi}"
                rows.append({'kind': 'observed', 'source_type': 'paa', 'source_record_id': record,
                             'exact_text': question, 'locale': locale, 'captured_at': captured,
                             'source_url': source, 'source_evidence': f'{evidence}#/serps/{pi}/people_also_ask/{gi}/items/{qi}',
                             'seed_query': seed, 'parent_question': None, 'expansion_depth': None,
                             'provider_language': pack.get('language'), 'provider_location': pack.get('country'), 'raw_question': q})
    return bank([{'observations': rows, 'limitations': ['Tree ancestry/depth unknown unless observed; requested depth is not observed depth.', 'Operator supplies locale: check against provider language/location.']}], max_items)


def brief(packet, plan):
    b = bank([packet], 500)
    if not isinstance(plan, dict):
        raise ValueError('plan must be an object')
    ids = plan.get('observation_ids')
    if not isinstance(ids, list) or not ids or not all(isinstance(i, str) for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('plan requires distinct observation_ids')
    known = {r['id']: r for r in b['observations']}
    if any(i not in known for i in ids):
        raise ValueError('unknown observation IDs')
    selected = [known[i] for i in ids]
    if len({r['locale'] for r in selected}) != 1:
        raise ValueError('do not combine different locales into one brief')
    if plan.get('coverage_decision') not in {'update_section', 'new_page_brief', 'video_brief'}:
        raise ValueError('rejected/unvalidated candidates cannot produce a brief')
    for f in ('page_check_evidence', 'video_fit_evidence', 'proof_plan'):
        nonempty(plan.get(f), f)
    page = url(plan.get('owned_page_url'), 'owned_page_url')
    return {'schema_version': 1, 'status': 'draft_incomplete', 'publication_status': 'not_approved',
            'observation_ids': ids, 'sources': selected, 'locale': selected[0]['locale'],
            'owned_page_url': page, 'coverage_decision': plan['coverage_decision'],
            'page_check_evidence': plan['page_check_evidence'], 'video_fit_evidence': plan['video_fit_evidence'],
            'proof_plan': plan['proof_plan'], 'title': None, 'direct_answer': None, 'original_script': None,
            'chapter_outline': [], 'description': None, 'cta_url': page, 'tracking_plan': None,
            'claim_sources': [], 'limitations': [], 'transcript': {'status': 'pending_recording', 'locator': None},
            'metrics': {'youtube_search_impressions': None, 'youtube_ctr': None, 'watch_time_seconds': None,
                        'google_clicks': None, 'ai_citations': None, 'referral_sessions': None, 'conversions': None},
            'note': 'Write original evidence-grounded content. A script is not a transcript. Validation never authorizes publication.'}


def check_brief(p):
    if not isinstance(p, dict) or p.get('publication_status') != 'not_approved':
        raise ValueError('drafts only, never publication approval')
    if p.get('status') not in {'draft_incomplete', 'draft_ready_for_review'}:
        raise ValueError('draft status required')
    brief({'observations': p.get('sources')}, p)
    for f in ('title', 'direct_answer', 'original_script', 'description', 'tracking_plan'):
        nonempty(p.get(f), f)
    for f in ('chapter_outline', 'claim_sources', 'limitations'):
        v = p.get(f)
        if not isinstance(v, list) or not v or not all(isinstance(x, str) and x.strip() for x in v):
            raise ValueError(f + ': nonempty list of strings required')
    if urlparse(url(p.get('cta_url'), 'cta_url')).hostname != urlparse(p['owned_page_url']).hostname:
        raise ValueError('CTA must point to owned-page host')
    t = p.get('transcript')
    if not isinstance(t, dict) or t.get('status') not in {'pending_recording', 'reviewed'}:
        raise ValueError('transcript status must be pending_recording or reviewed')
    if t['status'] == 'reviewed':
        nonempty(t.get('locator'), 'reviewed transcript locator')
    elif t.get('locator') is not None:
        raise ValueError('pending recording cannot claim transcript locator')
    return {'ok': True, 'status': 'draft_ready_for_review', 'publication_status': 'not_approved',
            'limitations': ['Completeness only; check factual truth, source authenticity, script quality and rights separately.']}


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    x = sub.add_parser('import-serp'); x.add_argument('input'); x.add_argument('--evidence', required=True); x.add_argument('--locale', required=True); x.add_argument('--max-items', type=int, default=50)
    for name in ('merge', 'check-bank'):
        x = sub.add_parser(name); x.add_argument('inputs', nargs='+'); x.add_argument('--max-items', type=int, default=50)
    x = sub.add_parser('brief'); x.add_argument('bank'); x.add_argument('plan')
    x = sub.add_parser('check-brief'); x.add_argument('input')
    a = p.parse_args()
    try:
        if a.command == 'import-serp':
            result = import_serp(load(a.input), a.evidence, a.locale, a.max_items)
        elif a.command in {'merge', 'check-bank'}:
            result = bank([load(f) for f in a.inputs], a.max_items)
        elif a.command == 'brief':
            result = brief(load(a.bank), load(a.plan))
        else:
            result = check_brief(load(a.input))
        print(json.dumps(result, indent=2, ensure_ascii=False)); return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}), file=sys.stderr); return 1


if __name__ == '__main__':
    sys.exit(main())
