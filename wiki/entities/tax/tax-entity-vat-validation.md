---
type: entity
nav_path: "Entity → Tax / Fee → VAT validation (external services)"
aliases: ["VAT validation", "VIES", "HMRC VAT check", "APIS Trade Register", "B2B VAT validation", "Reverse charge"]
tags: [entity, taxes, vat, validation, vies, hmrc, b2b]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax]]. See the hub for the other aspects (attributes, VAT vs Fee, overrides, order snapshot, business rules).

# Tax / Fee — external VAT-number validation

## Identity

When a customer enters a VAT number at checkout (for B2B / reverse-charge invoicing), the platform validates the number against an **external** tax-authority service before the order is placed. The validation result is stored on the customer's address row and influences the tax engine's reverse-charge decision. This is a **synchronous, fail-soft** check — if the external service is unreachable, the order still saves but the validation result is recorded as failed.

The Tax / Fee entity itself does not store VIES results — they live on the customer's address row attached to the [[order]] / [[customer]]. But the validation outcome feeds the engine's `isWithVat` decision, which then drives which Tax rule applies and whether the rule's no-VAT wording prints on the invoice.

## Aliases

- **VAT validation** — the umbrella term in the admin UI.
- **VIES** — EU-wide VAT validation service (EU non-BG).
- **HMRC VAT check** — UK validation endpoint.
- **APIS Trade Register** — Bulgaria-specific service.
- **B2B VAT validation** — merchant-facing phrasing for the same thing.
- **Reverse charge** — the legal mechanism the validation enables.

## Key Attributes — service mapping per country

| Country (`country_iso2`) | Service |
|--------------------------|---------|
| **Bulgaria (BG)** | APIS Trade Register |
| **EU non-BG** (AT, BE, HR, CY, CZ, DK, EE, FI, FR, DE, GR/EL, HU, IE, IT, LV, LT, LU, MT, NL, PL, PT, RO, SK, SI, ES, SE) | VIES |
| **Great Britain (GB)** | HMRC VAT-check API |
| **Switzerland (CH)** | None — accepted but NOT validated |

The Swiss case is intentional: the VAT field is accepted from CH customers but the `vies` validation object on the address remains empty. Swiss B2B sales rely on the merchant's own offline verification.

## When validation fires

All three conditions must be true:

1. The store setting **`checkout_validate_company_vat = 1`** on [[settings-cart]] (default ON).
2. The customer's `country_iso2` is in the EU list (or GB for HMRC, BG for APIS).
3. The VAT number **starts with the country prefix** (e.g., `BG123456789` for Bulgaria).

If any condition is false, no external call is made. Format-only validation is the fallback.

## What gets stored on the customer address

The response is stored on the customer's address row (attached to the order / customer record) in a `vies` object:

- `countryCode`
- `vatNumber`
- `requestDate`
- `valid` (boolean)
- `name` (returned by VIES / HMRC)
- `address` (returned by VIES / HMRC)
- `checkDate`

## Validation messages shown at checkout

- *"VAT number is invalid"* — the external service confirmed the number is not registered.
- *"VAT service unreachable"* — the external service did not respond.

## Fail-soft behaviour

VIES and HMRC requests are **synchronous on checkout** — no queueing or retry. If the external service is unreachable:

- The platform returns the *"VAT service unreachable"* message.
- The failed result is stored on the order.
- The order is **NOT blocked** — it saves with the unvalidated VAT number.
- The merchant can manually verify offline.

This is by design — external service downtime should not block sales.

## GB / HMRC specifics

The platform calls the HMRC VAT-check API **directly** for GB-prefix VAT numbers (when the customer is in Great Britain). The HMRC response shape is similar to VIES (`valid`, `name`, `address`). Format-only validation is the fallback when HMRC is unreachable — the same fail-soft pattern.

## How validation feeds the tax engine

The validation result influences `isWithVat`:

- **Valid VIES result + EU B2B sale + OSS off** → reverse charge applies; rule's `without_vat_reasons` text prints on the invoice; VAT amount on the line is zero.
- **Valid VIES result + EU B2B sale + OSS ON** → OSS suppresses reverse-charge (see [[tax-oss-semantics]]); destination-country VAT-rule rate applies normally.
- **Invalid / unreachable VAT validation** → reverse charge does NOT apply; the standard VAT rule fires as if the customer were a B2C buyer.

## Reverse-charge configuration on the entity

There is no single *"Enable B2B reverse charge"* toggle on the Tax row. The merchant configures the legal text in `without_vat_reasons` (max 64,000 chars — typical: *"Intra-community supply per Art. 138 Directive 2006/112/EC"*) and relies on VIES validation to flip the `isWithVat` decision at checkout. For non-EU exports, `without_vat_reasons_non_eu` carries the equivalent wording.

## Where it appears

- [[settings-cart]] — `checkout_validate_company_vat` toggle.
- [[checkout-flow]] — the synchronous validation call site.
- [[customer]] — the customer record carries the address row that stores the `vies` object.
- [[order]] — the failed-validation result is stored on the order for support investigation.
- [[tax]] — entity hub.

## Related

- [[tax]] — hub.
- [[tax-entity-attributes]] — `without_vat_reasons` / `without_vat_reasons_non_eu` field rows.
- [[tax-oss-semantics]] — OSS suppresses reverse-charge for EU B2B.
- [[settings-cart]] — `checkout_validate_company_vat` setting.
- [[settings-taxes]] — management screen.
- [[customer]] — address row carrying the `vies` object.
- [[order]] — failed-validation persistence.

## Open Questions

None.
