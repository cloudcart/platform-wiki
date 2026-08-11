---
type: entity
nav_path: "Entity → Credit Note → Numbering"
aliases: ["Credit Note numbering", "credit_number_formatting_prefix", "Credit Note sequence", "Credit Note number pattern", "Credit Note vs Invoice number", "Permanent credit note number", "credit note number jumped"]
tags: [entity, finance, invoicing, refund, credit-note, numbering]
created: 2026-06-10
updated: 2026-08-06
source_count: 0
---

> Part of [[credit-note]]. See the hub for the other aspects (attributes, lifecycle, send flow, template rendering, external providers).

# Credit Note — Numbering

## Identity

This page documents **how the Credit Note number is assigned, formatted, and frozen**. Credit Note numbers come from a counter that is **independent of the Invoice sequence** but **shared between whole-order and partial Credit Notes**. Once a number is consumed, it can never be reassigned — Credit Notes are part of the merchant's permanent tax audit trail.

## Aliases

- **`credit_number`** — the order field storing a whole-order note's raw sequence integer.
- **`credit_note_number`** — the same on a **return**, for a partial note.
- **`credit_number_formatting_prefix` / `_padding` / `_suffix`** — the three merchant-configured display settings. There is no single pattern field.
- **Credit Note sequence** / **counter** — the merchant's monotonically-increasing integer.
- **Кредитно известие номер** — Bulgarian label.

## Key Attributes

| Concern | Value | Notes |
|---------|-------|-------|
| Counter type | Sequential integer | Monotonically increasing per merchant. |
| Counter source | Separate from the invoice counter, shared across note kinds | Independent of `invoice_number`; one series covers whole-order and partial notes. |
| Starting number | Not merchant-settable | Always the highest number already used, plus one. |
| Format config | `credit_number_formatting_prefix` / `_padding` / `_suffix` on [[settings-invoicing]] | Merchant-editable; the prefix / suffix accept placeholders — see [[settings-invoicing-numbering]] for what each one substitutes. |
| Immutability | **Permanent after issuance** | Cannot be reassigned even if Order is deleted. |
| Audit retention | **Forever** | Part of the merchant's tax audit trail. |
| Validation routing | Errors auto-navigate to HTML templates tab | See "Validation routing" below. |

## Numbering — separate sequence from invoices

Invoice numbers and credit-note numbers come from two **independent** counters with two separate sets of formatting settings:

- `invoice_number` / `invoice_number_formatting_*` — the [[invoice|Invoice]]'s counter and format.
- the credit-note counter / `credit_number_formatting_*` — the Credit Note's.

There is **NO inherited relationship** between an Invoice number and its Credit Note number. If Invoice `#100` is later reversed with Credit Note `#1`, the Credit Note's number does NOT echo the Invoice number — no `#100C` / `Credit-100` / `INV-100-C` convention. Both numbers appear on the printed Credit Note (it references the original Invoice in the body text), but the Credit Note's own number is a separate monotonically-increasing integer.

They also **cannot be made to look related** through these settings. The available placeholders carry customer data and dates, not document identifiers — in particular `[CID]` is the **customer** ID, not a credit ID or order ID — so there is no token that would print the same value in an invoice number and its credit-note number.

## One series, two sources — why numbers appear to jump

The same series covers both kinds of Credit Note the store can issue: the **whole-order** note on a cancelled / refunded Order, and the **partial** note issued on a [[orders-returns|return]]. The next number is the highest already used across **both** sources, plus one.

So a merchant reviewing only whole-order Credit Notes will see gaps — those numbers were consumed by partial returns. Nothing is lost and nothing is reused; the series is continuous when both sources are read together, which is what a tax audit requires.

## Permanence rule

Once a Credit Note number is consumed (see [[credit-note-lifecycle]]):

- The number is stamped onto the Order (`credit_number`) for a whole-order note, or onto the return (`credit_note_number`) for a partial one.
- The number cannot be reassigned to another Order even if the original Order is later changed or deleted.
- If the Order is deleted, the Credit Note number may remain as an **orphan record** in the merchant's tax audit trail.

This permanence is required by tax regulations in most jurisdictions — auditors require a complete, non-reusable sequence of issued documents. Skipping numbers (e.g., when issuance fails after the counter has advanced) is acceptable; reusing or reordering numbers is NOT.

## `credit_number` validation errors route to the HTML templates tab

If the merchant submits [[settings-invoicing]] with a validation error on `credit_number` — the padding field on the HTML templates tab, capped at 10 — the page **automatically navigates** to that tab and scrolls the failed field into view. The merchant never has to hunt for which tab is breaking.

## Number display in admin, emails, and PDFs

Credit Note numbers in the admin, customer emails, and downloaded PDF all use the merchant's configured prefix + padding + suffix (e.g., `CRN-2026-000045`). The raw integer is never displayed — every surface that mentions the Credit Note number passes it through the formatter. This means if the merchant changes the format later, **already-issued** Credit Notes will re-render with the NEW format on subsequent downloads (the raw integer is the only frozen value — see [[credit-note-template-rendering]]).

## External providers assign their own numbers

When the active Invoicing provider is an external accounting App (e.g. Szamlazz), the external system assigns the Credit Note number AND stores the document there — the platform's own formatting settings are **bypassed** and its internal series is not advanced. The platform records which provider issued the note. See [[credit-note-external-providers]] for the full handoff.

## Where it appears

- [[settings-invoicing]] — the configuration screen with the format editor.
- [[settings-invoicing-numbering]] — the dedicated numbering sub-page (what each placeholder substitutes).
- [[settings-invoicing-credit-note]] — the Credit Note configuration sub-page where prefix / padding / suffix are set.
- [[orders-credit]] — the whole-order action that consumes the next sequence number.
- [[orders-returns-lifecycle]] — the partial-return action that consumes from the same series.
- [[orders-details]] — displays the formatted Credit Note number once issued.
- [[orders-history]] — audit trail records the consumed number.

## Related

- [[credit-note]] — hub.
- [[invoice]] — sibling document with its own fully independent number sequence.
- [[settings-invoicing]] — template + number formatting + header rows + `credit_payment` printed-method override.
- [[settings-invoicing-numbering]] — the number-format editor sub-page.
- [[order]] — carries `credit_number` + `credit_date` for a whole-order note.
- [[orders-credit-numbering]] — the merchant-facing version of these rules, plus the over-credit ceiling and the post-reversal status lock.
- [[orders-credit]] — the per-order action where the counter advances.

## Open Questions

None.
