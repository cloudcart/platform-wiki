---
type: feature
nav_path: "Profile → My subscriptions → Subscription → Transactions"
route_name: admin.subscriptions.transactions
route_path: /admin/subscriptions/{unique_id}/transactions
aliases: ["Subscription transactions", "Subscription history", "Subscription invoices", "Transaction details", "Транзакции на абонамент", "Хронология на абонамент"]
tags: [subscriptions, transactions, invoices, billing, account, modern-vue]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 0
---
# Subscription transactions

## Purpose

The **transaction history table** for one subscription — every renewal charge attempt the platform has made (successful + declined), each with the result and a downloadable invoice PDF when the charge succeeded. This is also where the merchant inspects **why** a charge was declined (card response code / message + which card was charged).

The table is rendered inline on [[subscriptions-detail]] under the three info cards (and inline within the expandable row on [[subscriptions]] for a quick-look preview).

This page was split into three aspect sub-pages because it covers three distinct concepts: the on-screen table (what columns show + how the status dropdown works), the invoice side (download + PDF generation rules), and the underlying transaction record (fields + the business rules that govern when rows are created). Drill into the aspect that matches the question.

## Where to find it

[[subscriptions]] → click a row → opens [[subscriptions-detail]] at `/admin/details/subscriptions/<unique_id>`. The transactions table appears below the info cards.

The transactions table is also rendered inline in the expandable row on [[subscriptions]] when the merchant clicks the expand toggle on the **Name** column — same data, condensed layout. See [[subscriptions-transactions-table]] for both layouts.

## Sub-pages (in this cluster)

- [[subscriptions-transactions-table]] — the on-screen table: the 7 columns (modern Vue), the Status dropdown showing the charged card's details, the legacy Smarty modal, the condensed inline expandable row, default sort, the no-filter limitation, and the Voided/Refunded render gap.
- [[subscriptions-transactions-invoices]] — the invoice side: the Download button (Approved-only), PDF generation rules (language follows recipient, site-scoping, best-effort generation), download access during suspension, and what the merchant cannot do (resend, edit, export, refund).
- [[subscriptions-transactions-fields]] — the underlying transaction record: the per-row field reference, the four `approved` status values (Approved / Declined / Voided / Refunded), and the business rules governing when rows are created (one row per attempt, bank vs card payments, zero-amount subscriptions, card-on-file snapshotting).

## What the merchant can do here

The merchant reads the charge history for one subscription, opens the Status dropdown on any attempt to see the card + processor response, and downloads the invoice PDF for any Approved charge. The full column-by-column breakdown is on [[subscriptions-transactions-table]]; the invoice-download behaviour is on [[subscriptions-transactions-invoices]].

The merchant **cannot** resend an invoice email, edit or refund a transaction, re-attempt a declined charge, or export the history from this surface — see [[subscriptions-transactions-invoices]] for the full list. Retries happen automatically on the platform's backoff schedule (see [[subscriptions]] → Renewal retry schedule); the merchant can trigger a fresh charge by clicking **Renew** on the list page.

## Settings & fields

Each row exposes a record with identity (`id`, `subscription_id`, `reference_id`), money (`amount` / `amount_formatted`, `currency`), result (`approved`, `invoice_id`, `invoice_number`), payment metadata (`payment_method`, `payment_provider`, `created_at`, `settled_at`), and a nested `details` object with the charged card (`card_unique_id`, `card_type`, `card_number`, `response`). The full per-field table is on [[subscriptions-transactions-fields]].

## Business rules

The substantive rules live on the aspect pages:

- **One transaction row per charge attempt** (success or failure) — a renewal that took 4 attempts has 4 rows. See [[subscriptions-transactions-fields]].
- **Approved transactions get an invoice; declined don't** — only `approved == 1` rows have an `invoice_id` + a Download button. See [[subscriptions-transactions-invoices]].
- **The `approved` field has 4 values** (Approved / Declined / Voided / Refunded), but the modern UI renders only Approved vs Declined — Voided/Refunded look like Declined. See [[subscriptions-transactions-fields]] + [[subscriptions-transactions-table]].
- **Invoice PDF language follows the recipient's stored language**, not the merchant's current admin locale; downloads are scoped to the merchant's own site. See [[subscriptions-transactions-invoices]].
- **Zero-amount ("pay-only") subscriptions never generate transaction rows** — no charge is attempted. See [[subscriptions-transactions-fields]].
- **Owner-only access** — inherits from [[subscriptions]] / [[subscriptions-detail]]; only store owners reach subscription screens.

## Related

- [[subscriptions]] — parent list (each row's expand toggle previews this data).
- [[subscriptions-detail]] — the parent screen where this table is rendered.
- [[plans]] — buying a plan creates the first transaction on this subscription.
- [[plans-purchase]] — the purchase flow that creates the initial transaction.
- [[billing-cards]] — the saved card whose details surface in the Status dropdown.
- [[details-billing]] — the merchant's all-subscriptions billing tab (cross-subscription transaction view) + invoicing-template / numbering / recipient settings used to generate each PDF.
- [[merchant-subscription-lifecycle]] — merchant-question hub for the full billing lifecycle.

## Open questions

(All resolved.)
