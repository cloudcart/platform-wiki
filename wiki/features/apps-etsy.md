---
type: feature
nav_path: "Apps → Etsy"
route_name: apps.etsy.settings
route_path: /admin/apps/etsy
aliases: ["Etsy", "Sale on Etsy", "Etsy marketplace", "Etsy sync"]
tags: [apps, marketplace, etsy, sync, two-way, handmade]
plan_gates: ["etsy", "etsy_total_products"]
created: 2026-05-22
updated: 2026-06-10
source_count: 1
---
# Etsy (marketplace sync)

## Purpose

**Etsy** integration — **two-way sync** between CloudCart and the merchant's **Etsy shop**. Unlike the competitor-migration apps [[apps-magento]] / [[apps-shopify]] / [[apps-woocommerce]] (one-way import), Etsy keeps an ongoing connection in both directions:

- **Push CloudCart products → Etsy** as listings (with Etsy-specific filtering + parameter mapping).
- **Pull Etsy products → CloudCart** to surface existing Etsy inventory in the CloudCart catalog.
- **Real-time sync** of price + quantity between the two platforms.
- **Per-listing state management** (Active / Draft / Inactive / Expired / Private / Sold out / Unavailable).
- **Etsy shipping template** selection per synced listing.

Used by merchants whose primary store is on CloudCart but who also want Etsy's reach for handmade / vintage / craft goods. The integration uses **Etsy's API** (OAuth-based) and is **not endorsed or certified by Etsy** — see the trademark note on [[apps-etsy-connection]].

## Where to find it

Sidebar → **Apps** → install → **Etsy** (titled *"Sale on Etsy"*). The route is `/admin/apps/etsy` / `apps.etsy.settings`.

Sub-views: install, config, listings (CloudCart-side), listings from Etsy, add listing, map parameters, not-available, tabs.

## What the merchant can do here

- **Connect** a CloudCart store to an Etsy shop via OAuth, and pick one Etsy shop when the account has several — [[apps-etsy-connection]].
- **Choose CloudCart products to push** to Etsy (pre-filtered to Etsy's eligibility requirements) and set per-listing Etsy metadata — category, who/when made, supply flag, shipping template — [[apps-etsy-listing-config]].
- **Map CloudCart product parameters** to Etsy attributes per category — [[apps-etsy-listing-config]].
- **Pull existing Etsy listings into CloudCart** and save them as catalog products — [[apps-etsy-variants-states]].
- **Control what auto-syncs** per listing (nothing / price / quantity / both) and let Etsy sales decrement CloudCart stock on the next sync — [[apps-etsy-sync-mechanics]].
- **Manage listing state** via Active / Drafts / Inactive / Expired tabs and re-publish expired listings — [[apps-etsy-variants-states]].

### What the merchant CANNOT do here

- Sync products that don't meet Etsy's requirements (CloudCart pre-filters; ineligible products are hidden) — [[apps-etsy-listing-config]].
- Sync without OAuth-connecting an Etsy account first (`err.settings_not_saved` until connected) — [[apps-etsy-connection]].
- Bypass parameter-mapping when Etsy requires parameters for the chosen category (`err.params_not_mapped`) — [[apps-etsy-listing-config]].
- Map one CloudCart parameter to multiple Etsy parameters (`err.same_params_mapping`).
- Sync more than one Etsy shop per CloudCart store, or use a per-listing shipping-template / publish-state override — those are global — [[apps-etsy-connection]] / [[apps-etsy-listing-config]].

## Sub-pages (in this cluster)

This integration is split into 4 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the support question, not read every page.

- [[apps-etsy-connection]] — OAuth connect flow, multi-shop selection, the Settings form fields, the password-label leftover, the error-message reference, trademark disclaimer, plan gates.
- [[apps-etsy-listing-config]] — per-listing Etsy metadata (category, when_made, who_made, made_to_order, is_supply), parameter mapping, shipping-template selection, eligibility pre-filter, listing expiry, Etsy listing fees.
- [[apps-etsy-sync-mechanics]] — push/pull data flow, per-listing sync scope (nothing/price/quantity/both), currency conversion, the lower-wins quantity-conflict rule, the edit-on-Etsy gate, image handling, the listing-vs-inventory API split, the request counter + background jobs.
- [[apps-etsy-variants-states]] — CloudCart variant ↔ Etsy "product" mapping (max 3 axes), the listing-state catalogue + management tabs, pulling listings from Etsy, per-state API fetch methods.

## Settings & fields

The connection form, dropdowns, and the full error-key reference are documented on [[apps-etsy-connection]]. The per-product Etsy metadata fields (category, who/when made, supply, sync scope) are on [[apps-etsy-listing-config]].

## Business rules

The full business-rules catalogue is distributed across the aspect pages:

- **Authentication + multi-shop** (OAuth only, one shop per store) → [[apps-etsy-connection]].
- **Eligibility pre-filter, parameter mapping, shipping template, listing expiry, Etsy fees** → [[apps-etsy-listing-config]].
- **Two-way real-time price+quantity sync, per-listing scope, lower-wins conflict rule, edit gate** → [[apps-etsy-sync-mechanics]].
- **Variant mapping (max 3 axes), listing states + tabs** → [[apps-etsy-variants-states]].
- **Permission** — standard apps scope.

## Related

- [[apps]] — App Store hub.
- [[apps-magento]] / [[apps-shopify]] / [[apps-woocommerce]] — sister competitor integrations (those are one-way migrations; Etsy is two-way ongoing sync).
- [[apps-olx]] — sister marketplace integration (similar two-way sync pattern).
- [[apps-tiktok-shop]] — sister marketplace integration (TikTok Shop).
- [[apps-google-shopping]] — sister marketplace integration (Google Shopping feed).
- [[products-products]] — product source / destination.
- [[products-property]] — parameter mapping references properties.
- [[inventory-tracking]] — the per-Variant stock model the price+quantity sync updates.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — the `etsy` + `etsy_total_products` gates.

## Open questions

- Behaviour on plan downgrade (existing installs continue until cancel) follows the general rule in [[plan-vs-feature-pack]]; not separately verified for Etsy.
