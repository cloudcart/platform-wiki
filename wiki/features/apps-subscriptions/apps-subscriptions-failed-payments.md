---
type: feature
nav_path: "Apps → Subscriptions → Settings → Failed payments"
route_name: apps.subscriptions.settings
route_path: /admin/apps/subscriptions/settings
aliases: ["subscription payment failed", "past due subscription", "declined card subscription", "subscription retry", "subscription cancelled automatically", "неуспешно плащане абонамент", "отказана карта абонамент", "автоматично прекратен абонамент"]
tags: [apps, subscriptions, dunning, failed-payments, retry]
plan_gates: ["subscriptions"]
created: 2026-08-28
updated: 2026-08-28
source_count: 5
---

> Part of [[apps-subscriptions]]. See the hub for the other aspects (setup, plans, billing cycle, customer controls, managing).

# Subscriptions — when a payment fails

## Purpose

A declined card does not end a subscription. The platform keeps the contract alive, retries on a widening schedule, and only gives up when the attempts run out. This aspect covers that ladder, the state the contract sits in meanwhile, and the separate case of a failure that is the **store's** fault rather than the card's.

## Where to find it

**Apps → Subscriptions → Settings** → the **Failed payments** section. What happened to an individual contract is on its detail view ([[apps-subscriptions-managing]]).

## What the merchant can do here

- Set how many failed attempts a subscription survives.
- Choose to be notified about every failed payment.

## Settings & fields

| Field | What it does |
|---|---|
| **Attempts before the subscription is cancelled** (`max_failed_attempts`) | How many declines the contract survives. On the last one it is cancelled. |
| **Notify me about every failed payment** (`notify_merchant_failed`) | Sends the merchant an alert on each failure, not only the final one. |
| **Tell the customer about a failed payment** (`notify_customer_failed`) | Whether the customer is e-mailed — see the rule about *when* below. |

## Business rules

### The contract goes past due, not cancelled

On a decline the subscription moves to **`past_due`** and **keeps its subscription** while the bank is retried. It is still a live contract: it stays in the billable set, its schedule is intact, and a later successful charge returns it to `active` with the failure counter cleared.

This is the answer to *"my customer's card bounced, have they lost their subscription?"* — not yet, and not for several days.

### 🔴 Retries are spaced further apart each time

The gap after each failed attempt widens, so a temporary problem — a card topped up, a limit reset — has progressively more time to resolve:

| After failure | Next attempt |
|---|---|
| 1st | 2 days later |
| 2nd | 3 days later |
| 3rd | 4 days later |
| 4th | 5 days later |
| 5th | 5 days later |

A subscription therefore survives roughly **two to three weeks** of a failing card before the ladder is exhausted, depending on where the merchant set the attempt limit. Nothing is charged in between; the contract simply is not due until the next step.

### Only the final attempt cancels

When the attempts run out, the subscription is **cancelled** with the reason recorded as a payment failure, and its due dates are cleared so it leaves the schedule for good. Everything before that is a retry, not an ending.

### The customer is e-mailed once, not on every retry

The failure e-mail goes out on the **first** failure only. The retries are days apart, and an e-mail on each one reads as pestering rather than helping — one clear message asking the customer to update their card serves better than five.

The merchant's own alert is separate and can be set to fire on every attempt, since the merchant is watching a business rather than being nagged.

### 🔴 A failure the store caused does not count against the customer

There are two quite different reasons a renewal can fail, and the platform treats them differently:

| What failed | Counted as a payment failure? |
|---|---|
| The **card** was declined | Yes — advances the ladder above. |
| The **order could not be built** — a product gone, unavailable, or otherwise unorderable | **No.** |

The second is not a payment problem: the card is fine, the store is not. Counting it would burn the customer's attempts and could cancel a subscription over a merchant-side problem. Instead the cycle gets **one grace attempt** — the first such failure marks the cycle and leaves it on the schedule, and only a repeat gives up on that cycle. The audit trail records whether another attempt is expected.

Only the merchant can fix this class of failure. A contract that stops renewing with no card problem is usually here — check that the subscribed product is still active and orderable ([[product-visibility]]) rather than looking at the payment method.

### Recovery is complete, not partial

A successful charge after failures clears the counter **and** the record of the last attempt, so the contract stops advertising a failure in the admin once it has recovered. A subscription showing a past failure is one that has not yet succeeded since.

## Related

- [[apps-subscriptions]] — hub.
- [[apps-subscriptions-billing-cycle]] — the normal path this branches off.
- [[apps-subscriptions-managing]] — where a contract's failure history is read, and the manual **Charge now**.
- [[apps-subscriptions-customer-controls]] — what the customer can do about their own card.
- [[product-visibility]] — the usual cause of a build-stage failure.

## Open questions

- Whether the customer is told when their subscription is finally cancelled for non-payment, or whether the first-failure e-mail is the only message they receive.
