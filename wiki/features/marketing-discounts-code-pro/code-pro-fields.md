---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Fields & validation"
route_name: discounts-code_pro-edit
route_path: /admin/marketing-new/discounts/code-pro/:id/:codeId
aliases: ["Code PRO fields", "Code PRO validation", "Code PRO field reference", "Code PRO listing columns"]
tags: [marketing, discounts, code-pro, fields, validation, reference]
plan_gates: ["discount-code-pro"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-code-pro]]. See the hub for the other aspects (overview, form, business rules, checkout, endpoints).

# Code PRO — fields, validation & listing columns

## Purpose

This page is the **citation-level reference** for the per-code form. Every field on [[code-pro-form]] is listed here with its backend key, what it does, and the verbatim validation rule. Use this page when answering *"what's the exact error message when X is empty?"* or *"what's the max length of the code field?"*.

## Where to find it

The fields documented here are submitted by the form at `/admin/marketing-new/discounts/code-pro/:id/:codeId` (see [[code-pro-form]]). The validation strings come from the `code_pro.validation.*` translation keys; the listing columns are rendered by the `CcTable` on `/admin/marketing-new/discounts/code-pro/:id`.

## What the merchant can do here

Look up the exact field name, key, default, and validation string for any control on the per-code form or the codes list.

## Settings & fields

### Top-level fields and validation

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Active** | `active` | If OFF the code is rejected at checkout. | 1 / 0. Default 1 on new. |
| **Code** | `code` | The literal string the customer enters. | Required, max 20, `alpha_num`, **unique on `discounts_code_pro.code`**. Error: *"Discount code is exists"* (`code_pro.validation.code.unique`). |
| **Code prefix (barcode)** | `code_prefix` | Treats the code as a barcode (with `code_format` ean13 / ean8). | 1 / 0; auto-set from `code_format` presence on save. There is NO separate input control for `code_prefix` — picking `code_format = ean13` or `ean8` implicitly sets `code_prefix = 1`; picking null sets it to 0. |
| **Barcode format** | `code_format` | Barcode standard. | `ean13` / `ean8` / null. |
| **Barcode prefix** | `barcode_prefix` | When ON, treats the entered `code` as a prefix and the scanner's value as `code + scanned`. | 1 / 0. |
| **Stack on discounted products** | `code_apply` | Allow code on top of existing per-product discounts. | 1 / 0. Default 0. |
| **Apply to base price** | `apply_regular_price` | Re-evaluate against the catalog price if it yields a larger discount. | 1 / 0. |
| **Only registered customers** | `only_customer` | Hides the code from guest carts. | 1 / 0. |
| **Date start** | `date_start` | Earliest day the code may redeem. | Required, formatted per store `date_format`. Error: *"Data is required"* (`code_pro.validation.date_start.required`). |
| **Date end** | `date_end` | Last day the code may redeem (or NULL for "No expiration"). | Required unless `no_expire` is ON. |
| **Max uses (total)** | `max_uses` | Total redemptions across all customers. | Required unless `unlimited` ON; integer 1–100,000. |
| **Max uses per customer** | `maxused_user` | Per-customer cap. | Required unless `unlimited_user` ON; integer 1–100,000. |
| **Customer groups** | `customer_groups[]` | Whitelist of groups that may redeem. | Required unless `customer_groups_target` is "All groups". |
| **Region** | `geo_zone_id` | Geo zone restriction. | Required unless `all_regions` is ON; must exist. |
| **Name** | `name` | Optional merchant-facing label; falls back to `code` value when blank. | Free string. |
| **Conditions array** | `condition[]` | The discount terms per code (see below). | Required, array. Error: *"Conditions are required"* (`code_pro.validation.condition.required`). |

### Per-condition fields

Each entry in the `condition[]` array is one discount term. The export reserves 5 columns; in practice **up to 5 conditions per code** is the documented design (the controller's `getConditions` method calls `->take(5)` so the form only shows the first 5 even if more exist in the DB).

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Type** | `condition.*.type` | Discount type for this row: `flat` / `percent` / `shipping`. | Required. |
| **Value** | `condition.*.value` | Amount (flat) or percentage. | Required if type=`flat`/`percent`; numeric, min 0.01. |
| **Setting** | `condition.*.setting` | Target type: `all`, `order_over`, `product`, `category`, `vendor`, `selection`, `category_vendor`. | Required. |
| **Order-over amount** | `condition.*.order_over` | The cart-subtotal threshold. | Required if setting=`order_over` (or with `allow_price`); numeric, min 0.01. Error: *"Amount is required"* (`code_pro.validation.condition.order_over.required_if`). |
| **Product targets** | `condition.*.product` | Product IDs (select2 multi-pick). | Required if setting=`product`. |
| **Category targets** | `condition.*.category` | Category IDs. | Required if setting=`category` or `category_vendor`. |
| **Vendor targets** | `condition.*.vendor` | Vendor IDs. | Required if setting=`vendor` or `category_vendor`. |
| **Selection targets** | `condition.*.selection` | Smart-collection IDs. | Required if setting=`selection`. |

### Listing columns (codes list table)

| Column | What it shows |
|--------|---------------|
| **Name** | Custom name or code string; clickable to open the edit form. |
| **Active** | Inline toggle. |
| **Uses** | Integer counter of successful redemptions (incremented by orders reaching the store's counted statuses — see [[code-pro-checkout]]). |
| **Max uses** | `max_uses` or `∞` if NULL. |
| **Date period** | "Starts: <date> / Ends: <date or '——'>". |
| **Targets count** | Number of distinct `row` groupings inside `condition[]` — i.e., how many separate conditions this code carries. |

### Table filters

The codes list table supports filters on:

- `active` (Yes/No).
- `time_used` (Exactly / Not equal to / More than / Less than).
- `uses_left` (same operators).
- `start_date` / `date_end` (Before / Before or equal / After / After or equal).

## Business rules

A few field-level rules worth flagging here (full set in [[code-pro-business-rules]]):

- **`code` is unique store-wide on `discounts_code_pro`** — across all Code PRO campaigns in the store, not just this one. See [[code-pro-overview]].
- **`code_prefix` has no input** — picking `code_format = ean13` or `ean8` implicitly sets `code_prefix = 1`; picking null sets it to 0. There is NO checkbox to toggle `code_prefix` independently.
- **`name` falls back to `code`** on save when blank.
- **Boolean checkbox derivation** — `active`, `code_apply`, `apply_regular_price`, `barcode_prefix`, `only_customer` are derived from the request payload on the controller side (the form sends `1`/`0`, not `yes`/`no` — different from the parent discount's row toggle which sends `yes`/`no`).
- **Date validation uses store-format** — the validator chains `date_format:<store-format>` and `dateToCarbon:<store-format>` using the store's display `date_format` setting (e.g., `d.m.Y` for BG / `Y-m-d` for ISO).

## How it works

The validation strings above are the **literal the application framework validator messages** the merchant sees inline next to each field. They are stable and ship in the platform's translation files under the `code_pro.validation.*` namespace. When citing an error in a support reply, prefer the verbatim string — merchants can grep for it in their browser.

## Related

- [[marketing-discounts-code-pro]] — hub.
- [[code-pro-form]] — the form structure that submits these fields.
- [[code-pro-business-rules]] — full set of save-time and runtime rules around these fields.
- [[code-pro-endpoints-api]] — the JSON-API v2 schema for the same fields; same validation.
- [[settings-statuses]] — `discounts_used_statuses` setting controls which statuses increment the `Uses` column.
- [[customers-custom-groups]] — target type for `customer_groups[]`.
- [[geo-zone]] — target type for `geo_zone_id`.

## Open questions

No outstanding questions.
