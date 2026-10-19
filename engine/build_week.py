"""Validate a week file, render its posters and write Metricool payloads.

Usage:  python3 engine/build_week.py weeks/<brand>/<YYYY-MM-DD>.json

Week file: JSON list of items
  {"date": "YYYY-MM-DD", "template": "quote|statement|workflow",
   "fields": {...on-image text...}, "caption": "caption body, no hashtags, no CTA"}

Outputs:
  media/<brand>/<date>.jpg                    (commit + push so the raw URL goes live)
  payloads/<brand>/<week>.json                (exact createScheduledPost arguments)
Exits non-zero and prints every problem if any item fails a check.
"""
import json, os, re, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import render

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "https://raw.githubusercontent.com/ishantsahni88/ig-small-business-automation-theme-page/main/"


def words(s):
    return len(str(s or "").replace("*", "").split())


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", str(s or "").lower()).strip()


def used_lines(brand_id):
    p = os.path.join(ROOT, "ledger", f"{brand_id}.csv")
    if not os.path.exists(p):
        return set()
    with open(p, newline="", encoding="utf-8") as fh:
        return {norm(r["headline"]) for r in csv.DictReader(fh)}


def headline(item):
    f = item["fields"]
    return f.get("quote") or f.get("headline") or f.get("title") or ""


def lint(item, brand, seen):
    f, t, issues = item["fields"], item["template"], []
    blob = " ".join(str(v) for v in list(f.values()) + [item.get("caption", "")])
    if t not in brand["templates"]:
        issues.append(f"template '{t}' is not used by this brand")
    if re.search(r"\d{1,3}\s?%", blob):
        issues.append("contains a percentage (no invented stats)")
    if re.search(r"\b(cure[sd]?|heal(s|ing)? (your )?(anxiety|depression|trauma)|diagnos\w*|clinically proven|guarantee[sd]?)\b", blob, re.I):
        issues.append("contains a health or guarantee claim")
    if "#" in item.get("caption", ""):
        issues.append("caption must not contain hashtags (added automatically)")
    if not item.get("caption"):
        issues.append("caption body missing")
    if t == "quote":
        if words(f.get("quote")) > 12: issues.append("quote longer than 12 words")
        if not f.get("support") or words(f.get("support")) > 22: issues.append("support line missing or over 22 words")
    elif t == "statement":
        if not re.search(r"\*[^*]+\*", f.get("headline", "")): issues.append("headline needs one *accent* phrase")
        if words(f.get("headline")) > 14: issues.append("headline longer than 14 words")
    elif t == "workflow":
        st = f.get("steps") or []
        if not 3 <= len(st) <= 5: issues.append("workflow needs 3-5 steps")
        if any(len(s) > 34 for s in st): issues.append("a step is longer than 34 characters")
        if words(f.get("title")) > 9: issues.append("title longer than 9 words")
        if not f.get("before") or not f.get("after"): issues.append("before/after missing")
    h = norm(headline(item))
    if h in seen:
        issues.append(f"headline already used: {headline(item)}")
    seen.add(h)
    return issues


def caption(item, brand, idx):
    ctas = [x for x in brand["ctas"].split("\n") if x.strip()]
    tags = [x for x in brand["hashtags"].split("\n") if x.strip()]
    return f"{item['caption'].strip()}\n\n{ctas[idx % len(ctas)]}\n.\n{tags[idx % len(tags)]}"


def main(week_path):
    brand_id = os.path.basename(os.path.dirname(week_path))
    brand = json.load(open(os.path.join(ROOT, "brands", f"{brand_id}.json"), encoding="utf-8"))
    items = json.load(open(week_path, encoding="utf-8"))
    seen = used_lines(brand_id)
    problems = []
    for it in items:
        for p in lint(it, brand, seen):
            problems.append(f"{it.get('date')}: {p}")
    if problems:
        print("FAILED CHECKS:\n  " + "\n  ".join(problems))
        sys.exit(1)
    week = os.path.splitext(os.path.basename(week_path))[0]
    payloads = []
    for i, it in enumerate(items):
        rel = f"media/{brand_id}/{it['date']}.jpg"
        render(brand, it, os.path.join(ROOT, rel))
        dt = f"{it['date']}T{brand.get('postTime', '19:45:00')}"
        ordinal = int(it["date"].replace("-", "")) % 1000  # rotates CTA/hashtag sets day to day
        info = {
            "autoPublish": True, "draft": False, "text": caption(it, brand, ordinal),
            "providers": [{"network": "instagram"}], "media": [RAW + rel],
            "mediaAltText": [headline(it).replace("*", "")],
            "publicationDate": {"dateTime": dt, "timezone": brand.get("timezone", "America/Toronto")},
            "firstCommentText": "", "descendants": [], "shortener": False, "smartLinkData": {"ids": []},
            "hasNotReadNotes": False,
            "instagramData": {"type": "POST", "showReelOnFeed": True, "isAiGenerated": False},
        }
        payloads.append({"date": it["date"], "headline": headline(it).replace("*", ""), "media": rel,
                         "args": {"blogId": str(brand["metricoolBlogId"]), "date": dt, "info": json.dumps(info, ensure_ascii=False)}})
    out = os.path.join(ROOT, "payloads", brand_id, f"{week}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(payloads, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK: {len(items)} posters rendered, payloads -> {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main(sys.argv[1])
