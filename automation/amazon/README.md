# Amazon Monitor

This module analyzes Amazon Seller Central CSV exports without requiring API credentials.

## First supported input
Business Reports / Detail Page Sales and Traffic style CSV.

## Run
```bash
python automation/amazon/analyze_business_report.py report.csv --output amazon-summary.json
```

It detects common Amazon column names, totals traffic/sales, calculates unit-session conversion, and flags products with meaningful traffic but zero or low conversion.

### Current alert rules
- 20+ sessions and zero units -> traffic_no_sales
- 20+ sessions and conversion below 3% -> low_conversion

Thresholds are intentionally conservative placeholders and should be tuned from AGRAVAT's actual baseline.
