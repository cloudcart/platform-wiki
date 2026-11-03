---
type: storefront-page
route_name: site.account.wallet
route_path: /account/wallet
themes_using: [all]
aliases: ["My wallet", "Customer wallet page", "Top up wallet", "Wallet balance on account", "Виртуален портфейл", "Зареди портфейла", "Наличност в портфейла", "Моят портфейл"]
tags: [storefront, customer, account, wallet, store-credit]
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

# My account → Virtual wallet

## Purpose

The customer's own view of their [[virtual-wallet|Virtual Wallet]]: the balance, funds about to expire, loading money, redeeming a gift card, and a history of everything that moved.

## URL & route

- Page: `site.account.wallet` → `GET /account/wallet`, in the signed-in account area.
- Menu label: `Virtual wallet` / `Виртуален портфейл`.
- The `wallet_topup` email links to `/account/wallet?filters[id]=…`, which shows that one credit, with a link back to the full list.

## How it loads

The page renders inside the shared account layout ([[customer-account]]). The menu item appears when the store has a wallet top-up product, even with top-ups off, or when the customer has any wallet history.

## What the customer sees

**Balance tile:** `Balance` / `Наличност`.

**Expiry banner:** when funds expire within 30 days, `Expiring funds %s on %s` / `Изтичащи средства %s на %s`, with the amount and the nearest date.

**Top-up section** `Top up wallet` / `Зареди портфейла`, only while top-ups are enabled and amounts exist:

- Amount tiles, one per amount set on [[virtual-wallet-settings]].
- `Other amount` / `Друга сума` if custom amounts are allowed, with a min and max hint.
- The button `Load` / `Зареди`.
- CloudCart Pay express buttons under it, for this signed-in customer, when express is on ([[cloudcart-pay-express-checkout]]).

**Redeeming:** with the [[apps-gift-card|Gift Card]] app active, a `Redeem a code` / `Активирай код` tile opens a dialog. With no active top-up, an inline redeem form shows instead. See [[apps-gift-card-redeem]].

**Activity table:** `Date`, `Description`, `Status`, `Expires`, `Amount`, 25 rows per page.

| Row | How it shows |
|---|---|
| A credit, in any status | The message, status and expiry. `∞` means it never expires |
| A spend | Grouped per order: `Spent on order:order` / `Използвано за поръчка:order` |
| Pending | Amount greyed |
| Rejected | Amount struck through, the merchant's reason in a tooltip |
| Expired with unused funds | Row in red, status `Expired` |
| Expiring soon with unused funds | Row in yellow |

With no activity: `No wallet activity yet.` / `Все още няма движения по портфейла.`

## Storefront behaviour

- **Loading money** goes straight to a separate checkout, without touching the main cart. See [[wallet-gift-instrument-checkout]] for its rules.
- **The credit arrives** when the payment completes, once, followed by the `wallet_topup` email ([[virtual-wallet-emails]]).
- **Out-of-range custom amount:** `Please enter a valid amount.` / `Моля, въведете валидна сума.` shows under the field.
- **Top-ups off:** the balance and history stay. `Top-up is currently unavailable.` / `Зареждането в момента не е достъпно.` answers a stale form.
- **Spending** happens at checkout ([[virtual-wallet-checkout]]).

## JavaScript behaviour

The top-up form posts in the background, shows errors under the amount field, and moves to the checkout on success. Picking `Other amount` reveals its input. The redeem tile opens its dialog with `.js-gc-redeem-open`, and `.js-gc-redeem-close` closes it.

## Customisations available to the merchant

- The amounts, the limits and the product name and image: [[virtual-wallet-settings]].
- The name of the method at checkout: **Payment method name** on [[virtual-wallet-settings]].
- Storefront labels sit under `sf.account.wallet.*`, and can be translated like other storefront texts.

## Theme variations

All themes use the shared template. Some labels may be restyled through the `cc-wallet-*` classes.

## Known issues / by-design vs bug

- **By design:** a Pending credit shows in the activity but is not in the balance. It waits for the merchant's approval ([[virtual-wallet-transactions]]).
- **By design:** the Amount on a credit does not shrink as it is spent. Spends are their own rows.
- **By design:** a manual credit or deduction by the merchant sends no email. It only appears here.
- **By design:** on a store that never set up top-ups, the menu item appears only once the customer has wallet history. The page itself still opens at its address, which is where the gift card links lead.
- **By design:** the headless storefront has no wallet page. See [[virtual-wallet-checkout]].

## Related

- [[virtual-wallet]] — the admin side.
- [[customer-account]] — the account area.
- [[customer-gift-cards]] — My account → Gift cards.
- [[virtual-wallet-expiry]] — the expiry rules.
- [[apps-gift-card-redeem]] — redeeming a code.

## Open questions

None.
