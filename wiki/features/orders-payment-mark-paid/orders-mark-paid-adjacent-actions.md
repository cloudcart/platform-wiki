---
type: feature
nav_path: "Orders → Order details → Payment → Mark as paid → Adjacent actions"
route_name: admin.orders.payment.mark_paid
route_path: /admin/orders/action/payment/mark_paid/:payment_id
aliases: ["Sync payment", "Payment lease", "Leasing request", "Adjacent payment buttons", "Multiple payment records", "Split payment workaround"]
tags: [orders, payment, manual-payment, sync, lease, bnpl]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-payment-mark-paid]]. See the hub for the other aspects (form & visibility, post-paid pipeline, status-flip rules, API position).

# Mark as paid — adjacent payment actions

## Purpose

The payment action row on the order details page shows *different* primary buttons depending on the payment's type and status. **Mark as paid** is only one of them. This page documents the buttons that share the row — **Sync payment** (for non-offline pending payments) and **Payment lease** (for credit-type / BNPL payments) — plus the provider exclusions and the multiple-payment-record workaround a merchant uses for split payments. Knowing which button appears prevents the merchant from looking for "Mark as paid" when the platform is instead offering Sync or Lease.

## Where to find it

All three buttons live in the same place — [[orders-details]] → Payment action row (primary `payment/action.tpl`) and the cog-dropdown secondary actions (`payment/details_action.tpl`) next to the payment status badge. Which one shows is decided by the payment's `type` and `status`.

## What the merchant can do here

Depending on the payment, the merchant sees and can click:

- **Mark as paid** — offline + Pending/Requested (the main flow; see [[orders-mark-paid-form]]).
- **Sync payment** — non-offline pending payment on a sync-capable gateway.
- **Payment lease** — credit-type (BNPL) payment in Requested status.

## Settings & fields

These are action buttons, not configurable settings. The relevant attributes are the payment's `type` (`offline` / `credit` / online) and `status` (`pending` / `requested` / `cancelled` / etc.), both set by the checkout flow and the chosen provider.

## Business rules

### Adjacent "Sync payment" button for non-offline pending payments

If the payment is **Pending** but NOT offline-type (e.g., a Pending card payment via Borica, DSK Bank, Btepos, or any gateway whose `sync` method is implemented), the platform shows a different primary button: **Sync payment** (`order.action.payment_sync`, label translated). Clicking it asks the gateway to refresh the payment's current status. Confirmation text: *"Sync payment?"* (`order.payment.confirm.sync`). This is a no-modal action — a pure AJAX call with a confirm dialog.

Sync is *only* surfaced when:
1. Payment status is `pending`, `requested`, OR `cancelled`.
2. Payment is NOT offline-type.
3. The gateway supports the `sync` method (verified set: DSK Bank, BoricaWay4, Btepos, CloudCart Pay, Fibank, Ibank, Icard, CIB Bank, Everypay, Paypal, Settle, TbiBank, PlatiPosle, BNP, DSK BNPL, Monri).

Sync does NOT mark the payment paid — it queries the gateway and updates CloudCart's local state to whatever the gateway reports. If the gateway says "still pending", the local status stays pending. This is the key contrast: **Mark as paid manually overrides; Sync queries the gateway.**

### Lease action — for credit-type payments

For payments with `type = credit` (BNPL: Mokka, Iute, Klear, generic creditor providers) in **Requested** status, the platform's PRIMARY action row shows a **Payment lease** button (`order.action.payment_lease`) INSTEAD of Mark as paid. It calls the credit provider's `sendRequestEmail` flow — which (1) sends the customer a lease-confirmation email with the order's data, and (2) flips the payment status from Requested → Pending. The button confirmation text is *"Send leasing request?"* (`order.payment.confirm.lease`).

For **offline-type credit** payments (a hybrid — credit-type payment with offline characteristics, common with Iute), the SECONDARY cog dropdown shows BOTH Mark-as-paid AND Payment lease as menu items. Mark-as-paid uses the green check-circle icon; Payment lease uses an orange envelope icon (`fa fa-envelope notification-orange`).

**Excluded providers from the lease flow:**
- **`fusion_pay`** — excluded from both primary and secondary lease actions.
- **`klear`** — excluded from both (Klear handles its own re-confirmation outside CloudCart via the dedicated "Confirm Klear" button on the order summary, see [[orders-payment-manual]]).
- **`dsk_bnpl`** — excluded from secondary cog dropdown only.
- **`fibank_bnpl`** — excluded from secondary cog dropdown only.

These providers handle their own re-confirmation via separate flows outside CloudCart's lease mechanism.

### Multiple offline payment records per order

The platform supports multiple payment rows per order. When the merchant uses Change Provider (per [[orders-payment-manual]]) to switch from one payment method to another, a NEW payment row is added. So 50% deposit by bank transfer + 50% on delivery COD is supported via two payment records — but the platform does NOT have a dedicated "record partial payment" UI; the merchant uses the Change Provider flow as a workaround, then marks each record paid via [[orders-mark-paid-form]] as the money arrives.

Beware: on such split orders, marking ONE record paid flips the whole order to "paid" — see [[orders-mark-paid-status-flip]] for the precedence rule.

## Related

- [[orders-payment-mark-paid]] — hub.
- [[orders-mark-paid-form]] — the Mark-as-paid flow itself.
- [[orders-mark-paid-status-flip]] — why marking one record paid flips a split order.
- [[orders-payment-manual]] — Change Provider flow + the Klear re-confirmation button.
- [[settings-payment-providers]] — provider list (offline / credit / online types).
- [[orders-details]] — parent page hosting all three buttons.

## Open questions

None.
