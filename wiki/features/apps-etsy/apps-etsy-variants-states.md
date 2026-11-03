---
type: feature
nav_path: "Apps → Etsy → Variants + states"
route_name: apps.etsy.settings
route_path: /admin/apps/etsy
aliases: ["Etsy variants", "Etsy variation properties", "Etsy listing states", "Etsy tabs", "Etsy listings from Etsy", "Etsy pull listings", "Etsy active draft expired", "Etsy listing state"]
tags: [apps, marketplace, etsy, variants, listings, states]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-etsy]]. See the hub for the other aspects (connection, listing config, sync mechanics).

# Etsy — variants, listing states + tabs

## Purpose

This aspect covers how CloudCart variants map onto Etsy's listing model, the full catalogue of Etsy listing states, the management tabs that surface them, and the "Listings from Etsy" pull that brings existing Etsy inventory into the CloudCart catalog. It's the page for *"why is my listing showing as Expired"* or *"how do my colour/size variants appear on Etsy"* tickets.

## Where to find it

Sidebar → **Apps** → **Etsy** → the listings management UI (tabs) and the *Listings from Etsy* tab. Route `/admin/apps/etsy` / `apps.etsy.settings`.

## What the merchant can do here

### Listings tabs (management UI)
| Tab | What it shows |
|---|---|
| **Active** (`listings.active`) | Live Etsy listings. |
| **Drafts** (`listings.drafts`) | Draft listings not yet published. |
| **Inactive** (`listings.inactive`) | Disabled listings. |
| **Expired** (`listings.expired`) | Expired listings (Etsy listings expire after a period and need renewal — see [[apps-etsy-listing-config]]). |

### Per-listing actions
- **Upload listing in Etsy** (`action.add.listing`).
- **Add your first listing in Etsy** (`action.add_first_listing`).
- **View product in Etsy** (`action.view_in_etsy`).
- **Sync** (`action_sync`) — triggers the runtime sync on [[apps-etsy-sync-mechanics]]; also used to re-publish an expired listing.

### Listings from Etsy (`save_listings_from_etsy`)
- Tab showing products pulled FROM Etsy.
- *"Your products from Etsy will be shown here"* (`notify.no_listings_from_etsy_info`).
- *"You do not have this type of products in Etsy"* (`notify.no_listings_from_etsy_yet`).
- The merchant can save Etsy listings into the CloudCart catalog (images are downloaded into the media library — see [[apps-etsy-sync-mechanics]]).

### What the merchant CANNOT do here
- Map a CloudCart variant manually to a specific Etsy product — the mapping is automatic (see Business rules).
- Push a product with more than three variation axes (Etsy's cap).

## Settings & fields

### Etsy listing states (`listing.state.*`)
| State | Meaning |
|---|---|
| `active` | Live and purchasable. |
| `draft` | Drafted, not published. |
| `edit` | Inactive (paused by merchant). |
| `expired` | Expired listing — past its Etsy validity window. |
| `private` | Private (only with direct link). |
| `sold_out` | Out of stock. |
| `unavailable` | Removed by Etsy admin. |
| `is_active` | Filter: *"Add products with 'Active' status"*. |
| `update_in_etsy` | Apply product changes on Etsy (the edit gate — see [[apps-etsy-sync-mechanics]]). |

## Business rules

### Variants — one CloudCart variant maps to one Etsy "product" inside an Etsy listing
Each CloudCart variant becomes a separate "product" inside an Etsy listing's Inventory. Up to **three** variant property axes are supported, matching Etsy's max of three variation properties per listing. The mapping is automatic — the merchant does not pick which Etsy product corresponds to which CloudCart variant. The structural [[variant|Variant]] model behind this is documented on [[variants-model]].

### Three-state listing publish — Active or Draft selected globally
When pushing a product, the integration sets the listing state to `active` or `draft` based on the global `listing_is_active` setting. There is no per-product override. Merchants who want to review listings before they go live keep this setting OFF (everything pushes as draft) and manually activate from the Etsy seller dashboard.

### Listing states are pulled by separate API methods per state
Each Etsy listing state (active / inactive / draft / expired) is fetched via a DIFFERENT Etsy API method. The merchant's tab UI maps to these methods; any unrecognised state defaults to the "active" fetch.

### Expired listings — re-publish via Sync
Expired listings surface in the **Expired** tab. Re-publishing requires a manual **Sync**; there is no scheduled auto-renew (this avoids accidental Etsy listing fees — see [[apps-etsy-listing-config]]).

## Related

- [[apps-etsy]] — hub.
- [[apps-etsy-sync-mechanics]] — the Sync action + how variant inventory data is pushed.
- [[apps-etsy-listing-config]] — listing expiry, eligibility, and the per-listing metadata.
- [[apps-etsy-connection]] — the OAuth connection the pull / push depend on.
- [[variant]] — the CloudCart Variant entity mapped to Etsy products.
- [[variants-model]] — the Parameter / Option / Variant hierarchy behind the three Etsy axes.
- [[products-products]] — catalog destination for pulled Etsy listings.

## Open questions

- Whether the `edit` state (paused) and the **Inactive** tab map one-to-one across all Etsy API responses is not fully confirmed in the source (verify).
