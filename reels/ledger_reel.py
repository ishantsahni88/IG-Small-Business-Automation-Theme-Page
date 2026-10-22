"""Record a Reel's scheduling outcome so future weeks never repeat a hook or double-book a slot.

Usage: python3 reels/ledger_reel.py <episode_id> <date> "<hook>" <status> [metricool_post_id]
status: ready | scheduled | failed
"""
import csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "ledger", "small-business-automation-reels.csv")
F = ["id", "date", "hook", "status", "metricool_id"]


def main(ep, date, hook, status, post_id=""):
    rows = []
    if os.path.exists(P):
        with open(P, newline="", encoding="utf-8") as fh:
            rows = [r for r in csv.DictReader(fh) if r["id"] != ep]
    rows.append({"id": ep, "date": date, "hook": hook, "status": status, "metricool_id": post_id})
    rows.sort(key=lambda r: (r["date"], r["id"]))
    with open(P, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=F); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main(*sys.argv[1:])
