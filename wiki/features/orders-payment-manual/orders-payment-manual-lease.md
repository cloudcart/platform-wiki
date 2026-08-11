---
type: feature
nav_path: "Orders → Order details → Payment → Lease (re-confirm credit)"
route_name: admin.orders.payment.lease
route_path: /admin/orders/action/payment/lease/:order_id
aliases: ["Payment lease", "Lease payment", "Re-confirm credit", "Credit re-confirmation", "Mokka lease", "Iute lease", "Повторно потвърждение на кредит"]
tags: [orders, payment, lease, bnpl, credit, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---

> Part of [[orders-payment-manual]]. See the hub for related aspects (Mokka confirm, Klear confirm, change provider, API access).

# Payment Lease — credit re-confirmation

## Purpose

The **Payment Lease** action re-sends a credit re-confirmation request to the customer for **credit-type BNPL** orders that are still in `requested` status — i.e., the customer started a credit application at checkout but hasn't finished confirming it with the provider. Clicking Lease prompts the credit provider to re-issue the confirmation request to the customer, nudging a stalled credit application forward. It is **distinct from** manual confirm (which captures an already-approved credit at dispatch).

## Where to find it

From [[orders-details]], in the order-actions summary, the platform shows a **Payment Lease** button **instead of** the standard Mark-as-paid button when the order's payment provider is a credit-type BNPL (Mokka, Iute, generic credit) AND the order is in `requested` status.

Route: `/admin/orders/action/payment/lease/{order_id}` `(verify exact route)`. The button sends the customer a re-confirmation request via the credit provider.

## What the merchant can do here

Click **Payment Lease** to trigger a re-confirmation request to the customer via the credit provider. This is useful when a customer's credit application is stuck in `requested` and the merchant wants to prompt them to complete it.

### What the merchant CANNOT do here

- Use Lease for providers outside the credit-type set — FusionPay, Klear, DSK BNPL, and Fibank BNPL are explicitly excluded (those providers handle their own re-confirmation outside CloudCart).
- Use Lease once the credit is already approved (order in `paid` / `completed`) — at that stage the merchant uses manual confirm (Mokka via [[orders-payment-manual-mokka]], Klear via [[orders-payment-manual-klear]]) to capture, not Lease.
- Approve the credit themselves — only the customer + the credit provider can complete the application; Lease merely re-issues the request.

## Settings & fields

This is a no-input action — there are no merchant-editable fields. Eligibility is driven entirely by the order's provider + status.

| Condition | Value |
|-----------|-------|
| Provider | Credit-type BNPL: Mokka, Iute, generic credit |
| Order status | `requested` |
| Excluded providers | FusionPay, Klear, DSK BNPL, Fibank BNPL |

## Business rules

### Lease replaces Mark-as-paid for credit-type BNPL in `requested`

When an order's payment is a credit-type BNPL still in `requested` status, the order-actions summary renders the **Payment Lease** button in place of the usual Mark-as-paid button (see [[orders-payment-mark-paid]]). This signals that the order can't simply be marked paid — the customer must complete the credit application first.

### Distinct from manual confirm

Lease (re-confirmation in `requested`) and manual confirm (capture at `completed` / `paid`) are two different stages of the credit lifecycle. Lease nudges the application; manual confirm commits the approved credit at dispatch. They never apply to the same order at the same time.

### Excluded providers handle their own re-confirmation

FusionPay, Klear, DSK BNPL, and Fibank BNPL are explicitly excluded from the Lease flow — their re-confirmation happens entirely on the provider's side, outside CloudCart.

### Permission

Standard orders write access; no specific lease grant.

## Related

- [[orders-payment-manual]] — hub.
- [[orders-details]] — parent page hosting the Lease button.
- [[orders-payment-mark-paid]] — the standard action Lease replaces for credit-type BNPL in `requested`.
- [[orders-payment-manual-mokka]] — Mokka manual confirm (the later, capture stage).
- [[orders-payment-manual-klear]] — Klear manual confirm (Klear is excluded from Lease).
- [[settings-payment-providers]] — credit-provider configuration.

## Open questions

- Confirm the exact route name / path for the Lease action `(verify)`.
- Confirm the full list of credit-type providers eligible for Lease beyond Mokka / Iute / generic credit `(verify)`.
