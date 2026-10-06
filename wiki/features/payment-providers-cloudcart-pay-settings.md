---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Settings"
route_name: apps.cloudcart_pay.settings
route_path: /admin/payment-providers/cloudcart_pay/settings
aliases: ["CloudCart Pay settings", "CloudCart Pay configuration", "Save customer card CloudCart Pay", "CloudCart Pay inline or popup", "CloudCart Pay digital wallets", "Настройки CloudCart Pay", "Показване при плащане", "Дигитални портфейли"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-05-21
updated: 2026-10-06
source_count: 4
---
# CloudCart Pay — Settings

## Purpose

The **Settings** tab of CloudCart Pay is where the merchant decides how the method behaves at checkout: whether customers can save cards, whether the card fields sit inline on the checkout page or open in a popup, whether Apple Pay and Google Pay are offered, and whether the express button appears on product pages. It also shows which CloudCart Pay account the store is linked to and whether the store domain is registered for Apple Pay. There are no API keys or test/live switches here.

## Where to find it

Settings → Payment methods → CloudCart Pay → **Settings** tab. Address: `/admin/payment-providers/cloudcart_pay/settings`.

## What the merchant can do here

- **See the connected account** and open the onboarding with **Manage Onboarding**, or start it with **Start Onboarding**.
- **Check and register the Apple Pay domain** — [[cloudcart-pay-apple-pay-domain]].
- **Turn Save Customer Card on or off** — [[cloudcart-pay-save-card]].
- **Turn express checkout on or off** on product pages (test environment only for now) — [[cloudcart-pay-express-checkout]].
- **Turn Apple Pay and Google Pay on or off.**
- **Choose the card form display**: inline or popup — [[cloudcart-pay-checkout-flow]].
- **Edit the standard fields** every payment method has: logo, title and description, minimum and maximum order amount, discount.

## Settings & fields

| Field / box | What it does | Default | Notes |
|---|---|---|---|
| **Connected Account** (Свързан акаунт) | The ID of the CloudCart Pay account the store is linked to, with **Manage Onboarding** (Управление на регистрацията). | — | Without an account the card reads **No connected account yet.** (Все още няма свързан акаунт.) with **Start Onboarding** (Започване на регистрацията). |
| **Apple Pay domain** (Домейн за Apple Pay) | The store domain, **Registered** / **Not registered**, and **Register domain** / **Re-register**. | — | Shown once an account is connected. See [[cloudcart-pay-apple-pay-domain]]. |
| **Save customer card** box → **Save Customer Card** | Signed-in customers can save their card and reuse it. | **On** | See [[cloudcart-pay-save-card]]. |
| **Express checkout** box (Експресно плащане) → **Express checkout on product pages** | Apple Pay / Google Pay button on product pages. | Off | Locked with **Coming soon** in the live environment. See [[cloudcart-pay-express-checkout]]. |
| **Digital wallets** box (Дигитални портфейли) → **Apple Pay**, **Google Pay** | Offers each wallet next to the card form and on the express button. | On, On | |
| **Checkout display** box (Показване при плащане) → **Card form display** | **Inline card fields** (Вградено) — the card fields inside the checkout page; **Popup window** (Изскачащ прозорец) — the card form opens after the complete-order button. | **Inline card fields** | Required; an empty value shows *"Card form display is required"*. |
| **Logo / Title / Description** | The method's label at checkout. | Provider defaults | Free to change. |
| **Amount (min / max)** | Order totals for which CloudCart Pay is offered. | Empty | Standard field. |
| **Discount** | A discount when the customer pays with CloudCart Pay. | None | Standard field. |
| **Active** (page header) | Turns the method on or off at checkout. | Off | Checked on every switch-on — see [[cloudcart-pay-activation-gate]]. |

Box help texts, verbatim:

- Save customer card — *"Enable saving customer cards for future purchases"*.
- Express checkout — *"Show an Apple Pay / Google Pay express checkout button on product pages so shoppers can buy a single product without going through the cart and checkout."*
- Digital wallets — *"Enable or disable Apple Pay and Google Pay. Applies to the popup checkout and the express checkout button on product pages."*
- Checkout display — *"Choose whether the card fields render directly in the checkout page or in a popup after clicking the complete order button."*

## Business rules

### Defaults, including for older stores

A store that never saved these settings gets: **Save Customer Card** on, **Apple Pay** and **Google Pay** on, **Inline card fields**. Express checkout starts off.

### Wallets apply everywhere

The **Apple Pay** and **Google Pay** switches apply to the inline card form, the popup and the express button alike, although the box's help text names only the popup and express. Apple Pay additionally needs the domain registered ([[cloudcart-pay-apple-pay-domain]]) and a device that supports it.

### Express checkout is "Coming soon" in the live environment

In the live environment (the badge in the page header) the express switch is disabled and shows **Coming soon**; it can be turned on only while the store charges in the test environment. See [[cloudcart-pay-express-checkout]].

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
- [[cloudcart-pay-save-card]] — saved cards.
- [[cloudcart-pay-express-checkout]] — express checkout on product pages.
- [[cloudcart-pay-apple-pay-domain]] — the Apple Pay domain card.
- [[cloudcart-pay-activation-gate]] — the Active switch.
- [[payment-providers-cloudcart-pay-transactions]] — the resulting card payments.
- [[settings-payment-providers]] — the payment methods list.
- [[settings-staff]] — staff roles and permissions.

## Open questions

- Bulgarian labels of the **Save Customer Card** switch and of the **Card form display** options as shown on screen (the Bulgarian names above come from the merchant help article).
