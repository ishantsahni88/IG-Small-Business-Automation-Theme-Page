# The physio rebooking-by-text workflow (REBOOK)

From the @automatesmallbusiness reel "Stop phoning patients to rebook." Written for physiotherapy clinics, and it works for chiropractic, massage therapy and any appointment-based practice. It is scheduling admin only: the clinician decides whether and when a patient should come back, and the workflow just helps them book it.

## What it does
1. **At the end of each day, it finds patients who were seen today but have no next appointment booked,** and whose clinician marked a follow-up in your booking system (for example "follow-up in 1 week").
2. **Each one gets a text:** a short note that their physio set a follow-up, plus a booking link or three open times that match the clinician's schedule.
3. **They tap a time and it books itself.** The calendar updates and they get a confirmation text.
4. **No reply after two days:** one friendly reminder. Never more than one.
5. **Still no reply:** they go on a short front desk call list for a human to follow up, or close out if the patient says they're done.
6. **Every message and booking is logged** on the patient's file in your booking system.

## What you need
| Piece | Common options |
| --- | --- |
| Booking / practice management system | Jane, Cliniko, WriteUpp, Noterro, or similar, with an API or Zapier/Make connector |
| Follow-up field set by the clinician | A tag, appointment note or custom field your system already has |
| Two-way SMS | Your practice system's built-in texting, or Twilio |
| Automation glue | n8n, Make or Zapier |
| Booking link | Your online booking page, filtered to the right clinician and appointment type |

## Setup checklist
- [ ] Agree with clinicians how they mark a follow-up (one field, used the same way by everyone).
- [ ] Write the first text: clinic name, the clinician's first name, the link, and how to reply STOP.
- [ ] Write the one reminder text. Keep it friendly and short.
- [ ] Decide the timing: same evening or next morning, and how long before the reminder.
- [ ] Exclude patients who were discharged, cancelled, or asked not to be texted.
- [ ] Test it on a staff member: book, reply "not now", reply STOP, and no reply.

## Rules worth keeping
- Admin only. The text never gives treatment advice and never decides who needs care; that comes from the clinician's follow-up note.
- Keep personal health details out of texts. First name, clinician and a link are enough.
- Get consent to text, honour STOP right away, and follow your local privacy rules for patient messaging.
- One reminder, then a human. Nobody gets chased by a bot.

Questions? DM @automatesmallbusiness.
