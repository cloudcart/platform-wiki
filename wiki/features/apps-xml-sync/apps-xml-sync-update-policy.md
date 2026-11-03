---
type: feature
nav_path: "Apps → XML Sync → Update policy"
route_name: apps.xml_sync
route_path: /admin/apps/xml_sync (per-task update policy)
aliases: ["XML Sync update policy", "XML Sync per-field update", "XML Sync stock-only mode", "XML Sync product_map", "XML Sync multi-feed", "XML Sync last sync wins", "XML Sync image refresh", "XML Sync URL hash"]
tags: [apps, imports, xml, sync, recurring, update-policy, matching]
plan_gates: ["xml_sync_limit"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-xml-sync]]. See the hub for the other aspects (job pipeline, discontinued handling, fetch transport, side effects).

# XML Sync — update policy

## Purpose

On each recurring run, the supplier feed and the CloudCart catalog will disagree about some fields. The **update policy** decides which fields the sync is allowed to overwrite, how an existing product is matched to a feed row, what happens when two feeds touch the same product, and how images are refreshed. This is what lets a merchant keep supplier-owned data (price, stock) in sync while protecting merchant-curated data (descriptions, custom images).

## Where to find it

- The per-field **Update checkboxes** live in [[apps-xml-sync-step2]] (the field-mapping step). Each mapped field has a checkbox controlling whether re-syncs overwrite that field.
- The matching column (`product_map`) is chosen on Step 1 of the wizard (the first screen).
- Multi-feed linkage is configured on Step 1 when the merchant has more than one task.

## What the merchant can do here

- Choose, per field, whether a re-sync **overwrites** the existing value or leaves it alone — the basis of "stock-only mode".
- Pick the column used to match feed rows to existing products: `sku`, `barcode`, or `id`.
- Run several sync tasks against the same catalog (subject to `xml_sync_limit` — see [[apps-xml-sync-settings]]).

What the merchant **cannot** do here:

- Set per-percentage "only update if delta < N%" guards as a built-in rule — the platform's native control is the per-field on/off Update checkbox, not a threshold-based policy. _(verify: percentage-delta guards are not exposed in the standard wizard.)_
- Get automatic conflict resolution between two feeds touching the same product — see "last sync wins" below.

## Settings & fields

| Control | Where | Effect |
|---------|-------|--------|
| Per-field Update checkbox | [[apps-xml-sync-step2]] | When checked, re-syncs overwrite that field; when unchecked, the field is set on first import only and never touched again. |
| `product_map` | Step 1 | The single column used to match a feed row to an existing product — `sku`, `barcode`, or `id`. |
| `updatable` | derived | A task is `updatable = 1` if at least one field has its Update checkbox set; this is also a precondition for the recurring re-parse gate (see [[apps-xml-sync-job-pipeline]]). |

## Business rules

### Per-field update policy (the basis of "stock-only mode")

Each mapped field carries its own Update checkbox. When the feed says price = 10.50 BGN for SKU X and CloudCart has 10.00 BGN, the **price field's checkbox** decides whether the sync overwrites. The same per-field logic applies to name, description, image, stock, and every other mapped field.

The common **stock-only mode**: the merchant checks Update only on price + stock and leaves it unchecked on name / description / images. Result — supplier price and quantity stay in sync on every run while descriptions stay merchant-curated and are never clobbered. This is the most-requested sync configuration.

### Matching by a single configurable column (`product_map`)

Each task matches feed rows to existing products by **one** column — `product_map` — chosen on Step 1: `sku`, `barcode`, or `id`. There is no composite / multi-key matching; the merchant picks one identifier and the whole task keys off it.

### Multi-feed merge: last sync wins, no conflict detection

When two sync tasks reference the **same** product (same `product_map` value), the **task that runs second overwrites the fields written by the task that ran first**. There is no merge, no "supplier priority", and no "no-touch column" mechanic between tasks — whichever sync finishes most recently wins. Merchants running multiple feeds against an overlapping catalog should ensure the feeds cover disjoint products, or accept that the later-running feed is authoritative. (For scoping *deactivation* across feeds, see [[apps-xml-sync-discontinued]].)

### Image refresh: compares URL hashes, not content

On each sync the platform computes a hash over the **URL strings** from the feed and compares the set against the URL hashes recorded on the product's existing images (stored under the `url_image` integration metadata). If the URL set is **unchanged, no re-download** happens ("Images unchanged, skipping replacement"). If the URLs differ, **all** existing image rows are deleted and the new URLs are re-downloaded.

There is **no checksum against image content** — rotating the same image at a new URL forces a full re-download even when the bytes are identical, and replacing image bytes at the same URL is NOT detected (the hash is over URLs, not pixels). Image fields also obey the per-field Update checkbox: if Update is unchecked for images, the URL-hash comparison never runs.

## Related

- [[apps-xml-sync]] — hub.
- [[apps-xml-sync-step2]] — where the per-field Update checkboxes live.
- [[apps-xml-sync-discontinued]] — what happens to products missing from the feed (the other half of "what a run changes").
- [[apps-xml-sync-job-pipeline]] — the `updatable` gate that depends on at least one Update checkbox being set.
- [[apps-xml-import-mapping-fields]] — the sibling import's mapping model (fields + variant patterns).
- [[products-products]] — products updated by the policy.
- [[products-change-log]] — every field change is auditable here.

## Open questions

_None._
