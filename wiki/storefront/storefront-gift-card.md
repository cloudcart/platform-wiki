---
type: storefront-page
route_name: apps.gift_card.storefront
route_path: /gift-card
themes_using: [all]
aliases: ["Gift card page", "Gift cards storefront", "Buy gift card page", "Gift card link", "Подаръчни ваучери", "Страница за подаръчни ваучери", "Купи подаръчен ваучер"]
tags: [storefront, gift-card, apps]
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

# Gift card page

## Purpose

The storefront page that sells gift cards, with an optional form for redeeming a code. Each issued card also has a page of its own, opened from its email or PDF.

## URL & route

- Page: `apps.gift_card.storefront` → `GET /gift-card`. Title `Gift cards` / `Подаръчни ваучери`.
- A single card: `apps.gift_card.view` → `/gift-card/{hash}`.
- A card's PDF: `apps.gift_card.pdf` → `/gift-card/pdf/{hash}`.

The `{hash}` is unique to the card and arrives through its email, PDF or the customer's account.

## How it loads

The page shows only while the [[apps-gift-card|Gift Card]] app is active and its product exists; otherwise it returns 404. It wraps in the store's theme. It is not listed in the catalog, so a merchant links to it through a menu: section `gift_card` in [[design-navigation]].

## What the customer sees

**The sales page:**

- The artwork, or the bundled image if none was uploaded, with the name and description from [[apps-gift-card-settings]].
- `Validity: …` / `Валидност: …`, or `No expiry` / `Безсрочна`.
- Amount tiles, plus `Other amount` / `Друга сума` if allowed, with a min and max hint.
- `Send to` / `Изпрати до`: `My email` / `Моя имейл` (default) or `Recipient's email` / `Имейл на получател`.
- For a recipient: `Recipient email (optional)`, `Recipient name (optional)`, `Message (optional)`, `Send on (optional)` / `Изпрати на (по избор)`. The rules are on [[apps-gift-card-delivery]].
- `Buy` / `Купи`, with CloudCart Pay express buttons below for signed-in customers.
- With **Show redemption form on the gift-card page** on: `Redeem a gift card` / `Активиране на подаръчен ваучер`. Guests see `Sign in to your account to redeem a gift-card code.` instead.

**A single card's page:** the value, the recipient's name and message, the full code with `Copy code` / `Копирай кода`, a QR code, the validity, the status, `Redeem into wallet` / `Активирай в портфейла` and `Open PDF` / `Отвори PDF`. The QR code and the redeem button show only while the card can be used. A recipient needs no account to open this page; redeeming needs one.

Status lines on a card's page:

- `This voucher has already been redeemed and its value added to a wallet.`
- `This voucher has expired.`
- `This voucher is no longer valid.`

## Storefront behaviour

- **Buy** adds to a gift-only cart and opens the cart panel, as with a normal product. See [[apps-gift-card-purchase]].
- **Checkout** follows [[wallet-gift-instrument-checkout]]: a customer account, online payment only, no discounts.
- **Express buttons** pay for just the gift chosen in the form.
- **Redeeming** credits the signed-in customer's wallet and moves to [[customer-wallet]]. See [[apps-gift-card-redeem]].

## JavaScript behaviour

The form posts in the background. A refused amount or recipient email shows under its field, and the express buttons are dimmed while the form cannot be paid. Success fires the normal cart events `cc.cart.product.addToCart` and `cc.addToCart.product.added`, which open the cart panel. **Copy code** copies the code and briefly shows `Copied!` / `Копирано!`.

## Customisations available to the merchant

- Name, description, image, amounts, validity and the redeem form: [[apps-gift-card-settings]].
- The link in a storefront menu: [[design-navigation]], section `gift_card`.
- The printable card: [[apps-gift-card-pdf-template]].

## Theme variations

All themes use the same template, wrapped in the theme's layout.

## Known issues / by-design vs bug

- **By design:** 404 when the app is inactive, or before its settings were first saved and the product exists.
- **By design:** the headless storefront has no gift card operations. See [[virtual-wallet-checkout]].

## Related

- [[apps-gift-card]] — the app.
- [[apps-gift-card-purchase]] — how buying works.
- [[apps-gift-card-redeem]] — how redeeming works.
- [[customer-gift-cards]] — the customer's list.
- [[customer-wallet]] — where the value lands.

## Open questions

None.
