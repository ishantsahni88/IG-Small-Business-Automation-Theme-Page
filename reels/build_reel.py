"""Validate, render and write the Metricool payload for one Reel episode.

Usage:  python3 reels/build_reel.py reels/episodes/<id>
        python3 reels/build_reel.py reels/episodes/<id> --check     # validate only, no render
        python3 reels/build_reel.py reels/episodes/<id> --no-render # rewrite the payload (e.g. new date), reuse the MP4

An episode folder holds:
  index.html   the seek(t) animation (copy the closest existing episode and change it)
  script.txt   the spoken/caption script, one beat per line
  meta.json    {"id", "date": "YYYY-MM-DD", "hook", "formula", "keyword", "caption", "cover_t", "hashtag_set": 0|1|2}

Checks (all must pass, every problem is printed):
  - hook scores >= 70 on reels/tools/hookscore.py
  - script runs 18-40 s at 165 wpm (reels/tools/beats.py)
  - hook not already used in ledger/small-business-automation-reels.csv
  - caption: 2-3 sentences, no hashtags, no call to action, no % or $ figures
  - reels/deliverables/<keyword>.md exists, so the comment-keyword promise can be kept
Outputs:
  media/small-business-automation/reels/<id>.mp4 and <id>.jpg   (commit + push so raw URLs go live)
  payloads/small-business-automation/reels/<id>.json            (exact createScheduledPost args)
"""
import csv, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REELS = os.path.join(ROOT, "reels")
TOOLS = os.path.join(REELS, "tools")
RAW = "https://raw.githubusercontent.com/ishantsahni88/ig-small-business-automation-theme-page/main/"
BRAND = "small-business-automation"
LEDGER = os.path.join(ROOT, "ledger", f"{BRAND}-reels.csv")


def norm(s): return re.sub(r"[^a-z0-9 ]", "", str(s).lower()).strip()


def tool_json(args):
    out = subprocess.run([sys.executable, *args, "--json"], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def used_hooks():
    if not os.path.exists(LEDGER): return {}
    with open(LEDGER, newline="", encoding="utf-8") as fh:
        return {norm(r["hook"]): r["id"] for r in csv.DictReader(fh)}


def caption_text(meta, brand):
    tags = [x for x in brand["hashtags"].split("\n") if x.strip()]
    # hashtag_set: 0 = trades, 1 = clinics, 2 = general automation (brands/small-business-automation.json)
    idx = int(meta.get("hashtag_set", int(meta["date"].replace("-", "")))) % len(tags)
    return (f"{meta['hook']}\n\n{meta['caption'].strip()}\n\n"
            f"Comment {meta['keyword'].upper()} and I'll send you the workflow.\n.\n{tags[idx]}")


def check(ep):
    issues = []
    meta = json.load(open(os.path.join(ep, "meta.json"), encoding="utf-8"))
    for k in ("id", "date", "hook", "formula", "keyword", "caption"):
        if not meta.get(k): issues.append(f"meta.json missing {k}")
    if issues: return meta, issues
    if meta["id"] != os.path.basename(os.path.normpath(ep)): issues.append("meta.id must match the folder name")
    hs = tool_json([os.path.join(TOOLS, "hookscore.py"), "--hook", meta["hook"]])
    hs = hs[0] if isinstance(hs, list) else hs
    score = hs.get("overall", hs.get("score", 0))
    if score < 70: issues.append(f"hook scores {score:.1f}; needs 70+ (weakest: {min(hs['checks'], key=lambda k: hs['checks'][k]['score'])})")
    b = tool_json([os.path.join(TOOLS, "beats.py"), os.path.join(ep, "script.txt"), "--target", "30"])
    if not 18 <= b["total_seconds"] <= 40: issues.append(f"script runs {b['total_seconds']:.1f}s; keep it 18-40s")
    prior = used_hooks().get(norm(meta["hook"]))
    if prior and prior != meta["id"]: issues.append(f"hook already used by {prior}")
    cap = meta["caption"]
    n = len(re.findall(r"[.!?](\s|$)", cap.strip()))
    if not 2 <= n <= 3: issues.append(f"caption has {n} sentences; write 2-3")
    if "#" in cap: issues.append("caption must not contain hashtags (added automatically)")
    if re.search(r"comment|follow|save this|link in bio", cap, re.I): issues.append("caption must not contain a call to action (added automatically)")
    if re.search(r"\d+\s?%|\$\s?\d", cap): issues.append("caption has a % or $ figure; never invent statistics")
    if not os.path.exists(os.path.join(REELS, "deliverables", f"{meta['keyword'].lower()}.md")):
        issues.append(f"reels/deliverables/{meta['keyword'].lower()}.md is missing; write the workflow the keyword promises")
    meta["_hook_score"] = round(score, 1); meta["_seconds"] = round(b["total_seconds"], 1)
    return meta, issues


def main(ep, only_check=False, no_render=False):
    brand = json.load(open(os.path.join(ROOT, "brands", f"{BRAND}.json"), encoding="utf-8"))
    meta, issues = check(ep)
    if issues:
        print("FAILED", meta.get("id", ep)); [print("  -", i) for i in issues]; sys.exit(1)
    if only_check:
        print(f"OK (check only) {meta['id']}  hook {meta['_hook_score']}  {meta['_seconds']}s"); return
    sys.path.insert(0, os.path.join(REELS, "engine"))
    from render import render
    mdir = os.path.join(ROOT, "media", BRAND, "reels"); os.makedirs(mdir, exist_ok=True)
    mp4, jpg = os.path.join(mdir, f"{meta['id']}.mp4"), os.path.join(mdir, f"{meta['id']}.jpg")
    if no_render and os.path.exists(mp4) and os.path.exists(jpg):
        dur = meta["_seconds"]
    else:
        dur = render(os.path.join(ep, "index.html"), mp4, meta.get("cover_t", 0.6), jpg)
    ver = meta["date"].replace("-", "")
    info = {
        "autoPublish": True, "draft": False, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False,
        "providers": [{"network": "instagram"}],
        "media": [f"{RAW}media/{BRAND}/reels/{meta['id']}.mp4?v={ver}"],
        "videoThumbnailUrl": f"{RAW}media/{BRAND}/reels/{meta['id']}.jpg?v={ver}",
        "mediaAltText": [], "shortener": False, "smartLinkData": {"ids": []},
        "publicationDate": {"dateTime": f"{meta['date']}T{brand['reelTime']}", "timezone": brand["timezone"]},
        "text": caption_text(meta, brand),
        "instagramData": {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": False},
    }
    payload = {"id": meta["id"], "date": meta["date"], "hook": meta["hook"], "keyword": meta["keyword"].upper(),
               "seconds": round(dur, 1), "hook_score": meta["_hook_score"],
               "args": {"blogId": brand.get("metricoolBlogId", ""), "date": f"{meta['date']}T{brand['reelTime']}", "info": json.dumps(info)}}
    pdir = os.path.join(ROOT, "payloads", BRAND, "reels"); os.makedirs(pdir, exist_ok=True)
    json.dump(payload, open(os.path.join(pdir, f"{meta['id']}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"OK {meta['id']}  hook {meta['_hook_score']}  {dur:.1f}s  -> media/{BRAND}/reels/{meta['id']}.mp4")
    if not brand.get("metricoolBlogId"): print("  note: metricoolBlogId is empty, so this payload can't be scheduled yet")


if __name__ == "__main__":
    main(sys.argv[1], "--check" in sys.argv, "--no-render" in sys.argv)
