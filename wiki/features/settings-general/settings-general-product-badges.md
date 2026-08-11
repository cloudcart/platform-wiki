---
type: feature
nav_path: "Settings → Store settings → Product settings"
route_name: general.settings
route_path: /admin/settings/general
aliases: ["New product badge", "Recommended product badge", "Featured product badge", "Auto-remove badge", "Product label expiry", "Етикет нов продукт", "Етикет препоръчан продукт"]
tags: [settings, general, products, badges, scheduled-jobs, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-general]]. See the hub for related aspects (store details, locale, language, maintenance, security key, operational toggles, industry multi-select).

# Store settings — Product settings (badge auto-expiry)

## Purpose

The Product settings box controls how the storefront's *"New Product"* and *"Recommended product"* badges expire automatically. Two switches, two day-count inputs. When enabled, a background sweep checks every 4 hours which products have aged past their configured day limit and flips off their `new` or `featured` flag — the badge disappears from the storefront on next page render.

This is a **scheduled-job** feature: the badge does NOT disappear instantly when the day-count expires; it disappears within up to 4 hours of expiry. Merchants who report *"my product still shows 'New' but it's been 31 days"* are asking about this latency.

> The right-side info panel reads: *"When you add products, they will automatically be marked as New Products for a certain interval of days. Automatically remove the label Recommended product after a selected time interval."*

Header label: "Product settings and Order processing".

## Where to find it

Sidebar → Settings → **Store settings** → Product settings box.

## What the merchant can do here

- Toggle whether new products are automatically marked with a *"New"* badge.
- Set how many days the *"New"* badge stays visible.
- Toggle whether the *"Recommended product"* (Featured) badge is automatically removed after a configured interval.
- Set how many days the *"Recommended"* badge stays visible.

## Settings & fields

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Automatic marking as "New Product"** (`new_products_mark`) | Switch — when ON, newly added products get a "New" badge for N days. | When OFF, no automatic marking happens and the sweep below is skipped. |
| **Remove the "New Product" label after** (`new_products_mark_time`) | Integer (days). | Only visible when the switch above is ON. |
| **Automatic label removal "Recommended product"** (`remove_feature_products`) | Switch — when ON, the "Recommended" badge is automatically removed after N days. | When OFF, the merchant must manually un-feature products to remove the badge. |
| **Remove the "Recommended product" label after** (`remove_feature_products_time`) | Integer (days). | Only visible when the switch above is ON. |

## Business rules

### "New product" / "Recommended product" badges expire on a 4-hour background sweep

Two scheduled jobs power the auto-expiry of these storefront badges. Both run every **4 hours** (interval 14 400 s) on the `system1` queue:

- **New-product sweep** — when `new_products_mark = yes`, finds products whose `new` flag is `1` AND whose `created_at` is older than `new_products_mark_time` days, then flips `new = 0`. The storefront's "New" badge disappears on the next page render.
- **Recommended-product sweep** — when `remove_feature_products = yes`, finds products whose `featured` flag is `1` AND whose `featured_at` is older than `remove_feature_products_time` days, then flips `featured = 0`. The "Recommended" badge disappears.

Both jobs are **skipped for plan-expired stores**.

**Practical merchant impact:** after a badge's day-count expires, it can take **up to 4 hours** of latency before it disappears from the storefront — not instantaneous. Merchants who want a badge removed sooner can edit the product manually and untick the New / Featured flag on the product editor (see [[products-products]]) — that change is immediate.

### Switch OFF disables the sweep entirely for that badge

When `new_products_mark = no`, the New-product sweep is skipped completely on its 4-hourly run — products keep their existing `new` flag indefinitely. Same for `remove_feature_products = no` and the Featured flag. Turning the switch from ON to OFF does NOT retroactively reset already-flipped flags; it just stops future flips.

### Conditional fields depend on switches

The "remove after N days" inputs only show when their parent switch is ON. Toggling the switch from ON to OFF hides the day-count input but does NOT clear the underlying value — turning it back ON restores the previous number.

### Defaults are deterministic on fresh stores

A fresh store starts with `new_products_mark = no` and `remove_feature_products = no` — meaning automatic badge removal is OFF until the merchant explicitly enables it. The day-count inputs have neutral defaults (verify the exact default — typically 30 / 14 days).

### Badge state is per-product, not per-Variant

The `new` and `featured` flags live on the Product record. Switching them ON/OFF affects every Variant under the product — there is no per-Variant "New" badge. See [[variants-model]] for the structural picture.

### The "New" flag is initialised on product creation

When a new product is created (manually or via import), the platform sets `new = 1` automatically — even when `new_products_mark = no`. The merchant can untick it on the product editor at any time. So a freshly created product has the *"New"* badge regardless of this setting; the setting only controls **expiry**, not initial marking.

### The "Featured" flag is NOT auto-set — only auto-cleared

Unlike `new`, the `featured` flag must be turned ON manually by the merchant on the product editor (or via bulk action / CSV import). This setting only controls the **automatic removal** side. So turning ON `remove_feature_products` doesn't suddenly make products "Recommended" — it just makes any product the merchant featured age out after N days.

### Storefront cache invalidation

When the background sweep flips a product's flag, the same downstream side-effects fire as for any product save — the storefront cache for that product is flushed, the search index re-indexes, the `product.updated` webhook fires. So a busy store could see a small spike in webhook traffic every 4 hours when the sweeps run. See [[settings-hooks]] for webhook details.

## Related

- [[settings-general]] — hub.
- [[products-products]] — product editor; the per-product `new` and `featured` flags live here and can be toggled manually.
- [[settings-hooks]] — `product.updated` webhook fires when the sweep flips a flag.
- [[background-queue-inventory]] — context on how scheduled jobs and the `system1` queue work.

## Open questions

- Default day-count values on a fresh store (`new_products_mark_time`, `remove_feature_products_time`) — confirm. (verify)
- Whether bulk-import sets `featured_at` correctly so the sweep can age-out imported featured products. (verify)
