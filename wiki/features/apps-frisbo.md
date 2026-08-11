---
type: feature
nav_path: "Apps → Frisbo"
route_name: apps.frisbo.overview
route_path: /admin/apps/frisbo
aliases: ["Frisbo", "Frisbo fulfillment", "Frisbo 3PL", "enable disable button", "app active toggle"]
tags: [apps, administration, fulfillment, 3pl, logistics]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 2
---
# Frisbo (3PL fulfillment center)

## Purpose

Connects CloudCart to **Frisbo**, a Romanian third-party-logistics (3PL) provider that handles warehousing, picking, packing, and shipping for e-commerce merchants. Orders placed on the storefront can be sent to Frisbo for fulfilment, so the merchant doesn't touch physical inventory. For merchants who want to outsource warehousing + shipping, scale without their own logistics, or offer same-/next-day shipping in Frisbo's regions. Requires a Frisbo merchant contract.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it. A disabled app stops working while keeping its settings — so *"the app is disabled"* IS a valid explanation to check here.

## Where to find it

Sidebar → Apps → install → **Frisbo**. Three tabs:

| Tab | Route | Purpose |
|-----|-------|---------|
| Overview | `apps.frisbo.overview` → `/admin/apps/frisbo` | App status. |
| Settings | `apps.frisbo.settings` → `/admin/apps/frisbo/settings` | Credentials + organisation scope + automation ([[apps-frisbo-settings]]). |
| Orders | `apps.frisbo.orders` → `/admin/apps/frisbo/orders` | Orders pushed to Frisbo + their response ([[apps-frisbo-orders]]). |

## What the merchant can do here

- Connect Frisbo with **email + password** and pick the Organisation / Warehouse / Channel scope.
- Send an order to Frisbo for fulfilment — manually, or automatically (see [[apps-frisbo-settings]]).
- View, per order, whether the push succeeded or the error it returned.

**Cannot do here:** use Frisbo without a Frisbo contract; receive returns or inbound stock (that lives in Frisbo's portal); cancel an already-pushed order reliably (see Business rules).

## Settings & fields

Authentication is **email + password** (not OAuth). On each API call the platform checks the stored token expiry; if it has passed, it re-authenticates with the email + password to get a fresh access token (a full re-auth each time, not a refresh-token flow). The password is held in CloudCart's encrypted settings.

Allowed settings keys: `email`, `password`, `organization_id`, `warehouse_id`, `channel_id`, `automate_send`, `order_status`, `create_products`. The Settings tab shows three cards:

**Connect** — `email` + `password`. The save button validates the pair before storing. Once valid, the card switches to slide-edit (the merchant must open it to change credentials).

**Organisation scope** (hidden until credentials are saved) — three searchable dropdowns:
- **Organization** — loads from `/admin/api/frisbo/organizations`. Selecting a new organisation **clears** `warehouse_id` and `channel_id` (cascading reset).
- **Warehouse** — loads from `/admin/api/frisbo/warehouses/<organization_id>`. Disabled until an organisation is chosen.
- **Channel** — loads from `/admin/api/frisbo/channels/<organization_id>`. Disabled until an organisation is chosen.

**Order automation** (hidden until credentials are saved):
- **Automatic order dispatch** (`automate_send`, switch, `1` / `0`, default off).
- **Sending an order with status** (`order_status`, select) — shown only when `automate_send = 1`. Options: "New order" / "Paid".
- A **Create products in Frisbo** field (`create_products`) exists in code but is not currently rendered.

The configured check requires only `email` + `password` to be non-empty; the other keys are persisted but not part of that gate.

## Business rules

**3PL outsourced fulfilment.** Frisbo holds the stock. Flow: CloudCart creates the order normally → the merchant (or the auto-trigger) sends it to Frisbo → Frisbo picks, packs, and ships → Frisbo reports tracking + delivery status.

**Auto-send trigger.** When `automate_send = 1`, the order is pushed automatically in two cases: (1) the order is created, and (2) the status changes to "paid" **and** `order_status = 'paid'` is configured. Other statuses (e.g. `completed`) are not supported as triggers — for those the merchant pushes manually. When `automate_send = 0` (default), every push is manual.

**Push is fire-and-forget.** Each push writes the result to the order's single `frisbo_response` meta field: `Success send order`, or the error message on failure. No per-attempt history (each push overwrites) and no automatic retry — the merchant clicks Send again to retry. The push carries the configured `organization_id`.

**Cancel is unreliable.** The app's cancel action is deprecated and behaves identically to a normal send (it re-pushes the order, then deletes the `frisbo_response` meta) — it does not call a real cancel endpoint. In-flight cancellations must be coordinated manually with Frisbo support, and once Frisbo has shipped, cancellation may not be possible. The Cancel-at-Frisbo button is therefore hidden in the Orders tab.

**Outbound only — no inventory sync back.** The integration only pushes orders out. It can query Frisbo for stock on demand, but nothing pulls Frisbo's stock counts **into** CloudCart's product quantities — those stay merchant-managed. Returns, inbound stock receipt, and inventory adjustments live in Frisbo's portal, not in CloudCart.

**No scheduled jobs.** Frisbo runs no recurring/cron sync — it never polls Frisbo for stock or status. It is purely event-driven (push on order-created or on status change to "paid").

**No conflict with shipping apps.** Frisbo can run alongside Econt, Speedy, etc. It is a fulfilment back-end, not a checkout courier provider. The order's chosen courier stays separate; sending the order to Frisbo triggers Frisbo's own couriering (Frisbo picks the courier). Frisbo therefore replaces normal waybill generation for fulfilled orders ([[orders-shipping-waybill]]).

**Fees not surfaced.** Per-order Frisbo fulfilment fees appear only in Frisbo's own portal/invoice; CloudCart's admin does not display them.

## Orders tab

A standard data table of orders pushed to Frisbo, sorted `id desc`, with a **Customer** filter (autocomplete via `/admin/api/core/customers/autocomplete`). Columns: **Order** (`Order #<id> ({increment_hash})`, links to `/admin/orders/details/<id>`), **Created at**, **Frisbo response** (`Success send order` or the latest error text), and **Actions** (only the **Send to Frisbo** button). There is no Status, Categories, Processed-products, Import-history, or Tasks tab — Frisbo is push-only with no product or stock sync.

## Related

- [[fulfillment-and-warehouse]] — fulfillment & warehouse hub.
- [[apps]] — App Store.
- [[apps-frisbo-settings]] — settings sub-page.
- [[apps-frisbo-orders]] — orders status.
- [[orders]] — orders source.
- [[orders-shipping-waybill]] — Frisbo replaces normal waybill generation for fulfilled orders.
- [[products-inventory]] — Frisbo-stocked items; stock does not auto-sync back here.
- [[apps-pick-and-pack]] — alternative IN-HOUSE warehouse app.

## Open questions

- Whether the unrendered `create_products` field will be wired up to auto-create missing products in Frisbo.
