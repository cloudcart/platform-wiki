---
type: feature
nav_path: "Apps → OLX → Sync behaviour"
route_name: apps.olx.configuration
route_path: /admin/apps/olx/configuration
aliases: ["OLX sync", "OLX stock sync", "OLX status sync", "OLX delete sync", "OLX price sync", "sync_quantity", "sync_status", "sync_delete"]
tags: [apps, olx, marketplace, sync, inventory, status]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# OLX — sync behaviour (stock / status / delete / price)

> Part of [[apps-olx]]. See the hub for the other aspects (connection, advert format, publishing).

## Purpose

How CloudCart product state propagates to OLX adverts after they're published. Three opt-in settings auto-mirror **stock**, **active/inactive status**, and **deletion**; price changes are the exception (manual re-sync only). This is the aspect to read for "my product sold out — why is the OLX advert still up?" and "I changed the price in CloudCart but OLX still shows the old one".

## Where to find it

Sidebar → Apps → OLX → **Configuration tab** for the auto-sync toggles ([[apps-olx-configuration]]), and the **Products tab** ([[apps-olx-products]]) for the manual bulk price re-sync action. Route: `/admin/apps/olx/configuration`.

## What the merchant can do here

- Turn on **stock auto-sync** (`sync_quantity`), **status auto-sync** (`sync_status`), and **delete auto-sync** (`sync_delete`).
- Manually trigger **bulk price re-sync** from the Products tab.
- Submit a **bulk publish** of several products at once.

## Settings & fields

| Setting | Effect when enabled |
|---|---|
| `sync_quantity` | OLX advert auto-deactivates when stock runs out; auto-reactivates when restocked. |
| `sync_status` | Marking the product Inactive deactivates the OLX advert; marking it Active reactivates it. |
| `sync_delete` | Deleting the CloudCart product auto-removes the linked OLX advert. |

Each is an independent toggle on [[apps-olx-configuration]]. With all off, adverts never change after publish except via manual actions.

## Business rules

### Stock auto-sync — advert auto-deactivates when the product runs out

When `sync_quantity` is enabled and a variant's quantity drops to 0 **with stock tracking on and "continue selling when out of stock" off**, the OLX advert is automatically deactivated. When the variant is restocked above 0, the advert is automatically reactivated. This is bound to the variant-update event. The conditions match the native inventory rules — see [[inventory-variant-model]] for the `tracking` / `continue_selling` master switches that decide whether stock-out even registers, and [[inventory-tracking]] for the overall model.

### Status auto-sync — product active/inactive mirrors to OLX

When `sync_status` is enabled, marking a product **Inactive** in CloudCart deactivates the OLX advert; marking it **Active** again reactivates the advert — but **only if its OLX status was `removed_by_user`**, not for adverts that an OLX moderator removed. A moderator-removed advert will not come back just by re-activating the product.

### Product delete auto-removes the OLX advert

When `sync_delete` is enabled and a CloudCart product is deleted, the linked OLX advert is automatically removed. **Without this setting, deleting a CloudCart product leaves the advert orphaned on OLX** — it stays live on the marketplace with no backing product.

### Price changes do NOT auto-sync — manual bulk re-sync only

Price changes do **not** propagate through the event subscriber. The merchant must explicitly push current CloudCart prices to OLX via the **bulk price re-sync** action on the Products tab (the `bulk.sync.price` action, reporting via `bulk_price.success`). This pushes current CloudCart prices to the corresponding OLX adverts. A merchant who edits prices in CloudCart and expects OLX to follow automatically will see stale prices until they run this.

### Bulk publish — per-product API calls inside one upload action

When the merchant selects multiple product IDs and submits them together, the platform loops the IDs and publishes each advert to OLX **one at a time**, returning a summary (`errors`, `uploaded`, `total`). So the merchant queues a bulk publish from one button, but OLX is hit per-product — partial success is normal, and the summary reports how many uploaded vs failed. See [[apps-olx-main-publishing]] for what causes individual failures.

## Related

- [[apps-olx]] — hub.
- [[apps-olx-configuration]] — Configuration tab where the sync toggles live.
- [[apps-olx-products]] — Products tab with the bulk price re-sync + bulk publish actions.
- [[apps-olx-history]] — operation log for sync results / failures.
- [[inventory-tracking]] — the native inventory model behind stock auto-sync.
- [[inventory-variant-model]] — the `tracking` + `continue_selling` switches that gate stock-out detection.

## Open questions

None.
