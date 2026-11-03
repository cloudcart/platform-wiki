---
type: feature
nav_path: "Apps → Gift Card → Settings"
route_name: apps.gift_card.settings
route_path: /admin/apps/gift_card/settings
aliases: ["Gift card settings", "Gift card amounts", "Gift card validity", "Gift card expiry", "Gift card custom amount", "Настройки на подаръчен ваучер", "Суми на подаръчен ваучер", "Валидност на подаръчен ваучер"]
tags: [apps, gift-card, settings]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Gift Card — Settings tab

> Part of [[apps-gift-card]]. See the hub for the other aspects.

## Purpose

The Settings tab sets what the store sells: the card's name and image, the amounts, an optional custom amount, how long a code stays valid, and whether the storefront page has a redeem form.

## Where to find it

Sidebar → Apps → **Gift Card** → **Settings**, at `/admin/apps/gift_card/settings`.

## What the merchant can do here

- Name and describe the card, and upload its image and the logo for its PDF.
- Set the fixed amounts, and allow a custom amount within limits.
- Make codes expire after a set time.
- Show a redeem form on the storefront gift card page.

## Settings & fields

| Box | Field | Setting | Default | Notes |
|---|---|---|---|---|
| Product | **Product Name** (placeholder `Gift card`) | on the hidden product | `Gift card` | Shown on the gift card screen, the order line and the receipt |
| Product | **Description** | on the hidden product | Empty | Rich text, shown on [[storefront-gift-card]] |
| Product | **Product image** | on the hidden product | Bundled artwork | Follows the store's upload size limit |
| Product | **PDF logo** | its own logo | None | Printed on the PDF. Without one, the store name is used |
| Gift card amounts | Repeater with **Add amount** | `amounts` | 10, 25, 50, 100 in the store currency | The fixed values on sale |
| Custom amount | **Allow custom amount** | `custom_amount_enabled` | Off | |
| Custom amount | **Minimum**, **Maximum** (placeholder `No limit`) | `min_amount`, `max_amount` | None | Outside the limits: `Please choose a valid gift-card amount.` |
| Validity | **Gift cards expire** | `validity_enabled` | Off | Off means codes never expire |
| Validity | **Valid for**, **Unit** (Days, Months, Years) | `validity_value`, `validity_unit` | 0, month | |
| On-page redemption | **Show redemption form on the gift-card page** | `redeem_on_page` | Off | Signed-in customers see the form. Guests see `Sign in to your account to redeem a gift-card code.` |

## Business rules

### Validity limits the code, not the money

**Gift cards expire** sets the window for **redeeming the code**. It is fixed when the card is issued, so changing the setting later does not affect cards already issued. Once a code is redeemed, the wallet credit never expires ([[virtual-wallet-expiry]]).

The help text cites EU consumer-protection guidance of at least 12 months for paid vouchers. The app's catalog description speaks of "how long a redeemed balance stays valid". That is not what this setting does.

On the storefront the page shows `Validity: …`, or `No expiry` / `Безсрочна` when off.

### Amounts become hidden variants

The app keeps one internal gift card product, and each amount is a hidden variant of it. The product does not appear in the catalog, search, feeds, the Google Sheets export, product pickers, up-sell, cross-sell or bumper offers, and its product URL returns 404. Opening it in the product editor redirects to this tab. The amounts are saved here, and the product follows on save.

### The app and its product switch together

The header toggle activates the app and the product together. While the app is inactive, [[storefront-gift-card]] returns 404, and no redeem form is offered.

### Validity and a scheduled send

If a card's code lapses before its **Send on** date, the recipient email is not sent. See [[apps-gift-card-delivery]].

## Related

- [[apps-gift-card]] — hub.
- [[storefront-gift-card]] — where these settings show.
- [[apps-gift-card-pdf-template]] — the PDF that uses the logo.
- [[apps-gift-card-redeem]] — what validity does when a code is entered.
- [[virtual-wallet-expiry]] — expiry of wallet credits.

## Open questions

None.
