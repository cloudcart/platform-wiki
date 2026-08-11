---
type: feature
nav_path: "Settings → Invoicing → Credit note template"
route_name: credit-note.template
route_path: /admin/settings/invoicing/credit-note
aliases: ["Credit note template", "credit_payment", "Credit note header rows", "credit_custom_header_text", "Method of payment by credit note"]
tags: [settings, invoicing, credit-note, refunds]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[settings-invoicing]]. See the hub for the other aspects (activation modes, numbering, issuer block, template editor, HTML templates, external systems).

# Invoicing — credit note template tab

## Purpose

The Credit note template tab carries the credit-note-specific equivalents of the invoice settings: header rows, numbering, and the **Method of payment by credit note** picker. The hidden detail: `credit_payment` neither routes a refund nor changes a payment status — it only overrides the **payment method printed on the document**.

## Where to find it

Sidebar → Settings → **Invoicing** → **Credit note template** tab. Route name `credit-note.template`. Route path `/admin/settings/invoicing/credit-note`.

## What the merchant can do here

- Configure credit-note-specific **header rows** via the row-builder feeding `credit_custom_header_text` JSON (same model as invoice header rows, separate field).
- Pick **Method of payment by credit note** (`credit_payment`) — the payment method **printed** on the document.
- Set the credit-note **number padding** (`credit_number_formatting_padding`) and edit the credit-note number **prefix / suffix** via the chip palette.
- See the variables-legend chips (`[OY]` / `[OM]` / `[OD]` / `[CID]` / `[CGID]` / `[DATE]`) — same tokens as the invoice tab, but writing into the credit-note prefix/suffix fields. See [[settings-invoicing-numbering]].

## Settings & fields

### Credit-note template — General settings box

| Field | Key | Type | Notes |
|-------|-----|------|-------|
| Method of payment by credit note | `credit_payment` | select (payment-provider ref) | Dropdown of the store's configured payment providers, plus a first option **"Do not change the payment method"**. Default literal value: `no_change`. Affects only what is printed — see Business rules. |
| Credit note number padding | `credit_number_formatting_padding` | number | Browser-side minimum of 0; **no server-side rule**. Default 10. This is the padding the credit-note renderer reads. |
| Credit-note number prefix / suffix | `credit_number_formatting_prefix`, `credit_number_formatting_suffix` | free text + chip palette | Edited through the variables-legend component on this tab. See [[settings-invoicing-numbering]]. |
| Credit-note header rows | `credit_custom_header_text` (JSON) + `credit_header_rows` (computed array) | row builder | Same model as invoice header rows; separate storage. |

### Cross-tab fields

Two credit-note controls also appear on the **HTML templates** tab, sharing the same storage — see [[settings-invoicing-html-templates]]:

- `credit_number` — a second, differently-named padding field ("Invoice number padding"), the one the save validator caps at 10.
- `credit_payment` — the same picker as above.

The credit-note **prefix / suffix** fields are NOT duplicated there; they exist only on this tab.

### Reference list, not a setting

`credit_items_default_classes` is a **read-only list of CSS class names** the platform's default credit-note markup already uses (`.product-name`, `.product-quantity`, `.total-amount`, …). It is shown so a merchant writing a custom HTML template knows which hooks exist. It is not stored, not editable, and nothing is filtered at render time — a custom template may use any class it likes.

### Credit-note issuer defaults

When `credit_issuer_name` / `credit_issuer_code` are empty, the platform auto-fills them the same way as invoice issuer fields — from the store owner's first/last name and admin user-ID padded to 7 digits. See [[settings-invoicing-issuer-block]] for the full default-issuer rule.

## Business rules

### `credit_payment` only changes the payment method PRINTED on the document

The label — *"Method of payment by credit note"* — reads like a refund instruction. It is not one. What it does:

- The dropdown lists the store's configured payment providers ([[settings-payment-providers]]) with a first option **"Do not change the payment method"** (the literal value `no_change`, which is the default).
- When a provider is selected, the payment line printed on the **credit note and the invoice** is relabelled with that provider's storefront name and dated with the credit-note's date, instead of showing the method the customer originally paid with.
- Nothing is saved to the order, no refund is routed anywhere, and no payment or order status changes. The substitution happens only while the document is being rendered.

So a merchant who refunds by bank transfer an order that was paid by card can make the credit note read "Bank transfer" — but they still have to move the money themselves ([[orders-payment-refund]]) and the order's own payment record still shows the card.

### Validation error on `credit_number` deep-links to HTML templates tab

Per the page's `errorKeysByPageEnum`, a validation error on `credit_number` navigates the merchant to the **HTML templates** tab — where that field lives. The merchant never has to hunt for which tab is breaking.

### Sequence is independent from invoice numbering

Credit-note numbers come from their own counter and `credit_number_formatting_*` fields — fully decoupled from invoice numbering. The merchant cannot set the sequence's starting number. See [[settings-invoicing-numbering]] for the full prefix + padded counter + suffix mechanics, the no-inherited-relationship rule between invoice and credit-note numbers, and the fact that one series covers both whole-order and partial-return credit notes.

### Header rows are independent from invoice header rows

`credit_custom_header_text` is stored separately from the invoice `custom_header_text`. So the merchant can show e.g., "Тhis is a credit document, issued in reference to invoice [parent]" only on credit notes, without touching invoices.

## Related

- [[settings-invoicing]] — hub.
- [[settings-invoicing-numbering]] — credit-note number prefix / padding / suffix mechanics.
- [[settings-invoicing-html-templates]] — third tab, which carries the second `credit_number` padding field and a duplicate `credit_payment` picker.
- [[settings-invoicing-template-editor]] — invoice equivalent of the row-builder + section modals.
- [[settings-invoicing-issuer-block]] — issuer-name / issuer-code defaults applied to credit notes too.
- [[settings-payment-providers]] — populates the `credit_payment` dropdown.
- [[settings-statuses]] — order payment-status workflow (NOT driven by `credit_payment`).
- [[credit-note]] — entity.
- [[order-processing-pipeline]] — actual status-transition pipeline.
- [[orders-payment-refund]] — where the money actually moves.
- [[orders-credit]] — refund money-movement audit (the financial side).

## Open questions

None.
