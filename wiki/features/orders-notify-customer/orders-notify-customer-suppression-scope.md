---
type: feature
nav_path: "Orders → Order details → Notify customer → Suppression scope"
route_name: admin.orders.notify-customer
route_path: /admin/orders/action/other/:order_id/notify-customer
aliases: ["What notify_customer suppresses", "Notification suppression scope", "Customer email kill switch", "Digital download link exception"]
tags: [orders, notification, customer, email]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders-notify-customer]]. See the hub for the other aspects (the toggle, send-URL flow, manual re-send).

# Notify customer — suppression scope

## Purpose

Exactly which emails the `notify_customer = no` flag suppresses, which it never blocks, the one non-suppressible digital exception, the store-wide kill switch that overrides everything, the queue-delay timing that defeats last-second suppression, and the channels the flag governs. This is the canonical "will the customer get an email?" reference for a single order.

## Where to find it

The flag is the per-order toggle on [[orders-details]] ([[orders-notify-customer-toggle]]). The store-wide kill switch `customer_email_notifications` and each mail's own active flag live on [[marketing-omnichannel-mails-list]]. There is no per-status notification setting — one status-change template covers every status. The combined three-switch model is documented on [[orders-status-change-notification]].

## What the merchant can do here

The merchant reasons about a single order's outbound emails:
- Flip `notify_customer = no` to suppress this order's automated emails (the suppressible set below).
- Know which emails will go out regardless (the non-suppressible set below).
- Check the store-wide kill switch when NO order is emailing.

## Settings & fields

### What `notify_customer = no` SUPPRESSES

The flag gates these automated customer emails:
- **Status change** — every transition that has a notification template configured in [[settings-statuses]].
- **Product fulfillment** — fires when the courier confirms dispatch.
- **Files download link** for NON-digital orders.

### What it does NOT suppress

- **Digital download link on paid / completed.** For orders containing DIGITAL products that transition to `paid` or `completed`, the platform STILL sends the file-download-link email even when `notify_customer = no` — the customer needs the link to access what they paid for. This is the only non-suppressible automated path.
- **Explicit merchant sends.** Manually-triggered invoice / credit-note / receipt sends are direct merchant actions and proceed regardless of the flag. See [[orders-notify-customer-resend]].

### Channels — email only

The platform's customer notifications are email-only. The `notify_customer` flag gates the email pipeline. SMS / push are NOT part of the built-in notification system, so the flag has no effect on them.

## Business rules

### Store-wide kill switch overrides the toggle

The store-wide setting `customer_email_notifications` (on [[marketing-omnichannel-mails-list]]) is the top-level gate. When it is anything OTHER than "yes", NO customer email leaves the platform — regardless of the per-order `notify_customer` flag. A merchant troubleshooting "why aren't emails firing on this order?" should check BOTH the per-order toggle AND the global kill switch. This switch is typically used by stores in test / dev mode and should not be left on for production.

### The three-gate model

A status-change email fires only when ALL THREE allow it: the per-order `notify_customer` flag, the status-change template's own active flag, and the store-wide `customer_email_notifications`. Any one OFF blocks the email. The canonical cross-aspect model is on [[orders-status-change-notification]].

### Email queue delay — under 5 minutes typical

When `notify_customer = yes` AND a status change occurs, the customer email is dispatched onto the `order-events2` queue with a built-in 10-second delay. It is NOT sent synchronously with the status-change request. Typical delivery is a few minutes (depends on queue depth + email-provider throughput). A quick double-click that flips status twice may deliver only the FINAL email — or both, depending on timing — so the merchant cannot rely on instant suppression of an in-flight email. The double-flip behaviour is detailed on [[orders-status-change-notification]].

### Banned-IP auto-suppression

When an order is auto-cancelled because the customer's IP matches the banned-IP list ([[settings-banned-ip]]), the platform automatically sets `notify_customer = 0` BEFORE performing the cancel — so the banned customer is NOT notified of the cancellation. This is one of two automatic flips the platform performs.

### Online-payment commit flow flips notify ON

When the merchant commits a draft with an online payment provider (the "Create order and send to client" / send-URL flow), the platform sets `notify_customer = 1` so the customer receives the checkout-link email. Drafts START with notifications effectively off but get flipped ON when the merchant explicitly commits via the online-payment send flow — see [[orders-notify-customer-send-url]]. This is the second automatic flip.

## Related

- [[orders-notify-customer]] — hub.
- [[orders-notify-customer-toggle]] — the per-order switch this scope governs.
- [[orders-status-change-notification]] — the canonical three-gate model + double-flip detail.
- [[marketing-omnichannel-mails-list]] — the status-change template's active flag + the store-wide kill switch.
- [[settings-cart]] — store-wide `customer_email_notifications` kill switch.
- [[settings-banned-ip]] — auto-cancel auto-flips `notify_customer`.
- [[orders-notify-customer-send-url]] — commit flow auto-flips `notify_customer` ON.
- [[orders-status-change]] — the gated mechanism.
- [[order-processing-pipeline]] — the flag gates emails at every pipeline stage.

## Open questions

None.
