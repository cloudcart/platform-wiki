---
type: feature
nav_path: "Settings → Invoicing → Invoice template editor"
route_name: invoicing.settings
route_path: /admin/settings/invoicing
aliases: ["Invoice template", "Click-to-edit preview", "Section modals", "Header rows", "Print toggles", "show_payment_details", "print_product_barcode"]
tags: [settings, invoicing, template, preview, sections]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[settings-invoicing]]. See the hub for the other aspects (activation modes, numbering, issuer block, credit note, HTML templates, external systems).

# Invoicing — invoice template editor (click-to-edit preview)

## Purpose

The default **Invoice template** tab. A live invoice preview is rendered on the right (desktop) or full-width (mobile); the merchant clicks any section of the preview and the matching settings open in a side-panel (desktop) or full-screen modal (mobile). Each section drives a focused group of fields: header rows / numbering, company info, products-list print toggles, payment-info print toggles, and footer text.

## Where to find it

Sidebar → Settings → **Invoicing** → **Invoice template** tab (default). Route: `/admin/settings/invoicing`. Three sub-tabs total:

| Label | Route name | Route path |
|-------|------------|------------|
| Invoice template | `invoicing.settings` | `/admin/settings/invoicing` |
| Credit note template | `credit-note.template` | `/admin/settings/invoicing/credit-note` |
| HTML templates | `invoicing.templates` | `/admin/settings/invoicing/template` |

## What the merchant can do here

- See a **live preview** of how the invoice will look.
- **Click a section in the preview** to open its settings modal/panel.
- Configure **header rows** — arbitrary `{ key, value }` pairs (e.g., `"VAT №" → "BG123456789"`). Stored as `custom_header_text` JSON. See [[settings-invoicing-issuer-block]] for the company-info side; this section also embeds the row builder for additional header lines.
- Configure **what's printed** on the invoice — toggles for product image thumbnails, barcodes, payment details, zero-shipping line hiding.
- Choose what the invoice's **payment block** prints (`show_payment_details`, `show_payment_description`).
- Edit **footer fields** — `issuer_name`, `issuer_code`, `footer_note`.
- Link to an **external accounting system** if installed — see [[settings-invoicing-external-systems]].

## Settings & fields

### Print-content toggles

| Field | Key | What it does |
|-------|-----|--------------|
| Show payment details | `show_payment_details` (bool) | Print the IBAN / account info on the invoice footer. |
| Show payment description | `show_payment_description` (bool) | Print the merchant-configured payment-method description text. |
| Print product barcode | `print_product_barcode` (bool) | Render each line item's SKU/EAN as a barcode in the items table. |
| Show product image in list | `show_product_image_list` (bool) | Render thumbnail next to each line item. |
| Hide zero shipping | `invoice_hide_zero_shipping` (bool) | If shipping cost is 0, don't show the shipping line. |
| Items default classes | `invoice_items_default_classes` | **Read-only reference list** of the CSS class names the default items table already uses, shown for custom-template authors. Not a setting; nothing is filtered at render time. |

`billing_invoicing` is **not** on this tab and is not a payment-provider picker — it is the *"Issue an invoice only if a billing address is selected"* switch in the General settings box. See [[settings-invoicing-activation-modes]].

### Click-to-edit section modal — the five sections

The five clickable sections in the preview and their corresponding modal titles:

| Section ID | Modal title | Settings exposed |
|------------|-------------|------------------|
| `header` | "Invoice header settings" | Logo (file slot via [[settings-brand]]), `invoice_number_formatting_padding`, and the number **prefix / suffix** fields with their variables legend (`[OY]`, `[OM]`, `[OD]`, `[CID]`, `[CGID]`, `[DATE]` — clicking a chip inserts or removes the token). |
| `company_info` | "Invoice company info settings" | All issuer fields: `company_name`, `company_bulstat`, `company_vat`, `site_phone`, `company_mol`, `country`, `site_city`, `site_street`, `postal_code`, plus the custom-rows builder. See [[settings-invoicing-issuer-block]]. |
| `list` | "Invoice products list settings" | `show_product_image_list`, `print_product_barcode`, `invoice_hide_zero_shipping`. |
| `payment` | "Invoice payment settings" | `show_payment_details`, `show_payment_description`. |
| `footer` | "Invoice footer settings" | `issuer_name`, `issuer_code`, `footer_note` (text area). |

Each modal carries its own preview sub-component so the merchant sees a focused preview of just the section being edited.

## Business rules

### Desktop vs mobile layout

- **Desktop (> 1024 px)**: section settings appear inline in the left side-panel (5/12 width), next to the live preview (7/12 width). Hint text *"Hover the invoice preview to edit sections"* shown above the panel.
- **Mobile (≤ 1024 px)**: clicking a section opens a **full-screen modal** with the section preview on top and settings below. Hint text changes to *"Click on the section you want to edit"*.

### Modal close = "Close X" only — no Cancel button

Modal Save button here is purely a "Close" — the actual persistence is the global page-level Save. The modal has **no Cancel button** (`hide-cancel: true`) — closing without saving is the X icon only.

### Logo is not uploadable here

The merchant **cannot** upload the invoice logo from this page. The invoice logo (`invoice` slot) is uploaded on [[settings-brand]]. The presence or absence of that logo affects what the invoice template renders, but this page only reads it.

### Custom header rows feed `custom_header_text` JSON

The header section embeds the row-builder for arbitrary `{ key, value }` lines (e.g., `"VAT №"` → `"BG123456789"`). Rows serialise into `custom_header_text` JSON on save and print at the top of the invoice. No count cap. The same row-builder appears on the Credit note tab feeding `credit_custom_header_text` — see [[settings-invoicing-credit-note]].

### Variables legend chips insert tokens — they do not copy

A small chip palette renders inline below the padding input on the Header section: `[OY]`, `[OM]`, `[OD]`, `[CID]`, `[CGID]`, `[DATE]`.

Clicking a chip **appends** that token to the prefix (or suffix) field the palette belongs to; clicking it again **removes** it from that field. It is a toggle, and nothing is placed on the clipboard. What each token actually substitutes — and why the on-screen labels are misleading — is on [[settings-invoicing-numbering]].

## Related

- [[settings-invoicing]] — hub.
- [[settings-invoicing-issuer-block]] — fields opened by the `company_info` section modal.
- [[settings-invoicing-numbering]] — numbering fields opened by the `header` section modal.
- [[settings-invoicing-credit-note]] — credit-note tab uses the same modal pattern.
- [[settings-invoicing-html-templates]] — third tab where the raw HTML is edited.
- [[settings-brand]] — `invoice` logo slot.
- [[settings-invoicing-activation-modes]] — where `billing_invoicing` and the generation modes actually live.
- [[settings-payment-providers]] — the payment data the invoice's payment block prints.
- [[invoice]] — entity.

## Open questions

None.
