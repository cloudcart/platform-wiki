---
type: feature
nav_path: "Marketing → Discounts → Quantity"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/quantity
aliases: ["Quantity Discount", "Buy-N-Get-M", "BOGO", "Volume discount", "Tier discount", "Buy more pay less", "Количествена отстъпка"]
tags: [marketing, discounts, quantity, bogo, tier]
plan_gates: ["discount_quantity", "total_discounts"]
created: 2026-05-23
updated: 2026-11-09
source_count: 5
---

# Quantity discount (volume / buy-more-pay-less)

## Purpose

The **Quantity discount** is the "buy more, pay less" type: ONE product gets **tiered per-unit pricing**. Each tier says "from N pieces, the unit price is X", one price for all variants or one per variant. The customer sees the ladder on the product page, and the cart applies the matching tier when the pieces on a line cross a threshold.

Typical merchant scenarios:

- **Wholesale ladders** — "1-9 pcs: 10 EUR each; 10-49: 8 EUR each; 50+: 6 EUR each."
- **Pack incentives** — "Buy 3 of this T-shirt, pay 15 EUR each (instead of 20)."
- **"3 for 2", approximately** — a tier at 3 pieces with the unit price at two-thirds of the regular price (rounded to the cent). The tier price applies to **every** piece on the line, once, not per group of 3: 3 pieces cost about the price of 2, 6 cost the price of 4, and 4 pieces also pay two-thirds each, not "one free". An exact "every 3rd free" has no native setting. The former **Buy X get Y** type (*Купи Х вземи Y*: buy N of one product, get 1 piece of another cheaper or free) was removed on 2026-03-05.

Each Quantity discount is bound to **one product only**, and a product can only be on **one Quantity discount at a time, active or not** — see [[quantity-discount-uniqueness-constraint]].

## Sub-pages (in this cluster)

Seven aspect pages. Drill into the one that matches the question.

- [[quantity-discount-form]] — form layout (five blocks), every field + validation, the omitted-fields catalogue vs other discount types.
- [[quantity-discount-tier-evaluation]] — "≥ quantity wins" cart-time logic; 12-tier cap; `0`-value rejection.
- [[quantity-discount-line-counting]] — each cart line counts alone; the **Quantity counting** switch and how it saves.
- [[quantity-discount-stacking]] — how a Quantity tier ranks against up-sell, cross-sell, bundle, and per-variant Fixed discounts on the same line; interaction with promo codes.
- [[quantity-discount-uniqueness-constraint]] — one Quantity discount per product (active + inactive both count); deactivation does NOT free the slot; the error strings.
- [[quantity-discount-plan-gating]] — the plan check on create; the `discount_quantity` quota on the Admin GraphQL API; `total_discounts` as a displayed figure; not exposed on JSON-API v2.
- [[quantity-discount-storefront-display]] — product-page tier-ladder rendering; admin order-edit does NOT re-evaluate tiers (saved price persists).

## Where to find it

From the [[marketing-discounts]] list, click **+ Add discount** and pick the **Quantity discount** card from the type-picker modal. The card's blurb reads:

> *"With this discount you can decrease a product's price based on the quantity added to the cart."*

The card stays clickable; the plan check runs when the discount is created — see [[quantity-discount-plan-gating]].

The breadcrumb on the form reads "Marketing → Discounts → Create discount". The URL is `/admin/marketing/discounts/create/quantity`. After save, the merchant lands on the edit URL `/admin/marketing/discounts/edit/{id}`.

## What the merchant can do here (at a glance)

- **Toggle Active / Inactive**; the switch takes effect immediately, any number of times.
- **Name the discount** (`name`).
- **Pick the target product** (`product_id`) — one-per-discount + one-per-product. See [[quantity-discount-uniqueness-constraint]].
- **Build tiers** — each tier has a **Quantity** + **Unit price**. For a product with one variant the tiers are simple rows (up to 12). For a product with more than one variant they form a table: clicking a tier's price opens **Quantity price**, where the merchant sets the quantity and picks **Common price** (one price for all variants) or **Multiple price** (a price per variant; a variant left empty gets no discount at that tier).
- **Quantity counting** — the form shows a switch to count all the product's cart lines (`quantity_count_all_lines`), but saving does not store it, so each cart line counts alone. See [[quantity-discount-line-counting]].
- **Restrict to customer groups** — `customer_groups[]` allow-list at the parent-discount level (not per-tier). Empty = everyone, including guests.
- **Date range** — `date_start` / `date_end` / **No expiration**. No timer fields render.

What the merchant **cannot** do: add the same product twice, save with `0` in either tier field, use a coupon code, set `max_uses` / `maxused_user`, set a region / geo-zone restriction, give different variants different tier quantities (the quantities are shared; only the price can differ per variant), or set per-tier customer groups. The Quantity form is the narrowest of all discount types — see [[quantity-discount-form]] for the omitted-fields catalogue.

## Settings & fields (summary)

The full per-field tables — labels, backend keys, validation strings, defaults — live on [[quantity-discount-form]]. At a glance, the form composes five blocks:

1. **General settings** — `active`, `name`.
2. **Discount conditions** — `product_id` + tier rows (`conditions[].quantity` + `conditions[].discount_value`), the price common to all variants or set per variant.
3. **Quantity counting** — `quantity_count_all_lines` (shown on the form; saving does not store it).
4. **Customer groups** — `customer_groups[]`.
5. **Date range** — `date_start` / `date_end` / `no_expire` (no timer fields).

## Business rules (at a glance)

Headlines; the detail is on the aspect pages:

- **One product, one Quantity discount** — counted across active AND inactive. *"A volume discount with this product already exists"* (BG: *"Вече съществува количествена отсъпка с този продукт"*); form-validator *"Product is already in use"*. See [[quantity-discount-uniqueness-constraint]].
- **12-tier cap + `empty(0)` rejection** — for a product with one variant, the UI hides **+ Add new condition** at 12 rows (the per-variant tier table has no cap); a tier price higher than the variant's current price is rejected with *"The quantity discount price cannot be higher than the variant current price"* (BG: *"Цената на количествената отстъпка не може да бъде по-висока от текущата цена на разновидността"*); with **Multiple price**, a variant's empty price only means no discount for that variant; tier values of exactly `0` are rejected with *"All conditions must be fulfilled"* (BG: *"Всички условия трябва да се попълнят"*). See [[quantity-discount-tier-evaluation]].
- **"≥ quantity wins"** — tiers sort by `quantity` DESC; the first whose threshold ≤ the line's pieces wins, and each cart line pays its own variant's price at that tier. Each line counts alone ([[quantity-discount-line-counting]]). Below the smallest tier, the Quantity ladder does not apply. See [[quantity-discount-tier-evaluation]].
- **Quantity tier replaces the Fixed price; up-sell / cross-sell / bundle beat Quantity** — per-line discount-priority resolver. See [[quantity-discount-stacking]].
- **`code_apply` is on for a discount saved from the admin form** — the form does not show it. The tier price then also has the variant's active Fixed or no-code Flat/Percent saving taken off, with or without a code; the ladder shows the plain tier price. See [[quantity-discount-stacking]].
- **Plan checks on create only** — the admin form checks whether the kind is enabled on the plan (`discount-quantity`). The Admin GraphQL API's `createDiscount` compares usage with `discount_quantity`, extendable via feature pack. `total_discounts` is a displayed figure, not enforced. Not exposed on JSON-API v2; the Admin GraphQL API ([[settings-pat-tokens]]) creates and edits it with `createDiscount` / `updateDiscount`, per-variant tier prices included. See [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]], and [[quantity-discount-plan-gating]].
- **`max_uses` / `maxused_user` / `force_save` / region / code — not used** for this type. Only `name`, `active`, `product_id`, and the tier rows are validated. See [[quantity-discount-plan-gating]].
- **Auto-disable runs in UTC** — an hourly sweep switches a discount off at the first run after 00:00 UTC on the day after its end date; carts stop applying tiers at the end of that date in store time. See [[background-queue-inventory]].
- **Always-automatic, never code-based** — no code field. Activates purely from the counted pieces. See [[quantity-discount-stacking]] for interaction with externally-applied promo codes.

## Related

- [[marketing-discounts]] — parent feature; one of seven discount types.
- [[marketing-discounts-fixed]] — per-variant fixed-price discount; fallback when no Quantity tier matches.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-codes]] / [[marketing-discounts-code-pro]] — sibling discount types.
- [[discounts-lifecycle]] / [[discounts-eligibility]] / [[discounts-storefront-display]] — cross-cutting discount aspects.
- [[apps-cart-rules]] — composes multi-product / multi-condition promotions Quantity cannot express.
- [[products-products]] — the target product; `quantity_discounts` relation.
- [[customers-custom-groups]] — `customer_groups[]` audience filter.
- [[discount]] — entity page for the parent Discount record (type=`quantity`).
- [[settings-hooks]] — `discount.created` / `discount.updated` webhooks fire when the discount record is saved through the form.
- [[analytics-top-order-product-discounts]] — analytics for top product-level discount usage.
- [[background-queue-inventory]] — hourly auto-disable sweep (UTC).

## Open questions

No outstanding questions.
