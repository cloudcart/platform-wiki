---
type: feature
nav_path: "Marketing → Discounts → Container codes → Generator"
route_name: discounts-codes_list
route_path: /admin/marketing/discounts/codes
aliases: ["Container codes generator", "Generate codes modal", "Bulk code generation", "Code shape and uniqueness", "Генериране на промо кодове"]
tags: [marketing, discounts, coupons, container, generated-codes, generator]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

# Container codes — the bulk generator

> Part of [[marketing-discounts-codes]]. See the hub for the list view, redemption, parent-term inheritance, and the JSON-API.

## Purpose

The generator is how the merchant mass-creates Container codes. It produces a batch of unique percent codes — the engine behind campaigns like "1,000 unique 10%-off codes for newsletter subscribers". The 10-character code shape is fixed platform behaviour. The modal validates only that the count is at least 1, with **no upper limit**.

## Where to find it

The bulk-generator modal is opened from the *Generate codes* action on the Container codes list page (`/admin/marketing/discounts/codes`). Codes are saved one at a time, so a failure part-way leaves the ones already made.

## What the merchant can do here

### The modal

The Container codes list page embeds the `DiscountsCodeGeneratePopup` modal. Layout:

- Title: *"Generate codes"*.
- Field 1: **Amount of the discount** — percent input. The user types a percent value (e.g., 15 → sent as `value × 100 = 1500`).
- Field 2: **Amount of codes** — integer input.
- **Cancel** (ghost variant) + **Generate** primary button (with loader). Backdrop / Esc are disabled while saving.

Save calls the generate-codes-for-container API with `{ type: 'percent', value: input × 100, amount }`. On success it closes the modal, refetches the list, and toasts *"Codes generated successfully!"*. The form payload resets to `{type: "percent", value: 0, amount: 0}` whenever the modal closes.

The modal generates percent codes only; there is no flat-amount option.

## Settings & fields

| Field / Control | Backend key | What it does | Validation |
|-----------------|-------------|--------------|------------|
| **Amount of the discount** | `value` | The percent, sent as percent × 100. | Required (*"Value is required"*). Not compared with any Container. |
| **Amount of codes** | `amount` | How many codes to generate in this batch. | Integer ≥ 1 (*"Amount is required"*, *"Amount must be at least 1"*). No upper limit. |

## Business rules

### Code shape and uniqueness

Generated codes are exactly **10 uppercase characters, randomly composed from `[A-Z]` letters and `[0-9]` digits** — drawn from a 36-character alphabet, giving a search space of 36^10 ≈ 3.6 × 10^15 possible codes. The platform generates one code at a time inside the batch loop. On any unique-constraint violation (a duplicate), the batch counter bumps up by 1 and the loop retries, so:

- **No two codes collide** across the entire codes table — even if two batches in different Container discounts happen to roll the same string.
- **The merchant can predict exactly how many codes they end up with** (= the input `amount`).
- **There is no merchant-tunable code shape.** The character set (`A-Z` + `0-9`) and length (10) are hard-coded constants in the generator, not configurable settings. For a chosen length, range-mode, or numeric-only generation, the merchant must use [[marketing-discounts-code-pro-generator]] on a [[marketing-discounts-code-pro]] discount — see [[discounts-codes-vs-code-pro]].

### Generator loop

The save endpoint runs:

1. Validate the inputs (`type`, `value`, `amount`).
2. Loop `amount` times — build a new code row with the chosen type/value and `active = 1`, fill it with a 10-char random uppercase alphanumeric string, and save. On a unique-constraint violation, increment `amount` by 1 (so this iteration doesn't count) and continue.
3. Return success.

On a heavily-populated codes table where collisions are more likely, the loop runs slightly longer than `amount` iterations but always produces exactly `amount` final rows.

### No upper limit on the count

The modal accepts any count of 1 or more, and Container codes have no plan limit — unlike [[marketing-discounts-code-pro-generator]], which caps at the `discount-code-pro-generator` plan-feature value (default 5,000 per request). JSON-API v2 generate takes up to 1,000 per call — see [[discounts-codes-api]].

## Related

- [[marketing-discounts-codes]] — hub.
- [[marketing-discounts-code-pro-generator]] — alternative generator with shape controls.
- [[discount-code]] — entity page for individual generated codes.

## Open questions

No outstanding questions.
