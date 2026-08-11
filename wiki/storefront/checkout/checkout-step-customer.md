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
updated: 2026-06-12
source_count: 4
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
| 3 | (none) | `checkout/authorize/no-authorize.tpl` | Neither — customer must use the **"You have an account → log in"** addon link in the step header |

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

A separate **Login with code** path exists, gated by the `checkout_login_code` functionality flag (see [[settings-cart]]). When enabled:

- The login form shows a **"Login with code"** secondary action.
- Clicking it opens `checkout/authorize/access-code.tpl` in an ajax panel.
- The customer enters their email; the platform creates the platform code code, emails it to them.
- The customer enters the code on the same panel; on success the cart is bound to the existing customer.

This is the "no password remembered" recovery path — useful for customers who registered once months ago and lost their password.

### Register form

`checkout/authorize/register.tpl` shows: email + password + password confirmation + GDPR + marketing consent + custom fields. POSTs to `checkout.authorize.register.post` (route-throttled at 20 req/min via a submission throttle).

## Settings & fields

Merchant-controllable settings that change what this step renders:

| Setting | Where set | Effect |
|---|---|---|
| Allow guest checkout | [[settings-cart]] | If OFF, removes `guest` from `allowed_tabs`. |
| Allow registration | [[settings-cart]] | If OFF, removes `register`. |
| `checkout_login_code` | [[settings-cart]] | Unlocks the email-code login path. |
| Custom fields (`type = register`) | [[customers-custom-fields]] | Adds extra inputs after email. |
| GDPR settings | [[settings-general]] | Adds marketing-consent + privacy-policy checkboxes. |

## Business rules

- **Allowed-tabs precedence — guest > register.** If both are allowed, the template renders **only the guest form** (the `{if $allowed_tabs->has('guest')}` branch wins). To force registration, the merchant must disable guest on [[settings-cart]].
- **Email is the single identity key.** Both guest and register paths bind on email. A guest email matching an existing [[customer|Customer]] does NOT auto-merge — the platform creates an unauthenticated session for the guest; the customer remains separate until they log in with their password.
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

The template is shared from the theme templates — every theme inherits the same DOM. Themes can override individual sub-templates for per-theme tweaks, but the structure documented here applies to the default `flair` theme and every variant unless explicitly overridden.

## Known issues / by-design vs bug

None recorded for this section. Any merchant-facing surprises specific to this step are noted inline in the sections above (Business rules / Open questions).

## Related

- [[checkout]] — hub.
- [[checkout-page-routing]] — step-machine + what triggers a reload of this container.
- [[checkout-step-shipping]] — next step after the customer step.
- [[settings-cart]] — toggles for guest / register / login-code.
- [[customers-custom-fields]] — custom-field configuration.
- [[customer]] — the entity the form binds to.
- [[subscriber]] — distinct entity; not bound by checkout.
- [[apps-bumpcart]] — block that can inject at the bottom of this step.
- [[settings-general]] — GDPR + marketing-consent settings.
- [[checkout-flow-guest-vs-registered]] — concept page on the difference.

## Open questions

None — guest / register / login / email-code paths all verified against the platform code + `themes/_global/templates/checkout/authorize/*` on 2026-06-12.
