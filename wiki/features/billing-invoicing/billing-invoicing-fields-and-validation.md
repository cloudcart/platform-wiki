---
type: feature
nav_path: "Profile → Billing → Invoice details → Fields & validation"
route_name: admin.billing.invoicing
route_path: /admin/billing/invoicing
aliases: ["Invoice details fields", "Billing invoicing fields", "Invoicing validation messages", "InvoicingRequest"]
tags: [billing, invoicing, fields, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[billing-invoicing]]. See the hub for the other aspects (EIK/APIS lookup, VAT/VIES lookup, country-driven form, save flow, Vue checkout editor).

# Invoice details — fields & validation

## Purpose

Document every field on the *Invoice details* side panel — label, what it controls, required-or-not, validation rules, and the merchant-visible error messages. This is the section the support assistant cites most when a merchant cannot save the form.

## Where to find it

The same panel as the hub: Profile dropdown → Billing → pencil icon on the invoice-details block. Route `POST /admin/billing/invoicing`.

## What the merchant can do here

- Fill the form fields below.
- See per-field validation errors inline.
- See a top-of-screen banner when stored details fail re-validation later.

## Settings & fields

The side panel is a single form with these fields, ordered top to bottom:

| Field | Required | What it does | Validation |
|-------|----------|--------------|------------|
| **Country** (`country`) | yes | Country of the invoiced entity. **Drives the rest of the form** — see [[billing-invoicing-country-driven-form]]. | `required`. Country list (full ISO list, searchable, flag-prefixed). |
| **Company ID** (`company_id`) | yes | Local company-registration number. In BG = the EIK / Bulstat number (9 or 13 digits). Outside BG = whatever the local equivalent is. | `required\|eik`. The `eik` rule is **conditional** — it only enforces real EIK checks when `country = BG`. See [[billing-invoicing-eik-apis-lookup]]. |
| **VAT ID** (`vat`) | only if VIES says the country collects VAT | The EU VAT ID, in `<country-code><digits>` format. For BG this is the EIK digits with `BG` prefix (often left blank — the EIK is enough). | `vat_number`. Validated against EU VIES for EU countries; skipped for BG and Switzerland; skipped for non-VAT-collecting countries. See [[billing-invoicing-vat-vies-lookup]]. |
| **Company or business name** (`company`) | yes | Legal name of the company / sole trader. Printed at the top of every CloudCart-issued invoice. | `required`. Locked (readonly) when auto-filled from a registry. |
| **Address** (`address`) | yes | Full street address (street + number + city + postal code, as one free-text line). Printed below the company name on every invoice. | `required`. Locked (readonly) when auto-filled from a registry. |
| **Materially Responsible Person** (`name`) — labelled "MOL" in BG | no (placeholder says "optional") | Person responsible for the company financially — typically the manager / director. Printed on the invoice. | No format validation; free text. Defaults to the merchant's own user name on first open. Note: the Smarty route's request marks this `required` — see "Required validation on save" below. |
| **Email** (`email`) | yes | Where CloudCart sends the PDF invoice every time. Independent of the merchant's account login email. | `required\|email`. Defaults to the merchant's own user email on first open. |

### Required validation on save (Smarty route)

The Smarty `POST /admin/billing/invoicing` route enforces ALL of these as `required` regardless of country:

- `company_id` — `required|eik` (even outside BG the merchant must provide a company identifier, and the `eik` rule runs on it).
- `company` — legal name (`required`).
- `address` — full address line (`required`).
- `name` — the MOL field (`required`). Note: the UI placeholder says "MOL (optional)" but this route's validator marks it `required`; leaving it blank fails the save with a per-field error.
- `country` — `required`.
- `email` — `required|email`.

If any of these is missing, the save fails and the merchant sees the per-field error. The Vue checkout API surface relaxes two of these (see [[billing-invoicing-vue-checkout-editor]] for the surface-level differences).

### Validation messages

The merchant will see one of these messages when validation fails:

- *"Invalid Company ID"* — the EIK number failed the local check-digit validation OR the BG Trade Register said it does not exist. See [[billing-invoicing-eik-apis-lookup]] for the algorithm.
- *"Invalid VAT ID"* — the VAT number failed the VIES check OR the format does not match the country's expected pattern. See [[billing-invoicing-vat-vies-lookup]].
- *"Currently, the VAT number validation system is not working. Please try again in a few minutes"* — VIES is unreachable. The save is rejected; VIES outages do not let the merchant bypass validation.
- *"You have an invalid invoice details! Please, change them!"* — top-of-screen banner shown elsewhere when the stored invoice details are flagged invalid (the merchant must return here and re-save).

## Business rules

### Fields auto-filled from a registry are locked (readonly)

When the BG EIK lookup or the VIES lookup succeeds, the `company`, `vat`, and `address` fields are flipped to readonly so the merchant cannot drift from the official registry data. The MOL `name` field stays editable — see [[billing-invoicing-country-driven-form]] for the full readonly mapping.

### `vat` field is optional at format level for sole traders

The save validators do NOT require the `vat` field — EU sole traders below their country's VAT threshold can save the form with the VAT field left empty. Only the FORMAT check fires when the field is filled. See [[billing-invoicing-vat-vies-lookup]] for the outage / empty-field rules.

### Single invoicing record per merchant

There is exactly one invoice-details record per merchant account. Saving the form replaces the existing record entirely — there is no history. See [[billing-invoicing-save-flow]].

### Validity warning surfaces on other screens

If the stored invoice details fail re-validation at any point (e.g. the EIK is no longer valid in the registry, or the registered VAT was deactivated), the platform may display the *"You have an invalid invoice details! Please, change them!"* banner on billing-related screens until the merchant returns and re-saves.

## Related

- [[billing-invoicing]] — hub.
- [[billing-invoicing-country-driven-form]] — how the Country dropdown swaps which field is primary and which fields lock.
- [[billing-invoicing-eik-apis-lookup]] — the EIK validator + APIS Trade Register call.
- [[billing-invoicing-vat-vies-lookup]] — VIES + HMRC validation paths.
- [[billing-invoicing-save-flow]] — what happens on submit.
- [[billing-invoicing-vue-checkout-editor]] — the Vue editor where `name` and `company_id` are `required_if:country,BG` instead of always required.

## Open questions

None.
