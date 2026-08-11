---
type: storefront-page
route_name: site.auth.register
route_path: /customer/auth/register
themes_using: [all]
tags: [storefront, customer, auth, register]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Customer register

## Purpose

Lets a new visitor open a customer account on the store. Used either as the standalone "create account" page (linked from header, login pane, checkout) or as the second step of social sign-in when the OAuth provider returned an email that is not yet in the customer table.

## URL & route

- Route name: `site.auth.register`
- Path: `/customer/auth/register`
- Methods: `GET` renders the form; `POST` → `site.auth.register.post` is rate-limited by a submission throttle and runs through the `gdpr_policy_acceptances` middleware (so GDPR checkbox enforcement happens before the controller).
- Checkout-context twin: `checkout.authorize.register` / `checkout.authorize.register.post` — the form swaps to those when the customer is mid-checkout, see [[checkout]].

## How it loads

1. the request handler builds the page array (`title`, `active`, `load_content => './auth/register.tpl'`, the platform code) and either returns a full `auth.tpl` render or a JSON envelope around `auth-content.tpl` when the platform code is true.
2. The custom merchant-defined fields injected as `$fields` come from the registration form configuration in the admin → see **settings-customers** (specifically the "Registration form fields" section). Each field is rendered by `themes/_global/templates/customer/custom-form-component/{type}.tpl`.
3. When the request originates from the social-login callback (`socialLoginCallback`), the controller passes `hash`, `social_first_name`, `social_last_name`, `social_email` into the same template — the email field is then rendered `readonly` and a hidden `hash` input is added so the form can finish wiring the OAuth account on submit.
4. On `POST`, the request validator validates, then the platform code creates the customer; `registerPost` then chooses the redirect.

## What the customer sees

Top section (fixed fields, all required):

- First name (id `register-fist_name` — note the typo, by design in template) and last name (id `register-last_name`). Both linked to `data-password="#register-password"` so the password-strength helper warns against using the name inside the password.
- Email (id `register-email`). Rendered `readonly` when arriving from social login. Validated as `required|email|unique_email|max:191`.
- Password (id `register-password`). Validated as `required|min:6|max:20` server-side. There is no zxcvbn-style strength meter — the password-helper only checks that name/email substrings are not reused. (verify)
- Alternative phone (id `checkout-shipping-marketplace-phone`) — rendered with the `js-phone-intl` class so the international-telephone-input module kicks in. Required.

Then, conditionally:

- Custom registration fields (`$fields`), chunked into two-per-row.
- Shipping-address sub-form — only when `setting('require_registration_shipping_address')` is on. Reuses `customer/address/_form.tpl` with `input_prefix='shipping'`.
- Billing-address sub-form — only when `setting('require_registration_billing_address')` is on. Same template with `input_prefix='billing'` and `force_hide_map=true`.
- GDPR consent block — pulled in via the platform code with `gdpr_form='register'`, see [[apps-gdpr-acceptance]] / [[apps-gdpr-policy]]. The contents (privacy, marketing, terms) are configured per-policy in [[apps-gdpr-settings]].

Footer: submit button (`cc-button js-loading`, disabled until JS binds), then a "back to login" meta link.

## Storefront behaviour

- the request validator enforces:
  - `first_name` required, max 255
  - `last_name` required, max 255
  - `email` required, valid, `unique_email`, max 191
  - `password` required, min 6, max 20
  - `alternative_phone` required
  - Plus GDPR rules from the request validator and the merchant's custom-fields rules from `CustomFields`
  - Plus, when the relevant settings are on, the full shipping/billing the request validator validation prefixed with `shipping.` / `billing.`
- the platform code creates the customer, fires registration events, and sets `is_activated` according to the customer-activation flow (the membership / private-store flow can leave the customer pending until an admin approves them).
- Post-registration redirect order:
  1. If a private-store redirect page is configured and the customer is not yet activated → membership redirect page.
  2. If the cart already has items → `/checkout`.
  3. If the form carried `checkout_express`, hand off to the express checkout authorise response (so the new customer keeps moving through checkout without re-clicking).
  4. Otherwise → `/customer/account` (same redirect helper as login).
- Newly-registered customers are auto-logged-in by the platform code unless `is_activated` is false. (verify the exact flag flow against the platform code)
- Default customer group is assigned by the platform code from the merchant's "default group" setting — see [[customers]] / **settings-customers**.

## JavaScript behaviour

- Form classes: `cc-form cc-form-register js-form-submit-ajax-new`, `data-submit-loader="true"`. Same AJAX submission machinery as login.
- Phone input: `js-phone-intl` triggers the international-telephone-input module with country flag, dial-code, and inline format validation. `data-error-label="sf.address.err.invalid_phone_number"` is shown when the entered number fails the lib's validation.
- When the registration sub-form is rendered inside an AJAX panel (drawer/checkout), the "back to login" link uses `data-dismiss="panel"` instead of a full navigation so the panel just closes back to the login pane.
- Address sub-forms inherit Google-Places autocomplete behaviour when a Maps key is configured — the visible street/city inputs feed hidden `data-google-place-*` inputs (`country_short`, `administrative_area_level_1_short`, `geo_name_city_id`, `geo_name_city_ascii_name`, `lat`, `lng`, `utc_offset`, `formatted_address`, `neighborhood`, `locality`) which are what gets POSTed.
- The `gdpr_form='register'` block emits its own JS for "accept all" / per-policy toggles; that JS is shared with the contact form and the newsletter module.

## Customisations available to the merchant

- Toggle `require_registration_shipping_address` and/or `require_registration_billing_address` in **settings-customers** to demand full address(es) at signup time.
- Toggle `checkout_hide_billing_address` to hide the billing block downstream (also affects the dashboard sidebar — billing link is removed).
- Add / remove / mark-required custom fields in the registration form configuration (Customers → Customer fields). Each `$field` renders via its `type` template.
- Configure the GDPR policies and which apply to the `register` form context — see [[apps-gdpr-policy]].
- Localise every label through the `sf.global.ph.*`, `sf.module.user.register.*`, `sf.address.*` translation keys.

## Theme variations

- All themes inherit the theme templates and the address `_form.tpl`. No per-theme override of the register template ships out-of-the-box. (verify by grep)
- Visual differences between themes come from CSS on `cc-form-*` / `cc-button-*` classes, not from template changes.
- The site flag `site_id == 17987` has a custom `account_17987.tpl` variant for orders, but the register flow is shared.

## Known issues / by-design vs bug

- **Typo by design**: `id="register-fist_name"` (missing the second `r`). Used as a JS selector elsewhere — renaming would break referrers.
- **By design**: a password is always required, even for social-sign-up users (the customer can later use the social provider OR the password to log in).
- **By design**: there is no double-opt-in email confirmation step blocking the registration itself — the platform code typically returns an authenticated customer immediately. A confirmation email may still be sent (see `site.auth.confirm.email` / `site.account.confirm.email`), but it does not gate access. The exception is the membership / private-store flow, which can hold the customer at the redirect page until activated.
- **Limitation**: the social-sign-up flow has no UI option to skip setting a password — the password field is still required even though the customer just authenticated via Google.
- **Limitation**: the international phone module validation is client-side only; the server check on `alternative_phone` is just `required`. A poorly-formatted phone can sneak through if JS is disabled. (verify whether downstream code re-validates)

## Related

- [[storefront-architecture]]
- [[storefront-known-issues]]
- [[customer-login]]
- [[customer-account]]
- [[customer-addresses]]
- [[checkout]]
- **settings-customers**
- [[customers]]
- **apps-google-login**
- [[apps-google-connect]]
- **apps-facebook-login**
- **apps-apple-login**
- [[apps-gdpr-acceptance]]
- [[apps-gdpr-policy]]
- [[apps-gdpr-settings]]
- [[apps-private-store]]

## Open questions

- Does the platform code actually issue an email-confirmation message by default, or only when a setting is on?
- Are there validation rules on the per-channel marketing-consent checkboxes that vary by GDPR-app configuration?
- What is the upper bound on the number of custom registration fields the form can render before layout breaks?
- Is the `unique_email` validator scoped per-site or per-merchant?
