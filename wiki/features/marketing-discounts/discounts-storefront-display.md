---
type: feature
nav_path: "Marketing → Discounts → Storefront display"
route_name: ""
route_path: ""
aliases: ["Discount storefront display", "From/Now pricing", "Discount badge", "Discount label", "Strikethrough price", "Discount banner", "Countdown timer", "Discount popup effect", "Hide discounted price", "MSRP display", "Display effect", "Confetti", "Fireworks", "Per-product attachment regeneration", "Listing engine", "Изобразяване на отстъпки на сайта", "Стара цена нова цена"]
tags: [marketing, discounts, promotions, storefront, ui, listing-engine]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

# Discount storefront display

> Part of [[marketing-discounts]]. See the hub for the other cross-cutting aspects (lifecycle, eligibility, audit trail, known issues) plus per-type details.

## Purpose

**What the customer sees** when a discount is active (was / now pricing, badge, timers, popup effect) and the per-variant price rows behind it.

## Where to find it

**Sidebar → Marketing → Discounts → Edit form.** Three blocks: **Color settings** (background + text colour), **Discount's amount in label** (a radio with **two** choices — As percent / As fixed amount), and **Date range** (timer switches `timer_list` + `timer_details`). These appear only on the **Global** (Flat / Percent / Free shipping) and **Fixed** forms. For the Countdown celebration effect, see [[marketing-discounts-countdown]].

## What the merchant can do here

- Pick a background + text colour for the on-product badge.
- Choose whether the badge shows percent (-15 %) or fixed amount (-10 EUR) — the two options in the "Discount's amount in label" radio.
- Show / hide the countdown badge on product listings (`timer_list`) and product detail pages (`timer_details`).
- (Countdown only) Pick the celebration animation — see [[marketing-discounts-countdown]].

## Settings & fields

| Field / Control | Backend key | What it does | Validation |
|-----------------|-------------|--------------|------------|
| **Background color** | `color` | Hex colour of the on-product badge background. | String (hex). |
| **Text color** | `text_color` | Hex colour of the badge text. | String (hex). |
| **Discount's amount in label** | `discount_amount_type_in_label` | What to display on the badge — the radio offers **only two** choices: **As percent** (`in_percent`) or **As fixed amount** (`in_flat`). Auto-defaults to `in_percent` when `type=percent`, `in_flat` when `type=flat`. | `in_percent` / `in_flat`. (A third value `dont_change` exists in the backend and is the seeded default for auto-created / Container discounts, but it is **not** selectable in this radio.) |
| **Show timer in product listing** | `timer_list` | Renders countdown badge on category / collection pages. Auto-disables when `date_end` is empty. | 1 / 0. |
| **Show timer in product details page** | `timer_details` | Renders countdown badge on the product detail page. Disabled until an end date is set. | 1 / 0. |
| **Banner position** | `position` | Where a label / banner appears on the product card. | `top-left` / `top-right` / `bottom-left` / `bottom-right`. |
| **Display effect** (Countdown) | `countdown_popup_effect` | The celebration animation type that fires at trigger. | `confetti` / `fireworks` / `school_pride` / null. |

## Business rules

### Per-product attachment regeneration — the listing-engine pipeline

When a no-code Flat or Percent discount or a Fixed discount is **created, edited, or has its target list changed**, the platform regenerates its per-variant rows. These rows are what the storefront reads to render "From X / Now Y" pricing on category and product detail pages. The list switch, bulk status and list delete start no rebuild.

The rows are written during the save; listings and smart collections refresh afterwards.

Triggers: a discount saved → rows for its matching products; target list edited → rows recomputed. A product saved from its form, the JSON-API, Google Sheets or an import rebuilds its own no-code Flat / Percent rows from the new price and re-checks its Fixed rows (`save = catalog − fixed`; a catalog price at or below the fixed price **deactivates** the row). A price changed on the **Inventory** screen or by an Admin GraphQL bulk price change rebuilds nothing, except a discount aimed at a smart collection, rebuilt whenever that collection re-evaluates.

### Storefront cache invalidation

Saving a discount flushes the product-page, category-fragment and variant-picker caches of the affected products before the listing refresh, so the storefront briefly reads from the database.

### Strikethrough rules

By default the storefront renders ~~10.00 EUR~~ **8.50 EUR** when a discount is on, with `save = variant.price − fixed_price` on a Fixed discount. The badge / label is rendered separately if `discount_amount_type_in_label` is `in_percent` or `in_flat`.

The **Discount price options** box (show MSRP as the "was" price, hide the discounted price) is not available on standard stores.

### After a price change that rebuilt nothing

Until the product is saved again through one of the paths above, or the discount is saved (rebuilding all its rows), a no-code Percent or Flat discount shows mixed values:

- **Now** price, on the product page and listings: the stored row, worked out from the old price.
- **Was** (struck-through) price: the current price.
- **You save** (*Спестяваш*): current price minus the stored row on the product page; listings show the saving stored with the row.
- The cart takes the percent off the current price, so the charge is right.

### Badge percent and where it shows

With **As percent**, a Percent discount's badge shows its own percentage, whatever the prices. For a Fixed or Flat discount the percent is worked out from the prices: per variant on the product page; on listings once per product, from the default variant's price row against that variant's price. Every theme shows the badge on the product page's main image; some also on product cards. Category, collection, vendor and search result pages share the same card, so search results show the same struck-through price and badge.

### Countdown timer + popup effect

The `timer_list` (product listings) and `timer_details` (product detail pages) switches are on the Global and Fixed forms and show that discount's end-date timer; both **auto-disable** when `date_end` is empty. A Countdown discount has no such switches: its timer runs at **checkout**, via the countdown popup, and the merchant cannot disable it.

When the countdown popup first shows at checkout, the `countdown_popup_effect` animation fires (`confetti`, `fireworks` or `school_pride`); preview it on the Countdown edit form. See [[marketing-discounts-countdown]].

### Label / Banner — visual only

The Label / Banner type is purely a product-card decoration. It is NOT a price reduction — adding a Label or Banner does NOT change the cart price. Full config lives on [[products-banners-labels]].

### Smart-collection refresh on discount save

Saving a discount also refreshes [[products-smart-collections]] that use it or the **Sale** rule, in the background. A discount starting on a later date joins a Sale collection at the nightly check — see [[smart-collection-entity-discount-link]].

## Related

- [[marketing-discounts]] — hub.
- [[discounts-lifecycle]] — status switch and date window.
- [[discounts-audit-trail]] — webhook events.
- [[discounts-known-issues]] — shipping-discount tie-break at checkout.
- [[marketing-discounts-fixed]] — per-variant fixed-price configuration.
- [[marketing-discounts-countdown]] — countdown timer + popup effect picker.
- [[products-banners-labels]] — Label / Banner visual-only discount type.
- [[products-smart-collections]] — "On sale" smart collections refreshed on discount save.
- [[storefront-architecture]] — the read-side architecture (the search index + DB caches).

## Open questions

- Exact cache-key list invalidated on discount save `(verify)`.
