---
type: feature
nav_path: "Products → Banners Labels → Scheduling & status"
route_name: product-banners.list
route_path: /admin/products/banners-labels
aliases: ["Banner scheduling", "Label scheduling", "Active from active to", "Banner expiry", "Auto-disable banner", "Banner status", "Banner permissions", "Plan gate products_banners", "График на банер", "Активен от до"]
tags: [marketing, products, banners-labels]
plan_gates: [products_banners]
created: 2026-06-10
updated: 2026-06-10
source_count: 10
---

> Part of [[products-banners-labels]]. See the hub for the other aspects (fields & forms, targeting / auto-population).

# Banners & Labels — scheduling & lifecycle

## Purpose

What controls **when** a banner / label is visible on the storefront, what happens when it expires, and the plan / permission gates around the feature. This aspect covers the storefront visibility scope (`status` + `active_from` + `active_to`), the daily auto-disable job, the `products_banners` plan gate, staff permissions, and delete cleanup. (For the appearance fields, see [[products-banners-labels-fields]]; for who it attaches to, see [[products-banners-labels-targeting]].)

## Where to find it

Sidebar → Products → **Banners Labels**. On the list view each row shows **Active from**, **Active to**, a **Products** count, and a **Status** toggle. The list filters by Active-from / Active-to dates (exactly / before / after / between), Status, and Has-products. Bulk actions: set status Active, set status Inactive, Delete.

## What the merchant can do here

- Toggle a banner / label **Active / Inactive** per row (PATCH `status`).
- Set an **Active from** start date and an **Active to** end date in the edit form.
- Bulk-activate, bulk-deactivate, or bulk-delete.
- Re-use an expired badge by editing its `active_to` to a future date and re-toggling Active.

The merchant CANNOT schedule different badges for different **times of day** — only date-range scheduling (date-only granularity).

## Settings & fields

| Field | Effect on visibility |
|-------|----------------------|
| `status` | `1` = candidate to show; `0` = never shown. |
| `active_from` | NULL or ≤ today → eligible; future date → hidden until then. |
| `active_to` | NULL or ≥ today → eligible; past date → hidden (and auto-disabled). |

All date comparisons are **date-only** and evaluated in the **store's timezone**.

## Business rules

### Storefront visibility scope: status + active_from + active_to

A banner / label renders on the storefront only when **ALL** of these are true:

- `status = 1` (Active toggle on).
- `active_from` is NULL **OR** ≤ today (store timezone).
- `active_to` is NULL **OR** ≥ today (store timezone).

Because the comparison uses the **store's timezone**, a UK store at 23:00 BST treats "today" differently from a US store. Time-of-day does not matter — only the date.

This scope is applied **on top of** the matched product set from [[products-banners-labels-targeting]]: a product can match a banner's conditions yet show no badge because the banner is outside its active window or toggled off.

### Auto-disable runs daily, ~6 hours after expiry

A scheduled job runs **daily at 02:00 UTC**:

- It finds every active banner / label whose `active_to` is more than **6 hours** in the past.
- Sets `status = 0` (inactive).

So after a badge expires it stays in the catalog but auto-deactivates the next morning — the merchant doesn't have to remember to turn it off. To reuse it, edit `active_to` to a future date and re-toggle Active.

### Plan feature: `products_banners`

Creating a **new banner** is gated by the plan feature `products_banners`, mapped to a feature-usage check on the create route. Plans without the feature get a paywall on the create button. Labels do not carry the same plan gate in the same way — they may be available on lower tiers. `(verify)`

### Permissions

The banners sidebar entry requires both `products` **AND** `products.banners` staff permissions. Labels require `products` **AND** `products.labels`. Moderators without these sections can't see or edit the page.

### Delete: deactivate and clean up

Deleting a banner / label removes the definition row **plus** all `products_banners_to_products` / `products_labels_to_products` junction rows. The storefront stops showing the badge on the next page load.

## Related

- [[products-banners-labels]] — hub.
- [[products-banners-labels-fields]] — where `status` / `active_from` / `active_to` are entered + date validation.
- [[products-banners-labels-targeting]] — the matched product set this visibility scope is applied on top of.
- [[products-products]] — products whose cards display (or stop displaying) the badge.
- [[product]] — entity page.

## Open questions

- How does the storefront handle two badges scheduled onto the same position simultaneously? Stacking order is theme-dependent. `(verify)`
