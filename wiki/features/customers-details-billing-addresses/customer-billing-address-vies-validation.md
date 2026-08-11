---
type: feature
nav_path: "Customers → Customer details → Billing addresses → VIES validation"
route_name: customers-billing-addresses.new
route_path: /admin/customers-new/details/:id/billing-addresses
aliases: ["VIES VAT check", "EU VAT validation", "Company VAT validation", "VIES 7-day cache", "Invalid company tax"]
tags: [customers, addresses, billing, vat, vies, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers-details-billing-addresses]]. See the hub for related aspects (list, modal, company fields, defaults, save hooks, storage, API).

# Customer billing address — VIES VAT validation

## Purpose

The EU VIES (VAT Information Exchange System) check the platform runs against the `company_vat` field on a billing address. It validates that the supplied VAT number is registered with the customer's EU member state. Despite older docs implying VIES only runs at checkout, the platform actually runs VIES at **save time** on the billing address — when four gating conditions all hold.

## Where to find it

The check runs transparently — there is no merchant-facing screen for it. Outcomes surface as:

- A field-level validation error on `company_vat` (e.g. *"Invalid company tax"*) when the save is rejected.
- A successful save with the validated VAT data persisted to the address row (when the check passes).
- A successful save with `vies.valid = false` persisted to the row (when the platform stores anyway — see Business rules below).

The merchant configures the master switch under [[settings-cart]] → `checkout_validate_company_vat` (default ON).

## What the merchant can do here

- Turn VIES enforcement ON / OFF globally via the `checkout_validate_company_vat` setting on [[settings-cart]].
- Save a billing address — the platform decides at save-time whether to call VIES based on the four gating conditions.
- Re-save the same address within 7 days — the cached VIES result is reused.
- Force a VIES refresh — change the VAT number (the validator treats VAT as "dirty") OR wait 7 days and re-save.

### What the merchant CANNOT do here

- Manually trigger a VIES refresh from the UI — there is no "Re-check VIES" button.
- See the raw VIES response object from the admin UI — it lives in the `vies` JSON column on the address row.
- Override / bypass VIES for one specific customer — the setting is store-wide.

## Settings & fields

| Setting / column | Where | Default | What it does |
|------------------|-------|---------|--------------|
| `checkout_validate_company_vat` | [[settings-cart]] | ON | Master switch; OFF skips VIES entirely. |
| `company_vat` (input) | Billing address modal | empty | The VAT number to validate. |
| `vies` (storage) | Address row, JSON column | `null` | Stores the VIES result object `{countryCode, vatNumber, requestDate, valid, name, address, checkDate}`. |

## Business rules

### Four gating conditions (ALL must hold)

VIES runs at save-time when:

1. `checkout_validate_company_vat` on [[settings-cart]] is ON.
2. `company_vat` has a non-empty value.
3. The address `country_iso2` is in the EU country list (config `vat.EU`).
4. The first 2 characters of the VAT number match the country code. **Special case:** Greece uses `EL` as the VAT prefix instead of `GR`.

If any one of these fails, VIES is skipped silently. A non-EU country, an empty VAT, the setting OFF, or a mismatched prefix all bypass the call.

### Outcomes

| VIES result | Persisted `vies.valid` | Save accepted? |
|-------------|------------------------|----------------|
| `valid: true` | `true` (plus name + address + checkDate) | Yes — row saves silently. |
| `valid: false` | `false` | **Depends on endpoint** — see "Two endpoints, two behaviours" below. |
| Service unreachable (an error) | `false` (defaults) | Yes — exception is swallowed, row saves with default `valid: false`. |

### Two endpoints, two behaviours

The save itself does NOT fail at the saving-hook level when VIES returns invalid — the result is stored and the hook returns. The actual reject behaviour depends on the calling endpoint's form-validator path:

- **Admin REST endpoint** (`POST /admin/api/core/customers/billing-address` from the modal) — runs the `vat_validation` extension, which rejects the save with *"Invalid company tax"* (`sf.err.invalid.company_tax`) when VIES returns invalid.
- **Legacy JSON-API path** — does NOT run the `vat_validation` extension; stores the data with `vies.valid = false` and returns 200. The merchant can create an invalid-VAT B2B record this way — the block kicks in only at checkout.

This is the "VIES runs at checkout, not at save" doc note that was partially correct: the legacy JSON-API path still stores invalid VATs, deferring the block to order placement.

### 7-day cache + re-collect rules

The stored `vies` object includes a `checkDate`. On every read the platform validates the stored object against a 7-day TTL — if older than 7 days, it gets re-collected and re-stored on the next save.

Re-saving within 7 days hits the saving hook's checks: if the VAT is **not dirty** AND the existing data is still valid AND `valid: true`, the round-trip is skipped (the platform reuses the cached object).

If `company_vat` is dirty (changed since last save), OR the previous result was `valid: false`, VIES is re-called on save regardless of cache age.

### VAT prefix is country-bound

Before VIES is called, the validator confirms the VAT number's first 2 characters match the address country code. A French address with a `DE`-prefixed VAT is rejected before VIES is even called. Greece is the lone exception — its VAT prefix is `EL`, not `GR`.

### VIES does NOT run at checkout time anymore (correction)

Earlier docs implied VIES only ran at checkout. The platform now runs VIES at billing-address save when the four gating conditions hold. The setting name `checkout_validate_company_vat` is historical — the actual check is at the address layer, not at order placement. Order placement re-uses whatever the address-level VIES has stored (subject to the 7-day cache rule).

## Programmatic access

API writes go through the JSON-API v2 path described in [[customer-billing-address-api]]. The four gating conditions and the 7-day cache apply identically to API writes — but the validator path differs between the admin REST and legacy JSON-API endpoints (see "Two endpoints, two behaviours" above).

## Related

- [[customers-details-billing-addresses]] — hub.
- [[customer-billing-address-company-fields]] — the `company_vat` field and the `company_name ↔ company_vat` coupling that gates this check.
- [[customer-billing-address-save-validation]] — the broader save-time validation pipeline VIES runs inside.
- [[customer-billing-address-storage]] — the `vies` JSON column where the result is persisted.
- [[customer-billing-address-api]] — JSON-API v2 endpoints and the two-endpoint behaviour gap.
- [[settings-cart]] — `checkout_validate_company_vat` master switch.
- [[settings-taxes]] — downstream tax computation that depends on the address geo-zone (not on VIES validity).

## Open questions

- Confirm whether an error is logged anywhere the merchant can see (or only in backend logs) (verify).
- Confirm whether the 7-day TTL is calendar days or wall-clock seconds (verify).
