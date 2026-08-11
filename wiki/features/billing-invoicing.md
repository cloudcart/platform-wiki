---
type: feature
nav_path: "Profile → Billing → Invoice details"
route_name: admin.billing.invoicing
route_path: /admin/billing/invoicing
aliases: ["Invoice details", "Invoicing details", "Billing invoice details", "Company details", "Данни за фактура", "Фирмени данни", "Фактурни данни"]
tags: [billing, invoicing, company-details, vat, eik, vies, apis]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---

# Invoice details (billing)

## Purpose

The **Invoice details** screen is where the merchant enters the company information that CloudCart prints on **the invoices CloudCart issues to the merchant** for every charge (store plan renewals, paid apps, paid feature packs, paid services). This is the merchant's identity as CloudCart's *customer* — it controls how the merchant's name, company, VAT/EIK number, and billing address appear on the invoices CloudCart bills them with, and it drives VAT treatment (reverse-charge for EU B2B, BG-rate for Bulgarian merchants, no-VAT for outside-EU).

This is **separate** from the store's own invoicing settings ([[settings-invoicing]]), which govern the invoices the merchant's storefront issues to *their* customers. Easy way to keep these straight:

- **Invoice details (this screen)** = the merchant tells CloudCart who to invoice.
- **Settings → Invoicing** = the merchant tells their storefront how to invoice their own buyers.

## Where to find it

- **Profile dropdown** (top-right user-account menu) → **Billing** opens the billing landing area where the invoice-details block is shown.
- From within that area, the **pencil icon** next to the invoice-details block opens the editor side panel. If no details exist yet, an **Add invoice details** button does the same.
- The same panel is also opened automatically from the services-purchase flow when the merchant has no invoice details on file (see [[services]]).

URL pattern: `/admin/billing/invoicing` (the editor side panel; the read-only summary lives at the billing landing area).

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[billing-invoicing-fields-and-validation]] — every form field (Country, Company ID, VAT, Company, Address, MOL `name`, Email); the platform code required-validation rules; the four merchant-visible validation messages.
- [[billing-invoicing-eik-apis-lookup]] — the BG branch: 9-digit / 13-digit EIK check-digit algorithm, EGN sole-trader path, APIS Trade Register call at `regdata.apis.bg`, Bulgarian-language address formatting.
- [[billing-invoicing-vat-vies-lookup]] — the non-BG branch: VIES validation, HMRC for `GB`, per-country VAT pattern enforcement, the three skip cases (BG / CH / non-VAT countries), outage handling.
- [[billing-invoicing-country-driven-form]] — how the Country dropdown swaps which field is primary; the `disabledMapping` named maps (`countryBg`, `countryNoBg`, `eikBg`, `vatNoBg`); the auto-trigger watchers; the DE-only `euOnly` filter.
- [[billing-invoicing-save-flow]] — what happens on Submit: silent APIS enrichment for non-BG, VIES overwriting submitted Company/Address values, language defaulted from country (`bg` vs `en`), single record replaced in place, panel auto-close + parent reload.
- [[billing-invoicing-vue-checkout-editor]] — the Vue inline editor inside Checkout (`/admin/api/core/billing/invoicing`): relaxed `required_if:country,BG` rules, Hungary's `VatIdHuRule` + `CompanyIdHuRule` carve-outs, DE-issuer EU-only country filter, hidden Company ID for DE.

## What the merchant can do here

- Enter the **country** of the invoiced entity — drives the rest of the form (see [[billing-invoicing-country-driven-form]]).
- For **Bulgaria** (`BG`): enter the EIK. The system auto-fills the company name, VAT, address and responsible person via APIS (see [[billing-invoicing-eik-apis-lookup]]).
- For **any other EU country**: enter the **VAT ID** (`<country-code><number>`, e.g. `DE123456789`). The system auto-fills the company name and address via EU VIES (see [[billing-invoicing-vat-vies-lookup]]).
- For **non-EU countries** (and any case where the auto-fill fails): enter all fields manually.
- Enter the **Materially Responsible Person** (MOL — typically the manager / director whose name is printed on the invoice).
- Enter the **billing email** the invoice PDFs will be sent to (separate from the merchant's account email).

What the merchant **cannot** do here: edit auto-filled fields in BG / EU-with-VIES mode (locked readonly), save invalid EIK / VAT IDs, or maintain multiple billing profiles (one record per merchant — see [[billing-invoicing-save-flow]]).

## Settings & fields

This page is the navigation hub — the full fields table (label / required / what it does / validation) lives on [[billing-invoicing-fields-and-validation]]. The seven fields are: **Country**, **Company ID**, **VAT ID**, **Company or business name**, **Address**, **Materially Responsible Person (MOL `name`)**, **Email**.

The merchant-visible validation messages — *"Invalid Company ID"*, *"Invalid VAT ID"*, *"Currently, the VAT number validation system is not working. Please try again in a few minutes"*, and the cross-screen banner *"You have an invalid invoice details! Please, change them!"* — are catalogued on the same aspect.

## Business rules (cluster-wide)

The cluster's rules live on the aspect pages. The headline rules:

- **The country drives everything.** Country = BG → Company ID is primary, APIS auto-fills. Country ≠ BG → VAT ID is primary, VIES auto-fills (or HMRC for GB). Switching country back unlocks every field. See [[billing-invoicing-country-driven-form]].
- **EIK validation is purely local before APIS is called.** A 9-digit / 13-digit weighted-sum check-digit algorithm rejects bad EIKs without contacting the registry. EGN (10-digit personal ID) is accepted for sole traders. See [[billing-invoicing-eik-apis-lookup]].
- **VIES outages do NOT let the merchant bypass validation when they entered a VAT.** Empty VAT field is allowed for sole traders below their VAT threshold; format-checked VAT with VIES unreachable fails the save with the *"system unreachable"* message. See [[billing-invoicing-vat-vies-lookup]].
- **GB uses HMRC, not VIES** — post-Brexit. UK merchants get the same auto-fill experience via a different upstream. See [[billing-invoicing-vat-vies-lookup]].
- **VIES values overwrite typed values on save** for non-BG EU records — VIES is authoritative. Similarly, when country ≠ BG, the save runs a silent APIS enrichment that can overwrite the typed country code with the APIS-derived country. See [[billing-invoicing-save-flow]].
- **Two save surfaces have different required-field rules.** The Smarty `/admin/billing/invoicing` route marks `company_id` + `name` + everything else as always-required. The Vue `/admin/api/core/billing/invoicing` checkout API relaxes `name` and `company_id` to `required_if:country,BG`, hides Company ID entirely for DE, and bypasses VIES for HU via `VatIdHuRule`. See [[billing-invoicing-vue-checkout-editor]].
- **Single invoicing record per merchant.** Save overwrites the existing record entirely — no audit log, no "old vs new" diff. To track changes the merchant must keep their own external record. See [[billing-invoicing-save-flow]].
- **Invoice language follows the country.** `country = BG` → `bg`; everything else → `en`. The merchant doesn't choose this. See [[billing-invoicing-save-flow]].

## Related

- [[billing-cards]] — sibling screen; the payment card these invoices are charged to.
- [[plans]] — billed against these invoice details.
- [[subscriptions]] — recurring items billed using these details.
- [[services]] — purchasing a service requires invoice details on file; auto-opens this panel when none exist.
- [[apps]] — paid apps billed using these details.
- [[settings-invoicing]] — the *other* invoicing screen (the merchant's storefront invoicing setup; do not confuse).
- [[settings-general]] — the store's own legal country setting (separate from this billing country).
- [[merchant-subscription-lifecycle]] — merchant-question hub: "where do I see my invoices / how do I edit the company info on my CloudCart invoices?".

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
