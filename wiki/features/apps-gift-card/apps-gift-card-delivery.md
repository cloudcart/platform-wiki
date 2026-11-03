---
type: feature
nav_path: "Storefront → Gift cards page → Send to"
route_name: ""
route_path: ""
aliases: ["Gift card delivery", "Send gift card to recipient", "Schedule gift card", "Send on", "Resend gift card", "Gift card not received", "Изпрати на", "Изпращане на подаръчен ваучер", "Изпрати отново подаръчен ваучер"]
tags: [apps, gift-card, email, delivery]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Gift Card — delivery

> Part of [[apps-gift-card]]. See the hub for the other aspects.

## Purpose

Who receives a gift card, when, and in what form. A card is delivered as a PDF attached to an email. The code itself is never in the email text.

## Where to find it

The buyer chooses on [[storefront-gift-card]] under `Send to` / `Изпрати до`. What was sent shows under the **Delivery** column on [[customer-gift-cards]]. The merchant sees the recipient on [[apps-gift-card-cards]].

## What the merchant can do here

- Edit the two emails on [[apps-gift-card-emails]].
- Change the PDF on [[apps-gift-card-pdf-template]].

The buyer controls the recipient, the date and any resend. The admin has no resend button; the merchant can open the PDF with **View** on [[apps-gift-card-cards]].

## Settings & fields

No settings of its own. The buyer's choices:

| Field | Rules |
|---|---|
| `Send to` | `My email` / `Моя имейл` (default), or `Recipient's email` / `Имейл на получател` |
| `Recipient email (optional)` | Required when sending to a recipient. Valid email, max 191 |
| `Recipient name (optional)` | Max 191 |
| `Message (optional)` | Max 200 |
| `Send on (optional)` / `Изпрати на (по избор)` | A date, today or later. *"Leave empty to send immediately."* |

## Business rules

### The buyer always gets every card, right away

One email with all the order's new cards attached as PDFs goes to the buyer as soon as the cards are issued, even when a recipient's email is scheduled for later. The **Send on** date only holds the recipient's email.

### The recipient gets one email per address

All of a recipient's cards from that order arrive in one email, each as its own PDF. With several recipients, each gets their own email.

### Send on

- With a future date, the recipient's email waits until that date.
- An empty date, or today's date, sends at once.
- The delivery lands on the chosen date, not at a set time. A background check looks for due cards every few hours.
- The email is not sent if the card's code has lapsed by then or the card is no longer active, for example because its order was cancelled.

### Resend

**Resend** (`Изпрати отново`) is on the buyer's [[customer-gift-cards]] page, and only for a card with a recipient. It sends the recipient email again for that card, with its current PDF, and updates the **Delivery** date. Success: `The recipient email has been resent.` Failure: `Could not send. Please try again.`

### Delivery status for the customer

The **Delivery** column shows `Scheduled for` / `Насрочен за` with the date, or `Sent on` / `Изпратен на` with the date.

### Email text and the global switch

These two emails ignore the store's global customer notifications switch, so a card is always delivered. See [[apps-gift-card-emails]].

### Language

Each email and its PDF use the language of the order.

### Opening the card without an account

A recipient opens the card's page and PDF from the email without an account. An account is needed only to redeem. See [[apps-gift-card-redeem]] and [[storefront-gift-card]].

## Related

- [[apps-gift-card]] — hub.
- [[apps-gift-card-emails]] — the two templates.
- [[customer-gift-cards]] — the buyer's list and **Resend**.
- [[storefront-gift-card]] — the form.
- [[apps-gift-card-reversal]] — why a scheduled card might not go out.

## Open questions

- Whether the recurring check for scheduled sends is running in production. It is registered by a staff-run command. (verify)
