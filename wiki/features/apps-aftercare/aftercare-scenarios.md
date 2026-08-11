---
type: feature
nav_path: "Apps → Withdraw from contract → Scenarios"
route_name: ""
route_path: ""
aliases: ["Aftercare scenarios", "Aftercare cases", "withdrawal scenarios", "withdrawal action sequence", "withdrawal worked examples", "aftercare return cases", "aftercare prerequisites", "aftercare dependencies", "aftercare what it does not do"]
tags: [apps, aftercare, orders, returns, withdrawal, scenarios]
plan_gates: []
created: 2026-07-31
updated: 2026-07-31
source_count: 1
---

> Part of [[apps-aftercare]]. See the hub for the other aspects (compliance, admin inbox, settings, free-vs-Pro, order-return sync, storefront flow).

# Aftercare — return cases & action sequences

## Purpose

The concrete end-to-end **cases** and **action sequences** that show how the [[apps-aftercare|Withdraw-from-contract]] app behaves in practice — the prerequisites, the customer's steps, the merchant's steps, and what changes per situation. Read the aspect pages for the mechanics; read this for "what actually happens".

## Where to find it

These sequences play out across the storefront flow ([[storefront-withdrawal]]) and the admin inbox ([[aftercare-withdrawals-admin]]). Nothing new to click here.

## What the merchant can do here

Use these cases to predict the flow before configuring, and to recognise which case a live request is in.

## Settings & fields

No settings — this page catalogues behaviour. The settings are on [[aftercare-settings-setup]].

## Business rules

### Prerequisites — when a withdrawal can be raised

- The order must be in an **`allow_return`** state — the **same core gate** as issuing a return: **invoiced (or ready to invoice)**, not already fully returned, and not in a reversed / [[order-status-workflow|negative]] status. An order that is not yet committed cannot be withdrawn.
- The right to withdraw exists from contract conclusion (even **before delivery**); the 14-day **countdown** only starts on delivery (see [[aftercare-compliance]]).

### The standard customer sequence

1. **Open** the withdrawal form (floating button / menu link → `/withdrawal`, or the in-account shortcut on Pro).
2. **Identify** — enter order number + email (+ name).
3. **Verify** — a **time-limited code** is emailed; the customer enters it. **Max 5 attempts**, a **60-second cooldown** between resends, and **max 3 resends** per session (all held in session, never persisted; the neutral "code sent" reply prevents order/email enumeration — see [[storefront-withdrawal]]).
4. **Pick items** — only still-withdrawable lines (already-withdrawn lines are hidden; measured / bundle / options lines are all-or-nothing; the picker is bundle-aware).
5. **(Pro) Choose the refund method** — a screen offering `bank` (IBAN / BIC) or, when the paying gateway supports it, `card`.
6. **Confirm** — this creates the request (`pending`), freezes the per-line refund totals, stores the terms snapshot, emails the **acknowledgement**, and alerts the merchant. The customer lands on a **done** screen and can **track** it by its hash.

### Case 1 — Partial withdrawal, free tier

Customer withdraws 2 of 5 lines → a `pending` request with the two frozen lines and `resolution_type = withdrawal`, `refund_method = bank`. The merchant reviews it in the inbox, refunds the customer **manually** (bank transfer from the IBAN captured), moves the status to `returned` (or `cancelled` to decline), optionally emailing a note. On the free tier the merchant handles restock and the credit note through the normal order flow; the app does not do it automatically.

### Case 2 — Whole-order withdrawal before shipping

The customer selects the entire order and it has **not shipped** and has **no prior returns** → treated as a **full** reversal. On **Pro** this is recorded as `resolution_type = cancel`; on the free tier it is a full `withdrawal`. The amount is the whole order (goods + shipping + fees), read live.

### Case 3 — Pro with `auto_create_return`

On confirmation the app mirrors the withdrawal into a **PENDING core order-return** carrying the refund choice. From then the **core return drives everything** — the merchant approves / restocks / refunds it on the order, and its `returned` / `cancelled` status **propagates back** to the withdrawal (whose status selector is locked). Full detail on [[aftercare-order-return-sync]].

### Case 4 — Refund routing

- **`bank`** (any plan) — manual transfer from the captured name / IBAN / BIC.
- **`card`** (Pro) — refunded through the gateway from the core return, full or partial, for **Stripe / PayPal / Revolut / CloudCart Pay** (see [[orders-payment-refund-partial-refunds]]).
- **`voucher` / `exchange` / `wallet`** — declared but **not yet operational** (see [[aftercare-free-vs-pro]]).

### Case 5 — Window edge cases

- **Before delivery:** the withdrawal can still be raised; there is simply no countdown yet.
- **After the window:** the in-account live-countdown CTA (Pro) disappears (`expired`), but the standalone `/withdrawal` flow gates on `allow_return`, not on the window — so a late request can still reach the inbox and the merchant decides.

### Case 6 — Resubmission & prior returns

- After a request is **`cancelled`**, its lines are freed for a new request — **unless** `block_resubmit` (Pro) keeps them locked.
- An order that already has a **partial** return / credit note can only be withdrawn as a **partial remainder** — a full reversal is no longer possible.

### What Aftercare does NOT do

- **It does not arrange return shipping** — no return waybill / label / carrier booking. The physical return of the goods is handled by the merchant (or through the core return / courier separately).
- **It does not issue the credit note or restock by itself** on the free tier — those go through the normal order / return flow.
- **It does not enforce the statutory exemptions** — every returnable line is offered; the merchant applies exemptions when resolving (see [[aftercare-compliance]]).

## Related

- [[apps-aftercare]] — hub.
- [[storefront-withdrawal]] — the customer flow these sequences run through.
- [[aftercare-withdrawals-admin]] — the admin inbox where the merchant resolves each case.
- [[aftercare-order-return-sync]] — the Pro core-return path (Case 3).
- [[aftercare-free-vs-pro]] — which cases need Pro; the deferred refund types.
- [[aftercare-compliance]] — the window, exemptions, and the `allow_return` prerequisite context.
- [[orders-returns]] — the core return the Pro path drives.

## Open questions

None.
