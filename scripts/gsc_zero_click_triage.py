#!/usr/bin/env python3
"""Build a read-only review ledger from saved GSC query/page observations."""
import argparse, csv, json, math, sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
REQUIRED_META=("property","search_type","dimensions","filters","date_range")
REQUIRED_ROW=("query","page","clicks","impressions","ctr","position")
def fail(msg): raise ValueError(msg)
def number(v,name,i):
 if not isinstance(v,(int,float)) or isinstance(v,bool) or not math.isfinite(v) or v<0: fail(f"rows[{i}].{name} must be a finite non-negative number")
def validate(p):
 if not isinstance(p,dict): fail("input must be an object")
 m=p.get("metadata")
 if not isinstance(m,dict): fail("metadata must be an object")
 for k in REQUIRED_META:
  if k not in m: fail(f"metadata.{k} is required")
 d=m["date_range"]
 if not isinstance(d,dict) or not all(k in d for k in ("start","end","timezone","finalized")): fail("metadata.date_range requires start, end, timezone, finalized")
 try:
  if date.fromisoformat(d["start"])>date.fromisoformat(d["end"]): fail("date range is reversed")
 except (TypeError,ValueError): fail("date range must contain ordered ISO dates")
 if not isinstance(d["finalized"],bool) or not isinstance(d["timezone"],str) or not d["timezone"].strip(): fail("date range finalized/timezone have invalid types")
 if not isinstance(m["property"],str) or not m["property"].strip() or not isinstance(m["search_type"],str) or not m["search_type"].strip(): fail("property/search_type must be non-empty strings")
 prop=m["property"]
 if not prop.startswith("sc-domain:") and urlparse(prop).scheme not in ("http","https"): fail("property must be an exact GSC domain or URL-prefix identifier")
 if not isinstance(m["dimensions"],list) or not all(isinstance(x,str) for x in m["dimensions"]) or not {"query","page"}.issubset(m["dimensions"]) or not isinstance(m["filters"],dict): fail("metadata dimensions must include query and page; filters must be an object")
 props=p.get("properties",[m["property"]])
 if not isinstance(props,list) or not all(isinstance(x,str) and x for x in props) or len(props)!=len(set(props)): fail("properties must be a unique string list; do not sum overlapping properties")
 if m["property"] not in props: fail("metadata.property must occur in properties")
 if not isinstance(p.get("rows"),list): fail("rows must be a list")
 for i,r in enumerate(p["rows"]):
  if not isinstance(r,dict): fail(f"rows[{i}] must be an object")
  for k in REQUIRED_ROW:
   if k not in r: fail(f"rows[{i}].{k} is required")
  if not isinstance(r["query"],str) or not r["query"].strip() or not isinstance(r["page"],str): fail(f"rows[{i}] query must be non-empty and page must be a string (empty means unknown)")
  if r["page"]:
   url=urlparse(r["page"])
   if url.scheme not in ("http","https") or not url.hostname or url.username or url.password: fail(f"rows[{i}].page must be an ordinary public result URL")
   if prop.startswith("sc-domain:"):
    host=prop[len("sc-domain:"):].lower()
    if url.hostname.lower()!=host and not url.hostname.lower().endswith("."+host): fail(f"rows[{i}].page is outside property")
   elif not r["page"].startswith(prop): fail(f"rows[{i}].page is outside URL-prefix property")
  for k in ("clicks","impressions","ctr","position"): number(r[k],k,i)
  if r["clicks"]>r["impressions"] or r["ctr"]>1 or (r["clicks"]==0 and r["ctr"]!=0) or (r["impressions"]>0 and r["position"]<1): fail(f"rows[{i}] has impossible metrics; CTR is a fraction, not a percent")
  for k in ("relevant","cannibalization","intent_mismatch"):
   if k in r and not isinstance(r[k],bool): fail(f"rows[{i}].{k} must be boolean")
 c=p.get("coverage")
 if not isinstance(c,list): fail("coverage must be a list with explicit query coverage evidence")
 for i,x in enumerate(c):
  if not isinstance(x,dict) or not all(k in x for k in ("query","status","evidence")): fail(f"coverage[{i}] requires query, status, evidence")
  if x["status"] not in ("covered","not_covered","unknown"): fail(f"coverage[{i}].status is invalid")
  if not isinstance(x["query"],str) or not isinstance(x["evidence"],str) or not x["evidence"].strip(): fail(f"coverage[{i}] needs a query and non-empty evidence")
 if len({x["query"] for x in c})!=len(c): fail("duplicate/conflicting query coverage evidence")
 quality=p.get("data_quality",{})
 if not isinstance(quality,dict): fail("data_quality must be an object")
 for k in ("complete_window","anonymous_rows","row_limit_reached"):
  if k in quality and not isinstance(quality[k],bool): fail(f"data_quality.{k} must be boolean")
 for name in ("history","query_totals"):
  values=p.get(name,{})
  if not isinstance(values,dict): fail(f"{name} must be an object")
  for key,v in values.items():
   if not isinstance(v,dict) or "clicks" not in v: fail(f"{name}.{key} requires clicks")
   number(v["clicks"],name+".clicks",key)
def clean(v):
 s=json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else str(v)
 return "'"+s if s.lstrip()[:1] in ("=","+","-","@") or s[:1] in ("\t","\r","\n") else s
def triage(p,min_impressions=1,high_rank_position=10,low_rank_position=20):
 validate(p); m=p["metadata"]; q=p.get("data_quality",{}); limits=[]
 for name,value in (("min_impressions",min_impressions),("high_rank_position",high_rank_position),("low_rank_position",low_rank_position)): number(value,name,"threshold")
 if high_rank_position<1 or low_rank_position<high_rank_position: fail("position thresholds must be ordered and at least one")
 if not m["date_range"]["finalized"]: limits.append("date range is not finalized")
 if not q.get("complete_window",True): limits.append("window is incomplete or not comparable")
 if q.get("anonymous_rows",False): limits.append("anonymous rows may be omitted")
 if q.get("row_limit_reached",False): limits.append("row limit/pagination may omit rows")
 blocking=not m["date_range"]["finalized"] or not q.get("complete_window",True)
 cov={x["query"]:x for x in p["coverage"]}; history=p.get("history",{}); records=[]
 clicked_queries={r["query"] for r in p["rows"] if r["clicks"]>0}
 clicked_queries.update(k for k,v in p.get("query_totals",{}).items() if v["clicks"]>0)
 for r in p["rows"]:
  if r["impressions"]==0 or r["impressions"]<min_impressions or r["query"] in clicked_queries: continue
  x=cov.get(r["query"]); status=x["status"] if x else "unknown"; evidence=x["evidence"] if x else "No explicit owned-page/inventory/intent coverage evidence."
  row_limits=list(limits); intent=r.get("intent")
  if r["query"] not in p.get("query_totals",{}): row_limits.append("Query-wide zero clicks inferred only from saved page rows; join the query-only snapshot before a final claim.")
  if not r["page"]: status="unknown"; row_limits.append("Observed page association is missing; not proof of no page.")
  if not r.get("relevant",True) or intent in ("brand","navigational","no_click_answer"): category,recommendation="irrelevant_brand_navigational_no_click_answer","Do not create or redirect a URL; retain reason and review only if intent changes."
  elif blocking or status=="unknown" or (status=="not_covered" and q.get("row_limit_reached",False)): category,recommendation="unknown_due_to_missing_evidence","Collect comparable complete data and explicit inventory/intent coverage evidence before a page decision."
  elif status=="not_covered": category,recommendation="relevant_untargeted_new_dedicated_page","Research intent and SERP; draft a useful dedicated-page brief only after duplication and cannibalization checks."
  elif r.get("cannibalization",False): category,recommendation="cannibalization","Compare competing owned pages and intent before any consolidation or redirect decision."
  elif r.get("intent_mismatch",False): category,recommendation="existing_page_content_or_intent_adjustment","Use the documented intent mismatch to draft a narrow existing-page or tool adjustment before considering a new URL."
  elif r["position"]>low_rank_position: category,recommendation="low_rank_authority_or_technical_issue","Investigate indexing, technical state, authority, and format before changing content."
  elif r["position"]<=high_rank_position: category,recommendation="relevant_well_ranked_snippet_ctr_investigation","Inspect SERP/snippet fit and no-click-answer intent; do not assume a title change will increase clicks."
  else: category,recommendation="existing_page_content_or_intent_adjustment","Inspect page-to-query intent fit and draft a narrow content adjustment; do not create a duplicate page."
  prior=history.get(r["query"],{}).get("clicks")
  if prior not in (None,0): row_limits.append(f"Earlier window recorded {prior} clicks; current zero clicks does not erase history.")
  records.append({"property":m["property"],"date_range":m["date_range"],"search_type":m["search_type"],"dimensions":m["dimensions"],"filters":m["filters"],"query":r["query"],"page_url":r["page"],"clicks":r["clicks"],"impressions":r["impressions"],"ctr":r["ctr"],"position":r["position"],"query_page_group":r.get("query_page_group",r["query"]+" | "+r["page"]),"coverage_status":status,"coverage_evidence":evidence,"category":category,"recommendation":recommendation,"confidence":"low" if row_limits or status=="unknown" else "medium","limitations":row_limits})
 return {"ledger_version":"1.0","mode":"read_only_draft","thresholds":{"min_impressions":min_impressions,"high_rank_position":high_rank_position,"low_rank_position":low_rank_position},"property_overlap_warning":"Properties are kept separate; never sum domain and URL-prefix properties as unique-site totals.","records":records}
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("input",type=Path); ap.add_argument("--output",required=True,type=Path); ap.add_argument("--csv",type=Path); ap.add_argument("--min-impressions",type=float,default=1); ap.add_argument("--high-rank-position",type=float,default=10); ap.add_argument("--low-rank-position",type=float,default=20); a=ap.parse_args()
 try: ledger=triage(json.loads(a.input.read_text(encoding="utf-8")),a.min_impressions,a.high_rank_position,a.low_rank_position)
 except (OSError,json.JSONDecodeError,ValueError) as e: print(f"error: {e}",file=sys.stderr); return 2
 a.output.write_text(json.dumps(ledger,indent=2)+"\n",encoding="utf-8")
 if a.csv:
  fields=["property","date_range","search_type","dimensions","filters","query","page_url","clicks","impressions","ctr","position","query_page_group","coverage_status","coverage_evidence","category","recommendation","confidence","limitations"]
  with a.csv.open("w",newline="",encoding="utf-8") as f:
   w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
   for r in ledger["records"]: w.writerow({k:clean(r[k]) for k in fields})
 return 0
if __name__=="__main__": sys.exit(main())
