---
type: feature
nav_path: "Marketing → Discounts → Flat → Eligibility"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Flat discount eligibility", "Flat discount date range", "Flat customer groups", "Flat geo zone", "Flat only_customer", "Flat max_uses", "Flat maxused_user", "discounts_used_statuses", "Flat auto-disable UTC", "Flat activation cooldown", "Flat plan gates", "discount_global", "discount_coupon"]
tags: [marketing, discounts, flat, eligibility, plan-gates, cooldown]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-discounts-flat]]. See the hub for the other aspects (form entry, targeting, value mechanics, stacking, programmatic access).

# Flat discount — eligibility

## Purpose

Documents **when a Flat discount qualifies to fire on a cart** — date window, customer-group / region / registered-user restrictions, the uses counter + counted statuses, plan-feature quotas, the daily UTC auto-disable sweep, and the 10-minute cooldown.

Tickets that land here: *"why did my Flat discount stay active past its end date"*, *"why does it work for some customers but not others"*, *"I deactivated and got an error re-activating"*, *"the create page says 'Not supported by plan'".*

## Where to find it

Eligibility spans several blocks on the create / edit page (see [[flat-discount-form-entry]]):

- **Customer groups** — `customer_groups_target` + `customer_groups[]`.
- **Registered users only** (shown only for `order_over`) — `only_customer`. That target also unlocks `force_save` (see [[flat-discount-targeting]]).
- **Discount limits** (shown only for `all` / `order_over`) — `max_uses` + `maxused_user`.
- **Region (Geo zone)** (code variant only) — `geo_zone_id` + `all_regions`.
- **Date range** — `date_start` + `date_end` + `no_expire`.

## What the merchant can do here

- Restrict to specific **customer groups** (or "All groups"), specific **customers** (`customers[]`), or **registered users only** (target = `order_over`).
- Set a **total uses cap** (`max_uses`) and **per-customer cap** (`maxused_user`).
- Restrict to a **region** via `geo_zone_id` (or "Make it Global").
- Set a **date range** (with or without expiration).

### What the merchant CANNOT do here

- Reactivate within 10 minutes of the previous toggle — see *Activation cooldown*.
- Create one when the `discount_global` (no-code) or `discount_coupon` (code) quota is exhausted — see *Plan-gating*.
- Save a `max_uses` / `maxused_user` above 100,000 — see *Discount limits*.

## Settings & fields

### Customer groups & registered users

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **All groups** | `customer_groups_target` | When ON, applies to every [[customers-custom-groups|customer group]]. | `yes` / `no`. |
| **Customer groups** | `customer_groups[]` | List of group IDs (when target = `no`). | Array. |
| **Discount available only to registered users** | `only_customer` | Guests cannot apply. | 1 / 0. Only shown for `order_over`. |
| **Customers** | `customers[]` | Specific customer IDs that may use it. | Array of IDs. |

### Discount limits

| Field | Backend key | What it does | Validation |
|-------|-------------|--------------|------------|
| **Global discount limit** | `max_uses` | Total uses across all customers. NULL = unlimited. | Integer 1-100,000. *"Maximum usage can be up to 100000"*. Only shown for `all` / `order_over`. |
| **Discount limit for customer** | `maxused_user` | Per-customer cap. NULL = unlimited. | Integer 1-100,000. |
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
| **End date** | `date_end` | Last day; skipped after it. | Nullable. Must be after start; cannot be today or earlier on save. |
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

A daily background process toggles `active = no` on Flat discounts whose `date_end` is **at least 1 day in the past in UTC** — NOT store timezone.

Example: for Europe/Sofia (UTC+2 / UTC+3 DST), a discount with `date_end = 2026-06-15` is not auto-disabled until the job runs after 2026-06-16 23:59 UTC — it can stay technically "active" up to ~27 hours past local end-of-day.

Storefront cart-engine checks DO use store timezone for the `date_end >= today` gate, so customer-visible behaviour stops on the expected local date — but the `active = yes` flag and "Active" listing label persist until the UTC sweep.

This is the *"Expired-discounts de-activation"* process in [[background-queue-inventory]] (runs hourly).

### Activation cooldown (10 minutes — applies to Flat)

Toggling a Flat discount's active status is rate-limited to **once per 10 minutes per discount**. Within the window the response is:

> *"You've already activated this discount. Please wait:minutes minutes in order to be able to deactivate it again."*

It exists because every active-toggle regenerates per-product attachment records (which feed the storefront's *"from X / now Y"* display); the throttle stops high-catalog stores thrashing the background queue.

It is enforced per-discount, not per-store — different discounts can toggle in quick succession, just not the same one — and is bypassed in development / command-line contexts.

**Scope:** no-code Flat / Percent / Shipping / Fixed only. Code-based variants, Container codes, Quantity, Countdown, and Code PRO have NO cooldown — see the per-type cooldown table on [[discount-stacking]].

### Uses counter — counted statuses

The `uses` counter increments ONLY when an order reaches a **counted status** — configurable per store via the `discounts_used_statuses` setting on [[settings-statuses]]; defaults to **`paid`, `completed`, `fulfilled`**.

This governs both `max_uses` and `maxused_user`. Carts that never check out, and orders that move to cancelled / refunded, do NOT consume a use.

### Plan-gating — counters and what the merchant sees

- **Without a code** → counts toward the **`discount_global`** quota (shared with no-code Percent and no-code Shipping).
- **With a code** → counts toward the **`discount_coupon`** quota (shared with all code-based variants).

Both quotas are also enforced on JSON-API v2 / GraphQL writes — see [[flat-discount-programmatic-access]].

At the limit for either quota, the create attempt returns **HTTP 403 Forbidden** with the message *"Not supported by plan"* plus a list of plans with more capacity. (403, not 402 — older wiki phrasing said 402; corrected.)

Because of a key-naming mismatch in the plan-feature catalogue, the 403 gate can silently pass for some store configurations; the reliable enforcement is the listing UI's *"X / N used"* counter. Watch that rather than expecting a 403 on every overflow. (verify)

### Per-customer cap auto-clears the code

Hitting the `maxused_user` cap removes the code from the cart entirely, not just blocks it — the customer needs a different code. See [[flat-discount-value-mechanics]] for the rejection model.

### Customer-group restriction at code validation

For code-based Flat discounts, group membership is checked at code-validation time. A guest redeeming a code restricted to a group is rejected.

A guest can still redeem a code with `customer_groups_target = yes` (all groups) provided `only_customer = 0`. When `only_customer = 1`, guests are blocked regardless of group settings.

## Related

- [[marketing-discounts-flat]] — hub.
- [[customers-custom-groups]] — customer-group restriction via `customer_groups[]`.
- [[geo-zone]] — region restriction via `geo_zone_id`.
- [[settings-statuses]] — `discounts_used_statuses` controls which statuses count toward the uses counter.
- [[background-queue-inventory]] — *"Expired-discounts de-activation"* recurring process.
- [[discount-stacking]] — per-type cooldown table (10 minutes for no-code Flat).

## Open questions

- Plan-feature key-naming mismatch (`discount-global` vs `discount_global`): which exact path silently passes — see *Plan-gating* `(verify)`.
