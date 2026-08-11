---
type: feature
nav_path: "Marketing → Discounts → Percent → Validity"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/global
aliases: ["Percent discount validity", "Percent discount date rules", "Percent discount activation cooldown", "Percent discount uses counter"]
tags: [marketing, discounts, percent, validity, dates]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, targeting, stacking, plan gates, programmatic access).

# Percent discount — validity (active gate, dates, cooldown, uses counter)

## Purpose

A Percent discount is evaluated at checkout only when ALL of its activity / date / per-customer-cap conditions are satisfied. This page documents the gating chain, the UTC vs store-timezone difference for the auto-disable sweep, the 10-minute activation cooldown for no-code Percent, and the strictly-greater subtotal check on `order_over`.

## Where to find it

The active flag, date range, and limits live on the Percent create / edit form ([[percent-discount-editor]]). The row's **Active** switch on the [[marketing-discounts]] list view triggers the 10-minute cooldown. The UTC auto-disable sweep runs in the background — see [[background-queue-inventory]]. The `discounts_used_statuses` setting that controls the uses counter lives at [[settings-statuses]].

## What the merchant can do here

- Set `date_start` / `date_end`, or toggle `no_expire`, to control the validity window.
- Toggle the row's **Active** switch on / off (subject to the 10-minute cooldown for no-code Percent).
- Set `max_uses` and `maxused_user` caps; pick which statuses count by configuring `discounts_used_statuses` at [[settings-statuses]].
- Plan around the strictly-greater `order_over` rule by setting 99.99 when "100 or more" is the intent.

## Settings & fields

### Validity-related fields

| Field | Backend key | What it does |
|---|---|---|
| **Discount status** | `active` | `yes` / `no`. The 10-minute cooldown applies on no-code Percent toggles. |
| **Start date** | `date_start` | First day the discount is eligible. Required. |
| **End date** | `date_end` | Last day. Nullable. `date_end = today` IS accepted. |
| **No expiration** | `no_expire` | Clears `date_end`. |
| **Global discount limit** | `max_uses` | Total uses across customers. NULL = unlimited. Integer 1-100,000. |
| **Discount limit for customer** | `maxused_user` | Per-customer cap. NULL = unlimited. |

The `discounts_used_statuses` setting that controls which statuses increment `uses` lives at [[settings-statuses]]. Full validation strings live on [[percent-discount-fields]].

## Active = within date window + uses remaining

A Percent discount is evaluated at checkout only when ALL of:

- `active = yes`.
- `date_start <= today` (store timezone).
- `date_end IS NULL OR date_end >= today`.
- `max_uses IS NULL OR max_uses > uses`.
- For code-based: cart's customer is in `customer_groups[]` (or list is empty) AND cart's shipping address is in `geo_zone_id` (or `all_regions=yes`) AND customer has used the code < `maxused_user` times.

## Strictly-greater subtotal check on `order_over` (no-code AND code-based)

The cart subtotal must be **strictly greater than** the `order_over` threshold for the discount to apply. A subtotal exactly equal to the threshold is rejected — the comparison is "discount's `order_over` is less than the cart subtotal" (the discount qualifies only when the cart strictly exceeds the threshold).

This strict-greater rule applies to **all `order_over` Percent / Flat discounts at cart-engine evaluation time** (both no-code and code-based variants). Merchants wanting *"X% off for orders 100 EUR or more"* should set the threshold to 99.99 EUR so that a 100.00 EUR cart still qualifies.

Code-based Percent on `order_over` shipping has a separate inclusive (`>=`) comparison at the code-validation step — see [[marketing-discounts-shipping]] for the shipping-specific exception.

## Auto-disable on expiry — runs in UTC, NOT store timezone

A daily background process toggles `active = no` on Percent discounts whose `date_end` is **at least 1 day in the past in UTC**. Timing nuance: the expiry check uses **UTC**, NOT the store's timezone. For a Europe/Sofia store, a discount with `date_end = 2026-06-15` (interpreted as end-of-day in store time) will NOT be auto-disabled until the daily process runs after 2026-06-16 23:59 UTC — i.e., the discount may remain technically "active" for up to ~27 hours after the merchant's local end-of-day.

Storefront cart-engine checks DO use store timezone for the `date_end >= today` gate at evaluation time, so customer-visible behaviour stops on the expected local date — but the row's `active = yes` flag and the listing's "Active" label persist until the UTC sweep runs.

This recurring process is part of [[background-queue-inventory]] (see *"Expired-discounts de-activation"*).

## Activation cooldown (10 minutes — applies to no-code Percent)

Toggling a no-code Percent discount's active status is rate-limited to **once per 10 minutes per discount**. Within the cooldown window the toggle response is:

> *"You've already activated this discount. Please wait:minutes minutes in order to be able to deactivate it again."*

The cooldown exists because every active-toggle triggers a per-product attachment regeneration — the platform rebuilds the join records that feed the storefront's *"from X / now Y"* pricing display. For high-catalog stores this regeneration consumes significant database write throughput, so the 10-minute throttle prevents thrashing the background queue.

The cooldown is enforced **per-discount** (not per-store) — the merchant can toggle different discounts in quick succession, just not the same one. The cooldown is bypassed in development environments and command-line contexts.

**Scope clarification:** the cooldown applies to **no-code** Flat / Percent / Shipping / Fixed discounts only. **Code-based Percent variants, Container codes, Quantity, Countdown, and Code PRO have NO cooldown** — see the per-type cooldown table on [[discount-stacking]].

## Uses counter — counted statuses

A Percent discount's `uses` counter increments ONLY when an order using it reaches one of the **counted statuses** — configurable per store via the `discounts_used_statuses` setting; defaults to **`paid`, `completed`, `fulfilled`**. Cancelled / refunded orders never burn a use. See [[settings-statuses]].

## Per-customer cap auto-clears the code

If a logged-in customer hits the `maxused_user` cap for this Percent code, the platform doesn't merely fail to apply — it **wipes the code off the cart** and returns: *"You have already used this discount the maximum number of times"*. They'd need to enter a different code.

## `date_end` rules — today IS allowed

The `date_end` validator compares against the **end of the current day** in store timezone using a strict "less-than" check — meaning a `date_end` value equal to today's date IS accepted (it represents end-of-day today). The previously documented rejection message *"End date cannot be less than now"* does not actually fire for today's date; the rule only rejects dates that already passed (`date_end < end-of-today`).

A merchant CAN save a Percent discount with `date_end = today`, and the discount will be valid through 23:59 today in store timezone. Auto-disable (the UTC sweep) won't pick it up until ~27 hours later — see *Auto-disable on expiry* above.

## Business rules

- The active-toggle 10-minute cooldown is the most-asked support question for the row's Active switch returning a rate-limit error — direct merchants to [[discount-stacking]] for the full per-type cooldown table.
- The 99.99 workaround for `order_over` is the canonical merchant-facing guidance when they want "100 EUR or more" semantics.
- The UTC sweep timing means *"my discount still says Active in the list but no customers can use it"* — explain that the customer-visible cutoff already happened in store timezone; the admin badge will catch up within ~27 hours.

## Related

- [[marketing-discounts-percent]] — hub.
- [[percent-discount-fields]] — `date_start`, `date_end`, `no_expire`, `max_uses`, `maxused_user` validation rules.
- [[percent-discount-stacking]] — `code_apply` rejection that runs at the same per-line evaluation moment.
- [[discount-stacking]] — full per-type cooldown table.
- [[settings-statuses]] — `discounts_used_statuses` configuration.
- [[background-queue-inventory]] — the expired-discounts UTC sweep.
- [[marketing-discounts-shipping]] — `>=` (inclusive) exception at the shipping-code-validation step.

## Open questions

None.
