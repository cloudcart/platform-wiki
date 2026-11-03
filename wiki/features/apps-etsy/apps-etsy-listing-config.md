---
type: feature
nav_path: "Apps → Etsy → Listing config"
route_name: apps.etsy.settings
route_path: /admin/apps/etsy
aliases: ["Etsy listing config", "Etsy category", "Etsy who_made", "Etsy when_made", "Etsy is_supply", "Etsy parameter mapping", "Etsy shipping template", "Etsy eligibility", "Etsy listing fees", "Etsy listing expiry"]
tags: [apps, marketplace, etsy, listings, parameters, shipping]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-etsy]]. See the hub for the other aspects (connection, sync mechanics, variants + states).

# Etsy — per-listing config + parameter mapping

## Purpose

Etsy requires structured metadata per listing that CloudCart products don't carry natively — a category from Etsy's taxonomy, who/when the item was made, whether it's a craft supply, mapped attributes, and a shipping template. This aspect covers everything the merchant configures **before** a product can be pushed, plus the eligibility pre-filter, listing expiry, and Etsy's listing fees.

## Where to find it

Sidebar → **Apps** → **Etsy** → *Choose listings to upload* and the per-product config view (`action.choose_listings`, `action.map_parameters`). Route `/admin/apps/etsy` / `apps.etsy.settings`.

## What the merchant can do here

### Choose listings to upload (`action.choose_listings`)
*"Choose the products you want to upload in Etsy. Note that they are pre-filtered by us to meet the Etsy's requirements."* — CloudCart auto-filters products that don't meet Etsy's listing requirements (e.g. requires a specific category, image, weight).

### Per-listing setup before upload
The merchant configures Etsy-specific data per product:
- **Category in Etsy** (`category`) — Etsy's required category taxonomy.
- **Year of production** (`listing.when_made`):
  - Made before 1700 (`listing.made_before_1700`).
  - Made before 1998 (`listing.made_before_1998`).
  - (Other Etsy year ranges.)
- **The products are produced by** (`listing.who_made`):
  - By me (`listing.made_by_me`).
  - By someone else (`listing.made_by_someone_else`).
  - Collectively (`listing.collective_made`).
- **Made to order** (`listing.made_to_order`) — yes/no.
- **All of the products are suppliable** (`listing.is_supply`) — Etsy's "supply" flag for craft materials.
- **To be synchronize** (`listing.to_be_sync`) — sets the per-listing sync scope; mechanics on [[apps-etsy-sync-mechanics]].

### Parameters synchronization (Header: "Synchronization", `action.map_parameters`)
*"Synchronize product's parameters with Etsy"* — maps CloudCart property fields to Etsy attribute fields per product. Failure modes:
- *"Please, synchronize your product parameters with those in Etsy"* (`err.params_not_mapped`).
- *"One Etsy parameter is associated with more than one from store"* (`err.same_params_mapping`).

### Etsy shipping template selection
**Choose an Etsy shipping template** (`shipping_templates`) — the merchant picks from their pre-configured Etsy shipping templates which one applies to the synced listings.

### What the merchant CANNOT do here
- Sync products that don't meet Etsy's requirements (CloudCart pre-filters; ineligible products are hidden).
- Bypass parameter-mapping if Etsy requires parameters for the chosen category (`err.params_not_mapped`).
- Map one CloudCart parameter to multiple Etsy parameters (`err.same_params_mapping`).
- Set a **per-listing** shipping template — the template is chosen globally per shop (see Business rules).

## Settings & fields

The per-product metadata fields are listed above. Validation surfaces through the error keys catalogued on [[apps-etsy-connection]] (`err.category_not_choosen`, `err.params_not_mapped`, `err.same_params_mapping`).

## Business rules

### Pre-filter eligibility
CloudCart filters out products that don't meet Etsy's requirements (e.g. missing weight, ineligible category, restricted material). Only eligible products appear in the *Choose listings to upload* view.

### Shipping template — one selection per shop, applied to every synced listing
The merchant picks ONE Etsy shipping template in the connection settings, and every listing created via this integration uses that template. There is no per-listing override — to use different templates, the merchant has to switch the global setting before each push.

### Listing expiry handled by Etsy — CloudCart only surfaces the state
CloudCart stores Etsy's listing expiry timestamp and surfaces expired listings in the **Expired** tab (see [[apps-etsy-variants-states]]). Etsy listings expire periodically (typically 4 months). Re-publishing requires the merchant to click Sync — there is no scheduled auto-renew, which avoids accidental Etsy listing fees.

### Etsy listing fees are NOT surfaced in CloudCart
There is no warning or disclaimer about Etsy's per-listing fees ($0.20 USD at the time of writing) anywhere in the integration. Each push to Etsy creates a real listing on Etsy's side and incurs Etsy's standard fees. The merchant has to understand Etsy's pricing model independently.

## Related

- [[apps-etsy]] — hub.
- [[apps-etsy-connection]] — the connection + error-key reference.
- [[apps-etsy-sync-mechanics]] — what the per-listing sync-scope setting controls at runtime.
- [[apps-etsy-variants-states]] — the Expired tab where expiry surfaces; variant attribute axes.
- [[products-property]] — the CloudCart properties that map to Etsy attributes.
- [[products-products]] — the product source for pushed listings.

## Open questions

- The exact set of Etsy requirements the pre-filter enforces (weight / category / material) is not fully enumerated in the source (verify).
