---
type: feature
nav_path: "Marketing → Channels → Email notifications"
route_name: ""
route_path: ""
aliases: ["Gift card emails", "gift_card_buyer", "gift_card_recipient", "Gift voucher to the buyer", "Gift voucher to the recipient", "Подаръчен ваучер — до купувача", "Подаръчен ваучер — до получателя", "Имейли за подаръчен ваучер"]
tags: [apps, gift-card, email, notifications]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Gift Card — customer emails

> Part of [[apps-gift-card]]. See the hub for the other aspects.

## Purpose

The two emails that deliver a gift card, and the tags each offers. Installing the app adds them to the store's email templates. Since a gift card order sends no ordinary order emails ([[wallet-gift-instrument-checkout]]), these are what the customer receives.

## Where to find it

Sidebar → Marketing → Channels → **Email notifications**, at `/admin/marketing/omnichannel/mails/list`. See [[marketing-omnichannel-mails-list]].

## What the merchant can do here

- Edit the subject and body of both emails in the email builder. They are not locked.
- Use the tags listed below.
- Use the store's own voice: the wording is meant to be changed.

## Settings & fields

| Label | Name (EN / BG) | Subject (EN / BG) |
|---|---|---|
| `gift_card_buyer` | Gift voucher — to the buyer / Подаръчен ваучер — до купувача | `Your gift cards from {$shop_name}` / `Вашите подаръчни ваучери от {$shop_name}` |
| `gift_card_recipient` | Gift voucher — to the recipient / Подаръчен ваучер — до получателя | `You received a gift from {$shop_name}` / `Получавате подарък от {$shop_name}` |

### Tags

| Email | Tag | What it prints |
|---|---|---|
| Both | `{$logo}` | The store's email logo |
| Both | `{$gift_icon}` | The gift card artwork |
| Both | `{$shop_name}` | The store name |
| `gift_card_buyer` | `{$customer_first_name}` | The buyer's first name |
| `gift_card_buyer` | `{$account_link}` | A link to My account → [[customer-gift-cards|Gift cards]] |
| `gift_card_recipient` | `{$buyer_name}` | The buyer's name, or the store name if there is none |
| `gift_card_recipient` | `{$amount}` | The total of the cards in this email |
| `gift_card_recipient` | `{$message}` | The buyer's message |
| `gift_card_recipient` | `{$redeem_link}` | See below |

## Business rules

### Where `{$redeem_link}` leads

- **One card in the email:** a link that redeems that card with one click ([[apps-gift-card-redeem]]).
- **Several cards in the email:** `/gift-card` if **Show redemption form on the gift-card page** is on, otherwise `/account/wallet`. One link cannot redeem several cards, and each PDF still has its own QR code.

### Attachments

Each card is attached as its own PDF ([[apps-gift-card-pdf-template]]). The code is not in the email text, and no tag prints it.

### They ignore the global switch

These two emails go out even with the store's global customer notifications switch off, so a paid card is always delivered.

### When they go out

The timing is on [[apps-gift-card-delivery]]. The buyer's email goes out at once. The recipient's follows the **Send on** date.

### Redeeming sends a different email

The confirmation after a code is redeemed is the wallet's `wallet_topup` template, not a gift card one. See [[virtual-wallet-emails]].

### Language

Each email uses the language of the order.

## Related

- [[apps-gift-card]] — hub.
- [[marketing-omnichannel-mails-list]] — where the templates are edited.
- [[apps-gift-card-delivery]] — timing.
- [[apps-gift-card-pdf-template]] — the attachment.
- [[virtual-wallet-emails]] — the wallet emails.

## Open questions

None.
