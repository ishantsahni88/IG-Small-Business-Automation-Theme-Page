# The storm-call photo triage workflow (STORM)

From the @automatesmallbusiness reel "Stop driving to every storm call." Written for roofers, and it works for any trade that gets a flood of requests after bad weather (siding, gutters, restoration, windows).

## What it does
1. **A homeowner fills in your quote form or texts your business number.**
2. **They get a text back within a minute:** thanks, and please reply with a photo of the damage plus where it is (roof, ceiling, attic, siding).
3. **The photo and their answer sort the job:**
   - **Water coming in now** (ceiling stain, dripping, attic leak): flagged urgent.
   - **Exterior damage only** (missing shingles, dented gutters): normal priority.
   - **No photo after a set time:** goes to a short call-back list.
4. **Urgent:** your on-call crew gets a text with the address, the issue and the photo.
5. **Normal:** the homeowner gets your booking link with inspection slots, grouped by area so your routes make sense.
6. **Every request is logged in your CRM** with the photos, address, phone number and status.

## What you need
| Piece | Common options |
| --- | --- |
| Quote form | Your website form, Jobber, ServiceTitan, AccuLynx or JobNimbus request forms |
| Two-way SMS that accepts photos (MMS) | Twilio, or your CRM's texting feature |
| Sorting step | A simple question flow ("Is water coming inside right now?"), optionally an AI model to read the photo and the reply |
| Automation glue | n8n, Make or Zapier |
| Booking | Your CRM's scheduler, Calendly or Google Calendar |

## Setup checklist
- [ ] Write the first text: company name, thanks, what photo you need, and a fallback number to call for emergencies.
- [ ] Decide what counts as urgent, in plain words your crew agrees with.
- [ ] Set who is on call and how they get the text.
- [ ] Block inspection slots by area for the days after a storm.
- [ ] Test it: a leak photo, a shingle photo, no photo, and a reply the system can't read.

## Rules worth keeping
- A person makes the final call on anything flagged urgent. The photo only decides who gets looked at first.
- Anything unclear goes to a human, never to "normal priority".
- Get consent to text, and don't promise arrival times you can't keep.

Questions? DM @automatesmallbusiness.
