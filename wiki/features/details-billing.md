---
type: feature
nav_path: "Details → Billing"
route_name: billing-list
route_path: /admin/details/billing
aliases: ["Billing history", "Transaction history", "Payment history", "Billing list", "Account billing", "История на плащанията", "Транзакции"]
tags: [accountdetails, details, billing, transactions, invoices]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# Billing

## Purpose

The **Billing** tab inside *Details* is the merchant's **transaction history** for everything they've paid to CloudCart — every plan renewal, app subscription charge, feature-pack purchase, professional-services invoice, manual top-up, refund, void. Each row represents ONE transaction (a single attempt to charge the card), shows whether it succeeded / failed / was refunded / voided, and links to the resulting invoice PDF if any.

This is a **read-only audit log** — the merchant cannot edit or void transactions from here. To affect future charges, they go elsewhere: change the card on [[billing-cards]], cancel a recurring item on [[subscriptions]], or contact CloudCart support for refunds.

The screen sits as one of the tabs in the *Details* area alongside [[customers-details|Subscriptions]] (the merchant's CloudCart subscriptions), Invoices (the issued PDFs), Offers, and Contracts. Each tab is a different lens on the same billing relationship.

## Where to find it

- **Details (sidebar) → Billing** tab.
- **Profile dropdown → Billing** routes the merchant into the *Details* area; the **Billing** tab is one of the sub-tabs there.
- Some in-app notifications about a failed renewal also link here so the merchant can see the failed transaction's details.

URL pattern: `/admin/details/billing`.

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[details-billing-transaction-list]] — the data-table layout; columns (Date / Description / Status / Total / Invoice); expandable card-details row; status filter; pagination + URL-state; the flattened per-row data shape; "no row actions" rule.
- [[details-billing-statuses]] — the `approved` code mapping (0/1/2/3); *Failed* vs *Voided* vs *Refunded* semantics; localised `status_name` badge; refunds / voids surface only when support runs them.
- [[details-billing-invoice-download]] — the per-row *Download* button; visibility rule (`approved == 1` AND `invoice_id` set); same PDF as the Invoices tab; transaction-vs-invoice distinction (many transactions per invoice).
- [[details-billing-retry-schedule]] — the failed-renewal retry table (2/3/4/5 days, max 5 attempts); PAST_DUE vs EXPIRED timing (~30-day window); why pre-flight rejections don't create a row.

## What the merchant can do here

- **View the transaction list** — one row per charge / refund / void attempt, with Date, Description, Status badge, Total, and an Invoice download link. See [[details-billing-transaction-list]].
- **Expand a row** to see the card metadata captured at charge time (brand, masked number, gateway response text). See [[details-billing-transaction-list]].
- **Filter by status** — *Unpaid* / *Paid* / *Voided* / *Refunded* (the `approved` filter). See [[details-billing-statuses]].
- **Paginate / sort** — page-size selector (25 default), newest-first by ID. No user-controllable column sort. See [[details-billing-transaction-list]].
- **Download the invoice PDF** for any successful transaction that has an issued invoice. See [[details-billing-invoice-download]].

## What the merchant cannot do here

- **Void / refund a transaction** — not exposed in the UI; requires CloudCart support. See [[details-billing-statuses]].
- **Edit / re-attempt a failed charge directly** — the platform auto-retries on its own schedule; to force a fresh attempt the merchant replaces the card on [[billing-cards]]. See [[details-billing-retry-schedule]].
- **See pre-flight rejections** — only charges actually attempted by the gateway create a row. See [[details-billing-retry-schedule]].
- **Download a PDF for an unpaid / voided / failed transaction** — the Download button is hidden unless `approved == 1`. See [[details-billing-invoice-download]].
- **Sort by description, status, or amount** — column sorting is disabled (fixed insert-ordered audit log). See [[details-billing-transaction-list]].

## Settings & fields

| Column | What it shows | Notes |
|--------|---------------|-------|
| **Date** (created_at) | Transaction creation timestamp | Formatted using merchant's `format.dateTime` setting |
| **Description** | Plain text — what was charged | Built from the transaction's invoice item or fallback description |
| **Status** (status_name) | Coloured badge: *Failed* / *Success* / *Voided* / *Refunded* | See [[details-billing-statuses]] |
| **Total** (amount_formatted) | Charge amount + currency | Includes VAT |
| **Invoice** | Download PDF link | Visible only when `approved == 1` AND `invoice_id` is set; see [[details-billing-invoice-download]] |

The only filter is **Status** (`approved`): 0 = Unpaid (Failed), 1 = Paid (Success), 2 = Voided, 3 = Refunded. Default sort is `id` descending. Full column / filter / data-shape detail lives on [[details-billing-transaction-list]].

## Business rules

- **List is scoped to the merchant's own site** — transactions are filtered to the current site; other sites under the same account are not mixed in.
- **Card details captured at transaction time** — the brand / masked number / response text shown on a row is the gateway response from the moment of the charge, independent of the card currently on file ([[billing-cards]]). Replacing the card later does not rewrite historical rows.
- **LTA-contract transactions** show here under the merchant's standard view; a separate internal "for-contract" lens is surfaced by [[contracts]], not browsable from this tab.
- Each row is a **transaction, not an invoice** — see [[details-billing-invoice-download]].
- Status semantics + the `approved` code mapping — see [[details-billing-statuses]].
- Failed-renewal retry timing + the PAST_DUE → EXPIRED window — see [[details-billing-retry-schedule]].

## Related

- [[customers-details|Subscriptions]] — the merchant's recurring CloudCart subscriptions (cancel from here).
- [[customers-details-payments|Invoices]] — list of issued invoices (the documents); this Billing tab lists the underlying transactions (the charge attempts).
- [[billing-cards]] — the saved card these transactions were charged against.
- [[billing-invoicing]] — the invoice details printed on each PDF.
- [[plans]] — plan purchases generate transactions visible here.
- [[plan-features]] — feature-pack purchases generate transactions visible here.
- [[plans-purchase]] — the purchase flow that creates the initial transactions.
- [[expired-subscription]] — what happens when transactions repeatedly fail.
- [[contracts]] — LTA-contract transactions show here under the same view.
- [[merchant-subscription-lifecycle]] — merchant-question hub: "where do I see my charge history / why was I charged / how do I download my invoice PDF?".

## Open questions

(All resolved.)
