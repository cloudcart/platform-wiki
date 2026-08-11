---
type: storefront-page
route_name: site.account.address.shipping.list / site.account.address.billing.list
route_path: /customer/account/address/shipping, /customer/account/address/billing
themes_using: [all]
tags: [storefront, customer, account, address]
created: 2026-06-08
updated: 2026-06-08
source_count: 4
---

# Customer addresses

## Purpose

Lets the signed-in customer maintain a personal address book — one collection for shipping, one for billing. Used both from the account area (manage / set default) and from checkout (the same list / form templates render inside the checkout panels). Every order pulls from this book so the customer never re-types.

## URL & route

Two parallel groups of routes, both inside the `account` prefix, both protected by the `customer` middleware **and** the `customer_addresses` middleware.

Shipping addresses:

- `site.account.address.shipping.list` — `GET /customer/account/address/shipping`
- `site.account.address.shipping.create` — `GET /customer/account/address/shipping/add/{checkout?}`
- `site.account.address.shipping.save` — `POST /customer/account/address/shipping/add/{checkout?}` (`XSS` middleware)
- `site.account.address.shipping.edit` — `GET /customer/account/address/shipping/edit/{address_id}/{checkout?}`
- `site.account.address.shipping.update` — `POST /customer/account/address/shipping/edit/{address_id}/{checkout?}` (`XSS` middleware)
- `site.account.address.shipping.default` — `GET /customer/account/address/shipping/default/{address_id}`
- `site.account.address.shipping.remove` — `GET /customer/account/address/shipping/remove/{address_id}`

Billing addresses use the same shape with `billing` in place of `shipping`. The optional `{checkout?}` segment is sent by the checkout pane so the save redirects back into checkout rather than to the account dashboard.

## How it loads

1. The list screen fetches the customer's addresses of the requested type and renders them inside the shared account wrapper (sidebar + main column).
2. The list template is **parameterised on `$type`** (`shipping` or `billing`) — it builds its route names from `$type`, so one template serves both lists.
3. The create / edit screens load the address form, which includes a shared form partial with `input_prefix='shipping'` or `'billing'`. The same partial powers the registration page and checkout, so behaviour stays consistent across entry points.
4. The `customer_addresses` middleware gates the feature for the site and the customer's right to manage their own book. (verify exact gating)

## What the customer sees

List view (`cc-address-book`):

- One `cc-address-book-item` card per address. The default card carries the `active` class.
- Each card is a clickable region (`cc-address-book-item-data`); **for non-default cards** it links to `site.account.address.{type}.default/{address_id}` with `data-ajax="toast"` and a `data-confirm="sf.account.details.confirm.set_default_address"` prompt. Clicking the default card is a no-op (`href="javascript:;"`).
- Display fields per card: full name, country, state, city, street + number, optional `address1`, postal code, phone (national format), and — when present — company name + company VAT.
- Two corner actions: pencil → edit, red × → remove (with confirm). Edit opens in an AJAX panel (`data-ajax-panel="true"` `data-panel-class="js-checkout-{type}-address-holder"`).
- "Add new address" tile (`cc-address-book-item-add`) at the end opens the create form in the same AJAX panel.

Form view (`_form.tpl`) — same fields as the checkout address pane:

- Hidden Google-Places data inputs (`data-google-place-*`): `country_short`, `country.iso2`, `administrative_area_level_1_short`, `geo_name_city_id`, `geo_name_city_ascii_name`, `lat`, `lng`, `utc_offset`, `formatted_address`, `neighborhood`, `locality`.
- First / last name fields, labelled differently for billing (`sf.global.ph.first_name_billing`, `sf.global.ph.last_name_billing`) and gated by `checkout_hide_first_name` / `checkout_hide_last_name` (values: `required`, `optional`, `hidden`).
- Country / state / city autocomplete chain — country is locked to the only option in a single-country store, otherwise a Google Places autocomplete (when a Google Maps key is set) or a plain select.
- Street, street number, address1, postal code, phone.
- Company toggle (commented out in the current template but the logic is wired) — would show company name + VAT fields, gated by the radio. (verify whether any theme override re-enables it)
- Save button. On submit the form fires the AJAX submission; on success it triggers `cc.ajax.reload` on `.js-address-{type}-holder:first`, re-rendering the list.

## Storefront behaviour

- Shipping country options are the union of countries any installed **shipping-providers** support; billing options are the union of tax-zone-enabled countries (see [[settings-taxes]]).
- Whether the state field is a free-text required input or an optional dropdown depends on the selected country.
- Setting a default flips the flag in the customer's address-of-type set and emits `cc.user.address.setDefault`, which the list binds to in order to refresh.
- Removing an address soft-removes it (verify) and emits `cc.user.address.removed`.
- The company-VAT field is validated server-side via the address request rules; it is meant for B2B billing addresses. (verify whether the VIES check runs sync or async)
- No documented cap on the number of saved addresses. (verify)

## JavaScript behaviour

- The list injects an inline script (rendered per `$type`, so each list type has its own bindings) that:
  - Binds `cc.user.address.setDefault` → reload the matching `.js-address-{type}-holder`.
  - Binds `cc.user.address.removed` → same reload.
  - Binds `submit.user.address.edited` on forms inside `.js-checkout-{type}-address-holder` → on `cc.ajax.success`, reload the list.
- AJAX panels: the "edit" and "add" links carry `data-ajax-panel="true"` and `data-panel-class="js-checkout-{type}-address-holder"`, so the panel framework swaps in the form without a full navigation.
- The form is wrapped by `js-form-submit-ajax-new` (same convention as login/register). `js-error-<field>` containers show per-field validation errors.
- Phone input runs `js-phone-intl` (international-telephone-input) and feeds the formatted number into the submission.
- With a Google Maps key, the autocomplete listens on `[data-google-place]` and writes the hidden `data-google-place-*` inputs. With no key, the customer gets free-text city/state plus the country dropdown only.
- The Google Maps **address picker** (map module) appears on shipping but is suppressed for billing via `force_hide_map=true` when included from the register page; the standalone billing form has its own behaviour. (verify exact flag wiring)

## Customisations available to the merchant

- `checkout_hide_billing_address` — when on, the billing list link is removed from the sidebar ([[customer-account]]), but the routes still exist and the form still renders if reached directly.
- `checkout_hide_first_name` / `checkout_hide_last_name` — `required` / `optional` / `hidden` per field, applied the same here and on checkout.
- To trim the country list: for shipping, limit each shipping provider's enabled countries (see **shipping-providers**); for billing, limit tax zones (see [[settings-taxes]]).
- Provide a Google Maps API key to switch from manual entry to autocomplete + map picker (see [[apps-google-tags]] / **apps-maps** — verify which app holds the key).
- The address form partial can be overridden per-theme by shadowing it in a custom theme.

## Theme variations

- All themes use the shared global list and form templates. No theme ships a fork of the list, though a few restyle the card layout via CSS. (verify by grep)
- The account wrapper (sidebar + main column) is also fully shared.

## Known issues / by-design vs bug

- **By design**: setting a default just toggles a flag — past orders are not rewritten.
- **By design**: disabling one shipping provider doesn't remove a country from the shipping list if another provider still ships there (the list is a union across providers).
- **By design**: the billing country list comes from tax zones, not shipping providers. A merchant with shipping but no tax zones sees a very short billing country list.
- **By design**: removing the **default** address does not auto-promote another — the customer must click another card to flag it. (verify)
- **Known sharp edge**: the commented-out company radio in the form partial means new addresses can't be marked as company-addresses from this UI on most themes — VAT/company fields rely on data already on the address. Some custom themes re-enable the radio.
- **Limitation**: with no address cap, the checkout address-picker gets hard to use beyond ~20 entries. (verify with a heavy-user merchant)

## Related

- [[storefront-architecture]]
- [[storefront-known-issues]]
- [[customer-account]]
- [[customer-register]]
- [[checkout]]
- **settings-customers**
- [[customers]]
- **shipping-providers**
- [[settings-taxes]]
- [[apps-gdpr-address]]

## Open questions

- What does the `customer_addresses` middleware gate — just "logged in", or also a feature flag?
- Is the VAT (VIES) validation synchronous on save, or queued?
- What happens to in-flight orders referencing a removed address? (likely soft-delete preserves them; verify)
- Is there a configurable upper bound on address-book size per customer?
- Does any theme re-enable the company-toggle radios in `_form.tpl`?
