---
type: feature
nav_path: "Customers → Customer details → Shipping addresses → Validation"
route_name: customers-shipping-addresses.new
route_path: /admin/customers-new/details/:id/shipping-addresses
aliases: ["Customer shipping address validation", "checkout_hide_* address validation", "post_code_not_required", "Address required fields per store settings"]
tags: [customers, addresses, shipping, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-shipping-addresses]]. See the hub for the other aspects (list, modal, Google Maps, defaults, save-hooks, storage, API).

# Customer shipping addresses — Validation rules

## Purpose

Address validation in CloudCart is **NOT hard-coded** — it's driven by store settings. The same the request validator validator reads multiple `checkout_hide_*` settings from [[settings-cart]] to decide which fields are required, optional, or hidden, plus a separate `post_code_not_required` toggle that weakens post-code rules. This aspect documents every setting that influences validation, the per-field defaults, the Google-Maps-only extra required fields, and the practical consequence: **two CloudCart stores can have different required-field sets on the same modal**.

## Where to find it

These rules run server-side on every save:

- POST / PATCH from the [[customer-shipping-address-modal]] saves.
- POST / PATCH / DELETE through [[customer-shipping-address-api]].
- The admin-side form mirrors the same rules — so the red "required" indicator in the modal also reads from these settings.

The settings themselves are edited on [[settings-cart]] (Settings → Cart).

## What the merchant can do here

- Configure which checkout fields are required vs optional vs hidden via the `checkout_hide_*` set on [[settings-cart]] — those choices automatically propagate to the saved-addresses modal validation.
- Loosen the post-code rule globally with `post_code_not_required` (weakens min-length from 3 chars to 2).
- See the validation rules respected on both the admin-side modal AND the JSON-API v2 endpoints.

### What the merchant CANNOT do here

- Override validation per address. The validator reads only store-wide settings.
- Skip required fields when a Google Maps API key is configured — the key adds extra required fields on top of the base set.

## Settings & fields

### `checkout_hide_*` settings (from [[settings-cart]])

Each can take one of three values: `required`, `optional`, or `hidden`. Listed below with the address field they govern:

| Setting | Field governed |
|---|---|
| `checkout_hide_first_name` | First name |
| `checkout_hide_last_name` | Last name |
| `checkout_hide_phone` | Phone |
| `checkout_hide_street_name` | Street |
| `checkout_hide_street_number` | Street number |
| `checkout_hide_additional_information` | Additional address info |
| `checkout_hide_state_iso2` | State (when state is identified by ISO2 code) |
| `checkout_hide_state_name` | State (when state is identified by name) |

### Other validation settings

| Setting | Effect |
|---|---|
| `post_code_not_required` | When ON, the post-code rule is **weakened** from required (min 3 chars) to optional (min 2 chars). The field is still validated for length, but it can be empty. |
| `google_maps_api_key` | When set, adds extra required fields on top of the base set — see below. |

### Field-level defaults (when no setting modifies them)

| Field | Type | Default rule |
|---|---|---|
| First name, Last name | text | Required, **min 2 / max 191 chars**. Single-character names are rejected. |
| Country | text | Required. |
| State | text | Conditional via `checkout_hide_state_iso2` / `checkout_hide_state_name`. |
| City (`locality`) | text | Required. |
| Street | text | Conditional via `checkout_hide_street_name`. |
| Street number | text | Conditional via `checkout_hide_street_number`. |
| City postal code | text | Required (min 3 chars by default; min 2 chars when `post_code_not_required` is ON). |
| Additional address info | text | Optional by default; can be made Required via `checkout_hide_additional_information`. |
| Phone | country-code phone | Conditional via `checkout_hide_phone`. Validated by libphonenumber against `country.iso2`. |

### Google-Maps-extra required fields

When `google_maps_api_key` is configured in [[settings-cart]], the following ADDITIONAL fields become required at validation:

- `country.iso2`
- `latitude`
- `longitude`
- `locality`
- `text` (the formatted text snapshot — see [[customer-shipping-address-save-hooks]])

Without a key, the admin form is strictly manual entry — these fields are not enforced.

## Business rules

### Name field minimum: 2 characters

`first_name` and `last_name` require **min 2 chars / max 191 chars**. Single-character names are rejected with a validation error. This applies even when the store has loose checkout-hide settings — there is no setting that lowers the name minimum.

### `post_code_not_required` is a global weakening, not a per-field hide

The setting does NOT hide the post-code field. It changes the minimum-length rule from 3 to 2 and makes the field optional (can be empty). The field is still rendered and still validated for length when filled.

### `checkout_hide_*` values map to validation rules

- `required` → the field must be present and pass its type / length rules.
- `optional` → the field can be empty; when present, type / length rules still apply.
- `hidden` → the field is not shown on the storefront checkout AND the validator does NOT require it when missing. The admin-side modal still renders it for completeness — but missing values won't trigger errors.

### Geo-name resolution is part of validation

When the modal posts an address that came from the autocomplete (with a Google place ID), the validator hits the platform's geo-names endpoint to resolve the place to a CloudCart city / state / country record. If resolution fails, the validator returns `geo_name_city_id` or `city_id` errors — the modal shows the geo-error banner *"Currently the address can not be saved, please try again later, or contact our support team."* See [[customer-shipping-address-google-maps]] for the geo-error UI.

### Bulk delete validates each ID exists

Bulk delete validates every ID against the actual shipping-address table — any non-existent ID fails the **entire batch**. Combined with the default-address delete-protection (see [[customer-shipping-address-defaults]]) — any ID matching the customer's current default also fails the entire batch — bulk delete needs careful ID curation.

### Two stores can have different required sets

Because validation reads live store settings, two CloudCart stores using the same admin modal can require different fields. For Bulgarian stores with a tight checkout config, Phone may be required; for international stores with a looser config (e.g., `checkout_hide_phone = optional`), Phone may be skippable. Support tickets like *"the same address won't save on Store A but saves on Store B"* almost always trace back here.

### Validation runs the same way on JSON-API v2

The same validator runs on POST / PATCH through [[customer-shipping-address-api]] — the API does NOT bypass the `checkout_hide_*` rules. So programmatic clients (ERP integrations, custom dashboards) must respect the same store-configurable required set.

### Side effects

Validation errors return HTTP 422 with field-by-field messages. On the modal, the central error store surfaces each error next to the offending field. On the API, errors return as a structured JSON-API v2 error response — see [[json-api-v2]].

## Related

- [[customers-details-shipping-addresses]] — hub.
- [[customer-shipping-address-modal]] — the modal that surfaces validation errors field-by-field.
- [[customer-shipping-address-google-maps]] — the autocomplete that drives the geo-name resolution leg of validation.
- [[customer-shipping-address-api]] — the JSON-API v2 path that runs the same validator.
- [[customer-shipping-address-save-hooks]] — the `text` snapshot recompute that satisfies the Google-Maps-extra `text` required field.
- [[settings-cart]] — where every `checkout_hide_*` + `post_code_not_required` + `google_maps_api_key` setting lives.

## Open questions

None.
