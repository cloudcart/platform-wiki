---
type: feature
nav_path: "Profile → Billing → Invoice details → Country-driven form"
route_name: admin.billing.invoicing
route_path: /admin/billing/invoicing
aliases: ["Country drives the form", "disabledMapping", "Readonly mapping", "Country watcher", "EIK watcher", "VAT watcher"]
tags: [billing, invoicing, country, readonly, ui-behaviour]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[billing-invoicing]]. See the hub for the other aspects (fields, EIK/APIS, VAT/VIES, save flow, Vue checkout editor).

# Invoice details — country-driven form behaviour

## Purpose

Document the cross-cutting UI rule that makes the *Invoice details* form feel context-aware: the **Country** dropdown sits at the top because it decides which field is primary, which lookup fires, and which fields lock readonly once the lookup completes. Same rule applies on both the Smarty side panel and the Vue checkout editor — though the Vue version exposes more of the wiring under named maps.

## Where to find it

The behaviour is global to the panel — visible the moment the merchant changes Country, types into Company ID, or types into VAT.

## What the merchant can do here

- Change Country at any time to swap which identifier is primary.
- Switch country back to unlock every field that was locked by a previous lookup.
- Type the EIK / VAT to trigger the appropriate auto-fill (BG → APIS; non-BG → VIES; UK → HMRC).
- Edit the **Materially Responsible Person** name freely — it is never locked by any lookup, even when the registry returned a default value.

## Settings & fields

The fields themselves are catalogued on [[billing-invoicing-fields-and-validation]]. This page documents how their **editable / readonly** state shifts as the merchant interacts with the form.

### The `disabledMapping` object (Vue editor)

The Vue form holds a `disabledMapping` object that controls which fields lock after each event:

- `countryBg` — `{ company_id: 0, company: 1, vat: 1, address: 1 }` — when country switches to BG, lock company/vat/address but leave Company ID editable so the merchant can type the EIK.
- `countryNoBg` — `{ company_id: 0, company: 0, vat: 0, address: 0, name: 0 }` — when country switches away from BG, everything unlocks.
- `eikBg` — `{ company: 1, vat: 1, address: 1 }` — after a successful APIS lookup, lock the three auto-filled fields.
- `vatNoBg` — `{ company: 1, address: 1, company_id: 1 }` — after a successful VIES lookup, lock company / address / company_id.

The MOL `name` field is NEVER locked by any of these — even when the registry returns a default value, the merchant can edit it.

### Auto-trigger logic on typing (Vue editor watchers)

- `invoicing.vat` is watched — on every keystroke (debounced inside the validator), if country is non-BG AND the VAT field is editable, calls `model.validateVat(vat)` against VIES (or HMRC for GB). See [[billing-invoicing-vat-vies-lookup]].
- `invoicing.company_id` is watched — when length ≥ 9 AND the field is editable, calls `model.validateCompanyId(company_id)` against APIS. After a successful lookup, sets `ignoreVarValidation = true` so the VAT-watcher does NOT re-trigger VIES against the just-filled VAT. See [[billing-invoicing-eik-apis-lookup]].
- `invoicing.country` is watched — switching country swaps the active map between `countryBg` and `countryNoBg`, immediately re-flipping `disabled` on every field.

The Smarty side panel uses the same conceptual wiring (per-field readonly toggled by the country selector + the AJAX lookups), but exposes fewer named maps.

## Business rules

### Country = BG → Company ID is primary

When `country = BG`:

- **Company ID** becomes the primary identifier and the only freely-editable identifier field.
- The VAT, Company, Address fields wait — they fill in only after the APIS lookup succeeds.
- The merchant typing ≥ 9 digits triggers the APIS call (see [[billing-invoicing-eik-apis-lookup]]).
- Result fields are locked readonly per the `eikBg` map.

### Country ≠ BG → VAT ID is primary

When `country ≠ BG`:

- **VAT ID** becomes the primary identifier.
- The merchant types it, an AJAX lookup goes to VIES (or HMRC for GB), and Company / Company ID / Address auto-fill.
- Result fields are locked readonly per the `vatNoBg` map.

### Switching country back unlocks everything

Switching the country selector unlocks every field — the readonly flag is purely a UI convenience driven by the country selector. The fields revert to editable so the merchant can re-enter for the new country.

### MOL is editable in every state

The MOL `name` field is never readonly. The registry's default MOL value is written into the field on a successful lookup, but the merchant can always override it with whatever name they want printed on the invoice.

### Country picker is filtered for CloudCart GmbH (DE) sites

For DE-invoiced sites (when `siteUser.issuer_company_id === 7` — CloudCart GmbH), the Vue editor's country picker is filtered to **EU countries only** via the `euOnly` computed flag. Merchants on non-CloudCart-GmbH sites see the full ISO list.

### Country picker config (Vue)

- Component: `CountriesComponent`.
- `cols-width="6"`.
- `can-clear="false"` — the merchant cannot leave the country unset.
- Searchable list with flag prefixes.

### Country list comes from the merchant's account on first open

When the Vue `FormDetails` component mounts and no invoicing record exists yet, it pre-fills:

- `invoicing.country = siteUser.country` (the merchant's saved account country).
- `invoicing.email = siteUser.email` (the merchant's account email).

Both can be edited freely before save.

### Country code can be overwritten silently on save

When the country is not BG, the save handler runs an additional APIS lookup against `company_id` (and falls back to `vat`). If APIS returns data, the country code from the request is replaced with the country from APIS's response — so a merchant who typed `DE` but whose company is actually registered in `AT` gets corrected silently. See [[billing-invoicing-save-flow]].

## Related

- [[billing-invoicing]] — hub.
- [[billing-invoicing-fields-and-validation]] — the field-level table this page references.
- [[billing-invoicing-eik-apis-lookup]] — what fires when the merchant types into Company ID at country = BG.
- [[billing-invoicing-vat-vies-lookup]] — what fires when the merchant types into VAT at country ≠ BG.
- [[billing-invoicing-save-flow]] — silent country-code overwriting on save when APIS returns a different country.
- [[billing-invoicing-vue-checkout-editor]] — the Vue editor whose `disabledMapping` object exposes the named maps catalogued here.

## Open questions

None.
