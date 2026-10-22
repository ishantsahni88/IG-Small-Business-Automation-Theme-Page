# The after-hours call workflow (CALLS)

From the @automatesmallbusiness reel "You miss the 9pm call." This is the workflow behind it, written for a plumbing, HVAC or roofing shop.

## What it does
1. **A call comes in after hours, or while you're on a job.** Your business line forwards unanswered calls to an AI voice agent.
2. **The agent answers in your company's name** and asks one question first: is this an emergency?
3. **It takes the details:** what's wrong, where in the house, the address, and a callback number.
4. **It sorts the call.**
   - Emergency (burst pipe, no heat in winter, active leak): your on-call tech gets a text right away with the address and the problem.
   - Routine (dripping tap, quote request): it offers the next open slot and books it on your calendar.
5. **Everything lands in your CRM:** caller, address, urgency, a short summary, the recording and the transcript.
6. **The customer gets a text confirming** what happens next.

## What you need
| Piece | Common options |
| --- | --- |
| Voice agent | Vapi, Retell, Synthflow |
| Phone number and forwarding | Twilio, or your existing carrier's "forward when unanswered" |
| Automation glue | n8n, Make or Zapier |
| Calendar | Google Calendar, Jobber, Housecall Pro, ServiceTitan |
| CRM | Whatever you already use; a Google Sheet works to start |
| SMS to the tech | Twilio SMS |

## Setup checklist
- [ ] Write your emergency rules in plain words: what counts as urgent, who's on call, and which hours.
- [ ] Give the agent your service area and turn away out-of-area calls politely.
- [ ] Set the forwarding rule: unanswered after a set number of rings, plus outside business hours.
- [ ] Make test calls as a panicked customer, a confused one, and a wrong number.
- [ ] Check that every test call created a CRM record and that emergencies texted the right phone.

## Rules worth keeping
- The agent never quotes a price it can't stand behind; it books the visit.
- A human can always be reached: "press 0" or "say 'person'" goes to your cell.
- Tell callers they're speaking with an automated assistant.

Questions? DM @automatesmallbusiness.
