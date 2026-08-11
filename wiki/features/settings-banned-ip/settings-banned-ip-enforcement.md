---
type: feature
nav_path: "Settings → Block Client IP addresses → Enforcement"
route_name: banned-ip.settings
route_path: /admin/settings/banned-ip
aliases: ["Banned IP enforcement", "Auto-cancel banned order", "Online payment exemption", "Ban reason note", "Silent block"]
tags: [settings, security, ban, fraud, ip, order]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[settings-banned-ip]]. See the hub for the other aspects (list & modal, IP formats, scope & limits).

# Block Client IP addresses — enforcement

## Purpose

This aspect documents **what actually happens** when an order arrives from a blocked IP: the server-side post-create auto-cancel, the online-payment exemption, and the customer-facing experience. For the admin UI that maintains the list, see [[settings-banned-ip-list-management]].

## Where to find it

There is no separate screen — enforcement is automatic and server-side. The merchant only configures the list at Sidebar → Settings → **Block Client IP addresses** (`/admin/settings/banned-ip`). Auto-cancelled orders appear in the normal Orders area in the `cancelled` status with a ban-reason administrator note.

## What the merchant can do here

- Nothing to configure for enforcement itself — it runs automatically against the list.
- After the fact, find auto-cancelled orders in [[orders-details]] with status `cancelled` and read the *"Ban reason: …"* administrator note.

## Settings & fields

Enforcement has no merchant-facing fields. Behaviour is keyed on two server-side values:

| Value | Effect |
|-------|--------|
| The blocklist match (request source IP vs stored `ip`) | Triggers the auto-cancel path. |
| `is_online_payment` on the payment-provider record | When `true`, the order is **exempt** from auto-cancel (gateway already cleared funds). When `false` (COD / bank transfer / manual), the order is auto-cancelled. |

## Business rules

### Enforcement is server-side and event-driven

The blocklist check runs in the post-order-created handler. The order row is briefly inserted into the database, then the listener consults the blocklist using the request's source IP. If a match exists AND the payment provider is NOT an online payment, the listener:

1. Sets the order's `notify_customer` flag to `0` (suppresses any confirmation email).
2. Writes the administrator note *"Ban reason: `<description or IP>`"* to the order.
3. Moves the order to the **cancelled** status.

This means the order DID briefly exist in `pending` (or the payment method's initial status) before the cancellation. Database-level analytics will count one "created" order and one cancellation — not a clean rejection; the platform does not suppress the order rows themselves.

### Online-payment exemption — the discriminator field

The exemption is keyed on `is_online_payment` on the payment-provider record (not a hard-coded provider-name list). Any provider the platform marks as "online" (Stripe, PayPal, ePay, CloudCart Pay, etc.) is exempt. Cash-on-delivery, bank transfer, manual payment, etc. all set `is_online_payment = false` and are therefore subject to the auto-cancel.

Online-payment orders are exempted deliberately: the money has already cleared on the gateway, a clean refund would require gateway-side work, and those methods are exactly where the merchant is already protected by the payment processor's own fraud tools.

> The bank-wire-transfer code `bwt` is also explicitly treated as online-payment-equivalent in some other parts of the platform — but for banned-IP purposes the discriminator is purely the `is_online_payment` boolean.

### Customer-facing UX of an auto-cancelled banned-IP order

The customer's experience is intentionally indistinguishable from a normal successful order:

- The storefront shows the standard thank-you page, with the order number.
- **No order-confirmation email is sent** (`notify_customer = 0` is set before the status change).
- The order DOES appear in the customer's account-area order history (if they have a registered account) — but with a `cancelled` status and no confirmation receipt.
- The customer is not told the cancellation reason; the *"Ban reason: …"* note is on the **administrator-note** field, visible only in the admin panel.

This silent treatment is the design intent — denying the fraudster feedback to retry. (The deeper "exact storefront error message vs silent block on rejection" UX edge is the only item the page itself does not fully document.)

### No stock stays locked

Because the order ends in `cancelled`, stock is restored automatically per [[settings-cart]] rules — the banned attempt does not lock inventory away from real customers.

### Invoice number is typically NOT consumed

Whether an invoice number gets consumed depends on the merchant's [[settings-invoicing]] config. If `invoice_generate = auto`, invoice-generation logic skips orders in non-completed payment statuses, so a cancelled order does NOT typically get an invoice issued (no number consumed). If `invoice_generate = manual`, no invoice issues unless the merchant explicitly generates one. So banned-IP cancellations leave the invoice sequence intact in the typical configuration.

### Cache + side effects

CRUD on the list is synchronous and adding an IP takes effect on the next checkout — no propagation delay, no queue, no extra notifications fired beyond the suppressed customer email.

## Related

- [[settings-banned-ip]] — hub.
- [[order]] — the entity that gets auto-cancelled.
- [[orders-details]] — where the cancelled order + ban-reason note appear.
- [[orders-status-change]] — the status-transition mechanism used to set `cancelled`.
- [[order-processing-pipeline]] — the broader post-create order pipeline this check sits in.
- [[checkout-flow]] — the IP check happens during checkout submission.
- [[settings-cart]] — cancelled-order stock-restore rules.
- [[settings-invoicing]] — `invoice_generate` mode that governs whether a number is consumed.

## Open questions

- The exact storefront UX on rejection (error message vs redirect vs silent block) — the design intent is silent, but the precise customer-side surface is not documented by the page itself. (verify)
