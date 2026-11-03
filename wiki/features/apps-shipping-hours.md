---
type: feature
nav_path: "Apps → Delivery time"
route_name: apps.shipping_hours.overview
route_path: /admin/apps/shipping_hours
aliases: ["Shipping Hours", "Delivery hours", "Delivery time", "Delivery time windows", "Часове за доставка", "Доставка по часове", "enable disable button", "app active toggle"]
tags: [apps, shipping, time-windows, scheduling]
plan_gates: ["shipping_hours"]
created: 2026-05-22
updated: 2026-08-06
source_count: 5
---
# Delivery time (Shipping Hours)

## Purpose

**Delivery time** is a scheduling app that adds time-slot booking to selected **non-courier** shipping methods. It is NOT a courier integration — it sits on top of OTHER (merchant-configured) shipping methods and lets the customer pick a specific delivery day + time window at checkout (e.g. "Tomorrow 14:00–16:00").

Used by merchants who:
- Sell perishable goods (groceries, food, flowers) and need scheduled delivery.
- Run same-day urban delivery via their own riders / partners.
- Need to cap parallel deliveries per slot (e.g. only 10 orders per 14:00–16:00 window).
- Want exception dates (holidays, special closures) excluded from the bookable calendar.

**Important constraint:** Delivery time only attaches to shipping methods that DON'T have a courier integration. Econt / Speedy / GLS / BoxNow / etc. supply their own delivery scheduling and the "Delivery days" link does not appear on those rows. The merchant must use a manual / flat-rate shipping method for this feature. See [[apps-shipping-hours-overview]] for the eligibility mechanism.

This page is the **hub** for the Delivery time cluster — it points to the aspect pages below. Drill into the aspect that matches the question rather than reading every page.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it. A disabled app stops working while keeping its settings — so *"the app is disabled"* IS a valid explanation to check here.

## Sub-pages (in this cluster)

- [[apps-shipping-hours-overview]] — what the app is + who it's for; the non-courier eligibility rule (`has_delivery_dates`); plan gating; the `action_after_add_to_cart` install side-effect.
- [[apps-shipping-hours-settings]] — the two global settings (`interval` days look-ahead + `category` lead-time toggle); Settings-tab fields + validation.
- [[apps-shipping-hours-shipping-list]] — the List-of-shipping-methods tab + the per-method editor UI (day grid, "New day with hours" modal, Exceptions modal).
- [[apps-shipping-hours-slots]] — the per-day schedule + per-time-slot fields (From / To / Orders limit / Start / Interval); exception calendar; storage model; validation messages.
- [[apps-shipping-hours-availability]] — the live (no-cache) bookable-slot computation; the `interval` window; category lead-time MAX; capacity counting + cancel-frees-slot.
- [[apps-shipping-hours-order-linkage]] — Expected Delivery on the order; admin order-detail slot picker; Orders-list column/filter; why schedule changes don't cancel existing orders.

## Where to find it

- Sidebar → Apps → install → **Delivery time**.
- After install: Sidebar → Apps → **Delivery time** → 3 tabs (Overview / Settings / List of shipping methods).
- Per-shipping-method: Settings → Shipping methods list — each row WITHOUT a carrier integration shows a small "Delivery days" link that opens the per-method schedule editor.

Four routes:

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.shipping_hours.overview` | `/admin/apps/shipping_hours` |
| Settings | `apps.shipping_hours.settings` | `/admin/apps/shipping_hours/settings` |
| List of shipping methods | `apps.shipping_hours.shipping_list` | `/admin/apps/shipping_hours/shipping-list` |
| Delivery days editor | `apps.shipping_hours.list` | `/admin/apps/shipping_hours/delivery_hours/:id` |

## What the merchant can do here

At a glance, across the cluster:
- Set two **global settings** (days of look-ahead + category lead-time) — see [[apps-shipping-hours-settings]].
- Attach a **per-method schedule** to any non-courier method (days + time slots + exceptions) — see [[apps-shipping-hours-slots]] and the editor UI in [[apps-shipping-hours-shipping-list]].
- The customer picks a slot at checkout; the merchant sees / edits it as the order's **Expected Delivery** — see [[apps-shipping-hours-order-linkage]].

### What the merchant CANNOT do here
- Use Delivery time with a courier-integrated method (Econt / Speedy / GLS / BoxNow / etc.).
- Set per-customer windows, force a customer into a slot, or set per-slot pricing.
- Track real-time courier availability or send slot-reminder emails automatically.

Full do/can't detail per aspect — start with [[apps-shipping-hours-overview]].

## Settings & fields

The configurable surfaces live on the aspect pages:
- **Global settings** (`interval`, `category`) — see [[apps-shipping-hours-settings]].
- **Per-day schedule + per-slot fields** (From / To / Orders limit / Start / Interval) + exceptions + validation — see [[apps-shipping-hours-slots]].

## Business rules

The detailed rules are distributed across the aspects; the load-bearing ones:
- **Non-courier only** — the slot computation aborts for providers whose `has_delivery_dates` flag is false. See [[apps-shipping-hours-overview]].
- **Live slot list, no cache** — recomputed on every checkout + order-edit request; cancelled / refunded orders free capacity. See [[apps-shipping-hours-availability]].
- **Category lead-time uses MAX across the cart** when the `category` setting is ON. See [[apps-shipping-hours-availability]].
- **Schedule changes don't retroactively cancel orders** — lowering `interval`, adding an exception, or deleting a day only stops NEW bookings. See [[apps-shipping-hours-order-linkage]].
- **Install side-effect** — forces `action_after_add_to_cart` to `stay_on_page` store-wide; not restored on uninstall. See [[apps-shipping-hours-overview]].
- **Permission** — standard apps scope (`store.shipping`).

## Plan gates

This app is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `shipping_hours` | Access gate (install URL) | The install URL `/admin/apps/shipping_hours/install` is blocked when the plan lacks the feature. The app is hidden from the Apps catalog for those plans. |

Behaviour: lower plans cannot install the app. Existing installs continue working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]].

## Related

- [[checkout-step-time-slots]] — storefront-side delivery-date / time-slot picker the app enables at checkout.

- [[delivery-scheduling]] — the cross-cutting model: how a slot relates to the shipping method (courier-scheduled vs app-scheduled).
- [[apps]] — App Store hub.
- [[apps-shipping-hours-overview]] — eligibility, plan gating, install side-effect.
- [[apps-shipping-hours-settings]] — the two global settings.
- [[apps-shipping-hours-shipping-list]] — per-method editor UI.
- [[apps-shipping-hours-slots]] — per-day schedule + per-slot fields.
- [[apps-shipping-hours-availability]] — live slot computation.
- [[apps-shipping-hours-order-linkage]] — Expected Delivery on the order.
- [[shipping]] — shipping providers landing.
- [[settings-shipping]] — shipping methods list (where the "Delivery days" link appears).
- [[products-categories]] — category editor (Technological delivery time in hours field used by the `category` setting).
- [[orders]] — Expected Delivery column / filter on the Orders list.

## Open questions

_None — behavior captured above._
