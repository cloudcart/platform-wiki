---
type: feature
nav_path: "Marketing → Discounts → Code PRO codes → Export → Columns"
route_name: discounts-code_pro-list
route_path: /admin/marketing-new/discounts/code-pro/:id
aliases: ["Code PRO export columns", "Export CSV column layout", "56 columns", "Condition columns export"]
tags: [marketing, discounts, code-pro, export, csv]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-code-pro-export]]. See the hub for the other aspects (overview, format, business rules).

# Code PRO export — CSV column layout

## Purpose

This aspect documents the **fixed CSV column layout** of the Code PRO codes export: the 16 base columns, the 8 columns per condition slot across 5 slots, the 56-column total, and how codes with fewer or more than 5 conditions are handled. The column set is **not configurable** — see [[code-pro-export-overview]] for why there is no column-picker.

## Where to find it

These columns appear in the `discount-codes-pro.csv` file produced by the "Export" toolbar anchor on the [[marketing-discounts-code-pro]] codes list — `GET /admin/api/core/discounts/code-pro/{id}/export`. The header row is the first CSV line after the UTF-8 BOM (see [[code-pro-export-format]]).

## What the merchant can do here

- **Read the full per-code terms** of every code in one spreadsheet: name, code string, active flag, barcode info, apply / overwrite flags, date window, usage stats, customer-only flag, geo zone, and timestamps.
- **Inspect up to 5 conditions per code**, each expanded into 8 columns (target type, discount type, value, and the targeted product / category / vendor / collection names + order-over amount).
- **Correlate the target type with the discount mechanic** — column "Condition i type" carries the target type, "Condition i type value" carries the flat / percent / shipping mechanic.

## Settings & fields

### Base columns (16) — fixed order

| # | Column | Source | Notes |
|---|--------|--------|-------|
| 1 | `Name` | `code.name` | Falls back to `code` value when blank. |
| 2 | `Code` | `code.code` | Prefixed with a space (` <code>`) so Excel doesn't auto-cast numeric codes to numbers — see [[code-pro-export-format]]. |
| 3 | `Active` | `yes` / `no` | Per the code's `active` flag. |
| 4 | `Is barcode` | `yes` / `no` | Derived solely from `code_format` — `yes` when `code_format ∈ {ean8, ean13}`, otherwise `no`. (Older wiki phrasing said the flag is derived from `code_prefix` + `code_format`; that was incorrect — `code_prefix` is not part of the derivation.) |
| 5 | `Barcode format` | Barcode-prefix display text | Empty if not a barcode. |
| 6 | `Apply to discounted products` | `yes` / `no` | Per `code_apply`. |
| 7 | `Overwrite product discount` | `yes` / `no` | Per `apply_regular_price`. |
| 8 | `Valid from` | ISO 8601 UTC, start of day | `date_start` converted to UTC start-of-day. |
| 9 | `Valid to` | ISO 8601 UTC, end of day, or empty | `date_end` converted to UTC end-of-day if set; empty when `date_end IS NULL`. |
| 10 | `Uses` | Integer | Current redemption count (counted-status orders only). |
| 11 | `Max uses` | Integer or empty | `''` when `max_uses IS NULL` (unlimited). |
| 12 | `Max uses per user` | Integer or empty | `''` when `maxused_user IS NULL` (unlimited). |
| 13 | `Only for customers` | `yes` / `no` | Per `only_customer`. |
| 14 | `Geo zone` | Geo zone name or empty | Looks up the geo zone's name; empty when `geo_zone_id IS NULL`. |
| 15 | `Created at` | ISO 8601 timestamp | Per `created_at`. |
| 16 | `Updated at` | ISO 8601 timestamp | Per `updated_at`. |

### Condition columns (8 per condition slot × 5 slots) — fixed order

For each condition slot `i` from 1 to 5 the export adds 8 columns:

| # | Column | Source |
|---|--------|--------|
| 1 | `Condition i type` | The condition's `setting` (e.g., `all_products`, `order_over`, `product`, `category`, `vendor`, `selection`, `category_vendor`, `free_shipping`) — note this is the **target type**, not the discount type. See [[code-pro-export-business-rules]] for the normalisation. |
| 2 | `Condition i type value` | The condition's `type` (`flat` / `percent` / `shipping`). |
| 3 | `Condition i value` | The discount value, formatted per type (percent vs money). |
| 4 | `Condition i product` | Semicolon-separated unique product names (when setting = `product` or `category_vendor`). |
| 5 | `Condition i category` | Semicolon-separated unique category names (when setting = `category` or `category_vendor`). |
| 6 | `Condition i vendor` | Semicolon-separated unique vendor names (when setting = `vendor`). |
| 7 | `Condition i selection` | Semicolon-separated unique smart-collection names (when setting = `selection`). |
| 8 | `Condition i order_over` | The order-over amount, formatted as money. |

**Total columns:** 16 base + (8 × 5) = **56 columns per row.**

### Codes with fewer than 5 conditions

Codes that have fewer than 5 conditions get **empty strings** in the unused condition slots. Codes with more than 5 conditions get **silently truncated** to the first 5 (in `row` order — the same grouping the per-code form uses).

## Business rules

- **The column set is fixed** — there is no column-picker (see [[code-pro-export-overview]]).
- **Column 1 of each condition carries the target type, column 2 the discount mechanic** — they are not the same thing; see [[code-pro-export-business-rules]] for the target-type normalisation table.
- **Multi-record conditions are semicolon-joined and de-duplicated** — a condition targeting three products renders `Product A; Product B; Product C` in the product column. See [[code-pro-export-business-rules]].
- **5-condition ceiling** — anything past the fifth condition is dropped from the CSV, even though it still applies to the code at redemption.

## Related

- [[marketing-discounts-code-pro-export]] — hub.
- [[marketing-discounts-code-pro]] — the rows being exported.
- [[discount-code]] — entity page for each code row.
- [[customers-custom-groups]] — customer-group names referenced per code.
- [[geo-zone]] — geo zone names in the `Geo zone` column.
- [[products-smart-collections]] — collection names in `Condition i selection`.
- [[products-vendors]] — vendor names in `Condition i vendor`.
- [[products-categories]] — category names in `Condition i category`.
- [[products-products]] — product names in `Condition i product`.

## Open questions

No outstanding questions.
