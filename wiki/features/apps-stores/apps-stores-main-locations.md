---
type: feature
nav_path: "Apps → Local Pickup (Stores) → Stores"
route_name: apps.stores.overview
route_path: /admin/stores
aliases: ["Local Pickup locations", "Physical store locations", "Pickup points", "Stores list", "Store address editor", "Working hours editor"]
tags: [apps, stores, local-pickup, physical-location, seo, working-hours]
plan_gates: ["stores"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Local Pickup — physical store locations

## Purpose

> Part of [[apps-stores]]. See the hub for the other aspects (shipping + payment methods, per-store stock).

Lets the merchant create and manage the **physical store locations** that power Local Pickup. Each location has a title, a friendly URL, a physical address (with GPS coordinates for the map embed), contact details, and per-day working hours. Locations are listed on an auto-generated public storefront page and become selectable pickup points at checkout.

## Where to find it

Sidebar → Apps → install → **Local Pickup** → manage stores. The route is `/admin/stores` (reached via the `RedirectOldApp` wrapper from `/admin/apps/stores`). Empty state (`notify.no_records_yet`): *"You have not added any stores yet."* (`notify.no_records_info`: *"Your stores will show up here."*)

## What the merchant can do here

- **Add a store** (`action.add`) — create a physical location.
- **Edit / delete** any store.
- Configure **per-store SEO** (Header: "SEO configuration") — friendly URL handle + standard meta tags so each store's public page is indexable separately.
- Set **working hours** per day of the week.
- Toggle a store **active / inactive** to control storefront visibility.
- Drag to **reorder** stores for storefront display order.

### What the merchant CANNOT do here
- Edit the public stores page layout — it's auto-generated from the saved locations.
- Add a manual "Google Maps embed code" — the map is derived from the saved GPS coordinates.
- Set per-store prices — pricing is product-level across all stores (see [[apps-stores-main-stock]]).

## Settings & fields

### Per-store fields

| Field | lang key | Placeholder / tip |
|---|---|---|
| **Title** | `label.title` | `ph.title`: "E.g. main store" — internal + customer-facing name. |
| **URL** (handle) | `label.url_handle` | `ph.seo_url_handle`: "Enter friendly and unique SEO url"; `tip.seo_url_handle`: "This is the store's friendly URL." |
| **Store Address** | `label.address` | Physical address — used for the Google Map embed. |
| **Email** | `label.email` | `ph.email`: "Email". |
| **Phone** | `label.phone` | `ph.phone`: "Phone". |
| **Work time** | `label.work_time` | `ph.work_time`: "Work time". |

### Working hours

The per-store working-hours editor exposes one row per day of the week (Monday–Sunday) with **From** / **To** times and an **active / closed** checkbox. The default fill is `10:00` – `22:00`. Special handling:

- If `From > To`, the platform interprets that as overnight (no error).
- `To = 00:00` is rewritten to `23:59` so the hours render correctly as "ends at midnight".

There is **no** holiday / special-date override (Christmas, public holidays, etc.) — the merchant manually edits a day or marks it closed for the period.

### Success / notify messages
- `succ.add`: "Successfully added".
- `succ.edit`: "Successfully edited".
- `notify.no_records_yet`: "You have not added any stores yet".
- `notify.no_records_info`: "Your stores will show up here".

## Business rules

### Unlimited locations

The merchant can create **unlimited** physical locations — there is no cap in the model.

### Active flag controls storefront visibility

Each store has an `active` boolean (0 / 1). The storefront's public-stores page lists only `active = 1` stores; inactive stores are hidden from customers but kept in the admin — useful for prepping a future store (data entry) without listing it. Inactive stores also won't appear as Local Pickup options at checkout.

### Sort order is per-store, auto-incremented at create

New stores get `sort = max(sort) + 1` automatically. The merchant can drag/reorder to change display order on the storefront. The platform does **not** auto-sort alphabetically; merchant-controlled order takes precedence.

### Unique URL handle; storefront route is `/stores/<handle>`

The `url_handle` field must be **unique** across stores; the platform validates uniqueness at save. The storefront's per-store public page renders at `/stores/<handle>` (route `stores.view`). Each store has its own indexable URL. The store's title plus its address (city, street, street number) is auto-formatted for sharing.

### GPS coordinates power the map

The store address captures GPS latitude / longitude (`gps_lt`, `gps_ll` on the Shop model) — these power the Google Map embed on the public page. There is no manual "Google Maps embed code" field; the platform derives the map from the saved coordinates.

### Stores listed by city for filtering

The storefront's stores listing module groups active stores by city so customers can filter by city. Each unique city in a store's address becomes a filter chip. This is a pure storefront concern — it affects nothing in admin.

### Delete cascades to addresses and shipping rates

Deleting a store also deletes its `ShopAddresses` row and any `ShippingProviderAddresses` whose `marketplace_id` equals the store id. The merchant loses the store's per-location shipping configuration on delete. The "marketplace" terminology is internal; merchant-facing it's just "store" / "physical location".

## Related

- [[apps-stores]] — hub.
- [[apps-stores-settings]] — install / overview screen.
- [[apps-store-locations]] — multi-warehouse inventory (separate, uncoupled app with a different data model).
- [[shipping]] — per-location shipping rates are keyed on the store id.
- [[api-stores]] — JSON-API v2 read surface for these locations (read-only).

## Open questions

None.
