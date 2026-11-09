---
type: feature
nav_path: "Marketing → Discounts → Percent → Validity"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Percent discount validity", "Percent discount date rules", "Percent discount uses counter"]
tags: [marketing, discounts, percent, validity, dates]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, targeting, stacking, plan gates, programmatic access).

# Percent discount — validity (active gate, dates, uses counter)

## Purpose

A Percent discount is evaluated at checkout only when ALL of its activity / date / per-customer-cap conditions are satisfied. This page documents the gating chain, the UTC vs store-timezone difference for the auto-disable sweep, and the strictly-greater subtotal check on `order_over`.

## Where to find it

The active flag, date range, and limits live on the Percent create / edit form ([[percent-discount-editor]]). The row's **Active** switch on the [[marketing-discounts]] list view takes effect immediately. The UTC auto-disable sweep runs in the background — see [[background-queue-inventory]]. The `discounts_used_statuses` setting that controls the uses counter lives at [[settings-statuses]].

## What the merchant can do here

- Set `date_start` / `date_end`, or toggle `no_expire`, to control the validity window.
- Toggle the row's **Active** switch on / off, any number of times.
- Set `max_uses` and `maxused_user` caps; pick which statuses count by configuring `discounts_used_statuses` at [[settings-statuses]].
- Plan around the strictly-greater `order_over` rule by setting 99.99 when "100 or more" is the intent.

## Settings & fields

### Validity-related fields

| Field | Backend key | What it does |
|---|---|---|
| **Discount status** | `active` | `yes` / `no`. |
| **Start date** | `date_start` | First day the discount is eligible. Required. |
| **End date** | `date_end` | Last day. Asked for unless **No expiration** is on. Today and past dates save. |
| **No expiration** | `no_expire` | Clears `date_end`. |
| **Global discount limit** | `max_uses` | Total uses across customers. NULL = unlimited. Integer up to 100,000. |
| **Discount limit for customer** | `maxused_user` | Per-customer cap for logged-in customers, on codes at entry and on no-code `order_over`. NULL = unlimited. |

The `discounts_used_statuses` setting that controls which statuses count toward `uses` lives at [[settings-statuses]]. Full validation strings live on [[percent-discount-fields]].

## Active = within date window + uses remaining

A Percent discount is evaluated at checkout only when ALL of:

- `active = yes`.
- `date_start <= today` (store timezone).
- `date_end IS NULL OR date_end >= today`.
- `max_uses IS NULL OR max_uses > uses`.
- For code-based: cart's customer is in `customer_groups[]` (or list is empty) AND cart's shipping address is in `geo_zone_id` (or `all_regions=yes`) AND customer has used the code < `maxused_user` times.

## Strictly-greater subtotal check on `order_over` (no-code AND code-based)

The cart subtotal must be **strictly greater than** the `order_over` threshold for the discount to apply. A subtotal exactly equal to the threshold is rejected — the comparison is "discount's `order_over` is less than the cart subtotal" (the discount qualifies only when the cart strictly exceeds the threshold). The subtotal is the lines after product discounts, line-level codes and product-level Cart Rule reductions, at the prices as entered: a store whose prices exclude VAT is compared without VAT.

This strict-greater rule applies to **all `order_over` Percent / Flat discounts at cart-engine evaluation time** (both no-code and code-based variants). Merchants wanting *"X% off for orders 100 EUR or more"* should set the threshold to 99.99 EUR so that a 100.00 EUR cart still qualifies.

Free shipping differs: a free-shipping code with a threshold must be strictly above it at entry, then at or above on the total before shipping; no-code free shipping is at or above — see [[marketing-discounts-shipping]].

## Auto-disable on expiry — runs in UTC, NOT store timezone

An hourly background process toggles `active = no` on Percent discounts at its first run after **00:00 UTC on the day after `date_end`**. Timing nuance: the expiry check uses **UTC**, NOT the store's timezone. For a Europe/Sofia store, a discount with `date_end = 2026-06-15` is auto-disabled at the first run after 00:00 UTC on 2026-06-16, a few hours after the merchant's local end-of-day. West of UTC the sweep can run before the local last day ends.

Storefront cart-engine checks DO use store timezone for the `date_end >= today` gate at evaluation time, so customer-visible behaviour stops on the expected local date — but the row's `active = yes` flag and the listing's "Active" label persist until the UTC sweep runs.

This recurring process is part of [[background-queue-inventory]] (see *"Expired-discounts de-activation"*).

## Uses counter — counted statuses

A Percent discount's `uses` figure is recounted from orders using it in one of the **counted statuses** — configurable per store via the `discounts_used_statuses` setting; defaults to **`paid`, `completed`, `fulfilled`**. The recount leaves out orders in a negative status such as `cancelled` or `refunded`, even when fulfilled, so it can go back down; the per-customer count does not leave out a fulfilled one. See [[settings-statuses]].

## Per-customer cap auto-clears the code

If a logged-in customer hits the `maxused_user` cap for this Percent code, the platform doesn't merely fail to apply — it **wipes the code off the cart** and returns: *"You have used this discount code the maximum number of times"*. They'd need to enter a different code.

## `date_end` rules — today IS allowed

The form refuses only an end date before the start (*"The end date must be after the start date"*), and asks for one unless **No expiration** is on (*"The end date is required"*). Today and past dates save.

A Percent discount with `date_end = today` is valid through 23:59 today in store timezone. The sweep switches it off at its first run after 00:00 UTC the next day — see *Auto-disable on expiry* above.

## Business rules

- The 99.99 workaround for `order_over` is the canonical merchant-facing guidance when they want "100 EUR or more" semantics.
- The UTC sweep timing means *"my discount still says Active in the list but no customers can use it"* — explain that the customer-visible cutoff already happened in store timezone; the status catches up at the first sweep run after 00:00 UTC.

## Related

- [[marketing-discounts-percent]] — hub.
- [[percent-discount-fields]] — `date_start`, `date_end`, `no_expire`, `max_uses`, `maxused_user` validation rules.
- [[percent-discount-stacking]] — `code_apply` rejection that runs at the same per-line evaluation moment.
- [[discount-stacking]] — cross-discount rules for all discount types.
- [[settings-statuses]] — `discounts_used_statuses` configuration.
- [[background-queue-inventory]] — the expired-discounts UTC sweep.
- [[marketing-discounts-shipping]] — free-shipping thresholds.

## Open questions

None.
