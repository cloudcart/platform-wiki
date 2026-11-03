---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Store locations"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Store locations module", "Shops module", "Physical stores block", "Pickup locations block", "Модул магазини", "Модул локации"]
tags: [design, modules, page-builder, store-locations, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Store locations block (`store_locations`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Store locations** block surfaces a list of physical store locations / pickup points on a Dynamic page. Used for a "Find a store" page, a "Our locations" landing, or a contact page with multiple stores. The block is gated by the **Store Locations** app — see [[apps-store-locations]].

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Store locations** from the block picker.

The block only appears in the picker when the Store Locations app is installed. On stores without it, the block is absent.

## What the merchant can do here

- Set a section **Title** (heading above the list).
- Pick an icon (when the theme advertises icon support) — surfaced as the `icon` setting and parsed into `icon_data` JSON on save.
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot add or edit individual store locations from this block — that lives in the Store Locations app's admin.
- The merchant cannot filter the list (e.g., show only locations in a specific city) — the block renders the full set of active locations.
- The merchant cannot embed a custom map alongside the list — for map embedding, use the `contact.googleMap` module on the theme-wide Modules screen.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. Stored as `int(0|1)`. |
| `title` | text input | `''` | Section title above the list. |
| `icon` | (theme-shipped icon picker) | `''` | When picked, parsed into `icon_data` JSON via `_getIconData`. |
| `icon_data` | JSON (computed) | `null` | Derived from `icon` on save; the storefront uses this for rendering. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]]. The `saveSettings` method coerces `enabled` to `int(0|1)` and computes `icon_data` from the picked icon.

## Business rules

### App-gated

The block only registers when the Store Locations app is installed:

_(platform implementation detail omitted)_


Without the app, the block is absent from the picker, and on the storefront the legacy fallback notice "Application 'Store location' is not installed" renders in place of the list.

### Location source is the app's location catalogue

The block reads from the same location catalogue as the Store Locations app — see [[apps-store-locations]] for the data model. Active, published locations surface in the list; deactivated locations are hidden.

### Map integration is separate

The block renders a list / cards layout, NOT a map. For a map view, the merchant uses the theme-wide `contact.googleMap` module (see [[design-modules]]) which overlays the Store Locations app's data on a Google Map.

### Theme dependencies for icon picker

Some themes ship an icon picker — when the theme advertises this, the `icon` field exposes the picker; otherwise the field is hidden.

### Per-language title

With the `multylang` app, the section title accepts per-language entries via the language switcher in the editor.

## Related

- [[design-modules-page-builder]] — hub.
- [[apps-store-locations]] — Store Locations app (gates this module; location catalogue lives here).
- [[design-modules]] — theme-wide `contact.googleMap` module (map view of the same data).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Per-location detail card.** Confirm what each card shows by default (name, address, hours, phone, photo) and whether any of those are merchant-toggleable per theme. (verify)
- 📡 **Distance / nearest-store integration.** Some merchants want a "nearest store" indicator — confirm whether this block exposes a geo-locator or whether that's part of the contact-page module. (verify)
