---
type: feature
nav_path: "Apps → XML Sync → Update policy"
route_name: apps.xml_sync
route_path: /admin/apps/xml_sync (per-task update policy)
aliases: ["XML Sync update policy", "XML Sync per-field update", "XML Sync stock-only mode", "XML Sync product_map", "XML Sync multi-feed", "XML Sync last sync wins", "XML Sync image refresh", "XML Sync URL hash", "Update for existing", "XML Sync delta threshold"]
tags: [apps, imports, xml, sync, recurring, update-policy, matching]
plan_gates: ["xml_sync_limit"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[apps-xml-sync]]. See the hub for the other aspects (job pipeline, discontinued handling, fetch transport, side effects).

# XML Sync — update policy

## Purpose

On each recurring run, the supplier feed and the CloudCart catalog will disagree about some fields. The **update policy** decides which fields the sync is allowed to overwrite, how an existing product is matched to a feed row, and what happens when two feeds touch the same product. This is what lets a merchant keep supplier-owned data (stock, and price if wanted) in sync while protecting values they manage themselves.

## Where to find it

- The per-field **Update checkboxes** live in [[apps-xml-sync-step2]] (the field-mapping step). Each mapped field has a checkbox controlling whether re-syncs overwrite that field.
- The matching column (`product_map`) is chosen on Step 1 of the wizard (the first screen).
- Multi-feed linkage is configured on Step 1 when the merchant has more than one task.

## What the merchant can do here

- Choose, per field, whether a re-sync **overwrites** the existing value or leaves it alone — the basis of "stock-only mode".
- Pick the column used to match feed rows to existing products: `sku`, `barcode`, or `id`.
- Run several sync tasks against the same catalog (subject to `xml_sync_limit` — see [[apps-xml-sync-settings]]).

What the merchant **cannot** do here:

- Set a percentage guard ("only update if the change is under N%") or any other per-field policy — none exists. Each field's Update checkbox is simply on or off, so a bad feed value on a checked field is written as-is.
- Get automatic conflict resolution between two feeds touching the same product — see "last sync wins" below.

## Settings & fields

| Control | Where | Effect |
|---------|-------|--------|
| Per-field **Update for existing** checkbox | [[apps-xml-sync-step2]] | Checked by default. When checked, each run writes the feed's value if it differs from the current one; when unchecked, the sync never changes that field. |
| `product_map` | Step 1 | The single column used to match a feed row to an existing product — `sku`, `barcode`, or `id`. |
| `updatable` | derived on Step 2 save | A precondition for the recurring re-parse gate (see [[apps-xml-sync-job-pipeline]]). The current wizard sends every updatable field, checked or not, so a saved task is normally marked updatable even with every box unchecked (verify). |

## Business rules

### Per-field update policy (the basis of "stock-only mode")

Each field the sync can change carries its own Update checkbox. When the feed says price = 10.50 EUR for SKU X and CloudCart has 10.00 EUR, the **price field's checkbox** decides whether the sync overwrites. The same applies to every field XML Sync maps: price, discounted price, quantity, minimum order quantity, status and (with the Stores app) per-store quantity. Names, descriptions and images are not part of XML Sync's mapping, so a sync never changes them.

The common **stock-only mode**: the merchant leaves Update checked only on quantity and unchecks price and status. Result — supplier stock stays in sync on every run while the merchant's own prices and visibility are never overwritten. Quantity is written even to variants whose inventory tracking is off (it then has no storefront effect until tracking is on); bundles are skipped, and only the first variant matching a feed item is updated.

### Matching by a single configurable column (`product_map`)

Each task matches feed rows to existing products by **one** column — `product_map` — chosen on Step 1: `sku`, `barcode`, or `id`. There is no composite / multi-key matching; the merchant picks one identifier and the whole task keys off it.

### Multi-feed merge: last sync wins, no conflict detection

When two sync tasks reference the **same** product (same `product_map` value), the **task that runs second overwrites the fields written by the task that ran first**. There is no merge, no "supplier priority", and no "no-touch column" mechanic between tasks — whichever sync finishes most recently wins. Merchants running multiple feeds against an overlapping catalog should ensure the feeds cover disjoint products, or accept that the later-running feed is authoritative. (For scoping *deactivation* across feeds, see [[apps-xml-sync-discontinued]].)

### Images are not synced

XML Sync's mapping has no image field, so a sync run never downloads, replaces or deletes product images. Images that came from [[apps-xml-import]] are refreshed by that app, and only when its image field's Update checkbox is on: it compares the feed's image URLs with those recorded on the product's images and, only if the set of URLs changed, deletes all of them and downloads the new ones. The comparison is over URLs, not file content: new bytes at the same URL are not picked up, and the same picture at a new URL is downloaded again.

## Related

- [[apps-xml-sync]] — hub.
- [[apps-xml-sync-step2]] — where the per-field Update checkboxes live.
- [[apps-xml-sync-discontinued]] — what happens to products missing from the feed (the other half of "what a run changes").
- [[apps-xml-sync-job-pipeline]] — the `updatable` re-parse gate.
- [[apps-xml-import-mapping-fields]] — the sibling import's mapping model (fields + variant patterns).
- [[products-products]] — products updated by the policy.
- [[products-change-log]] — every field change is auditable here.

## Open questions

_None._
