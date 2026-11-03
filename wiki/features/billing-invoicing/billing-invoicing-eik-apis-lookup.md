---
type: feature
nav_path: "Profile → Billing → Invoice details → EIK / APIS lookup"
route_name: admin.billing.invoicing
route_path: /admin/billing/invoicing
aliases: ["EIK auto-fill", "APIS Trade Register lookup", "Bulgarian company ID lookup", "EIK validator", "EGN sole trader"]
tags: [billing, invoicing, eik, apis, bulgaria, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[billing-invoicing]]. See the hub for the other aspects (fields, VAT/VIES, country-driven form, save flow, Vue checkout editor).

# Invoice details — EIK / APIS lookup (Bulgaria)

## Purpose

Document the **Bulgarian branch** of the invoice-details auto-fill: when the merchant picks `country = BG` and types a 9-digit or 13-digit Bulgarian company ID, the platform validates it locally with the Trade Register check-digit algorithm and then calls the **APIS Trade Register** service to pull the official company record (name, VAT registration status, address, responsible person). The merchant gets the registry-canonical data instead of typing it.

## Where to find it

Same panel as the hub. The lookup fires automatically while the merchant types into the **Company ID** field with `country = BG` selected.

## What the merchant can do here

- Type an EIK (9 or 13 digits) or an EGN (10 digits, for sole traders) into Company ID.
- See Company name, VAT, Address auto-fill from the registry.
- Edit MOL freely even after the auto-fill (it is NOT locked — see [[billing-invoicing-country-driven-form]]).
- See *"Invalid Company ID"* if the check-digit algorithm fails or the registry returns no match.

## Settings & fields

The relevant fields are documented on [[billing-invoicing-fields-and-validation]]. Field-level notes for this surface:

- **Company ID** — the only freely-editable identifier field while `country = BG`. Accepts 9-digit EIK, 13-digit EIK, or 10-digit EGN.
- **Company / VAT / Address** — locked readonly once a successful APIS call returns.
- **MOL `name`** — pre-filled from the registry's responsible-person value but stays editable; the merchant can override it.

## Business rules

### Trigger: country = BG + ≥ 9 digits typed

When `country = BG` and the merchant types a value of 9 or more digits into Company ID:

1. The platform's `validateCompanyId(company_id)` model method runs.
2. The local EIK check-digit validator runs **first** — invalid-format EIKs are rejected client-side without contacting the registry.
3. If the local validator passes, an AJAX lookup goes to the APIS Trade Register integration with that EIK.
4. The service returns the registry record — company name, VAT registration status, address (street + number + city with Bulgarian-language formatting like `жк`, `бл.`, `вх.`, `ет.`, `ап.`), and the responsible person.
5. The platform pastes those into the form's Company, VAT, Address, and MOL inputs and marks them readonly per the `eikBg` map: `{ company: 1, vat: 1, address: 1 }`.
6. The MOL `name` field is NEVER locked — only its default value is written from the registry; the merchant can edit it.
7. After a successful lookup, the form sets `ignoreVarValidation = true` so the subsequent VAT-watcher does NOT re-trigger VIES (which would conflict with the APIS-filled VAT). (verify)

### EIK validation algorithm (BG, purely local — no network)

The EIK validator uses the standard Bulgarian Trade Register check-digit algorithm:

- **9-digit number** — two weighted sums against weight vectors `[1,2,3,4,5,6,7,8]` and `[3,4,5,6,7,8,9,10]`; the result modulo 11 (or 0 if the modulo is 10) must equal the last digit.
- **13-digit number** — the first 9 digits are validated as above; the trailing 4 digits are validated by a separate weighted sum against `[2,7,3,5]` and `[4,9,5,7]`.

Numbers that do not pass this check never reach the APIS call.

### EGN fallback for sole traders

The 10-digit Bulgarian personal-identity number (EGN), used by sole traders billing under their own name, is accepted by an additional EGN validator. Sole traders enter their EGN in the same Company ID field; the platform routes it through the EGN check rather than the EIK algorithm.

### APIS endpoint

The platform calls its APIS integration at `https://regdata.apis.bg/api/v1/Data/Fetch/...` with the validated EIK. The merchant never sees this URL — the call is server-side from the form's auto-fill handler.

### APIS address formatting

APIS returns the address as multiple components (street, number, housing estate, block, entrance, floor, apartment). The platform assembles them into a single line using the Bulgarian-language prefixes — `жк` (residential complex), `бл.` (block), `вх.` (entrance), `ет.` (floor), `ап.` (apartment) — so the address printed on the CloudCart-issued invoice matches the official Trade Register formatting.

### Outside-BG: secondary APIS enrichment on save

When the country is NOT BG, the save handler still tries APIS as a silent backend enrichment step against the merchant's `company_id` (and falls back to the `vat` field). If APIS returns data, the platform replaces the country code from the request with the country from APIS's response, and fills additional fields. The merchant doesn't see this happen. See [[billing-invoicing-save-flow]].

### `Invalid Company ID` message

The validator surfaces *"Invalid Company ID"* in two cases:

- The EIK number failed the local check-digit validation (purely local, no registry hit).
- The BG Trade Register said the EIK does not exist (`Invalid` returned by APIS after a syntactically-valid number).

The merchant cannot save the form until they fix the value.

## Related

- [[billing-invoicing]] — hub.
- [[billing-invoicing-fields-and-validation]] — the full fields table including `company_id` validation rules.
- [[billing-invoicing-vat-vies-lookup]] — the parallel non-BG VAT path via VIES + HMRC.
- [[billing-invoicing-country-driven-form]] — the `eikBg` / `countryBg` readonly maps.
- [[billing-invoicing-save-flow]] — the silent APIS enrichment that runs on save when country ≠ BG.

## Open questions

- The exact request and response payload of the APIS Trade Register integration is not documented in this aspect (deliberately — outside the merchant-facing scope). (verify)
