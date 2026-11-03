---
type: feature
nav_path: "Profile → My subscriptions → Subscription → Transactions → Record"
route_name: admin.subscriptions.transaction.details
route_path: /admin/subscriptions/{unique_id}/transaction/{id}/details
aliases: ["Subscription transaction record", "Transaction fields", "Transaction approved values", "Transaction status values", "Запис на транзакция на абонамент"]
tags: [subscriptions, transactions, billing, account, modern-vue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions-transactions]]. See the hub for the other aspects (the table, invoices).

# Subscription transactions — the record

## Purpose

The **underlying transaction record** behind each row: the per-row field reference, the four `approved` status values, and the business rules that govern when rows are created and what their data means (one row per attempt, bank vs card payments, zero-amount subscriptions that never charge, card-on-file snapshotting). This is the "what does this field mean and why is this row here?" reference. The on-screen table is on [[subscriptions-transactions-table]]; the invoice side on [[subscriptions-transactions-invoices]].

## Where to find it

The fields back the table on [[subscriptions-detail]] (below the info cards) and the condensed expandable row on [[subscriptions]]. The detail-modal lookup goes through `admin.subscriptions.transaction.details` (legacy); the modern Vue stack reads the list via `/admin/api/core/billing?filters[subscription_id]=<unique_id>`.

## What the merchant can do here

This is a reference for understanding the record — there are no actions unique to it. The merchant reads these fields through the table (see [[subscriptions-transactions-table]]) and the Status dropdown. All rows are immutable historical records — the merchant cannot edit, delete, or add a transaction by hand.

## Settings & fields

The transactions endpoint exposes per-row:

| Field | Notes |
|-------|-------|
| `id` | Primary key. Used to look up the transaction-details modal. |
| `subscription_id` | The owning subscription's `unique_id` (foreign key). |
| `reference_id` | Gateway / processor reference — visible in the **ID** column. |
| `description` | Free-text description of the charge. |
| `amount` / `amount_formatted` | Amount + formatted version (with currency). |
| `currency` | Currency code (BGN / EUR / USD / etc.). |
| `approved` | `1` Approved (success), `0` Declined (failure), `2` Voided, `3` Refunded. The Status column only renders Approved/Declined badges; Voided/Refunded statuses don't have a dedicated badge in the modern UI. |
| `invoice_id` | When Approved, points to the issued invoice. Null when Declined. |
| `invoice_number` | The issued invoice's number (text). Visible in the **Document number** column. |
| `payment_method` | `card` (recurring auto-charge) or `bank` (manual bank-transfer payment). |
| `payment_provider` | Which payment provider processed this charge. |
| `created_at` | When the charge attempt happened. |
| `settled_at` | When the charge settled at the bank (when applicable). |
| `details.card_unique_id` | Card ID (from card on file). |
| `details.card_type` | Card brand. |
| `details.card_number` | Masked card number. |
| `details.response` | Processor response message. |

## Business rules

### One transaction row per charge attempt

Each renewal attempt creates a transaction row, whether it succeeds or fails. So a subscription that took 4 attempts to renew successfully has 4 transaction rows: 3 with `approved=0` and 1 with `approved=1`. This gives the merchant a full audit trail of dunning attempts.

### Transaction status values beyond Approved / Declined

The underlying `approved` field has 4 values:

- `0` — **Unpaid / Declined** (charge failed)
- `1` — **Paid / Approved** (charge succeeded)
- `2` — **Voided** (charge was reversed before settlement)
- `3` — **Refunded** (settled charge was refunded)

The modern Vue UI only renders Approved (1) and Declined (0/everything else) — Voided and Refunded transactions surface as Declined-styled badges with their underlying status name visible only via the gateway response message. See [[subscriptions-transactions-table]] for the render-gap detail.

### Card-on-file changes over time

The **Card ID** + **Card number** in the Status dropdown reflect the card that was charged at the moment of THIS attempt — not the card currently on file. So if the merchant updated their card after several failed attempts, older transaction rows still show the old card details. This is intentional — it preserves the audit trail.

### Manual bank-transfer payments also appear here

When `payment_method == 'bank'`, the transaction represents a bank-transfer payment manually confirmed by CloudCart staff (typically for enterprise customers or merchants who can't / don't want to pay by card). These rows have card details that may be empty or generic — the Response field carries the bank-confirmation note.

### Transaction reference_id is generated by the gateway

For card transactions, the `reference_id` is whatever the processor returned (e.g., a Stripe-style charge ID, an iCard transaction reference). For bank transactions, it's typically set to the current-time timestamp at the moment of confirmation. The reference is what support uses to investigate gateway-side issues.

### "Pay-only" subscriptions (zero-amount) don't generate transactions

Active subscriptions with `next_billing_amount = 0` (free trials, complimentary add-ons) never produce transaction rows because no charge is attempted. Their transaction table is empty.

### Permission — owner-only

Inherits from [[subscriptions]] / [[subscriptions-detail]] — only store owners can access subscription screens.

## Related

- [[subscriptions-transactions]] — hub.
- [[subscriptions-detail]] — the parent screen whose table is backed by these fields.
- [[billing-cards]] — the saved card whose snapshot is stored per attempt.
- [[plans-purchase]] — the purchase flow that creates the initial transaction row.

## Open questions

(All resolved.)
