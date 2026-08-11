---
type: feature
nav_path: "Settings → Invoicing"
route_name: invoicing
route_path: /admin/settings/invoicing
aliases: ["Invoicing", "Invoice template", "Credit notes", "Фактури", "Кредитни известия", "Фактуриране"]
tags: [settings, invoicing, finance, templates]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 7
---

# Invoicing

## Purpose

A three-tab screen where the merchant configures everything about invoices and credit notes the store issues: visual layout, numbering, what gets printed, which payment method the credit note prints, the raw HTML templates the platform uses to render PDFs, and the external system that can supply invoice numbers (**Gensoft** — the only App in that dropdown).

The Invoice-template tab has a click-to-edit visual preview — the merchant clicks a section on the rendered invoice and the corresponding settings open in a side modal. A single global Save button submits ALL three tabs in one request; validation errors auto-navigate to the offending tab.

## Where to find it

Sidebar → Settings → **Invoicing**. Route: `/admin/settings/invoicing`. Header icon: file-invoice-dollar. Three sub-tabs (rendered via `<router-view/>`):

| Label | Route name | Route path |
|-------|------------|------------|
| Invoice template | `invoicing.settings` | `/admin/settings/invoicing` |
| Credit note template | `credit-note.template` | `/admin/settings/invoicing/credit-note` |
| HTML templates | `invoicing.templates` | `/admin/settings/invoicing/template` |

## What the merchant can do here

- Activate the in-platform invoicing service and pick its generation mode — see [[settings-invoicing-activation-modes]].
- Configure invoice and credit-note numbering (prefix / padding / suffix, `[OY]`/`[OM]`/`[OD]`/`[CID]`/`[CGID]`/`[DATE]` placeholders) — see [[settings-invoicing-numbering]].
- Configure the issuer block (company name, VAT, BULSTAT, MOL, address) — see [[settings-invoicing-issuer-block]].
- Edit the invoice template visually via click-to-edit section modals — see [[settings-invoicing-template-editor]].
- Edit the credit-note template + pick the payment method printed on the credit note — see [[settings-invoicing-credit-note]].
- Edit the raw HTML for invoice / credit note / order-print templates and set a PDF watermark — see [[settings-invoicing-html-templates]].
- Choose which external App supplies invoice numbers in external numbering mode — see [[settings-invoicing-external-systems]].

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages — drill into the one that matches the question rather than reading every page.

- [[settings-invoicing-activation-modes]] — `invoicing` master toggle, `invoice_generate`, `invoice_number_type` (system / manual / external), `billing_invoicing`, and the `invoicing_provider` external-replacement mutex.
- [[settings-invoicing-numbering]] — number formatting (`invoice_number_formatting_prefix` / `_padding` / `_suffix`), credit-note equivalents, what each of `[OY]`/`[OM]`/`[OD]`/`[CID]`/`[CGID]`/`[DATE]` actually substitutes, 10-digit padding cap, independent sequences, and the one credit-note series shared with partial returns.
- [[settings-invoicing-issuer-block]] — company-info fields, BG-conditional `company_bulstat` + `company_mol` with `eik` checksum validation, English country-list carve-out for DE-issuer stores, no VIES auto-validation, onboarding-data fallback.
- [[settings-invoicing-template-editor]] — Invoice template tab; click-to-edit preview; the five section modals (`header`, `company_info`, `list`, `payment`, `footer`); print toggles (`show_payment_details`, `show_payment_description`, `print_product_barcode`, `show_product_image_list`, `invoice_hide_zero_shipping`).
- [[settings-invoicing-credit-note]] — Credit note template tab; `credit_payment` only overrides the payment method PRINTED on the document (no refund is routed, nothing is persisted), default literal `no_change`; `credit_custom_header_text` row builder.
- [[settings-invoicing-html-templates]] — HTML templates tab; download / variables-legend / editor trios for Invoice / Packing slip / Credit note; `invoice_watermark`; `print_order_sorter` product-sort tokens; no in-app preview (test via real order).
- [[settings-invoicing-external-systems]] — the External system dropdown (Gensoft only, and only in external numbering mode) vs full-replacement providers (Szamlazz, via `invoicing_provider`); no unified retry policy.

## Settings & fields

The full per-tab field tables live in the aspect pages. Cross-cutting fields:

- All three tabs submit in **one PUT** payload via the page-header Save. There is no per-tab partial save and no draft state.
- Validation error on a different tab → auto-navigates to that tab and scrolls the failed field into view (`errorKeysByPageEnum`).
- Saving bumps the `boarding_settings=1` flag — the onboarding wizard considers the invoicing step complete after the first save.

### What the merchant CANNOT do here

- Switch between sandbox-style and production-style invoice numbering on a per-order basis — the format is store-wide.
- Generate a one-off invoice with a custom number — this page configures the template; individual invoices are issued from [[orders-details]].
- Set per-country invoice templates — single template per store.
- Upload the invoice logo — the `invoice` logo slot is uploaded on [[settings-brand]].

## Business rules

Per-aspect rules live on the aspect pages. The cross-cutting rules:

- **Single global save** persists all three tabs in one request — the merchant can edit fields on multiple tabs before clicking Save once.
- **Validation errors deep-link** to the offending tab via `errorKeysByPageEnum`. E.g., a `credit_number` error opens the HTML templates tab; a company-info error opens the company section modal.
- **An invoice freezes its order.** Once an order has an invoice number it can no longer be edited ([[orders-details-products]]) and its prices can no longer be converted from BGN to EUR ([[orders-details-actions]]). Corrections go through a return / credit note instead — [[orders-returns]], [[orders-credit]].
- **Cache + side effects** — saving here flushes the platform Settings cache. The next render of any invoice / credit-note / order-print picks up the new template and settings immediately. No queued jobs from THIS page; the external-system push (when configured) IS queued — see each App's page and [[settings-invoicing-external-systems]].
- **Issuer block defaults from onboarding data** — when `company_name` is empty, the page falls back to the store's onboarding `Invoicing` record. So a brand-new merchant who hasn't opened this page yet still gets their company details printed on invoices.

## Related

- [[invoicing-and-accounting]] — invoicing & accounting concept hub.
- [[settings]] — parent hub.
- [[settings-general]] — `site_email`, `site_name`, `copyright` appear on invoices as defaults.
- [[settings-brand]] — `invoice` logo slot is rendered on the invoice template.
- [[settings-payment-providers]] — providers shown in the payment dropdowns (default invoice provider, credit-note refund provider).
- [[settings-cart]] — `invoicing_address` setting (BillingAddress vs ShippingAddress) influences how taxes are computed on the invoice; `checkout_validate_company_vat` gates customer-side VIES validation (NOT issuer VAT).
- [[settings-statuses]] — payment statuses referenced by the order pipeline (NOT auto-driven by `credit_payment`).
- [[settings-translations]] — invoice/credit-note labels are localised; the merchant's storefront language defaults are picked up here.
- [[invoice]] — entity page.
- [[credit-note]] — entity page.
- [[order]] / [[orders-details]] — invoices are issued from individual order screens.
- [[notification-delivery]] — invoice emails to the customer go via the customer-mail pipeline.
- [[order-processing-pipeline]] — when the invoicing provider is invoked during order processing.
- [[apps-gensoft]] — the App shown in the External system dropdown when installed and active.
- [[apps-szamlazz]], [[apps-smart-bill]], [[apps-fgo]], [[apps-flix-facts]] — other accounting Apps; each has its own settings screen and none appears in the External system dropdown.
- [[orders-details-products]] — the invoiced-order edit lock.
- [[orders-returns]] — how a partial correction is made once an invoice exists.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
