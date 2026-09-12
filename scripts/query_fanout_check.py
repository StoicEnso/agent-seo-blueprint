"""Offline structural checks for saved query fan-out evidence. No provider calls or writes."""
import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

STATES = {'observed', 'citation_only', 'not_exposed', 'no_search_observed', 'blocked', 'untested'}
METHODS = {'visible_query_ui', 'official_api_query_metadata', 'approved_export'}

def text(value):
    return isinstance(value, str) and bool(value.strip())

def stamp(value):
    if not text(value):
        return False
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).utcoffset() is not None
    except ValueError:
        return False

def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ['ledger must be an object']
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        errors.append('schema_version must be 1')
    if type(data.get('example_only')) is not bool:
        errors.append('example_only must be boolean')
    for field in ('questions', 'observations', 'hypotheses', 'limitations'):
        if not isinstance(data.get(field), list):
            errors.append(field + ' must be a list')
    if errors:
        return errors
    if not data['questions'] or not data['observations']:
        errors.append('questions and observations must be nonempty')
    keys = set()
    for q in data['questions']:
        if not isinstance(q, dict):
            errors.append('question must be an object'); continue
        if not text(q.get('prompt_id')) or type(q.get('prompt_version')) is not int or q['prompt_version'] < 1 or not text(q.get('exact_text')):
            errors.append('question requires ID, positive integer version and exact text'); continue
        key = (q['prompt_id'], q['prompt_version'])
        if key in keys:
            errors.append('duplicate question version')
        keys.add(key)
    seen = set()
    for i, r in enumerate(data['observations']):
        prefix = 'observation %d: ' % i
        if not isinstance(r, dict):
            errors.append(prefix + 'must be an object'); continue
        for field in ('observation_id', 'prompt_id', 'provider', 'surface', 'model', 'mode', 'search_setting', 'locale', 'account_state'):
            if not text(r.get(field)):
                errors.append(prefix + field + ' required')
        ident = r.get('observation_id')
        if text(ident):
            if ident in seen:
                errors.append(prefix + 'duplicate observation_id')
            seen.add(ident)
        pid, ver = r.get('prompt_id'), r.get('prompt_version')
        if not text(pid) or type(ver) is not int or (pid, ver) not in keys:
            errors.append(prefix + 'unknown question version')
        state = r.get('state')
        if not isinstance(state, str) or state not in STATES:
            errors.append(prefix + 'invalid state'); continue
        queries, citations = r.get('queries'), r.get('citations')
        if not isinstance(queries, list) or not isinstance(citations, list):
            errors.append(prefix + 'queries and citations must be lists'); continue
        if state != 'untested' and not stamp(r.get('captured_at')):
            errors.append(prefix + 'timezone-aware captured_at required')
        if state not in {'untested', 'blocked'} and not text(r.get('evidence')):
            errors.append(prefix + 'run evidence required')
        if state != 'observed' and queries:
            errors.append(prefix + 'non-observed state cannot contain actual queries')
        if state == 'observed' and not queries:
            errors.append(prefix + 'observed state needs actual queries')
        if state != 'observed' and not text(r.get('reason')):
            errors.append(prefix + 'non-observed state needs a reason')
        if state == 'citation_only' and not citations:
            errors.append(prefix + 'citation_only needs citations')
        if state in {'untested', 'blocked', 'no_search_observed', 'not_exposed'} and citations:
            errors.append(prefix + 'state is inconsistent with citations')
        if state == 'untested' and (r.get('captured_at') is not None or r.get('evidence') is not None):
            errors.append(prefix + 'untested cannot claim captured evidence')
        qids = set()
        for q in queries:
            if not isinstance(q, dict):
                errors.append(prefix + 'query must be an object'); continue
            for field in ('query_id', 'text', 'evidence'):
                if not text(q.get(field)):
                    errors.append(prefix + 'query ' + field + ' required')
            method = q.get('method')
            if not isinstance(method, str) or method not in METHODS:
                errors.append(prefix + 'query method is not observed evidence')
            qid = q.get('query_id')
            if text(qid):
                if qid in qids:
                    errors.append(prefix + 'duplicate query_id')
                qids.add(qid)
        for c in citations:
            if not isinstance(c, dict) or not text(c.get('url')) or not c['url'].startswith(('https://', 'http://')) or not text(c.get('evidence')):
                errors.append(prefix + 'citation requires URL and evidence')
    for h in data['hypotheses']:
        if not isinstance(h, dict) or h.get('kind') != 'inferred' or not text(h.get('text')) or not text(h.get('rationale')) or not text(h.get('validation_status')):
            errors.append('hypothesis requires inferred kind, text, rationale and validation_status')
    return errors

def summarize(data):
    groups = {}
    for r in data['observations']:
        key = (r['provider'], r['surface'])
        groups.setdefault(key, Counter())[r['state']] += 1
    return [{'provider': p, 'surface': s, 'states': dict(sorted(v.items()))} for (p, s), v in sorted(groups.items())]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('ledger', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.ledger.read_text(encoding='utf-8'))
        errors = validate(data)
    except (OSError, ValueError) as exc:
        print(json.dumps({'valid': False, 'errors': [str(exc)]})); return 1
    result = {'valid': not errors, 'errors': errors, 'verification': 'structure_only'}
    if not errors:
        result['example_only'] = data['example_only']
        result['provider_surface_states'] = summarize(data)
    print(json.dumps(result, indent=2))
    return int(bool(errors))

if __name__ == '__main__':
    raise SystemExit(main())
