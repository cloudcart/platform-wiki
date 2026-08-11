---
type: feature
nav_path: "Customers → Customer details → Default address card"
route_name: customers-details.new
route_path: /admin/customers-new/details/:id
aliases: ["Customer default address card", "Default address preview", "Default address Google Map"]
tags: [customers, profile, detail, address, maps]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers-details]]. See the hub for the other aspects (identity card, tab strip, ban flow, email verification, delete).

# Customer details — Default address card

## Purpose

The **right-column default-address card** on the customer detail page. The card surfaces the customer's chosen *"default"* address (the one that pre-fills checkout) as a field table + embedded Google Map preview. It has two distinct states (has-default vs no-default) and runs on a **separate** query from the rest of the page so that address edits refresh just this card without re-loading the entire customer record.

This aspect covers the card layout, the two states, the Google Maps integration, and the empty-state *+ Add address* flow. The address modal itself is documented on [[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]].

## Where to find it

[[customers]] → click any row → opens `/admin/customers-new/details/:id`. The card sits in the **right column** of the two-column layout, **below** the conditional [[customer-details-ban-flow|ban-reason card]] (when banned). It is the only persistent right-column card — visible on every customer regardless of ban state.

The card itself does NOT navigate to the addresses tab — to manage the full address list, the merchant uses the [[customers-details-shipping-addresses|Shipping addresses]] or [[customers-details-billing-addresses|Billing addresses]] sub-tabs of the [[customer-details-tab-strip|tab strip]].

## What the merchant can do here

### State 1: Has default address

When `default_address_id` is set on the customer AND the address fetch succeeded:

- **Title row**: *"Default address"* + pencil edit button.
- **Field table** (label: value) showing only fields that have a value:
  - Name (full_name of the address holder)
  - Country (`country.name`)
  - State (`state.name`)
  - City (`city.name`)
  - Street (`street.name` prefixed by `street_number`)
  - Post code (`post_code`)
  - Phone (`phone_international`)
- **Google Map** (when the `google_maps_api_key` server setting is set): a 125px-tall non-interactive map centred on the address coordinates. Controls disabled (no zoom, no pan, no street-view); a transparent click overlay on top intercepts clicks and opens `https://www.google.com/maps/?z=15&q=<lat>,<lng>` in a new tab.
- **Fallback centre**: if the address has no coordinates, the map centres on Sofia at `42.6977082, 23.3218675`.
- The map respects both the OLD and NEW Google Maps API versions per the `google_map_api_version` server setting.

Pencil click → opens the address modal pre-populated with the address. On save, the default-address card refreshes via its separate `defaultAddressQuery` (keyed by `customer_id + default_address_id`) without re-loading the rest of the page. See [[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]] for the modal field list and validation.

### State 2: No default address

When no `default_address_id` is set on the customer, OR the address fetch returned 404:

- **Title**: *"Default address"*.
- **Body text**: *"There is no default address currently set, you can add a new one and it will be set as the default one."*
- **+ Add address** link (purple) → opens the same address modal in CREATE mode. On save, the new address is marked default automatically (the address backend sets `is_default=1` on the first address for a customer).

So the merchant doesn't need to separately toggle "make default" — creating the first-ever address from this card auto-promotes it.

## Settings & fields

| Field | Role | Notes |
|-------|------|-------|
| `customer.default_address_id` | Pointer to the address shown in this card | Set by the address modal's "is default" checkbox, or auto-set on first-ever address creation. |
| `google_maps_api_key` (server setting) | Enables the embedded map | When unset, the field table renders but the map is hidden. |
| `google_map_api_version` (server setting) | OLD vs NEW Maps JS API | The card adapts to either version. |

The card itself has no per-store configuration knobs — its behaviour is entirely driven by the customer's address records and the two server settings above.

## Business rules

### Separate query for the default-address card

The default-address card is fetched separately by `default_address_id` (its own TanStack Query), so editing addresses on the [[customers-details-shipping-addresses|Shipping]] / [[customers-details-billing-addresses|Billing]] tabs refreshes just this card without re-loading the entire customer-detail object. This keeps the right column responsive even when the customer has dozens of addresses.

### First-ever address is auto-promoted to default

The address backend sets `is_default = 1` on the very first address created for a customer — so the merchant doesn't have to toggle "make default" when adding via the **+ Add address** link from the empty state. Subsequent address creations require the merchant to explicitly mark the new one as default if they want to replace the current one.

### Map controls are disabled — clicks escape to Google Maps

The embedded map is intentionally non-interactive (no zoom, no pan, no street-view). A transparent click overlay sits on top: clicking anywhere on the map opens the same coordinates on `maps.google.com` in a new tab. This keeps the in-admin card light (no map-tile network chatter from user pans) while still letting the merchant inspect the location at full resolution.

### Map respects the server-side API key + version setting

The map renders only when `google_maps_api_key` is set in the server config. Without a key, the field table shows but the map block is omitted entirely — no broken-iframe placeholder. The `google_map_api_version` server setting picks between the OLD and NEW Maps JS API versions; the card's loader handles either branch transparently.

### Fallback to Sofia when no coordinates

If the address fetch succeeds but the address has no `lat` / `lng` (e.g., manually-entered foreign-country addresses where geocoding failed), the map centres on Sofia at `42.6977082, 23.3218675`. The pinned marker shows the fallback centre, NOT the actual address, so the merchant should rely on the field table for the truth in that case `(verify)`.

### Edit-modal save refreshes only this card

When the merchant clicks the pencil and saves an edit through the address modal, the `defaultAddressQuery` invalidates and refetches — but the main customer record query does NOT. So the identity card, insights, and tab data are NOT re-fetched. The merchant sees the updated address in the right column on next render, but won't see (e.g.) a downstream KPI update until something else triggers a customer-record refresh.

## Related

- [[customers-details]] — hub.
- [[customers-details-shipping-addresses]] — Shipping addresses tab; full list + CRUD of saved shipping addresses.
- [[customers-details-billing-addresses]] — Billing addresses tab; full list + CRUD of billing addresses.
- [[customer]] — entity page; carries `default_address_id`.
- [[customer-details-tab-strip]] — sub-tab navigation that holds the full address lists.
- [[customer-details-identity-card]] — left-column identity card (sibling of this card in the two-column layout).

## Open questions

- Verify whether the Sofia fallback markers display a pin or hide it entirely when coordinates are missing.
- Verify whether the empty-state *+ Add address* link opens the shipping-address or billing-address modal (or a unified address modal).
