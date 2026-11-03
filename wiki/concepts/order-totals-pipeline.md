---
type: concept
nav_path: "Concept → Order totals pipeline"
aliases: ["Order totals", "Order total order of operations", "How the total is calculated", "Money pipeline", "Cart total composition", "Subtotal discount shipping tax total", "Why is my total this amount", "Order of operations totals", "Изчисляване на общата сума", "Ред на изчисление", "Как се формира тоталът"]
tags: [orders, totals, money, discount, shipping, tax, pricing, concepts]
plan_gates: []
created: 2026-06-13
updated: 2026-06-13
source_count: 3
---

# Order totals pipeline (order of operations)

## Definition

Every cart / order total is built by a **fixed sequence of stages**, each computing against the running result of the previous one. This concept answers *"in what order are discounts, shipping, fees and VAT combined — and what does a percent discount or the VAT compute against?"* — the question behind most *"why is my total this amount?"* tickets.

The verified stage order is:

1. **Subtotal** — the line items: catalogue/variant price × quantity.
2. **Discounts (before shipping)** — order-, line- and code-level discounts applied to the **goods**, before shipping and before VAT. The per-provider **payment discount** lands here too (see [[order-pipeline-recalculation]]).
3. **VAT on goods (taxes before shipping)** — VAT computed on the *discounted* goods.
4. **Shipping** — the shipping quote; any **COD / payment fee** rides here as a Fee (stacks per [[tax-fees-vs-vat]]).
5. **VAT on shipping (taxes after shipping)** — VAT on the shipping line, when the customer's zone taxes shipping.
6. **Total** — the grand total the customer pays.

A separate **"discounts after shipping" stage exists in the engine but is currently disabled** — so all discounts apply in the *before-shipping* stage, and shipping itself is not cut by a regular discount (free shipping is a shipping-type / `order_over` discount handled at the Shipping stage, not a post-shipping price reduction).

## Scope

Covered:

- The stage sequence and what each stage computes against.
- Where the payment discount and COD/payment fees land in the sequence.
- The disabled after-shipping discount stage.

Not covered here:

- *Which* discounts attach and in what priority **within** the discount stage — see [[discount-stacking]] + [[discount-stacking-evaluation-order]].
- VAT rate selection and the include-/exclude-VAT pricing models — see [[tax-computation]] + [[tax-pricing-models]].
- The shipping-quote arithmetic — see [[shipping-calculation]].
- Fee-vs-VAT stacking detail — see [[tax-fees-vs-vat]].
- Currency conversion + rounding — see [[multi-currency]].

## Contrasts

- **Before-shipping vs after-shipping discounts** — goods discounts apply *before* shipping and VAT; the after-shipping discount stage is disabled, so a regular discount never reduces the shipping line. Free shipping is modelled separately (a `shipping` / `order_over` discount at the Shipping stage).
- **VAT before vs after shipping** — VAT on goods (before) and VAT on shipping (after) are **separate stages**, so the invoice can show them as distinct lines and the shipping VAT follows the shipping rule for the zone.
- **Per-base, not cumulative** — each discount computes against its **own base**, not against the already-discounted running total (10% then 5% is *not* 14.5% off). See [[discount-stacking]].

## Where it applies

The total is recomputed whenever the order/cart changes — at checkout and on every qualifying order edit (see [[order-pipeline-recalculation]] for the triggers and the freeze rules). The stage map that produces it:

| # | Stage | Computes |
|---|-------|----------|
| 1 | Subtotal | Σ (line price × quantity) |
| 2 | Discounts (before shipping) | goods discounts incl. the payment-method discount |
| 3 | VAT on goods | VAT on the discounted goods |
| 4 | Shipping | shipping quote + COD/payment fee |
| 5 | VAT on shipping | VAT on the shipping line (zone-dependent) |
| 6 | Total | grand total |

The breakdown is what renders on [[orders-details]] and the invoice ([[orders-invoices]]); the same composition is frozen onto the order at placement (the tax portion as a snapshot — see [[tax-order-snapshot]]).

## Related

- [[order-pipeline-recalculation]] — when the total is recomputed vs frozen, and what a payment-method change re-derives.
- [[tax-computation]] — VAT rate selection; [[tax-pricing-models]] — include/exclude VAT; [[tax-fees-vs-vat]] — fees vs VAT; [[tax-order-snapshot]] — the frozen tax snapshot.
- [[discount-stacking]] — which discounts attach; [[discount-stacking-evaluation-order]] — priority within the discount stage.
- [[shipping-calculation]] — the shipping quote that feeds stage 4.
- [[multi-currency]] — currency conversion + rounding of the final figure.
- [[orders-details]] / [[orders-invoices]] — where the breakdown is shown.

## Open Questions

- Whether the after-shipping discount stage is permanently retired or feature-flagged for re-enablement (verify).
- The exact rounding stage (per-line vs whole-total) and its interaction with [[multi-currency]] conversion (verify).
