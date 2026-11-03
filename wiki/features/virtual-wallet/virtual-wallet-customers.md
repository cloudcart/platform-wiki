---
type: feature
nav_path: "Products → Virtual Wallet → Customers"
route_name: orders.wallet.customers
route_path: /admin/wallet/customers
aliases: ["Wallet customers", "Customer wallet balance", "Add wallet credit", "Deduct wallet credit", "Add transaction", "Wallet export", "Export wallet customers", "Ръчно добавяне в портфейл", "Баланс на клиент в портфейла", "Експорт на портфейли"]
tags: [wallet, store-credit, customers, export]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — Customers tab and the profile tab

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

Two screens show wallets per customer. The **Customers tab** lists everyone who ever had a credit, with their totals. The **Wallet tab on a customer's profile** shows one customer's credits, and is the only place to add or deduct credit by hand.

## Where to find it

- **Customers tab:** sidebar → Products → **Virtual Wallet** → **Customers**, at `/admin/wallet/customers`.
- **Profile tab:** sidebar → Customers → open a customer → **Wallet**, at `/admin/customers/details/:id/wallet`, route `customers-wallet`.

## What the merchant can do here

- See each customer's total credited, spent, current balance and funds expiring soon.
- Filter on the amounts, and search.
- Export the list.
- Open a customer from a row.
- On the profile tab: read that customer's credits, approve, reject or delete them, and add or deduct credit.

## Settings & fields

### Customers tab columns

| Column | Shows |
|---|---|
| **Customer** | Links to the profile |
| **Email** | The customer's email |
| **Ever had** | All approved credit ever received |
| **Spent** | What left the wallet |
| **Current balance** | **Ever had** minus **Spent** |
| **Expiring soon** | Amount and nearest date. Tooltip: *"Unspent funds expiring within the next 30 days"* |

The list holds customers who ever had a credit, with the biggest balance first.

**Filters** on **Ever had**, **Spent** and **Current balance**: At least, At most, Greater than, Less than, Exactly, Not. A search box covers the list.

### Export

**Export** goes through the two-factor confirmation and honours the applied filters. A small set downloads at once. A large set is queued and lands in Downloads. It uses the same permissions as the customers export (`customers`, `customers.all`, `customers.export`).

### Profile tab

The tab shows **Wallet balance**, **Expiring soon**, and the [[virtual-wallet-transactions|transactions table]] without the Customer column, with the same row actions.

**Add transaction** opens a modal:

| Field | Rules |
|---|---|
| **Amount** | Required, not 0. *"Positive to add, negative to deduct"* |
| **Expiry date** | With time. *"Optional — leave empty for no expiry"*. Ignored for a deduction |
| **Message** | Required, max 512. Placeholder *"Reason for the adjustment"* |

## Business rules

- **A manual credit counts at once.** It is saved with type Manual and status Approved.
- **A deduction cannot exceed the balance.** The refusal reads *"The amount exceeds the wallet balance."*
- **No email for a manual change.** The customer sees it in their activity on [[customer-wallet]].
- **A manual credit can be deleted** while nothing of it is spent; see [[virtual-wallet-transactions]].
- **The tab shows for every customer outside the Guests group**, even if the store never set up top-ups. For a customer in that group, adding credit is refused with *"The customer is a guest and has no wallet."*

### In the customers area

The [[customers-list-view|customers list]] has a **Wallet balance** column. The customer's page also shows the balance in its [[customer-details-identity-card|Insights]] card.

## Related

- [[virtual-wallet]] — hub.
- [[virtual-wallet-transactions]] — the table and its row actions.
- [[customer-details-tab-strip]] — the profile's tabs.
- [[customers-list-view]] — the list column.
- [[virtual-wallet-expiry]] — what "expiring soon" counts.

## Open questions

None.
