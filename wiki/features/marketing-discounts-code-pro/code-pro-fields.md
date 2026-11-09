---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Fields & validation"
route_name: discounts-code_pro-edit
route_path: /admin/marketing/discounts/code-pro/:id/:codeId
aliases: ["Code PRO fields", "Code PRO validation", "Code PRO field reference", "Code PRO listing columns"]
tags: [marketing, discounts, code-pro, fields, validation, reference]
plan_gates: ["discount-code-pro"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-discounts-code-pro]]. See the hub for the other aspects (overview, form, business rules, checkout, endpoints).

# Code PRO — fields, validation & listing columns

## Purpose

The **citation-level reference** for the per-code form: every field on [[code-pro-form]] with its key, what it does and the verbatim validation rule.

## Where to find it

The fields documented here are submitted by the form at `/admin/marketing/discounts/code-pro/:id/:codeId` (see [[code-pro-form]]). The validation strings come from the `code_pro.validation.*` translation keys; the listing columns are rendered by the `CcTable` on `/admin/marketing/discounts/code-pro/:id`.

## What the merchant can do here

Look up the exact field name, key, default, and validation string for any control on the per-code form or the codes list.

## Settings & fields

### Top-level fields and validation

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Active** | `active` | An inactive code is rejected at checkout. The form's switch saves the code as active either way; turn a code off with the Active toggle in the codes list. | `yes` / `no`. Default on. |
| **Code** | `code` | The literal string the customer enters. | Required, max 20, `alpha_num`, **unique on `discounts_code_pro.code`** when a new code is created. Error: *"Discount code is exists"* (`code_pro.validation.code.unique`). |
| **Code prefix (barcode)** | `code_prefix` | Treats the code as a barcode (with `code_format` ean13 / ean8). | 1 / 0; no input of its own: set to 1 when `code_format` is ean13 / ean8, else 0. |
| **Barcode format** | `code_format` | Barcode standard. | `ean13` / `ean8` / null. |
| **Barcode prefix** | `barcode_prefix` | When ON, treats the entered `code` as a prefix and the scanner's value as `code + scanned`. | 1 / 0. |
| **Stack on discounted products** | `code_apply` | Allow code on top of existing per-product discounts. | 1 / 0. Default 0 in the form; a single code created through JSON-API v2 without it is on. |
| **Apply to base price** | `apply_regular_price` | Works the code out on the regular price; if the code's price is lower than the discounted price, it replaces the product discount. | 1 / 0. |
| **Only registered customers** | `only_customer` | Refuses the code for guests with *"The code is valid only for registered users"*. The switch shows only when the code has an `order_over` condition. Saving an existing code through the edit form turns it on even when it was off. | 1 / 0. |
| **Date start** | `date_start` | Earliest day the code may redeem. | Required, formatted per store `date_format`. The form shows *"Field is required"*. |
| **Date end** | `date_end` | Last day the code may redeem (or NULL for "No expiration"). | Required unless `no_expire` is ON. |
| **Max uses (total)** | `max_uses` | Total redemptions across all customers. | Optional; integer 1–100,000. Blank means unlimited, with or without the `unlimited` switch. |
| **Max uses per customer** | `maxused_user` | Per-customer cap. | Optional; integer 1–100,000. Blank means unlimited, with or without the `unlimited_user` switch. |
| **Customer groups** | `customer_groups[]` | Whitelist of groups that may redeem. | With "All groups" off and none picked, the code has no group restriction. |
| **Region** | `geo_zone_id` | Geo zone restriction. | Must exist. With `all_regions` off and none picked, the code has no region restriction. |
| **Name** | `name` | Optional merchant-facing label; falls back to `code` value when blank. | Free string. |
| **Conditions array** | `condition[]` | The discount terms per code (see below). | Required, array. Error: *"Conditions are required"* (`code_pro.validation.condition.required`). |

### Per-condition fields

Each entry in the `condition[]` array is one discount term. The export reserves 5 columns; in practice **up to 5 conditions per code** is the documented design (the form only shows the first 5 even if more exist).

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Type** | `condition.*.type` | Discount type for this row: `flat` / `percent` / `shipping`. | Required. |
| **Value** | `condition.*.value` | Amount (flat) or percentage. | Required if type=`flat`/`percent`; numeric, min 0.01. |
| **Setting** | `condition.*.setting` | Target type: `all`, `order_over`, `product`, `category`, `vendor`, `selection`, `category_vendor`. | Required. |
| **Order-over amount** | `condition.*.order_over` | On `order_over`: the order subtotal threshold, at or above. On any other target: a minimum unit price per line, at or above (for `all`, lines are checked in cart order and the first below the minimum stops that condition). | Required if setting=`order_over` (or with `allow_price`); numeric, min 0.01. Error: *"Amount is required"* (`code_pro.validation.condition.order_over.required_if`). |
| **Product targets** | `condition.*.product` | Product IDs (select2 multi-pick). | Required if setting=`product`. |
| **Category targets** | `condition.*.category` | Category IDs. | Required if setting=`category` or `category_vendor`. |
| **Vendor targets** | `condition.*.vendor` | Vendor IDs. | Required if setting=`vendor` or `category_vendor`. |
| **Selection targets** | `condition.*.selection` | Smart-collection IDs. | Required if setting=`selection`. |

### What each target does with the value

What a target's amount comes off, across all discount kinds, is on [[discount-stacking-amount-by-target]]. For a Code PRO condition:

| Target (`setting`) | Flat value | Percent value | Rounding difference |
|---|---|---|---|
| `all` ("For every product in the cart") | Full amount off every matched line, once per line, whatever the quantity. | Off each line, with its options, after any product discount. | None; no split. |
| `order_over` ("Orders over") | One amount off the order, as a totals row, when the subtotal of the lines is at or above the threshold. | Percent of that subtotal (without option prices), as a totals row. | None. |
| `product`, `category`, `vendor`, `selection` | One amount per condition, split proportionally over its matched lines. | Off each line. | Put on the first matched line, so the split adds up to the amount. |
| `category_vendor` | Same split. | Off each line. | Not corrected; the split can end a cent off. |

The amount is never compared with the subtotal, for any target: lines and the total have no lower limit and can go below zero.

**Several conditions in one code:**

- A line takes the first specific condition that matches, in stored order, not the best one.
- `all` reaches only lines no specific condition matched; with two `all` conditions the later one overwrites.
- Each flat condition is split on its own, except when all specific conditions are smart collections with the same value: they act as one pool, and one line at the minimum price opens the collection for all its lines.
- Among `order_over` conditions, only the largest passing saving applies.
- Line conditions, one `order_over` amount and free shipping add up on the same order. The `order_over` minimum is checked on the subtotal of **every** cart line before the code, not only the lines a condition matched: after product discounts, or at regular prices with **Apply to base price** on.

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
- **Boolean checkbox derivation** — `code_apply`, `apply_regular_price` and `barcode_prefix` are on when the form sends them. `active` always saves as on. `only_customer` saves as on whenever sent, which an edit of an existing code does.
- **Dates use the store's format** — the store's display `date_format` setting (e.g., `d.m.Y` for BG / `Y-m-d` for ISO).

## How it works

The validation strings above are the **literal the application framework validator messages** the merchant sees inline next to each field. They are stable and ship in the platform's translation files under the `code_pro.validation.*` namespace. When citing an error in a support reply, prefer the verbatim string — merchants can grep for it in their browser.

## Related

- [[marketing-discounts-code-pro]] — hub.
- [[discount-stacking-amount-by-target]] — what a target's amount comes off, for every discount kind.
- [[code-pro-form]] — the form structure that submits these fields.
- [[code-pro-business-rules]] — full set of save-time and runtime rules around these fields.
- [[code-pro-endpoints-api]] — the JSON-API v2 schema for these fields; its own validation.
- [[settings-statuses]] — `discounts_used_statuses` setting controls which statuses increment the `Uses` column.
- [[customers-custom-groups]] — target type for `customer_groups[]`.
- [[geo-zone]] — target type for `geo_zone_id`.

## Open questions

No outstanding questions.
