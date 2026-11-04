---
type: feature
nav_path: "Marketing → Discounts → Shipping → Eligibility"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Free shipping eligibility", "Shipping discount target", "Shipping discount order_over", "Free shipping conditions", "Free shipping restrictions"]
tags: [marketing, discounts, shipping, eligibility, conditions]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (value mechanics, stacking, force-save, other zero-paths, plan gates / API, examples).

# Shipping discount — eligibility & conditions

## Purpose

This page is the catalogue of **every condition** that decides whether a Free-shipping discount fires on a cart at checkout: the discount target (`all` vs `order_over`), customer / group / region restrictions, date range, status, the `uses` counter and its counted statuses, and the UTC-based auto-disable on expiry.

If the merchant ticket is *"my free-shipping promo isn't applying on this cart"*, this is the page.

## Where to find it

All eligibility fields live on the Create / Edit form at `/admin/marketing/discounts/create/global` (or `/create/code` for the code variant). See [[marketing-discounts-shipping]] for the entry-surface flow.

## What the merchant can do here

- Pick the **target** — `all` or `order_over`.
- Set `order_over` (when target is `order_over`).
- Restrict to **Registered users only** (`only_customer`) and optionally specific customer accounts.
- Restrict to [[customers-custom-groups|customer groups]] via `customer_groups_target` + `customer_groups[]`.
- On the **Discount with promo code** form only, restrict to a [[geo-zone]] via `all_regions = no` + `geo_zone_id`.
- Set the **date range** (`date_start`, `date_end`, `no_expire`).
- Toggle `active`.
- Cap usage with `max_uses` and `maxused_user`.

## Settings & fields

### Discount target

| Value | Means | Required companion |
|---|---|---|
| `all` ("For every product in the cart") | No minimum (always-on free shipping). | — |
| `order_over` ("Orders over") | Total before shipping at or above the amount. A code also has an entry check, see below. | `order_over` (amount in store currency). |

Changing Discount type to `shipping` **forces `settings` to `all`** and hides product / category / vendor / selection options. The merchant can then switch to `order_over` if they want a threshold.

### General eligibility fields

| Field | Backend key | What it does | Validation |
|---|---|---|---|
| **Discount status** | `active` | Active = fires at checkout. Inactive = skipped. | `yes` / `no`. |
| **Discount name** | `name` | Merchant-facing label; also shown on the customer's totals row. | Required, max 191 chars. |
| **Start date** | `date_start` | When the discount becomes eligible. | Required, valid date. |
| **End date** | `date_end` | When the discount stops being eligible. NULL = no expiration. | Nullable; cannot be before the start. Today and past dates save. |
| **No expiration** | `no_expire` | UI helper — sets `date_end` to null. Without it the form asks for an end date. | — |

No-code free-shipping discounts use the **Global** form layout, so their Date range block **does** include the two storefront-timer switches — **Show timer in product listing** (`timer_list`) and **Show timer in product details page** (`timer_details`) — both disabled until an end date is set. (This is the countdown *badge*, unrelated to the Countdown discount type's per-session minute timer.)

### Customer + region + limits

| Field | Backend key | What it does |
|---|---|---|
| **Discount available only to registered users** | `only_customer` | On a code: guests are refused at entry with *"The code is valid only for registered users"*. On no-code free shipping, picking specific customers limits it. |
| **Specific customers** | `customers[]` | When `only_customer = 1` on no-code free shipping, only these accounts qualify. |
| **All groups** | `customer_groups_target` | `yes` = all groups; `no` = restrict. |
| **Customer groups** | `customer_groups[]` | Selected [[customers-custom-groups]] when restricted. |
| **Make it Global** | `all_regions` | Code form only. `yes` = all regions. |
| **Region** | `geo_zone_id` | Code form only. When `all_regions = no`, restrict to a [[geo-zone]]. |
| **Maximum total uses** | `max_uses` | Across all customers. NULL = unlimited. Integer 1-100,000. Counted only on orders reaching the **counted statuses**. |
| **Maximum uses per customer** | `maxused_user` | On a code, checked when a logged-in customer enters it. NULL = unlimited. Integer 1-100,000. |

The Registered-users block is shown only when target is `order_over`.

## Business rules

### The activation rule — when free shipping kicks in

A shipping discount applies only when **all** of:

- The cart has a non-zero shipping quote (provider selected, quote > 0). Pickup / digital-only carts silently skip the discount.
- Total before shipping (after whole-order discounts) at or above `order_over`. A discount created with target `all` has no minimum. One edited from "Orders over" to `all` keeps its old minimum and still enforces it.
- Active scope (status + date window + uses remaining) satisfied.
- Customer group and region match; if specific customers are picked, the customer is one of them.

If any fail, the discount silently doesn't apply — no customer-facing "did not qualify" error.

### Targets are limited to `all` and `order_over`

The Discount target dropdown hides the product / category / vendor / selection options when the type is Free shipping. The discount always takes the whole shipping row.

### The minimum amount: no-code at or above; a code strictly above at entry

No-code free shipping applies at or above the minimum: 50.00 qualifies on a 50 EUR minimum. It is measured on the total before shipping, after whole-order discounts, so a 60 EUR cart with 15 EUR off is 45 and does not reach a 50 EUR minimum.

A free-shipping code with a minimum is refused at the code box unless the products subtotal is strictly above the minimum. 50.00 on a 50 EUR minimum gets *"The discount could not be applied because the minimum total price of the products has not been reached."* Once accepted, shipping stays free while the total before shipping is at or above the minimum.

### `order_over` field — no maximum amount

The form takes the amount in euros, and `order_over` has no maximum.

### Counted statuses (uses counter)

The `uses` counter increments only when an order reaches a **counted status** — configured per store via `discounts_used_statuses`; defaults to `paid`, `completed`, `fulfilled`. Cancelled, voided, refunded, chargebacked, disputed, failed, or timeouted orders never burn a slot of `max_uses`. The per-customer count still includes a fulfilled order in one of those statuses.

### Auto-disable on expiry — runs in UTC, NOT store timezone

An hourly background process sets `active = no` at its first run after 00:00 **UTC** on the day after a discount's `date_end`. For a Europe/Sofia store that is about 2 to 4 hours after local midnight. For a store west of UTC it happens before the store's end date is over, so the discount stops early.

Storefront cart-engine checks DO use store timezone at evaluation time, so the customer's checkout stops applying the free shipping at local midnight on the end date — but the merchant's listing still shows the row as Active until that run.

### Date range — the end date cannot be before the start

The form refuses an end date before the start date, and asks for one unless **No expiration** is on. Today and past dates save; a discount whose end date has passed does not apply. To deactivate an in-flight discount immediately, toggle `active`; it takes effect at once.

## Related

- [[marketing-discounts-shipping]] — hub.
- [[customers-custom-groups]] — customer-group restriction.
- [[geo-zone]] — region restriction.
- [[settings-statuses]] — `discounts_used_statuses` setting.
- [[background-queue-inventory]] — hourly UTC sweep that auto-disables expired discounts.

## Open questions

None.
