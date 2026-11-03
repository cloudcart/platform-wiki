---
type: feature
nav_path: "Orders → Order details → Credit note → Send quirks"
route_name: admin.order.credit.action
route_path: /admin/orders/credit/action/:order_id
aliases: ["Credit note send quirks", "Send credit note behaviour", "Credit note email", "Credit note notify_customer bypass", "Credit note success toast"]
tags: [orders, credit-note, refund, invoicing, notifications]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 7
---
# Credit note — Send behaviour & UI quirks

> Part of [[orders-credit]]. See the hub for the other aspects (actions, eligibility, numbering, document).

## Purpose

The non-obvious behaviour of the **Send credit note** action — the parts that can mislead a merchant or a support agent. Specifically: Send ignores the order's customer-notification suppression, the success toast is unreliable, an ineligible order produces a silent no-op, there is no rate-limit, and external-provider failures surface late. Cite this aspect when a merchant says "the customer says they never got the credit note" despite seeing a success message.

## Where to find it

These behaviours all attach to the **Send credit note** link in the View credit note dropdown on [[orders-details]] (see [[orders-credit-actions]]). There is no separate screen — this aspect documents what happens after the click.

## What the merchant can do here

- Send the credit-note PDF to the customer by email.
- Re-send it (each click queues another delivery).
- Verify actual delivery via the order's history / notifications log, since the toast is not proof of delivery.

## Settings & fields

The Send action POSTs to `POST /admin/orders/credit/action/{order_id}` and queues a customer-notification job through the platform's standard send pipeline. The email body uses the configured per-store credit-note template ([[settings-invoicing-credit-note]]); the customer receives the PDF as an attachment. The merchant does not compose the email content. There are no merchant-editable fields on this aspect — the quirks below are behavioural.

## Business rules

### Send bypasses the `notify_customer` toggle — but not the two email switches

When the merchant clicks Send, the queue dispatches a job to email the credit note with the PDF attachment. There is **NO check** on the order's `notify_customer` flag (per [[orders-notify-customer]]). Even if the merchant has silenced notifications on this order, **clicking Send credit note WILL email the customer**. This is deliberate — Send is a one-shot, merchant-triggered action; the suppression flag only gates automated status-change emails.

Two other switches DO stop the mail, and either one is enough:

1. **The `send_credit_notify` template's own Active toggle** on [[marketing-omnichannel-mails-list]] — off means this specific email never goes out.
2. **The store-wide `customer_email_notifications` setting** — off means no customer emails at all.

Combined with the always-green toast below, this is the usual explanation for "I clicked Send, it said success, the customer got nothing": the template was switched off. See [[omnichannel-mails-toggles-gating]].

### Send silently no-ops when the order is ineligible

The Send POST handler queues the notification job, which internally calls the "issue and get credit note" helper. That helper returns null when the order doesn't meet eligibility (not cancelled / not refunded, OR no invoice number, OR invoicing disabled — see [[orders-credit-eligibility]]). When null is returned, no email is dispatched and the customer receives nothing — yet (see below) the merchant still sees a success toast. The merchant should verify delivery via the order's history / notifications log.

### Both Create and Send handlers always show a success toast

Inspecting the inline JS: `sendCreditNote` calls `toastr.success(response.msg)` on BOTH the success AND error branches (no distinction). So even when the controller returns `status: error` with the failure message, the merchant sees a GREEN success toast displaying the error text. The toast COLOR is not a reliable signal of success for Send. (The `createOrderNote` function does distinguish correctly — `toastr.success` for success, `toastr.error` for error — but the credit-note Send handler does not.)

### Toast is fire-and-forget, not delivery confirmation

Both **Create credit note** and **Send credit note** toasts confirm only that the platform accepted the request — NOT that the customer received an email or that the external provider succeeded. For external providers (Szamlazz, etc.) Send queues the job and any provider-side failure happens later, asynchronously; the merchant sees no follow-up error.

### Re-send is not rate-limited

Each click of Send enqueues another delivery job. There is no debounce or rate-limit, so the merchant can re-fire if the customer didn't get the first email — the recipient simply receives another copy.

### Send creates on the fly

If no credit note exists yet, Send issues one before sending (the issue-and-send chain — see [[orders-credit-actions]]). Combined with the silent no-op above, this means clicking Send on an eligible-but-uncreated order both creates and emails the credit note in one step.

## Related

- [[orders-credit]] — hub.
- [[orders-credit-actions]] — the Send action and the issue-and-send chain.
- [[orders-credit-eligibility]] — why Send can silently no-op.
- [[orders-notify-customer]] — the suppression flag that Send deliberately ignores.
- [[marketing-omnichannel-mails-list]] — where the `send_credit_notify` template's Active toggle lives.
- [[omnichannel-mails-toggles-gating]] — how the per-template toggle and the global switch combine.
- [[orders-invoice-single-customer-email]] — the same gating on the invoice email.
- [[settings-invoicing-credit-note]] — the credit-note document settings.

## Open questions

- Whether the always-green Send toast is ever fixed to distinguish error from success (current behaviour is a known UI quirk).
