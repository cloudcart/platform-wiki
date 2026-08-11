---
type: feature
nav_path: "Sidebar → Orders → Withdraw from contract"
route_name: orders.aftercare.list
route_path: /admin/orders/aftercare
aliases: ["Withdrawal inbox", "Withdrawal requests", "Aftercare inbox", "withdrawal lifecycle", "withdrawal status", "resolution type", "refund method", "aftercare emails", "withdrawal detail", "pending returned cancelled", "credit note withdrawal"]
tags: [apps, aftercare, orders, returns, withdrawal, inbox]
plan_gates: []
created: 2026-07-24
updated: 2026-07-24
source_count: 1
---

> Part of [[apps-aftercare]]. See the hub for the other aspects (compliance, settings, free-vs-Pro, storefront flow).

# Aftercare — the withdrawals inbox (admin)

## Purpose

Where the merchant receives, reviews, and resolves the withdrawal requests the storefront flow ([[storefront-withdrawal]]) creates, and the emails the app sends along the way.

## Where to find it

**Sidebar → Orders → Withdraw from contract** (`orders.aftercare.list`, `/admin/orders/aftercare`) — a list filterable by status (newest first), plus a per-request detail view. The screen shares a tabbed interface with the app's **Settings** ([[aftercare-settings-setup]]).

## What the merchant can do here

- Review each incoming withdrawal request (customer, order, items, refund total, terms snapshot).
- Advance its status (`pending → returned / cancelled`), optionally emailing the customer a note.
- Record the refund (method + reference) and, on Pro, let it flow into a core order-return.

## Settings & fields

Each request shows the customer (name / email), the order it references, the withdrawn items, the frozen refund total, the accepted terms snapshot ([[aftercare-compliance]]), and the event log.

## Business rules

### Lifecycle — `pending → returned / cancelled`

Each request carries a status the merchant advances: **`pending` → `returned` / `cancelled`** — the same three-state set as a core order return. `pending` is the new, unprocessed request; the merchant moves it to `returned` once accepted / processed, or `cancelled` to close it without a return. A status change can **email the customer** (`notify_customer`) together with a free-text **note** (`status_note`, e.g. the reason). Each change is recorded as an **event** on the request.

On **Pro** with `auto_create_return`, a **linked core order-return becomes the source of truth** for the status: the selector here is **locked** and a direct change is rejected — the return propagates `returned` / `cancelled` back instead. See [[aftercare-order-return-sync]].

### Resolution type + refund method

Two fields describe what the customer asked for:

- **Resolution type** — **`withdrawal`** (returning part of the order). On Pro, a whole, **not-yet-shipped** order selected in full is recorded as **`cancel`** instead. (The **`exchange`** and **`voucher`** resolutions exist in the data model but are not yet operational — see [[aftercare-free-vs-pro]].)
- **Refund method** — **`bank`** (the customer supplies name + IBAN / BIC for a manual transfer) is available on every plan. On Pro, when the order was paid by an online **card** gateway that supports the refund for that scope, the customer may instead choose **`card`** — the app records the choice for the merchant to execute (the automated gateway refund is not yet wired). A **`wallet`** method is declared but not yet built.

### Refund amount + credit note

A **partial** withdrawal (some lines) freezes a **refund total** per item — **goods only** (shipping and COD excluded), after the apportioned cart discount, VAT-inclusive — so the amount is fixed at request time; a **whole-order** withdrawal is a full return whose amount (**goods + shipping + fees**) is read from the order at display time.

Resolving a request does **not** itself issue a credit note: the app records the refund (amount, method, reference) and, on Pro, mirrors the withdrawal into a PENDING core order-return (`auto_create_return`); the merchant issues any credit note through the normal order / return flow, and the request links it via `credit_note_id`.

### Emails the app sends

Installing the app **seeds a set of editable, per-language email templates**; the app then sends, at each stage of the flow:

| Email | To | When | Template / label |
|---|---|---|---|
| **Verification code** | customer | on submitting the statement, and on **resend** | the platform's 2-factor code email ([[account-cc2fa-email]]) carrying the 6-digit code |
| **Acknowledgement of receipt** | customer | on confirmation | `aftercare_withdrawal_acknowledgement` — the Art. 11a durable-medium acknowledgement |
| **Status update** | customer | when the merchant moves the request to **returned / cancelled** *and* keeps **"Notify customer"** on | `aftercare_status_returned` / `aftercare_status_cancelled` |
| **New withdrawal received** | merchant | on each newly confirmed request | `aftercare_withdrawal_received` (admin notification) |

The seeded templates are **editable in the store's email-template builder**: the customer ones live with the transactional [[settings-emails|customer emails]] (one design per store language, editable in the Unlayer builder); the merchant alert is an [[settings-admin-notifications|admin notification]]. The just-submitted / `pending` state has **no** status email — the acknowledgement already covers creation — and a status email is **skipped** when the merchant turns "Notify customer" off for that change.

## Related

- [[apps-aftercare]] — hub.
- [[storefront-withdrawal]] — the customer flow that creates the requests.
- [[aftercare-compliance]] — the terms snapshot + audit trail attached to each request.
- [[aftercare-free-vs-pro]] — which resolution / refund options and controls (`block_resubmit`, card refund) need Pro.
- [[settings-emails]] / [[settings-admin-notifications]] — where the seeded templates are edited.
- [[orders-details]] — the order + any credit note.
- [[account-cc2fa-email]] — the verification-code email the flow reuses.

## Open questions

None.
