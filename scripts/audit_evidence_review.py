#!/usr/bin/env python3
"""Offline process/citation evidence reviewer. Never fetches, sends or promotes a pilot."""
import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path
from urllib.parse import urlsplit


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def evidence(value):
    return isinstance(value, list) and bool(value) and all(text(x) for x in value)


def summarize(data):
    require(type(data.get('schema_version')) is int and data['schema_version'] == 1, 'schema_version must be integer 1')
    require(isinstance(data.get('sites'), list) and data['sites'], 'sites must be a non-empty list')
    output = {'schema_version': 1, 'mode': 'offline_review_only', 'sites': []}
    site_ids = set()
    for site in data['sites']:
        sid = site.get('site_id')
        require(text(sid) and sid not in site_ids, 'site_id must be non-empty and unique')
        site_ids.add(sid)
        require(text(site.get('domain')), f'{sid}: domain required')
        workflow = site.get('workflow', {})
        scope = workflow.get('evidence_scope')
        require(scope in ('public_proposal', 'first_party_validated'), f'{sid}: invalid workflow evidence_scope')
        require(text(workflow.get('job')), f'{sid}: workflow job required')
        steps = workflow.get('steps')
        require(isinstance(steps, list) and steps, f'{sid}: workflow steps required')
        for step in steps:
            require(text(step.get('step')) and text(step.get('owner_role')), f'{sid}: step and owner_role required')
            if scope == 'first_party_validated':
                require(evidence(step.get('evidence')), f'{sid}: validated steps require evidence')
        baseline = site.get('baseline', {})
        require(baseline.get('status') in ('not_measured', 'measured'), f'{sid}: invalid baseline status')
        fields = ('period', 'completed_jobs', 'total_human_minutes', 'exception_jobs')
        metrics = {'status': baseline['status'], 'human_minutes_per_completed_job': None, 'exception_rate': None}
        if baseline['status'] == 'not_measured':
            require(all(baseline.get(k) is None for k in fields), f'{sid}: unknown baseline values must be null')
        else:
            require(scope == 'first_party_validated', f'{sid}: measured baseline requires first-party workflow evidence')
            require(text(baseline.get('period')) and evidence(baseline.get('evidence')), f'{sid}: measured baseline needs period and evidence')
            jobs, minutes, exceptions = (baseline.get(k) for k in fields[1:])
            require(type(jobs) is int and jobs >= 0 and type(exceptions) is int and 0 <= exceptions <= jobs, f'{sid}: invalid job counts')
            require(number(minutes), f'{sid}: invalid human minutes')
            require(jobs != 0 or minutes == 0, f'{sid}: cannot attach completed-job minutes to zero completed jobs')
            metrics.update({'period': baseline['period'], 'completed_jobs': jobs, 'total_human_minutes': minutes, 'exception_jobs': exceptions})
            if jobs:
                metrics['human_minutes_per_completed_job'] = minutes / jobs
                metrics['exception_rate'] = exceptions / jobs
        pilot = site.get('pilot', {})
        require(pilot.get('mode') in ('read_only', 'shadow', 'draft_only'), f'{sid}: pilot mode must have no live effects')
        require(text(pilot.get('success_measure')) and text(pilot.get('stop_condition')), f'{sid}: pilot needs success measure and stop condition')
        observations = site.get('provider_observations', [])
        require(isinstance(observations, list), f'{sid}: provider_observations must be a list')
        lanes, seen, question_versions = {}, set(), {}
        for row in observations:
            for field in ('provider', 'surface', 'locale', 'question_id', 'question_version', 'exact_question'):
                require(text(row.get(field)), f'{sid}: observation {field} required')
            qkey = (row['question_id'], row['question_version'])
            require(qkey not in question_versions or question_versions[qkey] == row['exact_question'], f'{sid}: changed wording requires a new question version')
            question_versions[qkey] = row['exact_question']
            status = row.get('status')
            require(status in ('observed', 'unavailable', 'not_checked'), f'{sid}: invalid observation status')
            key = (row['provider'], row['surface'], row['locale'])
            lane = lanes.setdefault(key, {'provider': key[0], 'surface': key[1], 'locale': key[2], 'observed': 0, 'unavailable': 0, 'not_checked': 0, 'brand_mentioned': None})
            citations = row.get('citations')
            require(isinstance(citations, list), f'{sid}: citations must be a list')
            if status == 'observed':
                require(type(row.get('brand_mentioned')) is bool and evidence(row.get('evidence')), f'{sid}: observed answer needs boolean and evidence')
                try:
                    stamp = dt.datetime.fromisoformat(row.get('captured_at', '').replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    raise ValueError(f'{sid}: observed answer requires ISO captured_at') from None
                require(stamp.tzinfo is not None, f'{sid}: captured_at needs timezone')
                identity = key + (row['question_id'], row['question_version'], stamp.isoformat())
                require(identity not in seen, f'{sid}: duplicate observation')
                seen.add(identity)
                for citation in citations:
                    parsed = urlsplit(citation.get('url', ''))
                    require(parsed.scheme in ('http', 'https') and parsed.netloc and not parsed.username and not parsed.password, f'{sid}: invalid public citation URL')
                    require(citation.get('source_type') in ('owned', 'editorial', 'community', 'directory', 'other'), f'{sid}: citation source_type required')
                lane['brand_mentioned'] = (lane['brand_mentioned'] or 0) + int(row['brand_mentioned'])
            else:
                require(row.get('brand_mentioned') is None and not citations, f'{sid}: unobserved answers cannot contain a presence judgment or citations')
                require(row.get('captured_at') is None, f'{sid}: unobserved answers cannot claim answer capture time')
            lane[status] += 1
        output['sites'].append({'site_id': sid, 'domain': site['domain'], 'workflow_evidence_scope': scope, 'baseline': metrics, 'pilot_mode': pilot['mode'], 'provider_lanes': list(lanes.values()), 'limits': ['No universal score', 'Not traffic, revenue or causal proof', 'No live action authorised by this review']})
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = summarize(json.loads(args.input.read_text(encoding='utf-8')))
        rendered = json.dumps(result, indent=2, allow_nan=False) + '\n'
        if args.output:
            args.output.write_text(rendered, encoding='utf-8')
        else:
            print(rendered, end='')
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
        print(f'Invalid audit evidence: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
