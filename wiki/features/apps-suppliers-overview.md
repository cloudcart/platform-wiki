---
type: feature
nav_path: "Apps → Suppliers → Overview"
route_name: apps.suppliers.overview
route_path: /admin/apps/suppliers/overview
aliases: ["Suppliers Overview", "Suppliers hub", "Supplier list"]
tags: [apps, administration, suppliers, overview]
plan_gates: []
created: 2026-05-21
updated: 2026-05-28
source_count: 1
---
# Suppliers → Overview

## Purpose

The **Overview** page for the Suppliers app — shows installation state, capability summary, and navigates to the actual supplier list (the management UI lives at `/admin/suppliers` per the legacy URL).

The Suppliers app adds **per-product supplier tracking** + the cross-order [[orders-supplier-products]] aggregation view. Used by merchants who buy from multiple suppliers and want to:
- Track per-supplier costs.
- Run drop-shipping flows (orders trigger purchase from supplier).
- Generate purchase orders from order demand.
- Compare supplier prices for same SKUs.

For the full Suppliers feature set, see [[apps-suppliers]].

## Where to find it

Sidebar → Apps → Suppliers → **Overview**. Route: `/admin/apps/suppliers/overview` (route name `apps.suppliers.overview`). The default landing for `/admin/apps/suppliers` is the Suppliers list (`apps.suppliers.settings`).

## What the merchant can do here

- See install state + capabilities.
- Trigger Install / Uninstall.
- Click through to the legacy `/admin/suppliers` to manage actual supplier records.
- Read help text: capability list of what the app enables.

### What the merchant CANNOT do here
- Add suppliers directly — that's `/admin/suppliers` (legacy URL) OR [[apps-suppliers-supplier-products]].
- Configure per-supplier settings — done in the legacy supplier-edit form.

## Settings & fields

This view is install-state / metadata + navigation aid. No editable fields.

## Business rules

### Installation enables related features

When Suppliers is installed:
- Sidebar gains a Suppliers section (linked to `/admin/suppliers`).
- Products gain a per-product Suppliers tab in the editor.
- [[orders-supplier-products]] becomes accessible.
- The Suppliers filter on [[orders]] list appears.

### Permission
Standard apps permission scope.

## Related

- [[fulfillment-and-warehouse]] — fulfillment & warehouse hub.
- [[apps-suppliers]] — Suppliers hub with full feature set.
- [[apps-suppliers-supplier-products]] — per-supplier product mapping view.
- [[orders-supplier-products]] — cross-order supplier aggregation.
- [[products-products]] — products gain Suppliers section after install.
- [[orders]] — Suppliers filter on the orders list.

## How it works (verified against backend)

### Install description (what the merchant sees on the App Store card)

The Overview page renders the Suppliers install description shown on the App Store card. As shipped it reads:

> - Add your suppliers
> - Set specific suppliers to specific products
> - Compare the product`s delivery price to the one in your store

So the value proposition is positioned around three points: maintain a supplier directory, attach suppliers to products, and compare cost against the storefront price.

### "Add supplier" + "Add product to this supplier" CTAs

The supplier list is empty by default — the empty-state copy reads *"You have not added any suppliers yet"* / *"Your suppliers will show up here"*. The merchant uses **Add supplier** to create a record (`name`, `email`, `phone`, address). Once a supplier exists, the per-supplier products view shows *"You don't have products from this supplier"* / *"Your products for that supplier will show up here"* until the merchant uses **Add product to this supplier**.

### Overview is a redirect target

The Overview route exists primarily as the App Store entry. Once installed, the actual management lives at the per-supplier product table (see [[apps-suppliers-supplier-products]]) — clicking deeper from the Overview lands the merchant there.

### App's direct URL is `/suppliers` (not `/apps/suppliers`)
The app's direct link points to `suppliers` — when the merchant clicks the Suppliers tile in the App Store, they land at the legacy `/admin/suppliers` URL, not at `/admin/apps/suppliers`. The Overview route exists separately for App Store metadata display.

### Per-product module renders ONLY when app is installed
The product editor conditionally renders the **Suppliers** block: when the app is installed AND the product has at least one supplier mapping. If the app is uninstalled OR the product has no mappings, the editor's Suppliers section is hidden entirely (not just empty).

### Supplier records lack timestamps
The integration stores suppliers and supplier-product links without `created_at` / `updated_at` fields. The merchant cannot sort the supplier list by "newest first" or audit when prices were last changed — only the current state is stored.

## Open questions

