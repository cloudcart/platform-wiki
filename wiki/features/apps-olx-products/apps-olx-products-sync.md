---
type: feature
nav_path: "Apps → OLX → Products → Sync"
route_name: apps.olx.products
route_path: /admin/apps/olx/products
aliases: ["OLX sync", "OLX stock sync", "OLX status sync", "OLX price sync", "OLX advert lifecycle", "OLX re-publish expired"]
tags: [apps, olx, marketplace, products, sync]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# OLX → Products — sync & advert lifecycle

> Part of [[apps-olx-products]]. See the hub for the other aspects (pipeline UI, validation, payload formatting).

## Purpose

This aspect covers **how a live OLX advert stays in step with its CloudCart product over time** — automatic stock / status / delete sync, the manual price re-sync, the per-row Sync action, the advert's finite lifetime on OLX, and why re-publishing an expired advert is a manual step.

## Where to find it

The Products tab (`/admin/apps/olx/products`) exposes the **Sync prices** bulk action and a per-row **Sync** action. The auto-sync behaviours below are driven by the toggles on [[apps-olx-settings]] (`sync_quantity`, `sync_status`, `sync_delete`), not by the table itself.

## What the merchant can do here

- Trigger **Sync prices** (bulk) to push current CloudCart prices to the linked OLX adverts.
- Use the per-row **Sync** action to re-format and push a single product's full advert payload to OLX.
- Toggle an advert's Active / Pending status from the **Status** column.
- Re-publish / re-sync an expired advert manually.

## Settings & fields

The sync toggles live on [[apps-olx-settings]]:

| Setting | Label | Effect |
|---|---|---|
| `sync_quantity` | `label.sync.qty` — "Stock synchronization" | Variant stock changes auto-deactivate / reactivate the advert. |
| `sync_status` | `config.sync.status` — "Status synchronization" | Product Active / Inactive toggle mirrors to the advert. |
| `sync_delete` | (delete sync) | Deleting the CloudCart product auto-removes the OLX advert. |

## Business rules

### Stock auto-sync — out-of-stock auto-deactivates the advert

When `sync_quantity` is enabled, variant updates fire the OLX event subscriber. If the variant's quantity becomes 0 (with stock tracking on and "continue selling when out of stock" off — see [[inventory-variant-model]] and [[inventory-oversell]]), the linked OLX advert is auto-deactivated. When stock returns above 0, the advert is auto-reactivated.

### Status auto-sync — product visibility mirrors to OLX

When `sync_status` is enabled, marking a product Inactive deactivates the advert; marking it Active reactivates it — but **only if** OLX previously had the advert as `removed_by_user` (not for adverts removed by an OLX moderator).

### Delete auto-sync — deleting the product removes the advert

When `sync_delete` is enabled and a CloudCart product is deleted, the linked OLX advert is automatically removed. Without this setting, deleting a CloudCart product leaves the advert orphaned on OLX.

### Price changes do NOT auto-sync

There is no listener for price-only changes. Price updates require either: (a) the **Sync prices** bulk action (pushes current CloudCart prices to OLX), or (b) the per-row **Sync** action, which re-formats the full advert payload (including current price) and pushes it. Promo-price precedence is documented on [[apps-olx-products-formatting]].

### Per-row Sync uses OLX's current category, not CloudCart's mapping

The per-row Sync action fetches the advert from OLX, reads OLX's current `category_id`, then re-formats the CloudCart product against THAT category (overriding CloudCart's mapping). This handles the case where the merchant changed the advert's category manually on OLX. If the categories differ, CloudCart updates the local Advert record's category to match OLX.

### Adverts have a finite lifetime

OLX adverts expire (typically after 30 days). After expiry the **Status** field updates to Expired and the merchant can re-publish from the Products tab.

### Re-publishing an expired advert is manual

There is **no** scheduled job that re-publishes adverts before their OLX expiry date. When an advert expires the merchant must refresh / re-sync from the Products tab manually — and neither the per-row Sync action nor the **Sync prices** bulk action triggers a full re-publish of an expired advert. Each expired advert must be re-published one by one; there is no "Bulk re-publish all expired" toggle.

### Failure surfaces in History

When a sync or publish operation fails, the API call + OLX error response is recorded in [[apps-olx-history]]. The merchant drills into History to see exactly what went wrong.

### Permission

Standard apps permission scope.

## Related

- [[apps-olx-products]] — hub.
- [[apps-olx]] — OLX feature hub.
- [[apps-olx-settings]] — the `sync_quantity` / `sync_status` / `sync_delete` toggles.
- [[apps-olx-history]] — where sync failures surface.
- [[inventory-variant-model]] — per-variant stock + the tracking master switch behind stock sync.
- [[inventory-oversell]] — "continue selling when out of stock" flag that gates auto-deactivation.
- [[products-products]] — source CloudCart products.

## Open questions

- Whether advert expiry length varies by OLX country / paid promotion (BG vs RO) (verify).
