---
type: feature
nav_path: "Apps → Stores Sync → API & conflict resolution"
route_name: apps.stores-sync.overview
route_path: /admin/apps/stores-sync
aliases: ["Stores Sync API", "Stores Sync ERP integration", "Stores Sync conflict resolution", "Stores Sync last-write-wins", "Per-store stock API"]
tags: [apps, administration, multi-store, sync, api]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-stores-sync]]. See the hub for the other aspects (sync model, real-time sync, full sync).

# Stores Sync — programmatic access & conflict resolution

## Purpose

This page covers two related concerns for merchants running an external system of record (ERP / WMS) alongside Stores Sync: **the per-store stock API** as an alternative or complement to the app, and **how conflicting quantity edits resolve** when several sources write the same SKU. The headline rule is **last-write-wins, with no conflict log**.

## Where to find it

The API is driven externally, not from a screen — see [[api-store-quantity]] for the endpoint and [[json-api-v2]] for authentication, rate limits, and the side-effects principle. The app side lives at Sidebar → Apps → Stores Sync → settings ([[apps-stores-sync-settings]]).

## What the merchant can do here

- Drive per-warehouse / per-store stock directly through the API from an ERP or WMS.
- Let the API and the Stores Sync app's built-in replication coexist on the same stores.
- Reconstruct who changed a quantity by consulting each store's own product Change log.

### What the merchant CANNOT do here

- Expect a merchant-visible conflict-resolution UI — there isn't one.
- Find a conflict log on the Stores Sync app itself — conflicts are not recorded there.

## Settings & fields

This aspect has no settings of its own. API behaviour is governed by [[api-store-quantity]] (the `(shop_id, product_id, variant_id)` triple and its uniqueness rule) and the app's `compare_by` / `selectedSites` settings on [[apps-stores-sync-settings]].

## Business rules

### The per-store stock API is the primary ERP path

The per-store stock API is the **primary use case** for external inventory tools. ERP systems sync per-warehouse stock through [[api-store-quantity]] — full CRUD on the `(shop_id, product_id, variant_id)` triple. Uniqueness on the triple is enforced server-side; attempts to create a duplicate row return a validation error rather than silently overwriting.

The Stores Sync app's built-in N-way real-time replication still runs in parallel — but for **one-way pushes** from an external system of record, driving [[api-store-quantity]] directly is often simpler than orchestrating the app's mesh syncs. Both can coexist; just be mindful of last-write-wins ordering **across the two channels** (the API write and the app's mesh sync both land on the same `quantity`).

### Conflict resolution = last-write-wins

There is **no** merchant-visible conflict-resolution UI. Because every edit propagates to every participating store and the only synced field is `quantity` (see [[apps-stores-sync-model]]), the resulting value on each store is simply *"the last edit that arrived wins"*. Two near-simultaneous edits on different stores produce a transient flicker as each propagates, then settle on whichever update reaches each target last. The platform does **not** snapshot the previous value, does **not** log a conflict, and does **not** notify the merchant.

### No conflict-log persistence

When two near-simultaneous edits hit the same SKU from different sites, the last-write-wins outcome is correct but the platform writes **no log entry recording the conflict**. Audit-conscious merchants who need to reconstruct "who changed the quantity to what" must consult the **per-site product Change log** ([[products-change-log]] / [[orders-history]]) on **each store separately** — not on the Stores Sync app itself. Every quantity change (auto-decrement, manual edit, import, ERP/API write, mesh sync) is recorded there with timestamp + Initiator; see [[inventory-debugging-playbook]] for the diagnostic workflow.

## Related

- [[apps-stores-sync]] — hub.
- [[api-store-quantity]] — the per-store stock API (the primary ERP integration path).
- [[json-api-v2]] — API authentication, rate limits, side-effects principle.
- [[apps-stores-sync-model]] — quantity-only scope + the match-key rule that conflicts settle on.
- [[apps-stores-sync-settings]] — `compare_by` + `selectedSites`.
- [[products-change-log]] — per-store audit trail for quantity changes.
- [[orders-history]] — per-store order/product history.
- [[inventory-debugging-playbook]] — the "stock changed and we didn't change it" investigation.

## Open questions

None.
