---
type: feature
nav_path: "Settings → Invoicing → Issuer block"
route_name: invoicing.settings
route_path: /admin/settings/invoicing
aliases: ["Invoice issuer", "Company info", "Issuer block", "Company VAT", "BULSTAT", "MOL", "company_bulstat", "company_mol", "Bulgarian issuer validation"]
tags: [settings, invoicing, issuer, company, vat, bulstat]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[settings-invoicing]]. See the hub for the other aspects (activation modes, numbering, template editor, credit note, HTML templates, external systems).

# Invoicing — issuer block (company info)

## Purpose

The "issuer block" is the merchant's own company-identity data that prints at the top of every invoice / credit note: company name, VAT, registration number (BULSTAT), MOL (Bulgarian legal owner), phone, country, city, street, postal code. The fields are validated according to the issuer country — Bulgarian issuers have additional mandatory fields with a checksum validator. A separate country-list carve-out forces English country names for German-issuer stores.

## Where to find it

Sidebar → Settings → **Invoicing** → Invoice template tab → click the **company info** section in the preview ("Invoice company info settings"; a full-screen modal on mobile). Saving needs the **Invoicing** staff permission (`settings.invoice`, [[settings-staff]]).

## What the merchant can do here

- Edit every field of the issuer block.
- Add `{ key, value }` header rows (`custom_header_text`; no cap).
- See validation errors scrolled-to via `errorKeysByPageEnum.company_info` if any required issuer field is missing.

## Settings & fields

| Field | Key | Validation when `invoicing=1` |
|-------|-----|-------------------------------|
| Company name | `company_name` | required |
| Company VAT | `company_vat` | optional |
| Company BULSTAT | `company_bulstat` | required when `country='BG'` AND must pass the `eik` validator (Bulgarian checksum) |
| MOL (legal owner) | `company_mol` | required when `country='BG'` |
| Phone | `site_phone` | required |
| Country | `country` | required |
| City | `site_city` | required |
| Street | `site_street` | required |
| Postal code | `postal_code` | required |
| Issuer name | `issuer_name` | **Footer** section; prints after *Съставил* on invoices. Default below |
| Issuer code | `issuer_code` | **Footer** section; prints after *Подпис: шифър* on invoices. Default below |
| Custom header rows | `custom_header_text` (JSON) + `header_rows` (computed `{key, value}` array) | optional, unbounded count |

## Business rules

### Bulgarian-issuer fields are mandatory with checksum validation

The save validator enforces country-conditional rules:

- If `country='BG'` (Bulgarian issuer), `company_bulstat` is **required** AND must pass the `eik` validator (Bulgarian company registration number checksum).
- If `country='BG'`, `company_mol` (legal owner name) is also **required**.
- All issuer cases: `company_name`, `site_phone`, `country`, `site_city`, `site_street`, `postal_code` are required when `invoicing=1`.

Other countries don't need BULSTAT / MOL — they're optional. A Bulgarian merchant accidentally setting an invalid BULSTAT cannot save the page until corrected.

### Country list shows English names for German-issuer stores

When the merchant's store is registered under the **DE (Germany)** issuer entity, the country dropdown shows countries in English regardless of the admin's display language. Otherwise countries appear in the active admin language. This is a German tax-compliance carve-out — DE-issued invoices require country names in English.

### Merchant company VAT is NOT auto-validated against VIES

The `checkout_validate_company_vat` setting on [[settings-cart]] gates **customer** VAT validation against the EU VIES service. The merchant's OWN `company_vat` field here is NOT validated against VIES — the platform accepts whatever the merchant types and writes it onto invoices as-is. There is also an internal command that can sync historical orders' invoice details with VIES, but it is an operator-run script, not a per-edit validation.

Practical guidance: merchants should double-check their own VAT number is in the correct format for their country (e.g., `BG123456789` with the leading country prefix) since a typo here will appear on every invoice.

### Who prints under *Съставил*

The *Съставил* / *Подпис: шифър* block prints at the bottom of **Bulgarian-language** invoices and credit notes only; documents in other languages have none.

- **Invoice:** **Issuer name** and **Issuer code** from the **Footer** section of the Invoice template tab.
- **Credit note:** its own pair, `credit_issuer_name` / `credit_issuer_code`; the invoice footer's values never reach it. The admin has **no field** for this pair (the Credit note tab shows none). It can be set through the Admin API's invoicing-settings update (`updateInvoicingSettings`).
- **A value left empty** is filled from the admin who first renders a numbered document of the order in the admin panel (first and last name, else username; code = their admin ID padded to 7 digits, e.g. `0001234`), or from the store owner when it is produced elsewhere. That person is saved on the order and reused for its invoice and credit note.
- **Saving the Invoicing page stores both pairs.** The page shows an empty name already filled with the signed-in admin's name and sends every value back, so a save writes that name into the invoice pair and the credit-note pair. A credit note can therefore show whoever last saved the page while it was empty.

### Issuer block defaults from store's onboarding invoicing data

When `company_name` is empty on this page, the Settings → Invoicing endpoint falls back to the store's onboarding `Invoicing` record (the data the merchant entered at store sign-up: company / company_id / vat / name / country / address / city). So a brand-new merchant who hasn't opened this page yet still gets their company details printed on invoices.

### Custom header rows are unbounded

Any number of `{ key, value }` rows (e.g. `"VAT №"` → `"BG123456789"`) print at the top of the invoice (`custom_header_text`). The Credit note tab has its own (`credit_custom_header_text`, [[settings-invoicing-credit-note]]).

### The issuer block is read LIVE on every render — it is not snapshotted

The company block printed on an invoice or credit note is read from these settings **each time the document is rendered**, not frozen when the number was issued. Editing the company name, VAT, address, or the footer issuer name here therefore changes how **already-issued, historical** invoices and credit notes look the next time anyone downloads or emails them.

To keep a document's original wording, save its PDF before editing these fields.

### The phone and address are also the store's contact details

**Phone** (`site_phone`) and the address fields here are the store's single saved contact phone and address: the storefront contact page shows them (*company name, phone*) when its own text is empty ([[design-module-contact-information]]). The GDPR app's store-address step and the Aftercare app's data step write the same fields; the last save wins. Emails have no store-phone variable ([[email-template-variables]]).

### Errors deep-link to this section

A validation error on any company-info field opens the Invoice template tab and scrolls to the company-info block (`errorKeysByPageEnum.company_info`).

## Related

- [[settings-invoicing]] — hub.
- [[settings-invoicing-template-editor]] — the click-to-edit preview that opens this modal.
- [[settings-invoicing-credit-note]] — credit-note tab also embeds the custom-rows module for `credit_custom_header_text`.
- [[settings-cart]] — `checkout_validate_company_vat` (customer-side VIES).
- [[settings-general]] — `site_email` and other defaults that also appear on invoices.
- [[settings-brand]] — `invoice` logo slot rendered alongside this issuer block.
- [[invoice]] — entity; reads the issuer block live on every render.
- [[credit-note]] — entity; reads the issuer block live on every render.

## Open questions

None.
