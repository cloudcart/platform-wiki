---
type: feature
nav_path: "Apps → Gift Card → Cards"
route_name: apps.gift_card.cards
route_path: /admin/apps/gift_card/cards
aliases: ["Issued gift cards", "Gift card list", "Find a gift card", "Gift card code lookup", "Издадени подаръчни ваучери", "Списък с подаръчни ваучери", "Търсене на подаръчен ваучер"]
tags: [apps, gift-card, list]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Gift Card — Cards tab

> Part of [[apps-gift-card]]. See the hub for the other aspects.

## Purpose

The Cards tab lists every issued gift card with its status, buyer, recipient and order. It is a read-only list for finding a card and opening its PDF.

## Where to find it

Sidebar → Apps → **Gift Card** → **Cards**, at `/admin/apps/gift_card/cards`.

Its notice reads: *"Issued gift cards. To cancel or refund a card, open its order — a card cannot be voided from this list."*

## What the merchant can do here

- Search and filter the cards.
- Open a card's PDF with **View**.
- Jump to the buyer's profile or the order.

Cancelling or refunding a card happens on its order; see [[apps-gift-card-reversal]].

## Settings & fields

### Columns

| Column | Shows |
|---|---|
| **Code** | Masked to its last group, like `••••-••••-••••-PQRS`. The full code is not shown here |
| **Amount** | The card's value |
| **Status** | Active, Redeemed, Disabled, Expired |
| **Buyer** | Links to the customer |
| **Recipient** | The recipient's email, if any |
| **Order** | Links to the order |
| **Issued** | Date and time |
| **Actions** | **View** opens the PDF |

### Filters and search

- **Status** (Is / Is not): `Active` / `Активен`, `Redeemed` / `Активиран`, `Disabled` / `Анулиран`, `Expired` / `Изтекъл`.
- **Customer**: the buyer.
- **Search**: the full code, the order number, the recipient's email and name.

## Business rules

### What each status means

| Status | Meaning |
|---|---|
| Active | Issued, not yet redeemed, still valid |
| Redeemed | Its value went into a wallet |
| Disabled | Its order entered a negative status before it was redeemed |
| Expired | The code's validity has passed without a redemption |

### Finding a card with a customer's code

The list never shows a full code, but the search matches one. Enter the customer's code in capitals without dashes to find its row. To see the code itself, open the PDF with **View**. See [[apps-gift-card-pdf-template]].

### One row per card

A quantity of 3 at 25 gives three rows, each with its own code ([[apps-gift-card-purchase]]).

### On the order page

A gift card line on [[orders-details]] shows status badges with a count per status, for example two Active and one Redeemed. Redeemed means already loaded into a wallet.

### No voiding, deleting or bulk actions

The list has no actions that change a card. A card stops working only through its order ([[apps-gift-card-reversal]]) or its validity.

### Who redeemed a card

The redeeming customer is not a column here. The wallet credit shows on [[virtual-wallet-transactions]] with type Gift and a message naming the code, and the card appears on that customer's [[customer-gift-cards]] page.

## Related

- [[apps-gift-card]] — hub.
- [[apps-gift-card-reversal]] — how a card is cancelled.
- [[apps-gift-card-pdf-template]] — what **View** opens.
- [[orders-details]] — the order line's badges.
- [[virtual-wallet-transactions]] — the credit a redemption creates.

## Open questions

None.
