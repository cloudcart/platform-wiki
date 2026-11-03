---
type: concept
nav_path: "Concept → Merchant subscription lifecycle → Invoices (auto-generation + InvoiceMail)"
aliases: ["Subscription invoices", "Auto-invoice generation", "InvoiceMail", "Invoice PDF email", "Invoice download flow", "Invoice list", "Invoice details vs invoices list", "Invoice language by recipient"]
tags: [billing, subscription, invoice, pdf, email, lifecycle, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[merchant-subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, expiration, cancellation, feature packs, payment methods, support flow).

# Subscription invoices

## Definition

Every successful charge on a CloudCart subscription — first purchase, every renewal, manual Renew, feature-pack purchase, service purchase, paid-theme purchase — generates an **invoice PDF** server-side and **auto-emails it to the recipient** on file. The PDF is rendered using the merchant's stored [[billing-invoicing|invoice details]] (company name, VAT number, address, etc.) and the language is fixed at issuance time based on the recipient's language preference — NOT the merchant's current admin locale.

The merchant has three related surfaces for invoices:

- **Invoice details** ([[billing-invoicing]]) — the COMPANY INFO CloudCart prints ON each invoice.
- **Invoices list** (`/admin/details/invoices`, Vue route `invoices-list`) — the LIST of issued invoice PDFs.
- **Transaction history** ([[details-billing]]) — every charge attempt with a *Download* button per row that opens the resulting invoice PDF.

## Scope

What this page covers:

- The auto-invoice generation on every successful charge.
- The InvoiceMail auto-send to the recipient on file.
- The three merchant-facing surfaces: invoice details (input) vs invoices list (output) vs transaction history (audit).
- The Download flow + the URL pattern.
- Invoice language tied to recipient, not current locale.
- The `invoice.create` webhook fired alongside the email.

What it does NOT cover:

- The invoice-details form fields (company name, VAT, address) — see [[billing-invoicing]].
- The transaction history columns + filters — see [[details-billing]].
- Why a charge attempt failed (declined card, throttle, etc.) — see [[subscription-renewal-retry]] + [[subscription-payment-methods]].

## Contrasts

- **Invoice details (input) vs invoices list (output)** — *Invoice details* is the merchant's company info CloudCart prints on each invoice (an input the merchant maintains). *Invoices* (the merchant's *Profile → Invoices* dropdown entry) is the LIST of issued invoices (CloudCart's output). They live at two different URLs (`/admin/billing/invoicing` vs `/admin/details/invoices`).
- **Invoices list vs transaction history** — *Invoices* shows every ISSUED invoice (one per successful charge). *Transaction history* ([[details-billing]]) shows every CHARGE ATTEMPT (success AND failure). Failed attempts don't produce invoices but DO appear on the transaction history.
- **Auto-email vs manual download** — invoice PDFs are auto-emailed to the recipient on every successful charge. The merchant doesn't need to download manually. Manual download is still available from [[details-billing]] (the Download button on each approved transaction row) OR from `/admin/details/invoices` directly.
- **Invoice language at issuance vs current admin locale** — the PDF language is fixed at the moment the invoice is issued (recipient's language preference at that time). Subsequent merchant locale changes don't retroactively re-issue invoices in the new language.

## Where it applies

### Auto-generation on every successful charge

When the daily renewal pipeline OR a manual purchase OR a Renew click results in a successful charge, the platform:

1. Creates an `Invoice` record with `subscription_id`, line items (one per cart item; subscriptions purchased together share an invoice), recipient details snapshotted from [[billing-invoicing]], and a unique `invoice_number`.
2. Renders the invoice PDF server-side using the recipient's stored language preference.
3. Fires the `InvoiceCreate` event → downstream `invoice.create` webhook event fires for any merchant integration listening on that event (see [[settings-hooks]] for webhook configuration).
4. Sends the **InvoiceMail** to the recipient on file with the PDF attached (`Invoice for {merchant} #{invoice_number}` template; the language matches the recipient's stored preference).
5. The invoice becomes available at `/admin/api/core/invoice/download/{invoice_id}` for later download.

### The merchant's three surfaces

**(a) Invoice details** — the company info CloudCart prints:

- **Where**: Profile dropdown → Billing / Cards → opens the *Details → Billing* area → header summary on the page → pencil icon next to the *Invoice details* block.
- **Exact URL**: `/admin/billing/invoicing` (side-panel form).
- **Full documentation**: [[billing-invoicing]].

**(b) Invoices list** — issued PDFs:

- **Where**: Profile dropdown → **Invoices** (owner-only).
- **Exact URL**: `/admin/details/invoices` (Vue route `invoices-list`).
- **What it shows**: every invoice CloudCart has issued to this account, with invoice number, date, amount, recipient, and a Download link.

**(c) Transaction history** — every charge attempt + Download links per approved row:

- **Where**: Profile dropdown → **Billing / Cards** → routes to `/admin/details/billing`.
- **Exact URL**: `/admin/details/billing` (Vue route `billing-list`).
- **Full documentation**: [[details-billing]].

### Download flow

Every approved transaction with an issued invoice has a **Download** button → opens `/admin/api/core/invoice/download/{invoice_id}` in a new tab. The PDF is generated on demand using the stored Invoice record (so re-downloads are consistent with the originally-sent attachment).

The same Download button is also available on the rows of `/admin/details/invoices` for invoices the merchant wants to retrieve directly without going via the transaction history.

### Invoice language behaviour

The PDF language is determined by the recipient's language preference **at the moment the invoice was issued** — stored on the Invoice record itself. Subsequent merchant locale changes do NOT retroactively re-issue invoices in the new language. If the merchant needs an invoice in a different language for tax / regulatory reasons, support can re-issue.

### When invoices do NOT get auto-emailed

- **Charge failure** — no invoice is generated on a failed renewal attempt. The transaction history still records the failed attempt; the merchant can see it on [[details-billing]] but there's no invoice to download.
- **Free / complimentary subscriptions** (`next_billing_amount = 0`) — no invoice issued because there's no charge.
- **LTA / invoiced enterprise accounts** — invoices are issued on the contract's cadence by the account manager rather than per-charge from the auto-pipeline. See [[subscription-payment-methods]].

### The `invoice.create` webhook

Every issued invoice fires the `invoice.create` webhook event (alongside the `subscription.renew` event for renewal charges). Merchants integrating their own accounting / ERP system subscribe to this hook to mirror invoices into their finance system. See [[settings-hooks]] for webhook setup + [[notification-delivery]] for the delivery pipeline.

## Related

- [[merchant-subscription-lifecycle]] — hub.
- [[billing-invoicing]] — the invoice-details form (company info printed on each invoice).
- [[details-billing]] — transaction history + per-row Download links.
- [[subscription-payment-methods]] — the card on file that gets charged (and the LTA / manual carve-out where invoices issue differently).
- [[subscription-renewal-retry]] — the daily pipeline that fires the InvoiceCreate event on success.
- [[settings-hooks]] — webhook configuration for `invoice.create` / `subscription.renew`.
- [[notification-delivery]] — the pipeline behind the InvoiceMail email + the `invoice.create` webhook.

## Open Questions

- ⏸️ **InvoiceMail template customisation** — verify whether the merchant can customise the InvoiceMail template (subject / body) or whether it is fixed per-locale by the platform.
- ⏸️ **Re-send invoice email** — verify whether there's a merchant-accessible "Re-send invoice" button on the invoices list, or whether the merchant must rely on the Download flow if the original email was missed.
