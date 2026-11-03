---
type: feature
nav_path: "Apps → Gift Card → PDF template"
route_name: apps.gift_card.pdf_template
route_path: /admin/apps/gift_card/pdf-template
aliases: ["Gift card PDF", "Gift card template", "Printable gift card", "Gift card design", "PDF на подаръчен ваучер", "Шаблон на подаръчен ваучер"]
tags: [apps, gift-card, pdf, template]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Gift Card — PDF template tab

> Part of [[apps-gift-card]]. See the hub for the other aspects.

## Purpose

Each issued card is a PDF: it is attached to the emails, opened from the customer's account, and printed if the customer wants. This tab replaces the built-in layout with the merchant's own HTML. Leaving it empty keeps the built-in layout.

## Where to find it

Sidebar → Apps → **Gift Card** → **PDF template**, at `/admin/apps/gift_card/pdf-template`.

The tab's intro reads: *"Custom HTML for the gift-card PDF. Leave empty to use the built-in default template. Click a variable to copy it."*

## What the merchant can do here

- Write the card's HTML in the editor.
- Click a token to copy it.
- Clear the editor to return to the built-in layout.

The logo for the PDF is uploaded on [[apps-gift-card-settings]].

## Settings & fields

**Tokens** (setting `pdf_body` holds the HTML):

| Token | What it prints |
|---|---|
| `{$amount}` | The value, in the order's currency |
| `{$code}` | The code, grouped, like `ABCD-EFGH-JKMN-PQRS` |
| `{$qr}` | A QR code that opens the scan-to-redeem link |
| `{$barcode}` | A barcode of the code |
| `{$recipient_name}` | The recipient's name |
| `{$message}` | The buyer's personal message, if any |
| `{$expires_at}` | The expiry date. Empty when the card never expires |
| `{$order_hash}` | The order's reference code |
| `{$site_id}` | The store's ID number |
| `{$logo}` | The uploaded PDF logo, or the store name when there is none |
| `{$shop_name}` | The store name |
| `{$domain}` | The store's web address |

## Business rules

### The built-in layout

It shows the value, the recipient and the message, the code with its valid-until date, the QR code, a **How to use** note and an **Important** note: `Treat this card like cash. Do not share the code with anyone you do not trust.` / `Пазете този ваучер като пари в брой. Не споделяйте кода с никого, ...`.

### A custom body that fails

If the custom HTML cannot be rendered, the PDF falls back to the built-in layout, so the customer always gets a card.

### The watermark follows the card's status

A diagonal watermark is added to the PDF whatever the template:

| Card | Watermark |
|---|---|
| Redeemed | `Redeemed` / `Активиран` |
| Disabled or past its validity | `Invalid` / `Невалиден` |
| Active | None |

The PDF is generated when it is opened or sent, so re-opening an old link shows the current status.

### QR code and barcode

The QR code opens a scan-to-redeem link: a signed-in customer redeems at once, and a guest goes through sign-in and returns ([[apps-gift-card-redeem]]). The barcode carries the plain code, for entry by hand or with a scanner.

### Language

The PDF is rendered in the language of the order.

## Related

- [[apps-gift-card]] — hub.
- [[apps-gift-card-settings]] — the PDF logo.
- [[apps-gift-card-delivery]] — where the PDF goes.
- [[apps-gift-card-redeem]] — what the QR code does.
- [[apps-gift-card-cards]] — **View** opens this PDF.

## Open questions

None.
