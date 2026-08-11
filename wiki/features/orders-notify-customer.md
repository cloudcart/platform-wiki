---
type: feature
nav_path: "Orders → Order details → Notify customer"
route_name: admin.orders.notify-customer
route_path: /admin/orders/action/other/:order_id/notify-customer
aliases: ["Notify customer", "Notification toggle", "Suppress notifications", "Customer email toggle", "Уведомявай клиента", "Изключи известия"]
tags: [orders, notification, customer, email, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 8
---
# Notify customer toggle

## Purpose

A **per-order toggle** that controls whether the customer receives automated email notifications for status changes on THIS specific order. The merchant uses it when they need to work on an order WITHOUT spamming the customer — test / internal orders, batch back-fills (bulk-completing 100 archived orders shouldn't fire 100 emails), data clean-up on old orders, or honouring a customer's "don't email me about this one" request.

This is NOT a "manual re-send" action — it's a persistent per-order FLAG (`notify_customer`) that gates ALL future automated notifications on the order. A related but distinct one-shot flow (**Send notification URL** / **Send as email**) lets the merchant manually e-mail a draft order's checkout-resume link; that flow can also COMMIT the draft into a live order.

This page is the hub for the cluster. Drill into the aspect that matches the question, rather than reading every page.

## Where to find it

From [[orders-details]] → **Customer sidebar card** → **Notify customer** toggle (with an info-icon tooltip explaining the behaviour).

Routes:
- `admin.orders.notify-customer` (GET) — toggle the `notify_customer` boolean on the order.
- `admin.orders.notification.new` (POST) — the one-shot **Send notification URL** / **Send as email** draft flow (see [[orders-notify-customer-send-url]]).

## Sub-pages (in this cluster)

This page is split into four aspect pages. The Assistant should drill into the aspect that matches the merchant's question, not read every page.

- [[orders-notify-customer-toggle]] — the toggle UI itself: `data-ajax-bool` mechanic, sidebar placement, default-ON / draft-disabled / Site-CP-default-OFF states, per-order persistence, no bulk toggle, no history audit entry.
- [[orders-notify-customer-suppression-scope]] — exactly which emails the flag gates (status / fulfilment / file-link) and which it never blocks (digital download link, explicit invoice / receipt / credit sends); the store-wide `customer_email_notifications` kill switch; queue delay + double-flip risk; email-only channels; banned-IP + commit-flow auto-flips.
- [[orders-notify-customer-send-url]] — the one-shot **Send notification URL** / **Send as email** draft flow: the validation conditions checked before sending, and the offline-vs-online payment behaviour (offline COMMITS the draft into a live order).
- [[orders-notify-customer-resend]] — how to manually re-send each transactional email type (confirmation, payment link, invoice, receipt, credit note, fulfilment, digital link, abandoned-cart link), and how the toggle interacts with each re-send path.

## What the merchant can do here

- Flip the per-order `notify_customer` switch ON / OFF — see [[orders-notify-customer-toggle]].
- Manually send a draft's checkout-resume URL (and, for offline-payment drafts, commit the draft) — see [[orders-notify-customer-send-url]].
- Manually re-fire a specific transactional email (invoice, receipt, credit note, fulfilment, etc.) — see [[orders-notify-customer-resend]].

What the merchant CANNOT do here:
- Suppress notifications for ALREADY-FIRED emails — the toggle gates FUTURE notifications only.
- Configure a per-status override on a single order (e.g. notify on Paid but not Cancelled) — it's binary on/off for ALL statuses on this order. There is no per-status control anywhere: one status-change email template serves every status.
- Bulk-set `notify_customer` from the [[orders]] list — the toggle is strictly per-order. See [[orders-notify-customer-toggle]].

## Settings & fields

### Field: `notify_customer`

| Value | Effect |
|-------|--------|
| **yes** (default for storefront orders) | Customer receives all configured status-change notifications per [[settings-statuses]]. |
| **no** | Customer does NOT receive any automated notification for this order, regardless of [[settings-statuses]] config. |

Orders created through the admin **Add order** flow ([[orders-add]]) default to `notify_customer = no` instead — see [[orders-notify-customer-toggle]]. The full catalogue of what the flag does and doesn't suppress is on [[orders-notify-customer-suppression-scope]].

## Business rules

- **Per-order, persistent flag.** The toggle saves to the order's `notify_customer` field and persists for the order's lifetime. Flipping it sends nothing on its own. To silence ALL orders globally instead, deactivate the status-change template or flip the store-wide kill switch on [[marketing-omnichannel-mails-list]] — see [[orders-notify-customer-suppression-scope]].
- **Draft orders are excluded.** The toggle is disabled in DRAFT state — drafts have no customer-facing existence yet, so there's nothing to notify about. Details on [[orders-notify-customer-toggle]].
- **The three switches.** For a status-change email to actually fire, the per-order flag, the status-change template's own active flag, AND the store-wide `customer_email_notifications` switch must all allow it. The cross-aspect canonical model lives on [[orders-status-change-notification]]; the suppression catalogue is on [[orders-notify-customer-suppression-scope]].
- **No history audit of the flip.** The toggle just updates the column silently — no entry in [[orders-history]]. The merchant cannot later prove who flipped it or when. See [[orders-notify-customer-toggle]].

## Related

- [[orders-details]] — parent page (Customer sidebar card hosts the toggle).
- [[orders-status-change]] — the gated mechanism (status changes that would normally fire emails are suppressed).
- [[orders-status-change-notification]] — the canonical three-gate customer-notification model.
- [[marketing-omnichannel-mails-list]] — the single status-change email template, its active flag, and the store-wide kill switch.
- [[settings-cart]] — `customer_email_notifications` kill switch + `checkout_require_billing_address`.
- [[settings-banned-ip]] — auto-cancel auto-flips `notify_customer`.
- [[orders-add]] — Site-CP add-order flow defaults the flag to OFF.
- [[orders-history]] — verify whether toggle changes appear here (they do not).
- [[order]] — entity page.
- [[order-processing-pipeline]] — the `notify_customer` toggle gates customer emails at every pipeline stage.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
