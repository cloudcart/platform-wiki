---
type: feature
nav_path: "Details → Billing → Transaction list"
route_name: billing-list
route_path: /admin/details/billing
aliases: ["Billing transaction list", "Billing table", "Transaction table", "Billing list columns", "Expand card details", "Списък с транзакции"]
tags: [accountdetails, details, billing, transactions, table]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Billing — transaction list

> Part of [[details-billing]]. See the hub for related aspects (statuses, invoice download, retry schedule).

## Purpose

This aspect documents the **table itself** on the *Details → Billing* tab: the columns shown per row, the expandable card-details panel, the status filter, the pagination + URL-state behaviour, and the flattened per-row data shape. Each row is one transaction — a single charge / refund / void attempt against the merchant's card on file. The table is the only UI on the screen; there is no card wrapper around it.

## Where to find it

- **Details (sidebar) → Billing** tab — the table renders directly under the tab.
- URL pattern: `/admin/details/billing`. The active page / per-page state is reflected in the query string (e.g. `?page=2&perpage=25`), so a specific page can be bookmarked or shared.

## What the merchant can do here

### View the transaction list

Each row shows:

- **Date** — created timestamp, formatted to the merchant's date+time format setting (`format.dateTime`). The expand-row chevron lives in this column.
- **Description** — short plain text of what was charged (e.g. *Plan Pro — yearly*, *App: Mailchimp — monthly*, *Feature pack: +500 products*).
- **Status** — coloured badge (see [[details-billing-statuses]]).
- **Total** — amount charged, formatted with currency (includes VAT).
- **Invoice** — *Download* link to the PDF, visible only for approved transactions with an issued invoice (see [[details-billing-invoice-download]]).

### Expand a row for card details

Each row is expandable via the chevron. The expanded view shows the **payment-method details captured at the time of charge**:

- Card type (Visa / Mastercard / etc., uppercased, e.g. *VISA*).
- Masked card number (last 4 digits, e.g. `**** 1234`).
- Gateway response message (e.g. *Approved*, *Insufficient funds*, *3DS authentication required*, *Authentication required*) — shown only when the gateway returned a verbose response.

If the gateway didn't return details, the expansion shows *"Currently no details"*.

### Filter by status

A single dropdown filter is exposed (key `approved`, select-only — not a search input). Selecting a value narrows the list and re-fetches from page 1. The four values and their code mapping are documented on [[details-billing-statuses]].

### Paginate / sort

Standard table controls: choose page size (25 default), navigate pages. Default sort is `id` descending (newest first). No column is sortable from the merchant UI — the audit log is fixed insert-ordered, so "by date" effectively means the default ID-desc ordering.

## What the merchant cannot do here

- **Sort by Description / Status / Total** — all columns are non-sortable.
- **Act on a row** — there is NO per-row action menu. The only interactive elements are the expand chevron and (when applicable) the Download Invoice button. The merchant cannot void, refund, retry, or edit a transaction here — see [[details-billing-retry-schedule]] for what *does* happen to failed charges.

## Settings & fields

| Column / element | Field | Notes |
|------------------|-------|-------|
| Date | `created_at` | Formatted via the merchant's `format.dateTime` setting; hosts the expand toggle |
| Description | `description` | Plain text from the invoice item or a fallback description |
| Status | `status_name` | Coloured badge per `approved`; see [[details-billing-statuses]] |
| Total | `amount_formatted` | Charge amount + currency, VAT-inclusive |
| Invoice | `invoice_id` | Download link, visible only when `approved == 1` AND `invoice_id` set |
| Expand panel | `details` | Card type + masked number + gateway response; *"Currently no details"* when null |

The flattened per-row shape returned to the table is: `{ id, invoice_id, subscription_id, payment_method, reference_id, description, amount_formatted, approved, status_name, created_at, invoice: {...}, details: {...} }`. Of these, `payment_method` (`card`, `bank`, etc.), `reference_id` (the gateway's unique transaction ID — Braintree transaction-id / Stripe PaymentIntent ID), and `subscription_id` are stored but NOT shown as columns; support can surface `reference_id` when investigating a specific charge, and the merchant should be ready to quote it on a billing ticket.

## Business rules

### URL-state preservation

On each pagination event the table syncs the active page / per-page into the URL query string, so the view is bookmarkable and browser back/forward restores it. Applying a filter resets to page 1.

### Card details captured at transaction time

The expand panel reflects the gateway response from the moment of the charge — last 4 digits, brand, response text — independent of the card currently on file on [[billing-cards]]. If the merchant replaced their card after a failed transaction, the OLD card's masked details are still shown for the historical row. That is by design: the audit log reflects what was actually charged.

### List is scoped to the merchant's own site

The table is filtered to the current site only. Other sites under the same user account / multi-store relationship are not mixed in — each site has its own billing history.

## Related

- [[details-billing]] — hub.
- [[details-billing-statuses]] — the status badge rendered in the Status column.
- [[details-billing-invoice-download]] — the Download link rendered in the Invoice column.
- [[billing-cards]] — the saved card whose historical metadata appears in the expand panel.

## Open questions

(All resolved.)
