---
type: feature
nav_path: "Customers → Customer details → Billing addresses → JSON-API v2"
route_name: customers-billing-addresses.new
route_path: /admin/customers-new/details/:id/billing-addresses
aliases: ["Customer billing address API", "api-customer-billing-address", "Billing address JSON-API v2", "Programmatic billing addresses"]
tags: [customers, addresses, billing, api, json-api-v2]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (list, modal, company fields, VIES, defaults, save hooks, storage).

# Customer billing address — JSON-API v2

## Purpose

The programmatic CRUD surface for customer billing addresses. Used by partner apps, ERPs, B2B onboarding flows, and merchant scripts that bulk-import company billing data. The endpoints respect the SAME save-time hooks, validation rules, VIES gating, and default-protection as the admin modal — with one important behavioural gap on the legacy JSON-API path documented under VIES.

## Where to find it

Endpoint base: `/api/v2/customers/{customer_id}/billing-addresses` (verify exact path; cross-reference [[json-api-v2]] for the v2 routing convention).

The endpoints are also reachable from the admin REST path (`/admin/api/core/customers/billing-address`) — but that path runs the additional `vat_validation` extension; see Business rules below.

## What the merchant can do here

- List billing addresses for a customer (paginated, filterable, sortable).
- Read a single billing address by id.
- Create a billing address.
- Update a billing address (full or partial).
- Delete a billing address (subject to the default-billing protection).
- Set the customer's default billing via the dedicated default-management endpoint.

### What the merchant CANNOT do here

- Delete the customer's current default billing — HTTP 422 *"Cannot delete customer default billing address."* The API enforces the same hard guard as the admin UI. See [[customer-billing-address-defaults]].
- Save an address that violates a `checkout_hide_* = required` rule from [[settings-cart]] — the same conditional validation runs.
- Bypass VIES — the four gating conditions are evaluated identically on API writes.

## Settings & fields

### Resource attributes

Same shape as the address row (see [[customer-billing-address-storage]] for the full column list). Key fields exposed in the API response:

- Person: `first_name`, `last_name`, `phone` (E.164).
- Address: `country_iso2`, `country_iso3`, `country_name`, `state_iso2`, `state_name`, `city`, `street`, `street_number`, `post_code`, `additional_information`, `latitude`, `longitude`, `text` (snapshot).
- Company: `company_name`, `company_vat`, `company_bulstat`, `company_mol`.
- VIES: `vies` (nested object — `countryCode`, `vatNumber`, `requestDate`, `valid`, `name`, `address`, `checkDate`).
- Timestamps: `created_at`, `updated_at`.

### Filters / sorts

- Filter by `is_company_address` (yes / no — same as the list filter — see [[customer-billing-address-list]]).
- Sort by `id` (default: descending).
- Other standard JSON-API v2 filters (date ranges on `created_at` / `updated_at`, equality on country / city) — see [[json-api-v2]] for the per-resource filter convention.

## Business rules

### Same side effects as the admin modal

API writes fire the same five save-time hooks as the modal:

- Phone normalisation to E.164.
- Lat / lng auto-fill from Google Maps geocoding fallback.
- Country ISO normalisation (upper-case iso2 + derived iso3 + localised country_name).
- Address text snapshot recomputation.
- **VIES VAT validation** when the four gating conditions hold (`checkout_validate_company_vat` ON in [[settings-cart]], `company_vat` non-empty, EU country, prefix matches country — special case Greece `EL`).

See [[customer-billing-address-save-validation]] for the hook pipeline and [[customer-billing-address-vies-validation]] for the gating + 7-day cache.

### Two-endpoint behaviour gap on VIES

The **admin REST endpoint** runs the `vat_validation` extension and rejects an invalid-VAT save with HTTP 422 *"Invalid company tax"*. The **legacy JSON-API path** does NOT run the extension — it stores the row with `vies.valid = false` and returns success. The merchant can create an invalid-VAT B2B record this way; the block kicks in only at checkout.

This is the most consequential behavioural gap between the two API paths. Integrators relying on save-time VIES rejection MUST use the admin REST endpoint.

### Coupled validation: company_name ↔ company_vat

Server-side coupled: filling either makes the other required at the validator level. Other company fields (`company_bulstat`, `company_mol`) stay independently optional. See [[customer-billing-address-company-fields]].

### Default-billing protection

- DELETE on the customer's current `default_billing_address_id` is rejected with HTTP 422 *"Cannot delete customer default billing address."* — promote a different billing address first.
- First-added billing address auto-promotes to default (zero merchant action required).
- Bulk delete: if any id in the batch matches the current default, the whole batch fails. See [[customer-billing-address-defaults]].

### Default management endpoint

`POST /admin/api/core/customers/billing-address/default/{customer_id}` with `{address_id}` to promote a billing address to default. Idempotent — promoting the already-default address returns success without side effects. Updates ONLY `default_billing_address_id`; `default_address_id` (shipping) is untouched.

### Conditional validation from store settings

The `checkout_hide_*` rules from [[settings-cart]] apply identically to API writes. Saving an address that violates a `required` rule returns HTTP 422 with field-level errors. The merchant must turn the setting to `optional` (or `hidden`) to allow blank values from the API. See [[customer-billing-address-save-validation]].

### Hard validation rules

- First / Last name min 2 chars (max 191).
- Country ISO must be a valid ISO 3166-1 alpha-2 code.
- Bulk delete: every id must exist (no silent skip).
- When Google Maps API key is configured, `country.iso2`, `latitude`, `longitude`, `locality`, `text` become required on write.

### Authentication, rate limit, side-effects principle

API writes through JSON-API v2 fire ALL the same downstream side effects as the admin UI — the VIES round-trip, the text snapshot recompute, the country ISO normalisation. There is no "API-only fast path" that skips these. See [[json-api-v2]] for the authentication scheme, rate limit, and the side-effects principle.

## Programmatic access

This page IS the programmatic-access aspect of the cluster.

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-modal]] — the admin modal that uses the parallel admin REST endpoints.
- [[customer-billing-address-vies-validation]] — the four gating conditions + the admin-REST-vs-legacy-JSON-API behaviour gap.
- [[customer-billing-address-defaults]] — the default-billing delete protection.
- [[customer-billing-address-save-validation]] — the hook pipeline + `checkout_hide_*` rules.
- [[customer-billing-address-storage]] — the resource shape and the `vies` JSON column.
- [[api-customer-billing-address]] — the API-resource page with the full endpoint surface.
- [[json-api-v2]] — authentication, rate limit, side-effects principle.

## Open questions

- Confirm the exact JSON-API v2 endpoint base path for billing addresses (verify against the route map).
- Confirm the partial-update semantics (PATCH replaces nested objects or merges them) (verify).
