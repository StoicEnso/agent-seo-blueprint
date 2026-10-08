#!/usr/bin/env python3
"""Build a read-only review ledger from saved GSC query/page observations."""
import argparse, csv, json, sys
from pathlib import Path
REQUIRED_META=("property","search_type","dimensions","filters","date_range")
REQUIRED_ROW=("query","page","clicks","impressions","ctr","position")
def fail(msg): raise ValueError(msg)
def number(v,name,i):
 if not isinstance(v,(int,float)) or isinstance(v,bool) or v<0: fail(f"rows[{i}].{name} must be a non-negative number")
def validate(p):
 if not isinstance(p,dict): fail("input must be an object")
 m=p.get("metadata")
 if not isinstance(m,dict): fail("metadata must be an object")
 for k in REQUIRED_META:
  if k not in m: fail(f"metadata.{k} is required")
 d=m["date_range"]
 if not isinstance(d,dict) or not all(k in d for k in ("start","end","timezone","finalized")): fail("metadata.date_range requires start, end, timezone, finalized")
 if not isinstance(m["dimensions"],list) or not isinstance(m["filters"],dict): fail("metadata dimensions/filters have invalid types")
 props=p.get("properties",[m["property"]])
 if not isinstance(props,list) or len(props)!=len(set(props)): fail("properties must be a unique list; do not sum overlapping properties")
 if m["property"] not in props: fail("metadata.property must occur in properties")
 if not isinstance(p.get("rows"),list): fail("rows must be a list")
 for i,r in enumerate(p["rows"]):
  if not isinstance(r,dict): fail(f"rows[{i}] must be an object")
  for k in REQUIRED_ROW:
   if k not in r: fail(f"rows[{i}].{k} is required")
  if not isinstance(r["query"],str) or not isinstance(r["page"],str): fail(f"rows[{i}] query/page must be strings")
  for k in ("clicks","impressions","ctr","position"): number(r[k],k,i)
 c=p.get("coverage")
 if not isinstance(c,list): fail("coverage must be a list with explicit query coverage evidence")
 for i,x in enumerate(c):
  if not isinstance(x,dict) or not all(k in x for k in ("query","status","evidence")): fail(f"coverage[{i}] requires query, status, evidence")
  if x["status"] not in ("covered","not_covered","unknown"): fail(f"coverage[{i}].status is invalid")
def clean(v):
 s=str(v); return "'"+s if s[:1] in ("=","+","-","@") else s
def triage(p,min_impressions=1,high_rank_position=10,low_rank_position=20):
 validate(p); m=p["metadata"]; q=p.get("data_quality",{}); limits=[]
 if not q.get("complete_window",True): limits.append("window is incomplete or not comparable")
 if q.get("anonymous_rows",False): limits.append("anonymous rows may be omitted")
 if q.get("row_limit_reached",False): limits.append("row limit/pagination may omit rows")
 cov={x["query"]:x for x in p["coverage"]}; history=p.get("history",{}); records=[]
 for r in p["rows"]:
  if r["impressions"]<min_impressions or r["clicks"]!=0: continue
  x=cov.get(r["query"]); status=x["status"] if x else "unknown"; evidence=x["evidence"] if x else "No explicit owned-page/inventory/intent coverage evidence."
  row_limits=list(limits); intent=r.get("intent")
  if not r.get("relevant",True) or intent in ("brand","navigational","no_click_answer"): category,recommendation="irrelevant_brand_navigational_no_click_answer","Do not create or redirect a URL; retain reason and review only if intent changes."
  elif limits or status=="unknown": category,recommendation="unknown_due_to_missing_evidence","Collect comparable complete data and explicit inventory/intent coverage evidence before a page decision."
  elif status=="not_covered": category,recommendation="relevant_untargeted_new_dedicated_page","Research intent and SERP; draft a useful dedicated-page brief only after duplication and cannibalization checks."
  elif r.get("cannibalization",False): category,recommendation="cannibalization","Compare competing owned pages and intent before any consolidation or redirect decision."
  elif r["position"]>low_rank_position: category,recommendation="low_rank_authority_or_technical_issue","Investigate indexing, technical state, authority, and format before changing content."
  elif r["position"]<=high_rank_position: category,recommendation="relevant_well_ranked_snippet_ctr_investigation","Inspect SERP/snippet fit and no-click-answer intent; do not assume a title change will increase clicks."
  else: category,recommendation="existing_page_content_or_intent_adjustment","Inspect page-to-query intent fit and draft a narrow content adjustment; do not create a duplicate page."
  prior=history.get(r["query"],{}).get("clicks")
  if prior not in (None,0): row_limits.append(f"Earlier window recorded {prior} clicks; current zero clicks does not erase history.")
  records.append({"property":m["property"],"date_range":m["date_range"],"search_type":m["search_type"],"dimensions":m["dimensions"],"filters":m["filters"],"query":r["query"],"page_url":r["page"],"clicks":r["clicks"],"impressions":r["impressions"],"ctr":r["ctr"],"position":r["position"],"query_page_group":r.get("query_page_group",r["query"]+" | "+r["page"]),"coverage_status":status,"coverage_evidence":evidence,"category":category,"recommendation":recommendation,"confidence":"low" if limits or status=="unknown" else "medium","limitations":row_limits})
 return {"ledger_version":"1.0","mode":"read_only_draft","thresholds":{"min_impressions":min_impressions,"high_rank_position":high_rank_position,"low_rank_position":low_rank_position},"property_overlap_warning":"Properties are kept separate; never sum domain and URL-prefix properties as unique-site totals.","records":records}
def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("input",type=Path); ap.add_argument("--output",required=True,type=Path); ap.add_argument("--csv",type=Path); ap.add_argument("--min-impressions",type=float,default=1); ap.add_argument("--high-rank-position",type=float,default=10); ap.add_argument("--low-rank-position",type=float,default=20); a=ap.parse_args()
 try: ledger=triage(json.loads(a.input.read_text(encoding="utf-8")),a.min_impressions,a.high_rank_position,a.low_rank_position)
 except (OSError,json.JSONDecodeError,ValueError) as e: print(f"error: {e}",file=sys.stderr); return 2
 a.output.write_text(json.dumps(ledger,indent=2)+"\n",encoding="utf-8")
 if a.csv:
  fields=["query","page_url","clicks","impressions","ctr","position","category","recommendation","confidence"]
  with a.csv.open("w",newline="",encoding="utf-8") as f:
   w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
   for r in ledger["records"]: w.writerow({k:clean(r[k]) for k in fields})
 return 0
if __name__=="__main__": sys.exit(main())
