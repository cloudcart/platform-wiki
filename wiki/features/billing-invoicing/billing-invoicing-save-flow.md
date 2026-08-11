---
type: feature
nav_path: "Profile → Billing → Invoice details → Save flow"
route_name: admin.billing.invoicing
route_path: /admin/billing/invoicing
aliases: ["Invoicing save flow", "Save handler invoicing", "Single invoicing record", "Field rewrite on save", "Language defaulted from country"]
tags: [billing, invoicing, save-flow, persistence]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[billing-invoicing]]. See the hub for the other aspects (fields, EIK/APIS, VAT/VIES, country-driven form, Vue checkout editor).

# Invoice details — save flow

## Purpose

Document what happens after the merchant clicks **Submit** (or Vue **Confirm**): which fields the platform silently overwrites with registry data, how the invoice language is decided, how the single per-merchant record gets replaced in place, and how the panel auto-closes the parent reload.

## Where to find it

Triggered by the **Submit** button on the Smarty side panel (`POST /admin/billing/invoicing`) or the **Confirm** button on the Vue inline checkout editor (`POST /admin/api/core/billing/invoicing` — see [[billing-invoicing-vue-checkout-editor]] for that surface's specific request rules).

## What the merchant can do here

- Submit the form to save the invoice-details record.
- See per-field validation errors inline if validation fails (the panel does NOT close on validation error).
- See a *"Save successful"* toast on success.
- Be redirected away from the panel on success — it closes itself and triggers a reload on the parent screen.

## Settings & fields

No new fields — this aspect is about the save handler's behaviour, not new form inputs. The fields it processes are catalogued on [[billing-invoicing-fields-and-validation]].

## Business rules

### Save sequence (Smarty `/admin/billing/invoicing`)

When the merchant clicks **Submit**:

1. The request validator runs the required-field + `eik` + `vat_number` validators. See [[billing-invoicing-fields-and-validation]] for the rules.
2. If validation fails, the per-field errors render inline and the save aborts.
3. The country is read from the request.
4. **If country ≠ BG, the platform tries an additional APIS lookup as an enrichment step** with `company_id` (and `vat` as fallback). If APIS returns data, the country code is overwritten with the APIS-derived country, and any additional fields APIS returned are merged in. The merchant doesn't see this happen — it's a silent backend enrichment with no UI feedback if it fails.
5. **If VIES returns valid VAT details (and country ≠ BG), the platform overwrites the submitted `company` and `address` fields with the VIES values**, even if the merchant typed something different. This is intentional — VIES is treated as authoritative for EU VAT records.
6. The full merged record is saved on the merchant's account.
7. The merchant sees the standard *"Save successful"* toast.

### Language defaulted from country

When saving, the platform sets the language of future invoices to `bg` if `country = BG`, otherwise `en`. The merchant doesn't choose this — it follows the country. This affects how field labels are translated on the generated PDF invoice.

### Single invoicing record per merchant — replaced in place

There is exactly one invoice-details record per merchant account. The save handler creates a NEW model instance from the gate site relation and OVERWRITES the previous record entirely on save. The same per-merchant invoicing row is updated in place — there is no audit log of prior values, no "old vs new" diff surfaced in the admin.

To bill a different company in the future, the merchant edits the same record. To track changes across years (e.g. for accounting reconciliation), the merchant must keep their own external record or request a support export.

### Panel auto-closes + parent re-loads on success

Submitting the form successfully returns the saved invoicing record as JSON. The Smarty side panel uses its `ajaxForm` handler — on success the panel closes itself and triggers a reload on the parent screen (typically *Details → Billing* or a checkout-flow caller) so the new invoice-details summary is shown immediately.

The Vue inline editor (see [[billing-invoicing-vue-checkout-editor]]) collapses back to the summary view instead of closing, and clones the new state into `original` so a subsequent Cancel reverts to the just-saved state.

### Validity warning surfaces on other screens after save

The save handler does NOT mark the just-saved record as invalid — that flag is set later if re-validation against APIS / VIES fails (e.g. the EIK gets deactivated in the registry). When that happens, the merchant sees the *"You have an invalid invoice details! Please, change them!"* banner on billing-related screens until they return here and re-save. See [[billing-invoicing-fields-and-validation]] for the message text.

### Side panel is opened via AJAX (Smarty)

The Smarty side panel is loaded into the right-side AJAX panel via `data-ajax-panel="true"`. The URL is rarely typed by hand — it expects to be opened from the Vue admin shell via one of the entry points (pencil icon, Add invoice details button, or the services-purchase flow when no invoice details exist on file). See [[services]] for the auto-open trigger from the services-purchase flow.

### Vue–Smarty hybrid: server form + AJAX submit

The page mounts as a Smarty template inside a Vue side-panel — the form is server-rendered HTML, but the submit is intercepted by the panel's AJAX layer. The validation messages are surfaced through the same Vue toast / inline-error system as other panels. To the merchant it looks like a regular Vue form; under the hood it's the legacy Smarty form harnessed into a panel.

### Discard-changes UX (Vue editor)

Clicking **Cancel** during edit on the Vue editor:

1. Restores `invoicing` from the `original` clone.
2. Closes the slide (`openSlide = false`).
3. Re-emits the unchanged state to the parent.

No confirm prompt is shown — discard is immediate. If the merchant had typed a partial VAT/EIK that triggered a lookup, those filled fields are also reverted.

## Related

- [[billing-invoicing]] — hub.
- [[billing-invoicing-fields-and-validation]] — the validation rules that gate the save.
- [[billing-invoicing-eik-apis-lookup]] — the BG path; APIS is also called silently on save for non-BG countries.
- [[billing-invoicing-vat-vies-lookup]] — VIES overwriting submitted Company / Address values on save.
- [[billing-invoicing-country-driven-form]] — country-code overwriting on save when APIS returns a different country.
- [[billing-invoicing-vue-checkout-editor]] — the alternate save surface (`/admin/api/core/billing/invoicing`) with relaxed required-field rules.
- [[services]] — entry point that auto-opens the panel when no invoice details exist on file.

## Open questions

None.
