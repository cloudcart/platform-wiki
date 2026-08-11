---
type: feature
nav_path: "Profile → Billing → Invoice details → VAT / VIES lookup"
route_name: admin.billing.invoicing
route_path: /admin/billing/invoicing
aliases: ["VAT auto-fill", "VIES lookup", "HMRC VAT lookup", "Per-country VAT pattern", "Invalid VAT ID", "VAT outage"]
tags: [billing, invoicing, vat, vies, hmrc, eu, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[billing-invoicing]]. See the hub for the other aspects (fields, EIK/APIS, country-driven form, save flow, Vue checkout editor).

# Invoice details — VAT / VIES lookup (non-BG)

## Purpose

Document the **non-Bulgaria branch** of the invoice-details auto-fill: when the merchant picks any country other than BG and types a VAT ID, the platform calls the EU VIES service (or HMRC for the UK) to verify the VAT and pull the official company name + address. Same idea as the BG / APIS path but the upstream service is different. This page also catalogues the outage-handling and per-country VAT pattern rules.

## Where to find it

Same panel as the hub. The lookup fires automatically while the merchant types into the **VAT ID** field with any non-BG `country` selected.

## What the merchant can do here

- Type a VAT ID in `<country-code><digits>` format (e.g. `DE123456789`).
- See Company name, Company ID, Address auto-fill from VIES.
- Leave the VAT field blank if they are a sole trader below the VAT threshold (see "EU VAT outage / sole-trader fallback").
- See *"Invalid VAT ID"* or the system-unreachable message if the call fails.

## Settings & fields

The relevant field is `vat` — see [[billing-invoicing-fields-and-validation]] for the full table. Field-level notes for this surface:

- **VAT ID** — the primary identifier when `country ≠ BG`. Validated against VIES (or HMRC for GB) on every keystroke (debounced).
- **Company / Company ID / Address** — locked readonly after a successful VIES call per the `vatNoBg` map: `{ company: 1, address: 1, company_id: 1 }`.

## Business rules

### Trigger: country ≠ BG + VAT field edited

When `country ≠ BG` and the merchant types into VAT:

1. The platform's `validateVat(vat)` model method runs (debounced inside the validator).
2. The per-country VAT pattern check runs first — a wrong-format VAT is rejected before reaching VIES.
3. The platform calls the EU VIES service at `https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl` with the VAT number.
4. If VIES returns `valid = true`, the platform fills Company, Company ID, and Address from the VIES response and locks them.
5. If VIES returns `valid = false`, the merchant sees *"Invalid VAT ID"* and the save is rejected.
6. If VIES is unreachable, the merchant sees *"Currently, the VAT number validation system is not working. Please try again in a few minutes"* — the save is rejected.

### VIES validation is SKIPPED in three cases

- The country is `BG` — covered by the EIK / APIS path; see [[billing-invoicing-eik-apis-lookup]].
- The country is `CH` (Switzerland) — Switzerland is not in the VIES system; VAT entry is optional and not validated.
- The country is not on VIES's "collects VAT" list (most non-EU countries) — VAT field is treated as optional and not validated.

### Special handling for `GB` (United Kingdom)

After Brexit, the UK is no longer on VIES. The platform calls HMRC's own VAT lookup API instead at `/organisations/vat/check-vat-number/lookup/<number>` — UK merchants get the same auto-fill experience, just via a different upstream. No merchant-visible difference, but the verification path is HMRC, not VIES.

### Per-country VAT pattern enforcement

VAT IDs must match the EU's per-country format. Examples:

- `AT` — `U` + 8 alphanumerics.
- `BG` — 9 or 10 digits.
- `DE` — 9 digits.
- `FR` — 2 alphanumerics + 9 digits.
- `IT` — 11 digits.
- `PL` — 10 digits.

A wrong-format VAT is rejected before reaching VIES.

### EU VAT outage / sole-trader fallback

The save validation rules do NOT require the `vat` field — EU sole traders below their country's VAT threshold can save the form with the VAT field left empty. Only the FORMAT check fires when the field is filled. So:

- If VIES is unreachable AND the merchant entered a VAT → the save fails with the *"system unreachable"* message; the merchant must retry later. VIES outages do not let the merchant bypass validation when they have entered a value.
- If the merchant leaves VAT empty → the save proceeds normally (the registry lookup is skipped; Company / Address fields stay as the merchant typed them).

### Hungary (HU) bypasses VIES on the Vue checkout API path

The modern Vue checkout API (`POST /admin/api/core/billing/invoicing`) treats Hungary as a special case — for HU it bypasses the default `vat_number` rule and applies a dedicated Hungarian VAT-format validator (`HU` + 8 digits typically) without consulting VIES. The Smarty `/admin/billing/invoicing` route does NOT have this carve-out — it always runs the `vat_number` rule. See [[billing-invoicing-vue-checkout-editor]].

### VIES values overwrite typed values on save

When VIES returns valid VAT details on save (and country ≠ BG), the platform overwrites the submitted `company` and `address` fields with the VIES values, even if the merchant typed something different. VIES is treated as authoritative for EU VAT records. See [[billing-invoicing-save-flow]] for the full save-time field-rewrite sequence.

## Related

- [[billing-invoicing]] — hub.
- [[billing-invoicing-fields-and-validation]] — the full fields table including the `vat` validation rule.
- [[billing-invoicing-eik-apis-lookup]] — the parallel BG path via the APIS Trade Register.
- [[billing-invoicing-country-driven-form]] — the `vatNoBg` / `countryNoBg` readonly maps; how the VAT-watcher is wired.
- [[billing-invoicing-save-flow]] — VIES values overwriting typed values on submit.
- [[billing-invoicing-vue-checkout-editor]] — Hungary's `VatIdHuRule` carve-out on the Vue API path.

## Open questions

None.
