---
type: feature
nav_path: "Orders → Order details → Status → Customer notification"
route_name: admin.orders.change-status
route_path: /admin/orders/action/status/:order_id/:status
aliases: ["Status change customer notification", "Customer email on status change", "notify_customer flag", "Notification gating", "Notification kill switch"]
tags: [orders, status, notification, email]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[orders-status-change]]. See the hub for the other aspects (pill, transition rules, side effects, fulfillment gate, bulk, API).

# Order status change — Customer notification

## Purpose

Every status change can — but does not always — send the customer an email. There is **one status-change email template shared by every status**; it is not per-status, and the status list on [[settings-statuses]] offers nothing but a name field. Whether that one email goes out is decided by **three switches**, all of which must allow it. This page is the canonical model of those switches plus the queue-delay behaviour that creates the "double-flip" risk. Bulk status changes follow the same gating, which is why bulk-completing 100 orders can result in 100 outbound emails (see [[orders-status-change-bulk]]).

## Where to find it

- **Per-order flag**: `notify_customer` on [[orders-details]] (the right-rail toggle, documented on [[orders-notify-customer]]). The merchant flips this BEFORE changing status to suppress / enable the email for that specific order.
- **The template's own on/off**: the status-change customer mail in the customer-mail list ([[marketing-omnichannel-mails-list]]). Deactivating it silences the status-change email for the whole store, for every status.
- **Store-wide kill switch**: `customer_email_notifications`, on the same customer-mails screen. Anything other than "yes" suppresses ALL customer-notification emails store-wide.

## What the merchant can do here

### The three switches — ALL must allow it

The customer-notification email on a status change fires ONLY when all three allow it:

1. **Per-order**: `notify_customer = 1` on this specific order (the [[orders-notify-customer]] right-rail toggle).
2. **Per-template**: the status-change customer mail is **active** in [[marketing-omnichannel-mails-list]].
3. **Store-wide**: `customer_email_notifications = "yes"`.

Any one switch in the OFF position blocks the email. There is NO per-change inline toggle and **no per-status toggle** — the merchant cannot say "email on Completed but not on Paid". The single template covers them all; its body reflects whichever status the order is in when the email is rendered.

### Per-order silencing — flip BEFORE the status change

To silence the email for a single order, the merchant must flip `notify_customer = no` FIRST (via the right-rail toggle on [[orders-notify-customer]]), THEN change the status. After-the-fact silencing is impossible — once the change has been processed, the email is already queued.

### Store-wide silencing — the two blunt instruments

Deactivating the status-change customer mail in [[marketing-omnichannel-mails-list]] silences status-change emails across the whole store while leaving order confirmations and everything else alone. The `customer_email_notifications = "no"` switch on the same screen silences EVERY customer notification email store-wide — order confirmations, status changes, abandoned-cart, the lot. That one is typically used only by stores running in test / dev mode.

### The admin copy rides on the customer email

The store's own "order status changed" notification is not an independent notification — it is sent from inside the same step as the customer email. So an order with `notify_customer = 0`, or a store with the status-change template deactivated, sends **neither** copy. Merchants who expect an internal alert on every status change and have suppressed customer emails will not get one.

### Banned-IP auto-cancel — automatic silencing

The banned-IP auto-cancel flow (see [[settings-banned-ip]]) flips `notify_customer = no` before cancelling the offending order — so banned customers are NOT notified when their orders are auto-cancelled. The platform handles this automatically; the merchant doesn't have to configure it.

## Settings & fields

| Setting | Page | Effect when OFF |
|---------|------|----------------|
| `notify_customer` | Per-order toggle on [[orders-details]] | This specific order's status changes don't email the customer (and don't email the store either) |
| Status-change mail active flag | [[marketing-omnichannel-mails-list]] | No status-change email for any order, store-wide |
| `customer_email_notifications` | [[marketing-omnichannel-mails-list]] | Store-wide silence on all customer notifications |

## Business rules

### Queue delay — ~10 seconds, and the email is rendered at SEND time

When the switches pass, the platform queues the customer email with a **~10-second delay**. The queued job carries only the order's identifier — the template is rendered when the job runs, from the order as it looks **then**.

That has a concrete consequence: **two status changes inside that window produce two emails that both show the final status.** A merchant who goes Paid → Cancelled quickly does not get one "paid" mail and one "cancelled" mail; they get two "cancelled" mails.

### Double-flip risk

Beyond the duplicate-content case above, queue ordering is not strictly guaranteed under load, so rapid flips can also arrive out of order. The merchant should avoid quick double-flips on customer-facing transitions. There is no dedupe by order + status.

### Gateway-driven changes usually send nothing

A routine online payment moving the order `pending → paid` from the gateway's return / webhook path sends **no** status-change email at all — that half of the cascade is deliberately skipped, because the order was already announced at creation. Cancellations and recoveries from a negative status are the exceptions and do send. See [[orders-status-change-side-effects]]. This is the usual explanation for *"the customer never got the paid email"* on an online-payment order.

### Bulk multiplier

Bulk status changes do not bypass the gating — every selected order runs through the same three switches. So bulk-completing 100 orders where all three allow it will fire 100 outbound emails. Before a large bulk operation the options are: pre-flip `notify_customer = no` on the selected orders, or deactivate the status-change template for the duration. See [[orders-status-change-bulk]].

### Custom statuses

Custom statuses (merchant-defined) use the same single template and the same three switches. There is no separate notification behaviour for them.

### Digital download links bypass the per-order flag

For `paid` / `completed` orders containing digital products, the download-link email is queued **even when `notify_customer = 0`** — the customer paid for those files. Only the store-wide switch and the template's own flag can stop it.

### "Send notification" does not send anything

The notification control on [[orders-notify-customer]] only flips the order's `notify_customer` flag on or off. It does **not** send an email, and there is no way to re-send the status email for the current status. To make an email go out, the merchant must apply a status change with the flag on.

### Cancel without emailing — the standard workflow

1. Flip `notify_customer = no` via the right-rail toggle ([[orders-notify-customer]]).
2. Change status to `Cancelled` via the pill ([[orders-status-change-pill]]) or the 3-dot dropdown's **Cancel order** action.

## Programmatic access

JSON-API v2 PATCH of `status` honours all three switches — the API does not bypass any of them. The `notify_customer` flag on the order can also be PATCHed via the API before the status change. See [[orders-status-change-api]].

## Related

- [[orders-status-change]] — hub.
- [[orders-notify-customer]] — the per-order `notify_customer` toggle.
- [[marketing-omnichannel-mails-list]] — the status-change template, its active flag, and the store-wide kill switch.
- [[settings-statuses]] — status taxonomy (rename / add custom); no notification settings live here.
- [[settings-banned-ip]] — auto-cancel auto-flips notify_customer.
- [[orders-status-change-bulk]] — multiplier risk on bulk operations.
- [[orders-status-change-side-effects]] — full side-effect chain, including the gateway-path suppression.
- [[orders-status-change-api]] — API honours the same three switches.

## Open questions

None.
