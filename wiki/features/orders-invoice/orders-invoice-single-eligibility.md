---
type: feature
nav_path: "Orders → Order details → Invoice → Eligibility & gates"
route_name: admin.orders.generate.invoice
route_path: /admin/orders/generate-invoice/:order_id
aliases: ["Invoice eligibility", "Invoice gates", "When can I issue an invoice", "Invoice plan gate", "Billing address requirement", "Право на издаване на фактура"]
tags: [orders, invoice, invoicing, plan-gates, eligibility]
plan_gates: ["invoices"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
> Part of [[orders-invoice]]. See the hub for the other aspects (action surfaces, numbering, rendering, customer email).

# Invoice — eligibility & gates (per order)

## Purpose

Documents **every gate that decides whether an order can be invoiced** and whether the invoice surfaces appear: the `invoices` plan feature, an active Invoicing provider, the order-status eligibility rule, the configurable billing-address requirement, and the permanence rule that makes invoice numbers part of the audit trail. This is the aspect to read for "the View invoice button isn't showing" and "why can't I issue an invoice for this order" tickets.

## Where to find it

The gates are evaluated on [[orders-details]] when rendering the invoice action surfaces (see [[orders-invoice-single-surfaces]]) and when the manual-number form (`/admin/orders/generate-invoice/{order_id}`) tries to save.

## What the merchant can do here

Nothing is directly configured here — this aspect describes the conditions that must all be satisfied before the merchant can issue or view an invoice. The configurable inputs (`invoicing`, `billing_invoicing`) live on [[settings-invoicing]]; the plan gate is set by the subscription plan.

## Settings & fields

The eligibility logic reads:
- The `invoices` plan feature (subscription-level).
- The store-wide `invoicing` provider toggle on [[settings-invoicing]].
- The `billing_invoicing` toggle on [[settings-invoicing]].
- The order's `status`, `status_fulfillment`, and line-item types.
- The order's billing address.

## Business rules

### Plan-feature gate (`invoices`)

The whole invoicing surface is gated by the `invoices` plan feature (see [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]]). When the merchant's plan lacks it, the plan middleware blocks access: the cross-order list ([[orders-invoices]]) redirects to [[plan-features]], and the per-order **View invoice** action is hidden even when an invoice number exists. `invoices` is a boolean access gate — it does NOT extend via feature packs. This is DISTINCT from the store-wide `invoicing` setting and from the per-order `invoice_number` field; the plan gate sits above both.

### Active Invoicing provider required

The merchant must have an active Invoicing app or built-in provider configured in [[settings-invoicing]]. Without it the **View invoice** button doesn't render and the invoice route returns 404.

### Eligibility = `paid` / `completed` OR fulfilled OR digital-only

The platform refuses to issue an invoice number until the order is in one of these states: `status_fulfillment = fulfilled`, `status` IN `paid` / `completed`, or the order contains only digital products. Pending orders cannot be invoiced even manually.

### Billing-address requirement (configurable)

A second gate: when `billing_invoicing = yes` is set in [[settings-invoicing]], the order MUST have a billing address before an invoice number can be assigned. Without that address the **View invoice** action stays hidden and the manual-number form refuses to save.

### Invoice number is per-order and permanent

Once an invoice number is generated for an order, it stays attached even if the order is later voided, cancelled, or refunded. Numbers are NEVER reused — the next order uses the next number in sequence (see [[orders-invoice-single-numbering]] for the `max + 1` rule). This preserves the audit trail required by tax law.

### Re-issuing is not supported via the UI

Because numbers are consumed sequentially and persisted, there is no merchant-facing "re-issue invoice with corrected number" action. To correct mistakes the merchant issues a credit note via [[orders-credit]] and creates a new corrected order — see [[orders-invoice-single-customer-email]] for the full re-issue note.

### Permission

Standard orders permission scope. Some invoicing apps (e.g., Szamlazz, SmartBill) may add per-app permissions.

## Related

- [[orders-invoice]] — hub.
- [[settings-invoicing]] — `invoicing` provider toggle + `billing_invoicing` requirement.
- [[plan-features]] — upsell target when the `invoices` gate is hit.
- [[plan-gates]] — plan-feature gating model.
- [[plan-vs-feature-pack]] — why `invoices` is an access gate, not a pack.
- [[orders-credit]] — credit-note path for corrections.
- [[orders-details]] — where the gates are evaluated.

## Open questions

None.
