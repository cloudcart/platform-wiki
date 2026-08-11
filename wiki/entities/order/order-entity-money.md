---
type: entity
nav_path: "Entity → Order → Money & accounting documents"
aliases: ["Order totals", "price_subtotal", "price_products_subtotal", "price_total", "Order weight", "Order VAT included", "Invoice number on order", "Credit number on order", "Receipt number on order", "Mark paid", "Payment record on order"]
tags: [entity, orders, money, payments, invoices, accounting]
created: 2026-06-10
updated: 2026-08-06
source_count: 4
---

> Part of [[order]]. See the hub for the other aspects (identifiers, lifecycle, side-effects, API access).

# Order — Money & accounting documents

## Identity

Every Order carries the **money picture** for a single sale: the totals (subtotal, products subtotal, shipping, tax, discount, grand total), the **VAT-included** flag that decides gross-vs-net display, the linked **payment records** (one or more, each with its own status — see [[payment-status]]), and the issued **accounting documents** (invoice number, credit number, receipt number). The money picture is **partially independent of the order lifecycle**: order status answers "where is this order in the workflow?", payment status answers "where is the money?", and they move independently.

This page covers the order-side of money. The 14-value money lifecycle taxonomy lives on [[payment-status]]; refund / capture / mark-paid actions live on their feature pages.

## Aliases

- **Order totals** — `price_subtotal`, `price_products_subtotal`, `price_total` (+ shipping / tax / discount breakdown).
- **Money in cents** — all monetary fields stored as integers in cents.
- **VAT included** — `vat_included` flag, gross-vs-net pricing model.
- **Issued documents** — invoice / credit note / receipt with numbers + dates.
- **Mark paid** — informal label for the manual `paid` transition (offline payments only).

## Key Attributes

### Totals (computed from line items)

| Attribute | What it represents | Notes |
|-----------|--------------------|-------|
| `price_subtotal` | Sum of line items before discounts (verify) | Integer in cents. |
| `price_products_subtotal` | Sum of line items including per-line discounts (verify) | Integer in cents. |
| `price_total` | Grand total the customer pays | Integer in cents. |
| `quantity` | Total units (sum of line-item quantities) | Shown in the [[orders]] list. |
| `weight` | Sum of line-item weights | Drives shipping. Pairs with `unit_system` (`metric` / `imperial` — frozen per order; see [[order-entity-identifiers]]). |

The exact per-line arithmetic — discount stacking, tax inclusion, free-line behaviour — lives on [[orders-details-products]] and [[apps-cart-rules]].

### VAT-included flag

| Attribute | Source | Effect |
|-----------|--------|--------|
| `vat_included` | Inherits from store tax settings at order create time (verify) | Whether displayed line prices include VAT (gross-priced store) or not (net-priced store). Selects the invoice template variant and how line totals are itemised on the customer-facing invoice. |

### Payment records (one-to-many)

Each Order has **zero or more payment records**, each carrying:

- `provider` — payment provider (Stripe, PayPal, Borica, COD, bank transfer, etc.).
- `amount` — payment amount (integer cents).
- `provider_reference_id` — gateway transaction reference, used to reconcile refunds / captures.
- `status` — one of the 14 [[payment-status]] enum values.

The **most recent payment's status** is what [[orders-details]] surfaces in the payment row — but the order's overall `status` is **independent** of it (see *Independent payment status* below).

### Manual "Mark paid" — updates existing record, doesn't create new

When the merchant clicks **Mark paid** via [[orders-payment-mark-paid]], the platform:

1. Updates the **existing** payment record's `status` to `completed` (it does NOT create a new record).
2. Emits `order.updated` to [[settings-hooks]] subscribers.
3. Writes an [[orders-history]] row.

This action runs **only on offline payment types** (COD, bank transfer, ePay POS-pay-after-arrival). Other providers (Stripe, PayPal, Borica) sync through the gateway — never marked paid manually.

### Independent payment status

Concrete examples: an order can be `status = completed` while its payment is `refunded` (refund issued after completion), or `status = pending` while its payment is `authorized` (pre-auth held, awaiting capture). See [[order-status-workflow]] for the full Order × Payment matrix.

### Issued accounting documents

Each Order has THREE optional document attribute pairs:

| Pair | Issued via | Numbering rule |
|------|------------|----------------|
| `invoice_number` + `invoice_date` | [[orders-invoice]] | Per [[settings-invoicing]], assigned at issue time. Not editable from any admin screen, though both are writable through [[api-orders]]. |
| `credit_number` + `credit_date` | [[orders-credit]] | The **whole-order** credit note. A **partial** credit note is not stored here — it lives on the return that produced it. See [[orders-credit-numbering]]. |
| `receipt_number` + `receipt_date` | [[orders-receipt]] | Cash receipt number; generated on issuance. |

All three default to `null` and are populated **at issue time only**. An issued number is never re-used.

Once `invoice_number` is populated the order is **frozen**: it can no longer be edited ([[orders-details-products]]) and its prices can no longer be converted from BGN to EUR.

### Credit-note gating

A credit note is allowed only when `status IN (cancelled, refunded)` AND the order has an `invoice_number` populated (per [[orders-credit]]). Otherwise the action is hidden on [[orders-details]] — see [[order-status-action-gates]] for the broader action-gate matrix.

### A credit note is never auto-cleared — it LOCKS the order instead

There is no auto-clearing of `credit_number` on any status change. The real rule is the opposite: once a `cancelled` / `refunded` order carries a credit number (or a return record), it is **locked** — it can no longer be moved to any non-reversal status, only toggled between `cancelled` and `refunded`. See [[order-status-entity-edge-cases]].

### Currency and locale locked at create time

The order's `currency` and `locale` are **frozen at create time** (see [[order-entity-identifiers]]). Even if the store later changes its default currency or language, historical totals stay in the original currency, and downloadable invoices plus customer-facing emails stay in the original locale.

The BGN→EUR transition is the one deliberate exception: the **Convert prices to EUR** button on [[orders-details]] permanently rewrites the order's stored amounts at the fixed rate and sets its currency to EUR. It is one-way, and it is refused once the order has an invoice number — see [[orders-details-actions]].

### Discount uses count toward the cap on counted statuses

When an order using a [[discount]] reaches one of the **counted statuses** (per the `discounts_used_statuses` setting — default `paid`, `completed`, `fulfilled` — verify against [[settings-cart]]), the discount's `uses` counter and the per-customer cap counter both increment. Cancelled / refunded orders do **NOT** consume a slot. Full counted-status rule on [[marketing-discounts]]; mechanics on [[order-status-side-effects]].

### Source attribution for revenue

| Attribute | Used for |
|-----------|----------|
| `cart_id` | Cart-to-order conversion analytics. |
| `campaign_id` / `campaign_action_id` | Campaign attribution — [[analytics-orders-by-social-source]] aggregates these. |
| `subscriber_id` | Newsletter-driven revenue attribution. |
| `abandoned` + `restore_source` meta | Abandoned-cart recovery — [[orders-abandoned]]. |

## Where it appears

- [[orders]] — list shows `price_total` per row + aggregated totals at the top.
- [[orders-details]] — totals breakdown, payment row, "Edit payment", invoice / credit / receipt rows.
- [[orders-payment-mark-paid]] — manual paid transition for offline payments.
- [[orders-payment-capture]] — capture-style gateways (Borica Way4, Stripe pre-auth).
- [[orders-payment-refund]] — refund flow.
- [[orders-payment-manual]] — manual payment record entry.
- [[orders-invoice]] — invoice issuance.
- [[orders-invoices]] / [[orders-invoices-download]] / [[orders-invoices-export]] — invoice listing + export.
- [[orders-credit]] — credit-note issuance (gated by `status IN (cancelled, refunded)` + `invoice_number`).
- [[orders-receipt]] — cash receipt issuance.
- [[orders-discount-add]] — add order-level discount.
- [[orders-export]] — exports include totals.
- [[settings-invoicing]] — numbering scheme + template.
- [[settings-cart]] — `order_complete`, `order_status_for_quantity_decrease`, `discounts_used_statuses` (verify the exact key).
- [[analytics-average-order-value]] / [[analytics-percentage-of-orders]] — totals aggregation.

## Related

- [[order]] — hub.
- [[payment-status]] — the independent payment-side 14-value enum.
- [[payment-provider]] — every payment record carries one provider.
- [[invoice]] — accounting document issued against the order.
- [[credit-note]] — accounting document for refunds / reversals.
- [[discount]] — order-level + per-line discounts; uses-counter rule.
- [[tax]] — per-line tax breakdown carried on the order.
- [[order-entity-lifecycle]] — negative-status transitions that affect the money picture.
- [[order-entity-identifiers]] — `currency` / `locale` / `unit_system` snapshot.
- [[order-status-action-gates]] — gating matrix for refund / credit / mark-paid.
- [[order-status-side-effects]] — discount uses-counter + revenue-exclusion semantics.
- [[settings-invoicing]] — numbering scheme + invoice template.

## Open Questions

- Arithmetic distinction between `price_subtotal` and `price_products_subtotal` (verify: which includes per-line discounts?).
- Exact setting key for "discount uses counted statuses" — `discounts_used_statuses` (verify against [[settings-cart]]).
- Whether `vat_included` can change after create (e.g., if the tax model changes) — current understanding: frozen at create (verify).
