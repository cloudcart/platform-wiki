---
type: feature
nav_path: "Apps → Store Locations"
route_name: apps.store_locations.overview
route_path: /admin/apps/store_locations
aliases: ["Store Locations", "Warehouses", "Multi-warehouse", "Geo-based inventory", "Локации", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, inventory, multi-warehouse, geo]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# Store Locations (multi-warehouse inventory)

## Purpose

**Store Locations** enables **multi-warehouse / multi-location inventory**. Each product variant tracks stock PER LOCATION instead of one global count. The integration ties locations to GEO ZONES (per [[settings-geo-zones]]) so customers in a given region see stock from the warehouse serving that region.

Used by merchants who:
- Operate multiple physical stores plus online (omnichannel).
- Run geographically separate warehouses (e.g. Sofia + Plovdiv).
- Want closer-warehouse routing for faster, cheaper shipping.

When installed, order quantity calculations check stock for the location driven by the customer's geo zone (stored in a cookie).

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.

## Where to find it

Sidebar → Apps → install → **Store Locations**. See [[apps-store-locations-settings]] for configuration.

## What the merchant can do here

- Create / manage locations (warehouses, physical stores).
- Map locations to geo zones (Sofia warehouse → Sofia zone; Plovdiv warehouse → Plovdiv zone).
- Set per-variant stock per location.
- Configure default routing rules.

### What the merchant CANNOT do here
- Use Store Locations without [[settings-geo-zones]] configured — geo zones drive the routing.
- Keep a single shared global stock — the integration's whole point is per-location tracking.
- Set per-location prices — the catalog price is one global value across all locations. For location-differentiated pricing use [[customers-custom-groups]] or run multiple storefronts.
- Transfer stock between locations from a built-in UI — there is no "move 10 units Sofia → Plovdiv" screen. A transfer is two manual edits in the [[apps-stores]] per-store quantity editor (subtract from one shop, add to another).

## Settings & fields

The settings page exposes:

- **Cookie validity** (days) — how long the customer's selected location persists. Help text: *"Choose how many days the users cookie is valid when selecting an address. After the period you selected expires, the user will need to re-enter a delivery address."* Set to 30 → the picker re-prompts on day 31.
- **Access to site without an address** (toggle) — see Business rules below. When ON, these two fields are required:
  - **Text for buy button in product listing** (`text_buy_listing`) — replaces the *Buy* button on category cards.
  - **Text for buy button on detail page** (`text_buy_details`) — replaces the *Buy* button on the product detail page.
  - Fallback text for both: *"You have not entered an address!"* (`no_exist_address` translation).
- **Select a page** — the CMS page that hosts the address-picker module (used when the toggle is OFF).
- **Main store** — required when the toggle is ON; the warehouse whose products show before the customer picks an address. Help text: *"If the user does not select an address, the products from the selected store will be visible"*.
- **Choice of delivery location** — configurable title of the picker module; optional after-pick redirect to a chosen page (`module.home_page_select`).

**Google Maps API Key is required.** Saving the settings without one returns *"To save the settings, you need to have a Google API Key entered."* The key lives at Settings → Cart Settings → Google Maps API Key. The picker uses Google address autocomplete to capture city, quarter, street and street number; without it the picker cannot function.

## Business rules

### Cookie-driven storefront stock

On first visit the customer picks a delivery address; the platform writes a `store_location` cookie holding their geo zone, and later visits show stock only for that location. The cookie is read **only on the storefront** — admin and theme-builder browsing never trigger zone-based filtering. With no cookie, the customer must select a location (toggle OFF) or sees the **Main store** catalog (toggle ON).

The `store_location` cookie stores the full structured address, not just a zone ID: `country_name`, `city_name`, `quarter_name`, `street_name`, `street_number`, `geo_zone_id`, and a `no_address_exist` boolean. A storefront navigation module renders these under a map-marker icon (e.g. "Bulgaria, Sofia, Lozenets, Vitosha 100"), exposing the zone as a `zone_id` HTML attribute for theme styling. Clicking the marker re-opens the picker; a different address overwrites the cookie and refreshes the catalog filter on the next page load.

### Zone-to-location mapping

Each geo zone (from [[settings-geo-zones]]) maps to one or more shops/warehouses; one zone can serve MULTIPLE warehouses (overlap allowed). When a customer is in the Sofia zone, the storefront shows products stocked in the Sofia warehouse, and orders and shipping rates are fulfilled from Sofia. The zone name is also shown to the customer ("you're shopping from <Zone Name>").

### Per-variant per-location stock

Each variant has separate quantity per location — adding stock to "Sofia" does not affect "Plovdiv". The merchant manages stock per warehouse in [[products-inventory]] with a location filter.

### Order assignment

A placed order is attributed to the location serving the customer's zone, so fulfillment workflows know which warehouse picks and packs.

### Catalog filters strictly by zone — no cross-zone shipping

With a `store_location` cookie set, the catalog is limited to products stocked in shops linked to the customer's zone. Admin warns: *"Attention! Only products that have been added to the selected stores will be visible in the selected area"*. Products stocked only in another zone do not appear — there is no built-in cross-zone "longer delivery time" mode. To sell cross-zone, the merchant must add the product to a shop in that zone too.

### Address-picker UX (the "Access to site without address" toggle)

Two storefront modes:

- **OFF (default)** — until the customer picks an address, the platform redirects them to the address-picker page (the **Select a page** setting). They cannot browse the catalog first.
- **ON** — the customer can browse, but the *Buy* button on every card and detail page is replaced with the configured text (`text_buy_listing` / `text_buy_details`) linking to the picker pop-up (route `apps.store_locations.location_popup`). This is the "tell us your location first" upsell. The merchant must also pick a **Main store** (above). Once the customer selects an address the cookie populates and normal *Buy* buttons return.

The picker is **manual** — there is no automatic IP-geo zone detection. If the entered address matches no defined zone, the cookie stores `no_address_exist = true` and the buy buttons show the alt text (`no_exist_address`). When no address can be resolved, storefront templates fall back to the same localised string, typically *"You have not entered an address!"*.

### Click-and-Collect / BOPIS

This app routes the **online catalog** only; it adds neither a pickup shipping method nor a pay-in-store payment method. For pickup-in-store the merchant installs [[apps-stores]] alongside it (Stores adds the **Local Pickup** shipping method and **Pay on place** payment method). Store Locations decides which warehouse's catalog the customer sees; Stores decides whether they can pick up in person.

### Suppliers are independent

[[apps-suppliers]] is unrelated to Store Locations. The supplier `in_stock` flag tracks the *supplier's* availability, not the warehouse's, and there is no automatic re-order when a warehouse runs low.

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[apps-store-locations-settings]] — settings sub-page.
- [[settings-geo-zones]] — zone definitions that map to locations.
- [[products-inventory]] — per-location stock view (when this app is installed).
- [[products-variants-options]] — per-variant stock tracked here.
- [[apps-stores]] / [[apps-stores-sync]] — multi-storefront / pickup concept (distinct from multi-warehouse).
- [[apps-suppliers]] — supplier availability (independent of warehouse stock).
- [[customers-custom-groups]] — customer-group pricing (the per-location-pricing alternative).
- [[orders]] — orders attributed to locations.

## Open questions
