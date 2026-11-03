---
type: feature
nav_path: "Products → Virtual Wallet → Settings → Third-party credits (API)"
route_name: ""
route_path: ""
aliases: ["Wallet API", "Wallet credit API", "wallet-credit", "creditCustomerWallet", "Loyalty integration wallet", "wallet_amount", "API за портфейла", "Кредитиране на портфейл през API"]
tags: [wallet, store-credit, api, json-api-v2, graphql, webhooks]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — API and webhooks

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

How an outside system, such as a loyalty integration, adds credit to a customer's wallet, which Admin GraphQL operations read and manage wallets, and what webhooks carry about the wallet.

## Where to find it

No admin screen of its own. The merchant's rules for these credits are under **Third-party credits** on [[virtual-wallet-settings]]. The credits appear on [[virtual-wallet-transactions]] with source `Third party`.

## What the merchant can do here

- Choose whether API credits wait for approval: **Auto-approve third-party credits**.
- Set the default validity: **Default validity for third-party credits**.
- Approve or reject the Pending credits on [[virtual-wallet-transactions]].

## Settings & fields

### Adding credit

REST: `POST /api/v2/customers/{id}/wallet-credit` ([[api-customers]]). The body can be flat or under `data.attributes`.

GraphQL: `creditCustomerWallet(customerId, amount, message, reference, expiredAt)` ([[admin-graphql-api]]).

| Field | Rules |
|---|---|
| `amount` | Integer in cents, required, min 1. Credit only: the API cannot deduct |
| `message` | Required, max 512. Shown in the customer's wallet history |
| `reference` | Optional, max 191. Your own reference for the credit |
| `expired_at` / `expiredAt` | Optional date, must be in the future |

REST returns 201, and errors are 422. GraphQL returns errors in its usual form.

### Admin GraphQL operations

Staff permissions apply on Admin GraphQL.

| Operation | Permission | Notes |
|---|---|---|
| `approveWalletTransaction` | `orders` | Pending credits only |
| `rejectWalletTransaction(id, note)` | `orders` | `note` required, max 512 |
| `deleteWalletTransaction` | `orders` | Credits added by hand, unspent |
| `customerWalletTransactions` | `orders` | Page size max 100. Filters `status`, `type` |
| `customerSections` | `customers` | `walletEnabled` is false for a guest. Also carries the balance |

### Webhook fields

The order payload ([[webhook-entity-events]]) carries:

- `wallet_amount` — the wallet money applied to the order, 0 when unused. `payment.amount` is already net of it.
- on each line, `type_digital` — `file`, `page`, `wallet`, `gift_card`, or null for a physical product.

## Business rules

### What an API credit becomes

Type `bonus`, source `third_party`, and status `pending` unless auto-approve is on. A Pending credit does not count in the balance until approved.

### The expiry rule

- A date sent by the caller wins, and it must be in the future. Otherwise: `The expiry date must be in the future.`
- With no date, the merchant's default applies.
- **With no date and a default of 0, which is the out-of-box value, the credit is refused:** `An expiry date (expired_at) in the future is required — the default validity for third-party credits is set to 0 (never expires).`

So out of the box, an integration must send a date, or the merchant must set a default validity. The help text on [[virtual-wallet-settings]] describes 0 as "never expires"; the refusal above is what happens.

### Other refusals

- `The customer is a guest and has no wallet.`
- `The credit amount must be a positive number.`

### One reference per customer

`reference` is unique per customer and credit type, so it can guard against sending the same credit twice.

### The API covers credits only

Deducting, manual credits and top-up settings are done in the admin. Spending happens at checkout.

## Related

- [[virtual-wallet]] — hub.
- [[api-customers]] — the customers resource.
- [[admin-graphql-api]] — the Admin GraphQL API.
- [[settings-api-keys]] — API keys for REST.
- [[webhook-entity-events]] — the webhook catalog.
- [[virtual-wallet-transactions]] — approving what arrives.

## Open questions

- The exact response when a duplicate `reference` is sent. (verify)
