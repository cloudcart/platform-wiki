---
type: feature
nav_path: "Apps → Etsy → Sync mechanics"
route_name: apps.etsy.settings
route_path: /admin/apps/etsy
aliases: ["Etsy sync", "Etsy sync mechanics", "Etsy price sync", "Etsy quantity sync", "Etsy sync conflict", "Etsy currency conversion", "Etsy edit gate", "Etsy update_in_etsy", "Etsy background jobs", "Etsy request counter"]
tags: [apps, marketplace, etsy, sync, inventory, currency]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-etsy]]. See the hub for the other aspects (connection, listing config, variants + states).

# Etsy — sync mechanics (price, quantity, edits)

## Purpose

This aspect covers what actually moves between CloudCart and Etsy at runtime: the two-way price + quantity sync, the per-listing sync-scope picker, currency conversion, the lower-wins quantity-conflict rule, the edit-on-Etsy gate, image handling, and the listing-vs-inventory API split. It's the page to read for *"why did my CloudCart stock change"* or *"why isn't my Etsy listing updating"* tickets.

## Where to find it

There is no dedicated screen — the merchant controls sync via the per-listing *To be synchronize* setting on [[apps-etsy-listing-config]] and the **Sync** action (`action_sync`) on the listings tabs (see [[apps-etsy-variants-states]]). Route `/admin/apps/etsy` / `apps.etsy.settings`.

## What the merchant can do here

- Set a listing's sync scope: **Nothing** / **Price** / **Quantity** / **Price and quantity** (`listing.nothing_to_be_sync`, `listing.price_to_be_sync`, `listing.quantity_to_be_sync`, `listing.price_and_quantity_to_be_sync`).
- Trigger a manual **Sync** (`action_sync`) on a listing to push CloudCart changes to Etsy or reconcile.
- Decide whether CloudCart product edits propagate to Etsy automatically via the `update_in_etsy` gate (see Business rules).

### What the merchant CANNOT do here
- Get instant CloudCart-stock decrement at the moment of an Etsy sale — Etsy sales reflect only on the next sync run, not on the purchase event.
- Have CloudCart edits push to Etsy when `update_in_etsy` is OFF.

## Settings & fields

- **To be synchronize** (`listing.to_be_sync`) — per-listing scope picker; field lives in the per-product config on [[apps-etsy-listing-config]].
- **`update_in_etsy`** — the edit-on-Etsy gate (Business rules below).
- **`etsy_request`** — backend request counter (not shown in the UI).
- **Etsy currency** setting — holds the Etsy shop's currency; the store currency is the CloudCart side.

## Business rules

### Two-way real-time sync of price + quantity
*"The best thing is that all your Etsy and CloudCart product quantities and prices are synced in real time."* When stock changes on either side, both reflect (subject to the conflict rule below). The per-Variant stock model being updated is documented on [[inventory-tracking]].

### Per-listing sync scope
Each product's *To be synchronize* setting controls what auto-syncs:
- **Nothing** — manual control (no automated sync).
- **Price only** — quantity changes don't propagate.
- **Quantity only** — price stays manual.
- **Price and quantity** — full real-time sync.

### Currency conversion runs on every price sync
On every Etsy ↔ CloudCart price sync, the price is converted using the platform's currency helper. The Etsy currency setting holds the Etsy shop's currency; the store's currency is the CloudCart side. So an Etsy listing in USD syncs into CloudCart converted to BGN / EUR / whatever the store currency is at the time of the sync.

### Sync conflict — Etsy quantity wins when it's lower than CloudCart's
When reconciling, CloudCart compares Etsy's listing quantity against the CloudCart variant's quantity:
- If Etsy has MORE stock, CloudCart pushes its own number up to Etsy.
- If Etsy has LESS stock (typical after an Etsy sale), CloudCart adopts Etsy's lower value.

So Etsy sales decrement CloudCart inventory automatically — but only on the next sync run, not in real-time on the Etsy purchase event.

### Edit-on-Etsy gate — `update_in_etsy` setting
The product-edited event handler (fired when a CloudCart product is updated) only pushes the change to Etsy if `update_in_etsy` is true. When OFF, edits made to CloudCart products do not propagate to Etsy — the Etsy listing stays as-is, and the merchant has to manually re-sync from the Etsy tab.

### Image handling
- **Etsy → CloudCart**: when the merchant pulls an Etsy listing into CloudCart, the listing's images are fetched from Etsy and uploaded into CloudCart's media library — not hot-linked. The CloudCart product keeps its own image copies.
- **CloudCart → Etsy**: each image is uploaded to Etsy through CloudCart. There is no client-side resize / format validation before upload; if Etsy rejects an image as too small, the rejection comes back as an API error.

### Listing details and inventory are separate API calls
When updating a CloudCart product that already has an Etsy listing, two API calls are made — one for listing metadata (title, description, who_made, is_supply, when_made, shipping_template, state) and one for inventory (variants data). Failure of one does not roll back the other, so the merchant can end up with synced metadata but unsynced inventory if Etsy returns an error mid-flight.

### Request counter + rate limit
Every Etsy API call increments a counter stored in the `etsy_request` setting along with the function name — used for rate-limit observability (Etsy enforces 10 calls/sec). The merchant doesn't see this counter in the UI; it's a backend metric.

### Background jobs: categories, parameters, listings
The integration has three queue tasks — fetch Etsy's category tree, fetch category-specific parameters, and sync listings. The merchant triggers the categories / listings sync through the UI; the parameters fetch runs in response to category-mapping changes (see [[apps-etsy-listing-config]]).

## Related

- [[apps-etsy]] — hub.
- [[apps-etsy-listing-config]] — where the per-listing sync-scope field lives + parameter mapping.
- [[apps-etsy-variants-states]] — the Sync action button + how variant data is built for the inventory call.
- [[apps-etsy-connection]] — the OAuth connection these API calls authenticate with.
- [[inventory-tracking]] — the per-Variant stock model the quantity sync updates.
- [[products-products]] — the product whose edits the `update_in_etsy` gate governs.

## Open questions

- The exact sync-run cadence ("next sync run") and whether it is scheduled or event-driven for the quantity-conflict reconciliation is not pinned down in the source (verify).
