---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Product reviews"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Product reviews module", "Product review listing", "Reviews carousel block", "Модул отзиви"]
tags: [design, modules, page-builder, product-review, marketing, reviews]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Product reviews block (`product_review`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Product reviews** block renders a list (or carousel) of customer reviews on a Dynamic page. Used for testimonial sections, social-proof rows on landing pages, and "What our customers say" blocks on the homepage. The block sources reviews from the **Product Review** app — the same database that powers product-page reviews — and lets the merchant filter by rating, review group, and per-product / aggregate display modes.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Product reviews** from the block picker.

The block only appears in the picker when the Product Review app is installed AND enabled. On stores without it, the picker hides the block; if already added, the storefront falls back to an "Application not installed" notice.

## What the merchant can do here

- Toggle **Enable slider** — when ON, the reviews render as a horizontal carousel; when OFF, as a grid.
- Toggle **Show product image** — adds the reviewed product's image to each review card.
- Toggle **Show product title** — adds the reviewed product's title.
- Set **Per row** — how many review cards per row.
- Set **Limit characters** — truncates each review body to N characters (default 300).
- Pick **Show** — `all` (rating + comment), `only_rating`, or `only_comment`.
- Pick **Filter rating** — all / specific star count.
- Pick **Filter group** — `all` (all reviews), or filter by a specific review group / category / product / vendor.
- Set the section **Title** (rendered above the reviews row).
- Pick **Sort by** + **Sort direction** — by created date or rating, asc / desc.
- Set **Limit** — total reviews to show across all sources (default 12).
- Set **Per product** — when grouping by product, max reviews per product (default 3).
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot add or edit individual reviews from this block — that lives in the Product Review app's admin.
- The merchant cannot moderate / approve / reject reviews from here.
- The merchant cannot render reviews from external sources (Yotpo, Trustpilot, Google) — for those, use the relevant integration block (`yotpo-reviews`) or an embedded code block.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |
| `enable_slider` | toggle | `true` | Render as carousel vs. grid. |
| `show_product_image` | toggle | `false` | Show reviewed product image. |
| `show_product_title` | toggle | `true` | Show reviewed product title. |
| `title` | text input | `''` | Section title above the reviews row. |
| `per_row` | number | `3` | Reviews per row. |
| `show` | select | `all` | `all` / `only_rating` / `only_comment`. |
| `sort_by` | select | `created_at` | Sort field. |
| `sort_value` | select | `desc` | Sort direction. |
| `per_product` | number | `3` | Max reviews per product (when grouping by product). |
| `filter_rating` | select | `all` | Star-rating filter. |
| `filter_group` | select | `all` | Source filter (all / category / product / vendor / specific group). |
| `filter_group_value` | autocomplete | `false` | Required when `filter_group != all` — the picked category / product / vendor ID. |
| `limit` | number | `12` | Total reviews to show. |
| `limit_characters` | number | `300` | Per-review character truncation. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]]. The `saveSettings` method coerces `enabled` and `enable_slider` to `int(0|1)` and validates the filter pairing (filter_group + filter_group_value must both be set).

## Business rules

### App-gated

The block only registers when the Product Review app is BOTH installed AND enabled (the platform code). On stores without it, the block is absent from the picker, and on the storefront the legacy fallback notice "Application 'Product Review' is not installed" renders in place of the reviews row.

### `filter_group != all` requires `filter_group_value`

When the merchant picks a non-all filter group (specific category, product, or vendor) but leaves `filter_group_value` blank, `saveSettings` throws an error with the translation `module.product.showcase.err.filter_value_required`. The pairing is enforced server-side, not just client-side.

### Slider vs. grid is a runtime choice

The `enable_slider` toggle controls the layout client-side — the same review HTML renders, wrapped in either a Slick / Swiper carousel or a static grid. Switching modes does not change which reviews surface.

### `limit_characters` is per-review

The truncation applies to each review's body independently — a 300-character cap means each card shows up to 300 characters of the review text, then "..." and an optional "read more" link (verify per theme).

### `per_product` only applies when grouping

When `filter_group = product`, the block surfaces up to `per_product` reviews per featured product. When `filter_group != product`, the setting is ignored.

## Related

- [[design-modules-page-builder]] — hub.
- [[design-module-pb-request-review]] — sibling: request-review form.
- [[design-module-pb-product]] — sibling: product detail block (often paired with reviews).
- [[apps-product-review]] — Product Review app (gates this module).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Review group taxonomy.** Confirm the exact list of `filter_group` options + how each maps to a picker (verify against the Product Review app's data model).
- 📡 **Truncation UX.** When a review is truncated, is there a "read more" link or just the ellipsis? (verify per theme)
