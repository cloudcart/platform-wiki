---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → JSON-API v2"
route_name: customers-shipping-addresses.new
route_path: /admin/customers-new/details/:id/shipping-addresses
aliases: ["Customer shipping address JSON-API v2", "Customer shipping address API side effects", "Customer shipping address default-protection API"]
tags: [customers, addresses, shipping, api, json-api-v2]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (list, modal, Google Maps, defaults, save-hooks, storage, validation).

# Customer shipping addresses — JSON-API v2 access

## Purpose

Customer shipping addresses can be read, created, updated, or deleted via **JSON-API v2**. This aspect documents what the API path adds to the picture beyond the admin modal: same side effects, same default-address protection, the auto-promotion behaviour, the conditional-validation rule inherited from store settings, and where the canonical resource page lives.

The resource page itself (endpoint paths, attribute list, allowed filters, full request/response shapes) is [[api-customer-shipping-address]]. This page focuses on the **behaviour** the API shares with the admin UI.

## Where to find it

- Resource page: [[api-customer-shipping-address]].
- Generic JSON-API v2 conventions: [[json-api-v2]] (authentication, rate limit, the side-effects principle).
- Equivalent admin UI: this hub + [[customer-shipping-address-modal]] for the per-field semantics.

## What the merchant can do here

- Read a customer's shipping addresses through the JSON-API v2 endpoints (GET).
- Create a new shipping address (POST) — same field semantics as the modal.
- Update an existing address (PATCH) — same field semantics as the modal.
- Delete an address (DELETE) — same default-address protection as the admin UI.
- Bulk operations on the API: documented on [[api-customer-shipping-address]] when supported.

### What the merchant CANNOT do here

- Skip validation. The same the request validator validator runs on the API (see [[customer-shipping-address-validation]]).
- Bypass the courier-mapping regeneration on save. It runs on every PATCH / POST — see [[customer-shipping-address-save-hooks]].
- Delete the customer's current default shipping address through the API — rejected with HTTP 422 *"Cannot delete customer default address."* Same protection as the admin bulk delete (see [[customer-shipping-address-defaults]]).

## Settings & fields

### Endpoint paths

| HTTP | Path | Purpose |
|---|---|---|
| GET | `/api/v2/customers/{customer_id}/shipping-addresses` | List a customer's shipping addresses. |
| POST | `/api/v2/customer-shipping-addresses` | Create. |
| PATCH | `/api/v2/customer-shipping-addresses/{id}` | Update. |
| DELETE | `/api/v2/customer-shipping-addresses/{id}` | Delete. |

`(verify)` exact paths against [[api-customer-shipping-address]] — that page is the canonical source.

### Attributes

The address attributes mirror the modal fields plus the discriminator columns:

- `country.iso2`, `country.iso3`, `country.name`, `state`, `city_name` (`locality`), `street_name`, `street_number`, `post_code`, `additional_address_info`, `latitude`, `longitude`, `text`.
- `first_name`, `last_name`, `phone` (stored E.164 — see [[customer-shipping-address-save-hooks]]).
- `office_id` + `integration` for pickup-point addresses, `marketplace_id` for marketplace pickup — see [[customer-shipping-address-storage]].

See [[api-customer-shipping-address]] for the full attribute table + types + validation rules.

## Business rules

### Same side effects as the admin modal

A POST / PATCH / DELETE through JSON-API v2 fires the **same hooks** as the [[customer-shipping-address-modal]] save:

1. **Country ISO normalisation** — uppercase + alpha-3 derivation.
2. **Phone E.164 normalisation** — via libphonenumber.
3. **Lat/lng auto-fill** — from `<post_code> <city_name> <country_iso2>` via Google Maps geocoding.
4. **Text snapshot recompute** — the formatted address string.
5. **Post-save courier-mapping regeneration** — deletes ALL existing courier-mappings for the address, then loops every active courier via OmniShip to recompute.

See [[customer-shipping-address-save-hooks]] for the full sequence + the office-address skip rule. For merchants with many active couriers, this is a substantial per-save cost on the API too.

### Default-address protection applies via API

- **DELETE on the customer's current `default_address_id`** is rejected with HTTP 422 *"Cannot delete customer default address."* Promote a different address to default first.
- **First-added auto-promotes** — the FIRST shipping address created for a customer with zero existing addresses sets the customer's `default_address_id` automatically.
- **Setting default** is a customer-level pointer update (`customers.default_address_id`), NOT a flag on the address row. See [[customer-shipping-address-defaults]] + [[customer-shipping-address-storage]].

There is a separate "set default" endpoint that mirrors the admin "Set as default" action — `(verify)` the exact path against [[api-customer-shipping-address]].

### Conditional field requirements

The validator reads the same `checkout_hide_*` settings from [[settings-cart]] as the UI — so what's required vs optional depends on store configuration. See [[customer-shipping-address-validation]] for the full set. Programmatic clients (ERP / dashboard / sync integrations) must respect the same store-configurable required set.

### Pickup-point + marketplace addresses through the API

Office addresses (with `office_id`) and marketplace addresses (with `marketplace_id`) can be created / read / deleted through the API. The courier-mapping regeneration is skipped on office addresses, same as the admin modal. See [[customer-shipping-address-storage]] for the discriminator scheme.

### Snapshot decoupling applies to API edits too

PATCH-ing a customer's saved shipping address does NOT update the snapshot held on past orders. The order keeps its order-time snapshot. To update an order's address, the API call must target the order's shipping snapshot resource, not the customer's saved address. See [[customer-shipping-address-storage]] for the snapshot model and [[orders-details]] for order-level address edits.

### Authentication, rate limit, error shape

Standard JSON-API v2 conventions apply — see [[json-api-v2]]. Errors return as structured JSON-API v2 error objects with `status: "422"` + per-attribute pointers on validation failure.

### Side effects (cluster-wide via API)

- Successful POST / PATCH: address row written + customer pointer updated (when first-added) + courier-mappings regenerated.
- Successful DELETE: address row removed; past-order snapshots unaffected; if the deleted ID was a pointer target (`default_address_id`), the DELETE was rejected before reaching this step.
- Validation errors: HTTP 422 with field pointers; no state mutations.

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[api-customer-shipping-address]] — the canonical resource page (endpoints, attributes, full request/response).
- [[json-api-v2]] — authentication, rate limit, side-effects principle.
- [[customer-shipping-address-defaults]] — first-added auto-promotion + delete protection (same as UI).
- [[customer-shipping-address-save-hooks]] — the four save-time hooks fired by every API write.
- [[customer-shipping-address-validation]] — the conditional `checkout_hide_*` validator shared with the modal.
- [[customer-shipping-address-storage]] — pickup-point + marketplace discriminators and the order-snapshot decoupling.
- [[settings-cart]] — Google Maps API key + `checkout_hide_*` settings the API validator reads.
- [[orders-details]] — order-level address edits target the order snapshot, not the saved address.

## Open questions

- Exact endpoint paths for the "Set as default" + bulk-delete operations on the API — `(verify)` against [[api-customer-shipping-address]].
