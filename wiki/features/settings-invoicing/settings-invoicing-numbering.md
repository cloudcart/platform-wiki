---
type: feature
nav_path: "Settings → Invoicing → Numbering"
route_name: invoicing.settings
route_path: /admin/settings/invoicing
aliases: ["Invoice numbering", "Invoice number formatting", "Number padding", "Number placeholders", "Credit-note numbering", "invoice_number_formatting_prefix"]
tags: [settings, invoicing, numbering, placeholders]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[settings-invoicing]]. See the hub for the other aspects (activation modes, issuer block, template editor, credit note, HTML templates, external systems).

# Invoicing — numbering

## Purpose

How invoice and credit-note numbers are assembled. The number = **prefix + zero-padded counter + suffix**, with `[OY]`/`[OM]`/`[OD]`/`[CID]`/`[CGID]`/`[DATE]` placeholders available inside the free-text prefix and suffix fields. Invoice and credit-note sequences are independent counters, neither of which the merchant can set a starting value for. Padding is capped at 10 digits.

## Where to find it

Sidebar → Settings → **Invoicing**. The numbering fields live on the **Invoice template** tab (Header section modal) and on the **Credit note template** tab. The variables-legend chip palette appears inline below the padding input on both tabs.

## What the merchant can do here

- Edit the **invoice** number's prefix / padding / suffix (`invoice_number_formatting_prefix`, `invoice_number_formatting_padding`, `invoice_number_formatting_suffix`).
- Edit the **credit-note** number's prefix / padding / suffix (`credit_number_formatting_prefix`, `credit_number_formatting_padding`, `credit_number_formatting_suffix`).
- Embed the placeholder tokens by clicking the chips in the variables legend — a chip click **appends** the token to the prefix (or suffix) field it belongs to, and clicking it again **removes** that token from the field. It is a toggle, not a copy-to-clipboard.

Neither sequence has a merchant-settable starting number. Both counters are platform-managed (`max(existing) + 1`).

## Settings & fields

### Invoice number storage (three separate fields, NOT one template string)

| Field | Key | Validation |
|-------|-----|------------|
| Invoice number prefix | `invoice_number_formatting_prefix` | Free text. Placeholders substituted at issue time. |
| Invoice number padding | `invoice_number_formatting_padding` | Integer, `min:0|max:10`. Default 10. Zero-pads the numeric counter. |
| Invoice number suffix | `invoice_number_formatting_suffix` | Free text. Placeholders substituted at issue time. |

### Credit-note number storage (mirrors invoice fields)

| Field | Key | Validation |
|-------|-----|------------|
| Credit-note number prefix | `credit_number_formatting_prefix` | Free text. |
| Credit-note number padding | `credit_number_formatting_padding` | Integer. The input enforces a minimum of 0 in the browser; there is **no server-side rule** on this key, so nothing rejects a large value on save. This is the padding the platform actually applies to credit-note numbers. Default 10. |
| Credit-note number suffix | `credit_number_formatting_suffix` | Free text. |
| Credit-note number padding (second field, HTML templates tab) | `credit_number` | Integer, `required|numeric|min:0|max:10`. Labelled **"Invoice number padding"** and its help tip describes zero-fill (*"if the credit note number is 123 and you set a fill of 10, the number will look like 0000000123"*), but the padding the renderer reads is `credit_number_formatting_padding` above. Default 10. Despite the name it is **not** a starting number for the credit-note sequence. See [[settings-invoicing-html-templates]]. |

### Placeholder set (`invoice_number_vars`)

Available inside both invoice and credit-note prefix/suffix free-text fields:

Available inside both the invoice and the credit-note prefix / suffix fields. The two groups of date tokens read **different** dates, and the on-screen legend labels are misleading about it:

- `[OY]` / `[OM]` / `[OD]` — year / month / day of the **document's own date**: the invoice date on the invoice tab, the credit-note date on the credit-note tab. Only when the document has no date of its own yet do they fall back to the order date.
- `[DATE]` — the **order** date (when the customer placed the order), in the store's configured date format. The legend labels this one "invoice date"; the value substituted is the order date.
- `[CID]` — the **customer's** ID. It is not a credit ID, an order ID, or any document identifier.
- `[CGID]` — the customer group ID.

So a merchant who wants the fiscal issue year in the number uses `[OY]`, not `[DATE]`. On a store that issues December orders' invoices in January, `[OY]` rolls the year over at the issue date, not at the order date.

## Business rules

### Format = prefix + padded counter + suffix

The number is NOT a single template string. The three fields are concatenated at issue time: prefix (with placeholders substituted) + the next integer in the sequence zero-padded to the configured width + suffix.

Example: prefix `INV-[OY]-` + padding `6` + empty suffix + counter `123` → `INV-2026-000123`.

### Invoice and credit-note sequences are fully independent

The two counters and their two sets of formatting fields are entirely separate, and there is no inherited relationship between an invoice and the credit note that reverses it: if invoice #100 is reversed by credit note #1, the credit note's number does NOT echo the invoice number (no `#100C` / `Credit-100` convention).

They also cannot be **made** to echo each other here: no placeholder carries a document identifier, so there is no token that would print the same value in both numbers.

### The credit-note series spans full AND partial credit notes

One continuous credit-note series covers both kinds of credit note the store can issue: the **whole-order** note issued on a cancelled / refunded order, and the **per-return** note issued against a partial [[orders-returns|return]]. The next number is the highest one already used across **both** sources, plus one. So a merchant looking only at whole-order credit notes will see numbers "jump" — the missing ones were consumed by partial returns (visible on [[orders-returns-lifecycle]]). This is by design: a tax audit needs a single gap-free series per document type, not one per source.

### Padding is capped at 10 digits — on the two validated fields only

`invoice_number_formatting_padding` and `credit_number` are validated `required|numeric|min:0|max:10`; a save above 10 fails. `credit_number_formatting_padding` — the value the credit-note renderer actually reads — has **no server-side rule**, only a browser-side minimum of 0. Validation error on `credit_number` routes the merchant to the HTML templates tab (where that field lives).

### Once consumed, a number is permanent

Once an invoice or credit-note number is issued to an order, it cannot be reassigned to another order — sequences are part of the merchant's permanent tax audit trail. See [[invoice]] / [[credit-note]] entity pages.

An invoice number also **freezes the order**: an invoiced order can no longer be edited at all (see [[orders-details-products]]), and its prices can no longer be converted from BGN to EUR (see [[orders-details-actions]]).

### Number generation timing depends on `invoice_number_type`

When `invoice_number_type=1` (system, default), the next number is auto-generated when the invoice is issued. When `invoice_number_type=2` (manual), the merchant types the number in a modal. When `invoice_number_type=3` (external), the external App supplies the number and the fields here are ignored. See [[settings-invoicing-activation-modes]].

## Related

- [[settings-invoicing]] — hub.
- [[settings-invoicing-activation-modes]] — `invoice_number_type` decides who supplies the next number.
- [[settings-invoicing-credit-note]] — credit-note tab where the credit-number formatting lives.
- [[settings-invoicing-html-templates]] — the tab that carries the second `credit_number` padding field.
- [[invoice]] — entity; the order carries `invoice_number` / `invoice_date`.
- [[credit-note]] — entity; a whole-order note lives on the order's `credit_number` / `credit_date`, a partial one on the return's `credit_note_number` / `credit_note_date`.
- [[orders-returns-lifecycle]] — partial returns that consume numbers from the same credit-note series.
- [[orders-details-products]] — the invoiced-order edit lock.
- [[orders-details]] — where individual invoices and credit notes are issued against orders.

## Open questions

None.
