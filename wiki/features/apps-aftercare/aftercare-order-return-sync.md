---
type: feature
nav_path: "Apps → Withdraw from contract → Order-return sync (Pro)"
route_name: ""
route_path: ""
aliases: ["Aftercare order return sync", "auto_create_return", "withdrawal core return", "withdrawal return mirror", "status managed by return", "withdrawal refund execution", "withdrawal restock", "withdrawal source return"]
tags: [apps, aftercare, orders, returns, withdrawal, pro]
plan_gates: ["aftercare_pro"]
created: 2026-07-24
updated: 2026-07-24
source_count: 1
---

> Part of [[apps-aftercare]]. See the hub for the other aspects (compliance, admin inbox, settings, free-vs-Pro, storefront flow).

# Aftercare — order-return sync (Pro)

## Purpose

On **Pro**, with `auto_create_return` on (its default), a confirmed withdrawal does not just sit in the Aftercare inbox — it is **mirrored into a real core [[orders-returns|order-return]]**, and from then on the **core return, not the Aftercare request, drives the workflow**. This page describes that integration precisely: what the mirror creates, how the status becomes single-sourced, and how the refund and restock are executed. On the **free** tier none of this happens — the merchant works the withdrawal entirely inside the Aftercare inbox ([[aftercare-withdrawals-admin]]) and handles the refund off-platform.

## Where to find it

The mirrored return is worked in the store's normal returns handling on the order ([[orders-details]]); the Aftercare request shows a link to it and locks its own status while the link exists. The `auto_create_return` toggle lives on [[aftercare-settings-setup]].

## What the merchant can do here

Work the withdrawal exactly like any other return — approve, restock, and refund from the **core return** on the order — and let the Aftercare request follow automatically. There is nothing extra to reconcile between the two.

## Settings & fields

Driven by `auto_create_return` (Pro, on by default — see [[aftercare-settings-setup]]). No other settings.

## Business rules

### What the mirror creates

When a withdrawal is confirmed, and **only** for a **committed order** (`allow_return` — the same gate as the manual *Issue return* button; a not-yet-invoiced order is skipped) and **never twice** for the same request, the app creates a **PENDING** core order-return:

- A **whole-order** (`cancel`) withdrawal → a **header-only** return (no line items or frozen totals) whose grand total is the entire order (goods + shipping + fees), exactly like a core full return.
- A **partial** withdrawal → a return carrying its **frozen selected lines** (`order_product_id → quantity`).

The return is tagged with **source = withdrawal** and carries the request id, the customer's **reason** (their optional note), and their **refund choice** (method + bank name / IBAN / BIC) — so the merchant never re-enters any of it.

### The core return is the single source of truth for the status

Once a return is linked, the Aftercare request's **status selector is locked**, and a direct status change on the request is rejected (validation message *"status managed by return"*). Instead:

- The merchant advances the **core return** through its own lifecycle (approve → restock → refund).
- When the return reaches **`returned`** or **`cancelled`**, that status is **propagated back** to the Aftercare request automatically, so the two always agree.

The sync is **one-way** (return → withdrawal) and has **no loop** — the propagated status change does not re-fire the return events that triggered it.

### Refund + restock happen on the core return

The withdrawal record itself does **not** restock inventory or move money — those are the core return's job (which is exactly why mirroring it into a return is the Pro value). The customer's refund choice rides along:

- **`bank`** — a **manual** payout by the merchant, from the carried name / IBAN / BIC.
- **`card`** — a refund back to the original gateway, **executed from the core return's "refund to card" button** via the provider's API: a **full** return issues a **full refund**, a **partial** return issues a **partial refund**. This works for providers that support the matching capability — **partial refunds are live for Stripe, PayPal, Revolut, and CloudCart Pay** (Mollie / PayU / Mokka / Klear and others are full-only or unsupported). Card is therefore offered **per scope**: on a partial withdrawal the `card` option only appears when the gateway supports partial refunds; otherwise the customer is steered to `bank`. See [[orders-payment-refund-partial-refunds]].

Any credit note is issued through the normal order / return flow ([[orders-credit]]); the Aftercare request links it via `credit_note_id`.

## Related

- [[apps-aftercare]] — hub.
- [[orders-returns]] — the core order-return process the mirror feeds into (states, refund, credit note).
- [[aftercare-withdrawals-admin]] — the request whose status the return drives (and where the lock is enforced).
- [[aftercare-free-vs-pro]] — the Pro tier this belongs to; the deferred refund automations.
- [[aftercare-settings-setup]] — the `auto_create_return` toggle.
- [[orders-details]] — where the mirrored core return is worked.
- [[orders-payment-refund]] — executing the card / bank refund.
- [[orders-credit]] — the credit-note flow the return feeds.

## Open questions

None.
