---
type: storefront-page
nav_path: "Storefront → Checkout → Customer step → Code popup"
route_name: checkout
route_path: /checkout
themes_using: [all]
aliases: ["Checkout code popup", "Recognised account", "You have an account with this email", "Remember me on this device", "Guest email already registered", "Code login at checkout", "Имате профил с този имейл", "Разпознат профил", "Запомни ме на това устройство", "Смени имейла", "Изпрати нов код", "Код за вход при поръчка"]
tags: [storefront, checkout, customer, login, email-code, popup]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 3
---

> Part of [[checkout]]. The step around it is [[checkout-step-customer]].

# Checkout — code popup for a registered email

## Purpose

A guest at the checkout's customer step types an email that already has an account. The store mails a 6-digit code to that address and opens a popup over the checkout to enter it. The right code signs the customer in, and the checkout continues with their profile.

The mail goes out while the platform option `checkout_login_code` is on. It has no screen in the admin. This page describes the flow with the option on.

## URL & route

The popup opens over `/checkout`. See `route_path` in the frontmatter. It answers the guest form (`checkout.guest`) and checks the code on `checkout.authorize.code`.

## How it loads

It comes back as the answer to the guest email form, or to the email field when the store collects the email in the shipping address form. Guest refusals come first: a cart with digital products, a cart with a subscription and a members-only store refuse the guest with their own messages (*"Only registered customers can purchase digital products"*, *"Only registered customers can purchase a subscription"*, *"Only registered users can perform checkouts"*).

## What the customer sees

| Element | English | Bulgarian |
|---|---|---|
| Badge | Recognised account | Разпознат профил |
| Title | You have an account with this email | Имате профил с този имейл |
| Text | We sent a 6-digit code to:email. Enter it to continue with your order. | Изпратихме 6-цифрен код на:email. Въведете го, за да продължите с поръчката. |
| Link | Change email | Смени имейла |
| Checkbox, ticked by default | Remember me on this device | Запомни ме на това устройство |
| Resend | Send a new code | Изпрати нов код |
| Tries | :count attempts left with this code. | Остават:count опита с този код. |
| Wrong code | The code is wrong or has expired. Check the latest email. | Кодът е грешен или е изтекъл. Проверете последното писмо. |
| Code used up | This code is no longer valid. Send yourself a new one. | Кодът вече не е валиден. Изпратете си нов. |

Six digit fields take typing or a paste. On a phone the popup rises from the bottom of the screen.

## Storefront behaviour

| Rule | Value |
|---|---|
| Code is valid for | 60 minutes |
| Tries per code | 5, then a new code is needed |
| Time between sends | 60 seconds, with a countdown |
| Checked | Automatically, on the sixth digit |

- **The popup ends with the code or through Change email.** It has no close button, and a click outside leaves it open.
- **Change email** opens a field for another address inside the popup. Another registered address gets a fresh code and popup. Any other address closes the popup, goes into the checkout form and continues as a guest.
- **Remember me on this device** keeps the customer signed in for 400 days. Without it, the session lasts 7 days.
- **After the right code**, the popup closes with *"You are signed in to your account."* and the checkout reloads with the customer's data.
- **An inactive account** is refused with *"Your user account is not active"*. A banned account is refused too.
- **The password login** stays available through the **You have an account?** link in the step's header ([[checkout-step-customer]]).

## JavaScript behaviour

The popup is sent with the form's answer and runs on its own. The resend countdown is kept per address for the browser session, so reloading the page or reopening the popup continues it. Esc on the code screen opens **Change email**.

## Customisations available to the merchant

None. The wording comes from the storefront translations ([[settings-translations]]).

## Theme variations

The template is shared from the global checkout templates, so every theme shows the same popup.

## Known issues / by-design vs bug

None recorded.

## Related

- [[checkout]] — hub.
- [[checkout-step-customer]] — the guest form that opens the popup.
- [[checkout-flow-guest-vs-registered]] — guest and registered checkout.
- [[customer-login]] — the sign-in page.
- [[customer]] — the account behind the email.

## Open questions

None.
