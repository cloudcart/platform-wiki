---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Per-code form"
route_name: discounts-code_pro-edit
route_path: /admin/marketing-new/discounts/code-pro/:id/:codeId
aliases: ["Code PRO form", "Per-code form", "Code PRO create form", "Code PRO edit form", "Conditions config row"]
tags: [marketing, discounts, code-pro, form, conditions]
plan_gates: ["discount-code-pro"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-code-pro]]. See the hub for the other aspects (overview, fields, business rules, checkout, endpoints).

# Code PRO — per-code form structure

## Purpose

This page documents the **structure and conditional UI** of the per-code create / edit form: the six blocks, the conditions array row builder, and the per-target sliding sub-forms. Use this page when answering *"why does this field appear / disappear?"* or *"what's the difference between the type select and the target select?"*.

For the backend keys, defaults, and validation strings see [[code-pro-fields]]. For business rules around saving see [[code-pro-business-rules]].

## Where to find it

Reached from the codes list ([[marketing-discounts-code-pro]]) via **+ Add code** (route `discounts-code_pro-create`, path `/admin/marketing-new/discounts/code-pro/:id/create`) or by clicking a row (route `discounts-code_pro-edit`, path `/admin/marketing-new/discounts/code-pro/:id/:codeId`).

## What the merchant can do here

Configure one code's full set of terms:

- **Active** (yes/no), **Code** literal string, **Barcode mode** (treat code as EAN-13 / EAN-8).
- **Conditions array** — up to 5 distinct conditions per code (see the row builder below). Each condition has a Type (`flat` / `percent` / `shipping`), Value, Setting (target), and target records.
- **Date range** — start date (required) + end date (or "No expiration").
- **Usage limits** — `max_uses` (total across all customers) and `maxused_user` (per customer). Either or both can be Unlimited.
- **Customer groups** — limit redemption to selected [[customers-custom-groups]], or "All groups" via the `customer_groups_target` checkbox.
- **Region** — limit redemption to a [[geo-zone]], or "All regions" via the `all_regions` checkbox.
- **Stacking flags** — `code_apply` ("Apply discount even if the cart contains products with a discount") and `apply_regular_price` ("Apply to the base price if this discount is higher").
- **Guest restriction** — `only_customer` to hide the code from guest checkouts.

## Settings & fields

### The six form blocks (in render order)

1. **General settings** — status + name + `DiscountsConfigCodeGenerator` slot (the code-format dropdown + literal code + Generate button).
2. **Conditions config** — `DiscountsCodeProConditionsConfig` (array of up to 5 condition rows; *"Add new condition"* link disappears at 5).
3. **Discount limits** — shared `DiscountsConfigDiscountLimit` block (`max_uses` + `maxused_user` with Unlimited checkboxes).
4. **Customer groups** — shared block (All groups switch + multi-pick on OFF).
5. **Regions** — shared block (Make it Global switch + geo-zone single-pick on OFF).
6. **Date range no-timer** — shared block, with timer switches hidden (`hideTimer=true`).

### Per-condition row (`DiscountsCodeProConditionsConfigRow`)

Each row in the Conditions array is a card wrapped with an index badge (1, 2, 3, …) and a remove-row X icon. The card contains:

| Control | Behaviour |
|---------|-----------|
| **Discount type** select | `Fixed amount` (`flat`) / `Percentage` (`percent`) / `Free shipping` (`shipping`). |
| **Discount value** input | Slides open ONLY when type ∈ {`flat`, `percent`}. Currency input for `flat` (in cents); percent input for `percent` (0–100). |
| **Discount target** select | When type=`shipping`: only `all` and `order_over`. When type=`flat`/`percent`: all seven (`all`, `order_over`, `product`, `category`, `vendor`, `selection`, `category_vendor`). |
| **Per-setting sub-form** | Slides open the matching picker / threshold input depending on the selected target (see table below). |
| **Allow-price sub-form** (`DiscountsCodeProConditionsConfigRowAllowPrice`) | Shown for target ∈ {`all` when type≠shipping, `product`, `category`, `vendor`, `selection`, `category_vendor`}. Contains the *"Where the price of the product is minimum"* switch (`allow_price`) which, when ON, reveals an `order_over` currency input. This is the per-target minimum-cart-amount constraint that the Code PRO engine uses to gate the condition. |

### The target sub-forms

| Target | Sliding sub-form |
|--------|-------------------|
| `all` | Allow-price sub-form only (no extra input; or, when type=`shipping`, nothing). |
| `order_over` | Order-over currency input + Save-the-discount-on-your-order switch. |
| `product` | Multi-pick product search (api `/admin/api/core/products/search`) + Allow-price sub-form. |
| `category` | Warning info-box (*"will only apply to main product category"*) + multi-pick category search (api `/admin/api/core/product-categories/search`) + Allow-price sub-form. Category options get post-processed: each option name is split on `>` and only the leaf name is shown. |
| `vendor` | Multi-pick vendor search + Allow-price sub-form. |
| `selection` | Multi-pick smart-collection search + Allow-price sub-form. |
| `category_vendor` | Warning info-box + category multi-pick + vendor multi-pick + Allow-price sub-form. |

### Row add / remove behaviour

- Removing the last condition auto-inserts a fresh empty row so there's always at least one.
- Adding rows: the *"Add new condition"* link is shown next to the last row but only when `condition.length < 5`.
- The export reserves columns for **5** conditions; the form caps the displayed rows at 5 via the controller's `->take(5)` call even if more exist in the DB — see [[code-pro-business-rules]] for the deletes-and-recreates behaviour on save.

## Business rules

The conditional reveal of the **Discount value** input on type ∈ {flat, percent} matches the validation: `condition.*.value` is required only for those types (see [[code-pro-fields]]). The **Allow-price** sub-form is the per-condition minimum-cart-subtotal gate; it differs from the row-level `order_over` target — `order_over` makes the whole condition a "cart-over X" rule, while `allow_price` adds a "minimum X" gate on top of a product / category / vendor / selection target.

## How it works

The form posts to `/admin/api/core/discounts/code-pro/{id}/save` (POST, see [[code-pro-endpoints-api]]). The submitted `condition[]` array is the per-row state of the conditions builder. The save runs in a single DB transaction that **deletes all `targets` and `customer_groups` rows first**, then re-inserts them from the submitted payload — so the post-save state matches the form exactly, with no stale rows. See [[code-pro-business-rules]] for the full save-flow rules and [[code-pro-endpoints-api]] for the JSON-API v2 path (same side effects).

## Related

- [[marketing-discounts-code-pro]] — hub.
- [[code-pro-fields]] — backend keys, defaults, validation strings for each control on this form.
- [[code-pro-business-rules]] — deletes-and-recreates save flow, date validation, customer-group / region toggles.
- [[marketing-discounts-code-pro-generator]] — bulk-generator form that reuses the same `DiscountsCodeProConditionsConfig` block.
- [[customers-custom-groups]] — multi-pick source for the Customer groups block.
- [[geo-zone]] — single-pick source for the Regions block.
- [[products-smart-collections]] — selections used by `setting=selection`.
- [[products-categories]] — categories used by `setting=category` / `category_vendor`.
- [[products-vendors]] — vendors used by `setting=vendor` / `category_vendor`.

## Open questions

No outstanding questions.
