---
type: entity
nav_path: "Entity → Credit Note → Template & rendering"
aliases: ["Credit Note template", "Credit Note PDF rendering", "credit_body", "Credit note HTML template", "Credit Note placeholders", "PDF re-render", "Credit Note HTML editor"]
tags: [entity, finance, invoicing, refund, credit-note, templates, rendering]
created: 2026-06-10
updated: 2026-08-06
source_count: 0
---

> Part of [[credit-note]]. See the hub for the other aspects (attributes, lifecycle, numbering, send flow, external providers).

# Credit Note — Template & rendering

## Identity

This page documents **how the Credit Note PDF is generated** when the merchant downloads or sends it. The Credit Note is **NOT stored as an archived PDF** — every download re-renders fresh from the current Order data, using the merchant's configured HTML template (or the platform's default if no custom template is set). The `credit_number` + `credit_date` stamp is frozen on issuance; everything else in the rendered body can drift if the Order is edited after the Credit Note is issued.

## Aliases

- **`credit_body`** — the setting holding the merchant's custom credit-note HTML. Empty means the platform default is used.
- **HTML templates tab** — the [[settings-invoicing]] sub-tab where the merchant edits the template.
- **`credit_orders_placeholders`** — the placeholder set documented inside the editor.
- **`credit_items_default_classes`** — read-only list of the CSS class names the default markup uses.

## Key Attributes

| Concern | Behaviour | Notes |
|---------|-----------|-------|
| Storage model | **No archived PDF** — re-renders on every download | Only `credit_number` + `credit_date` are frozen. |
| Default template | Platform default | Used when `credit_body` is empty. |
| Custom template | Edited via HTML templates tab on [[settings-invoicing]] | Plain HTML + placeholder substitution. |
| Placeholder set | `credit_orders_placeholders` | Documented inside the HTML templates tab. |
| Validation | **None** — broken HTML renders as broken PDFs | No syntax validation on save. |
| CSS hooks | `credit_items_default_classes` | A read-only reference list of the class names the default markup uses. Nothing is filtered at render time. |
| Field validation routing | `credit_number` errors auto-jump to HTML templates tab | See [[credit-note-numbering]] for the routing rule. |

## PDF re-renders fresh from current Order data

The Credit Note is **NOT stored as an archived PDF** — every download re-renders from the current Order data (with the frozen `credit_number` + `credit_date`). This means **anything that changes after issuance will appear in subsequent re-downloads.** Only the number and date stay put.

Implications for the merchant:

- **Frozen**: the Credit Note's own number and date, and the parent invoice reference.
- **Live on every render**: the issuer / company block, which is read from [[settings-invoicing-issuer-block]] each time — so editing the company name, VAT, or address changes how historical Credit Notes print.
- **Live on every render**: addresses, tax breakdown, and credited total, which follow the Order's current state. (Line items are in practice stable, because an invoiced Order can no longer be edited — see [[orders-details-products]].)

Merchants who want a stable PDF should download the file once and archive it externally — the platform itself does not preserve the exact bytes that were issued. Most tax authorities accept this model because the auditable values (number, date, customer) are immutable; other drift is traceable via [[orders-history]].

## Template editing

The merchant edits the raw HTML for the Credit Note template directly in the admin via the embedded code editor on [[settings-invoicing]] (the HTML templates tab). The template uses **placeholder substitution** from the `credit_orders_placeholders` set documented inside the same tab.

**No syntax validation** — broken HTML renders as broken PDFs. If the merchant introduces a malformed tag or an undefined placeholder, the download produces a malformed PDF; the platform does not block the save or flag the template as broken. The merchant must test by downloading a sample Credit Note after editing.

Two custom-template hooks the merchant can target:

- **`credit_items_default_classes`** — the reference list of CSS class names the default markup uses, so a custom items table can be styled consistently. It is a read-only list, not a setting; a template may use any class it likes.
- **`credit_custom_header_text`** — free-form key/value lines printed at the top of the document — separate from the Invoice's header rows.

## Default template (when `credit_body` is empty)

When the merchant has not provided a custom template, the platform falls back to its built-in credit-note template. The default renders:

- Issuer block (merchant's company name, VAT, BULSTAT, MOL, address) — read **live** from [[settings-invoicing-issuer-block]] on every render, not snapshotted at issue time.
- Customer block (billing name, address, VAT).
- Credit Note metadata (number, date, parent Invoice reference).
- Line items table (product name, SKU/EAN, quantity, unit price, line total, per-line VAT reversal).
- Totals block (refund amount including VAT reversal).
- VAT exemption reason (when applicable — same wording as the Invoice).
- Header rows from `credit_custom_header_text`.

The default template renders in the customer's storefront language at order time, falling back to the site's primary language and then to the admin language.

## Locale and currency rendering

- **Locale** is copied from the Order's `locale` field (frozen at order time). The PDF renders in the customer's storefront language at order time. Fallback chain: order locale → site primary language → admin language.
- **Currency** is copied from the Order's `currency` (locked at order time). The Credit Note always renders in the Order's original currency, even if the store has since switched defaults.

These snapshot fields are not editable on the Credit Note itself — they're inherited from the parent Order's frozen-at-create snapshots.

## Items table content

Line items render with: product name, SKU / EAN (optionally as a barcode), quantity, unit price, line total, per-line VAT reversal. The content is **computed from the Order line items at render time** — there is no separate Credit Note line-item table. For **partial refunds**, the merchant edits the Order's line items first (which adjusts the Order total), then issues the Credit Note against the adjusted total — see [[credit-note-lifecycle]].

## Where it appears

- [[settings-invoicing]] — three-tab configuration screen including the HTML templates tab.
- [[settings-invoicing-html-templates]] — the dedicated HTML template editor sub-page.
- [[settings-invoicing-credit-note]] — the Credit Note configuration sub-page.
- [[orders-credit]] — the per-order action that triggers re-rendering on download.
- [[orders-details]] — where the Download button surfaces.

## Related

- [[credit-note]] — hub.
- [[settings-invoicing]] — template editor + numbering + header rows.
- [[settings-invoicing-html-templates]] — the HTML templates tab where the merchant edits the Credit Note template.
- [[settings-invoicing-issuer-block]] — issuer / company block, read live on every render.
- [[orders-credit]] — the per-order action.
- [[invoice]] — sibling document using a parallel template editor with its own placeholder set.

## Open Questions

None.
