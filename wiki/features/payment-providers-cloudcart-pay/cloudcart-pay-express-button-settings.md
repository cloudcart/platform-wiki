---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings → Express checkout"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["Express checkout settings", "Express button look", "Wallet order", "Button layout", "Button height", "Button corner radius", "Button theme", "Google Pay first", "Apple Pay first", "Настройки на експресното плащане", "Вид на бутоните Apple Pay", "Цвят на бутона Google Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay, express-checkout, apple-pay, google-pay]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects; the general rules of the buttons are on [[cloudcart-pay-express-checkout]].

# CloudCart Pay — express checkout settings

## Purpose

The **Express checkout** box on the CloudCart Pay Settings tab turns the Apple Pay and Google Pay express buttons on for each placement and sets how they look. This page lists every field, its values and its default. The box's help text: *"Show Apple Pay / Google Pay express checkout buttons on product pages, and optionally in the cart and the checkout, so shoppers can pay in one tap without filling in the checkout."*

## Where to find it

Settings → Payment methods → CloudCart Pay → **Settings** tab → **Express checkout** box (Експресно плащане). Address: `/admin/payment-providers/cloudcart_pay/settings`.

## What the merchant can do here

- **Turn each placement on or off.**
- **Set the order of the wallets** and whether the buttons sit side by side or stacked.
- **Set the height, the corner radius and the theme** of the buttons.

## Settings & fields

| Label | Setting key | Values | Default |
|---|---|---|---|
| **Express checkout on product pages** (Експресно плащане в продуктовите страници) | `express_checkout` | On / Off | On |
| **Express checkout in the cart** | `express_cart` | On / Off | On |
| **Express checkout in the checkout** | `express_checkout_page` | On / Off | Off |
| **Wallet order** | `express_wallet_order` | Google Pay first, Apple Pay first | Google Pay first |
| **Button layout** | `express_layout` | Side by side, Stacked | Side by side |
| **Button height** | `express_button_height` | Default, 40 px, 44 px, 48 px, 56 px | Default |
| **Button corner radius** | `express_button_radius` | Default, 0 px, 4 px, 8 px, 12 px, 24 px | Default |
| **Button theme** | `express_button_theme` | Black, White, White with outline | Black |

**Apple Pay** and **Google Pay** in the **Digital wallets** box decide which buttons appear: see [[payment-providers-cloudcart-pay-settings]].

## Business rules

- **The first switch rules the rest.** Every other field shows only while **Express checkout on product pages** is on. With it off, no express button appears anywhere, including the gift card and wallet top-up forms.
- **Defaults apply to stores that never chose.** A store that never saved these settings gets the defaults above, so the product and cart buttons are on. A value the merchant switched off stays off.
- **Button theme.** Google Pay has no outline style, so **White with outline** gives plain white on Google Pay and white with an outline on Apple Pay.
- **Default height and radius** are the payment form's own.
- **Saving** needs no key and no check with a provider, as with the rest of this tab ([[payment-providers-cloudcart-pay-settings]]). Only the **Apple Pay** switch has a condition of its own ([[cloudcart-pay-apple-pay-domain]]).

## Related

- [[cloudcart-pay-express-checkout]] — when the buttons appear, the wallet sheet, the order.
- [[payment-providers-cloudcart-pay]] — hub.
- [[cloudcart-pay-express-placements]] — where each switch puts the buttons.
- [[payment-providers-cloudcart-pay-settings]] — the rest of the Settings tab.

## Open questions

- Bulgarian labels of these fields (production translation table).
