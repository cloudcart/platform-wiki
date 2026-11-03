---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Brand + model"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Brand model module", "Car parts picker", "Brand model homepage filter", "Модул марка модел"]
tags: [design, modules, page-builder, brand-model, car-parts, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Brand + model block (`brand-model`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Brand + model** block renders a cascading **make → model → year** (and optionally **category**) picker that lets a car-parts shopper narrow the catalogue to compatible parts. The customer picks a vehicle, the block submits, and the storefront filters listings to parts compatible with that vehicle.

This block is exclusive to stores running the **Brand Model** app — automotive parts retailers, motorcycle parts shops, agricultural equipment dealers, anywhere where products are compatible with specific vehicle / equipment models.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Brand + model** from the block picker.

The block only appears in the picker when the `brand_model` app is installed (see [[brand-model]]). On stores without the app, the block is hidden.

## What the merchant can do here

- Pick whether to surface the **Categories** dropdown — when `categories = yes`, the picker chain ends with a categories dropdown so the customer can pick a part category (e.g., "Brakes", "Filters") alongside the vehicle.
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot configure the brand / model catalogue from this module — that lives in the [[brand-model]] app.
- The merchant cannot pick which brands / models the picker exposes — the picker always shows the full set published in the brand-model catalogue.
- The merchant cannot use the picker outside the page builder context (the equivalent storefront filter for product-listing pages is configured via the global `filters` module in [[design-modules-utility-editable]]).

## Settings & fields

| Field | Type | Validation | Default | Notes |
|-------|------|------------|---------|-------|
| `enabled` | toggle | `bool` | `true` | Master on/off. Hidden when the module class returns `canDisable == false`. |
| `categories` | select | `in:yes,no` | `no` | When `yes`, the picker exposes a categories dropdown alongside the vehicle. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]] for the builder's save flow.

## Business rules

### App-gated

The block only appears in the page-builder picker when the `brand_model` app is installed. The module is registered conditionally in the platform code:

_(platform implementation detail omitted)_


Uninstalling the app removes the block from the picker on subsequent builder loads — existing block instances on saved pages render but cannot be re-edited until the app is reinstalled.

### Picker chain

The picker is a multi-step cascade — brand → model → year (and optionally category). Each step's options are loaded based on the previous step's selection. The chain ends in a submit button that redirects the customer to a filtered product-listing URL.

### Categories vs. picker-only mode

The `categories = yes` mode adds a final categories dropdown so the customer can narrow further to a part type. The `categories = no` mode submits as soon as the merchant fills the vehicle chain — useful when the merchant wants a vehicle-only filter that lands the customer on the full compatible-parts catalogue.

### Storefront behaviour after submit

The picker submits to the product-listing page with the chosen brand / model / category as query parameters. The listing then applies the standard brand-model filter logic — see [[products-categories]] for how the underlying compatibility data is stored.

## Related

- [[design-modules-page-builder]] — hub.
- [[brand-model]] — Brand Model app (gates this module).
- [[design-modules-utility-editable]] — global `filters` module (the equivalent on product-listing pages).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.
- [[products-categories]] — category catalogue (brand-model + category combine on the storefront listing).

## Open questions

- 📡 **Picker depth.** Confirm the exact chain (brand → model → year → ...) and whether year is always shown or theme-controlled. (verify)
- 📡 **Uninstall-with-existing-instance behaviour.** What happens to a saved page when the Brand Model app is uninstalled and the block is still in the page content — graceful skip or broken render? (verify)
