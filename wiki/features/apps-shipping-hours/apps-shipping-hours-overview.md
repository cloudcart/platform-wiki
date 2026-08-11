---
type: feature
nav_path: "Apps → Delivery time → Overview"
route_name: apps.shipping_hours.overview
route_path: /admin/apps/shipping_hours
aliases: ["Delivery time overview", "Shipping Hours overview", "Delivery time eligibility", "Non-courier delivery scheduling"]
tags: [apps, shipping, time-windows, scheduling]
plan_gates: ["shipping_hours"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[apps-shipping-hours]]. See the hub for the other aspects (slots, availability, order linkage) and the two sibling tabs (settings, shipping list).

# Delivery time → Overview & eligibility

## Purpose

This aspect covers **what the Delivery time app is, who it is for, the hard non-courier eligibility rule, plan gating, and the install side-effect**. The slot fields are on [[apps-shipping-hours-slots]]; the live availability algorithm is on [[apps-shipping-hours-availability]]; how the picked slot lands on the order is on [[apps-shipping-hours-order-linkage]].

**Delivery time** is a scheduling app that adds time-slot booking to selected **non-courier** shipping methods. It is NOT a courier integration — it sits on top of OTHER (merchant-configured) shipping methods and lets the customer pick a specific delivery day + time window at checkout (e.g. "Tomorrow 14:00–16:00").

Used by merchants who:
- Sell perishable goods (groceries, food, flowers) and need scheduled delivery.
- Run same-day urban delivery via their own riders / partners.
- Need to cap parallel deliveries per slot (e.g. only 10 orders per 14:00–16:00 window).
- Want exception dates (holidays, special closures) excluded from the bookable calendar.

## Where to find it

- Sidebar → Apps → install → **Delivery time**.
- After install: Sidebar → Apps → **Delivery time** → 3 tabs (Overview / Settings / List of shipping methods).
- Per-shipping-method: Settings → Shipping methods list — each row WITHOUT a carrier integration shows a small "Delivery days" link that opens the per-method schedule editor.

The app exposes four routes:

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.shipping_hours.overview` | `/admin/apps/shipping_hours` |
| Settings | `apps.shipping_hours.settings` | `/admin/apps/shipping_hours/settings` |
| List of shipping methods | `apps.shipping_hours.shipping_list` | `/admin/apps/shipping_hours/shipping-list` |
| Delivery days editor | `apps.shipping_hours.list` | `/admin/apps/shipping_hours/delivery_hours/:id` |

## What the merchant can do here

The Overview tab is the app's landing surface. From here the merchant navigates to the Settings tab ([[apps-shipping-hours-settings]]) for the two global settings and to the List of shipping methods tab ([[apps-shipping-hours-shipping-list]]) to attach a per-method schedule.

### What the merchant CANNOT do here
- Use Delivery time with a courier-integrated shipping method (Econt / Speedy / GLS / BoxNow / etc.). The "Delivery days" link only shows for non-integration shipping methods.
- Set per-customer windows — slots are global per method; the customer picks from what's available.
- Force a customer into a specific slot — they always pick from the available list.
- Track real-time courier availability — no GPS / dispatch integration. The merchant manages slot capacity manually via the per-slot **Orders limit** (see [[apps-shipping-hours-slots]]).
- Set per-slot pricing — slot capacity has no surcharge field. All slots of a method share the same shipping price.
- Send slot-reminder emails automatically — that's a notifications / CRM job, not handled by this app.

## Settings & fields

The Overview tab itself has no configurable fields — it is purely navigational. The configurable surfaces are:

- **Two global settings** (`interval`, `category`) on the Settings tab — see [[apps-shipping-hours-settings]].
- **Per-method schedules** (days + slots + exceptions) in the per-method editor — see [[apps-shipping-hours-slots]].

## Business rules

### Only available for non-courier shipping methods
The "Delivery days" link appears on a shipping-method row ONLY if that method has NO carrier integration. Configured-by-merchant flat-rate methods, Personal delivery, store-local pickup, and similar work. Courier integrations (Econt / Speedy / GLS / BoxNow / etc.) supply their own delivery scheduling and bypass this app entirely.

The technical mechanism behind this is the shipping provider's `has_delivery_dates` flag: the slot-list computation aborts (returns null) when `has_delivery_dates` is false. Courier integrations set this flag to false because they provide their own scheduling — see [[shipping-provider-lifecycle]].

### Install side effect — `action_after_add_to_cart` forced
On install, the app force-sets the store-level `action_after_add_to_cart` setting to `stay_on_page`. This is a global setting change the merchant should be aware of — it overrides whatever the merchant had configured (e.g. "go to cart"). Uninstalling does NOT restore the previous value.

### Paid app
Delivery time is a **paid app**: installing it opens a billing step (invoice details + payment method + an optional discount code, then **Pay now**) before the app activates — the standard paid-app install flow described on [[apps]]. The plan gate below applies on top.

### Plan gating
Listed under the plan feature key `shipping_hours` (the app's `APP_KEY`). The install URL `/admin/apps/shipping_hours/install` is blocked when the plan lacks the feature, and the app is hidden from the App Store for those plans. Existing installs keep working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]].

### Permission
Standard apps permission scope (`store.shipping`).

## Related

- [[apps-shipping-hours]] — hub.
- [[apps]] — App Store hub.
- [[shipping-provider-lifecycle]] — the `has_delivery_dates` provider flag behind the non-courier eligibility rule.
- [[settings-shipping]] — shipping methods list (where the "Delivery days" link appears).
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — `shipping_hours` plan gating.

## Open questions

_None — behavior captured above._
