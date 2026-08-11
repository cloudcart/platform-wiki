---
type: feature
nav_path: "Apps → R-Keeper → Behaviour modes"
route_name: apps.rkeeper.overview
route_path: /admin/apps/rkeeper
aliases: ["R-Keeper sync modes", "Rkeeper behaviour modes", "R-Keeper order export trigger", "R-Keeper delivery method", "Rkeeper sync only", "R-Keeper personal delivery vs Glovo"]
tags: [apps, erp, restaurant, sync, behaviour]
plan_gates: []
created: 2026-06-16
updated: 2026-06-16
source_count: 1
---

> Part of [[apps-rkeeper]]. See the hub for credentials, the tab layout, the full per-setting reference, the order-push dispatch matrix, and the two-stage payment push.

# R-Keeper — behaviour modes

## Purpose

R-Keeper is not one on/off integration. Its settings form **independent axes**, and a store's actual behaviour is the *combination* of the choices on each. This page is the behavioural model — how the settings combine into "what syncs, in which direction, when, and how orders are delivered". The per-setting reference (where each field lives, its defaults, the dispatch matrix) is on the hub [[apps-rkeeper]].

Inbound (catalogue / stock) and outbound (orders) are configured, and behave, independently — choosing one does not gate the other.

## Where to find it

All of these are on **Sidebar → Apps → R-Keeper → Settings** (`/admin/apps/rkeeper`). R-Keeper requires the [[apps-store-locations|Store Locations]] app first — each R-Keeper object (restaurant) links to a CloudCart store location.

## What the merchant can do here

Pick the behaviour along each axis independently:

- **Inbound** — whether R-Keeper creates products in CloudCart or only refreshes them.
- **Outbound** — when a placed order is pushed to R-Keeper.
- **Delivery** — whether the restaurant delivers itself or hands off to Glovo.
- **Location** — which R-Keeper object feeds the store, and how its payment methods map back.

## Settings & fields

### Inbound — catalogue / stock (R-Keeper → CloudCart)

Set by **Action mode** (`action`):

- **Import and Sync** — R-Keeper's catalogue is *created* in CloudCart (new products land in the chosen default category) and kept synced.
- **Sync only** — no new products; the CloudCart catalogue is kept and only refreshed.

Modifiers: **product matching** pairs a CloudCart identifier (`compare_by` — ID / SKU / Barcode) with an R-Keeper identifier (`compare_rkeeper` — ID / Code); **`qty_default`** sets a fallback stock applied regardless of the per-product quantity-tracking switch; **`default_category`** (required only when Action = Import) is where new products land.

### Outbound — order export (CloudCart → R-Keeper)

Set by the **Order export trigger** (`send_order`), **independent of the inbound axis** — four options:

- **New Order** — on order creation.
- **Sent** — when a fulfilment is added.
- **Paid** — when the order status becomes `paid`.
- **Order complete** — when the order status becomes `completed`.

An order is pushed **at most once** (an `rkeeper_order_id` marker suppresses duplicate sends). Separately, an order that already reached R-Keeper and then becomes paid/completed pushes its **payment details in a second stage**, so R-Keeper learns of the order and the payment in two steps. There is **no master pause toggle and no close-order setting** (unlike Barsy).

### Delivery — `delivery_type`

- **Personal delivery** — the restaurant delivers itself.
- **Delivery with Glovo** — orders are forwarded to [[apps-glovo|Glovo]] for last-mile (requires the Glovo app configured with locations).

### Location & payment mapping

Each R-Keeper object (restaurant location) is linked to a CloudCart store location (needs [[apps-store-locations]]); the merchant picks which object feeds products. R-Keeper payment methods are mapped to CloudCart [[settings-payment-providers|payment providers]] so synced orders carry the right payment.

## Business rules

The axes do not gate each other:

- Choosing **Sync only** does **not** stop orders exporting.
- The **delivery method** does not change the inbound/outbound behaviour — it only routes fulfilment.
- The order trigger fires regardless of whether the catalogue is imported or sync-only.

So a store's behaviour is the *product* of the choices, for example:

| Inbound | Outbound | Delivery | Resulting behaviour |
|---|---|---|---|
| Import and Sync | New Order | Glovo | "R-Keeper owns the menu; every new order goes to R-Keeper at once and ships via Glovo." |
| Sync only | Paid | Personal | "Keep my CloudCart menu, just refresh it, and push each order to R-Keeper when it's paid; I deliver myself." |
| Import and Sync | Order complete | Personal | "R-Keeper owns the menu; push orders only once they're completed." |

Catalogue / stock pulls run every **8 hours**; order pushes fire on the chosen event.

## Related

- [[apps-rkeeper]] — hub: credentials, tabs, per-setting reference, dispatch matrix, two-stage payment push.
- [[apps-store-locations]] — required prerequisite; each R-Keeper object ↔ a CloudCart store location.
- [[apps-glovo]] — last-mile when the Glovo delivery method is chosen.
- [[food-restaurant-grocery]] — restaurant / hospitality concept hub.
- [[erp-integrations]] — ERP category; the shared catalogue / stock / order sync model.
- [[order-processing-pipeline]] — the order events that fire the outbound push.

## Open questions

_None._
