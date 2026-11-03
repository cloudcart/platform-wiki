---
type: feature
nav_path: "Apps → Gift Card"
route_name: apps.gift_card.overview
route_path: /admin/apps/gift_card
aliases: ["Gift Card", "Gift card app", "Gift cards", "Gift voucher", "Sell gift cards", "Подаръчен ваучер", "Подаръчни ваучери", "Подаръчна карта", "Подаръчни карти", "Ваучер за подарък", "Gift card payment"]
tags: [apps, gift-card, wallet, store-credit, hub]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Gift Card

## Purpose

The **Gift Card** app (`Подаръчен ваучер`, app key `gift_card`) lets a store sell gift cards. A customer buys a value and receives a code. Whoever redeems the code gets that value in their [[virtual-wallet|Virtual Wallet]], and spends it from there at checkout.

The card holds no money itself. The money moves when the code is redeemed into a wallet, so the app sits on top of the wallet: buy value → get a code → redeem into the wallet → spend.

The app is marked **beta**. This is a navigation hub. Each aspect has its own page.

## Where to find it

Sidebar → Apps → **Gift Card**, at `/admin/apps/gift_card`. It has four tabs:

| Tab | Path | Route name |
|---|---|---|
| Overview | `/admin/apps/gift_card` | `apps.gift_card.overview` |
| Settings | `/admin/apps/gift_card/settings` | `apps.gift_card.settings` |
| Cards | `/admin/apps/gift_card/cards` | `apps.gift_card.cards` |
| PDF template | `/admin/apps/gift_card/pdf-template` | `apps.gift_card.pdf_template` |

## Sub-pages (in this cluster)

- [[apps-gift-card-settings]] — the product, the amounts, custom amount, validity, on-page redemption.
- [[apps-gift-card-cards]] — the list of issued cards, and how a card shows on its order.
- [[apps-gift-card-pdf-template]] — the printable card, its tokens and watermark.
- [[apps-gift-card-purchase]] — how a customer buys a card and how codes are issued.
- [[apps-gift-card-delivery]] — who receives what and when, including **Send on** and **Resend**.
- [[apps-gift-card-redeem]] — where and how a code is redeemed, and the error messages.
- [[apps-gift-card-emails]] — the two emails and their tags.
- [[apps-gift-card-reversal]] — what cancelling or refunding the order does to its cards.

Customer-facing pages: [[storefront-gift-card]] and [[customer-gift-cards]]. Rules shared with wallet top-ups: [[wallet-gift-instrument-checkout]].

## What the merchant can do here

- Activate the app with the header toggle. It activates the hidden gift card product with it.
- Set the amounts, a custom amount and the code validity — [[apps-gift-card-settings]].
- Review issued cards, look one up by its code, open its PDF — [[apps-gift-card-cards]].
- Change the printable card — [[apps-gift-card-pdf-template]].
- Edit the customer emails — [[apps-gift-card-emails]].
- Add the `/gift-card` page to a storefront menu — [[design-navigation]], section `gift_card`.

To cancel or refund a card, work on its order — [[apps-gift-card-reversal]].

## Settings & fields

All fields are on [[apps-gift-card-settings]]. The API behind the tabs needs the `apps` permission.

## Business rules

- **A gift card is a code for the wallet.** It is not a payment method at checkout and not a discount code. The customer redeems first, then pays with the wallet ([[virtual-wallet-checkout]]).
- **Its value is one-time.** One card, one redemption. The whole value goes into one wallet ([[apps-gift-card-redeem]]).
- **Once redeemed, the credit never expires.** The validity setting limits only how long a code can be redeemed ([[apps-gift-card-settings]]).
- **Bought on its own checkout.** A gift card cannot share a cart with products, and is paid by online methods only ([[wallet-gift-instrument-checkout]]).
- **No invoice or VAT at purchase.** See [[virtual-wallet-vat-documents]].
- **Billing.** The app bills monthly and has no trial. It can be uninstalled. Its price depends on production and is not stated here. (verify)
- **The wallet need not be switched on.** Redeeming a code works with wallet top-ups off: the wallet page then shows the redeem form directly ([[customer-wallet]]).
- **Manual Voucher is separate.** The [[payment-providers-voucher|Voucher]] payment method is an offline method with no codes and no balance tracking.

## Related

- [[virtual-wallet]] — where the redeemed value lives.
- [[storefront-gift-card]] — the page that sells the card.
- [[customer-gift-cards]] — My account → Gift cards.
- [[wallet-gift-instrument-checkout]] — how the purchase works.
- [[apps]] — the App Store hub.

## Open questions

- The app's price in production. (verify)
- No plan gate was found in the code. (verify)
