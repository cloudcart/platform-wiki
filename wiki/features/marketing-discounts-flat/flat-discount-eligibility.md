---
type: feature
nav_path: "Marketing → Discounts → Flat → Eligibility"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Flat discount eligibility", "Flat discount date range", "Flat customer groups", "Flat geo zone", "Flat only_customer", "Flat max_uses", "Flat maxused_user", "discounts_used_statuses", "Flat auto-disable UTC", "Flat plan gates", "discount_global", "discount_coupon"]
tags: [marketing, discounts, flat, eligibility, plan-gates]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, targeting, value mechanics, stacking, programmatic access).

# Flat discount — eligibility

## Purpose

Documents **when a Flat discount qualifies to fire on a cart** — date window, customer-group / region / registered-user restrictions, the uses counter + counted statuses, plan checks, and the hourly UTC auto-disable sweep.

Tickets that land here: *"why did my Flat discount stay active past its end date"*, *"why does it work for some customers but not others"*, *"the create page says this feature is not enabled for my plan"*.

## Where to find it

Eligibility spans several blocks on the create / edit page (see [[flat-discount-form-entry]]):

- **Customer groups** — `customer_groups_target` + `customer_groups[]`.
- **Registered users only** (shown only for `order_over`) — `only_customer`. That target also unlocks `force_save` (see [[flat-discount-targeting]]).
- **Discount limits** (no-code form: shown only for `all` / `order_over`; code form: every target) — `max_uses` + `maxused_user`.
- **Region (Geo zone)** (code variant only) — `geo_zone_id` + `all_regions`.
- **Date range** — `date_start` + `date_end` + `no_expire`.

## What the merchant can do here

- Restrict to specific **customer groups** (or "All groups"), or **registered users only** (target = `order_over`), and within that specific **customers** (`customers[]`).
- Set a **total uses cap** (`max_uses`) and **per-customer cap** (`maxused_user`).
- Restrict to a **region** via `geo_zone_id` (or "Make it Global").
- Set a **date range** (with or without expiration).

### What the merchant CANNOT do here

- Create one in the admin when that kind is not enabled on the plan, or through JSON-API v2 when the `discount_global` (no-code) or `discount_coupon` (code) quota is used up — see *Plan-gating*.
- Save a `max_uses` / `maxused_user` above 100,000 — see *Discount limits*.

## Settings & fields

### Customer groups & registered users

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **All groups** | `customer_groups_target` | When ON, applies to every [[customers-custom-groups|customer group]]. | `yes` / `no`. |
| **Customer groups** | `customer_groups[]` | List of group IDs (when target = `no`). | Array. |
| **Discount available only to registered users** | `only_customer` | Guests cannot apply. | 1 / 0. Only shown for `order_over`. |
| **Customers** | `customers[]` | Specific customers who may get a no-code `order_over` discount. | Array of IDs. Shown when `only_customer` is on. |

### Discount limits

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Global discount limit** | `max_uses` | Total uses across all customers. NULL = unlimited. | Integer up to 100,000. *"Max uses must be less than 100000"*. No-code form: shown only for `all` / `order_over`; code form: every target. |
| **Discount limit for customer** | `maxused_user` | Per-customer cap for logged-in customers, on codes at entry and on no-code `order_over`. NULL = unlimited. | Integer up to 100,000. *"Max used user must be less than 100000"*. |
| **Unlimited** | (toggle) | Sets the limit to NULL. | — |

### Region (code variant only)

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Region (Geo zone)** | `geo_zone_id` | Restrict to a specific [[geo-zone]]. | Nullable. |
| **Make it Global** | `all_regions` | When ON, no region restriction. | `yes` / `no`. |

### Date range

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Start date** | `date_start` | First day the discount applies. | Required. |
| **End date** | `date_end` | Last day; skipped after it. | Asked for unless **No expiration** is on (*"The end date is required"*). The form refuses only an end date before the start (*"The end date must be after the start date"*). Today and past dates save. |
| **No expiration** | `no_expire` | When ON, sets `date_end` to null. | — |

## Business rules

### Active = within date window + uses remaining

Evaluated at checkout only when ALL of:

- `active = yes`.
- `date_start <= today` (store timezone).
- `date_end IS NULL OR date_end >= today`.
- `max_uses IS NULL OR max_uses > uses`.
- For code-based: customer in `customer_groups[]` (or empty) AND shipping address in `geo_zone_id` (or `all_regions = yes`) AND code used fewer than `maxused_user` times.

The `code_apply` stacking gate runs AFTER these — see [[flat-discount-stacking]].

### Auto-disable on expiry — runs in UTC, NOT store timezone

An hourly background process toggles `active = no` on Flat discounts at its first run after **00:00 UTC on the day after `date_end`** — NOT store timezone.

Example: for Europe/Sofia (UTC+2 / UTC+3 DST), a discount with `date_end = 2026-06-15` is auto-disabled at the first run after 00:00 UTC on 2026-06-16, a few hours past local end-of-day. West of UTC the sweep can run before the local last day ends.

Storefront cart-engine checks DO use store timezone for the `date_end >= today` gate, so customer-visible behaviour stops on the expected local date — but the `active = yes` flag and "Active" listing label persist until the UTC sweep.

This is the *"Expired-discounts de-activation"* process in [[background-queue-inventory]] (runs hourly).

### Uses counter — counted statuses

The `uses` figure is recounted from orders in a **counted status** — configurable per store via the `discounts_used_statuses` setting on [[settings-statuses]]; defaults to **`paid`, `completed`, `fulfilled`**.

This governs both `max_uses` and `maxused_user`. Carts that never check out do NOT consume a use. The `uses` recount leaves out orders in a negative status such as `cancelled` or `refunded`, even when fulfilled, so it can go back down; the per-customer count does not leave out a fulfilled one.

### Plan-gating — what each path checks

- **Admin form** — on create only, checks whether that kind is enabled on the plan (`discount-global` without a code, `discount-code` with one). If not, HTTP 403 with *"This feature is not enabled for your plan. To access it, please upgrade your plan."* There is no numeric limit on this path.
- **JSON-API v2** — on create only, compares usage with `discount_global` (no code) or `discount_coupon` (code) and returns **HTTP 402 Payment Required** at the limit.
- **GraphQL `createDiscount`** — does not check these quotas for a Flat discount.

`discount_global` is shared with no-code Percent and no-code Shipping. `discount_coupon` counts only discounts holding their own code. Usage counts discounts whether active or not; only deleting lowers it.

### Per-customer cap auto-clears the code

A logged-in customer over the `maxused_user` cap sees *"You have used this discount code the maximum number of times"* and the code is cleared from the cart — they need a different code. See [[flat-discount-value-mechanics]].

### Customer-group restriction at code validation

For code-based Flat discounts, group membership is checked at code-validation time. A guest is rejected unless the guests group is among the allowed groups.

A guest can still redeem a code with `customer_groups_target = yes` (all groups) provided `only_customer = 0`. When `only_customer = 1`, guests are blocked regardless of group settings.

## Related

- [[marketing-discounts-flat]] — hub.
- [[customers-custom-groups]] — customer-group restriction via `customer_groups[]`.
- [[geo-zone]] — region restriction via `geo_zone_id`.
- [[settings-statuses]] — `discounts_used_statuses` controls which statuses count toward the uses counter.
- [[background-queue-inventory]] — *"Expired-discounts de-activation"* recurring process.
- [[discount-stacking]] — cross-discount rules for all discount types.

## Open questions

None.
