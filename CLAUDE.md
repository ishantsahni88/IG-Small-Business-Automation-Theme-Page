# IG poster engine

- Follow `RUNBOOK.md` for the weekly posting run. It is the source of truth.
- Brand voice, rules, colours, CTAs and hashtag sets live in `brands/*.json`. Change them there, not in code.
- `engine/build_week.py` validates, renders and writes Metricool payloads. Never hand-write `info` payloads.
- `ledger/*.csv` is the record of what has been scheduled. Update it after every Metricool call.
- Fonts in `engine/fonts` are SIL Open Font License (Inter, Cormorant Garamond, JetBrains Mono).
- Requires Python 3 with Pillow (`pip install pillow`).
