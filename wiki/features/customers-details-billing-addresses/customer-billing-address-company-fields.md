---
type: feature
nav_path: "Customers → Customer details → Billing addresses → Company details"
route_name: customers-billing-addresses.new
route_path: /admin/customers-new/details/:id/billing-addresses
aliases: ["B2B fields", "Company details", "Company name", "MOL", "BULSTAT", "Company VAT", "Фирмени данни"]
tags: [customers, addresses, billing, b2b]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (list, modal, VIES, defaults, save hooks, storage, API).

# Customer billing address — Company details (B2B fields)

## Purpose

The four **B2B-only fields** that distinguish a billing address from a shipping address: company name, company owner, company registration number, and company VAT. They are the data the merchant prints on a legal invoice when selling to a business — and the data CloudCart's VIES check validates against the EU registry. For B2C customers the entire section is left blank.

## Where to find it

In the **Company details** card of the Add / Edit billing address modal — see [[customer-billing-address-modal]]. The card is hidden on shipping addresses ([[customers-details-shipping-addresses]]).

## What the merchant can do here

- Fill in any subset of the four company fields. None is hard-required by default — see Business rules below.
- Leave the whole card blank to produce a B2C-style invoice (just person name + address).
- Edit any of the four fields on an existing billing address — re-saving runs the validator + (when applicable) re-checks VIES.

### What the merchant CANNOT do here

- Fill in only `company_name` without `company_vat` (or vice-versa) — they are coupled at the server validator. Either both filled, or neither.
- Make `company_mol` or `company_bulstat` conditionally required from this card — they are required only when the per-store `checkout_hide_company_mol` / `checkout_hide_company_bulstat` settings on [[settings-cart]] are set to `required`.

## Settings & fields

| Field | DB column | UI label | Required when | Validation | Max length |
|-------|-----------|----------|---------------|------------|------------|
| Company name | `company_name` | Company name | `checkout_hide_company_name = required` OR `company_vat` is filled (server-coupled) | text | 191 |
| Company owner | `company_mol` | Company owner | `checkout_hide_company_mol = required` | text | 191 |
| Company registration number | `company_bulstat` | Company registration number | `checkout_hide_company_bulstat = required` | text | 191 |
| Company VAT identification number | `company_vat` | Company VAT identification number | `checkout_hide_company_vat = required` OR `company_name` is filled (server-coupled). Country-prefix + VIES checks when `checkout_validate_company_vat` is ON (see [[customer-billing-address-vies-validation]]) | text + country-prefix + VIES | 191 |

## Business rules

### Per-country label conventions

The labels "Company owner" and "Company registration number" map to the Bulgarian concepts **MOL** (Materially-Responsible Person) and **BULSTAT** (company-registration ID). The UI labels stay generic in English / other languages — the merchant interprets them according to their country's invoice law. Storage uses the Bulgarian-named columns regardless of locale.

### Independent optionality (with one exception)

Three of the four fields — `company_name`, `company_mol`, `company_bulstat` — are independently optional. The merchant can fill any combination. Some merchant countries' invoice law requires the data grouped, but the platform does NOT enforce that grouping itself — the merchant is responsible for filling the fields they legally need.

### The `company_name ↔ company_vat` coupling

The one exception to independent optionality. The server-side `vat_validation` extension enforces a bidirectional rule:

- Filling `company_name` makes `company_vat` required (and vice-versa).
- Both blank → OK (B2C invoice).
- Both filled → OK (B2B invoice; VIES runs when its other gating conditions hold).
- One filled, the other blank → REJECTED with the field-level validation error.

The other two fields (`company_mol`, `company_bulstat`) are NOT part of this coupling.

### VAT prefix must match the country

Before VIES is even called, the validator confirms the VAT number's first 2 characters match the address country code. Special case: Greece uses `EL` as the VAT prefix instead of `GR`. A French address with a German-prefixed VAT is rejected before VIES runs. See [[customer-billing-address-vies-validation]] for the full prefix + cache mechanics.

### Used by invoice rendering

The invoice / credit note rendering pulls the four company fields from the customer's default billing address at order placement time. If the customer changes any company field AFTER an order is placed, the original order's invoice retains its snapshot — see [[customer-billing-address-storage]] for the snapshot model. See [[settings-invoicing]] for the invoice template.

### Used by tax matching

The address country ISO is matched against VAT geo-zones via the `activeByGeoZones` scope — this is how the invoice rendering decides which tax rate to apply (see [[settings-taxes]]).

## Programmatic access

All four company fields are exposed on the JSON-API v2 endpoints for billing addresses — see [[customer-billing-address-api]]. The `company_name ↔ company_vat` interlock and the VIES gating apply identically to API writes.

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-modal]] — the modal that exposes these fields.
- [[customer-billing-address-vies-validation]] — the EU VIES check the `company_vat` field triggers.
- [[customer-billing-address-save-validation]] — the conditional `checkout_hide_*` rules that promote these fields from optional to required per store.
- [[customer-billing-address-api]] — JSON-API v2 representation of the four fields.
- [[settings-invoicing]] — the invoice template that prints these fields.
- [[settings-taxes]] — VAT geo-zones evaluated against the billing-address country.

## Open questions

- Confirm whether some merchant countries' invoice law is enforced by a per-locale plugin layered on top of the base `vat_validation` extension (verify).
