# The invoice reminder-by-text workflow (PAID)

From the @automatesmallbusiness reel "Stop chasing invoices by phone." Works for any small business that invoices after the job: trades, cleaners, landscapers, clinics' private-pay balances, agencies.

## What it does
1. **Every morning it checks your accounting software for invoices past their due date.**
2. **First reminder (a few days overdue):** a polite text, and optionally an email, with the invoice number and a pay-by-card link.
3. **Second reminder (a few days later):** one shorter, friendly nudge with the same link.
4. **The moment it's paid, it stops.** Your accounting software marks the invoice paid and no further messages go out.
5. **Still unpaid after two weeks (or whatever you choose):** it creates a task for you or your office with the customer's details and the message history, so a person makes the call.
6. **Everything is logged** on the invoice or customer record.

## What you need
| Piece | Common options |
| --- | --- |
| Accounting / invoicing | QuickBooks Online, Xero, FreshBooks, Wave, or your field-service tool (Jobber, Housecall Pro, ServiceTitan) |
| Online payment link | Stripe, Square, or your accounting tool's built-in card payments |
| SMS | Twilio, or your CRM / field-service tool's texting |
| Automation glue | n8n, Make or Zapier (many accounting tools also have basic built-in reminders) |
| Task list | Your CRM, Asana, Trello, or a simple email to the office |

## Setup checklist
- [ ] Choose the timing: days after due date for reminder 1, reminder 2 and the hand-off to a human.
- [ ] Write both texts: business name, invoice number, the link, and a number to call with questions. Keep them friendly.
- [ ] Exclude invoices that are disputed, on a payment plan, or marked "don't remind".
- [ ] Make sure a payment instantly updates the invoice status, so nobody gets reminded after paying.
- [ ] Test it: an overdue invoice, one paid after reminder 1, one partly paid, and one disputed.

## Rules worth keeping
- Two reminders, then a person. Never an endless loop.
- Only text customers who agreed to receive texts, and honour STOP right away.
- Polite and factual: no threats, no late fees you haven't agreed in writing.
- Don't put sensitive details in the text. Invoice number and a link are enough.

Questions? DM @automatesmallbusiness.
