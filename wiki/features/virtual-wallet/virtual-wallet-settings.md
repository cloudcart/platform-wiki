---
type: feature
nav_path: "Products → Virtual Wallet → Settings"
route_name: orders.wallet.settings
route_path: /admin/wallet
aliases: ["Wallet settings", "Top-up amounts", "Wallet top-up amounts", "Refunded-funds expiry", "Third-party credits", "Auto-approve third-party credits", "Настройки на портфейла", "Суми за зареждане на портфейла", "Име на метода за плащане портфейл"]
tags: [wallet, store-credit, settings, products]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---
# Virtual Wallet — Settings tab

> Part of [[virtual-wallet]]. See the hub for the other aspects.

## Purpose

The Settings tab controls whether customers can load their own wallet, how much they can load, what the payment method is called, and how long refunded and API credits last.

## Where to find it

Sidebar → Products → **Virtual Wallet** (`Виртуален Портфейл`), at `/admin/wallet`. It is the first tab. Changes are saved through the **Discard / Save** bar that appears when a field changes.

## What the merchant can do here

- Switch customer top-ups on or off.
- Name the wallet payment method shown at checkout and on the order and invoice.
- Name the top-up product and give it an image.
- Set the fixed top-up amounts, and allow a custom amount within limits.
- Set how long refunded credit stays valid.
- Decide whether API credits need approval, and their default validity.

## Settings & fields

| Box | Field | Setting | Default | Limits and notes |
|---|---|---|---|---|
| Virtual wallet | **Enable virtual wallet** | the top-up product's active flag | Off until first enabled | See below |
| Payment method name | **Payment method name** (placeholder `Wallet`) | the name on the wallet payment method | Empty uses the default | Max 191. Shown at checkout and on the order and invoice |
| Top-up product | **Product name** (placeholder `Wallet top-up`) | the top-up product | `Wallet top-up` | Max 191. Shown on the top-up screen, the order line and the receipt |
| Top-up product | **Product image** | the top-up product | None | Follows the store's upload size limit |
| Top-up amounts | Repeater with **Add amount** | one hidden variant per amount | None seeded | Min 0.01. The last row cannot be removed. Empty shows `No amounts yet.` |
| Custom amount | **Allow custom amount** | `wallet_custom_amount_enabled` | Off | |
| Custom amount | **Minimum**, **Maximum** (placeholder `No limit`) | `wallet_min_topup`, `wallet_max_topup` | 0 | 0 means no bound. Out of range: `Please enter a valid amount.` / `Моля, въведете валидна сума.` |
| Refunded-funds expiry | **Days until expiry** (placeholder `0 = never`) | `wallet_refund_expiry_days` | 0 | 0 to 3650 |
| Third-party credits | **Auto-approve third-party credits** | `wallet_auto_approve_thirdparty` | Off | Off means API credits wait as Pending |
| Third-party credits | **Default validity for third-party credits** (days) | `wallet_thirdparty_default_expiry_days` | 0 | 0 to 3650. See below |

## Business rules

### The on/off switch covers top-ups only

Help text: *"Turn the wallet top-up on or off for your store. When off, customers can no longer load their wallet themselves — but credit added another way (refunds or third-party integrations) still works and can be spent, and existing balances are kept."*

When it is off, the **Top-up product**, **Top-up amounts** and **Custom amount** boxes hide. **Payment method name**, **Refunded-funds expiry** and **Third-party credits** stay, because they apply either way.

### Top-ups never expire

There is no top-up expiry setting. A loaded credit lasts until it is spent. The page header ("Set the top-up amounts and expiry here") and the help text of **Refunded-funds expiry** ("A separate window from the top-up one") still use older wording. The expiry rule for each kind of credit is on [[virtual-wallet-expiry]].

### Default validity of 0 refuses API credits with no date

The help text says a default of 0 gives credits that never expire. The platform does something else: with 0, an API credit sent without an expiry date is **refused**, and the caller must send a future date. See [[virtual-wallet-api]].

### The top-up product is hidden everywhere

Amounts are stored as hidden variants on one internal product. It does not appear in the catalog, search, feeds, the Google Sheets export, product pickers, up-sell, cross-sell or bumper offers, and its product URL returns 404. Opening it in the product editor redirects to this page. The merchant manages it only here.

### The cart line label follows the store

On the cart line the amount appears under `Virtual wallet amount` / `Суми на виртуалния портфейл`. Changing the store's currency or language re-labels the saved amounts; the amounts themselves do not change.

### Online payment warning

When no online method is active, every wallet tab shows a warning, because top-ups cannot be paid in any other way. See [[wallet-gift-instrument-checkout]].

### Who can use this tab

The sidebar link needs the `products` permission, but the tab's data loads under `orders`. A staff member needs `orders` to read or save these settings.

## Related

- [[virtual-wallet]] — hub.
- [[customer-wallet]] — where customers see the amounts and load their wallet.
- [[wallet-gift-instrument-checkout]] — how a top-up is bought.
- [[settings-payment-providers]] — the online methods a top-up can be paid with.
- [[settings-staff]] — staff permissions.

## Open questions

- Whether the help text of the third-party default and the refund expiry box will be reworded in the admin translations. (verify)
