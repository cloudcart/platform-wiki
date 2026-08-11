---
type: feature
nav_path: "Marketing → Discounts → Container codes → Generator"
route_name: discounts-codes_list
route_path: /admin/marketing-new/discounts/codes
aliases: ["Container codes generator", "Generate codes modal", "Bulk code generation", "Code shape and uniqueness", "Генериране на промо кодове", "1000 кода на заявка"]
tags: [marketing, discounts, coupons, container, generated-codes, generator]
plan_gates: ["discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Container codes — the bulk generator

> Part of [[marketing-discounts-codes]]. See the hub for the list view, redemption, parent-term inheritance, and the JSON-API.

## Purpose

The generator is how the merchant mass-creates single-use Container codes. It produces a batch of unique, identically-termed coupons in one transaction — the engine behind campaigns like "1,000 unique 10%-off codes for newsletter subscribers". The 10-character code shape is fixed platform behaviour. The **1,000-per-request batch cap applies to the legacy generator only** — the modern Vue modal validates only that the count is at least 1, with **no upper cap**.

## Where to find it

The bulk-generator modal is opened from the *Generate codes* action on the Container codes list page (`/admin/marketing-new/discounts/codes`). It saves in a single transaction. To generate **flat-amount** Container codes, the merchant uses the legacy generator URL `/admin/discounts/generate-codes` (the modern modal sends percent only — see below).

## What the merchant can do here

### Modern Vue modal

The modern Vue Container codes list page wraps the standard table and embeds the `DiscountsCodeGeneratePopup` modal. Layout:

- Title: *"Generate codes"*.
- Field 1: **Amount of the discount** — percent input. The user types a percent value (e.g., 15 → sent as `value × 100 = 1500`).
- Field 2: **Amount of codes** — integer input.
- **Cancel** (ghost variant) + **Generate** primary button (with loader). Backdrop / Esc are disabled while saving.

Save calls the generate-codes-for-container API with `{ type: 'percent', value: input × 100, amount }`. On success it closes the modal, refetches the list, and toasts *"Codes generated successfully!"*. The form payload resets to `{type: "percent", value: 0, amount: 0}` whenever the modal closes.

The Vue modal **does not currently expose the flat-amount type toggle** — only `percent` is sent. Merchants generating flat-amount Container codes use the legacy generator instead.

### Legacy generator (flat + percent)

- Pick the discount **type**: `flat` (currency amount off) or `percent`.
- For `percent`: enter the percentage value (0-100). Validation caps the value against the maximum type-value across the store's Container discounts — see [[discounts-codes-parent-terms]] for the cap rule.
- Enter the **batch size** (number of codes) — between **1 and 1,000 per request**. To produce more than 1,000, run the generator multiple times.
- Submit. The platform creates that many 10-character uppercase alphanumeric codes in one transaction, retrying any that hit a unique-constraint collision so the final count always matches the requested amount.

## Settings & fields

| Field / Control | Backend key | What it does | Validation |
|-----------------|-------------|--------------|------------|
| **Discount type** | `type` | Whether generated codes give a flat-amount or percent discount. | Required; must be `flat` or `percent`. Else: *"The selected type is invalid"*. |
| **Percent value** | `value` | The percentage off (0-100, capped against the max Container type-value in store). | Required when type=`percent`. Else: *"The percentage value can not be empty"*. |
| **Flat value** | `value` | The currency-amount off, in store currency. | Required when type=`flat`. |
| **Number of codes** | `amount` | How many codes to generate in this batch. | Integer ≥ 1. The **legacy** generator caps at 1,000 (*"You can generate maximum 1000 promo codes"*); the **modern Vue modal has no upper cap**. |

> The type toggle, flat value, and max-value cap reflect the **legacy** generator. The modern Vue `DiscountsCodeGeneratePopup` exposes only **Amount of the discount** (percent) and **Amount of codes** — it always sends `type: 'percent'`.

## Business rules

### Code shape and uniqueness

Generated codes are exactly **10 uppercase characters, randomly composed from `[A-Z]` letters and `[0-9]` digits** — drawn from a 36-character alphabet, giving a search space of 36^10 ≈ 3.6 × 10^15 possible codes. The platform generates one code at a time inside the batch loop. On any unique-constraint violation (a duplicate), the batch counter bumps up by 1 and the loop retries, so:

- **No two codes collide** across the entire codes table — even if two batches in different Container discounts happen to roll the same string.
- **The merchant can predict exactly how many codes they end up with** (= the input `amount`).
- **There is no merchant-tunable code shape.** The character set (`A-Z` + `0-9`) and length (10) are hard-coded constants in the generator, not configurable settings. For prefix, suffix, fixed length, range-mode, or numeric-only generation, the merchant must use [[marketing-discounts-code-pro-generator]] on a [[marketing-discounts-code-pro]] discount — see [[discounts-codes-vs-code-pro]].

### Generator loop

The save endpoint runs:

1. Validate the inputs (`type`, `value`, `amount`).
2. Loop `amount` times — build a new code row with the chosen type/value and `active = 1`, fill it with a 10-char random uppercase alphanumeric string, and save. On a unique-constraint violation, increment `amount` by 1 (so this iteration doesn't count) and continue.
3. Return success.

On a heavily-populated codes table where collisions are more likely, the loop runs slightly longer than `amount` iterations but always produces exactly `amount` final rows.

### Bulk-generate cap = 1,000 per request

The hard cap is **`amount BETWEEN 1 AND 1,000`** per generate request. To produce 5,000 codes, run the generator 5 times. There is no plan-feature-gated higher limit for Container codes; it is a fixed platform cap — unlike [[marketing-discounts-code-pro-generator]], which caps at the `discount-code-pro-generator` plan-feature value (default 5,000 per request). Practical guidance:

- Plan campaigns in 1,000-code batches so each finishes in a single transaction.
- For very large campaigns (100,000+ codes), Code PRO with `random` mode is more efficient because it does up to 5,000 codes per request.

> Programmatic generation via JSON-API v2 has **no built-in 1,000 cap** — see [[discounts-codes-api]].

## Related

- [[marketing-discounts-codes]] — hub.
- [[marketing-discounts-code-pro-generator]] — alternative generator with shape controls and a higher cap.
- [[discount-code]] — entity page for individual generated codes.

## Open questions

No outstanding questions.
