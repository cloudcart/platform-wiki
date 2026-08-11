---
type: concept
nav_path: "Concept → Tax computation → Order snapshot"
aliases: ["Tax order snapshot", "orders_taxes snapshot", "Frozen tax on order", "Historical tax accuracy", "vat_included", "Re-edit recomputation"]
tags: [taxes, vat, finance, snapshot, orders, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax-computation]]. See the hub for the other aspects (rate selection, pricing models, overrides, OSS, address resolution, fees-vs-VAT).

# Tax — frozen-on-order snapshot

## Definition

When an order is persisted, the platform writes the applied tax rules into an **`orders_taxes`** snapshot on the order row. This snapshot is the **authoritative tax record** for that order from then on — later edits to the merchant's [[settings-taxes]] rules do NOT retroactively re-tax this order. Historical invoices, credit notes, and accounting exports all read from the snapshot, not from the live rules.

A complementary capture — the per-order **address-priority snapshot** (`invoicing_address`) — protects which address the matcher reads on a re-computation. See [[tax-address-resolution]] for that side.

## Scope

Covered:

- What `orders_taxes` records per applied tax line.
- The `vat_included` field that captures the pricing model.
- The recompute-on-edit rule for `pending` / `paid` / `authorized` orders.
- The currency-conversion guarantees (snapshot is in the order's currency).
- The historical-rate-change scenario (VAT raised from 20% to 22%).

Not covered here:

- The rate-matching engine that produced the snapshot — see [[tax-rate-selection]].
- The address-priority snapshot — see [[tax-address-resolution]].
- The fee stacking that lives on the order alongside VAT — see [[tax-fees-vs-vat]].

## What gets snapshotted

Each applied tax line on `orders_taxes` carries:

- `rate` — the percent or flat amount that was applied (after overrides per [[tax-overrides]]).
- `vat` flag — whether the row was a VAT-type tax or a fee.
- `oss_registration` flag — captured for audit / re-computation context.
- `without_vat_reasons` + `without_vat_reasons_non_eu` — the wording strings that drive invoice rendering even years later (see [[tax-oss-semantics]]).
- The resulting **amount** — already converted to the order's currency.

The order row itself also carries:

- `vat_included` — captures the pricing model in effect (GROSS vs NET, per [[tax-pricing-models]]).

## The recompute carve-out

Editing line items on a `pending` / `paid` / `authorized` order **does** recompute the tax line. The logic:

- The recomputation uses the snapshot's stored rates for lines that already existed.
- A **newly added** line item runs through the rate-selection + override flow against the **current** [[settings-taxes]] rules — so if a new line is in a category with a per-category override that didn't exist before, that NEW override applies to the NEW line only.
- Existing lines are not back-rewritten with newer rates.

This narrow carve-out preserves historical accuracy on the lines that were there originally, while still allowing edit flexibility for whatever the merchant adds.

Terminal-status orders (`cancelled`, `refunded`, `completed`, etc.) do not recompute — they are read-only for tax purposes.

## Multi-currency in the snapshot

The order's **final tax amount** is snapshotted in the **order's currency**. So an order placed in EUR carries EUR-denominated tax amounts even if the merchant's base currency is BGN. The conversion happened at order-creation time using the live FX rate; later FX-rate drift does not retroactively re-convert the snapshot.

- Percentage taxes are currency-independent on the way in (20% of 100 EUR is 20 EUR) — no conversion is needed at compute time.
- Flat taxes / fees ARE currency-dependent. A 5 BGN flat fee on a EUR order is converted using the latest FX rate from the internal Fixer.io-synced rate table at the moment of order creation, then frozen.

See [[multi-currency]] for the underlying FX-rate sync.

## Contrasts

- **Frozen snapshot vs live recompute** — the snapshot wins on every read. The engine recomputes only as a hidden detail when line items are edited.
- **Rates snapshot vs address-priority snapshot** — two distinct freezings; the rates lock the amounts, the address-priority locks which address gets resolved on re-computation. See [[tax-address-resolution]].
- **Editable statuses (`pending` / `paid` / `authorized`) vs terminal statuses (`cancelled` / `refunded`)** — editable orders allow line-item edits that partially re-tax; terminal orders are read-only.

## Worked example — historical rate change

Setup:

- Merchant has been charging 20% VAT for 2 years.
- Government raises VAT to 22% effective Jan 1.
- Merchant edits the [[settings-taxes]] rule to 22% on Jan 1.

Result:

- All orders placed BEFORE Jan 1 keep their 20% snapshot. Their invoices stay at 20%. Refunds, credit notes, and accounting exports all use the snapshot.
- All orders placed FROM Jan 1 forward use 22%.
- The merchant does NOT need to back-fix anything.

## Worked example — line-item edit on pending order

Setup:

- Order is in `pending` status with one line: T-shirt at 20% VAT (snapshot says rate = 20).
- Merchant then adds a paperback line.
- Meanwhile a per-category override exists: category Books → 9%.

Result:

- T-shirt line: keeps its 20% rate from the snapshot.
- Paperback line (newly added): runs through [[tax-overrides]] → 9% applies.
- Order totals re-aggregate, but the existing T-shirt line is not re-rated.

## Settings cache flushed on save

Saving a tax rule in [[settings-taxes]] flushes the platform's Settings cache so the next checkout computation picks up the new rule immediately. No queue, no notifications, no webhooks fire from the tax management screen. Existing snapshots are untouched.

## Where it applies

- [[orders-details]] — totals section shows the snapshotted per-line + total tax breakdown.
- [[orders-invoice]] — the issued invoice document carries the snapshotted tax values.
- [[orders-credit]] — credit notes carry the same tax values for accounting reversal.
- [[orders-receipt]] — cash receipts include the tax breakdown.
- [[order-processing-pipeline]] — tax computation happens at order placement (Stage 1); the snapshot is preserved in the webhook payload.

## Related

- [[tax-computation]] — hub.
- [[tax-rate-selection]] — the matcher that produced the snapshot.
- [[tax-address-resolution]] — the separate address-priority snapshot.
- [[tax-pricing-models]] — `vat_included` captures GROSS vs NET.
- [[order]] — entity carrying the snapshot.
- [[orders-details]] / [[orders-invoice]] / [[orders-credit]] / [[orders-receipt]] — all read the snapshot.
- [[order-processing-pipeline]] — order placement stage that freezes the snapshot.
- [[multi-currency]] — FX rate behaviour for flat fees inside the snapshot.

## Open Questions

- ⏸️ **Tax bulk-export for accounting is NOT a current feature.** There is no one-click *"export all orders with tax breakdown by country"* report today. Merchants reconcile manually from per-order details, or via [[apps]] accounting integrations (Smart Bill, FGO, Szamlazz).
