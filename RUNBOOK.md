# Weekly posting runbook

This repo is the poster engine and public image host for two Instagram pages.
Metricool schedules each post from the image's raw GitHub URL.

| Brand file | Page | Metricool brand ID | Poster templates |
| --- | --- | --- | --- |
| `brands/unhurried.json` | @unhurried_daily | 7195689 | `quote` (mindfulness positive thoughts) |
| `brands/small-business-automation.json` | @automatesmallbusiness | not connected yet | `workflow`, `workflow`, `statement` (rotating) |

A brand with an empty `metricoolBlogId` is skipped until the ID is filled in.

## Every week (run on Monday)

For each brand with a `metricoolBlogId`:

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
- Reels are not part of this weekly run.
