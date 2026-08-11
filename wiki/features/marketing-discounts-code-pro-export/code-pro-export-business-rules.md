---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Export → Business rules"
route_name: discounts-code_pro-list
route_path: /admin/marketing-new/discounts/code-pro/:id
aliases: ["Code PRO export business rules", "Export no filter scope", "Export condition type semantics", "Export permission plan-gate"]
tags: [marketing, discounts, code-pro, export, csv]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-code-pro-export]]. See the hub for the other aspects (overview, columns, format).

# Code PRO export — business rules

## Purpose

This aspect covers the **semantic rules** of the Code PRO codes export — what scope the CSV captures, how condition "type" is normalised in the output, how multi-record conditions are rendered, and the permission / plan position of the export. These rules explain why the merchant sees what they see in the file and why it always contains everything.

## Where to find it

These rules govern the `discount-codes-pro.csv` file produced by the "Export" toolbar anchor on the [[marketing-discounts-code-pro]] codes list — `GET /admin/api/core/discounts/code-pro/{id}/export`. The merchant cannot change any of them (see [[code-pro-export-overview]]).

## What the merchant can do here

- **Predict the file scope** — the export always contains the complete codes list for the chosen discount, never a filtered subset.
- **Read the condition target type in merchant terms** — the export normalises raw backend setting names into the categories the merchant recognises (product-targeted vs cart-wide vs free-shipping vs over-threshold).
- **Rely on the same permission they already have** — if they can see the Code PRO discount, they can export it.

## Settings & fields

There are no merchant-adjustable settings — the rules below are fixed behaviours of the exporter. The shape of the output is on [[code-pro-export-columns]]; the encoding is on [[code-pro-export-format]].

## Business rules

### One CSV per Code PRO discount, no filter scope

The export always emits the **full codes list** for the chosen discount. Even though the export reuses the same search object as the listing, it is called with an **empty filter array** — so listing-level filters are not honoured and the file contains all rows. The merchant must filter in their spreadsheet after download. (This is the single most-common surprise — see the "cannot do" list on [[code-pro-export-overview]].)

### Condition type semantics in the CSV

The "Condition i type" column doesn't carry the **discount type** (flat / percent / shipping) — that's in "Condition i type value". Instead "type" carries the **target type**, with some normalisation:

- `setting = 'all'` with non-shipping type → emitted as `all_products`.
- `setting = 'order_over'` with non-shipping type → emitted as `order_over`.
- `type = 'shipping'` (any setting) → emitted as `free_shipping`, with `order_over` filled if present.
- `setting in ('product', 'category', 'vendor', 'selection', 'category_vendor')` → emitted as the setting name.

This mirrors how merchants typically think about discount targeting (product-targeted vs cart-wide vs free-shipping vs over-threshold) better than the raw backend setting names. The companion "Condition i type value" column carries the discount mechanic (`flat` / `percent` / `shipping`), so the merchant can correlate target type with mechanic without back-translating. Both columns are listed on [[code-pro-export-columns]].

### Many target records per condition

When a single condition row targets multiple products / categories / vendors / collections, the CSV joins the names with `; ` (semicolon + space). For example, a condition targeting three products → `Product A; Product B; Product C` in the "Condition 1 product" column. Names are **deduplicated**.

### Permission

The export inherits the parent Code PRO discount's permission scope — the standard `marketing.discounts` permission is required. There is no separate export-only permission.

### Plan-gating — decoupled from the generator

The export is **not separately plan-gated**. As long as the merchant has access to the Code PRO discount (via the `discount-code-pro` plan feature), they can export its codes regardless of the `discount-code-pro-generator` setting — the generator and the exporter are decoupled. Once a merchant has any Code PRO discount, the export route is reachable.

## Related

- [[marketing-discounts-code-pro-export]] — hub.
- [[code-pro-export-overview]] — the "cannot filter before download" surprise this scope rule explains.
- [[marketing-discounts-code-pro]] — the codes being exported.
- [[marketing-discounts-code-pro-generator]] — decoupled from the export at the plan-gate level.
- [[plan-gates]] — `discount-code-pro` plan feature governing access.
- [[discount]] — entity page for the parent Code PRO discount.
- [[products-smart-collections]] — collection names joined in `Condition i selection`.

## Open questions

No outstanding questions.
