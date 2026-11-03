---
type: feature
nav_path: "Apps → Stores Sync"
route_name: apps.stores-sync.overview
route_path: /admin/apps/stores-sync
aliases: ["Stores Sync", "Multi-store sync", "Multi-store catalog sync", "Quantity sync between stores", "enable disable button", "app active toggle"]
tags: [apps, administration, multi-store, sync]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 3
---
# Stores Sync (multi-store quantity synchronisation)

## Purpose

**Stores Sync** keeps stock levels in step across several CloudCart stores the same merchant owns. When a SKU's quantity changes on one store — an order, a manual edit, a return — the same SKU's quantity updates on every other participating store, in real time. Despite its name it syncs **`quantity` only**: not names, prices, images, categories, or customers.

It is used by merchants who run multiple separate CloudCart stores under one ownership (per-brand or per-country, via [[apps-stores]]) and need a shared, always-current stock count across them. It is different from [[apps-multilang]], which is for LANGUAGE variants within ONE store.

This topic is split into four aspect pages because each covers a distinct concept — the sync model, the automatic real-time path, the on-demand bulk path, and the API / conflict behaviour. The Assistant should drill into the aspect that matches the question, not read all four.

> **Has an on/off control.** The app screen carries an **Enable / Disable** button, so the merchant can switch it off without uninstalling it — a disabled app stops working while keeping its settings. The button is briefly absent while the screen is still loading its configuration; it appears once the settings arrive.

## Where to find it

Sidebar → Apps → install → **Stores Sync** → settings. Configuration (participating stores + match key + the Full sync button) lives on [[apps-stores-sync-settings]]. Stores Sync depends on the multi-store setup — see [[apps-stores]].

## What the merchant can do here

- Pick which of their own stores participate in the sync group, and the product field used to match SKUs across them — see [[apps-stores-sync-model]].
- Rely on stock changes propagating automatically between every participating store — see [[apps-stores-sync-realtime]].
- Trigger an on-demand full sync to populate a new group or reconcile drift — see [[apps-stores-sync-full-sync]].
- Drive per-store stock from an ERP/WMS via the API, and understand how conflicting edits resolve — see [[apps-stores-sync-api-conflicts]].

### What the merchant CANNOT do here

- Sync any field other than `quantity` (no names, prices, images, categories, customers, tags).
- Sync orders / payments — each store keeps its own.
- Use it without the multi-store concept — see [[apps-stores]].
- Designate a "master" store — the model is a peer mesh, see [[apps-stores-sync-model]].

## Sub-pages (in this cluster)

- [[apps-stores-sync-model]] — what syncs (`quantity` only) and between which stores: the N-way peer mesh (no master), `selectedSites`, the `compare_by` match key (sku / barcode / both-required fallback), the tracking-flag gate on both sides, per-site pricing independence, same-SKU collision handling.
- [[apps-stores-sync-realtime]] — the automatic per-variant sync: only a `quantity` dirty-flag fires it, the `import4` queue, the 180-second SLA, active-app-on-both-sides requirement, no backfill on re-activation, and the target-side search re-index.
- [[apps-stores-sync-full-sync]] — the on-demand **Full sync** button: 24-hour cooldown, 100-variant batch chunking, the live progress bar, supersede-cancel of an in-flight run, the `import6` queue, and scale/performance behaviour.
- [[apps-stores-sync-api-conflicts]] — programmatic per-store stock via [[api-store-quantity]] as an ERP path, plus conflict resolution: last-write-wins, no conflict log, audit only via each store's own Change log.

## Settings & fields

Two settings, both required, both configured on [[apps-stores-sync-settings]]:

- **`compare_by`** — the match key used to pair products across stores (`sku`, `barcode`, or a both-required fallback). Detailed on [[apps-stores-sync-model]].
- **`selectedSites`** — the array of participating store IDs (plural — any number). Detailed on [[apps-stores-sync-model]].

The settings page also hosts the **Full sync** button (with its 24-hour cooldown and progress bar) — see [[apps-stores-sync-full-sync]].

## Business rules

- **Only `quantity` syncs.** Prices, names, images, categories, and customers stay independent per store. See [[apps-stores-sync-model]].
- **Peer mesh, no master.** Every participating store syncs to every other; any edit on any store propagates everywhere. See [[apps-stores-sync-model]].
- **Both sides must have `tracking` ON** for a synced quantity to be honoured — see [[apps-stores-sync-model]] and [[inventory-tracking]].
- **Real-time fires only on a `quantity` change** — edits to SKU, barcode, price, name, or status do not propagate. See [[apps-stores-sync-realtime]].
- **The app must be ACTIVE on both sides;** deactivating stops sync from that store and re-activating does not backfill — reconcile with a Full sync. See [[apps-stores-sync-realtime]] + [[apps-stores-sync-full-sync]].
- **Conflicts settle last-write-wins, with no conflict log** — audit via each store's Change log. See [[apps-stores-sync-api-conflicts]].

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-stores-sync-settings]] — the settings screen (participating stores, match key, Full sync button).
- [[apps-stores]] — multi-store concept (Stores Sync depends on it).
- [[apps-multilang]] — different concept (multi-language sister sites within ONE store).
- [[api-store-quantity]] — per-store stock API (the primary ERP integration path).
- [[json-api-v2]] — API authentication, rate limits, side-effects principle.
- [[products-products]] — the catalog whose `quantity` is synced.
- [[inventory-tracking]] — the `tracking` master switch that gates sync.

## Open questions

None — uncertainties distributed to the aspect pages.
