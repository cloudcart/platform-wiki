---
type: feature
nav_path: "Marketing → Channels → Email notifications"
route_name: ""
route_path: ""
aliases: ["Wallet emails", "Wallet top up email", "Wallet funds expiring email", "wallet_topup", "wallet_adjusted", "wallet_expiring", "Имейли за портфейла", "Имейл за зареждане на портфейл"]
tags: [wallet, store-credit, email, notifications]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — customer emails

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

The three emails the wallet sends to customers, when each goes out, and which tags it offers. A top-up order has no ordinary order emails, so these are what the customer receives. See [[wallet-gift-instrument-checkout]].

## Where to find it

Sidebar → Marketing → Channels → **Email notifications**, at `/admin/marketing/omnichannel/mails/list`. See [[marketing-omnichannel-mails-list]].

## What the merchant can do here

- Edit the subject and body of each email in the email builder.
- Use the tags listed below.
- Switch an email off through its status.

## Settings & fields

| Label | Name | Subject (EN) | When it goes out |
|---|---|---|---|
| `wallet_topup` | Wallet top up | `Your virtual wallet in {$shop_name} has been topped up.` | A paid top-up is credited, once per order. Also when a gift card is redeemed |
| `wallet_adjusted` | Virtual Wallet Adjustment | `Your {$shop_name} wallet balance was adjusted` | An order edit returned wallet funds |
| `wallet_expiring` | Wallet Funds Expiring | `Funds in your {$shop_name} wallet are expiring soon` | The daily reminder ([[virtual-wallet-expiry]]) |

### Tags beyond the common ones

| Email | Tags |
|---|---|
| `wallet_adjusted` | `{$amount}` (the amount returned), `{$wallet_balance_new}` (the new balance) |
| `wallet_expiring` | `{$amount}` (the unspent amount expiring), `{$wallet_expiry_date}` (the nearest date), `{$wallet_balance}` (the full balance) |
| `wallet_topup` | Order and shop tags. It offers no discount, address, shipping or tracking tags, because a top-up has none |

The button in `wallet_topup` links to `/account/wallet?filters[id]=…`, which shows that one credit on [[customer-wallet]].

## Business rules

- **A single email for a top-up.** `wallet_topup` is sent at the moment of crediting, once, and retried payments do not send it again. The generic order confirmation, status-change, shipped and file-download emails are not sent for a top-up order.
- **No email when an order is cancelled.** A negative status returns the wallet money with a history entry and no email ([[virtual-wallet-order-lifecycle]]).
- **No email for a manual credit or deduction** made on the customer's profile ([[virtual-wallet-customers]]).
- **The expiry reminder needs a sendable template.** It goes out when the template is active and customer email notifications are on. See [[virtual-wallet-expiry]].
- **Gift card emails are separate.** Those are on [[apps-gift-card-emails]]; only the confirmation after redeeming reuses `wallet_topup`.

## Related

- [[virtual-wallet]] — hub.
- [[marketing-omnichannel-mails-list]] — where the templates are edited.
- [[virtual-wallet-expiry]] — the reminder's timing.
- [[virtual-wallet-order-lifecycle]] — when `wallet_adjusted` fires.
- [[apps-gift-card-emails]] — the gift card emails.

## Open questions

- Which existing stores have these three templates. They reach existing stores through a staff-run seed. (verify)
