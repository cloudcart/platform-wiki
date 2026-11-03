---
type: feature
nav_path: "Apps → Stores Sync → Settings"
route_name: apps.stores-sync.settings
route_path: /admin/apps/stores-sync/settings
aliases: ["Stores Sync Settings", "Multi-store sync config", "CloudCart quantity sync"]
tags: [apps, administration, stores-sync, multi-store, settings]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 2
---
# Stores Sync → Settings

## Purpose

The **Settings** tab configures **product-quantity synchronisation** across the merchant's own CloudCart stores. The app keeps stock quantities identical across stores in real time. The install screen states it plainly: *"This app will sync products quantities between all of your stores in real time."* It syncs **only quantity** — no prices, names, translations, categories, or other fields. See [[apps-stores-sync]] for the full feature set.

## Where to find it

Sidebar → Apps → Stores Sync → **Settings tab**. Route: `/admin/apps/stores-sync/settings`.

## What the merchant can do here

- **Pick the match key** (`compare_by`) used to identify the same variant across stores.
- **Pick which of their own stores join the sync mesh** (`selectedSites`).
- **Enable / disable the app** for the whole mesh with one toggle.
- **Trigger a Full sync** to re-push all quantities (subject to a 24-hour cooldown), with a live progress bar.

### What the merchant CANNOT do here
- Use without [[apps-stores]] (multi-store concept dependency).
- Pick which **entities** sync — there is no products / categories / customers selector. Only quantity syncs.
- Sync prices, currencies, names, or translations — these stay independent per store.
- Add another person's CloudCart store. Only stores owned by the same account appear.

## Settings & fields

| Field | Key | Required | Notes |
|---|---|---|---|
| **Compare by** | `compare_by` | when activating | Match key for finding the same variant across stores. Values: `sku`, `barcode`, or both. Validation: *"Compare by is required"*. |
| **Choose all the stores that you wish to be synchronized** | `selectedSites` | when activating | Multi-select of the merchant's other CloudCart stores (sites under the same account, current site excluded). Each option shows the store's primary domain. Validation: *"Selected sites is required"* / *"Selected sites must be an array"*. |
| **Enable app** | `active` | — | Master toggle, labelled *"Enable app (global for all stores that are in the synchronization)"*. Toggling once applies to every store in the mesh in real time. |

`compare_by` and `selectedSites` are validated only when activating (`required_if:active,1`). The merchant can save the app deactivated (`active = 0`) with empty config — useful for pre-configuring or clearing settings without errors.

## Business rules

### Bi-directional N-way sync — no master / slave
Every store reads from and writes to every other store; there is no master-vs-slave distinction. Saving builds a directional link for every ordered pair of stores in the mesh (n × (n−1) links for n stores). A quantity change on any store propagates to all others.

### Which variants actually sync
There is no per-product opt-in/opt-out. At runtime the platform syncs a variant only when:
- the variant has a non-empty value in the `compare_by` field, AND
- **both** the source and target sides have stock tracking turned **on**. Variants with tracking off are skipped — this protects manually-managed inventory from being overwritten.

### Prices stay independent
Only the `quantity` field is written. Per-store prices, currencies, names, and translations are never touched, so merchants can run different prices per store with no sync conflict.

### Excluding a store
The settings page warns: *"WARNING! All stores below will synchronize their quantities in real time. Disabling and Enabling the app from the 'Enable app' button will be applied in real time to all the stores that are included in the sync. If you wish to exclude a store from the process, you need to uninstall the app from that store or you could manually remove it from the settings in one of the other stores."* So a store leaves the mesh either by uninstalling the app on it, or by removing its id from `selectedSites` on any other store.

### Save is atomic
Saving replaces the entire mesh in one transaction: old links are removed and the fresh full mesh is written. If any step fails the whole save rolls back, leaving the previous valid mesh in place. Errors return HTTP 400 with a generic "Unexpected error" message.

### Full sync, progress, and the 24-hour cooldown
The **Full sync** button queues one background task per variant and runs them as a batch with a live progress bar (showing total / pending / completed / percent / cancelled). Regular admins can trigger a full sync **once every 24 hours**; until the cooldown elapses the button reads *"Full synchronization for {app} can be started after {date}."* The cooldown is **global per app instance** — if any admin on the store triggered a full sync within 24h, every admin sees the lock. The last-full-sync time is stored in UTC. CloudCart support, logged in via the support console, can trigger Full sync at any cadence (the cooldown is skipped for the duration of the console session). Real-time delta sync is never affected by the cooldown — only the bulk re-sync trigger is capped.

## Related

- [[apps-stores-sync]] — hub.
- [[apps-stores]] — multi-store concept.
- [[apps-multilang]] — DIFFERENT concept (multi-language sister sites, not multi-store); shares the same same-account ownership rule for linking stores.
- [[products-products]] — the catalog whose quantities are synced.

## Open questions

- Exact behaviour when `compare_by` is set to "both" and `sku` matches one variant while `barcode` matches another.
