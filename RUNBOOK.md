# Weekly posting runbook

This repo is the poster engine and public image host for two Instagram pages.
Metricool schedules each post from the image's raw GitHub URL.

| Brand file | Page | Metricool brand ID | Poster templates |
| --- | --- | --- | --- |
| `brands/unhurried.json` | @unhurried_daily | 7195689 | `quote` (mindfulness positive thoughts). **Weekly run skips this brand**: from Nov 21 the "Unhurried weekly autopilot" in `ishantsahni88/unhurried-media` owns it. |
| `brands/small-business-automation.json` | @automatesmallbusiness | not connected yet (the weekly run fills this in once the page appears in Metricool) | `workflow`, `workflow`, `statement` (rotating) |

A brand with an empty `metricoolBlogId` is skipped until the ID is filled in.

## Every week (runs Sunday morning, scheduled task "Small Business Automation weekly autopilot")

For each brand with a `metricoolBlogId`, except Unhurried (owned by the unhurried-media autopilot):

1. **Find the next 7 dates.** Read `ledger/<brand>.csv` and take the 7 days after the last scheduled date. Skip any date already in the ledger. If the ledger is empty, start from the brand's `startAfter` date (or tomorrow).
2. **Write the week** to `weeks/<brand>/<first-date>.json`, following the brand file's `voice`, `audience`, `pillars` and `rules`:
   - `quote`: `quote` of 12 words or fewer, original, positive and believable. The poster shows only the quote (matching the Canva series), so put any extra thought in the caption.
   - `statement`: `headline` of 14 words or fewer with one `*accent*` phrase; `sub` as one sentence.
   - `workflow`: `industry` (HVAC, PLUMBING, DENTAL, PHYSIO, ROOFING or ANY SMALL BUSINESS), `title` of 9 words or fewer, 3–5 `steps` of 34 characters or fewer, `before` and `after` of 9 words or fewer.
   - `caption`: 2–3 short sentences, with no hashtags and no call to action (both are added automatically).
   - Never repeat a line already in the ledger, never invent statistics, and keep healthcare content administrative only.
3. **Self-check before building.** Score each item from 1 to 5 on voice, clarity, specificity and rule compliance. Rewrite any item averaging below 4. Then run
   `python3 engine/build_week.py weeks/<brand>/<first-date>.json`
   and fix and re-run until it prints `OK`.
4. **Publish the images:** commit `weeks/`, `media/` and `payloads/`, then `git push origin main`. Wait until `https://raw.githubusercontent.com/ishantsahni88/ig-small-business-automation-theme-page/main/media/<brand>/<date>.jpg` returns HTTP 200 for every new image.
5. **Schedule:** for each entry in `payloads/<brand>/<first-date>.json`, call Metricool `createScheduledPost` with exactly `entry.args` (`blogId`, `date`, `info`). After each call, run
   `python3 engine/ledger.py <brand> <date> "<headline>" scheduled <metricool id or ->`
   If a call fails, record `failed`, stop that brand, and report the error.
6. **Commit and push** the ledger update.
7. **Report:** dates scheduled per brand, any failures, and the Metricool planner links.

## Rules

- Times come from the brand file (`postTime`, `timezone`).
- Do not edit or delete posts already in Metricool.
- Reels for @automatesmallbusiness run in the same weekly session; see **Reels** below.

## Reels (@automatesmallbusiness only)

Three Reels a week, **Mon, Wed and Fri at `reelTime`** (12:30 Toronto), kept scheduled about 14 days ahead.
Every frame is code: an HTML page with a `seek(t)` function, rendered in headless Chromium and piped to ffmpeg,
with an original soundtrack synthesized by `reels/engine/synth.py`. No generation credits, no licensed audio.

| Path | What it is |
| --- | --- |
| `reels/episodes/<id>/` | `index.html` (animation), `script.txt` (one beat per line), `meta.json` |
| `reels/deliverables/<keyword>.md` | The workflow a viewer gets when they comment the keyword |
| `reels/tools/` | `hookscore.py`, `hooks.json` (26 hook formulas), `beats.py`, `detect.py` from instagram-agent-skill (MIT) |
| `reels/build_reel.py` | Validates, renders MP4 + cover JPG, writes the Metricool payload |
| `ledger/small-business-automation-reels.csv` | Every Reel: id, date, hook, status (`ready`, `scheduled`, `failed`) |

### Every week

1. **Schedule what's ready.** For each `ready` row in the reels ledger: if its date has passed or the slot is taken, move it to the next free Mon/Wed/Fri, update `meta.json`, and run `python3 reels/build_reel.py reels/episodes/<id> --no-render`.
2. **Count the gap.** Work out how many Mon/Wed/Fri slots in the next 14 days have no Reel. Make that many new episodes (normally 3).
3. **For each new episode:**
   - **Topic:** one pillar from the brand file, applied to one industry. Rotate industries (plumbing, HVAC, dental, physio, roofing, any small business) and don't repeat a workflow already in the ledger.
   - **Hook:** write three hooks from three different formulas in `reels/tools/hooks.json`, score them with `python3 reels/tools/hookscore.py hooks.txt`, and keep the best one that has **no invented number**. It must score 70 or more.
   - **Script:** 18 to 40 seconds, one beat per line, ending on a line that echoes a word from the hook. Run `python3 reels/tools/beats.py script.txt --target 30` and fix every flag (hook over 3 seconds, beats over 4 seconds, no loop). Run `python3 reels/tools/detect.py script.txt` and fix anything flagged.
   - **Keyword and deliverable:** pick a one-word keyword not used before and write `reels/deliverables/<keyword>.md` in the same shape as `calls.md`: what it does step by step, what you need, a setup checklist, and the rules.
   - **Animation:** copy the closest episode. `ep001` is scene by scene; `ep002` and `ep003` are one card morphing through every state. Change the content, the `CAP` caption timings (one entry per script line) and the `EVENTS` sound cues. Use the palette: bg `#0d0e0b`, ink `#f3f1ea`, orange `#ff5a1f`, lime `#c8f03c`.
   - **Contact sheet:** `python3 reels/engine/render.py reels/episodes/<id>/index.html sheet.png --sheet`, then look at it. Fix text that's cut off, overlaps the captions or leaves the safe zone (keep content between y=230 and y=1440 and out of the right 230px), cursors that miss what they click, and empty or broken states. Repeat until clean.
   - **Caption:** 2 to 3 sentences, no hashtags, no call to action, no % or $ figures. The hook, the keyword CTA and the hashtags are added automatically. Set `hashtag_set`: 0 for trades, 1 for clinics, 2 for general automation.
   - **Build:** `python3 reels/build_reel.py reels/episodes/<id>` until it prints `OK`. Then `python3 reels/ledger_reel.py <id> <date> "<hook>" ready`.
4. **Publish media:** commit and push. Wait until both raw URLs (the `.mp4` and the `.jpg` under `media/small-business-automation/reels/`) return HTTP 200.
5. **Schedule** (only when `metricoolBlogId` is filled in): for each `ready` Reel inside the 14-day window, first check `getScheduledPosts` for that date and skip it if a REEL is already there. Otherwise call `createScheduledPost` with exactly `args` from `payloads/small-business-automation/reels/<id>.json`, then run `python3 reels/ledger_reel.py <id> <date> "<hook>" scheduled <metricool id>`. On an error, record `failed`, stop scheduling Reels and report it.
6. **Commit and push** the ledger, then include the Reels in the weekly report: what was scheduled, the hooks and their scores, and every new keyword. Ishant has to deliver each keyword's workflow by DM.

### Reel rules
- Instagram allows at most 5 hashtags per post. Each set in the brand file has exactly 5; never add more.
- An episode may carry `caption_full` in `meta.json` (a finished caption written and linted for it); `build_reel.py` then uses it as-is.
- Never invent clients, results, revenue, call counts or statistics. Names, addresses and numbers on screen are clearly fictional (555 phone numbers).
- Healthcare Reels show scheduling and admin only, never clinical decisions.
- One idea per Reel and one ask at the end.
- Requirements: Python 3 with `playwright`, `numpy` and `scipy`, plus ffmpeg and Chromium. If they're missing, run `pip install --break-system-packages playwright numpy scipy`; Chromium is preinstalled at `/opt/pw-browsers`.
