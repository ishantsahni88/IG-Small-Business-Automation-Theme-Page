# The no-show prevention workflow (CHAIR)

From the @automatesmallbusiness reel "No-shows cost you a chair." Written for dental clinics, and it works for physio, chiro and any appointment-based practice. **Scheduling admin only. No clinical advice or decisions.**

## What it does
1. **At a set time the day before** (for example 4pm), every patient booked for tomorrow gets a reminder text.
2. **Patients reply C to confirm or R to reschedule.**
3. **Confirmed:** the appointment is marked confirmed in your schedule. Nobody calls.
4. **Reschedule:** the patient sees open slots and picks one, and the old slot is freed.
5. **A freed slot is offered to your waitlist automatically,** first come, first served, until someone books it.
6. **No reply by a set time on the morning** (for example 9am): those patients go on a short call list for the front desk.
7. **Everyone else is already sorted** before the clinic opens.

## What you need
| Piece | Common options |
| --- | --- |
| Practice management or scheduling system | Dentrix, Open Dental, Jane, Cliniko, or whatever you use (check its API or built-in reminders first) |
| Two-way SMS | Twilio, or your PMS's texting feature |
| Automation glue | n8n, Make or Zapier |
| Waitlist | A simple list in your PMS, or a Google Sheet to start |

## Setup checklist
- [ ] Check what your practice management system already does; many have reminders built in, and you only need the waitlist and call-list pieces.
- [ ] Write the reminder text: clinic name, day, time, and how to reply. Keep health details out of it.
- [ ] Decide your cut-off times: when reminders go out, and when non-replies go to the call list.
- [ ] Test with staff phones: confirm, reschedule, no reply, and a reply the system doesn't understand.

## Rules worth keeping
- Keep messages administrative: no diagnosis, treatment or clinical details in texts.
- Follow your province or state's privacy rules for patient communication, and get consent to text.
- Any reply the system doesn't understand goes to a human.

Questions? DM @automatesmallbusiness.
