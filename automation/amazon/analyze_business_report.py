#!/usr/bin/env python3
"""AGRAVAT Amazon business report analyzer.

Input: CSV exported from Amazon Seller Central.
Output: compact JSON summary and SKU/ASIN exception list.
No Amazon credentials are required.
"""
import argparse, csv, json
from pathlib import Path

ALIASES = {
    "sku": ["sku", "seller sku"],
    "asin": ["asin", "(parent) asin", "parent asin", "(child) asin", "child asin"],
    "sessions": ["sessions"],
    "page_views": ["page views", "pageviews"],
    "units": ["units ordered", "units ordered - b2b"],
    "sales": ["ordered product sales", "ordered product sales - b2b"],
    "buy_box": ["buy box percentage", "featured offer (buy box) percentage"]
}

def norm(s): return " ".join((s or "").strip().lower().split())

def find_col(headers, aliases):
    m={norm(h):h for h in headers}
    for a in aliases:
        if norm(a) in m: return m[norm(a)]
    return None

def num(v):
    if v is None: return 0.0
    s=str(v).replace(",","").replace("₹","").replace("$","").replace("%","").strip()
    try: return float(s)
    except ValueError: return 0.0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv_file")
    ap.add_argument("--output", default="amazon-summary.json")
    args=ap.parse_args()
    rows=list(csv.DictReader(open(args.csv_file, encoding="utf-8-sig", newline="")))
    if not rows: raise SystemExit("CSV contains no data rows.")
    headers=list(rows[0].keys())
    cols={k:find_col(headers,v) for k,v in ALIASES.items()}
    exceptions=[]
    totals={"sessions":0.0,"page_views":0.0,"units":0.0,"sales":0.0}
    for r in rows:
        sessions=num(r.get(cols["sessions"])) if cols["sessions"] else 0
        views=num(r.get(cols["page_views"])) if cols["page_views"] else 0
        units=num(r.get(cols["units"])) if cols["units"] else 0
        sales=num(r.get(cols["sales"])) if cols["sales"] else 0
        for k,v in [("sessions",sessions),("page_views",views),("units",units),("sales",sales)]: totals[k]+=v
        conversion=(units/sessions*100) if sessions else 0
        if sessions >= 20 and units == 0:
            exceptions.append({"type":"traffic_no_sales","sku":r.get(cols["sku"]) if cols["sku"] else None,"asin":r.get(cols["asin"]) if cols["asin"] else None,"sessions":sessions})
        elif sessions >= 20 and conversion < 3:
            exceptions.append({"type":"low_conversion","sku":r.get(cols["sku"]) if cols["sku"] else None,"asin":r.get(cols["asin"]) if cols["asin"] else None,"sessions":sessions,"conversion_pct":round(conversion,2)})
    summary={
      "rows_analyzed":len(rows),
      "detected_columns":cols,
      "totals":{k:round(v,2) for k,v in totals.items()},
      "overall_unit_session_pct":round(totals["units"]/totals["sessions"]*100,2) if totals["sessions"] else 0,
      "exceptions":exceptions[:50]
    }
    Path(args.output).write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
