---
type: feature
nav_path: "Profile → My subscriptions → Subscription → Transactions → Table"
route_name: admin.subscriptions.transactions
route_path: /admin/subscriptions/{unique_id}/transactions
aliases: ["Subscription transactions table", "Transaction columns", "Transaction status dropdown", "Transaction card details", "Таблица с транзакции на абонамент"]
tags: [subscriptions, transactions, billing, account, modern-vue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions-transactions]]. See the hub for the other aspects (invoices, transaction fields).

# Subscription transactions — the table

## Purpose

The on-screen surface the merchant reads to answer *"what was charged, when, and did it go through?"* — the transactions table for one subscription, plus the **Status dropdown** that reveals which card was charged and the processor's response. This page covers the visible layout (modern Vue table, legacy modal, and the condensed inline expandable row); the invoice side is on [[subscriptions-transactions-invoices]], the record fields on [[subscriptions-transactions-fields]].

## Where to find it

[[subscriptions]] → click a row → opens [[subscriptions-detail]] at `/admin/details/subscriptions/<unique_id>`. The table sits below the three info cards. The same data also renders, condensed, in the expandable row on the [[subscriptions]] list (click the expand toggle on the **Name** column).

## What the merchant can do here

### Table columns (modern Vue, 7 columns)

| Column | What it shows |
|--------|---------------|
| **Created at** | Datetime of the charge attempt, formatted per the store's locale. |
| **ID** | The `reference_id` — the gateway / processor's reference for this charge (used by support to look up the charge in the payment provider's dashboard). |
| **Description** | Free-text description of what was charged (e.g., *Plan: Business — 12 months, period 2026-05 to 2027-05*). |
| **Amount** | Charged amount in the transaction's currency, formatted (e.g., `199.00 BGN`). |
| **Status** | Badge: `Approved` (green check) or `Declined` (red cross). Clicking opens a dropdown showing the **card details** for that attempt (see "Status dropdown" below). |
| **Document number** | Invoice number issued for this charge (only populated when the charge was Approved). |
| **Actions** | **Download** button (only when Approved) — opens the invoice PDF in a new tab; see [[subscriptions-transactions-invoices]]. |

The table is paginated (default page size 25). Default sort: `id DESC` (newest charge attempts first).

### Status dropdown (modern Vue)

Clicking the **Status** badge opens a popover dropdown with the card details used for this attempt:

| Field | What it shows |
|-------|---------------|
| **Card ID** | The card's internal unique ID — useful to confirm which card on file from [[billing-cards]] was charged. |
| **Card type** | Card brand (Visa / MasterCard / etc.). |
| **Card number** | Masked card number (e.g., `4111 **** **** 1111`). |
| **Response** | The payment processor's raw response message — for Declined attempts this includes the decline reason (e.g., *Insufficient funds*, *Card expired*, *Do not honour*). |

The dropdown shows the same four fields whether the charge was Approved or Declined; on Approved attempts the Response field shows the success message. The card shown is the card charged **at that moment** — not necessarily the card currently on file (see [[subscriptions-transactions-fields]]).

### Legacy Smarty modal

On the legacy `/admin/subscriptions/<unique_id>` view, clicking the status icon opens a **modal dialog** (not a dropdown popover) titled **Details**, with the same four fields displayed in form-control rows. The modal is loaded via `admin.subscriptions.transaction.details`.

### Inline transactions in the expandable row ([[subscriptions]])

The expand toggle on the list page renders the SAME transaction data, in a more compact layout — date + description + amount + Approved/Declined badge + (for declined) the response message + (for approved) a **Download** button. The inline row shows `amount_formatted` (with currency) directly, but uses a simpler "Approved" / "Declined" badge **without** the dropdown of card details — the merchant who needs the card / response message must open the full detail page. When the subscription has no transactions, shows *"There is no data"*.

### What the merchant CANNOT do here

- Sort the table — there's no sortable indicator on any column; sort is fixed at `id DESC`.
- Filter the table — there is NO date / status / amount filter UI on this surface (see Business rules).
- Edit, refund, or re-attempt a transaction — all of that is covered on [[subscriptions-transactions-invoices]] and [[subscriptions-transactions-fields]].

## Settings & fields

The columns map to the transaction record's `created_at`, `reference_id` (ID column), `description`, `amount_formatted` (Amount), `approved` (Status badge), `invoice_number` (Document number), and the nested `details.*` card fields (Status dropdown). The full per-field table is on [[subscriptions-transactions-fields]].

## Business rules

### Approved-status check uses `approved == 1`

The Download button and the Approved badge style render only when `approved === 1`. Any other value (0/2/3) renders as the Declined style.

### Voided / Refunded transactions render the same as Declined

The modern admin UI does NOT have distinct status badges for **Voided** or **Refunded** transactions — both render identically to **Declined** (red "Failed" pill). To distinguish the three, the merchant must open the Status dropdown and read the **Response** text — that field carries the gateway's actual response code/message (e.g. *"Refunded"*, *"Voided"*, or a decline reason). The four underlying `approved` values are documented on [[subscriptions-transactions-fields]]. This is a known UI gap; a future iteration should add distinct badges for the three "non-Approved" states.

### Status dropdown is always available

Even on Declined transactions, the dropdown opens with the response message visible. Merchants use this to self-diagnose: "Insufficient funds" → top up card, "Card expired" → update card in [[billing-cards]], "Do not honour" → contact the card issuer.

### No filter UI on this surface

There is NO date / status / amount filter UI on the transactions detail surface. The full list of transactions for the subscription is loaded at once and paginated. To find a specific charge the merchant uses pagination + visual scan; for very long histories this is awkward. As a workaround, the per-row expandable row helps locate problem charges quickly.

### Default sort

The legacy Smarty list orders transactions by `id DESC` (newest first); the modern Vue list inherits the same default. Sort is not user-changeable from the column header.

## Related

- [[subscriptions-transactions]] — hub.
- [[subscriptions]] — parent list (the expandable row renders this same data, condensed).
- [[subscriptions-detail]] — the parent screen where this table is rendered.
- [[billing-cards]] — the saved card whose details surface in the Status dropdown.

## Open questions

(All resolved.)
