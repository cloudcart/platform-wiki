---
type: feature
nav_path: "Apps → OLX → Adverts"
route_name: apps.olx.download
route_path: /admin/apps/olx/adverts
aliases: ["OLX Adverts", "OLX live listings", "OLX adverts download"]
tags: [apps, olx, marketplace, adverts, live-listings]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 2
---
# OLX → Adverts

## Purpose

The **Adverts** tab is the LIVE view of what the merchant has on OLX right now — the OLX-side inventory pulled back from OLX's API. It is the opposite data flow from [[apps-olx-products]] (the OUTGOING pipeline that publishes CloudCart products to OLX): the Products tab reads from CloudCart, the Adverts tab reads from OLX. This is why the route is internally named "download" — its job is to surface OLX adverts that aren't yet tracked locally and pull them into CloudCart. For the full OLX feature set, see [[apps-olx]].

Used by the merchant to:
- Audit what's actually visible on OLX (compare against expected).
- See adverts created OUTSIDE of CloudCart (manually added on OLX).
- Download (import) existing OLX adverts into CloudCart for management.

## Where to find it

Sidebar → Apps → OLX → **Adverts tab**. Route: `/admin/apps/olx/adverts` (route name `apps.olx.download`). The same data-table UI as the Products tab, in "adverts" mode against a different data source.

## What the merchant can do here

### View live OLX adverts

Standard data table, fetched straight from OLX on each load. Columns:

| Column | Notes |
|---|---|
| **Advert title** | OLX-side title (may differ from the CloudCart product name if edited on OLX). |
| **OLX status** | See status values under Settings & fields. |
| **Created on OLX** | Date the advert was created (expiry date also returned). |
| **OLX URL** | Click-through to the public OLX listing. |
| **Linked CloudCart product** | Shown when the advert maps to a CloudCart product; otherwise "Unmapped". |

### Download to store (import an OLX advert)

The merchant clicks **Download** on an advert → CloudCart creates a new **inactive (draft)** product using the OLX advert's title, description, price and images. Images are downloaded from the OLX URLs into CloudCart's media library. Requires the `download_category` setting — a default CloudCart category assigned to incoming OLX-imported products (set in [[apps-olx-configuration]]). After import, future CloudCart-side updates can propagate to the OLX advert.

### Sync a row back to OLX

Per-row **Sync** re-pushes the CloudCart product to OLX. See Business rules — this can silently overwrite OLX-side edits and re-map the category.

### Per-advert statistics

The merchant can request OLX-side metrics (views, calls, etc.) for **one advert at a time**. There is no bulk metrics dashboard and no aggregated KPIs.

### Activate / deactivate an advert

The merchant can toggle an advert active/inactive directly on OLX (status-update action, route `apps.olx.products.product.update.status`). This is a direct OLX command — no re-formatting, no full re-publish, and no OLX fee. Useful for temporarily hiding an advert without deleting it.

### What the merchant CANNOT do here
- Bulk-edit advert content — edits happen on the source CloudCart product (then Sync) or on OLX directly.
- Create new adverts — that is [[apps-olx-products]]' job.
- Delete OLX adverts from this view without confirmation.

## Settings & fields

### Adverts list (per-advert fields)

Each OLX advert record returns: OLX advert ID, title, description, price, category, status, created date, expiry date, and the public OLX URL. (Whether a view count is returned: verify.)

### Status values (surfaced 1:1 from OLX)

`new` / `active` / `limited` / `outdated` / `unconfirmed` / `unpaid` / `moderated` / `blocked` / `disabled` / `removed_by_user` / `removed_by_moderator`. An advert that no longer exists on OLX (deleted there) shows as `removed`.

### Pagination

Offset-based, defaulting to **25 per page**; the merchant can change the page size via the `perpage` query parameter.

### `download_category`

Default CloudCart category applied to products imported via **Download to store**. Configured in [[apps-olx-configuration]].

### Permission

Standard apps permission scope.

## Business rules

### OLX is the source of truth for advert state

The Adverts tab READS from OLX on every page load — there is no local caching layer. If OLX rejects an advert, removes it for policy reasons, or it expires, the merchant sees the current state HERE, not in [[apps-olx-products]].

### Already-imported adverts are filtered out

The list excludes adverts already tracked locally — only OLX adverts not yet imported into CloudCart appear here. This prevents re-importing what is already linked.

### Discrepancy between Products and Adverts tabs

Products tab = CloudCart's outgoing pipeline. Adverts tab = OLX's current live state. When they diverge (e.g. 100 products published but only 80 active on OLX because 20 expired), the merchant compares the two and investigates via [[apps-olx-history]].

### Sync silently overwrites OLX-side manual edits

When the merchant triggers **Sync** on an advert, the platform re-formats the current CloudCart product into a fresh OLX payload and pushes it. Anything edited directly on OLX (title, description, price, photos) is replaced by the current CloudCart values. There is **no pre-sync confirmation or warning** — the overwrite is immediate. To preserve OLX-side edits, the merchant must first mirror them onto the CloudCart product.

### Sync can re-map the category from OLX

During Sync the platform first reads the advert's **current OLX category**, formats the push using that OLX category (not the CloudCart category mapping), and if it differs, updates the CloudCart record's category to match. This silent category re-sync is unique to the Adverts tab.

### Deleted-on-OLX adverts show as `removed` and are not auto-cleaned

When CloudCart asks OLX for an advert that no longer exists, the entry is marked `removed` and flagged deleted. CloudCart does NOT auto-clean these orphaned rows — the merchant must manually delete or re-publish.

### Side effects of refresh

A read-only API call to OLX. No customer-side or cart-side impact.

## Related

- [[apps-olx]] — OLX hub.
- [[apps-olx-products]] — outgoing publishing pipeline.
- [[apps-olx-configuration]] — category mapping (incl. `download_category`).
- [[apps-olx-history]] — operation log (refresh + per-advert errors).

## Open questions

- Whether a per-advert view count is returned in the adverts list payload.
- Precedence rules when CloudCart Sync and OLX-side edits conflict beyond the documented "Sync wins" behavior.
