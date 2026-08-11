---
type: feature
nav_path: "Marketing → Discounts → Storefront display"
route_name: ""
route_path: ""
aliases: ["Discount storefront display", "From/Now pricing", "Discount badge", "Discount label", "Strikethrough price", "Discount banner", "Countdown timer", "Discount popup effect", "Hide discounted price", "MSRP display", "Display effect", "Confetti", "Fireworks", "Per-product attachment regeneration", "Listing engine", "Изобразяване на отстъпки на сайта", "Стара цена нова цена"]
tags: [marketing, discounts, promotions, storefront, ui, listing-engine]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Discount storefront display

> Part of [[marketing-discounts]]. See the hub for the other cross-cutting aspects (lifecycle, eligibility, audit trail, known issues) plus per-type details.

## Purpose

This aspect covers **what the customer sees** when a discount is active — strikethrough "was / now" pricing, per-product badge / label, countdown timer, popup celebration effect (confetti / fireworks / school_pride), MSRP "was-price" override — plus the **per-product attachment regeneration** pipeline (the listing-engine job that rebuilds `product_to_discount` rows so the storefront renders badges fast).

## Where to find it

**Sidebar → Marketing → Discounts → Edit form.** Three blocks: **Color settings** (background + text colour), **Discount's amount in label** (a radio with **two** choices — As percent / As fixed amount), and **Date range** (timer switches `timer_list` + `timer_details`). The Color + amount-in-label blocks and the timer switches appear only on the **Global** (Flat / Percent / Free shipping) and **Fixed** forms — not on the code, container, quantity, or countdown forms. For the Countdown celebration effect, see [[marketing-discounts-countdown]].

## What the merchant can do here

- Pick a background + text colour for the on-product badge.
- Choose whether the badge shows percent (-15 %) or fixed amount (-10 EUR) — the two options in the "Discount's amount in label" radio.
- Show / hide the countdown badge on product listings (`timer_list`) and product detail pages (`timer_details`).
- Hide the "was / now" strikethrough (`hide_discount_price`) — show only the discounted price.
- (Fixed only) Show MSRP as the struck-through "was" price (`msrp = 1`) — see [[marketing-discounts-fixed]].
- (Countdown only) Pick the celebration animation — see [[marketing-discounts-countdown]].

## Settings & fields

| Field / Control | Backend key | What it does | Validation |
|-----------------|-------------|--------------|------------|
| **Background color** | `color` | Hex colour of the on-product badge background. | String (hex). |
| **Text color** | `text_color` | Hex colour of the badge text. | String (hex). |
| **Discount's amount in label** | `discount_amount_type_in_label` | What to display on the badge — the radio offers **only two** choices: **As percent** (`in_percent`) or **As fixed amount** (`in_flat`). Auto-defaults to `in_percent` when `type=percent`, `in_flat` when `type=flat`. | `in_percent` / `in_flat`. (A third value `dont_change` exists in the backend and is the seeded default for auto-created / Container discounts, but it is **not** selectable in this radio.) |
| **Display discounted price as a regular price** | `hide_discount_price` | Hides the "was X / now Y" formatting — shows only the discounted price. | 1 / 0. |
| **Manufacturer's Suggested Retail Price** | `msrp` | (Fixed only) Shows MSRP as the struck-through "was" price. | 1 / 0. |
| **Show timer in product listing** | `timer_list` | Renders countdown badge on category / collection pages. Auto-disables when `date_end` is empty. | 1 / 0. |
| **Show timer in product details page** | `timer_details` | Renders countdown badge on the product detail page. Disabled until an end date is set. | 1 / 0. |
| **Banner position** | `position` | Where a label / banner appears on the product card. | `top-left` / `top-right` / `bottom-left` / `bottom-right`. |
| **Display effect** (Countdown) | `countdown_popup_effect` | The celebration animation type that fires at trigger. | `confetti` / `fireworks` / `school_pride` / null. |

## Business rules

### Per-product attachment regeneration — the listing-engine pipeline

When a discount is **created, edited, status-toggled, deleted, or has its target list changed**, the platform regenerates the per-product attachment rows in `product_to_discount`. This table is what the storefront reads to render "From X / Now Y" pricing on category and product detail pages.

This is the slowest part of the discount lifecycle: for high-catalog stores (10 000+ products) it can take several minutes. It's the underlying reason for the 10-minute activation cooldown (see [[discounts-lifecycle]]) and the **"Latest update"** badge on freshly-saved discounts.

Triggers: new discount save → matching products get attachment rows; status `yes → no` → rows soft-deactivate; target list edited → rows recomputed against the new set; **catalog product price changed** (independent of any discount edit) → per-variant Fixed-discount rows auto-recalculate `save = catalog − fixed`; if catalog price drops at or below the fixed price, the row is **deactivated** (no fake "discount").

### Storefront cache invalidation

Saving a discount also flushes storefront caches: product-detail page cache (per affected product), category-page fragment cache, variant-picker fragment cache. The cache is flushed BEFORE the listing-engine regenerates rows, so the storefront briefly reads from the database while new rows are being built — usually milliseconds; on high-traffic stores it can be noticeable.

### Strikethrough rules — `hide_discount_price` opt-out

By default the storefront renders ~~10.00 EUR~~ **8.50 EUR** when a discount is on. `hide_discount_price = 1` disables the strikethrough — the storefront shows only the discounted price (useful for "stealth" sales or B2B price-list contexts). The badge / label is still rendered separately if `discount_amount_type_in_label` is `in_percent` or `in_flat` — the merchant can hide the strikethrough but keep the on-card "-15 %" badge.

### MSRP mode for Fixed discounts

When a Fixed discount has `msrp = 1`, the strikethrough price shown is the MSRP value, not the actual catalog price. The denormalised `save` column on the per-variant attachment row is computed differently:

- **Standard mode (`msrp = 0`)**: `save = variant.price − fixed_price` (catalog minus fixed).
- **MSRP mode (`msrp = 1`)**: `save = msrp_price − fixed_price` (MSRP minus fixed).

So in MSRP mode, the "Save X EUR" label shown to customers reflects the **apparent saving against MSRP**, not the actual saving against the catalog price the customer would otherwise see. See [[discounts-known-issues]] for the merchant-trap this can create. See [[marketing-discounts-fixed]] for the per-product configuration UI.

### Countdown timer + popup effect

The Countdown timer is rendered on three surfaces: **product listings** (gated by `timer_list = 1`), **product detail pages** (gated by `timer_details = 1`), and **checkout** (always, via `countdown_discount_popup` — the merchant cannot disable the checkout-stage timer). Both listing / detail switches **auto-disable** when `date_end` is empty.

When the customer adds the Countdown-discounted product to cart, a celebration animation fires per `countdown_popup_effect`: `confetti` (two-sided burst, 350 particles, 50° spread), `fireworks` (six positions, 550 ms intervals), or `school_pride` (1 000 red particles, 5 × 100 ms iterations). The merchant previews via the in-page Preview button on the Countdown edit form. See [[marketing-discounts-countdown]].

### Label / Banner — visual only

The Label / Banner type is purely a product-card decoration. It is NOT a price reduction — adding a Label or Banner does NOT change the cart price. Full config lives on [[products-banners-labels]].

### Smart-collection refresh on discount save

Saving a discount that targets specific products / categories also refreshes any [[products-smart-collections]] matching the affected products — an "On sale" smart collection automatically includes newly-discounted products. Part of the same async pipeline as the per-product attachment regen; contributes to the "Latest update" badge delay.

## Related

- [[marketing-discounts]] — hub.
- [[discounts-lifecycle]] — the 10-minute activation cooldown that throttles this regeneration pipeline.
- [[discounts-audit-trail]] — webhook events that fire when the regeneration completes.
- [[discounts-known-issues]] — MSRP-display gotcha + shipping-discount tie-break ambiguity at checkout.
- [[marketing-discounts-fixed]] — MSRP mode + per-variant fixed-price configuration.
- [[marketing-discounts-countdown]] — countdown timer + popup effect picker.
- [[products-banners-labels]] — Label / Banner visual-only discount type.
- [[products-smart-collections]] — "On sale" smart collections refreshed on discount save.
- [[storefront-architecture]] — the read-side architecture (the search index + DB caches).

## Open questions

- Exact cache-key list invalidated on discount save `(verify)`.
