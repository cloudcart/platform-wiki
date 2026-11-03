---
type: feature
nav_path: "Orders → Virtual Wallet transactions"
route_name: orders.wallet.transactions
route_path: /admin/wallet/transactions
aliases: ["Wallet transactions", "Virtual Wallet transactions", "Pending wallet transactions", "Approve wallet credit", "Reject wallet credit", "Транзакции на виртуалния портфейл", "Транзакции на портфейла", "Одобряване на кредит в портфейл"]
tags: [wallet, store-credit, orders, approvals]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — Transactions tab

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

The Transactions tab lists every wallet credit in the store, newest first. It answers where a balance came from, which order used it, and which API credits are waiting for approval. The same table, without the Customer column, is on the customer's profile ([[virtual-wallet-customers]]).

## Where to find it

Sidebar → Orders → **Virtual Wallet transactions** (`Транзакции на виртуалния портфейл`), at `/admin/wallet/transactions`. It is also the second tab of the wallet page at `/admin/wallet`.

The dashboard box **Pending wallet transactions** opens this list filtered to Pending. See below.

## What the merchant can do here

- Search and filter credits.
- See which order or orders used a credit.
- Approve or reject a Pending credit.
- Delete a credit an admin added by hand, while it is unspent.
- Read a credit's message and note from the hover icons in the Actions column.

Adding or deducting credit is done on the customer's profile, with **Add transaction**. See [[virtual-wallet-customers]].

## Settings & fields

### Columns

| Column | Shows |
|---|---|
| **Reference** | The credit's number |
| **Customer** | Links to the profile. Global list only |
| **Type** | Top-up, Refund, Gift, Manual, Bonus, Points |
| **Source** | Paid (real money), Bonus, Third party, or the admin's name for a credit an admin added |
| **Status** | Approved, Pending, Rejected, Expired |
| **Amount** | The credit's full amount |
| **Used in order** | The orders that spent it. One credit can list several |
| **Expires** | The date, marked `expired` when past. `∞` means never |
| **Created on** | Date and time |
| **Actions** | Approve, Reject, Delete, and the message and note icons |

### Filters and search

| Filter | Operators or values |
|---|---|
| **Type**, **Status**, **Source** | Is / Is not |
| **Expires** | Between, Exactly, Before, After |
| **Never expires** | Yes / No |
| **Used in order** | Yes / No |

The search box covers the credit number, order number, message, reference, and the customer's name or email.

### Row actions

| Action | Offered on | What it asks | Result |
|---|---|---|---|
| **Approve** | Pending credits | *"Approve this transaction?"* | Status Approved. It starts counting in the balance |
| **Reject** | Pending credits | Modal **Reject transaction** with a mandatory **Reason for rejection**, max 512 | Status Rejected. It never counts. The reason is kept as the note and shown to the customer |
| **Delete** | Credits an admin added by hand, with nothing spent | *"Delete this transaction?"* | The record is removed |

Refusal messages: *"Only pending transactions can be approved or rejected."* and *"Only manually added, unspent transactions can be deleted."*

## Business rules

- **What lands as Pending.** Only credits sent through the API, and only while **Auto-approve third-party credits** is off ([[virtual-wallet-settings]]). Top-ups, refunds, redeemed gift cards and manual credits are approved at once.
- **Pending and Rejected do not count.** The customer sees them in their activity, but cannot spend them ([[customer-wallet]]).
- **System credits stay.** Top-ups, refunds, gifts and API credits cannot be deleted. Reversing a top-up or a gift card goes through its order; see [[virtual-wallet-order-lifecycle]] and [[apps-gift-card-reversal]].
- **The Amount column does not shrink as a credit is spent.** The spent part is read from **Used in order**, and per customer from the Customers tab.

### Where the pending count shows

- The dashboard box **Pending wallet transactions**, hidden at 0 ([[dashboard]]).
- A count on the **Virtual Wallet transactions** sidebar link.
- The Orders badge in the sidebar, whose total includes this count.

## Related

- [[virtual-wallet]] — hub.
- [[virtual-wallet-customers]] — the per-customer view and **Add transaction**.
- [[virtual-wallet-api]] — the API credits that arrive as Pending.
- [[dashboard]] — the pending box.
- [[orders-details]] — the orders listed under **Used in order**.

## Open questions

None.
