---
type: feature
nav_path: "Apps → Stores Sync → Sync model"
route_name: apps.stores-sync.overview
route_path: /admin/apps/stores-sync
aliases: ["Stores Sync model", "Multi-store sync mesh", "Stores Sync N-way mesh", "Stores Sync compare_by", "Stores Sync selectedSites"]
tags: [apps, administration, multi-store, sync]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-stores-sync]]. See the hub for the other aspects (real-time sync, full sync, API + conflicts).

# Stores Sync — the sync model (what syncs, between which stores)

## Purpose

This page answers the two questions every merchant asks first about Stores Sync: **which stores participate** and **what data actually crosses between them**. The short answer: Stores Sync is a **fully-connected mesh of selected stores** that synchronises **one thing only — `quantity`**. It is not a catalog-replication tool and it has no "master" store.

## Where to find it

Sidebar → Apps → install → **Stores Sync** → settings. The participating-stores list and match-key picker live on [[apps-stores-sync-settings]]. Stores Sync depends on the multi-store concept — see [[apps-stores]].

## What the merchant can do here

- Pick which of their own CloudCart stores participate in the sync group (`selectedSites`).
- Choose the canonical match key used to pair products across stores (`compare_by`).
- Rely on stock changes propagating automatically between every participating store.

### What the merchant CANNOT do here

- Sync product names, descriptions, prices, images, categories, customers, or tags — **only `quantity` syncs**.
- Sync orders / payments (each store keeps its own orders).
- Use Stores Sync without the multi-store setup — see [[apps-stores]].
- Designate a "master" store — there isn't one (see Business rules).

## Settings & fields

Two settings are required for the integration to function:

| Setting | Meaning |
|---|---|
| `compare_by` | Comparison key — how the platform matches products across stores. Accepts `sku`, `barcode`, or anything-else (fallback). |
| `selectedSites` | Array of site IDs that participate in this sync network. **Plural** — the group can be any number of the merchant's stores. |

### `compare_by` drives the match key

- `sku` — match variants by SKU.
- `barcode` — match variants by barcode.
- *(anything else)* — fall back to **both** SKU **and** barcode: both must be set and both must match exactly on the target side for the sync to apply.

If a variant has no value in the chosen match field, the sync simply **skips it** — the platform never falls back to name-matching. The choice is global per store, not per-product. So variants with only one of SKU/barcode are skipped when the merchant left `compare_by` on the both-required fallback.

## Business rules

### What actually syncs: `quantity` only

Despite the wider wording in the help text, the sync writes exactly one column on the target variant: **`quantity`**. The translation header confirms it — *"CloudCart quantity sync"* — and the help text reads *"This app will sync products quantities between all of your stores in real time"*. Merchants who need full-catalog cross-store sync should not expect that here; they still maintain catalog data store-by-store. Stores Sync only solves *"when a customer buys at store A, the same SKU's stock drops at store B"*.

### N-way mesh, not master / slave

`selectedSites` is plural, and the platform creates **every directed pair** between the current site and the selected ones, plus every pair among the selected sites themselves. With 3 sites in the group that is 6 (= 3 × 2) directional pairs — a fully connected mesh. There is **no "master" / "canonical" store**; any edit on any participating site propagates to every other participating site.

The site that **uninstalls** the app is removed from the mesh. Disabling the app on a site has the same runtime effect — the sync job ends early when the active check is false. (Re-activation does not backfill missed updates; see [[apps-stores-sync-realtime]].)

### Tracking flag must be ON on both sides

The sync writes `quantity` only when **both** sides have the product's `tracking` flag set to true. If a store has tracking off for that product (manual stock entry), the synced quantity is ignored on that side. This deliberately prevents the sync from clobbering stores that intentionally don't track stock. See [[inventory-tracking]] for the `tracking` master switch.

### Per-site pricing is unaffected

Because only `quantity` syncs, prices stay fully independent per store. The merchant can set BGN 100 on store A and BGN 90 on store B for the same SKU without the sync overriding anything. The same independence holds for names, descriptions, images, and categories.

### Same-SKU collision on the target side

When the same SKU already exists on the target site (created manually or pre-existing), the sync **updates** the existing variant's quantity. There is no "merge or error" prompt — the platform always tries to update the matching row. If multiple variants on the target share the same SKU, only the **first hit** is updated.

### Permission

Standard apps permission scope.

## Related

- [[apps-stores-sync]] — hub.
- [[apps-stores-sync-settings]] — the settings screen where `compare_by` + `selectedSites` are configured.
- [[apps-stores]] — multi-store concept (Stores Sync depends on it).
- [[apps-multilang]] — different concept (multi-language sister sites within ONE store).
- [[inventory-tracking]] — the `tracking` master switch that gates whether a synced quantity is honoured.
- [[products-products]] — the catalog whose `quantity` is synced.

## Open questions

None.
