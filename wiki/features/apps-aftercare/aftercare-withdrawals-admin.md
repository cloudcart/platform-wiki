---
type: feature
nav_path: "Sidebar → Orders → Withdraw from contract"
route_name: orders.aftercare.list
route_path: /admin/orders/aftercare
aliases: ["Withdrawal inbox", "Withdrawal requests", "Aftercare inbox", "withdrawal lifecycle", "withdrawal status", "resolution type", "refund method", "aftercare emails", "withdrawal detail", "pending returned cancelled", "credit note withdrawal"]
tags: [apps, aftercare, orders, returns, withdrawal, inbox]
plan_gates: []
created: 2026-07-24
updated: 2026-11-09
source_count: 2
---

> Part of [[apps-aftercare]]. See the hub for the other aspects (compliance, settings, free-vs-Pro, storefront flow).

# Aftercare — the withdrawals inbox (admin)

## Purpose

Where the merchant receives, reviews, and resolves the withdrawal requests the storefront flow ([[storefront-withdrawal]]) creates, and the emails the app sends along the way.

## Where to find it

**Sidebar → Orders → Withdraw from contract** (`orders.aftercare.list`, `/admin/orders/aftercare`) — a list filterable by status (newest first), plus a per-request detail view. It is the third tab, **Withdraw from contract**, after **Overview** and **Settings** ([[aftercare-settings-setup]]), under a header showing the app's name („Отказ от договора“, with " (Free)" without Pro). The menu entry and the tab use the admin's translated label for "Withdraw from contract"; a code note gives it as „Оттегляне от договор“ (verify). The menu entry shows only while the app is installed and to staff with access to orders and to the app.

## What the merchant can do here

- Review each incoming withdrawal request (customer, order, items, refund total, terms snapshot).
- Advance its status (`pending → returned / cancelled`), optionally emailing the customer a note.
- Record the refund (method + reference) and, on Pro, let it flow into a core order-return.

## Settings & fields

Each request shows the customer (name / email), the order it references, the withdrawn items, the frozen refund total, the accepted terms snapshot ([[aftercare-compliance]]), and the event log.

## Business rules

### The box on the order page

The order page's right sidebar has a box titled with the app's title, directly above **Returns & exchanges** ([[orders-details-returns]]). It shows when the app is installed and the order has a request that is not cancelled, including a withdrawal on an unpaid, unshipped order that has no return. Each row: the request reference, opening `/admin/orders/aftercare/{id}` in a new tab; **Whole order** / **Цялата поръчка** or **Selected products** / **Избрани продукти**; a pending or returned badge; date and time. Oldest first. An orange left border marks the box while any request is pending. It reloads with the Returns box.

### Lifecycle — `pending → returned / cancelled`

Each request carries a status the merchant advances: **`pending` → `returned` / `cancelled`** — the same three-state set as a core order return. `pending` is new; the merchant sets `returned` once processed, or `cancelled` to close it without a return. A status change can **email the customer** (`notify_customer`) together with a free-text **note** (`status_note`, e.g. the reason). Each change is recorded as an **event** on the request.

On **Pro** with `auto_create_return`, a **linked core order-return becomes the source of truth** for the status: the selector here is **locked** and a direct change is rejected — the return propagates `returned` / `cancelled` back instead. See [[aftercare-order-return-sync]].

### Resolution type + refund method

Two fields describe what the customer asked for:

- **Resolution type** — **`withdrawal`** (returning part of the order). On Pro, a whole, **not-yet-shipped** order selected in full is recorded as **`cancel`** instead. (The **`exchange`** and **`voucher`** resolutions exist in the data model but are not yet operational — see [[aftercare-free-vs-pro]].)
- **Refund method** — Pro only: **`bank`** (the customer supplies name + IBAN / BIC for a manual transfer) or, when the order was paid by an online **card** gateway that supports the refund for that scope, **`card`**, recorded for the merchant to execute (the automated gateway refund is not yet wired). The free tier collects no refund method. Refunding to the [[virtual-wallet|Virtual Wallet]] is done on the core return ([[orders-returns-refunds]]).

### Refund amount + credit note

A **partial** withdrawal (some lines) freezes a **refund total** per item — **goods only** (shipping and COD excluded), after the apportioned cart discount, VAT-inclusive — so the amount is fixed at request time; a **whole-order** withdrawal is a full return whose amount (**goods + shipping + fees**) is read from the order at display time.

Resolving a request does **not** itself issue a credit note: the app records the refund (amount, method, reference) and, on Pro, mirrors the withdrawal into a PENDING core order-return (`auto_create_return`); the merchant issues any credit note through the normal order / return flow, and the request links it via `credit_note_id`.

### Emails the app sends

Installing the app **seeds editable, per-language email templates**; it sends:

| Email | To | When | Template / label |
|---|---|---|---|
| **Verification code** | customer | on submitting the statement (only when the order matches), and on **resend** | the store's customer two-factor code email (`cc2fa_email`), carrying the 6-digit code and the line „Използвайте този код, за да потвърдите заявлението си за отказ.“ |
| **Acknowledgement of receipt** | customer | on confirmation | `aftercare_withdrawal_acknowledgement` — the Art. 11a durable-medium acknowledgement |
| **Status update** | customer | when the merchant moves the request to **returned / cancelled** *and* keeps **"Notify customer"** on | `aftercare_status_returned` / `aftercare_status_cancelled` |
| **New withdrawal received** | merchant (store email) | on each newly confirmed request | `aftercare_withdrawal_received`: order number, customer name and email, time, *Requested items* (item × quantity, listed only for a partial request, so empty on Free) and a *View order* link; not the customer's note (shown on the request as *Customer's note*) |

**When the code email does not go out.** It is not an app template: it is the store's customer email „Двуфакторно удостоверяване в CloudCart с код“ ("CloudCart two-factor authentication with a code", subject „<store> - Код за удостоверяване“ by default) in [[marketing-omnichannel-mails-list]], edited there and shared with the checkout login code ([[checkout-code-popup]]). Switched off there (its **Active** switch is not locked) or missing from the list, it sends nothing while the storefront still answers neutrally (verify on a store). The store-wide "Send notifications to customers" switch does not stop it; the locked `notify_email` covers only the app's own emails. It goes from the store's name and email through CloudCart's sending service for codes, never the store's [[apps-smtp|SMTP app]]. Each code sent appears in the request's event log.

The seeded templates are **editable in the store's email-template builder**: the customer ones live with the transactional [[settings-emails|customer emails]] (one Unlayer design per language); the merchant alert is an [[settings-admin-notifications|admin notification]]. The just-submitted / `pending` state has **no** status email — the acknowledgement already covers creation — and a status email is **skipped** when the merchant turns "Notify customer" off for that change.

## Related

- [[apps-aftercare]] — hub.
- [[storefront-withdrawal]] — the customer flow that creates the requests.
- [[aftercare-compliance]] — the terms snapshot + audit trail attached to each request.
- [[aftercare-free-vs-pro]] — which resolution / refund options and controls (`block_resubmit`, card refund) need Pro.
- [[settings-emails]] / [[settings-admin-notifications]] — where the seeded templates are edited.
- [[orders-details]] — the order + any credit note.
- [[marketing-omnichannel-mails-list]] — where the two-factor code email is edited and switched on or off.

## Open questions

None.
