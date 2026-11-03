---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["CloudCart Pay settings", "CloudCart Pay configuration", "Save customer card CloudCart Pay", "CloudCart Pay inline or popup", "CloudCart Pay payment page", "CloudCart Pay digital wallets", "Настройки CloudCart Pay", "Показване при плащане", "Дигитални портфейли"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-05-21
updated: 2026-11-03
source_count: 4
---
# CloudCart Pay — Settings

## Purpose

The **Settings** tab of CloudCart Pay is where the merchant decides how the method behaves at checkout: whether customers can save cards, whether the card fields sit inline on the checkout page, open in a popup or on a separate payment page, whether Apple Pay and Google Pay are offered, and where the express buttons appear. It also shows which CloudCart Pay account the store is linked to and whether the store domain is registered for Apple Pay. There are no API keys or test/live switches here.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Settings** tab. Address: `/admin/payment-providers/cloudcart_pay/settings`.

## What the merchant can do here

- **See the connected account** and open the onboarding with **Manage Onboarding**, or start it with **Start Onboarding**.
- **Check and register the Apple Pay domain** — [[cloudcart-pay-apple-pay-domain]].
- **Turn Save Customer Card on or off** — [[cloudcart-pay-save-card]].
- **Set up express checkout**: on or off for product pages, the cart and the checkout, and the look of the buttons — [[cloudcart-pay-express-button-settings]].
- **Turn Apple Pay and Google Pay on or off.**
- **Choose the card form display**: inline, popup ([[cloudcart-pay-checkout-flow]]) or a payment page ([[cloudcart-pay-hosted-page]]).
- **Edit the standard fields** every payment method has: logo, title and description, minimum and maximum order amount, discount.

## Settings & fields

| Field / box | What it does | Default | Notes |
|---|---|---|---|
| **Connected Account** (Свързан акаунт) | The ID of the CloudCart Pay account the store is linked to, with **Manage Onboarding** (Управление на регистрацията). | — | Without an account the card reads **No connected account yet.** (Все още няма свързан акаунт.) with **Start Onboarding** (Започване на регистрацията). |
| **Apple Pay domain** (Домейн за Apple Pay) | The store domain, **Registered** / **Not registered**, and **Register domain** / **Re-register**. | — | Shown once an account is connected. See [[cloudcart-pay-apple-pay-domain]]. |
| **Save customer card** box → **Save Customer Card** | Signed-in customers can save their card and reuse it. | **On** | See [[cloudcart-pay-save-card]]. |
| **Express checkout** box (Експресно плащане) | Three switches for the placements, plus wallet order, layout, height, radius, theme. | Product pages on, cart on, checkout off | See [[cloudcart-pay-express-button-settings]]. |
| **Digital wallets** box (Дигитални портфейли) → **Apple Pay**, **Google Pay** | Offers each wallet next to the card form and on the express buttons. | On, On | While the store domain is not verified, Apple Pay is left out of the store and its switch cannot be turned on. See [[cloudcart-pay-apple-pay-domain]]. |
| **Checkout display** box (Показване при плащане) → **Card form display** | **Inline card fields** (Вградено) — the card fields inside the checkout page; **Popup window** (Изскачащ прозорец) — the card form opens after the complete-order button; **CloudCart Pay payment page** — the shopper is sent to a separate page ([[cloudcart-pay-hosted-page]]). | **Inline card fields** | Required; an empty value shows *"Card form display is required"*. |
| **Logo / Title / Description** | The method's label at checkout. | Provider defaults | Free to change. |
| **Amount (min / max)** | Order totals for which CloudCart Pay is offered. | Empty | Standard field. |
| **Discount** | A discount when the customer pays with CloudCart Pay. | None | Standard field. |
| **Active** (page header) | Turns the method on or off at checkout. | Off | Checked on every switch-on — see [[cloudcart-pay-activation-gate]]. |

Box help texts, verbatim:

- Save customer card — *"Enable saving customer cards for future purchases"*.
- Express checkout — *"Show Apple Pay / Google Pay express checkout buttons on product pages, and optionally in the cart and the checkout, so shoppers can pay in one tap without filling in the checkout."*
- Digital wallets — *"Enable or disable Apple Pay and Google Pay. Applies to the popup checkout and the express checkout button on product pages."*
- Checkout display — *"Choose whether the card fields render directly in the checkout page, in a popup after clicking the complete order button, or on a CloudCart Pay payment page the customer is sent to. The payment page needs no Apple Pay verification of your store domain."*

## Business rules

### Defaults, including for older stores

A store that never saved these settings gets: **Save Customer Card** on, **Apple Pay** and **Google Pay** on, **Inline card fields**, express checkout on for product pages and the cart, off for the checkout. A value the merchant switched off stays off.

### Wallets apply everywhere

The **Apple Pay** and **Google Pay** switches apply to the inline card form, the popup, the payment page and the express buttons alike, although the box's help text names only the popup and express. Apple Pay additionally needs the domain verified ([[cloudcart-pay-apple-pay-domain]]) and a device that supports it.

### No credentials, no test/live switch

The merchant enters no keys: CloudCart holds them, and the store works through its connected account ([[cloudcart-pay-account-model]]). Saving therefore never fails on a credential. Whether the store charges in the **test** or **live** environment is set by CloudCart for the whole platform and shown read-only in the page header; the [[payment-providers-cloudcart-pay-transactions|Transactions tab]] shows only payments of that environment.

### What is saved

Only the settings on this tab are saved here. The business details, people, documents and bank accounts are not part of this form; they live on the connected account and are edited on the [[payment-providers-cloudcart-pay-onboarding|Onboarding tab]]. Saving also removes leftovers of older versions of the integration (old keys and cached business data) from the store's configuration.

### Connected account shown without a reload

Connecting or disconnecting on the Onboarding tab updates the **Connected Account** card here as soon as the merchant switches tabs.

### Staff access

The CloudCart Pay tabs open only for staff whose role allows the store's payment methods settings — see [[settings-staff]].

### Plan

No plan gate is declared for CloudCart Pay.

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-onboarding]] — where the connected account is created or linked.
- [[cloudcart-pay-checkout-flow]] — inline and popup card forms at checkout.
- [[cloudcart-pay-hosted-page]] — the payment page.
- [[cloudcart-pay-save-card]] — saved cards.
- [[cloudcart-pay-express-checkout]] — express checkout.
- [[cloudcart-pay-apple-pay-domain]] — the Apple Pay domain card.
- [[cloudcart-pay-activation-gate]] — the Active switch.
- [[payment-providers-cloudcart-pay-transactions]] — the resulting card payments.
- [[settings-payment-providers]] — the payment methods list.
- [[settings-staff]] — staff roles and permissions.

## Open questions

- Bulgarian labels of the **Save Customer Card** switch and of the **Card form display** options as shown on screen (the Bulgarian names above come from the merchant help article).
