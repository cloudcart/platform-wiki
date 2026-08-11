---
type: feature
nav_path: "Apps → Delivery time → Settings"
route_name: apps.shipping_hours.settings
route_path: /admin/apps/shipping_hours/settings
aliases: ["Shipping Hours Settings", "Delivery time settings"]
tags: [apps, shipping, shipping-hours, settings]
plan_gates: [shipping_hours]
created: 2026-05-21
updated: 2026-05-28
source_count: 1
---
# Delivery time → Settings

## Purpose

The **Settings** tab holds the two GLOBAL settings for the Delivery time app. Per-shipping-method schedules (the actual time slots) are configured in [[apps-shipping-hours-shipping-list]]. See [[apps-shipping-hours]] for the full feature.

## Where to find it

Sidebar → Apps → Delivery time → **Settings tab**. Path `/admin/apps/shipping_hours/settings`.

## What the merchant can do here

Two global settings only:

| Setting | Notes |
|-------|-------|
| **Number of days for which reservations can be made in advance** (`interval`) | How many days ahead the customer can book a slot. Default 5 days. Minimum 1. |
| **Time Intervals in Product Categories** (`category`) | Switch. When ON, the cart's MAXIMUM product-category lead time (from each category's "Technological delivery time in hours" field) is ADDED to "now" before computing the earliest bookable slot. Used for made-to-order goods with prep time. **Affects Delivery-time (non-courier) methods only — courier methods ignore this field.** |

### What the merchant CANNOT do here
- Configure per-shipping-method slots — that's done in [[apps-shipping-hours-shipping-list]].
- Set defaults that auto-apply to new methods — each method's schedule is configured from scratch.
- Set a global exception calendar — exceptions are per shipping method.
- Override individual slot rules from this tab — every slot's From / To / Orders limit / Start / Interval lives in the per-method editor.

## Settings & fields

| Field | Notes |
|-------|-------|
| `interval` | Integer, default 5, minimum 1. |
| `category` | Switch (on/off). Default off. |

### Validation messages
Backend the request validator:
- *"The value must be a number"* — non-numeric input (`interval.numeric`).
- *"The value must be an integer"* — fractional input (`interval.integer`).
- *"The value must be at least 0"* — `interval` below minimum (`interval.min`).

## Business rules

### Setting changes don't affect existing slots
Changing `interval` here does NOT alter the per-method schedules. It only changes how many days into the future the customer sees as bookable at checkout. If a merchant lowers `interval` from 7 to 3, slots configured for day 4–7 remain stored — they're just not shown at checkout until the merchant raises the value back up.

### Category lead time uses MAX across cart
With `category` ON, when a cart contains items from multiple categories the platform uses the MAXIMUM lead-time across the cart. A single "48 hours prep" item pushes the entire cart's earliest available slot 48 hours forward, regardless of how many other items have lead time 0.

### Technological delivery time is per-category (no inheritance)
The per-category "Technological delivery time in hours" is set on each category individually and is **NOT inherited by subcategories** — a subcategory with a blank value contributes 0 even if its parent has a prep time. Set it on every category that needs it. See [[products-categories]].

### Permission
Standard apps permission scope.

## Related

- [[apps-shipping-hours]] — hub.
- [[apps-shipping-hours-shipping-list]] — per-method slot configuration.
- [[products-categories]] — Technological delivery time in hours field (per category) used by the `category` setting.

## Open questions

_None._
