"""Record what was scheduled so future weeks never repeat a line or a date.

Usage: python3 engine/ledger.py <brand_id> <date> "<headline>" <status> [metricool_post_id]
status: scheduled | failed
"""
import csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(brand_id, date, headline, status, post_id=""):
    p = os.path.join(ROOT, "ledger", f"{brand_id}.csv")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    rows = []
    if os.path.exists(p):
        with open(p, newline="", encoding="utf-8") as fh:
            rows = [r for r in csv.DictReader(fh) if r["date"] != date]
    rows.append({"date": date, "headline": headline, "status": status, "metricool_id": post_id})
    rows.sort(key=lambda r: r["date"])
    with open(p, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "headline", "status", "metricool_id"])
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main(*sys.argv[1:])
