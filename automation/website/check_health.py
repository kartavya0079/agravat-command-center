#!/usr/bin/env python3
"""AGRAVAT website health checker.

Checks configured public endpoints and exits non-zero when a required endpoint
is unavailable. No credentials or customer data are used.
"""
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

CONFIG = Path(__file__).resolve().parents[2] / "config" / "website-health.json"

def check(url: str, timeout: int = 15):
    request = urllib.request.Request(url, headers={"User-Agent": "AGRAVAT-Automation-Health/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, None
    except urllib.error.HTTPError as exc:
        return exc.code, str(exc)
    except Exception as exc:
        return None, str(exc)

def main():
    cfg = json.loads(CONFIG.read_text())
    failed = []
    for item in cfg["endpoints"]:
        status, error = check(item["url"], cfg.get("timeout_seconds", 15))
        ok = status is not None and 200 <= status < 400
        print(f'{"OK" if ok else "FAIL"} | {item["name"]} | status={status} | {item["url"]}')
        if not ok and item.get("required", True):
            failed.append({"name": item["name"], "status": status, "error": error})
    if failed:
        print(json.dumps({"failed": failed}, indent=2))
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
