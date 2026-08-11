---
type: storefront-page
route_name: site.auth.login
route_path: /customer/auth/login
themes_using: [all]
tags: [storefront, customer, auth, login]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Customer login

## Purpose

Authenticates an existing customer against the store. Used both as a standalone page (link from header / account drawer) and as an in-checkout pane when checkout requires sign-in. After login the customer is redirected to a safe `_redirect` (if provided), to `/checkout` when their cart already has items, or to the account dashboard.

## URL & route

- Route name: `site.auth.login`
- Path: `/customer/auth/login` (or whichever locale prefix is active)
- Methods: `GET` renders the page; `POST` submits credentials and is wrapped in a submission throttle (20 attempts per minute per IP).
- Sibling routes used by the same form: `site.auth.forgotten`, `site.auth.register`, `site.auth.logout`, `site.auth.confirm.email`, `site.auth.reset_password`, `site.auth.login.social` (`provider` = `facebook|google`), `site.auth.login.social.callback`.

The form action is `route('site.auth.login')` by default, but if the page was opened during checkout (`activeRoute('checkout.authorize.login')`) the form swaps to the checkout-prefixed routes (`checkout.authorize.login`, `checkout.auth.forgotten`, `checkout.authorize.register`, `checkout.authorize.code`) so the login pane lives inside the checkout panel stack.

## How it loads

1. the request handler returns either a full page (via the platform code) or, when the platform code is true, a JSON envelope around `templatePath('auth-content')`. The latter is what the panel drawer uses.
2. The shared wrapper the theme templates renders the breadcrumb + container, then includes `./auth-content.tpl`, which dispatches on `$load_content` (here `./auth/login.tpl`).
3. The form is constrained by the request validator (`email` required + valid + `exist_customer_email:invalid-credentials` + max 191; `password` required, 3–20 chars). The rule `exist_customer_email:invalid-credentials` is what produces the generic "invalid credentials" error rather than leaking that an email exists.
4. On `POST`, `loginPost` first re-fetches the customer by email, checks `$customer->active` (throws `sf.err.account.inactive` if not), then calls the platform code.

## What the customer sees

- Email field (id `login-email`, `data-password="#login-password"` — used by the password-strength helper to relate the two inputs).
- Password field (id `login-password`).
- "Remember me" checkbox (id `login-remember`, value `1`).
- Primary submit: `cc-button cc-button-full js-loading` — disabled until the JS form binding wires it.
- "Login with Google" SSO button — only rendered when the platform code is true, see [[apps-google-connect]] / **apps-google-login**.
- "Access code" button (`cc-button-login-access-code`) — only shown during checkout (`$login_code` + `$code_url` set) so the customer can request a one-time login code instead of typing the password.
- Meta links at the bottom: forgotten-password link and register link, both opened either as full pages or as AJAX panels depending on the platform code.


## Storefront behaviour

- Both standalone-page and checkout-pane variants share the same template via the `activeRoute('checkout.authorize.login')` switch at the top.
- `_redirect` is honoured **only if it starts with `site->getSiteUrl`** — open-redirect protection. Same check runs again on the success path before storing `$this->complete_redirect`.
- After a successful login, redirect precedence is: `before_page` cookie (membership/private store, see [[apps-private-store]]) → safe `_redirect` query → `/checkout` if `getCustomerCart->has_products` → `/customer/account`.
- `logout` runs the platform code up to 5 times (500 ms back-off), forgets `policies_popup` session, and disposes the cart via the platform code. Redirect goes back to the login page.
- 2FA is not implemented on the storefront login flow — there is no second-factor prompt anywhere in the request handler. Admin 2FA lives in a different controller. (verify there is no app that injects a 2FA step)
- A "marketing newsletter" checkbox is **not** present on the login template. (verify whether any subscribe app injects one through Smarty `appendNew`)

## JavaScript behaviour

- Form class hooks: `cc-form`, `cc-form-login`, `js-form-submit-ajax-new`, `data-submit-loader="true"`.
  - `js-form-submit-ajax-new` is the canonical AJAX form binding — submits via XHR, listens for `cc.ajax.success` / `cc.ajax.error`, renders validation errors next to inputs via `js-error-<field-name>` containers.
  - `data-submit-loader="true"` adds the spinner on the submit button.
- Wrapping `<div class="cc-form-section js-error-invalid-credentials">` is the target for the generic "invalid credentials" error message.
- When the form is in an AJAX panel (the platform code), the forgotten/register/access-code links get `data-ajax-panel="true"`, `data-panel-class="short"`, and `data-ajax-panel-history='{"old":...,"new":...}'`, so navigating between the panes updates the panel stack instead of doing a full navigation.
- On success the controller usually returns an HTTP redirect; in the checkout-authorize variant it falls through `authorizeResponse` and can emit `cc.user.sign.in` events. (verify exact event payload)

## Customisations available to the merchant

The login form itself is intentionally minimal — most knobs sit upstream:

- Enabling [[apps-google-connect]] makes the "Login with Google" button appear without theme edits.
- `setting('checkout_hide_billing_address')` and the customer-fields configuration (see **settings-customers**) do not affect login but do reshape the register/account templates that the login page links to.
- Account lockout / brute-force defence is handled by the framework-level a submission throttle middleware on the POST route; the merchant cannot relax it from the admin.
- "Forgotten password" copy and email template are localisable via the `sf.module.user.login.*`, `sf.module.global.err.*` and forgotten-password mail templates.

## Theme variations

- Every storefront theme shares the theme templates and `auth.tpl` via the `_global` fallback. No theme in `themes/` ships its own `customer/auth/login.tpl` override at the time of writing. (verify by grepping each theme)
- Themes can still re-skin the form because the markup uses generic `cc-form`/`cc-button` classes that every theme styles.

## Known issues / by-design vs bug

- **By design**: identical "invalid credentials" message for both unknown email and wrong password. Driven by `exist_customer_email:invalid-credentials` validator + `js-error-invalid-credentials` wrapper.
- **By design**: inactive customers (`$customer->active === false`) get `sf.err.account.inactive` on the email field rather than a generic credentials error — this is how merchants can see that a deactivation in [[customers]] is taking effect.
- **By design, surprising**: when the customer's cart already has products, login redirects to `/checkout` not to the account dashboard. Reported regularly as "the system skipped my account page".
- **Limitation**: no rate-limit on the social-login flow itself beyond the upstream CC-Socialite service. (verify)
- Facebook and Apple social login buttons are not rendered on the storefront login template even when the apps are installed — only Google is wired in. (verify whether **apps-facebook-login** / **apps-apple-login** inject their own buttons)

## Related

- [[storefront-architecture]]
- [[storefront-known-issues]]
- [[customer-register]]
- [[customer-account]]
- [[checkout]]
- **settings-customers**
- [[customers]]
- **apps-google-login**
- [[apps-google-connect]]
- **apps-facebook-login**
- **apps-apple-login**

## Open questions

- Do **apps-facebook-login** / **apps-apple-login** inject their buttons via Smarty hooks, or are the routes effectively dormant?
- What is the actual lifetime of the "remember me" cookie? — needs to be read from the `auth.guards.customer` config.
- Is there any rate-limit on `socialLoginCallback`?
- Is the `cc.user.sign.in` event documented anywhere for theme developers to bind analytics to?
