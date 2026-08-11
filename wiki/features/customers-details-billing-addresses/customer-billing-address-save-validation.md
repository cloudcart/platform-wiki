---
type: feature
nav_path: "Customers → Customer details → Billing addresses → Save hooks & validation"
route_name: customers-billing-addresses.new
route_path: /admin/customers-new/details/:id/billing-addresses
aliases: ["Billing address save hooks", "Billing address validation", "checkout_hide_company_*", "Phone E.164 normalisation", "Country ISO normalisation"]
tags: [customers, addresses, billing, validation, save-hooks]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (list, modal, company fields, VIES, defaults, storage, API).

# Customer billing address — Save hooks & validation

## Purpose

The pipeline that runs on every billing-address save: form validation (with conditional rules driven by store-level `checkout_hide_*` settings) plus the saving-lifecycle hooks that normalise data and write a formatted text snapshot. VIES sits inside this pipeline as its own concern — see [[customer-billing-address-vies-validation]].

## Where to find it

The hooks run server-side on every save from:

- The Add / Edit modal — see [[customer-billing-address-modal]].
- The Set-as-default endpoint (re-saves the row).
- The JSON-API v2 endpoints — see [[customer-billing-address-api]].

The merchant tunes the validation behaviour from [[settings-cart]] via the `checkout_hide_*` settings (per field: `required` / `optional` / `hidden`).

## What the merchant can do here

- Configure per-field required-status from [[settings-cart]] — see Settings & fields.
- Save an address from any of the three entry points above — the same hooks run regardless.
- Re-save without changing fields — the hooks re-run (text snapshot recomputes, VIES respects its 7-day cache).

### What the merchant CANNOT do here

- Skip the four invariant hooks (phone normalisation, lat/lng, country ISO, text snapshot). They always run on every save.
- Manually edit the `text` snapshot column — it is computed from the structured fields.
- Disable phone normalisation — every saved phone is forced to E.164 if libphonenumber accepts it.

## Settings & fields

### Saving-lifecycle hooks (every billing-address save)

| Hook | What it does |
|------|--------------|
| **Phone normalisation** | libphonenumber → E.164 (e.g. `+359888123456`). The original input format is replaced before save. The platform also stores phone_international, phone_national, and phone_rfc3966 representations as derived fields. |
| **Lat / lng auto-fill** | When `latitude` + `longitude` are missing on save, the platform calls Google Maps geocoding as a fallback to populate them from the city + postcode. |
| **Country ISO normalisation** | `country_iso2` is upper-cased; `country_iso3` is derived (ISO 3166-1 alpha-3); `country_name` is populated from the system locale at save time (French admins see French names, English admins see English names). |
| **Address text snapshot** | A formatted text representation of the address is stored in the `text` column at save time. This is what shows in lists and API responses. Editing any field re-formats and re-stores it. |
| **VIES VAT validation** | Runs INSIDE this pipeline when the four gating conditions hold — see [[customer-billing-address-vies-validation]]. |

**No per-courier mapping hook** — that's shipping-only (billing has no per-carrier mapping needs because it's used for invoicing and tax, not for delivery routing). See [[customers-details-shipping-addresses]] for the shipping-specific courier-mapping save-hook chain.

### Conditional validation from store settings

The platform code form validator reads several `checkout_hide_*` settings from [[settings-cart]] and adjusts validation per field. Each setting accepts three values: `required`, `optional`, or `hidden`.

| Setting (from [[settings-cart]]) | Field affected |
|----------------------------------|----------------|
| `checkout_hide_first_name` | First name |
| `checkout_hide_last_name` | Last name |
| `checkout_hide_phone` | Phone |
| `checkout_hide_street_name` | Street |
| `checkout_hide_street_number` | Street number |
| `checkout_hide_additional_information` | Additional address info |
| `checkout_hide_state_iso2` / `checkout_hide_state_name` | State |
| `checkout_hide_company_name` | Company name |
| `checkout_hide_company_vat` | Company VAT |
| `checkout_hide_company_bulstat` | Company registration number |
| `checkout_hide_company_mol` | Company owner |
| `post_code_not_required` | Post code (toggles from required to optional, min 2 chars when required) |

The admin form's "required" markers are dynamically computed from these settings, not hard-coded. Two CloudCart stores can have different required-vs-optional behaviour for the same field depending on their checkout configuration.

### Hard validation rules (always enforced)

| Rule | Detail |
|------|--------|
| Name minimum length | First / Last name require min 2 characters (max 191). Single-character names are rejected. |
| Country ISO format | Must be a valid 2-letter ISO 3166-1 alpha-2 code. Free-form country values rejected. |
| Phone country code | Validated against ISO 3166. |
| Google Maps mode | When a Google Maps API key is configured, additional fields become required: `country.iso2`, `latitude`, `longitude`, `locality`, `text`. Without a key, the manual fields alone suffice. |
| Company name ↔ Company VAT coupling | Server-coupled — see [[customer-billing-address-company-fields]] for the bidirectional rule. |

## Business rules

### Hook order matters for VIES

Phone normalisation, lat/lng, country ISO normalisation, and the text snapshot all run before VIES is called. VIES then reads the normalised `country_iso2` to decide whether the address is in the EU list — so an address saved with `bg` is correctly identified as EU after the upper-casing hook runs. See [[customer-billing-address-vies-validation]].

### Conditional fields apply to admin saves AND API writes

The `checkout_hide_*` rules from [[settings-cart]] apply to both:

- Admin modal saves (POST / PATCH `/admin/api/core/customers/billing-address`).
- JSON-API v2 writes (see [[customer-billing-address-api]]).

There is no "admin bypass" — even an admin merchant cannot save an address that violates a `required` rule, because the rule is enforced at the request validator (not at the UI level).

### `vat_validation` extension splits across endpoints

The validator extension that emits *"Invalid company tax"* runs on the admin REST endpoint but NOT on the legacy JSON-API path. This is the same gap documented under VIES — see [[customer-billing-address-vies-validation]] for the two-endpoint behaviour comparison.

### Text snapshot is read-only downstream

Downstream consumers (list table, JSON-API responses, invoice rendering, customer notification emails) all read the `text` snapshot rather than re-formatting the structured fields. Saving any field change recomputes and re-stores the snapshot before the new save returns.

## Programmatic access

The same hooks + validation run on JSON-API v2 writes. See [[customer-billing-address-api]] for the endpoint surface and the legacy-vs-admin-REST behaviour gap.

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-modal]] — the modal that triggers this pipeline.
- [[customer-billing-address-vies-validation]] — VIES VAT check inside this pipeline.
- [[customer-billing-address-company-fields]] — the company-field coupling enforced by this pipeline.
- [[customer-billing-address-storage]] — the `text` snapshot column and the country-ISO storage shape.
- [[customer-billing-address-api]] — JSON-API v2 endpoint parity.
- [[settings-cart]] — the `checkout_hide_*` settings + `post_code_not_required` + Google Maps API key.
- [[customer-shipping-address-save-hooks]] — sibling concept for shipping, with the extra per-courier mapping hook.

## Open questions

- Confirm whether libphonenumber rejection (i.e. an unparseable phone) returns a field-level error or silently leaves the original input (verify).
