---
type: feature
nav_path: "Apps → Delivery time → Order linkage"
route_name: apps.shipping_hours.overview
route_path: /admin/apps/shipping_hours
aliases: ["Delivery time on the order", "Expected Delivery", "Shipping Hours order linkage", "Expected Delivery column", "Edit delivery slot on order"]
tags: [apps, shipping, time-windows, scheduling, orders]
plan_gates: ["shipping_hours"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-shipping-hours]]. See the hub for the other aspects (overview, slots, availability).

# Delivery time → Order linkage (Expected Delivery)

## Purpose

This aspect documents **how a booked slot lands on the order and how the merchant sees / edits it afterwards**: the "Expected Delivery" stored on the order, the admin order-detail picker, the Orders-list column/filter, and the side-effects of changing the schedule after orders exist. The live slot computation behind the picker is on [[apps-shipping-hours-availability]].

## Where to find it

- **Order detail page** — the chosen Expected Delivery slot is shown, and the merchant can change it.
- **Orders list** — an Expected Delivery column / filter.

## What the merchant can do here

### On the order detail screen
- See the customer's chosen Expected Delivery slot.
- Change the slot from the order (a radio list of available slots). The picker re-runs the same live availability computation for that method — see [[apps-shipping-hours-availability]].

### On the Orders list
- Filter / sort by **Expected Delivery**, with text like *"Expected Delivery [date]"* and per-slot detail *"Interval from:from to:to. Elapsed:remaining from:limit"*.

### What the merchant CANNOT do here
- Assign a slot that is full / past its lead-time cutoff — the order picker only offers currently-available slots.
- Auto-notify the customer of a slot change — there is no built-in slot-change email.

## Settings & fields

When a customer (or admin) picks a slot, the order saves two fields:

| Field | Notes |
|-------|-------|
| `shipping_hour_id` | The chosen slot value's ID. |
| `shipping_date` | The calendar date of the booking. |

The admin "Expected Delivery" radio picker re-runs the slot-availability computation to refresh the slots offered for that method — see [[apps-shipping-hours-availability]].

## Business rules

### Order's Expected Delivery
- Stored on the order along with the booked slot ID and date.
- Shown on the Orders list / detail screen.
- Editable by the merchant from the order detail (radio picker of slots available for that method).

### Schedule changes do not retroactively cancel orders
- Changing the `interval` setting downward does NOT cancel existing future bookings beyond the new window — they remain on the orders (the setting only changes what is OFFERED at checkout; see [[apps-shipping-hours-settings]]).
- Adding an exception date does NOT cancel orders already booked for that date.
- Deleting a day schedule does NOT cancel orders booked for that day — only stops NEW bookings.

### Cancelling frees the slot
Because slot capacity counts only orders in `pending` / `paid` / `completed` / `authorized`, cancelling or refunding a slot-booked order returns its capacity to the slot for the next customer — see [[apps-shipping-hours-availability]].

### Permission
Standard apps permission scope (`store.shipping`).

## Related

- [[apps-shipping-hours]] — hub.
- [[apps-shipping-hours-availability]] — the live computation the order picker re-runs.
- [[apps-shipping-hours-settings]] — `interval` / `category` settings; downward `interval` change does not cancel existing bookings.
- [[orders]] — Expected Delivery column / filter on the Orders list.
- [[orders-details-shipping]] — order-detail shipping section where the Expected Delivery slot is shown and edited.

## Open questions

_None — behavior captured above._
