---
type: feature
nav_path: "Profile → Billing → Invoice details → Vue checkout editor"
route_name: admin.billing.invoicing
route_path: /admin/api/core/billing/invoicing
aliases: ["Vue inline invoicing", "Inline Vue editor invoicing", "Checkout panel invoicing", "Hungary VAT validator", "VatIdHuRule", "CompanyIdHuRule"]
tags: [billing, invoicing, vue, checkout, hungary, surface-differences]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[billing-invoicing]]. See the hub for the other aspects (fields, EIK/APIS, VAT/VIES, country-driven form, save flow).

# Invoice details — Vue checkout editor

## Purpose

Document the **alternate save surface** that the *Invoice details* feature exposes inside the merchant's checkout panel. When the merchant is buying a plan, app, service, or feature pack via the Vue checkout, the *Invoice details* card mounts as a Vue inline editor (`InvoiceDetails` + `FormDetails` components) instead of opening the Smarty side panel. This surface posts to a DIFFERENT endpoint with DIFFERENT required-field rules and has Hungary-specific custom validators that the Smarty surface does NOT have.

## Where to find it

Inside any Checkout panel — plan purchase ([[plans-purchase]]), service purchase ([[services]]), app purchase ([[apps]]), feature-pack purchase — the *Invoice details* card appears with a collapsed summary by default. A pencil icon (`fa-pen`) expands it inline (using `Vue3SlideUpDown`, duration 250ms) into the full form.

Route for the save: `POST /admin/api/core/billing/invoicing` (NOT `/admin/billing/invoicing` — that's the Smarty surface, see [[billing-invoicing-save-flow]]).

## What the merchant can do here

- See a collapsed summary of the current invoice details without leaving the checkout flow.
- Click the pencil icon to expand the form inline.
- Edit any field per the country-driven readonly rules — see [[billing-invoicing-country-driven-form]].
- Click **Confirm** to save (the inline form collapses back to summary).
- Click **Cancel** to discard pending edits (restores from `original` clone).

## Settings & fields

### Collapsed summary

By default the card renders a collapsed summary with these labelled rows:

- Company name.
- Company number (VAT) — shown only when `vat` is set.
- Company number — shown only when `country !== 'DE'`.
- Country.
- Address.
- Name.
- Email.

The pencil icon (`fa-pen`) expands it into the full form.

### Expanded form

- **Country** picker (`CountriesComponent`) — `cols-width="6"`, `can-clear="false"`. For DE-invoiced sites (`siteUser.issuer_company_id === 7` — CloudCart GmbH) the picker is filtered to **EU countries only** (`euOnly` computed). See [[billing-invoicing-country-driven-form]].
- **Company or business name** — disabled when registry auto-fill is active (BG or non-BG EU).
- **Company ID** — **HIDDEN entirely for DE** (`v-if="invoicing.country !== 'DE'"`). For all other countries it follows the standard rules.
- **VAT ID** — always editable; triggers VIES validation as the merchant types (or HMRC for GB; format-only for HU — see "Country-required fields differ by surface" below).
- **Address** — disabled when registry-filled.
- **Materially Responsible Person** — always editable.
- **Email** — always editable.

### Action buttons (during edit)

- **Cancel** (`btn-cc cancel`) — discards changes; restores `invoicing` from the `original` clone; closes the slide; re-emits the unchanged state to the parent. No confirm prompt is shown — discard is immediate. If the merchant had typed a partial VAT/EIK that triggered a lookup, those filled fields are also reverted.
- **Confirm** (`btn-cc save`) — saves via the model; while submitting shows a `<b-spinner small>` instead of the check icon.

### Pre-fill from user account

When the `FormDetails` component mounts and no invoicing exists yet, it pre-fills:

- `invoicing.country = siteUser.country` (the merchant's saved account country).
- `invoicing.email = siteUser.email` (the merchant's account email).

Both can be edited freely before save.

## Business rules

### Country-required fields differ by surface

The two save surfaces enforce different required-field rules:

- **Smarty `/admin/billing/invoicing` route** — `company_id`, `company`, `address`, `name`, `country`, `email` are ALL `required` regardless of country. See [[billing-invoicing-fields-and-validation]].
- **Vue checkout API** (`/admin/api/core/billing/invoicing`) — relaxes two of them:
  - `name` (MOL) — `required_if:country,BG` (optional for non-BG countries at save level).
  - `company_id` — `required_if:country,BG|eik` (for HU with the HU format rule when filled). For other non-BG countries it's not blockingly required.
  - `country`, `company`, `address`, `email` remain always required.

The form UI marks fields visually as required regardless of country; the relaxed `required_if:country,BG` rules apply only on the Vue-checkout API path.

### Hungary (HU) custom validators — Vue path only

The Vue checkout API request treats Hungary as a special case — for HU it bypasses the default `eik` / `vat_number` rules and applies its own Hungarian-format validators:

- **VAT ID for HU**: a dedicated `VatIdHuRule` validator runs against the Hungarian VAT format (`HU` + 8 digits typically). VIES is NOT consulted for HU on save.
- **Company ID for HU**: when the merchant fills the company-id field on a HU record, a dedicated `CompanyIdHuRule` validator runs against the Hungarian company-registration format.

These HU rules only fire when the corresponding field is filled, and they enforce format-only validation (no remote registry lookup). NOTE: this HU special-casing exists ONLY in the Vue-checkout API request — the Smarty route does NOT have it (it always uses `eik` + `vat_number`). See [[billing-invoicing-vat-vies-lookup]] for the parallel VIES path.

### Save success collapses the editor (not closes it)

On save success, the inline editor collapses back to the summary view AND `original` is cloned from the new `invoicing` state. The merchant stays in the parent checkout flow — the editor does NOT close like the Smarty side panel does. See [[billing-invoicing-save-flow]] for the Smarty surface's panel-close behaviour.

### Save error renders inline

On save error, the per-field validation messages render inline next to the offending fields. The editor stays open so the merchant can fix.

### Country picker filtering for DE-issuer sites

When the issuing CloudCart entity is CloudCart GmbH (`siteUser.issuer_company_id === 7`), the country picker is restricted to EU countries only via the `euOnly` computed flag. The Smarty side panel does NOT have this filter; merchants on non-CloudCart-GmbH sites see the full ISO list everywhere. (verify)

### Company ID hidden for DE

Specifically on the Vue editor, when `invoicing.country === 'DE'` the **Company ID** field is hidden entirely (`v-if`). German merchants identify only via the **VAT ID** field. The Smarty side panel always renders the Company ID input regardless of country. (verify)

## Related

- [[billing-invoicing]] — hub.
- [[billing-invoicing-fields-and-validation]] — the Smarty surface's required-field rules (which the Vue surface relaxes).
- [[billing-invoicing-eik-apis-lookup]] — the EIK path (used at country = BG on both surfaces).
- [[billing-invoicing-vat-vies-lookup]] — the VIES path (used at country ≠ BG on the Smarty surface; the Vue surface bypasses VIES for HU).
- [[billing-invoicing-country-driven-form]] — the `disabledMapping` map and the country-watcher logic for this Vue surface.
- [[billing-invoicing-save-flow]] — the Smarty save handler's sequence (silent APIS enrichment + VIES overwrite + language defaulting).
- [[plans-purchase]] / [[services]] / [[apps]] — entry points where this Vue editor mounts.

## Open questions

None.
