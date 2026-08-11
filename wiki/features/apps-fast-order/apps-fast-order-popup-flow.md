---
type: feature
nav_path: "Apps → Fast Order → Popup form & cart"
route_name: apps.fast_order.overview
route_path: /admin/apps/fast_order
aliases: ["Fast Order popup", "Fast Order form", "Fast Order panel", "Quick order popup", "Fast Order cart lifecycle"]
tags: [apps, others, conversion, checkout, conversion-rate]
plan_gates: ["checkout"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[apps-fast-order]]. See the hub for the other aspects (COD payment + customer + address, Pixel + meta-flag + countdown).

# Fast Order — popup form & cart lifecycle

## Purpose

This aspect covers what the customer actually sees and fills in when they click the **Fast Order** button — the popup form, its configurable required fields, button labels, intro text, and GDPR consent — plus the **ephemeral cart** the platform creates behind the scenes and force-deletes on success. The payment side is on [[apps-fast-order-payment-cod]]; tracking is on [[apps-fast-order-tracking]].

## Where to find it

The button renders on the storefront product detail page once **Fast Order** is installed and active (Sidebar → Apps → Fast Order). The required-field toggles and button titles are edited on [[apps-fast-order-settings]].

## What the merchant can do here

- Set the storefront button label and the in-popup confirm-button label.
- Choose which of phone / first name / last name the customer must fill in.
- Add a custom rich-text intro shown at the top of the popup.

## Settings & fields

### Configurable fields in the popup

The merchant configures WHICH fields appear via per-field toggles:
- **Email** — ALWAYS required (not toggleable — appears regardless).
- **Phone** — toggle `require_phone`.
- **First name** — toggle `require_first_name`.
- **Last name** — toggle `require_last_name`.

Address is NOT collected on the fast-order popup itself — the order is placed with minimum customer details (email + phone + name); the shipping address is built downstream from geolocation (see [[apps-fast-order-payment-cod]]).

### Required button titles

When the app is active, both `button_title` and `finish_button_title` are required. The `button_title` is the storefront button label; `finish_button_title` is the "Confirm order" button inside the popup.

### Button titles are single-string fields — no per-language variants

`button_title` and `finish_button_title` are stored as single strings. The settings page does not expose a per-language editor or a translation-key picker — whatever the merchant types is shown verbatim on every storefront language. Multi-language stores that want translated labels must pick one neutral phrase or rely on the default localised fallback (`fast_order.info.title`) when leaving `button_title` empty.

### Custom description text in the popup

The merchant can set `fast_order_description` (rich text editor) — shown to the customer at the top of the popup explaining what "Quick order" is.

## Business rules

### Single-form bypass

The customer fills minimal fields (email + optionally phone / first name / last name) and submits. The platform creates an order with Pending status, COD payment, and a configured-default or geolocation-derived shipping side. No account creation is required (guest checkout).

### GDPR consent integration

The Fast Order panel includes the same GDPR consent block (form key `submit_payment`) and terms-of-service acceptance as the regular checkout — see [[apps-gdpr-overview]]. Fast Order does NOT skip consent capture.

### No built-in CAPTCHA / rate-limit / IP-throttle

The Fast Order create-order endpoint validates the form (email required; phone / first_name / last_name conditionally required; GDPR terms accepted; customer-not-banned; cart price within `checkout_min_price` / `checkout_max_price`) and runs the banned-customer check, but there is NO CAPTCHA, reCAPTCHA, rate limit, or per-IP throttle on the panel-open or order-submit endpoints. Merchants in spam-prone niches should add upstream protection (Cloudflare / WAF) themselves.

### Quantity IS customer-configurable — passed in from the product page

The Add-to-cart request that opens the panel carries a `quantity` value from the product page. Customers can use the product page's quantity selector before clicking the Fast Order button; the panel forwards that quantity into the order. The platform enforces `cart_max_products` / `cart_max_quantity` storewide caps from [[settings-cart]] (rejecting with *"More than X items not allowed in cart"* when exceeded). Fast Order is NOT hard-coded to qty = 1.

### Cart created on panel OPEN, force-deleted on order success

The flow:
1. Customer clicks the Fast Order button → the panel-open step creates an **ephemeral cart** in the database (random MD5 key) with the selected product / variant + quantity + options.
2. The panel step loads the cart and shows the form.
3. On submit, the save-order step runs in a 4-retry-attempt transaction that:
   - Validates min / max cart price (see [[apps-fast-order-payment-cod]]).
   - Force-sets the payment provider to COD.
   - Disables countdown discounts for the cart (see [[apps-fast-order-tracking]]).
   - Creates the order, then **force-deletes** the temporary cart row.

If the customer abandons mid-flow, the cart row stays in the DB until cleaned up by housekeeping. Multiple panel-opens by the same visitor create separate cart rows.

### Button hidden below the cart minimum price

The button itself is hidden on product pages where the product's price-to-input is below `checkout_min_price` (from [[settings-cart]]). The full min / max enforcement on submit is documented on [[apps-fast-order-payment-cod]].

## Related

- [[apps-fast-order]] — hub.
- [[apps-fast-order-settings]] — settings tab where these fields are edited.
- [[apps-gdpr-overview]] — the shared GDPR consent block (`submit_payment`).
- [[settings-cart]] — `checkout_min_price`, `cart_max_products` / `cart_max_quantity` caps.

## Open questions

None.
