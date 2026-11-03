---
type: feature
nav_path: "Storefront → My account → Virtual wallet → Redeem a code"
route_name: ""
route_path: ""
aliases: ["Redeem gift card", "Gift card code not working", "Gift card code invalid", "Redeem a code", "Активирай код", "Активиране на подаръчен ваучер", "Кодът на ваучера не работи"]
tags: [apps, gift-card, wallet, redemption]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Gift Card — redeeming a code

> Part of [[apps-gift-card]]. See the hub for the other aspects.

## Purpose

Where a customer enters a gift card code, what the rules are, and what each error message means. Redeeming moves the card's whole value into the customer's [[virtual-wallet|Virtual Wallet]].

## Where to find it

A customer can redeem from five places:

| Place | Notes |
|---|---|
| [[customer-wallet]] at `/account/wallet` | `Redeem a code` / `Активирай код`, always there while the app is active. With no active top-up, the form shows inline |
| [[storefront-gift-card]] at `/gift-card` | When **Show redemption form on the gift-card page** is on |
| The card's own page | `Redeem into wallet` / `Активирай в портфейла` |
| The QR code on the PDF | A guest signs in and comes back |
| The link in the recipient's email | For one card, a one-click redeem |

## What the merchant can do here

- Choose whether `/gift-card` shows the form, on [[apps-gift-card-settings]].
- Look up a code on [[apps-gift-card-cards]] to see its status.
- See the resulting credit on [[virtual-wallet-transactions]], type Gift.

An admin cannot redeem a code for a customer; the customer does it from their account. To credit a customer by hand, see **Add transaction** on [[virtual-wallet-customers]].

## Settings & fields

No settings of its own. The form has one field for the code, and the button `Redeem` / `Активиране`.

**Messages:**

| Case | EN | BG |
|---|---|---|
| Success | `Your gift card was redeemed and your wallet has been topped up.` | `Подаръчният ваучер е активиран и портфейлът ви е зареден.` |
| Unknown code | `This gift-card code is not valid.` | `Този код на подаръчен ваучер не е валиден.` |
| Past its validity | `This gift card has expired.` | `Срокът на този подаръчен ваучер е изтекъл.` |
| Already used | `This gift card has already been redeemed.` | `Този подаръчен ваучер вече е активиран.` |
| Order cancelled or refunded | `This gift card is no longer valid.` | `Този подаръчен ваучер вече не е валиден.` |
| Not signed in | `Please sign in to redeem a gift card.` | `Моля, влезте в профила си, за да активирате подаръчен ваучер.` |
| Too many unknown codes | `Too many invalid attempts. Please try again in:hours hour(s).` | `Твърде много невалидни опити. Опитайте отново след:hours ч.` |

## Business rules

### A registered customer redeems

A guest, or a customer in the Guests group, has no wallet to receive the value.

### The value goes to whoever redeems

The credit goes to the signed-in customer who enters the code, whichever email the card was sent to. The card's PDF tells the holder to treat it like cash.

### One card, one redemption

The whole value goes in at once. A used card cannot be redeemed again, and two attempts at the same moment cannot both succeed.

### How the code can be typed

Dashes, spaces and letter case are ignored.

### What redeeming creates

A wallet credit with type Gift, source Paid (real money), status Approved and no expiry, with the message `Gift card:code redeemed` / `Активиран подаръчен ваучер:code`. It can be spent at checkout right away ([[virtual-wallet-checkout]]).

The customer also receives the `wallet_topup` email, with a link to that credit ([[virtual-wallet-emails]]). If the merchant switched that email off, none goes out.

### Validity

A code past its validity is refused, and the card's status becomes Expired. The window is set on [[apps-gift-card-settings]].

### Repeated unknown codes

Repeatedly entering codes that do not exist temporarily locks redemption for that customer, with the message above. A real code that is expired, used or disabled does not count towards it.

### After redeeming

If the buyer's order is later cancelled or refunded, the unspent part of the credit is removed from the wallet. See [[apps-gift-card-reversal]].

## Related

- [[apps-gift-card]] — hub.
- [[customer-wallet]] — the main place to redeem.
- [[virtual-wallet-checkout]] — spending the value.
- [[apps-gift-card-reversal]] — what can undo a redemption.
- [[virtual-wallet-emails]] — the confirmation email.

## Open questions

None.
