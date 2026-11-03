---
type: entity
nav_path: "Entity → Credit Note → Send flow"
aliases: ["Send credit note", "Credit Note send", "Credit Note email", "Credit Note notify_customer bypass", "Issue-and-send", "Credit Note re-send", "Credit Note rate-limit"]
tags: [entity, finance, invoicing, refund, credit-note, notifications]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[credit-note]]. See the hub for the other aspects (attributes, lifecycle, numbering, template rendering, external providers).

# Credit Note — Send flow

## Identity

This page documents **how the Credit Note gets delivered to the customer** when the merchant clicks **Send credit note** on the [[orders-credit]] dropdown. The Send action has three distinctive behaviours the merchant must understand: (1) it **bypasses** the Order's `notify_customer` flag (sends even when notifications are silenced), (2) it **chains issuance** with delivery (creates the Credit Note on the fly if one doesn't yet exist), and (3) it has **no debounce** (each click queues a fresh delivery, the customer gets duplicates if the button is double-clicked).

## Aliases

- **Send credit note** — the merchant-facing button label.
- **Credit Note email** — the notification email carrying the PDF attachment.
- **Issue-and-send chain** — the internal flow that creates-then-delivers in one action.
- **Изпрати кредитно известие** — Bulgarian label.

## Key Attributes

| Aspect | Behaviour | Notes |
|--------|-----------|-------|
| Trigger | Click **Send credit note** on the [[orders-credit]] dropdown | Surfaces on [[orders-details]] header toolbar. |
| Toast on success | *"Credit note sent"* | Asynchronous — the toast confirms queueing, not delivery. |
| Delivery mechanism | Standard customer-notification pipeline | Queues a job; email goes out asynchronously. |
| Template used | Configured per-store Credit Note email template | Merchant edits in platform notification settings; not composed per-order. |
| `notify_customer` flag | **Bypassed** (see below) | Deliberate distinction from automated status-change emails. |
| Auto-create on Send | **Yes** — issues the Credit Note if it doesn't exist | The issue-and-send chain (see below). |
| Rate limit / debounce | **None** | Each click queues another delivery — see below. |
| Attachment | The rendered Credit Note PDF | Re-rendered fresh per send — see [[credit-note-template-rendering]]. |

## Send bypasses the `notify_customer` flag

When the merchant clicks **Send credit note**, the platform queues a job to email the Credit Note PDF to the customer.

There is **NO check** on the Order's `notify_customer` flag (per [[orders-notify-customer]]). Even if the merchant has globally silenced notifications on this order, clicking **Send credit note** WILL email the customer.

This is a **deliberate distinction**:

- The `notify_customer` flag suppresses **automated** status-change emails (when the order moves to `cancelled`, `refunded`, etc.).
- The Send action is a **one-shot, merchant-triggered** action — explicit intent to deliver. The suppression flag does not apply.

Merchant operational consequence: the merchant cannot rely on `notify_customer = no` to prevent the Credit Note email. If the merchant truly wants no email, they should NOT click Send — they should issue the Credit Note via **Create credit note** and let the merchant download the PDF separately for offline delivery.

## Issue-and-send chain

The Send flow internally **issues-AND-fetches** the Credit Note — so if no Credit Note has been created yet, **Send credit note will create one on the fly** before sending. The merchant can skip the Create step if they're confident the Order is eligible and just click Send directly.

Sequence when Send is clicked on an Order with no existing Credit Note:

1. Check eligibility (per the active Invoicing provider).
2. Issue the Credit Note (consume next number from sequence — see [[credit-note-numbering]]).
3. Stamp `credit_number` + `credit_date` on the Order.
4. Queue the email with the freshly-rendered PDF attached.

Sequence when a Credit Note already exists:

1. Skip issuance (number is already permanent — see [[credit-note-lifecycle]]).
2. Re-render the PDF from current Order data.
3. Queue the email with the PDF.

This convenience means a merchant who clicks Send without first clicking Create still gets a Credit Note issued — and once issued, the number is permanent (no undo without contacting support — see [[credit-note-lifecycle]]).

## Re-send is not rate-limited

Each click of **Send credit note** enqueues another delivery job. There is **no debounce, no soft rate-limit, and no confirmation dialog** after the first send — each click queues a new outgoing email with the PDF attached.

Merchant operational consequence: if the customer didn't receive the first email, the merchant can re-fire the action. The recipient simply gets another copy. The merchant **should avoid double-clicking** the action — each click is a separate email.

## Customer notification email uses the configured template

The Send action uses the configured Credit Note email template — the merchant doesn't compose the email content per-Order. The customer receives a **PDF attachment** plus the **templated email body**. To customise wording, the merchant edits the Credit Note email template in the platform notification settings.

The email subject, body, and reply-to address all come from the merchant's per-store template configuration — not from anything on the Order or the Credit Note itself.

## No dedicated `credit_note.*` webhook event

The Credit Note creation handler does **NOT** dispatch a dedicated `credit_note.*` webhook event. If the underlying [[order|Order]] is also updated as a side effect of issuing the Credit Note, the `order.updated` event fires (standard order-update payload), but receivers cannot subscribe specifically to "a Credit Note was issued".

External integrations that need to track Credit Notes should:

- Reconcile on the Order's `credit_number` field (poll for non-null).
- Subscribe to `order.updated` and check whether `credit_number` changed.
- Pull the Order detail via the JSON-API v2 endpoint after status transitions.

See [[settings-hooks]] for the available webhook event taxonomy.

## Permission and side effects

- Standard orders permission scope (no extra permission to Send).
- **Send credit note** → may issue the Credit Note (if not yet issued) AND queues a job in the customer-notification pipeline.
- The email delivery happens asynchronously via the standard notification queue.

## Where it appears

- [[orders-credit]] — the per-order Credit Note generation + download + send flow.
- [[orders-details]] — the order detail hub; the **View credit note** dropdown lives in the header toolbar.
- [[orders-notify-customer]] — the `notify_customer` flag this Send action bypasses.
- [[notification-delivery]] — the platform's customer-notification queue/pipeline.
- [[settings-hooks]] — the webhook event taxonomy (no dedicated `credit_note.*` event).

## Related

- [[credit-note]] — hub.
- [[orders-credit]] — the per-order action.
- [[orders-notify-customer]] — flag the Send action bypasses.
- [[notification-delivery]] — when the merchant sends the Credit Note, the platform queues an email to the customer with the PDF attached.
- [[orders-details]] — the order detail hub where the Send button surfaces.
- [[settings-hooks]] — webhook taxonomy (no Credit Note-specific event).

## Open Questions

None.
