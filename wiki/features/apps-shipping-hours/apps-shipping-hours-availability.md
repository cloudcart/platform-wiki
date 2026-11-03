---
type: feature
nav_path: "Apps → Delivery time → Availability"
route_name: apps.shipping_hours.list
route_path: /admin/apps/shipping_hours/delivery_hours/:id
aliases: ["Delivery time availability", "Shipping Hours slot computation", "Bookable slot list", "Delivery slot lead time", "Delivery slot capacity"]
tags: [apps, shipping, time-windows, scheduling]
plan_gates: ["shipping_hours"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-shipping-hours]]. See the hub for the other aspects (overview, slots, order linkage).

# Delivery time → Availability computation

## Purpose

This aspect documents **how the bookable slot list is computed and filtered every time it is shown** — at storefront checkout and on the admin order-edit screen. It explains the live (no-cache) algorithm, the `interval` look-ahead window, the category lead-time bump, and how slot capacity is counted and freed. The slot fields themselves are on [[apps-shipping-hours-slots]]; the two global settings driving the window are on [[apps-shipping-hours-settings]].

## Where to find it

The computed list surfaces to the customer at checkout (after they select a Delivery-time-enabled shipping method) and to the merchant on the order detail's "Expected Delivery" radio picker — see [[apps-shipping-hours-order-linkage]].

## What the merchant can do here

The merchant does not edit the availability computation directly — it is derived from the per-method schedule ([[apps-shipping-hours-slots]]) plus the two global settings (`interval`, `category` — see [[apps-shipping-hours-settings]]). Understanding it matters for support: it explains why a configured slot may not appear at checkout (past lead-time cutoff, outside the `interval` window, exception date, or at capacity).

### Customer-facing at checkout
When the customer picks a shipping method with Delivery time configured, the checkout shows a date+time-slot picker grouped by day. Past times are hidden; days outside the `interval` window are hidden; exception dates are hidden; slots past their lead-time cutoff are hidden; slots at their **Orders limit** are shown but disabled. The picked slot is saved on the order as the "Expected Delivery".

## Settings & fields

The computation reads from:
- The per-method schedule rows + slots + exceptions — see [[apps-shipping-hours-slots]].
- `interval` — how many days ahead the customer can book — see [[apps-shipping-hours-settings]].
- `category` — whether to add the cart's max product-category lead time — see [[apps-shipping-hours-settings]].

There are no fields to edit on this aspect — it is computed output.

## Business rules

### Slot list built live at checkout + order edit (no cache)
The bookable list is computed fresh on every request — there is no background sync. The algorithm:

1. Start from "now".
2. If the `category` setting is ON and the cart's max category lead time is non-zero, add that lead time to "now" (storefront only, via the checkout wrapper).
3. Look up the day of week for "now" and iterate forward day-by-day (capped at a safety upper bound).
4. For each day: skip if the date is in the exceptions list; otherwise pull the schedule row matching that weekday; for each slot row, build the candidate window.
5. Apply the lead-time cutoff: `checkDate = (start ? from: to) − interval hours`. If `checkDate` is already in the past relative to "now", drop the slot.
6. Chunk the result by `interval` days and keep only the first chunk — so the customer sees up to `interval` days of bookable slots.
7. Run a single grouped query against the orders table: for each (slot, date), count orders in statuses `pending`, `paid`, `completed`, `authorized`.
8. For each slot: `remaining = limit − orders_count`; the slot is `disabled` when `remaining < 1`. Disabled slots are still shown, marked unbookable.

This means the customer-facing slot picker always reflects real-time capacity — no manual refresh.

### Category lead-time uses MAX across cart
When the `category` setting is ON and the cart contains items from multiple categories, the platform uses the MAXIMUM category lead-time across the cart (each category's "Technological delivery time in hours" — see [[products-categories]]). A single item with "48 hours prep" pushes the entire cart's earliest available slot 48 hours forward, regardless of how many other items have lead time 0. This bump runs **only inside the non-courier checkout computation** — the eligibility gate aborts for courier methods *before* it applies, so the category "Technological delivery time in hours" field affects **only** Delivery-time (non-courier) slots; courier methods (Econt / Speedy / etc.) ignore it entirely.

### Cancelled orders free up slot capacity
The slot's remaining count includes only orders in statuses `pending` / `paid` / `completed` / `authorized`. Cancelled / refunded orders are excluded, so cancelling a slot-booked order automatically frees the slot for the next customer.

### A slot is required — and an unavailable slot blocks the method

When the Delivery time app is installed and the chosen method has a schedule (`has_delivery_dates`), the customer **must** book a slot to place the order. The checkout re-validates the pick on submit and, on failure, **resets the shipping selection** (the customer is sent back to re-choose) with one of three messages:

- **No slot chosen** → *delivery date required* (`sf.delivery_date.error.required`).
- **Chosen slot no longer in the list** (it expired between page load and submit, or the list is now empty) → *invalid* (`sf.delivery_date.error.invalid`).
- **Chosen slot is full** (`remaining < 1`) → *no remaining capacity* (`sf.delivery_date.error.remaining`).

So when the computation returns **no bookable slots at all** (every slot is past its cutoff, on an exception date, or outside the `interval` window), the customer **cannot complete checkout with that method** — they must pick a different shipping method. A Delivery-time method is also **never auto-selected** as the sole shipping option (unlike ordinary methods): the customer always has to open the picker and book a slot before the order can go through.

### Eligibility gate
The computation aborts (returns null) when the shipping provider's `has_delivery_dates` flag is false — i.e. for courier-integrated methods. This is the mechanism behind "only non-courier methods" — see [[apps-shipping-hours-overview]] and [[shipping-provider-lifecycle]].

### Permission
Standard apps permission scope (`store.shipping`).

## Related

- [[apps-shipping-hours]] — hub.
- [[apps-shipping-hours-slots]] — the slot fields (From / To / Orders limit / Start / Interval) this algorithm filters.
- [[apps-shipping-hours-settings]] — the `interval` window + `category` lead-time settings the algorithm reads.
- [[apps-shipping-hours-order-linkage]] — where the chosen slot lands on the order and how the admin re-runs this computation.
- [[products-categories]] — "Technological delivery time in hours" field used by the `category` lead-time bump.

## Open questions

_None — behavior captured above._
