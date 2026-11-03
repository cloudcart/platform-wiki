---
type: entity
nav_path: "Entity → Credit Note → Attributes & relationships"
aliases: ["Credit Note attributes", "Credit Note fields", "credit_number", "credit_date", "credit_payment", "Credit Note relationships", "Credit Note 1:1 invoice"]
tags: [entity, finance, invoicing, refund, credit-note, attributes]
created: 2026-06-10
updated: 2026-08-06
source_count: 0
---

> Part of [[credit-note]]. See the hub for the other aspects (lifecycle, numbering, send flow, template rendering, external providers).

# Credit Note — Attributes & relationships

## Identity

A **whole-order** Credit Note is not stored as its own record — it is the rendered PDF plus two fields on the parent [[order|Order]] (`credit_number` + `credit_date`). A **partial** Credit Note is stored on the **return** that produced it (`credit_note_number` + `credit_note_date`), which is what lets one Order carry several. Both draw on the same configuration on [[settings-invoicing]] (template, number formatting, header rows, printed-payment-method selector), reference the same parent [[invoice|Invoice]], inherit the [[tax|Tax]] treatment from the Order, and optionally carry an external-system reference when an external accounting App owns issuance.

## Aliases

- **`credit_number`** — the order field carrying the whole-order note's sequence integer.
- **`credit_date`** — the order field carrying the whole-order note's issuance timestamp.
- **`credit_note_number`** / **`credit_note_date`** — the same pair on a **return**, for a partial note.
- **`credit_payment`** — the dropdown on [[settings-invoicing]] that overrides the payment method **printed** on the document.
- **`credit_body`** — the merchant-editable HTML template for the credit note.
- **`credit_custom_header_text`** — free-form key/value lines printed at the top of the document.
- **`credit_items_default_classes`** — read-only list of CSS class names the default markup uses.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Credit-note number** (`credit_number` on the Order, `credit_note_number` on a return) | Set at issue time — formatted per the `credit_number_formatting_prefix` / `_padding` / `_suffix` settings on [[settings-invoicing]] | Sequential integer consumed from the platform's credit-note counter. **Immutable once assigned.** The counter is independent of the invoice counter but shared between whole-order and partial notes — see [[credit-note-numbering]]. |
| **Credit-note date** (`credit_date` on the Order, `credit_note_date` on a return) | n/a (set automatically at issue time) | Timestamp when the Credit Note was issued — distinct from the Order's `date_added` and the Invoice's `invoice_date`. Used as the tax point on the document. **Immutable once assigned.** |
| **Parent invoice number** | n/a (already present on the Order from the prior invoice issuance) | The Credit Note references the parent Invoice number in its body text. There is no inherited relationship between the two numbers — invoice and credit-note sequences are fully independent unless the merchant embeds the order ID in both formatting patterns. |
| **Credited amount** | n/a (computed) | A whole-order note credits the Order's totals as they stand at issuance. A **partial** note credits the frozen totals of the return's own lines. The sum of all non-cancelled notes on an Order can never exceed the Order total — see [[credit-note-lifecycle]]. Editing the Order down first is not an option: an invoiced Order cannot be edited ([[orders-details-products]]). |
| **Currency** | n/a (copied from the Order's `currency` at order time) | Currency is locked on the Order at create time — Credit Note always renders in the Order's original currency. |
| **Locale** (rendering language) | n/a (copied from the Order's `locale`) | The PDF renders in the customer's storefront language at order time, falling back to the site's primary language and then to the admin language. |
| **Reason / note** | (Limited — verify per provider) | Some external Apps let the merchant type a reason; the built-in renderer derives content from the order without a free-text field. |
| **Credit-note header rows** (`credit_custom_header_text`) | Configured on [[settings-invoicing]] | Free-form key/value lines at the top of the document — separate from the invoice's header rows. |
| **Printed payment method** (`credit_payment`) | Configured on [[settings-invoicing]] | Dropdown of the store's payment providers. It overrides only the payment method **printed** on the document; nothing is persisted and no refund is routed. Default `no_change` = print what the customer actually paid with. Label: *"Method of payment by credit note"*. |
| **HTML template** (`credit_body`) | Edited via the HTML templates tab on [[settings-invoicing]] | Default template when empty; merchant HTML with `credit_orders_placeholders` substitution when populated — see [[credit-note-template-rendering]]. |
| **Credit-items default classes** (`credit_items_default_classes`) | Not configurable — a read-only reference list | The CSS class names the default credit-note markup already uses, listed on [[settings-invoicing]] for template authors. Nothing is filtered at render time. |
| **Items table content** | n/a (computed at render time) | Product name, SKU/EAN, quantity, unit price, line total, per-line VAT reversal. |
| **VAT exemption reason** | Inherited from store/order tax config | Free-text legal reason when refunded lines qualify (intra-community supply, export). |
| **External-system reference** | Set by an external accounting App (e.g. Szamlazz) when it is the active provider | The external system assigns the number AND stores the document; the platform records which provider issued it — see [[credit-note-external-providers]]. |

Re-downloads re-render fresh from current Order data — see [[credit-note-template-rendering]].

## Relationships

A Credit Note **references** exactly one [[invoice|Invoice]] (the parent it reverses) in its body text, and **carries forward** the [[tax|Tax]] treatment from the Order — its line items reverse the same tax amounts the Invoice originally charged. An Order has **at most one Invoice**, but it can accumulate **one whole-order Credit Note plus one per credited return** — capped by the rule that the total credited must not exceed the Order total.

A Credit Note is **distinct from** but often paired with a **payment refund** ([[orders-payment-refund]]) — the money movement at the payment provider. The refund happens at the gateway; the Credit Note proves it. The two are independent: a merchant can refund without a Credit Note, or issue a Credit Note without refunding (rare — full-cancellation orders that were never paid).

## `credit_payment` only changes what the document PRINTS

The `credit_payment` setting on [[settings-invoicing]] (label: *"Method of payment by credit note"*) is neither a refund instruction nor a payment-status rule. Picking a provider simply relabels the payment line printed on the credit note (and on the invoice) with that provider's storefront name, dated with the credit-note's date, instead of showing the method the customer originally paid with. Nothing is saved to the Order, no money is moved, and no status changes. Default `no_change` — the first dropdown option, *"Do not change the payment method"* — leaves the original method printed. The actual refund is a separate action on [[orders-payment-refund]].

## Where it appears

- [[orders-credit]] — the per-order Credit Note generation + download + send flow.
- [[orders-details]] — the order detail hub; the **View credit note** dropdown lives in the header toolbar.
- [[settings-invoicing-credit-note]] — the dedicated Credit Note configuration sub-page.
- [[settings-invoicing-numbering]] — the number-format editor.
- [[settings-invoicing-issuer-block]] — issuer / company block, read live on every render (not snapshotted).
- [[orders-returns-lifecycle]] — where a partial Credit Note is issued and stored.
- [[orders-history]] — per-order audit log records Credit Note issuance.

## Related

- [[credit-note]] — hub.
- [[order]] — every Credit Note belongs to exactly one Order; an Order holds at most one whole-order note plus one per credited return.
- [[invoice]] — the Credit Note reverses all or part of the parent Invoice.
- [[orders-details-products]] — the invoiced-order edit lock behind the "no editing before crediting" rule.
- [[settings-invoicing]] — template + number formatting + `credit_payment` printed-method override + header rows.
- [[settings-payment-providers]] — the `credit_payment` dropdown lists the store's payment providers.
- [[tax]] — the Credit Note reverses the tax line from the Order's tax snapshot.
- [[orders-payment-refund]] — the payment-refund flow that typically pairs with the Credit Note issuance.

## Open Questions

- Pending: **External-system reference visibility** — when the active provider is an external App, where does the merchant see the external system's Credit Note ID? On the Order detail, on the PDF, or only in the external system itself?
- Pending: **Currency for refund vs Credit Note** — when the payment provider refunds in a different currency than the Order's original (rare but possible with FX), does the Credit Note's totals reflect the Order's currency or the refund's actual currency?
