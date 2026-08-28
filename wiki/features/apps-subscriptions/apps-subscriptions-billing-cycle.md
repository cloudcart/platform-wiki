---
type: feature
nav_path: "Apps → Subscriptions → how a renewal happens"
route_name: apps.subscriptions.details
route_path: /admin/apps/subscriptions/list/:id
aliases: ["subscription renewal", "how often is a subscription charged", "prepaid subscription", "subscription cycle", "subscription stock", "when is the next order created", "подновяване на абонамент", "предплатен абонамент", "цикъл на абонамент"]
tags: [apps, subscriptions, billing, renewal, inventory, background-jobs]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-08-28
source_count: 5
---

> Part of [[apps-subscriptions]]. See the hub for the other aspects (setup, plans, failed payments, customer controls, managing).

# Subscriptions — the billing cycle

## Purpose

What actually happens each time a subscription comes round: when the platform looks, what it charges, what order it raises, and when the stock moves. This is the aspect to read for *"when will the next order appear"* and *"why was my customer charged now"*.

## Where to find it

Nothing to configure — this is the machinery. Its results are visible per contract on the detail view ([[apps-subscriptions-managing]]) and as ordinary orders in [[orders]].

## What the merchant can do here

Read the schedule and understand it. The only manual intervention is the per-contract **Charge now**, and pausing or skipping — all on [[apps-subscriptions-managing]].

## Settings & fields

No fields of its own. What the cycle does is decided by the plan the contract was bought on — its two intervals and its stock policy, both on [[apps-subscriptions-plans]].

## Business rules

### The schedule is checked every hour

Contracts due are picked up **hourly**, not on a nightly pass, and due dates are compared **by date** — so a contract due today is charged within the hour rather than at some point after midnight. This is deliberate: a merchant watching a customer's first renewal go through should not have to wait a day to see it.

Each store bills its own contracts independently, so a busy store does not delay a quiet one.

### A cycle is one turn of the schedule

Every turn is recorded as a **cycle** with its own state:

| Cycle state | Meaning |
|---|---|
| **Scheduled** | Due, not yet processed. |
| **Paid** | Charged successfully; the order was raised. |
| **Delivered (prepaid)** | Sent out under a payment already taken on an earlier cycle — no charge of its own. |
| **Skipped** | Passed over, by the customer or the merchant. The schedule moves on without charging. |
| **Payment failed** | The charge did not go through — see [[apps-subscriptions-failed-payments]]. |

The cycle history is the answer to *"what happened on this subscription and when"*, and it is per contract rather than per order.

### 🔴 Prepaid cycles are deliveries, not sales

When a plan bills less often than it delivers ([[apps-subscriptions-plans]]), one payment covers several deliveries. The first cycle takes the money; the ones it covers are marked **Delivered (prepaid)** and produce their orders **without any charge at all**.

Two things follow that surprise merchants:

- A **prepaid delivery order carries no payment** of its own. Its money was taken on an earlier order. It is not an unpaid order to chase.
- **Revenue is not evenly spread.** A quarterly-billed, monthly-delivered subscription shows the full quarter's income in one month and nothing in the next two, while orders appear in all three.

### Stock is taken on one of two events

The plan's stock policy decides when the subscription's stock is consumed:

| Policy | Stock moves |
|---|---|
| **On sale** | When the payment is taken. |
| **On fulfilment** | When the parcel actually goes out. |

The distinction matters most for prepaid plans, where money and dispatch are months apart. Taking stock on sale reserves the whole prepaid run up front — the customer is guaranteed their goods, but the stock sits committed. Taking it on fulfilment keeps the stock available for longer, at the risk of a prepaid customer's later delivery meeting an empty shelf. See [[inventory-tracking]] for the underlying stock behaviour.

### A renewal produces an ordinary order

Nothing about the resulting order is special: it appears in [[orders]], follows the same status pipeline, is invoiced by the same rules, decrements stock through the same mechanism, and can be fulfilled, returned and refunded like any other. The only difference is who created it.

That is why a subscription needs no separate reporting surface — the money and the fulfilment are already in the ordinary order flow.

### Some charges have no immediate answer, so the platform asks again

Not every payment resolves at once. Because there is no notification when a charge later fails, an unresolved one is only ever discovered by **asking the payment method** — so a second pass runs **every two hours** to settle charges still in flight.

The visible consequence: a charge can sit unresolved for up to a couple of hours before its outcome shows. A subscription that looks stuck immediately after a renewal is usually mid-settlement rather than broken.

### A subscription with a maximum ends by itself

A plan with a maximum number of payments moves the contract to **expired** once it has been charged that many times. This is a normal ending, not a cancellation and not a failure — the customer completed what they agreed to.

## Related

- [[apps-subscriptions]] — hub.
- [[apps-subscriptions-plans]] — the two intervals that produce this schedule, and the stock policy.
- [[apps-subscriptions-failed-payments]] — the branch taken when a charge is declined.
- [[apps-subscriptions-managing]] — where the cycle history is read.
- [[orders]] — where every renewal order lands.
- [[inventory-tracking]] — the stock mechanics behind the two policies.
- [[background-queue-inventory]] — the platform's background processing generally.

## Open questions

- Whether a prepaid run's remaining deliveries are still sent when the customer cancels mid-run, or whether cancellation stops them despite having been paid for.
