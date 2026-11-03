---
type: concept
nav_path: "Concept → Delivery scheduling"
route_name: (none)
route_path: (none)
aliases: ["Delivery scheduling", "Delivery date and time", "Delivery time slots", "When orders get delivered", "Delivery day", "Доставка по график", "Кога се доставя", "Ден и час за доставка", "Часови слот за доставка", "Delivery slot setup"]
tags: [shipping, delivery, scheduling, time-slots, concepts, hub]
plan_gates: []
created: 2026-06-11
updated: 2026-06-11
source_count: 2
---
# Delivery scheduling

## Definition

**Delivery scheduling** is how CloudCart decides the **delivery day / time** for an order and how that relates to the chosen **shipping method**. Two models exist:

- **Courier-scheduled** — a courier-integrated method (Econt, Speedy, GLS, BoxNow, …) delivers on the courier's own timetable; the store does not offer time slots.
- **Merchant-scheduled (time slots)** — the [[apps-shipping-hours|Delivery time]] app adds bookable **day + time-slot** booking on top of a **non-courier** shipping method, so the customer picks a window at checkout (e.g. "Tomorrow 14:00–16:00").

A manual method without the app configured has no scheduling at all — the order simply carries no delivery window.

## Scope — the setup relationship (slot ↔ shipping method)

The slot schedule is **attached to a specific shipping method**, not set globally:

1. **Pick the shipping method** in [[settings-shipping]]. It must be a **manually-configured (non-courier)** method — courier methods own their own timing and never get a slot schedule.
2. **Install the Delivery time app** ([[apps-shipping-hours]]) — a **paid** app (the install opens a billing step). Set its two global settings (`interval` look-ahead days + `category` prep-time toggle) — see [[apps-shipping-hours-settings]].
3. On that method's row a **"Delivery days"** link appears → open it to define **days + time slots + exceptions** for the method — see [[apps-shipping-hours-shipping-list]] and [[apps-shipping-hours-slots]].
4. **At checkout** the customer must book a slot; the bookable list is computed live from the schedule + the `interval` window + category prep-time + per-slot capacity — see [[apps-shipping-hours-availability]].
5. **On the order** the booked slot is stored as **Expected Delivery** (editable by the merchant) — see [[apps-shipping-hours-order-linkage]].

## Contrasts

- **Courier-scheduled vs slot-scheduled vs none** — couriers schedule themselves; the Delivery time app schedules non-courier methods; an unconfigured manual method has no delivery window.
- **Delivery time vs delivery price** — the slot is *when*; [[shipping-calculation]] decides *how much*. Slots carry **no surcharge** — every slot shares the method's shipping price.
- **Per-method, not per-store** — each method has its own schedule and its own exception calendar; there is no global delivery calendar.

## Where it applies

- **Setup** — [[settings-shipping]] (the method) + the "Delivery days" editor ([[apps-shipping-hours]]).
- **Prep time** — per-category "Technological delivery time in hours" pushes the earliest slot forward ([[products-categories]] + [[apps-shipping-hours-settings]]); set per category, **not inherited by subcategories**.
- **Checkout** — the slot picker ([[checkout-flow]] / [[apps-shipping-hours-availability]]).
- **Order** — Expected Delivery ([[apps-shipping-hours-order-linkage]]).

## Related

- [[apps-shipping-hours]] — the Delivery time app (full how-to: install, settings, slots, exceptions).
- [[settings-shipping]] — where the shipping method (and its "Delivery days" link) live.
- [[shipping-calculation]] — delivery price (distinct from delivery time).
- [[apps-shipping-hours-availability]] — the live slot computation + checkout rules.
- [[apps-shipping-hours-order-linkage]] — Expected Delivery on the order.

## Open Questions

- Whether any courier integration also exposes merchant-editable time slots (currently none — couriers self-schedule).
