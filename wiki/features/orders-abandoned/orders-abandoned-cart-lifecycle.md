---
type: feature
nav_path: "Orders → Abandoned → Cart lifecycle"
route_name: (settings — abandoned_remainder_interval) + (scheduled — clear_all_old_carts hourly)
route_path: /admin/settings/cart
aliases: ["Abandoned threshold", "Abandoned cart inactivity window", "abandoned_remainder_interval", "Abandoned cart lifetime", "Sent carts persistence", "Cart cleanup", "cart.lifetime", "Изтичане на изоставени колички"]
tags: [orders, abandoned, cart-lifecycle, cleanup, threshold]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-abandoned]]. See the hub for the other aspects (list view, detail view, eligibility, restore link, auto-recovery, plan gates).

# Abandoned carts — Cart lifecycle

## Purpose

Documents the **timing rules** that decide when a cart becomes "abandoned", when sent carts disappear from the list, and how the underlying cart records eventually age out. Three rules sit at the heart of this:

- **`abandoned_remainder_interval`** (default 60 minutes) — inactivity threshold before a cart qualifies.
- **30-minute floor clamp** — values below 30 minutes silently fall back to 60 in some matching contexts.
- **`cart.lifetime`** (default 7 days) — the hourly `clear_all_old_carts` cleanup soft-deletes any cart untouched for longer than this.

These rules are the reason the abandoned-cart list churns: yesterday's untouched carts age out within a week, even without action.

## Where to find it

The settings live on store settings (sidebar → Settings → Cart). The cleanup is a background job — catalogued in [[background-queue-inventory]].

## What the merchant can do here

- Set `abandoned_remainder_interval` to override the 60-minute default (subject to the 30-minute floor — see below).
- Delete sent / unsent carts manually from [[orders-abandoned-list-view]] (the only way to clear them before the 7-day age-out).
- Adjust `cart.lifetime` is NOT a merchant-facing setting in normal stores — it's a platform-level configuration.

## Settings & fields

| Setting | Default | Where | Notes |
|---|---|---|---|
| `abandoned_remainder_interval` | `60` minutes | [[settings-cart]] | Inactivity threshold before a cart appears in the abandoned list. Has an effective floor of 30 minutes — see clamp rule below. |
| `abandoned_remainder` | `no` (?)`(verify)` | [[settings-cart]] | Master switch for the auto-recovery job. Off by default. See [[orders-abandoned-auto-recovery]]. |
| `cart.lifetime` | `7` days | Platform config | Maximum cart-record lifetime. Cleanup runs hourly. |

## Business rules

### Default threshold — 60 minutes

The `abandoned_remainder_interval` setting defaults to **60 minutes**. A cart needs to sit untouched for that long before it appears in [[orders-abandoned-list-view]]. Stores can override this (lower the threshold to catch shorter abandonment windows, or raise it to avoid noise).

### Minimum threshold clamped to 30 minutes

The `abandoned_remainder_interval` setting is read with a floor — values below 30 minutes silently fall back to the default 60-minute window in some segment-matching contexts. **Setting 15 minutes won't actually catch carts 15 minutes after their last update everywhere** — the merchant should treat 30 minutes as the practical minimum if they want consistent behaviour across the list + auto-job + analytics surfaces.

The floor is not exposed in the settings UI — there is no validation error or warning when the merchant configures a sub-30-minute value. The behaviour just diverges silently from expectations.

### Underlying cart auto-deletes after 7 days inactivity

A separate cleanup job (`clear_all_old_carts`, runs hourly) soft-deletes ANY cart whose `updated_at` is older than `cart.lifetime = 7 days`. So abandoned carts naturally age out of the list after a week of customer inactivity — even if the merchant never deletes them and the underlying customer never converts.

This is **why the merchant sees abandoned-list churn**: yesterday's untouched carts are gone by next week, even without action. Support agents who get a "where did my abandoned carts go" ticket should first check whether the missing carts are older than 7 days — if so, the hourly cleanup is the answer.

### No automatic deletion of SENT carts — they stay until the 7-day age-out

Sent abandoned carts (with a non-NULL `date_sent`) REMAIN in the list, with the timestamp visible in [[orders-abandoned-detail-view]]. There is **no scheduled cleanup task specific to sent carts** — they persist indefinitely until:

- The merchant uses bulk Delete from [[orders-abandoned-list-view]].
- The customer eventually converts (the cart is referenced by an order — silently deleted on next Send attempt via the eligibility check).
- The underlying cart's `updated_at` ages past `cart.lifetime = 7 days` and `clear_all_old_carts` soft-deletes it.

The merchant should expect the sent-cart subset of the list to grow continuously until one of those three things happens.

### The threshold + cleanup interact

The merchant who configures `abandoned_remainder_interval = 120` (2 hours) and never bulk-deletes will see:

- Carts appear in the list 2 hours after their last update.
- Sent carts stay until they're 7 days old (5 days of "sent + still visible" state typically).
- Unsent carts that the customer eventually returned to (after 2+ hours of inactivity) disappear once the cart records an `updated_at` more recent than the threshold — the list query filters on inactivity, so any cart re-touched moves out of scope.
- The whole list rolls over within a week regardless of merchant action.

### Inactivity is measured from the cart's last update

The threshold compares NOW vs the cart's `updated_at`. Any of: customer adding an item, removing an item, changing quantity, applying a discount code, or updating the shipping address resets `updated_at`. The cart drops out of the abandoned list (until the new threshold elapses), then re-enters once it crosses the threshold again.

This is why a cart can leave and re-enter the abandoned list multiple times over a 7-day window if the customer keeps coming back briefly without checking out.

### Soft-delete vs hard-delete

The hourly cleanup performs a **soft-delete** — the cart record remains in the database but is marked deleted. Soft-deleted carts:

- No longer appear in the abandoned list (eligibility rule 7 — see [[orders-abandoned-eligibility]]).
- Cannot be restored by the customer clicking an old restore link (rule 7 again).
- Eventually get hard-deleted by a deeper cleanup pass (timing not exposed to merchants).

### The threshold does not apply to the cart-cleanup job

`abandoned_remainder_interval` controls **only** which carts appear in the abandoned-cart list and which carts the auto-recovery job picks up. It does NOT influence `cart.lifetime` — even if the merchant sets the abandoned threshold to 30 days, the underlying cart still ages out at 7 days. The two settings are independent.

## Plan gates

None — these timing rules apply uniformly across all plans.

## Related

- [[orders-abandoned]] — hub.
- [[orders-abandoned-list-view]] — what the threshold filters into.
- [[orders-abandoned-auto-recovery]] — reads the same threshold.
- [[orders-abandoned-eligibility]] — rule 7 (not soft-deleted) ties to the cleanup.
- [[settings-cart]] — where `abandoned_remainder_interval` lives.
- [[cart]] — entity page; the `updated_at` column drives both threshold and cleanup.
- [[background-queue-inventory]] — catalogue of background jobs (auto-recovery + hourly `clear_all_old_carts`).

## Open questions

- Confirm the `abandoned_remainder` default value — whether `yes` or `no` out of the box across all plans. `(verify)`
