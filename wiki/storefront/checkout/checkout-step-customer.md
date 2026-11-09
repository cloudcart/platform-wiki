---
type: storefront-page
nav_path: "Storefront → Checkout → Customer step (authorize)"
route_name: checkout
route_path: /checkout
themes_using: [all]
aliases: ["Checkout authorize step", "Checkout login", "Checkout guest", "Checkout register", "Email-code login", "Passwordless checkout login", "Стъпка клиент", "Идентификация на клиент"]
tags: [storefront, checkout, customer, authorize, login, guest, register]
plan_gates: []
created: 2026-06-12
updated: 2026-11-09
source_count: 5
---

> Part of [[checkout]]. See the hub for the other aspects (shipping, payment, sidebar, submit, routing, JavaScript).

# Checkout — Customer step (authorize)

## Purpose

The first step on `/checkout`. The customer either signs in (returning), registers a new account, or continues as guest. The merchant configures **which combination of these three** is allowed on [[settings-cart]]; the storefront then renders only the allowed tab. The chosen identity sticks on the cart for the rest of the flow — see [[customer]] vs [[subscriber]] for the distinction.

## URL & route

See `route_name` and `route_path` in frontmatter. This is a sub-section of [[checkout]] — the parent `/checkout` page hosts these step containers; container reload routes are listed under "Where to find it".

## How it loads

Loaded as a sub-region of the `/checkout` page (see [[checkout-page-routing]] for the parent route + middleware stack). On step transitions, the container is GET-reloaded via its `data-ajax-box` URL — see [[checkout-flow-storefront-backend-bridge]] for the full reload-fragment map.

## Where to find it

Top accordion section of the checkout page (`/checkout`). DOM: `<div class="cc-checkout-step cc-checkout-step-authorize js-checkout-authorize">`. The container reloads via `data-ajax-box="{route('checkout.authorize')}"` whenever the step machine ([[checkout-page-routing]]) tells it to.

## What the customer sees — three mutually-exclusive forms

The controller passes an `$allowed_tabs` collection from `cart->getAllowedLoginMethods`. The template picks ONE include based on a priority order:

| Priority | Tab key | Template | When shown |
|---|---|---|---|
| 1 | `guest` | `checkout/authorize/guest.tpl` | Allowed tabs includes `guest` — the most common configuration |
| 2 | `register` | `checkout/authorize/register.tpl` | No guest allowed but register is |
| 3 | (none) | `checkout/authorize/no-authorize.tpl` | Neither. A notice says why: a digital product (*"Only registered customers can purchase digital products"*) or a subscription in a guests-only store, else no sign-in method enabled |

The **"You have an account?"** link is rendered in the step's right-side addon (`cc-checkout-title-addon`) whenever `$allowed_tabs->has('login')`. Clicking it opens the login form in an ajax panel (`checkout/authorize/login.tpl`) without leaving the checkout page.

### Guest form fields

The guest form (`<form action="{route('checkout.guest')}" method="POST">`) collects:

- **Email** — `name="email"`, required, always shown.
- **Custom fields** (Customers → Custom Fields, type=`register`) — rendered through `customer/custom-form-component/{type}.tpl`. The first one shares a row with the email; the rest chunk into 2-column rows.
- **GDPR / marketing consent** — included from `checkout/include/gdpr.tpl` when the cart has guest email config; gated by store-wide GDPR settings (see [[settings-general]]).

The **Continue** button (`<button type="submit">`) is `disabled` until the email field has a value (initial state, JS lifts the disable as soon as the customer types).

### Login form

The login form is reused from the standard customer auth — `customer/auth/login.tpl` with `action=route('checkout.authorize.login')`. Email + password fields. Forgotten-password link goes to `checkout/authorize/forgotten-password.tpl`.

### Passwordless / email-code login

The platform option `checkout_login_code` turns on email codes at checkout. With it on, two paths use them:

- **A registered email in the guest form.** A 6-digit code goes to the address and a popup opens over the checkout: [[checkout-code-popup]].
- **Login with code** on the login form. The panel `checkout/authorize/access-code.tpl` takes the email, mails a code and takes the code; on success the cart is bound to the existing customer. This is the "no password remembered" path. Within a minute of the last code no new one is made. A code lives 60 minutes and takes 5 tries; spaces around a pasted code are trimmed. Refusals: `sf.error.access_code.invalid` (en *"Code is invalid"*, bg *"Кодът е невалиден"*), `sf.error.access_code.expired` (en *"Code is expired"*, bg *"Кодът е изтекъл"*, also for a code past its tries), and `sf.err.account.inactive` (en *"Your user account is not active"*, bg *"Вашият потребителски профил не е активен"*).

### Register form

`checkout/authorize/register.tpl` shows: email + password + password confirmation + GDPR + marketing consent + custom fields. POSTs to `checkout.authorize.register.post` (route-throttled at 20 req/min via a submission throttle).

## Settings & fields

Merchant-controllable settings that change what this step renders:

| Setting | Where set | Effect |
|---|---|---|
| **Customer profiles** (`checkout_customer_access`) | [[settings-cart-accounts-registration]] | `both`: guest, register, login. `member`: register, login. `guest`: guest only. A digital or subscription line drops `guest`. |
| `checkout_login_code` | Platform option, no admin screen | Turns on the email codes. |
| Custom fields (`type = register`) | [[customers-custom-fields]] | Adds extra inputs after email. |
| GDPR settings | [[settings-general]] | Adds marketing-consent + privacy-policy checkboxes. |

## Business rules

- **Allowed-tabs precedence — guest > register.** If both are allowed, the template renders **only the guest form**. To force registration, the merchant sets Customer profiles to registered only on [[settings-cart]]. A digital product or a subscription in the cart removes `guest` whatever the setting, so under `both` the register form (with password) shows — see [[checkout-flow-guest-vs-registered]].
- **Email is the single identity key.** Both guest and register paths bind on email. A guest email matching an existing [[customer|Customer]] does not continue as a guest: the code popup opens ([[checkout-code-popup]]).
- **Custom fields gate the Continue button.** Required custom fields must pass validation before the form submits; the guest endpoint (`checkout.guest`) re-validates server-side.
- **Bumper Offer block can render here.** If the `bumper_offer` app is installed and enabled and has products to surface, its block injects at the bottom of this step in mobile view — see [[apps-bumpcart]].
- **GDPR policy acceptances middleware** applies to both POST endpoints (`checkout.authorize.register.post` and `checkout.guest`) — the platform records consent on every submit. Failing to accept rejects the submit with a validation error.

## Storefront behaviour

See [[checkout-flow-storefront-backend-bridge]] for the DOM → endpoint → cart-attribute → reload-fragment full map. This section's specific form/click handlers + reload arrays are documented inline in the sections above.

## JavaScript behaviour

The container uses the universal checkout JS hooks — `.js-form-submit-ajax-new` (intercepts form submit, processes JSON response), `.js-checkout-hash-reload` (URL hash → auto-reload on page entry), `cc.checkout.step` event. Full catalogue: [[checkout-page-javascript]].

## Customisations available to the merchant

Merchant-controlled settings affecting this section are listed under "Settings & fields" above. Full theme-wide customisation catalogue: [[checkout-page-customisation]].

## Theme variations

Shared from the theme templates, so every theme inherits it unless it overrides a sub-template.

## Known issues / by-design vs bug

None beyond the business rules above.

## Related

- [[checkout]] — hub.
- [[checkout-page-routing]] — step-machine + what triggers a reload of this container.
- [[checkout-step-shipping]] — next step after the customer step.
- [[settings-cart]] — toggles for guest / register.
- [[checkout-code-popup]] — the popup for a registered email.
- [[customers-custom-fields]] — custom-field configuration.
- [[customer]] — the entity the form binds to.
- [[subscriber]] — distinct entity; not bound by checkout.
- [[apps-bumpcart]] — block that can inject at the bottom of this step.
- [[settings-general]] — GDPR + marketing-consent settings.
- [[checkout-flow-guest-vs-registered]] — concept page on the difference.

## Open questions

None — guest / register / login / email-code paths all verified against the platform code + `themes/_global/templates/checkout/authorize/*` on 2026-06-12.
