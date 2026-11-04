---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Business rules"
route_name: discounts-code_pro-edit
route_path: /admin/marketing/discounts/code-pro/:id/:codeId
aliases: ["Code PRO business rules", "Code PRO save flow", "Code PRO barcode mode", "Code PRO stacking", "Code PRO bulk operations"]
tags: [marketing, discounts, code-pro, business-rules, save-flow]
plan_gates: ["discount-code-pro"]
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[marketing-discounts-code-pro]]. See the hub for the other aspects (overview, form, fields, checkout, endpoints).

# Code PRO — business rules & save flow

## Purpose

This page documents the **non-obvious admin-side behaviours** around Code PRO codes: the per-code active flag (independent from the parent), the deletes-and-recreates save transaction, customer-group / region targeting toggles, stacking flags, barcode mode, and bulk operations. Use it when answering *"why did this child row disappear?"*, *"how does barcode mode work?"*, or *"can I stack a Code PRO on a discounted product?"*.

For the form layout see [[code-pro-form]]. For field definitions see [[code-pro-fields]]. For checkout-time behaviour see [[code-pro-checkout]].

## Where to find it

These rules apply on the per-code form save (`/admin/marketing/discounts/code-pro/:id/:codeId`), on the bulk-toggle / bulk-delete actions in the table action bar at `/admin/marketing/discounts/code-pro/:id`, and, with its own validation, on the JSON-API v2 path (see [[code-pro-endpoints-api]]).

## What the merchant can do here

Manage one code at a time (save / toggle / delete) or multiple codes at once via the table action bar.

## Settings & fields

This page is about behaviour, not fields. For field reference see [[code-pro-fields]].

## Business rules

### Per-code active flag — independent from parent

The parent Code PRO discount has its own `active` toggle in the [[marketing-discounts]] list. Each child code under it has its own `active` flag (`active = 1` / `0`). **A code is redeemable only when BOTH the parent and the child are active.**

The merchant can pause one specific code (e.g., an influencer whose contract expired) without affecting the rest of the campaign. The row's Active switch calls `apiMarketingDiscounts.statusDiscountCodes` with `{ ids: [code_id], status: 1|0 }` (note: numeric `1`/`0`, NOT `yes`/`no` — different from the parent discount's toggle). Only this toggle or the list's bulk action turns a code off: the status switch on the code form saves it as active either way.

### Conditions are deleted-and-recreated on save

When the merchant edits a code's conditions, the controller wraps the save in a **single DB transaction** that:

1. **Deletes all `targets` and `customer_groups` join rows** for the code.
2. Re-inserts them from the submitted payload.

This means stale conditions don't accumulate; the post-save state is exactly what the merchant submitted. **External integrations that hold references to specific target / join row IDs will see those IDs change after every save** — they must re-look-up by `code_id`, not by row ID.

### Save flow — full sequence

1. The save endpoint resolves the parent Discount by `discount_id` (must be `type=code-pro`) and either finds the existing code or instantiates a new one.
2. Top-level fields are filled with explicit casting:
   - `code_apply`, `apply_regular_price` and `barcode_prefix` are on when the form sends them. The status switch (`active`) always saves the code as active. `only_customer` is saved as on whenever the form sends it, which it does when an existing code is edited, so saving an existing code through the edit form turns "registered users only" on even when it was off.
   - `name` falls back to `code` when blank.
   - `code_prefix` is derived from the presence of `code_format` (so picking ean13/ean8 implicitly enables barcode mode).
   - `geo_zone_id` is nulled when `all_regions` is ON.
   - `max_uses` / `maxused_user` are nulled when `unlimited` / `unlimited_user` are ON.
   - `date_end` is nulled when `no_expire` is ON.
3. The submitted `condition[]` array is processed into per-condition rows.
4. The customer-group join rows are built from `customer_groups[]`.
5. The save runs inside a single DB transaction:
   - If the code exists, **all `targets` and `customer_groups` rows are deleted first** (then re-inserted from the submitted data).
   - The cascading save persists the code and its sub-records.
6. Response: success with a redirect to the codes list for the parent discount.

### Date validation uses store-format

Date fields use the store's display `date_format` setting (e.g., `d.m.Y` for BG / `Y-m-d` for ISO). The form asks for a start date (*"Field is required"*) and for an end date unless `no_expire` is checked (*"The end date is required"*); `no_expire` sets `date_end = null`.

### Customer-group and region targeting — binary toggles

The form has a binary toggle for each:

- **Customer groups**: `customer_groups_target = 'yes'` → applies to all groups, no list needed. With it off, the listed groups apply; if none is picked, the code has no group restriction.
- **Region**: `all_regions = 'yes'` → no geo restriction. With it off, `geo_zone_id` names an existing [[geo-zone]]; if none is picked, the code has no region restriction.

At checkout, the discount-lookup applies both filters — see [[code-pro-checkout]] for the active-scope check.

### Stacking — `code_apply`

By default (`code_apply = 0`), a Code PRO code is refused at checkout with *"Invalid discount code"* if any cart line already has a product discount (e.g., a Fixed discount on a product). When the merchant turns ON *"The discount is applied even when the cart contains discounted products."*, the code stacks on top of those.

With `apply_regular_price` also on, the code is worked out on the regular price and compared with the current discounted price. If the code's price is lower, it replaces the product discount; otherwise the line keeps the product discount and no code. A flat value whose share for a line reaches that line's discounted unit price is not applied at all.

### Barcode mode (`code_prefix` + `code_format`)

For physical-retail merchants integrating an in-store POS scanner:

- Pick `code_format = ean13` or `ean8` — this implicitly sets `code_prefix = 1`.
- The code is then validated as a barcode (EAN-13 / EAN-8 checksum) at checkout.
- Optionally, with `barcode_prefix = 1`, the entered `code` field is treated as a prefix and the scanner appends the actual code digits — useful for store-prefixed barcodes.

There is no separate input control for `code_prefix` — see [[code-pro-fields]].

### Bulk operations

The list at `/admin/marketing/discounts/code-pro/:id` supports bulk status toggle and bulk delete from the table action bar. The merchant ticks multiple rows and uses the action selector:

- **Set status active** / **Set status unactive** → POST to `/admin/api/core/discounts/code-pro/:id/status` with `{ ids: [...], status: 1|0 }`.
- **Delete** → DELETE to `/admin/api/core/discounts/code-pro/:id?ids[]=...`.

Bulk delete removes the selected codes in one step, and their conditions and customer-group rows go with them.

### Delete cascade

Deleting a code cascades to:

- The per-condition `targets` rows.
- The per-code `customer_groups` join rows.

**Historical order-discount rows referencing the code remain in place** for accounting / analytics — see [[code-pro-checkout]] for how the `uses` counter behaves after deletes.

## How it works

The deletes-and-recreates pattern runs on every admin save; the JSON-API v2 path replaces conditions and groups only when they are sent — see [[code-pro-endpoints-api]]. The store-wide uniqueness of `discounts_code_pro.code` is a form check, not a database rule (see [[code-pro-overview]]): the admin runs it on new codes, the JSON-API on create and edit, and the generator checks against existing codes itself.

## Related

- [[marketing-discounts-code-pro]] — hub.
- [[code-pro-fields]] — field reference; the keys this save flow casts.
- [[code-pro-form]] — the form that posts to the save endpoint.
- [[code-pro-checkout]] — runtime active-scope rules that consume what's saved here.
- [[code-pro-endpoints-api]] — the JSON-API v2 path and how it differs.
- [[customers-custom-groups]] — customer-group join target.
- [[geo-zone]] — region target.

## Open questions

No outstanding questions.
