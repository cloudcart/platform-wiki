---
type: feature
nav_path: "Settings → Invoicing → HTML templates"
route_name: invoicing.templates
route_path: /admin/settings/invoicing/template
aliases: ["HTML templates", "Invoice HTML", "Credit note HTML", "Packing slip HTML", "Order print template", "Watermark", "invoice_watermark", "template variables", "Template placeholders"]
tags: [settings, invoicing, html, templates, placeholders]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[settings-invoicing]]. See the hub for the other aspects (activation modes, numbering, issuer block, template editor, credit note, external systems).

# Invoicing — HTML templates tab

## Purpose

The third tab is the raw HTML editor for the three template types: **Invoice**, **Packing slip / Order print**, and **Credit note**. For each, the merchant can download the default template as a starting point, see the documented set of template variables, and paste a custom HTML body that the platform substitutes at render time. A free-text watermark setting (`invoice_watermark`) is also surfaced here.

## Where to find it

Sidebar → Settings → **Invoicing** → **HTML templates** tab. Route name `invoicing.templates`. Route path `/admin/settings/invoicing/template`.

## What the merchant can do here

- **Download** the default HTML for each template type as a starting point.
- See the **template-variables legend** for each template type — copy variables to paste into HTML.
- **Edit raw HTML** for each template in the embedded code editor.
- Set the **Watermark** text (`invoice_watermark`) that gets stamped diagonally across the printed PDF.
- See the **product-sorting tokens** available in the packing-slip template.
- Also edit two credit-note controls (`credit_number`, `credit_payment`) that share their storage with the Credit note tab.

## Settings & fields

### Three template panels — download + variables + editor trio

| Template | Download slot | Variables-legend slot | Editor target |
|----------|---------------|------------------------|----------------|
| Invoice | `downloadInvoice` | `invoice` (variables legend: `invoice_orders_placeholders`) | Raw HTML editor for invoice template |
| Packing slip / Order print | `downloadPackingslip` | `orderList` (variables legend) | Raw HTML editor for order-print template |
| Credit note | `downloadCreditnote` | `credit_orders_placeholders` (variables legend) | Raw HTML editor for credit-note template |

### Tab-specific extra fields

| Field | Key | Notes |
|-------|-----|-------|
| Watermark | `invoice_watermark` | Free text. Stamped diagonally across the printed invoice PDF. |
| Credit-note number padding | `credit_number` | Labelled **"Invoice number padding"**; its help tip describes zero-fill. Validated `required|numeric|min:0|max:10` — this is the field the deep-link from other tabs lands on. Despite the name it is neither an invoice setting nor a starting number; the padding the credit-note renderer actually applies is `credit_number_formatting_padding` on the Credit note tab. See [[settings-invoicing-numbering]]. |
| Credit-note payment | `credit_payment` | Same picker as the Credit note tab, same storage. Overrides only the payment method printed on the document. See [[settings-invoicing-credit-note]]. |
| Product sorting (packing slip) | `print_order_sorter` | A **read-only legend** on the packing-slip panel listing the sort tokens a custom packing-slip template can append to the products placeholder — `:id-asc`, `:id-desc`, `:name-asc`, `:name-desc`, `:price-asc`, `:price-desc`, `:quantity-asc`, `:quantity-desc`, `:sku-asc`, `:sku-desc`, `:barcode-asc`, `:barcode-desc`, `:category-asc`, `:category-desc`. Using one of them makes the printed picking list come out in that order. Nothing is saved — the choice lives inside the template the merchant writes. |
| CSS classes for the default elements | `invoice_items_default_classes` / `credit_items_default_classes` / `print_items_default_classes` | **Read-only reference lists** of the CSS class names the platform's default markup already uses, shown so a template author knows which hooks exist. Not settings; nothing is filtered at render time. |

## Business rules

### HTML templates are stored per type as full strings

The custom HTML template a merchant pastes is stored as a single setting value (string) per template type. At render time, the platform's print/render layer substitutes the variable placeholders documented in the legend. There is **no syntax validation** in this page — broken HTML or malformed placeholder tokens silently render literally on the final PDF.

### No in-app HTML template preview — issue a test invoice to verify

The HTML editor does **NOT** offer a "Preview" or "Render with sample data" action. To check how a custom template renders, the merchant must save the template and then generate an actual invoice from an order (or order print) and open the resulting PDF.

Practical workflow recommendation for merchants: keep a recent "throwaway" test order in the system specifically for previewing template changes — issue an invoice on it, view the PDF, tweak the template, repeat. Broken HTML or unknown placeholders fail silently (render literally on the PDF), so visual checks are the only line of defence.

### Three independent variable legends

Each template type has its OWN placeholder set documented inline:

- **Invoice** variables (`invoice_orders_placeholders`) — order header fields, line items, totals, payment block, issuer block.
- **Packing slip / Order print** variables (`orderList`) — order fields + addresses + shipping block, optimised for warehouse picking.
- **Credit note** variables (`credit_orders_placeholders`) — credit-note-specific fields including the parent-invoice reference.

The legends are visible inline on the page; the merchant copies tokens into their HTML and the platform substitutes them at render time.

### Watermark is free text — no styling controls

`invoice_watermark` is a single free-text string. The platform stamps it diagonally across the invoice PDF with platform-fixed positioning, opacity, and angle. The merchant cannot change the typography or position — only the text.

### Only two credit-note controls appear on this tab

`credit_number` (the "Invoice number padding" number field) and `credit_payment` (the payment-method picker) sit in the **Credit notification information** box on this tab. `credit_payment` shares its storage with the identical picker on the Credit note tab — editing it in one place updates the other.

The credit-note number **prefix** and **suffix** are NOT on this tab. They live only on the Credit note tab — see [[settings-invoicing-credit-note]].

### Default HTML is downloadable, not auto-restored

The download is a one-way "starting point" export. There is no "Reset to default" button — once the merchant has saved a custom HTML, restoring the default requires re-downloading the default file and pasting it back in. (Operator support can clear the custom HTML at the DB layer if needed.)

### Validation errors on `credit_number` deep-link HERE

The `errorKeysByPageEnum` mapping routes `credit_number` errors to this tab (not the Credit note tab) — the page auto-navigates here and scrolls the field into view on a save failure referencing that padding field.

## Related

- [[settings-invoicing]] — hub.
- [[settings-invoicing-template-editor]] — visual editor for invoice settings.
- [[settings-invoicing-credit-note]] — credit-note tab where `credit_payment` and credit-note fields primarily live.
- [[settings-invoicing-numbering]] — the prefix / padding / suffix mechanics that the duplicated credit fields feed.
- [[invoice]] — entity rendered using the invoice HTML template.
- [[credit-note]] — entity rendered using the credit-note HTML template.
- [[order]] — packing slip / order print covers the order itself.
- [[orders-details]] — where the test-order workflow happens.

## Open questions

None.
