---
type: feature
nav_path: "Marketing → Discounts → Code PRO → Generator → Fields"
route_name: discounts-code_pro-generator
route_path: /admin/marketing-new/discounts/code-pro/:id/generator
aliases: ["Generator fields", "Generator backend keys", "Code PRO generator field reference"]
tags: [marketing, discounts, coupons, code-pro, bulk-generation]
plan_gates: ["discount-code-pro", "discount-code-pro-generator"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Code PRO generator — fields reference

> Part of [[marketing-discounts-code-pro-generator]]. See the hub for related aspects (form layout, modes, validation, business rules, API).

## Purpose

This aspect is the **field-level reference** for the Code PRO bulk generator: every visible input, its backend key, what it controls, and its validation rules. Two tables: generator-type and code-shape fields (Range / Random parameters), then the shared per-code fields applied uniformly to every generated row.

## Where to find it

Every field documented here lives on the bulk-generator page: **Marketing → Discounts → Code PRO → "Generate codes" toolbar button** — route name `discounts-code_pro-generator`, path `/admin/marketing-new/discounts/code-pro/:id/generator`. See [[code-pro-generator-form-layout]] for the settings-box layout that groups these fields visually.

## What the merchant can do here

Configure both the **generator-type-specific fields** (Range or Random parameters; only one set is in use per submission) and the **shared per-code fields** that propagate to every generated code in the batch.

## Settings & fields

### Generator type and code-shape fields

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Generator type** | `code.generator_type` | `range` or `random`. | Implicit; defaults to `range`. |
| **From** (range) | `code.from` | First integer in the sequence. | Required if generator_type = range; numeric, int, 1-999999999999999; numeric-range validator checks total count ≤ plan cap. |
| **To** (range) | `code.to` | Last integer in the sequence. | Required if generator_type = range; numeric, int, 1-999999999999999; must be greater than `code.from`. |
| **Limit** (random) | `code.limit` | How many codes to produce. | Required if generator_type = random; numeric, int, 1-`<plan-cap>`; numeric-random validator checks against max representable numeric of `length`. |
| **Length** (random) | `code.length` | Characters per code (uniform across the batch). | Numeric, int, 6-18; nullable (blank = random length per code between 6 and 18). |
| **Structure** (random) | `code.structure[]` | Array containing `alpha` and/or `numeric`. | Required if generator_type = random; array; at least one element. |

For the pipeline that consumes these fields, see [[code-pro-generator-modes]].

### Shared per-code fields (applied to every generated code)

These propagate uniformly — every code in the batch carries the **same** values for every row in this table. Only the `code` string differs across rows. The `name` is also set equal to the `code` string.

| Field | Backend key | Notes |
|-------|-------------|-------|
| **Active** | `active` | Boolean — all generated codes share this flag. |
| **Stack on discounted products** | `code_apply` | Boolean. |
| **Apply to base price** | `apply_regular_price` | Boolean. Only visible when `code_apply = 1`. |
| **Barcode prefix** | `barcode_prefix` | Boolean. |
| **Only registered customers** | `only_customer` | Boolean. |
| **Region** | `geo_zone_id` or `all_regions` | Either pick a [[geo-zone]] or check "All regions". |
| **Max uses (total)** | `max_uses` or `unlimited` | Integer 1-100,000 or "Unlimited" → NULL. |
| **Max uses per customer** | `maxused_user` or `unlimited_user` | Integer 1-100,000 or "Unlimited" → NULL. |
| **Date start** | `date_start` | Required; parsed against the store's `date_format`. |
| **Date end** | `date_end` or `no_expire` | Required unless `no_expire` checked. |
| **Conditions** | `condition[]` | Same schema as [[marketing-discounts-code-pro]]'s per-code conditions. Up to 5 condition rows. |
| **Customer groups** | `customer_groups[]` or `customer_groups_target` | Pick groups or "All groups". |

## Business rules

- The conditions builder is the **same** repeating `DiscountsCodeProConditionsConfig` block used by the per-code form — see [[code-pro-form]] for the condition schema and types.
- `date_start` and `date_end` are parsed against the **store's display date format** (e.g., `d.m.Y` for BG, `Y-m-d` for ISO). Merchants typing in their preferred format always work — but copy-pasting a date in a different format will fail validation. The platform does not auto-detect the format.
- `apply_regular_price` is only visible when `code_apply = 1` — preventing the merchant from saving a nonsensical "stack-off + base-price-on" combination.
- The campaign-countdown timer field is HIDDEN on this page (`hide-timer: true`) — see [[code-pro-generator-form-layout]] for why.

## Related

- [[marketing-discounts-code-pro-generator]] — hub.
- [[code-pro-generator-form-layout]] — the visual layout that surfaces these fields.
- [[code-pro-generator-modes]] — what Range vs Random parameters drive at submit time.
- [[code-pro-generator-validation]] — full validation-message list for every field.
- [[code-pro-form]] — per-code form sharing the conditions sub-component.
- [[marketing-discounts-code-pro]] — parent feature (the discount these codes belong to).
- [[geo-zone]] — region entity used by `geo_zone_id`.
- [[customers-custom-groups]] — customer-group catalogue queried by the picker.

## Open questions

None.
