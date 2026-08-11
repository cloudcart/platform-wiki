---
type: feature
nav_path: "Orders → open an order → Returns → Lifecycle"
route_name: admin.core.orders.returns
route_path: ""
aliases: ["Return lifecycle", "Return states", "Return status", "pending returned cancelled return", "Issue return flow", "full vs partial return", "credit note locks full", "return source", "receive return", "cancel return"]
tags: [orders, returns, lifecycle, status, credit-note]
plan_gates: []
created: 2026-07-24
updated: 2026-08-06
source_count: 1
---

> Part of [[orders-returns]]. See the hub for the other aspect (refund methods).

# Order returns — lifecycle & states

## Purpose

How a return is created, the states it moves through, and the two rules that most often surprise merchants: receiving a return restocks the goods but does **not** issue the credit note (that is a separate manual step), and a **partial** credit note locks the order out of a later **full** reversal.

## Where to find it

On the order — open it from [[orders-details]] and use its **Returns** panel. The state and every transition are recorded on the return's own history log.

## What the merchant can do here

- **Issue** a return (full or partial), **receive** it, or **cancel** it while still pending.
- Read the return's state and history from the order.

## Settings & fields

### Types

| Type | What it covers |
|---|---|
| **`full`** | The whole order — header-only (no frozen line items); the amount is read live from the order (goods + shipping + fees), exactly like a full reversal. |
| **`partial`** | Selected lines only — the return **freezes** those lines' totals (goods, apportioned cart-rule discount, tax) at creation, so the refund amount is fixed. |

### Sources

A return records **where it came from**: `manual` (the merchant's **Issue return** action), `withdrawal` (mirrored from an [[apps-aftercare|EU withdrawal]] — see [[aftercare-order-return-sync]]), or **`refund`** — a return the platform creates **automatically** (see below).

### 🔴 Cancelling / refunding a COMMITTED order auto-creates a return

Moving an order to **`cancelled` or `refunded`** — and only those two of the seven negative statuses — does not only flip the status: when the order was a **committed sale**, the platform **automatically records a system return** for it — created straight as **`returned`**, with `source = refund` and `created_by = system`, covering the whole (or the remaining) quantity. The other negative statuses (`voided`, `timeouted`, `failed`, `chargebacked`, `disputed`) do **not** record a return.

- **"Committed"** means the order was already invoiced, or its pre-flip status was a positive / committed one (e.g. `paid`) — the same notion as the [[orders-returns|Issue-return]] gate. A plain cancel of a never-committed order (e.g. an unpaid, uninvoiced `pending` one) is **not** recorded as a return.
- It is **idempotent** — flipping the status back and forth does not pile up returns — and it settles the restock netting so already-returned units are not restocked twice.
- **A credit note is NOT required** for this to happen — the return record is created by the reversal itself.

**Merchant-visible consequence:** these auto-created returns are real return records — they are listed under the order and behave like any other return — but they are **not counted in return reporting**. Return analytics counts **partial returns only**; full returns and cancelled orders are excluded, because the reversal is already visible through the order's status and through the order leaving the sales figures. Counting it again on the returns side reported the same reversal twice, which is what previously inflated the *Returns over time*, *Net revenue* and *Return rate* boxes for merchants who cancel paid orders. See [[analytics-overview-returns-boxes]] — including the note that **past periods keep their old figures**, so a long date range can show a step change at the changeover.

## Business rules

### Statuses — `pending → returned / cancelled`

| Status | Meaning |
|---|---|
| **`pending`** | The return is raised and awaiting processing. Nothing has committed yet — no restock, no credit note — so it can still be **cancelled**. |
| **`returned`** | The goods were **received / processed**: the quantities are **restocked**, the return is complete, and the customer is notified. The **credit note is not issued here** — it is a separate manual action (see below). |
| **`cancelled`** | The return was reversed. Only reachable **from `pending`**, and **only before a credit note exists** — a reversing entry is written (the record is never hard-deleted), and the order's `return_status` is re-derived. |

### How a return is created

**Issue return** is available only for a **committed order** — one that is **invoiced** (or ready to be invoiced) and is not already fully returned or in a reversed / [[order-status-workflow|negative]] status (the order's `allow_return` gate). A not-yet-committed, directly-editable order is edited in place instead of through a return. The merchant then picks **full** or **partial** (selecting lines and quantities for a partial), and the form shows a **live totals preview** of what will be refunded before saving. The [[apps-aftercare|Withdraw-from-contract]] app creates the same kind of return automatically from a confirmed withdrawal ([[aftercare-order-return-sync]]).

### Receiving = goods back in stock. The credit note is a SEPARATE, manual step

Moving a `pending` return to **`returned`** (the **Receive** action) is the *"goods received"* step: it **restocks** the returned quantities ([[inventory-tracking]]), marks the return `returned`, and notifies the customer. A return that is not `pending` can no longer be received.

**It does NOT issue the credit note.** Issuing the credit note is a **deliberate, separate action** on the return — the fiscally-committing step the merchant triggers when they are ready. So a received return can sit `returned` with the goods back in stock and **no credit note yet**; the order is not fiscally credited until the merchant issues it. See [[orders-credit]].

### A partial credit note locks the order out of a full reversal

Once a **partial** return's **credit note** exists, the fiscal base for those lines is committed, so the order can **no longer be reversed as a whole** — every further return must be a **partial remainder**. The editor warns before issuing when this lock is about to apply (and only when something is still returnable). This mirrors the [[apps-aftercare|withdrawal]] rule that a full-order reversal is only possible on a clean order with no prior returns.

### The order's derived `return_status`

Separately from its real (payment-derived) status, the order carries a **derived `return_status`** flag — **`null`** (none), **`partial`** (some quantity returned), or **`full`** (every line fully returned) — re-derived from the order's **issued** returns whenever one changes. It is only an indicator; it **never overwrites** the order's actual status. (A full return *does* move the order into a reversed / [[order-status-workflow|negative]] status, but through its **refund**, not this flag — see [[orders-returns-refunds]].)

### Each return keeps its own history log

Every return has its **own** audit log — `created` (with type + refund method), `received`, `refunded`, `cancelled`, and `credit-note-issued` entries, each stamped with the actor — separate from the order-level [[orders-history]].

### Refund status is separate from the return status

A refund can happen independently of the `pending → returned` move, and its side-effects differ by scope — a **full** refund flips the order to `refunded`, a **partial** one does not. That is covered on [[orders-returns-refunds]].

## Related

- [[orders-returns]] — hub.
- [[orders-returns-refunds]] — the money side (methods + side-effects).
- [[orders-details]] — where the return is issued and its state shown.
- [[orders-credit]] — the credit note issued at receipt.
- [[inventory-tracking]] — the restock a received return performs.
- [[aftercare-order-return-sync]] — how an EU withdrawal becomes one of these returns.

## Open questions

None.
