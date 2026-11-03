---
type: feature
nav_path: "Products → Virtual Wallet → Settings → Refunded-funds expiry"
route_name: ""
route_path: ""
aliases: ["Wallet expiry", "Wallet funds expiring", "Store credit expiry", "Do wallet funds expire", "Изтичане на средства в портфейла", "Срок на портфейла", "Изтичащи средства"]
tags: [wallet, store-credit, expiry]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — expiry

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

Which wallet credits expire, how the date is set, what happens at that moment, and when the customer is reminded.

## Where to find it

- Refunded credit: **Refunded-funds expiry** on [[virtual-wallet-settings]].
- API credit: **Default validity for third-party credits** on [[virtual-wallet-settings]].
- Manual credit: **Expiry date** in **Add transaction** on the customer's profile ([[virtual-wallet-customers]]).
- Dates: the **Expires** column on [[virtual-wallet-transactions]], and **Expires** on the customer's [[customer-wallet]] page.

## What the merchant can do here

- Set how many days refunded credit stays valid.
- Give a manual credit an exact date and time, including a short-lived one.
- See and filter credits by expiry on [[virtual-wallet-transactions]].
- See customers with funds expiring soon on [[virtual-wallet-customers]] and [[customers-list-view]].

## Settings & fields

| Credit | Expiry | Set by |
|---|---|---|
| Top-up | Never | Fixed. There is no setting |
| Redeemed gift card | Never | Fixed. The card's validity only limits when it can be redeemed ([[apps-gift-card-settings]]) |
| Refund | The set number of days from the refund date. 0 means never | **Refunded-funds expiry** |
| Manual | Optional exact date and time | **Add transaction** |
| Third-party API | The caller's date, otherwise the merchant's default | [[virtual-wallet-api]] |

## Business rules

### At the moment of expiry

Expired unspent funds leave the balance and cannot be spent at that exact moment, even before the write-off runs.

- A partly spent credit loses only its unused part.
- Funds reserved on a live order are not written off.
- Money returned from a cancelled order to a credit that has expired stays out of the balance ([[virtual-wallet-order-lifecycle]]).

### The write-off

A background task writes off lapsed funds every 4 hours. A credit expiring within the next 4 hours gets its own timed task, so a short-lived credit is written off right after it lapses. The merchant does not need to do anything. The customer's balance is already correct before the task runs.

### The reminder email

A daily task at 08:00 sends the email `wallet_expiring`:

- It covers unspent credits expiring within 30 days.
- Each credit triggers a reminder only once.
- A customer receives one email per run, summarising the amount at stake and the nearest date. A new credit entering the 30-day window later brings one more.
- It sends only if the store has the template active and customer email notifications are on. Until then, credits are not marked as reminded, so the reminder goes out once the template can send.

The email is on [[virtual-wallet-emails]].

### What "expiring soon" means

The same 30-day window drives the banner on [[customer-wallet]] and the **Expiring soon** figures in the admin.

### What the customer sees

On [[customer-wallet]], a row is red when it expired with unused funds, and yellow when it is expiring soon. `∞` marks a credit that never expires.

### Spending order

The soonest-to-expire credit is spent first, so a customer loses as little as possible to expiry. See [[virtual-wallet-checkout]].

## Related

- [[virtual-wallet]] — hub.
- [[virtual-wallet-settings]] — the two expiry settings.
- [[virtual-wallet-emails]] — the reminder email.
- [[customer-wallet]] — how the customer sees expiry.

## Open questions

None.
