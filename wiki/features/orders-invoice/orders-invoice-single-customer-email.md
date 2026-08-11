---
type: feature
nav_path: "Orders → Order details → Invoice → Customer email"
route_name: admin.orders.generate.invoice
route_path: /admin/orders/generate-invoice/:order_id
aliases: ["Invoice customer email", "sendInvoice", "Invoice email notification", "Invoice generation failure", "Re-issue invoice", "Имейл с фактура до клиента"]
tags: [orders, invoice, invoicing, email, notifications]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-08-06
source_count: 7
---
> Part of [[orders-invoice]]. See the hub for the other aspects (action surfaces, numbering, eligibility, rendering).

# Invoice — customer email & failures (per order)

## Purpose

Documents the **side effects of generating an invoice number**: the email with the PDF attachment that the platform sends to the customer, the global-only setting that gates it, how external-mode (mode 3) failures are handled, and why re-issuing an invoice is not supported. This is the aspect to read for "the customer got an unexpected invoice email" and "the external app failed to issue a number" tickets.

## Where to find it

The email fires automatically after a successful invoice-number assignment (Surfaces A and B on [[orders-invoice-single-surfaces]]). There is no separate screen — the behaviour is observed on the order timeline of [[orders-details]] and in the customer's inbox.

## What the merchant can do here

- Stop the customer email BEFORE issuing the invoice, in either of two places: switch the **`send_invoice`** email template off on [[marketing-omnichannel-mails-list]], or disable the store-wide `customer_email_notifications` setting (see Business rules — the per-order flag does not help here).
- Retry a failed external-mode generation, or temporarily switch the numbering mode on [[settings-invoicing]] as a fallback.

## Settings & fields

The behaviour reads the store-wide `customer_email_notifications` toggle, the **Active** toggle on the `send_invoice` email template ([[omnichannel-mails-toggles-gating]]), and the `invoice_number_type` mode from [[settings-invoicing]] (see [[orders-invoice-single-numbering]]).

## Business rules

### The email fires in EVERY generation mode

Whenever an invoice number is assigned — automatically by the pipeline, or manually from the order page, in any of the three number modes — the platform queues a send-invoice job that emails the PDF (file name `invoice_<number>.pdf`) using the `send_invoice` template. There is no "issue quietly" option at generation time.

### Two switches can stop it — the per-order flag is not one of them

The job IGNORES the per-order `notify_customer` flag. Two other switches DO stop it, and either one is enough:

1. **The `send_invoice` template's own Active toggle** on [[marketing-omnichannel-mails-list]] — turn that template off and no invoice email is sent, even with global notifications on.
2. **The store-wide `customer_email_notifications` setting** — off means no customer emails at all.

Merchants who issue invoices for archival purposes (not wanting to disturb the customer) usually want option 1, since it targets just this one email. This is the single most common surprise: the per-order "notify customer" toggle has NO effect on the invoice email.

The same two switches govern the credit-note email, through the `send_credit_notify` template — see [[orders-credit-send-quirks]].

### Invoice language follows the order

The emailed PDF is rendered in the order's locale (then site primary, then admin) — see [[orders-invoice-single-rendering]]. The email itself follows the customer's order context, not the merchant's session language.

### External-mode failures don't block the order

When an external Invoicing app (mode 3) returns null (API down or rejection), the route returns an error response *"Could not generate invoice"*. The order is NOT blocked — the merchant can retry later, or temporarily switch the mode in [[settings-invoicing]] to manual / auto. The order remains usable for shipping, payment, etc.

### Re-issuing invoice — not supported via the UI

The platform consumes invoice numbers sequentially and persists them on the order (see [[orders-invoice-single-eligibility]] for permanence). There is no merchant-facing "re-issue invoice with corrected number" action — once an invoice number is assigned, it's part of the audit trail. To correct mistakes the merchant typically issues a credit note via [[orders-credit]] and creates a new corrected order.

## Related

- [[orders-invoice]] — hub.
- [[marketing-omnichannel-mails-list]] — where the `send_invoice` template's Active toggle lives.
- [[omnichannel-mails-toggles-gating]] — how the per-template toggle and the global switch combine.
- [[orders-credit-send-quirks]] — the same gating on the credit-note email.
- [[settings-invoicing]] — provider mode + template settings.
- [[orders-invoice-single-rendering]] — the PDF that gets attached + its render language.
- [[orders-invoice-single-eligibility]] — number permanence behind the no-re-issue rule.
- [[orders-credit]] — credit-note path for corrections.
- [[orders-details]] — where the timeline / email side-effects appear.

## Open questions

None.
