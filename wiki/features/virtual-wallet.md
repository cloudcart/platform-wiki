---
type: feature
nav_path: "Products → Virtual Wallet"
route_name: orders.wallet.settings
route_path: /admin/wallet
aliases: ["Virtual Wallet", "Wallet", "Customer wallet", "Store credit", "Store credit balance", "Customer balance", "Wallet top-up", "Top up wallet", "Виртуален Портфейл", "Виртуален портфейл", "Портфейл", "Зареждане на портфейл", "Захранване на портфейл", "Баланс на клиент"]
tags: [wallet, store-credit, customers, checkout, orders, products, hub]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet

## Purpose

The **Virtual Wallet** is store credit held per registered customer. Customers load money into it, receive refunds and gift cards into it, and pay orders from it at checkout, fully or in part. It is a core feature of the platform, not an app. Both sidebar links carry a **beta** badge.

A customer needs an account to have a wallet. Guests, and customers in the Guests group, have none (`The customer is a guest and has no wallet.` / `Клиентът е гост и няма портфейл.`).

The balance is what is left of the customer's approved, unexpired credits after what was spent or written off. Each credit is a separate record with its own optional expiry, so one customer can hold several credits at once.

This is a navigation hub. Each aspect has its own page.

## Where to find it

One admin page, reached from two sidebar links:

| Tab | Path | Route name | Reached from |
|---|---|---|---|
| Settings | `/admin/wallet` | `orders.wallet.settings` | Products → **Virtual Wallet** (`Виртуален Портфейл`) |
| Transactions | `/admin/wallet/transactions` | `orders.wallet.transactions` | Orders → **Virtual Wallet transactions** (`Транзакции на виртуалния портфейл`) |
| Customers | `/admin/wallet/customers` | `orders.wallet.customers` | The tab on this page |

One customer's wallet is on their profile: `/admin/customers/details/:id/wallet`, route `customers-wallet`. See [[virtual-wallet-customers]].

## Sub-pages (in this cluster)

- [[virtual-wallet-settings]] — the Settings tab: the on/off switch, payment method name, top-up amounts, custom amount, refunded-funds expiry, third-party credits.
- [[virtual-wallet-transactions]] — the Transactions tab: every credit, its filters, and approving, rejecting and deleting.
- [[virtual-wallet-customers]] — the Customers tab with its export, and the Wallet tab on a customer's profile with **Add transaction**.
- [[virtual-wallet-checkout]] — paying with the wallet: the checkout box, partial and full payment, what the summary shows.
- [[virtual-wallet-order-lifecycle]] — what an order does to the wallet: reserved, spent, returned, and reversing a top-up.
- [[virtual-wallet-expiry]] — which credits expire, when they are written off, and the reminder.
- [[virtual-wallet-emails]] — the three customer emails and where to edit them.
- [[virtual-wallet-shipping-cod]] — cash on delivery and who pays shipping when a wallet is used.
- [[virtual-wallet-vat-documents]] — what the platform does for VAT, invoices, receipts and the Н-18 audit file.
- [[virtual-wallet-api]] — crediting through the API, Admin GraphQL operations, webhook fields.

The customer's side is on [[customer-wallet]]. Rules shared with gift cards are on [[wallet-gift-instrument-checkout]].

## What the merchant can do here

- Switch customer top-ups on or off and set the amounts — [[virtual-wallet-settings]].
- Name the payment method customers see — [[virtual-wallet-settings]].
- See every credit, and approve or reject credits waiting as Pending — [[virtual-wallet-transactions]].
- Add or deduct credit by hand on a customer's profile — [[virtual-wallet-customers]].
- Export the per-customer summary — [[virtual-wallet-customers]].
- Refund a return to the wallet — [[orders-returns-refunds]].

## Settings & fields

The settings themselves are on [[virtual-wallet-settings]]. Every credit carries these values:

**Type**

| Value | Label | Created by |
|---|---|---|
| `topup` | Top-up / Зареждане | A paid top-up order |
| `refund` | Refund / Възстановяване | A return refunded to the wallet |
| `gift` | Gift / Подарък | A redeemed gift card ([[apps-gift-card-redeem]]) |
| `manual` | Manual / Ръчно | **Add transaction** on the customer's profile |
| `bonus` | Bonus / Бонус | A credit sent through the API |
| `points` | Points / Точки | A label and filter value; no current flow creates it |

**Status**

| Value | Label | Counts in the balance |
|---|---|---|
| `approved` | Approved / Одобрен | Yes, until it expires |
| `pending` | Pending / В очакване | No |
| `rejected` | Rejected / Отхвърлен | No; kept for the record |

`Expired` / `Изтекъл` is shown for an approved credit past its expiry. It is a display and filter value, not a stored status.

**Source** (filter values): `real` Paid (real money) / Платено (реални пари), `bonus` Bonus / Бонус, `third_party` Third party / Трета страна. A credit an admin added shows that admin's name in the Source column.

## Business rules

- **No plan gate found.** The wallet code has no plan-feature check. (verify)
- **Top-ups can be paid online only.** Every tab shows a warning when the store has no active online payment method: *"Wallet top-ups can only be paid online. Enable at least one online (card) payment method, otherwise customers can reach the top-up checkout but will not be able to pay."* See [[wallet-gift-instrument-checkout]].
- **Switching top-ups off keeps the wallet.** Existing balances stay, and refunds and API credits still work and can be spent.
- **It is a tender, not a discount.** The order total, VAT base and invoice total stay full. See [[virtual-wallet-checkout]].
- **Staff permissions.** The Products link needs the `products` permission and the Orders link needs `orders`. All the wallet tabs load their data under `orders`, so a staff member with `products` only sees the link but cannot load the page's data.
- **Manual Voucher is separate.** The [[payment-providers-voucher|Voucher]] payment method is an offline method with no balance tracking and has nothing to do with this feature.

## Related

- [[customer-wallet]] — My account → Virtual wallet on the storefront.
- [[apps-gift-card]] — gift cards redeem into the wallet.
- [[wallet-gift-instrument-checkout]] — the rules for top-up and gift card checkouts.
- [[orders-returns-refunds]] — refunding a return to the wallet.
- [[customer-details-tab-strip]] — the Wallet tab on the customer profile.
- [[checkout-step-payment]] — the payment step that hosts the wallet box.
- [[products]] / [[orders]] — the sidebar areas that link here.

## Open questions

- Whether a plan restricts the wallet in production. The code shows no gate. (verify)
- Which existing stores already have the internal `wallet` payment provider and the email templates. Both are installed by staff-run commands. (verify)
