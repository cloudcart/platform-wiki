---
type: feature
nav_path: "Apps → Local Pickup (Stores) → shipping & payment"
route_name: apps.stores.overview
route_path: /admin/apps/stores
aliases: ["Local Pickup shipping method", "Pay on place", "Click-and-Collect", "Pickup payment", "Public stores page"]
tags: [apps, stores, local-pickup, shipping, payment, click-and-collect, storefront]
plan_gates: ["stores"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Local Pickup — shipping & payment methods

## Purpose

> Part of [[apps-stores]]. See the hub for the other aspects (managing locations, per-store stock).

Documents what installing the Local Pickup app **plugs into the storefront**: a new **Local Pickup** shipping method, a new **Pay on place** payment method, and an auto-generated public stores page. Together these let a customer choose to collect at a physical store and pay cash on pickup — or, combined with online payment, build a true Click-and-Collect flow.

## Where to find it

The methods are created automatically on install (Sidebar → Apps → install → **Local Pickup**). After install:

- The **Local Pickup** shipping method appears in [[shipping]] config.
- The **Pay on place** payment method appears in [[settings-payment-providers]].
- The public stores page is reachable on the storefront (per-store pages at `/stores/<handle>`).

## What the merchant can do here

- Offer **Local Pickup** as a checkout shipping method (customer picks a specific store from the list).
- Offer **Pay on place** (cash on pickup at the chosen store).
- Combine Local Pickup shipping with any existing online payment method to offer Click-and-Collect (pay online, collect in store).

### What the merchant CANNOT do here
- Use Local Pickup without these methods being auto-installed — the app installs them.
- Configure courier-based shipping here — Local Pickup is for collection at the merchant's own physical locations only.
- Edit the public stores page layout — it's auto-generated.

## Settings & fields

The app installs, per the install description (`info.install`):

- A new shipping method called **Local Pickup** (`action.depending_on_marketplace`: "Add shipping: Local Pickup"). It is configured like any other method in [[shipping]] — per-store shipping rates are keyed on the store id (see [[apps-stores-main-locations]] for the delete cascade).
- A new payment method called **Pay on place**, configured in [[settings-payment-providers]].
- A new public page listing all physical locations with Working hours, Address, Email, Telephone, Google Map.

There are no dedicated configuration fields beyond what the standard shipping / payment screens expose.

## Business rules

### Auto-installs the shipping + payment methods

When the app installs, the platform auto-creates the Local Pickup shipping method and the Pay on place payment method. They are standard methods afterward — the merchant manages them from the normal [[shipping]] and [[settings-payment-providers]] screens.

### Auto-creates the public stores page

The storefront gains a new public page listing all **active** physical stores with a Google Map (derived from each store's GPS coordinates — see [[apps-stores-main-locations]]). No design work is needed by the merchant; the page is auto-generated.

### Click-and-Collect: shipping and payment are independent

"Pay on place" is one payment method created by this app. Other payment methods (online card, PayPal, etc.) still apply — the merchant can build true Click-and-Collect (pay online, pick up later) by allowing Local Pickup shipping with any online payment method. There is **no** built-in "Pay-online-pickup-in-store" mode flag — it is just the combination of Local Pickup shipping + the merchant's existing online payment.

### Pickup eligibility depends on per-store stock

A customer can only select Local Pickup for a store that has the product in stock at that location. The eligibility check is part of the per-store stock model — see [[apps-stores-main-stock]] for how the platform blocks the selection when the chosen store has zero quantity.

## Related

- [[apps-stores]] — hub.
- [[shipping]] — Local Pickup appears here as a shipping method.
- [[settings-payment-providers]] — Pay on place appears here as a payment method.
- [[apps-store-locations]] — multi-warehouse inventory routing (different concept; affects online shipping, not pickup).

## Open questions

None.
