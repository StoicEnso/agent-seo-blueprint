#!/usr/bin/env python3
"""
Search the Danny Postma SEO course: lessons + distilled playbooks.

Usage:
    python3 scripts/search_course.py "keyword finding"
    python3 scripts/search_course.py "programmatic seo" --full   # include transcript body matches
    python3 scripts/search_course.py "haro" --json

Returns the best-matching lessons (with their distilled playbooks) and the matching
playbooks directly. Dependency-free (Python stdlib only).

Answers "what does the course say about X" by ranking over lesson titles, summaries,
key takeaways, and (with --full) the private transcripts in _source/.
"""
import argparse, json, re, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
INDEX = SKILL / "references/course-index/course-index.json"
TRANSCRIPTS = SKILL / "_source/transcripts"

STOP = set("a an and the of to for in on with how what when why is are be do this that your you it as at or".split())


def tokenize(text):
    return [t for t in re.findall(r"[a-z0-9]+", (text or "").lower()) if t not in STOP and len(t) > 1]


def score(query_tokens, text, weight=1.0):
    toks = tokenize(text)
    if not toks:
        return 0.0
    counts = {}
    for t in toks:
        counts[t] = counts.get(t, 0) + 1
    s = 0.0
    for q in query_tokens:
        s += counts.get(q, 0) * weight
        if q not in counts:
            for t in counts:
                if t.startswith(q) or q.startswith(t):
                    s += 0.4 * weight
                    break
    return s


def load_index():
    if not INDEX.exists():
        sys.exit(f"course-index.json not found at {INDEX}")
    return json.loads(INDEX.read_text(encoding="utf-8"))


def search(query, full=False, limit=8):
    qtoks = tokenize(query)
    if not qtoks:
        sys.exit("Empty query after removing stopwords.")
    results = []
    for e in load_index():
        s = 0.0
        s += score(qtoks, e.get("title", ""), 5.0)
        s += score(qtoks, " ".join(e.get("aliases", [])), 6.0)
        s += score(qtoks, " ".join(e.get("key_takeaways", [])), 3.0)
        s += score(qtoks, e.get("summary", ""), 2.5)
        s += score(qtoks, e.get("chapterName", ""), 1.5)
        if full:
            tp = SKILL / e["transcript"]
            if tp.exists():
                s += score(qtoks, tp.read_text(encoding="utf-8"), 0.15)
        if s > 0:
            results.append((s, e))
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:limit]


def collect_playbooks(results):
    seen, pbs = set(), []
    for _, e in results:
        for pb in e.get("playbooks", []):
            if pb not in seen:
                seen.add(pb)
                pbs.append(pb)
    return pbs


def main():
    ap = argparse.ArgumentParser(description="Search the SEO course (lessons + playbooks).")
    ap.add_argument("query", help="What to search for, e.g. 'keyword finding'")
    ap.add_argument("--full", action="store_true", help="Also search transcript bodies (slower).")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--json", action="store_true", help="Machine-readable output.")
    args = ap.parse_args()

    results = search(args.query, full=args.full, limit=args.limit)
    pbs = collect_playbooks(results)

    if args.json:
        print(json.dumps({
            "query": args.query,
            "lessons": [{"code": e["code"], "title": e["title"], "chapter": e["chapterName"],
                         "score": round(s, 2), "summary": e.get("summary", ""),
                         "playbooks": e.get("playbooks", []), "transcript": e["transcript"]}
                        for s, e in results],
            "playbooks": pbs,
        }, indent=2))
        return

    if not results:
        print(f'No matches for "{args.query}". Try --full or broader terms.')
        return

    print(f'\nCourse says - top matches for "{args.query}":\n')
    for s, e in results:
        print(f"  [{e['code']}] {e['title']}  ({e['chapterName']}, score {s:.1f})")
        if e.get("summary"):
            print(f"       {e['summary']}")
        if e.get("playbooks"):
            print(f"       playbooks: {', '.join(e['playbooks'])}")
        print()
    if pbs:
        print("Distilled playbooks to read (relative to references/playbooks/):")
        for pb in pbs:
            print(f"  - {pb}")
        print()


if __name__ == "__main__":
    main()
