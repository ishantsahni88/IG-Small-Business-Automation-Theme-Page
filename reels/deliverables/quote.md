# The instant quote follow-up workflow (QUOTE)

From the @automatesmallbusiness reel "Stop calling quotes back tomorrow." Written for HVAC, and it works for any trade that gets quote requests from a website form.

## What it does
1. **A homeowner submits your quote form.** The form sends the submission to your automation tool by webhook.
2. **Within a minute, they get a text from your business:** "Thanks for the request. Two quick questions so we can book you in."
3. **It asks two qualifying questions** that matter for your trade, for example: what system is it, and roughly how old?
4. **Their answers sort the lead** into hot (replacement, urgent, in your area), warm, or just browsing.
5. **Hot leads get your booking link right away** and pick a time themselves. Warm leads get a follow-up the next morning.
6. **The booking lands on your calendar,** and the tech gets a job sheet with the customer, equipment and time.
7. **Every step is logged in your CRM,** so nothing depends on someone remembering to call back.

## What you need
| Piece | Common options |
| --- | --- |
| Website form with a webhook | Your site builder's form, Typeform, Jotform, Tally |
| Automation glue | n8n, Make or Zapier |
| Two-way SMS | Twilio, or your field-service tool's texting |
| Lead sorting | Simple rules, or an AI step in n8n or Make that reads the replies |
| Booking link | Calendly, Cal.com, or your field-service tool's online booking |
| Job sheet to the tech | Jobber, Housecall Pro, ServiceTitan, or a text and email |

## Setup checklist
- [ ] Pick your two questions. If an answer wouldn't change what you do next, cut the question.
- [ ] Define "hot" in one sentence the whole team agrees with.
- [ ] Only offer slots you can really keep.
- [ ] Send yourself five test requests (hot, warm, out of area, no reply, nonsense) and check each path.

## Rules worth keeping
- Text from a number people can reply to and reach a human.
- Respect quiet hours for follow-ups.
- Get consent for texts on the form, as your local rules require.

Questions? DM @automatesmallbusiness.
