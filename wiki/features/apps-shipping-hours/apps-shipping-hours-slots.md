---
type: feature
nav_path: "Apps → Delivery time → Slots & schedule"
route_name: apps.shipping_hours.list
route_path: /admin/apps/shipping_hours/delivery_hours/:id
aliases: ["Delivery time slots", "Shipping Hours time slots", "Delivery day schedule", "Per-slot fields", "Delivery time exceptions"]
tags: [apps, shipping, time-windows, scheduling]
plan_gates: ["shipping_hours"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-shipping-hours]]. See the hub for the other aspects (overview, availability, order linkage).

# Delivery time → Slots & per-day schedule

## Purpose

This aspect documents **how the merchant defines the bookable schedule for one non-courier shipping method**: the per-day rows, the per-time-slot fields (From / To / Orders limit / Start / Interval), the exception calendar, and the validation messages. How those slots are then filtered and offered at checkout is on [[apps-shipping-hours-availability]].

## Where to find it

Per-method editor at `/admin/apps/shipping_hours/delivery_hours/:id`, reached from the List of shipping methods tab — see [[apps-shipping-hours-shipping-list]] for the navigation and the modal layout.

## What the merchant can do here

For each non-courier shipping method, the merchant defines:
- A schedule per day of week (Monday–Sunday). **One schedule entry per weekday.**
- Multiple time slots per day — each with From / To / Orders limit / Start / Interval.
- Exception dates — calendar days excluded from booking (holidays, special closures).

### Per-time-slot fields

| Field | Notes |
|-------|-------|
| **From** | Slot start time (HH:mm). |
| **To** | Slot end time (HH:mm). |
| **Orders limit** | Max orders bookable into this slot. Once reached, the slot is shown as full / disabled at checkout. |
| **Start** | Toggle. ON = lead-time cutoff measured from **From**; OFF = measured from **To**. Affects whether late same-day bookings are still allowed. Tooltip: *"If you enable this option, the distance that will be taken into account will start from the start time. If it is turned off, the end time will be used."* |
| **Interval** | Required lead-time hours between order placement and the slot. Slots whose cutoff is already past are hidden at checkout. Tooltip: *"Choose a gap of hours between the order and the first possible delivery time."* |

### What the merchant CANNOT do here
- Configure two schedule rows for the same weekday — each weekday is unique per method (the day picker hides already-configured days).
- Set per-slot pricing — there is no surcharge field; all slots share the method's shipping price.
- Apply one exception calendar across methods — exceptions are stored per shipping method only.

## Settings & fields

### Per-day schedule (per shipping method)

| Field | Notes |
|-------|-------|
| **Day** | Monday–Sunday picker. One schedule entry per weekday. |
| **From** | Slot start time (HH:mm). |
| **To** | Slot end time (HH:mm). |
| **Orders limit** | Max orders per slot. |
| **Start** | Toggle for lead-time cutoff anchor (From vs To). |
| **Interval** | Required lead-time hours. |

### Exception calendar (per shipping method)
- The merchant adds specific calendar dates that are excluded from booking, via the **Exceptions** button in the per-method editor.
- Stored independently per shipping method — there is no global "store closed" calendar that cascades across methods.

### Storage — three tables (verified against backend)
The schedule is stored across three tables, all linked to a shipping provider (`provider_id`):
- **shipping_hours** — one row per (provider, day_of_week). `day_of_week` is `1` (Monday) through `7` (Sunday). A unique constraint forbids two rows with the same (provider, day_of_week).
- **shipping_hours_values** — child rows under `shipping_hour_id`. Each row is one slot: `from`, `to` (HH:mm), `limit` (orders cap), `start` (boolean — cutoff anchor), `interval` (hours of lead time).
- **shipping_hours_exceptions** — per-provider list of `exception` dates (datetime-cast). Each row excludes ONE calendar day for that provider.

Deleting a `shipping_hours` row cascades — its slot children are deleted automatically.

### Validation messages
Per-day form (the request validator):
- *"Day is required"* — `day_of_week.required`.
- *"Day already exists"* — `day_of_week.unique` (weekday already configured for this method).
- *"Hours are required"* — `hours.required`.
- *"From is required"* — `hours.*.from.required`.
- *"To is required"* — `hours.*.to.required`.
- *"To must be after From"* — `hours.*.to.after`.
- *"To must be after previous To"* — custom `after_previous` rule on `from` (prevents overlapping / out-of-order slots within the same day).
- *"Limit is required"* — `hours.*.limit.required`.
- *"Limit must be greater than 0"* — `hours.*.limit.min`.

Backend rules: `day_of_week` required, between 1–7, unique per provider; `hours` required array; `hours.*.from` HH:mm and after the previous slot's `to`; `hours.*.to` HH:mm and after `from`; `hours.*.limit` integer ≥ 0; `hours.*.interval` numeric integer ≥ 0; `hours.*.start` defaults to 0.

## Business rules

### One schedule per day per method
Each shipping method can have one schedule entry per weekday. To run different rules on different weeks, the merchant uses exception dates (or edits the schedule when needed).

### Exception dates apply to this method only
- Apply to that method only — there's no global "store closed" calendar that cascades across methods.
- Don't cancel existing orders booked on that date — only stop NEW bookings.

### Deleting schedule does not cancel orders
- Deleting a day schedule does NOT cancel orders booked for that day — only stops NEW bookings.
- Adding an exception date does NOT cancel orders already booked for that date.

These are deliberate side-effects; the consequences for already-placed orders are detailed in [[apps-shipping-hours-order-linkage]].

### Permission
Standard apps permission scope (`store.shipping`). The route also requires the `shipping_hours` plan gate to be active.

## Related

- [[apps-shipping-hours]] — hub.
- [[apps-shipping-hours-shipping-list]] — the per-method editor UI (modals, day grid, exceptions modal) that hosts these fields.
- [[apps-shipping-hours-availability]] — how these slot fields are filtered into the bookable list at checkout.
- [[settings-shipping]] — where non-courier shipping methods are created.

## Open questions

_None — behavior captured above._
