---
type: feature
nav_path: "Settings → Store settings → Operational toggles (Order locking, Image proportions, Admin bar)"
route_name: general.settings
route_path: /admin/settings/general
aliases: ["Lock orders", "Order locking", "Lock time", "Product image proportions", "Square images", "Admin bar", "Admin overlay", "Заключване на поръчки", "Админ бар", "Пропорции на снимки"]
tags: [settings, general, order-locking, admin-bar, image-proportions, operational]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-general]]. See the hub for related aspects (store details, locale, language, maintenance, security key, product badges, industry multi-select).

# Store settings — Operational toggles (Order locking, Image proportions, Admin bar)

## Purpose

Three small operational boxes grouped together here because each is a single switch (plus, for one, a duration field) and none warrants its own aspect page:

- **Locking orders** — prevents two staff members from editing the same order simultaneously by making the order read-only for everyone except the Administrator who opened it, for a configurable number of minutes.
- **Additional settings → Image proportions** — chooses how product images are rendered (`original` vs `square`).
- **Admin bar** — an overlay banner shown to logged-in Administrators when they visit the public storefront, warning them that they're seeing a cache-bypassed view.

## Where to find it

Sidebar → Settings → **Store settings** → three separate boxes near the bottom of the page (*Locking orders*, *Additional settings*, *Admin bar*).

## What the merchant can do here

- Turn order-locking on/off and set the lock duration.
- Choose whether product images render with their original aspect ratio or are forced into a square.
- Show or hide the admin overlay bar on the storefront for logged-in Administrators.

## Settings & fields

### Box: Locking orders (`lock_orders`)

> "Lock open orders from different administrators. If one administrator opens an order, another will not be able to open it in the interval specified below. The store owner can open it before the interval expires."

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Lock orders** (`lock_orders`) | Switch — when ON, an order opened by one Moderator becomes read-only for others. | |
| **Lock time** (`lock_orders_time`) | Integer (minutes). Lock duration. | Only visible when Lock orders is ON. **Default 7 minutes** (backend fallback). Backend validation requires a positive integer (not decimal, not zero) when `lock_orders=yes`. |

### Box: Additional settings (`additional_settings`)

Header label: "Additional settings — Images".

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Select image proportion** (`product_image_type`) | `original` (keep uploaded proportions) or `square`. | Affects product image rendering across the store. |

### Box: Admin bar (`admin_bar`)

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Show admin bar** (`admin_bar`) | Switch — when ON, an administrator visiting the storefront sees an admin overlay bar. | |

## Business rules

### Order locking — Administrator can override

When `lock_orders` is ON and a Moderator opens an order, every other Moderator sees the order as read-only until `lock_orders_time` minutes have passed since the lock was acquired. The **Administrator** (store owner) is exempt — they can open and edit a locked order at any time, even before the interval expires. This is by design so the owner can never be "frozen out" by a Moderator who walked away from their desk mid-edit. See [[merchant-roles]] for the Admin / Moderator distinction.

### Lock auto-releases after the interval

The lock is implicit (no explicit "unlock" action) — once `lock_orders_time` minutes elapse since acquisition, the next admin who opens the order can edit it freely. There is no warning to the original locker that their lock expired; they may save and get a stale-state error if someone else edited in the meantime.

### Conditional field — Lock time only shows when switch is ON

The `lock_orders_time` field only renders in the UI when `lock_orders` is ON. Toggling the switch off hides the field but doesn't clear the underlying value; turning it back on restores the previous duration.

### Lock time validation

Backend requires `lock_orders_time` to be a **positive integer** when `lock_orders=yes`. Submitting a decimal, zero, or negative number returns a validation error. Frontend may not catch all invalid values — relies on backend.

### Image proportions are a global render setting

`product_image_type` applies to every product image across the storefront and admin previews. There is no per-product override — choosing `square` crops every image into a square; choosing `original` preserves uploaded aspect ratios. Merchants who switch between modes after uploading lots of product images should expect a visual change everywhere — there's no migration / re-crop step.

### Admin bar appears as a top banner on the storefront

When `admin_bar` is ON and a logged-in Administrator views the public storefront, the storefront renders a banner at the top of the page with:

- The CloudCart logo.
- A warning: *"You are logged in as an administrator and the online store may load slower due to disabled cache."*
- The Administrator's avatar and username.
- Two links: **Admin** (jump back to the admin panel) and **Logout**.

Customers never see this bar. The banner exists specifically so that an Administrator browsing their own store doesn't mistake cache-bypassed performance for the customer experience. The cache-bypass behaviour is independent of this toggle — it always happens for logged-in admins; the bar just makes it visible.

### Admin bar visibility is per-session, not per-store

The bar is only visible to the currently-logged-in admin's session. Other admins (in their own sessions) make their own visibility decision based on their own login state. Logging out makes the bar disappear immediately (because the cache-bypass criterion stops being met). Customers and anonymous visitors never see it regardless of this setting.

### No plan-gating

None of these three toggles is gated by any plan-feature.

## Related

- [[settings-general]] — hub.
- [[merchant-roles]] — Administrator vs Moderator distinction (relevant to order locking — only Administrators bypass locks).
- [[settings-staff]] — where individual Staff members and their roles are managed.
- [[orders-details]] — the per-order detail screen where the lock applies; opening an order acquires the lock.
- [[products-products]] — product editor; image proportions affect the product image previews here too.

## Open questions

- Whether `product_image_type = square` triggers any storefront cache invalidation on change, or whether the visual change is purely client-side via CSS. (verify)
- Whether the order lock acquisition is per-order or per-Moderator-session. (verify)
