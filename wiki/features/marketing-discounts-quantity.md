---
type: feature
nav_path: "Marketing → Discounts → Quantity"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/quantity
aliases: ["Quantity Discount", "Buy-N-Get-M", "BOGO", "Volume discount", "Tier discount", "Buy more pay less", "Количествена отстъпка"]
tags: [marketing, discounts, quantity, bogo, tier]
plan_gates: ["discount_quantity", "total_discounts"]
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---

# Quantity discount (volume / buy-more-pay-less)

## Purpose

The **Quantity discount** is the merchant's "buy more, pay less" promotion type — a single product gets **tiered per-unit pricing** based on how many of it the customer puts in the cart. The merchant picks ONE product, then declares up to twelve **tiers**: each tier says "starting from N pieces, the unit price drops to X". The customer sees the price ladder on the product page and on the storefront cart line, and the platform automatically applies the matching tier when their cart-line quantity crosses each threshold.

Typical merchant scenarios:

- **Wholesale ladders** — "1-9 pcs: 10 EUR each; 10-49: 8 EUR each; 50+: 6 EUR each."
- **Pack incentives** — "Buy 3 of this T-shirt, pay 15 EUR each (instead of 20)."
- **BOGO equivalents** — "Buy 2, get 1 free" = "buy 3 pcs, set the unit price so the third is free."

Unlike [[marketing-discounts-fixed]] (fixed price per variant regardless of cart quantity) and the **Global / Promo code** types (which discount the whole cart or a sub-total), a Quantity discount is **cart-quantity-aware on a single product**. Add one more piece, drop into the next tier; remove pieces, climb back up. Each Quantity discount is bound to **one product only**, and a product can only be on **one active Quantity discount at a time** — see [[quantity-discount-uniqueness-constraint]].

## Sub-pages (in this cluster)

Six aspect pages. Drill into the one that matches the question.

- [[quantity-discount-form]] — form layout (four blocks), every field + validation, the omitted-fields catalogue vs other discount types.
- [[quantity-discount-tier-evaluation]] — "≥ quantity wins" cart-time logic; 12-tier cap; `0`-value rejection; per-line evaluation for same product / different variants.
- [[quantity-discount-stacking]] — how a Quantity tier ranks against up-sell, cross-sell, bundle, and per-variant Fixed discounts on the same line; interaction with promo codes.
- [[quantity-discount-uniqueness-constraint]] — one Quantity discount per product (active + inactive both count); deactivation does NOT free the slot; the error strings.
- [[quantity-discount-plan-gating]] — `discount_quantity` + `total_discounts` caps; *"Not supported by plan"* card; over-cap response; not exposed on JSON-API v2.
- [[quantity-discount-storefront-display]] — product-page tier-ladder rendering; admin order-edit does NOT re-evaluate tiers (saved price persists).

## Where to find it

From the [[marketing-discounts]] list, click **+ Add discount** and pick the **Quantity discount** card from the type-picker modal. The card's blurb reads:

> *"With this discount you can decrease a product's price based on the quantity added to the cart."*

If the merchant's plan doesn't include the `discount_quantity` feature, the card shows **"Not supported by plan"** and is disabled — see [[quantity-discount-plan-gating]].

The breadcrumb on the form reads "Marketing → Discounts → Create discount". The URL is `/admin/marketing-new/discounts/create/quantity`. After save, the merchant lands on the edit URL `/admin/marketing-new/discounts/edit/{id}`.

## What the merchant can do here (at a glance)

- **Toggle Active / Inactive**; no 10-minute activation cooldown applies to Quantity discounts.
- **Name the discount** (`name`).
- **Pick the target product** (`product_id`) — one-per-discount + one-per-product. See [[quantity-discount-uniqueness-constraint]].
- **Build up to 12 tiers** — each tier has a **Quantity** + **Unit price**.
- **Restrict to customer groups** — `customer_groups[]` allow-list at the parent-discount level (not per-tier). Empty = everyone, including guests.
- **Date range** — `date_start` / `date_end` / **No expiration**. No timer fields render.

What the merchant **cannot** do: add the same product twice, save with `0` in either tier field, use a coupon code, set `max_uses` / `maxused_user`, set a region / geo-zone restriction, set per-variant tiers, or set per-tier customer groups. The Quantity form is the narrowest of all discount types — see [[quantity-discount-form]] for the omitted-fields catalogue.

## Settings & fields (summary)

The full per-field tables — labels, backend keys, validation strings, defaults — live on [[quantity-discount-form]]. At a glance, the form composes four blocks:

1. **General settings** — `active`, `name`.
2. **Discount conditions** — `product_id` + tier rows (`conditions[].quantity` + `conditions[].discount_value`).
3. **Customer groups** — `customer_groups[]`.
4. **Date range** — `date_start` / `date_end` / `no_expire` (no timer fields).

## Business rules (at a glance)

The detailed rules — with validation strings, edge cases, cart-time consequences — live on the aspect pages. Headlines:

- **One product, one Quantity discount** — counted across active AND inactive. *"A volume discount with this product already exists"* (BG: *"Вече съществува количествена отсъпка с този продукт"*); form-validator *"Product is already in use"*. See [[quantity-discount-uniqueness-constraint]].
- **12-tier cap + `empty(0)` rejection** — UI hides **+ Add new condition** at 12 rows; tier values of exactly `0` are rejected with *"All conditions must be fulfilled"* (BG: *"Всички условия трябва да се попълнят"*). See [[quantity-discount-tier-evaluation]].
- **"≥ quantity wins"** — tiers sort by `quantity` DESC; the first whose threshold ≤ cart-line quantity wins. Below the smallest tier, the Quantity ladder does not apply. See [[quantity-discount-tier-evaluation]].
- **Quantity tier beats per-variant Fixed; up-sell / cross-sell / bundle beat Quantity** — per-line discount-priority resolver. See [[quantity-discount-stacking]].
- **`code_apply` branch mostly dormant** — the form does NOT expose `code_apply`; defaults to `0`. The "subtract `save` before promo-code allocation" branch effectively never fires for admin-saved discounts. See [[quantity-discount-stacking]].
- **Plan-gated** — `discount_quantity` (per-plan cap; lower plans see *"Not supported by plan"*, extendable via feature pack) + `total_discounts` (aggregate cap across all discount types). Not exposed on JSON-API v2; programmatic create is admin-panel only. See [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]], and [[quantity-discount-plan-gating]].
- **`max_uses` / `maxused_user` / `force_save` / region / code / `code_apply` — not used** for this type. Only `name`, `active`, `product_id`, and the tier rows are validated. See [[quantity-discount-plan-gating]].
- **Auto-disable runs in UTC** — daily sweep flips `active = no` when `date_end` is ≥ 1 day past in **UTC**. Storefront cart-engine evaluates in store timezone, so customers' carts stop applying tiers at expected local time, while the merchant's listing keeps showing Active for up to ~27 hours after end-of-day (Europe/Sofia). Part of [[background-queue-inventory]].
- **Always-automatic, never code-based** — no code field. Activates purely from cart-line quantity. See [[quantity-discount-stacking]] for interaction with externally-applied promo codes.

## Related

- [[marketing-discounts]] — parent feature; one of seven discount types.
- [[marketing-discounts-fixed]] — per-variant fixed-price discount; fallback when no Quantity tier matches.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-codes]] / [[marketing-discounts-code-pro]] — sibling discount types.
- [[discounts-lifecycle]] / [[discounts-eligibility]] / [[discounts-storefront-display]] — cross-cutting discount aspects.
- [[apps-cart-rules]] — composes multi-product / multi-condition promotions Quantity cannot express.
- [[products-products]] — the target product; `quantity_discounts` relation.
- [[customers-custom-groups]] — `customer_groups[]` audience filter.
- [[discount]] — entity page for the parent Discount record (type=`quantity`).
- [[settings-hooks]] — fires `discount.created` / `discount.updated` / `discount.deleted` webhooks on save.
- [[analytics-top-order-product-discounts]] — analytics for top product-level discount usage.
- [[background-queue-inventory]] — daily auto-disable sweep (UTC).

## Open questions

No outstanding questions.
