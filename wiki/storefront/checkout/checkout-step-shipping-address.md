---
type: storefront-page
nav_path: "Storefront → Checkout → Shipping → To address"
route_name: checkout.shipping.address
route_path: /checkout/shipping-address
themes_using: [all]
aliases: ["Checkout to-address", "Checkout address form", "Saved shipping address list", "Add new shipping address inline", "Доставка до адрес"]
tags: [storefront, checkout, shipping, address, customer-address]
plan_gates: []
created: 2026-06-12
updated: 2026-06-12
source_count: 3
---

> Part of [[checkout]]. See [[checkout-step-shipping]] for the channel picker and the sibling channels [[checkout-step-shipping-pickup]].

# Checkout — Shipping to address

## Purpose

The "to address" channel — the courier delivers the order to a typed customer address. This page documents the **address-selection UX** the customer sees: when they have saved addresses they pick one; when they don't they fill in a new address form inline.

## URL & route

See `route_name` and `route_path` in frontmatter. This is a sub-section of [[checkout]] — the parent `/checkout` page hosts these step containers; container reload routes are listed under "Where to find it".

## How it loads

Loaded as a sub-region of the `/checkout` page (see [[checkout-page-routing]] for the parent route + middleware stack). On step transitions, the container is GET-reloaded via its `data-ajax-box` URL — see [[checkout-flow-storefront-backend-bridge]] for the full reload-fragment map.

## Where to find it

Inside the shipping-type accordion (see [[checkout-step-shipping]]) when the customer picks the **address** radio. DOM container: `<div class="js-checkout-shipping-address-holder">`.

## What the customer sees — two states

The template (`shipping-address/address.tpl`) branches on `$addresses->count`:

### State A — Customer has saved addresses (`$addresses->count > 0`)

A nested accordion of address cards, each:

- **Radio button** with the formatted address text (`$a->format(false)` — the multi-line "Name, Phone, City, Street, Country" stamp).
- **Pencil edit icon** — opens the saved address in an ajax side panel (route `site.account.address.shipping.edit`) where the customer can change it without leaving checkout. See [[customers-details-shipping-addresses]] for the panel.
- The default address is auto-selected (`$cc_cart->customer->default_address_id`).

A final accordion row reads **"+ Add new address"** — opens the create form in the same ajax side panel (route `site.account.address.shipping.create`).

### State B — Customer has no saved addresses (guest OR registered with no address)

The full address form renders inline. The form template is the canonical `customer/address/_form.tpl` shared with [[customers-details-shipping-addresses]]; the input prefix is `checkout[shipping][address]` so all field names nest under that key on submit.

Field set + visibility per `checkout_hide_*` settings (from [[settings-cart]]):

| Field | Required by default | Settings key |
|---|---|---|
| First name | yes | `checkout_hide_first_name` |
| Last name | yes | `checkout_hide_last_name` |
| Email (guest only) | yes | (always shown when guest) |
| Phone | yes | `checkout_hide_phone` |
| Country | yes | (always shown) |
| State / region | depends | (driven by selected country) |
| City | yes | (typeahead) |
| Post code | depends | `checkout_hide_post_code` |
| Street + number | yes | `checkout_hide_address_line1` / `_line2` |
| Floor + apartment | optional | (extra address fields) |
| Custom fields (`type=shipping`) | per-field | [[customers-custom-fields]] |

Each `checkout_hide_*` setting takes one of three values: `hidden` (field removed), `optional` (rendered but not required), or `required` (rendered + required). Default for missing keys is `required`.

### Google Maps integration

When a Google Maps API key is configured (`hasGoogleMapKey` returns true) AND the `checkout_hide_address_map` setting is not set:

- An interactive map appears alongside the city + street fields.
- The address-autocomplete writes back country / region / city / lat / lng to the form fields.
- A "localize me" affordance lets the customer pin their current location.

When NO Maps key OR `checkout_hide_address_map = yes`:

- Only the input fields are rendered — no map, no place autocomplete.
- The country / region / city pickers use CloudCart's static dataset (the same backing data as the rest of the platform — see [[geo-targeting-address-resolution]]).
- City is a typeahead-search box backed by the city dataset; the customer types and picks.

## Settings & fields

| Setting key | Where set | Effect on this step |
|---|---|---|
| `checkout_hide_first_name` / `_last_name` / `_phone` / `_post_code` | [[settings-cart]] | `hidden` / `optional` / `required` per field. |
| `checkout_hide_address_map` | [[settings-cart]] | Hides the Google Map even when the API key is set. |
| `checkout_hide_billing_address` / `checkout_require_billing_address` | [[settings-cart]] | Controls the billing-address checkbox below the address (see [[checkout-step-shipping]]). |
| `default_country` | [[settings-general]] | Default country in the country picker. |
| Custom fields (type `shipping`) | [[customers-custom-fields]] | Adds extra fields to the form. |

## Business rules

- **Address selection writes to the cart immediately on submit.** The form POSTs to `checkout.shipping.address.save`; the controller binds the chosen address (or saves the new one) to `cart.customer_shipping_address_id` and advances the step machine.
- **Auto-heal of geo fields on save.** Addresses save through the `HealMissingGeo` trait — see [[customers-details-shipping-addresses|customer-shipping-address-save-hooks]]. So even a manually-typed address without map interaction gets a lat / lng backfilled if Geonames can resolve it.
- **Editing a saved address opens a side panel, NOT inline edit.** The customer's edit interactions don't disrupt the checkout DOM; on save the address card refreshes via ajax and the customer continues.
- **Guest customers without a saved address see ONLY the form** — no "saved addresses" list. The form fields render directly inside `js-checkout-shipping-address-holder`.
- **Country/state/city dependency.** Changing the country re-fetches the region picker; changing the region re-fetches the city typeahead. JS event `cc.place.change` may fire on each — see [[checkout-page-javascript]].

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

- [[checkout-step-shipping]] — the parent (channel picker).
- [[checkout-step-shipping-pickup]] — sibling: office + locker channels.
- [[customers-details-shipping-addresses]] — the saved-addresses entity + the ajax side panel for edit/create.
- [[customer-shipping-address-save-hooks]] — geo auto-heal on save.
- [[customer-shipping-address-validation]] — server-side validation rules the form must pass.
- [[customer-shipping-address-google-maps]] — Google Maps autocomplete configuration.
- [[settings-cart]] — `checkout_hide_*` settings catalogue.
- [[settings-general]] — `default_country`.
- [[customers-custom-fields]] — custom fields on the shipping form.
- [[geo-targeting-address-resolution]] — static country / region / city dataset behind the pickers when no Maps.

## Open questions

- Whether the `cc.place.change` JS event fires on every level (country → state → city) or only on the leaf-most change. (verify)
