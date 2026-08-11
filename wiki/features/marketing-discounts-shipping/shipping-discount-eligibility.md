---
type: feature
nav_path: "Marketing → Discounts → Shipping → Eligibility"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Free shipping eligibility", "Shipping discount target", "Shipping discount order_over", "Free shipping conditions", "Free shipping restrictions"]
tags: [marketing, discounts, shipping, eligibility, conditions]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (value mechanics, stacking, force-save, other zero-paths, plan gates / API, examples).

# Shipping discount — eligibility & conditions

## Purpose

This page is the catalogue of **every condition** that decides whether a Free-shipping discount fires on a cart at checkout: the discount target (`all` vs `order_over`), customer / group / region restrictions, date range, status, the `uses` counter and its counted statuses, and the UTC-based auto-disable on expiry.

If the merchant ticket is *"my free-shipping promo isn't applying on this cart"*, this is the page.

## Where to find it

All eligibility fields live on the Create / Edit form at `/admin/marketing-new/discounts/create/global` (or `/create/code` for the code variant). See [[marketing-discounts-shipping]] for the entry-surface flow.

## What the merchant can do here

- Pick the **target** — `all` or `order_over`.
- Set `order_over` (when target is `order_over`).
- Restrict to **Registered users only** (`only_customer`) and optionally specific customer accounts.
- Restrict to [[customers-custom-groups|customer groups]] via `customer_groups_target` + `customer_groups[]`.
- Restrict to a [[geo-zone]] via `all_regions = no` + `geo_zone_id`.
- Set the **date range** (`date_start`, `date_end`, `no_expire`).
- Toggle `active`.
- Cap usage with `max_uses` and `maxused_user`.

## Settings & fields

### Discount target

| Value | Means | Required companion |
|---|---|---|
| `all` | All carts (always-on free shipping). | — |
| `order_over` | Cart subtotal ≥ `order_over` value. | `order_over` (amount in store currency). |

Changing Discount type to `shipping` **forces `settings` to `all`** and hides product / category / vendor / selection options. The merchant can then switch to `order_over` if they want a threshold.

### General eligibility fields

| Field | Backend key | What it does | Validation |
|---|---|---|---|
| **Discount status** | `active` | Active = fires at checkout. Inactive = skipped. | `yes` / `no`. |
| **Discount name** | `name` | Merchant-facing label; also shown on the customer's totals row. | Required, max 191 chars. |
| **Start date** | `date_start` | When the discount becomes eligible. | Required, valid date. |
| **End date** | `date_end` | When the discount stops being eligible. NULL = no expiration. | Nullable; end > start; cannot be today or earlier on save. |
| **No expiration** | `no_expire` | UI helper — sets `date_end` to null. | — |

Free-shipping discounts use the **Global** form layout, so their Date range block **does** include the two storefront-timer switches — **Show timer in product listing** (`timer_list`) and **Show timer in product details page** (`timer_details`) — both disabled until an end date is set. (This is the countdown *badge*, unrelated to the Countdown discount type's per-session minute timer.)

### Customer + region + limits

| Field | Backend key | What it does |
|---|---|---|
| **Only registered users** | `only_customer` | Hidden from guest carts. |
| **Specific customers** | `customers[]` | When `only_customer = 1`, restrict further. |
| **All groups** | `customer_groups_target` | `yes` = all groups; `no` = restrict. |
| **Customer groups** | `customer_groups[]` | Selected [[customers-custom-groups]] when restricted. |
| **Make it Global** | `all_regions` | `yes` = all regions. |
| **Region** | `geo_zone_id` | When `all_regions = no`, restrict to a [[geo-zone]]. |
| **Maximum total uses** | `max_uses` | Across all customers. NULL = unlimited. Integer 1-100,000. Counted only on orders reaching the **counted statuses**. |
| **Maximum uses per customer** | `maxused_user` | Per-customer cap. NULL = unlimited. Integer 1-100,000. |

The Registered-users block is shown only when target is `order_over`.

## Business rules

### The activation rule — when free shipping kicks in

A shipping discount applies only when **all** of:

- The cart has a non-zero shipping quote (provider selected, quote > 0). Pickup / digital-only carts silently skip the discount.
- Cart subtotal (before shipping) ≥ `order_over` if target is `order_over`. For target `all`, the subtotal check is skipped.
- Active scope (status + date window + uses remaining) satisfied.
- Customer-group + region + `only_customer` restrictions match.

If any fail, the discount silently doesn't apply — no customer-facing "did not qualify" error.

### Targets are limited to `all` and `order_over`

Shipping discounts can only target the whole cart. Enforced at three layers: the Discount target dropdown hides product / category / vendor / selection options when type=shipping; the backend validator rejects `products`, `product_categories`, `vendors`, `selections` payloads with *"Type is not valid for products or product category targets"*; and the discount-lookup engine restricts shipping-typed queries to `all` / `order_over`.

### Code-based shipping uses inclusive `>=` on `order_over`; no-code uses strict `>`

Unlike Flat / Percent code-based discounts (strict `>` on `order_over`), a code-based **Free-shipping** coupon uses an **inclusive `>=` comparison** at the code-validation step. A cart subtotal **exactly equal to** the threshold qualifies — the code is accepted.

Example: a "Free shipping with code WELCOME, order_over = 50 EUR" coupon on a cart with subtotal exactly 50.00 EUR — the shipping coupon IS accepted; a comparable Percent code at the same threshold would be rejected. Merchants do NOT need to set `order_over = 49.99` to make a "50 EUR or more" promise work. The invented error message *"The cart sum is not over the discount minimum"* does not exist in the platform's translation files.

### `order_over` field — practically uncapped (currency stored in cents)

The `order_over` threshold field validates through the platform's currency-amount validator. The "max" parameter is the maximum number of CHARACTERS in the input string, NOT a numeric value cap (default 1,000,000-character ceiling). There is **no built-in numeric ceiling** on `order_over`.

The platform stores monetary values in **cents** (1 EUR = 100), so `order_over = 5000` means a 50 EUR threshold. Merchants entering very high thresholds simply see the discount never fire — there is no validation error for *"unreasonably high"*.

### Counted statuses (uses counter)

The `uses` counter increments only when an order reaches a **counted status** — configured per store via `discounts_used_statuses`; defaults to `paid`, `completed`, `fulfilled`. Cancelled, voided, refunded, chargebacked, disputed, failed, or timeouted orders never burn a slot.

### Auto-disable on expiry — runs in UTC, NOT store timezone

A daily background process toggles `active = no` on shipping discounts whose `date_end` is more than 1 day in the past in **UTC** — NOT the store's timezone. For a Europe/Sofia store, a shipping discount with `date_end = 2026-06-15` may remain technically "active" for up to ~27 hours after local end-of-day before the UTC sweep flips the flag.

Storefront cart-engine checks DO use store timezone at evaluation time, so the customer's checkout stops applying the free shipping at the expected local time — but the merchant's listing still shows the row as Active until the next UTC sweep runs.

This recurring process is part of [[background-queue-inventory]].

### Date range — end-date cannot be today or earlier on save

The form validator rejects a `date_end` of today or earlier — the merchant cannot create a pre-expired discount. To deactivate an in-flight discount immediately, toggle `active` instead (see [[shipping-discount-plan-gates-api]] for the 10-minute cooldown).

## Related

- [[marketing-discounts-shipping]] — hub.
- [[customers-custom-groups]] — customer-group restriction.
- [[geo-zone]] — region restriction.
- [[settings-statuses]] — `discounts_used_statuses` setting.
- [[background-queue-inventory]] — daily UTC sweep that auto-disables expired shipping discounts.

## Open questions

None.
