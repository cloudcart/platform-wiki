---
type: feature
nav_path: "Settings → Invoicing → Issuer block"
route_name: invoicing.settings
route_path: /admin/settings/invoicing
aliases: ["Invoice issuer", "Company info", "Issuer block", "Company VAT", "BULSTAT", "MOL", "company_bulstat", "company_mol", "Bulgarian issuer validation"]
tags: [settings, invoicing, issuer, company, vat, bulstat]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[settings-invoicing]]. See the hub for the other aspects (activation modes, numbering, template editor, credit note, HTML templates, external systems).

# Invoicing — issuer block (company info)

## Purpose

The "issuer block" is the merchant's own company-identity data that prints at the top of every invoice / credit note: company name, VAT, registration number (BULSTAT), MOL (Bulgarian legal owner), phone, country, city, street, postal code. The fields are validated according to the issuer country — Bulgarian issuers have additional mandatory fields with a checksum validator. A separate country-list carve-out forces English country names for German-issuer stores.

## Where to find it

Sidebar → Settings → **Invoicing** → Invoice template tab → click the **company info** section in the preview to open the "Invoice company info settings" modal. On desktop the settings appear inline in the left side-panel; on mobile they open as a full-screen modal.

## What the merchant can do here

- Edit every field of the issuer block.
- Add arbitrary `{ key, value }` rows to print extra header lines (e.g., `"VAT №"` → `"BG123456789"`) — the `custom_header_text` JSON. The same row-builder appears on the credit-note tab feeding `credit_custom_header_text`. There is no count cap.
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
| Issuer name | `issuer_name` | optional — defaults to store owner's first/last name (or username fallback) |
| Issuer code | `issuer_code` | optional — defaults to owner's admin ID padded to 7 digits |
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

### Default issuer name / code derive from the store owner

When `issuer_name` / `issuer_code` are empty, the platform auto-fills:

- `issuer_name` from the store owner's first/last name (or username fallback)
- `issuer_code` from the owner's admin user-ID padded to 7 digits (e.g., `0001234`)

Same for credit-note issuer fields (`credit_issuer_name` / `credit_issuer_code` — see [[settings-invoicing-credit-note]]). Merchants who want a different name on their invoices should fill these fields explicitly.

### Issuer block defaults from store's onboarding invoicing data

When `company_name` is empty on this page, the Settings → Invoicing endpoint falls back to the store's onboarding `Invoicing` record (the data the merchant entered at store sign-up: company / company_id / vat / name / country / address / city). So a brand-new merchant who hasn't opened this page yet still gets their company details printed on invoices.

### Custom header rows are unbounded

The merchant can add as many `{ key, value }` rows as they want via the row-builder. They serialise into `custom_header_text` JSON on save and print at the top of the invoice. The same module appears on the Credit note tab feeding `credit_custom_header_text` independently — see [[settings-invoicing-credit-note]].

### The issuer block is read LIVE on every render — it is not snapshotted

The company block printed on an invoice or credit note is read from these settings **each time the document is rendered**, not frozen when the number was issued. Editing the company name, VAT, address, or the footer issuer name here therefore changes how **already-issued, historical** invoices and credit notes look the next time anyone downloads or emails them.

Merchants who change legal entity or move address should be aware that old documents will re-print with the new details. If a document must keep its original wording, the merchant needs to save a copy of the PDF before editing these fields.

### Errors deep-link to this section

A validation error on any company-info field auto-navigates to the Invoice template tab and scrolls the company-info block into view — via `errorKeysByPageEnum.company_info`. The merchant never has to hunt for which tab is breaking.

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
