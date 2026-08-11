---
type: feature
nav_path: "Design → Modules → Engagement → Product reviews (product_review)"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/{product_review_instance}
aliases: ["Product review module", "product_review module", "Reviews showcase module", "Review carousel module", "Модул ревюта на продукти"]
tags: [design, modules, engagement, product-review, reviews, page-builder]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Engagement module — product_review (Reviews showcase)

> Part of [[design-modules-engagement]]. See the category page for the other engagement modules.

## Purpose

`product_review` is the **page-builder block** that displays a row (or carousel) of **collected product reviews** as social proof. Merchants use it on landing pages, homepages built as Dynamic pages, and category-promo landing pages to surface ratings + comments collected via the [[apps-product-review]] app. Settings control the row's filters (rating threshold, product source), sort order, layout (per-row count, slider vs grid), and which review-card elements render (stars, comment, product image, product title).

The block requires the **Product Review** app ([[apps-product-review]]) to be installed and enabled — without it, the edit panel shows *"Application 'Product Review' is not installed"* and nothing renders on the storefront (see Business rules).

## Where to find it

This is a **page-builder block** — it appears in the **Add module** picker when the merchant is editing a **Dynamic** page in [[marketing-landing-pages]]. After drop, clicking the block opens its settings panel with the fields below.

The block does NOT appear on the **Design → Modules** tab list directly; it is only added via page-builder drag-and-drop.

## What the merchant can do here

- Set the **title** above the row and choose **carousel** vs static grid (`enable_slider`).
- Control the card contents: stars + comment / stars only / comment only (`show`), plus the reviewed product's **title** (`show_product_title`) and **thumbnail** (`show_product_image`), and a comment-length cap (`limit_characters`).
- Choose how many reviews appear per row, 1–3 (`per_row`).
- **Sort** by newest (`created_at`) or highest rating, ascending or descending (`sort_by` / `sort_value`).
- **Filter** by minimum rating (`filter_rating`) and by product group (`filter_group` + `filter_group_value`).
- **Cap** reviews per product (`per_product`, keeps the row diverse) and the total fetched (`limit`).

See the field table below for defaults and validation.

## Settings & fields

| Field | Type | Validation | Default | What it controls |
|-------|------|------------|---------|------------------|
| `enabled` | toggle | (bool) | `true` | Master on/off |
| `enable_slider` | toggle | (bool) | `true` | Carousel vs static grid |
| `title` | text | `char:0,100` | empty | Section title shown above the row |
| `show_product_image` | toggle | `bool` | `false` | Show the reviewed product's thumbnail on each card |
| `show_product_title` | toggle | `bool` | `true` | Show the reviewed product's name on each card |
| `per_row` | number | `int:1,3` | `3` | Reviews per row (1 / 2 / 3 supported by the template) |
| `show` | select | `in:all,only_rating,only_comment` | `all` | What to render in each card |
| `sort_by` | select | `in:created_at,rating` | `created_at` | Sort field |
| `sort_value` | select | (free-form) | `desc` | Sort direction — `asc` / `desc` |
| `per_product` | number | (free-form) | `3` | Maximum reviews shown per product (de-dupes when the same product has many reviews) |
| `filter_rating` | select | `in:all,1,2,3,4` | `all` | Show only reviews with at least this rating |
| `filter_group` | select | `in:all,category,vendor,product,selection` | `all` | Limit to reviews of products in this group |
| `filter_group_value` | autocomplete | (validated per group) | empty | The actual categories / vendors / products / selection chosen — shown only when `filter_group` is set |
| `limit` | number | `int:1,100` | `12` | Maximum total reviews to fetch |
| `limit_characters` | number | (free-form) | `300` | Truncate the review comment to this many characters (with "...") |

When the merchant changes `filter_group`, the panel surfaces `filter_group_value` as a picker for the chosen kind (categories / vendors / products / smart-collection selection IDs).

**Validation on save:**

- When `filter_group` is not `all` AND `filter_group_value` is empty → error *"Filter value is required"*.
- When `filter_group` is `category` / `vendor` / `product` / `selection`, the picked items are re-checked on save — if any were deleted in the meantime the save fails with a specific message (*"One or more categories no longer exist"*, etc.) and the merchant must re-pick.

## Business rules

### Product Review app gate

The block requires the **Product Review** app ([[apps-product-review]]) to be both **installed and enabled**. Disabling the app (without uninstalling) is enough to hide the block from the page-builder picker AND to hide already-placed instances on the storefront. The block's saved settings survive — re-enabling the app restores everything. The block works across any theme that supports the page-builder; the visual treatment (border, shadow, fonts, stars) follows the active theme.

### `filter_rating` semantics

The values are `all`, `1`, `2`, `3`, `4` (no `5`). The number is a **minimum** — `filter_rating=4` means "rating >= 4". There is no way to show only 5-star reviews; `4` is the closest threshold.

### `per_product` de-duplication

When sorting by `rating desc`, a single popular product with many 5-star reviews could dominate the row. `per_product` caps the per-product appearance so the row stays diverse. The default `3` allows up to 3 reviews per product before de-duping.

### `limit_characters` truncation

Cards normalise visually by truncating the review comment to `limit_characters` (default 300) characters with an ellipsis. The reviewer's name, date, and product link are always shown in full — only the comment body is clipped.

### `show` modes

- `all` — stars + comment + product link + reviewer name + date.
- `only_rating` — stars + product link + reviewer name + date (no comment).
- `only_comment` — comment + product link + reviewer name + date (no stars).

The product image and product title toggles work alongside `show` — meaning a `show = only_rating` row CAN still show the product thumbnail if `show_product_image = true`.

### Deleted filter targets are not auto-cleaned

When the merchant picks specific products / categories / vendors for `filter_group`, deleting one of those later does NOT auto-clean the block. The next save fails with *"One or more products no longer exist"* (or the matching message) and the merchant has to re-pick.

### Empty result

When no reviews match the filters, the block still renders the title with an empty row — there is no "no reviews found" fallback message. Loosen `filter_rating` / `filter_group` or lower `per_product` if a showcase looks blank.

### `per_row` cap

`per_row` only supports 1, 2, or 3 reviews per row — wider rows are not available. Use a carousel (`enable_slider`) when more reviews need to fit.

### Source data and filter order

Only **enabled** reviews collected through the Product Review app are eligible. The filters apply in order: minimum `filter_rating`, then `filter_group`, then the `per_product` cap, then the chosen sort, then the overall `limit`.

### Reset behaviour

Reset clears all settings to defaults: `enabled=true`, `enable_slider=true`, `title=''`, `per_row=3`, `show=all`, `sort_by=created_at`, `sort_value=desc`, `per_product=3`, `filter_rating=all`, `filter_group=all`, `limit=12`, `limit_characters=300`.

## Related

- [[design-modules-engagement]] — hub.
- [[apps-product-review]] — installs the Product Review app; provides the review data this module displays.
- [[design-module-request-review]] — sibling; the CTA block asking shoppers to submit reviews.
- [[marketing-landing-pages]] — Dynamic pages use the page-builder, which exposes this block.
- [[design-themes]] — theme provides the visual styling.
- [[marketing-campaigns]] — pair `product_review` blocks with post-purchase email campaigns to drive traffic to review showcases.

## Open questions

- 📡 **5-star filter.** `filter_rating` offers `all,1,2,3,4` only. (verify) whether a dedicated `5` value is planned.
- ⏸️ **`per_row > 3`.** Only 1 / 2 / 3 are supported. (verify) whether wider rows are planned.
- ⏸️ **`filter_group = tags`.** A tags filter is not selectable in the dropdown today. (verify) whether tags filtering is a planned future option.
