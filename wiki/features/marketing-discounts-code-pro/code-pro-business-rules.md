---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Business rules"
route_name: discounts-code_pro-edit
route_path: /admin/marketing-new/discounts/code-pro/:id/:codeId
aliases: ["Code PRO business rules", "Code PRO save flow", "Code PRO barcode mode", "Code PRO stacking", "Code PRO bulk operations"]
tags: [marketing, discounts, code-pro, business-rules, save-flow]
plan_gates: ["discount-code-pro"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-code-pro]]. See the hub for the other aspects (overview, form, fields, checkout, endpoints).

# Code PRO — business rules & save flow

## Purpose

This page documents the **non-obvious admin-side behaviours** around Code PRO codes: the per-code active flag (independent from the parent), the deletes-and-recreates save transaction, customer-group / region targeting toggles, stacking flags, barcode mode, and bulk operations. Use it when answering *"why did this child row disappear?"*, *"how does barcode mode work?"*, or *"can I stack a Code PRO on a discounted product?"*.

For the form layout see [[code-pro-form]]. For field definitions see [[code-pro-fields]]. For checkout-time behaviour see [[code-pro-checkout]].

## Where to find it

These rules apply on the per-code form save (`/admin/marketing-new/discounts/code-pro/:id/:codeId`), on the bulk-toggle / bulk-delete actions in the table action bar at `/admin/marketing-new/discounts/code-pro/:id`, and on the JSON-API v2 path (see [[code-pro-endpoints-api]]) — same rules, same side-effects.

## What the merchant can do here

Manage one code at a time (save / toggle / delete) or multiple codes at once via the table action bar.

## Settings & fields

This page is about behaviour, not fields. For field reference see [[code-pro-fields]].

## Business rules

### Per-code active flag — independent from parent

The parent Code PRO discount has its own `active` toggle in the [[marketing-discounts]] list. Each child code under it has its own `active` flag (`active = 1` / `0`). **A code is redeemable only when BOTH the parent and the child are active.**

The merchant can pause one specific code (e.g., an influencer whose contract expired) without affecting the rest of the campaign. The row's Active switch calls `apiMarketingDiscounts.statusDiscountCodes` with `{ ids: [code_id], status: 1|0 }` (note: numeric `1`/`0`, NOT `yes`/`no` — different from the parent discount's toggle).

### Conditions are deleted-and-recreated on save

When the merchant edits a code's conditions, the controller wraps the save in a **single DB transaction** that:

1. **Deletes all `targets` and `customer_groups` join rows** for the code.
2. Re-inserts them from the submitted payload.

This means stale conditions don't accumulate; the post-save state is exactly what the merchant submitted. **External integrations that hold references to specific target / join row IDs will see those IDs change after every save** — they must re-look-up by `code_id`, not by row ID.

### Save flow — full sequence

1. The save endpoint resolves the parent Discount by `discount_id` (must be `type=code-pro`) and either finds the existing code or instantiates a new one.
2. Top-level fields are filled with explicit casting:
   - Boolean checkboxes (`active`, `code_apply`, `apply_regular_price`, `barcode_prefix`, `only_customer`) are derived from the request payload.
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

Date fields use the store's display `date_format` setting (e.g., `d.m.Y` for BG / `Y-m-d` for ISO). The validator chains `date_format:<store-format>` and `dateToCarbon:<store-format>` so merchants typing in their preferred format always work. The `date_end` may be omitted entirely if `no_expire` is checked (sets `date_end = null`).

### Customer-group and region targeting — binary toggles

The form has a binary toggle for each:

- **Customer groups**: `customer_groups_target = 'all'` → applies to all groups, no list needed. Otherwise an array of group IDs is required.
- **Region**: `all_regions = 'yes'` → no geo restriction. Otherwise `geo_zone_id` is required and must reference an existing [[geo-zone]].

At checkout, the discount-lookup applies both filters — see [[code-pro-checkout]] for the active-scope check.

### Stacking — `code_apply`

By default (`code_apply = 0`), a Code PRO code is rejected at checkout if any cart line already has a discount applied (e.g., a Fixed discount on a product). When the merchant turns ON *"Apply discount even if the cart contains products with a discount"*, the code stacks on top of those.

The `apply_regular_price` flag pairs with it to make the code re-evaluate against the catalog price if that yields a larger discount.

### Barcode mode (`code_prefix` + `code_format`)

For physical-retail merchants integrating an in-store POS scanner:

- Pick `code_format = ean13` or `ean8` — this implicitly sets `code_prefix = 1`.
- The code is then validated as a barcode (EAN-13 / EAN-8 checksum) at checkout.
- Optionally, with `barcode_prefix = 1`, the entered `code` field is treated as a prefix and the scanner appends the actual code digits — useful for store-prefixed barcodes.

There is no separate input control for `code_prefix` — see [[code-pro-fields]].

### Bulk operations

The list at `/admin/marketing-new/discounts/code-pro/:id` supports bulk status toggle and bulk delete from the table action bar. The merchant ticks multiple rows and uses the action selector:

- **Set status active** / **Set status unactive** → POST to `/admin/api/core/discounts/code-pro/:id/status` with `{ ids: [...], status: 1|0 }`.
- **Delete** → DELETE to `/admin/api/core/discounts/code-pro/:id?ids[]=...`.

Bulk delete wraps the loop in a transaction and deletes per row so any registered model events fire (e.g., the `targets` / `customer-groups` cascade cleanup). Older wiki phrasing referenced a `bulk-status` route name — that name doesn't exist; the unified status-change endpoint handles single + bulk via the IDs array.

### Delete cascade

Deleting a code cascades to:

- The per-condition `targets` rows.
- The per-code `customer_groups` join rows.

**Historical order-discount rows referencing the code remain in place** for accounting / analytics — see [[code-pro-checkout]] for how the `uses` counter behaves after deletes.

## How it works

The deletes-and-recreates pattern is the same on both the admin-panel path and the JSON-API v2 path — see [[code-pro-endpoints-api]] for the same-side-effects guarantee. The store-wide unique constraint on `discounts_code_pro.code` is DB-level (see [[code-pro-overview]]) so it fires whether the duplicate comes from the form, a bulk-generator, or an API call.

## Related

- [[marketing-discounts-code-pro]] — hub.
- [[code-pro-fields]] — field reference; the keys this save flow casts.
- [[code-pro-form]] — the form that posts to the save endpoint.
- [[code-pro-checkout]] — runtime active-scope rules that consume what's saved here.
- [[code-pro-endpoints-api]] — JSON-API v2 path with identical side-effects.
- [[customers-custom-groups]] — customer-group join target.
- [[geo-zone]] — region target.

## Open questions

No outstanding questions.
