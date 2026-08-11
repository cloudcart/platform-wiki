---
type: feature
nav_path: "Orders → open an order → Returns / Issue return"
route_name: admin.core.orders.returns
route_path: ""
aliases: ["Order return", "Order returns", "Issue return", "Return goods", "Full return", "Partial return", "Return refund", "Returned status", "Върната поръчка", "Връщане на стока", "Издай връщане", "Частично връщане", "Пълно връщане", "order return lifecycle", "return status", "return"]
tags: [orders, returns, refund, credit-note, restock, compliance]
plan_gates: []
created: 2026-07-24
updated: 2026-07-24
source_count: 1
---

# Order returns (Issue return)

## Purpose

An **order return** is the merchant-side record of goods (or value) coming back on a placed order — the core mechanism behind refunds, restock, and credit notes (fiscal basis: **Наредба Н-18 / §18**). A return can be a **full** reversal of the whole order or a **partial** one covering selected lines, and it moves the returned quantities back into stock, gives the customer their money back through a chosen method, and issues the fiscal credit note.

> Do **not** confuse this with [[checkout-return]] — that is the *payment-gateway* return (the page a customer lands on after an off-site payment), an unrelated mechanism that happens to share the word "return".

Returns are created three ways: the merchant clicks **Issue return** on an order; the [[apps-aftercare|Withdraw-from-contract]] app mirrors a customer withdrawal into a return (see [[aftercare-order-return-sync]]); or the return is raised as part of a refund. This is a navigation hub; each aspect is on its own page.

## Where to find it

Returns are worked **on the order** — open an order from [[orders-details]] and use its **Returns** panel / **Issue return** action. The API lives under `/api/.../returns` (`admin.core.orders.returns`, permission `orders.returns`); it is a **core** feature, not app-gated.

## Sub-pages (in this cluster)

- [[orders-returns-lifecycle]] — the states (`pending → returned / cancelled`), full vs partial, how a return is created, and the two rules that trip people up: **a partial credit note locks the order out of a full reversal**, and a partial refund leaves the order status untouched.
- [[orders-returns-refunds]] — how the money goes back: the refund methods (`card` / `bank` / `voucher` / `wallet` / `exchange` / `none`), the platform-side **card refund** (full and partial, per provider), and how it relates to the standalone [[orders-payment-refund|Refund payment]] button.

## What the merchant can do here

- **Issue** a full or partial return against an order.
- **Receive** it (`pending → returned`) — restocking the goods, issuing the credit note, and notifying the customer.
- **Refund** the customer by card (via the gateway), bank transfer, voucher, or record it as handled manually — see [[orders-returns-refunds]].
- **Issue the credit note** and **cancel** a still-pending return.

## Settings & fields

There are no return-specific settings — a return is created and worked **per order**. The fields that shape a return (its type, source, refund method, frozen totals) are documented on [[orders-returns-lifecycle]] and [[orders-returns-refunds]]; the credit-note / invoicing settings it relies on live on [[orders-credit]] and [[settings-invoicing]].

## Business rules

- **Status set:** `pending` (raised, awaiting processing — cancellable, no restock/credit note yet) → `returned` (received / processed → restocked) or `cancelled` (reversed, only from `pending`). Detailed on [[orders-returns-lifecycle]].
- **Full vs partial:** a full return is header-only (the whole order, read live); a partial return itemises and freezes the selected lines' totals.
- **The credit note is the fiscal commit** — created when the return is received, and once a **partial** one exists the order can no longer be reversed as a whole. See [[orders-returns-lifecycle]].
- **Refund side-effect asymmetry:** a **full** card refund flips the order to `refunded` (and auto-restocks via PaymentSync); a **partial** refund leaves the order status unchanged (it re-computes the customer's spend for income / segments). See [[orders-returns-refunds]].
- **Connection to the order:** the order gates **Issue return** behind `allow_return` (committed / invoiced, not already fully returned or reversed) and carries a derived **`return_status`** (`null` / `partial` / `full`) that reflects returns **without** overwriting its real [[order-status-workflow|status]]. Each return also keeps its own audit log. See [[orders-returns-lifecycle]].

## Related

- [[orders-details]] — the order the return is issued against; the Returns panel lives here.
- [[orders-returns-lifecycle]] / [[orders-returns-refunds]] — this cluster's aspects.
- [[orders]] — the Orders hub / list.
- [[order]] — the order entity (`return_status`, `allow_return`).
- [[order-status-workflow]] — how a full return / refund moves the order into a negative status.
- [[order-processing-pipeline]] — where a return sits among the order's lifecycle side-effects.
- [[orders-history]] — the order-level history (the return also keeps its own log).
- [[orders-payment-refund]] — the standalone full-only Refund button (a different surface).
- [[orders-payment-refund-partial-refunds]] — how partial refunds work across the two surfaces.
- [[orders-credit]] — the credit note a return issues.
- [[apps-aftercare]] / [[aftercare-order-return-sync]] — EU withdrawals feed into this return flow.
- [[inventory-tracking]] — the restock a received return performs.
- [[checkout-return]] — the unrelated payment-gateway return page (name collision only).

## Open questions

None.
