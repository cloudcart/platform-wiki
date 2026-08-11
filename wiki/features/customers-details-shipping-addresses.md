---
type: feature
nav_path: "Customers → Customer details → Shipping addresses"
route_name: customers-shipping-addresses.new
route_path: /admin/customers-new/details/:id/shipping-addresses
aliases: ["Customer shipping addresses", "Customer shipping address list", "Shipping addresses", "Адреси за доставка"]
tags: [customers, addresses, shipping]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 12
---

# Customer shipping addresses

## Purpose

The list of **saved shipping addresses** for one customer. The merchant uses this sub-tab to view, add, edit, set-as-default, or delete addresses where the customer wants their orders delivered. Each customer can have many shipping addresses but exactly **one default** (the address pre-selected when the customer reaches checkout). Setting a new default automatically unsets the previous one.

Addresses are typed-up through a Google Maps autocomplete (when the merchant has set up a Google Maps API key in [[settings-cart]]), so cities and street numbers come pre-validated; otherwise the merchant uses a manual entry form.

This hub is split into focused aspects — read the one that matches the question, not all of them.

## Sub-pages (in this cluster)

- [[customer-shipping-address-list]] — list table columns (Region, Address, Post code, Phone, Type), sort order, the company-address filter, bulk delete, and what the merchant CANNOT do from this view.
- [[customer-shipping-address-modal]] — the Add / Edit side-panel: Customer info + Address sections, field-by-field, country-code phone, hidden Company details on shipping, save handler routes.
- [[customer-shipping-address-google-maps]] — Google Maps autocomplete + interactive map, marker-drag reverse-geocoding, geo-names lookup, the two API versions (old / new), no-key fallback, error banner.
- [[customer-shipping-address-defaults]] — one-default-per-customer rule, first-added auto-promotion, "Set as default" action, hard-guarded deletion of the current default, sidebar refresh, default-shipping vs default-billing independence.
- [[customer-shipping-address-save-hooks]] — the four save-time hooks: phone E.164 normalisation, lat/lng auto-fill from postcode, country ISO uppercase + alpha-3 derivation, and the post-save courier-mapping regeneration across every active courier.
- [[customer-shipping-address-storage]] — the address table, the `default_address_id` pointer on the customer row (not on the address), pickup-point (`office_id`) + marketplace (`marketplace_id`) discriminators, the `realAddress` scope, and the per-order snapshot decoupling.
- [[customer-shipping-address-validation]] — conditional field requirements driven by `checkout_hide_*` settings on [[settings-cart]], the name-field minimum, the `post_code_not_required` weakening, and the extra Google-Maps-only required fields.
- [[customer-shipping-address-api]] — JSON-API v2 read / create / update / delete for shipping addresses, same side effects as the admin modal, default-address delete protection, plus the API auto-promotion behaviour.

## Where to find it

From [[customers-details]] → **Shipping addresses** tab. The route is `/admin/customers-new/details/:id/shipping-addresses`.

## What the merchant can do here

- View every saved shipping address in a paginated, sortable, filterable table — see [[customer-shipping-address-list]].
- Add a new address through the Add modal — see [[customer-shipping-address-modal]].
- Edit any existing address (click the row's Address cell) — see [[customer-shipping-address-modal]].
- Promote a non-default address to default via "Set as default" — see [[customer-shipping-address-defaults]].
- Bulk-delete selected addresses (with confirmation) — see [[customer-shipping-address-list]].
- Use Google Maps autocomplete / interactive map (when the API key is configured) — see [[customer-shipping-address-google-maps]].

### What the merchant CANNOT do here

- Add an address from a customer-side **billing** address — billing addresses live in their own list. See [[customers-details-billing-addresses]].
- Toggle "ship to ANOTHER address vs same as billing" — that's a customer-side checkout-time flag, not stored on the address record.
- Delete the customer's current default shipping address without promoting another address first — see [[customer-shipping-address-defaults]].

## Settings & fields

This is a hub — per-aspect pages carry the field tables. Quick map:

- List columns + filter → [[customer-shipping-address-list]].
- Add / Edit modal fields → [[customer-shipping-address-modal]].
- Conditional required-vs-optional rules per store setting → [[customer-shipping-address-validation]].
- Google Maps adds extra required fields → [[customer-shipping-address-google-maps]] + [[customer-shipping-address-validation]].

## Business rules

This is a hub — full mechanics live on the aspect pages. Five rules every consumer of this cluster must know:

- **Default is a customer-level pointer, NOT a flag on the address row.** "Is this the default?" is computed by comparing the customer's `default_address_id` to the address ID. See [[customer-shipping-address-defaults]] + [[customer-shipping-address-storage]].
- **Deletion does NOT cascade to past orders.** Orders carry a snapshot of the address at the time they were placed; deleting the saved address only removes it from the customer's saved-addresses list for FUTURE use. See [[customer-shipping-address-storage]].
- **Default shipping CANNOT be deleted directly.** A delete that targets the customer's current default is rejected with HTTP 422 *"Cannot delete customer default address."* The merchant must promote a different address first. Bulk delete that includes the default also fails for the whole batch. See [[customer-shipping-address-defaults]].
- **Every save runs four hooks (including a heavy courier-mapping rebuild).** Phone is normalised to E.164, lat/lng auto-filled, country ISO normalised, and ALL courier-mapping rows for the address are deleted then re-computed across every active courier via OmniShip. For merchants with many active couriers, this is the heavy cost of every shipping-address save. See [[customer-shipping-address-save-hooks]].
- **Validation is conditional on `checkout_hide_*` settings from [[settings-cart]].** What's required vs optional differs between two CloudCart stores depending on their checkout configuration. See [[customer-shipping-address-validation]].

### Permission

Standard `customers` permission scope. All admin API endpoints under `/admin/api/core/customers/shipping-address` are protected by `hasApiPermission:customers` middleware.

### Storefront sync

Changes here reflect immediately on the storefront — the next time the customer visits their address book on the storefront account page, they see the updated list.

## Programmatic access

Customer shipping addresses can be read, created, updated, or deleted via **JSON-API v2** — see [[customer-shipping-address-api]] and [[api-customer-shipping-address]].

**Same side effects apply.** API writes fire the same save-time hooks as the address modal (phone E.164, lat/lng auto-fill, country ISO normalisation, courier-mapping regeneration) and respect the same default-address delete protection. See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Related

Aspects in this cluster — see Sub-pages above: [[customer-shipping-address-list]], [[customer-shipping-address-modal]], [[customer-shipping-address-google-maps]], [[customer-shipping-address-defaults]], [[customer-shipping-address-save-hooks]], [[customer-shipping-address-storage]], [[customer-shipping-address-validation]], [[customer-shipping-address-api]].

External pages:

- [[customers-details]] — parent details page (Default address sidebar card reads from here).
- [[customers-details-billing-addresses]] — sister tab for billing addresses with the same modal but with Company details fields exposed.
- [[settings-cart]] — Google Maps API key + `checkout_hide_*` setting set configured here.
- [[settings-geo-zones]] — geo-zones use city / country / state stored on the address for shipping rate matching.
- [[settings-taxes]] — taxes use the address country for VAT bracket matching.
- [[api-customer-shipping-address]] — JSON-API v2 endpoints.
- [[customer]] — entity page.

## Open questions

None — all previously-flagged items distributed to sub-pages.
