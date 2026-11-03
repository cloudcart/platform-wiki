---
type: feature
nav_path: "Orders → Order details → Draft alert → Send notification URL"
route_name: admin.orders.notification.new
route_path: /admin/orders/action/other/:order_id/notification/new
aliases: ["Send notification URL", "Send as email", "Create order and send to client", "Checkout-resume link", "Изпрати известие на клиента"]
tags: [orders, notification, customer, email, draft, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-notify-customer]]. See the hub for the other aspects (the toggle, suppression scope, manual re-send).

# Notify customer — Send notification URL (draft flow)

## Purpose

A ONE-SHOT manual flow, distinct from the persistent toggle: for a DRAFT order awaiting payment, the merchant clicks **Send as email** / **Send notification URL** to e-mail the customer their order's checkout-resume link. For OFFLINE-payment drafts, this same action COMMITS the draft into a live order. This page covers the validation conditions checked before sending and the offline-vs-online split.

## Where to find it

From [[orders-details]] → the **Draft alert** banner shown on a draft order → **Send as email** button.

Route:
- `admin.orders.notification.new` (POST) — dispatches the checkout-resume URL e-mail (and, for offline payment, commits the draft).

This is a separate control from the persistent [[orders-notify-customer-toggle]] switch — that switch is disabled on drafts; this button is the way to reach the customer from a draft.

## What the merchant can do here

- **Send the checkout-resume URL** to the draft customer's email so they can complete the order themselves.
- **Commit an offline-payment draft** into a live order in the same click (see Business rules).

The merchant CANNOT send the URL when the draft fails the pre-send validation below — each failing condition is shown as an error line.

## Settings & fields

### Pre-send validation conditions

Before sending, the platform validates the draft and appends each failure to a list shown together at the top of the error dialog:

1. Order has at least one product, OR error *"Order has no products"*.
2. If the order has shippable products, it must have shipping selected, OR error *"Order has no shipping"*.
3. Order has a payment provider attached, OR error *"Order has no payment"*.
4. If [[settings-cart]] `checkout_require_billing_address = 1`, the order must have a billing address.
5. If the order has ONLY digital products AND [[settings-cart]] `checkout_hide_billing_address = 0`, the order STILL needs a billing address (a separate digital-orders requirement).
6. If the order is digital-only AND `checkout_digital_shipping = 0`, the platform silently DELETES any attached shipping address + shipping record before sending — digital orders don't ship.

A draft with no products AND no payment provider triggers TWO error lines in one response.

## Business rules

### Behaviour depends on payment provider type

| Payment provider | What the send does |
|---|---|
| **Offline** (cash on delivery, bank transfer, etc.) | The platform CONVERTS the draft into a LIVE order: sets `notify_customer = 1`, removes `is_draft`, sends the "New order created" email, and fires the `order.created` webhook. The draft becomes a real order. |
| **Online** | The platform leaves the draft as-is and only emails the customer a checkout-resume URL. The customer must complete payment for the order to become live. |

So "Send notification URL" on an offline-payment draft is not just a notification — it COMMITS the draft.

### Flips notify_customer ON

For both paths the platform sets `notify_customer = 1` so the customer receives the email — this is one of the two automatic flips the platform performs (the other is banned-IP auto-cancel; see [[orders-notify-customer-suppression-scope]]). It is also why a draft, whose toggle starts effectively off, ends up notifying once committed.

### Store-wide kill switch still applies

Even though this is an explicit merchant action, the store-wide `customer_email_notifications` kill switch on [[settings-cart]] still governs whether the email actually leaves the platform — see [[orders-notify-customer-suppression-scope]].

### Distinct from the persistent toggle

The persistent [[orders-notify-customer-toggle]] gates FUTURE automated status emails. This send-URL flow is a single deliberate dispatch (plus, for offline payment, a draft commit). The two should not be confused: flipping the toggle never sends an email; clicking Send as email always attempts one.

## Related

- [[orders-notify-customer]] — hub.
- [[orders-details]] — parent page; the Draft alert hosts the Send-as-email button.
- [[orders-notify-customer-toggle]] — the persistent toggle (disabled on drafts; this flow is how to reach the customer from a draft).
- [[orders-notify-customer-suppression-scope]] — the auto-flip ON + kill-switch override.
- [[settings-cart]] — `checkout_require_billing_address`, `checkout_hide_billing_address`, `checkout_digital_shipping`, `customer_email_notifications`.
- [[orders-payment-manual]] — related payment-link re-trigger path.
- [[orders-add]] — admin draft creation.

## Open questions

None.
