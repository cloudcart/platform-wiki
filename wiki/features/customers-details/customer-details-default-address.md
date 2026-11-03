---
type: feature
nav_path: "Customers → Customer details → Default address card"
route_name: customers-details
route_path: /admin/customers/details/:id
aliases: ["Customer default address card", "Default address preview", "Default address Google Map"]
tags: [customers, profile, detail, address, maps]
plan_gates: ["customers"]
created: 2026-06-10
updated: 2026-11-03
source_count: 4
---

> Part of [[customers-details]]. See the hub for the other aspects (identity card, tab strip, ban flow, email verification, delete).

# Customer details — Default address card

## Purpose

The **right-column default-address card** on the customer detail page. The card surfaces the customer's default **shipping** address (the one that pre-fills checkout) as a field table + embedded Google Map preview. It has two distinct states (has-default vs no-default), and address edits refresh just this card without re-loading the entire customer record.

This aspect covers the card layout, the two states, the Google Maps integration, and the empty-state *+ Add address* flow. The address modal itself is documented on [[customers-details-shipping-addresses]] / [[customers-details-billing-addresses]].

## Where to find it

[[customers]] → click any row → opens `/admin/customers/details/:id`. The card sits in the **right column** of the two-column layout, **below** the conditional [[customer-details-ban-flow|ban-reason card]] (when banned). It is the only persistent right-column card — visible on every customer regardless of ban state.

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
- **Fallback centre**: if the address has no coordinates, the map and its pin sit on Sofia at `42.6977082, 23.3218675`.
- The map respects both the OLD and NEW Google Maps API versions per the `google_map_api_version` server setting.

Pencil click → opens the address panel pre-populated with the address, saving to the customer's shipping addresses. On save, the card updates without re-loading the rest of the page. See [[customer-shipping-address-modal]] for the field list and validation.

### State 2: No default address

When no `default_address_id` is set on the customer, OR the address fetch returned 404:

- **Title**: *"Default address"*.
- **Body text**: *"There is no default address currently set, you can add a new one and it will be set as the default one."*
- **+ Add address** link (purple) → opens the same address panel in CREATE mode, saving a shipping address.

The customer's first-ever shipping address becomes the default by itself. If the customer already has other shipping addresses, the new one shows on this card until the page is reloaded; to keep it as the default, use **Set as default** on [[customer-shipping-address-list]].

## Settings & fields

| Field | Role | Notes |
|-------|------|-------|
| `customer.default_address_id` | Pointer to the address shown in this card | Set by **Set as default** on the Shipping addresses tab, or auto-set on first-ever shipping address creation. |
| `google_maps_api_key` (server setting) | Enables the embedded map | When unset, the field table renders but the map is hidden. |
| `google_map_api_version` (server setting) | OLD vs NEW Maps JS API | The card adapts to either version. |

The card itself has no per-store configuration knobs — its behaviour is entirely driven by the customer's address records and the two server settings above.

## Business rules

### The card refreshes on its own

Saving or deleting addresses on the [[customers-details-shipping-addresses|Shipping]] / [[customers-details-billing-addresses|Billing]] tabs updates just this card, without re-loading the entire customer-detail object. If the default address no longer exists (for example it was deleted), the card switches to the no-default state.

### First-ever shipping address is auto-promoted to default

The first shipping address created for a customer becomes the default. Later addresses require **Set as default** to replace the current one.

### Map controls are disabled — clicks escape to Google Maps

The embedded map is intentionally non-interactive (no zoom, no pan, no street-view). A transparent click overlay sits on top: clicking anywhere on the map opens the same coordinates on `maps.google.com` in a new tab. This keeps the in-admin card light (no map-tile network chatter from user pans) while still letting the merchant inspect the location at full resolution.

### Map respects the server-side API key + version setting

The map renders only when `google_maps_api_key` is set in the server config. Without a key, the field table shows but the map block is omitted entirely — no broken-iframe placeholder. The `google_map_api_version` server setting picks between the OLD and NEW Maps JS API versions; the card's loader handles either branch transparently.

### Fallback to Sofia when no coordinates

If the address has no coordinates (e.g., manually-entered foreign-country addresses where geocoding failed), the map centres on Sofia at `42.6977082, 23.3218675`. The pin sits on that fallback centre, so the merchant should rely on the field table for the truth in that case.

### Edit save refreshes only this card

When the merchant clicks the pencil and saves an edit through the address panel, the card and the open address list update, but the customer record is NOT re-fetched. The identity card and insights stay as they were until the page is reloaded.

## Related

- [[customers-details]] — hub.
- [[customers-details-shipping-addresses]] — Shipping addresses tab; full list + CRUD of saved shipping addresses.
- [[customers-details-billing-addresses]] — Billing addresses tab; full list + CRUD of billing addresses.
- [[customer]] — entity page; carries `default_address_id`.
- [[customer-details-tab-strip]] — sub-tab navigation that holds the full address lists.
- [[customer-details-identity-card]] — left-column identity card (sibling of this card in the two-column layout).

## Open questions

None.
