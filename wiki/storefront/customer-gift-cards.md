---
type: storefront-page
route_name: site.account.gift-cards
route_path: /account/gift-cards
themes_using: [all]
aliases: ["My gift cards", "Gift cards on account", "Resend gift card from account", "Моите подаръчни ваучери", "Подаръчни ваучери в профила"]
tags: [storefront, customer, account, gift-card]
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

# My account → Gift cards

## Purpose

The customer's list of gift cards: the ones they bought and the ones they redeemed. From here a buyer can see the delivery status, open a card's PDF and resend it to the recipient.

## URL & route

- Page: `site.account.gift-cards` → `GET /account/gift-cards`, in the signed-in account area.
- Menu label: `Gift cards` / `Подаръчни ваучери`. Page heading: `My gift cards` / `Моите подаръчни ваучери`.
- The `{$account_link}` tag in the buyer's email leads here ([[apps-gift-card-emails]]).

## How it loads

The page renders inside the shared account layout ([[customer-account]]), right after the Virtual wallet item in the menu. It exists only while the [[apps-gift-card|Gift Card]] app is installed and active; otherwise the menu item is gone and the address returns 404.

## What the customer sees

A table, with pagination, of every card they bought or redeemed:

| Column | Shows |
|---|---|
| `Code` / `Код` | Masked to its last group, like `••••-••••-••••-PQRS`. The full code shows on hover on a desktop |
| `Amount` / `Сума` | The value |
| `Recipient` / `Получател` | The recipient's email, if any |
| `Delivery` / `Доставка` | `Scheduled for` / `Насрочен за` or `Sent on` / `Изпратен на`, with the date |
| Date | When the card was issued |
| Status | `Active` / `Активен`, `Redeemed` / `Активиран`, `Expired` / `Изтекъл`, `Disabled` / `Невалиден` |
| `PDF` | The PDF icon opens the card. The resend icon appears for a card with a recipient |

With no cards: `You have no gift cards yet.` / `Все още нямате подаръчни ваучери.`

## Storefront behaviour

- **Resend** sends the recipient's email again for that card, and is available only to the buyer. See [[apps-gift-card-delivery]].
- **The PDF** shows the card's current status as a watermark ([[apps-gift-card-pdf-template]]).
- **Redeeming** is not on this page. It is on [[customer-wallet]].

## JavaScript behaviour

The resend button posts in the background, shows the result, and reloads the list so the row shows the new date.

## Customisations available to the merchant

- The labels can be translated like other storefront texts.
- The PDF: [[apps-gift-card-pdf-template]].

## Theme variations

All themes use the same template inside the shared account layout.

## Known issues / by-design vs bug

- **By design:** a card redeemed by someone else stays on the buyer's list, showing Redeemed. It also appears on the redeeming customer's list.
- **By design:** the status label for a cancelled card differs: `Невалиден` here, `Анулиран` on the admin list. They are the same status ([[apps-gift-card-cards]]).
- **By design:** the code is masked in the table so an open page does not show it at a glance.

## Related

- [[apps-gift-card]] — the app.
- [[customer-account]] — the account area.
- [[customer-wallet]] — the redeem form and the balance.
- [[apps-gift-card-delivery]] — delivery and resend.
- [[storefront-gift-card]] — buying a card.

## Open questions

None.
