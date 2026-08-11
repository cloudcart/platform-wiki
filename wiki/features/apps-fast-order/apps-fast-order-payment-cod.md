---
type: feature
nav_path: "Apps → Fast Order → COD payment & customer"
route_name: apps.fast_order.overview
route_path: /admin/apps/fast_order
aliases: ["Fast Order COD", "Fast Order payment", "Fast Order customer creation", "Fast Order shipping address", "Fast Order plan gate"]
tags: [apps, others, conversion, checkout, conversion-rate]
plan_gates: ["checkout"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

> Part of [[apps-fast-order]]. See the hub for the other aspects (popup form + cart lifecycle, Pixel + meta-flag + countdown).

# Fast Order — COD payment, customer & address

## Purpose

This aspect covers everything that happens on **order submission**: the strict cash-on-delivery payment path, the hard block on online providers, the plan-tier gate, the min / max cart-price enforcement, how the customer record is matched or created, the banned-customer block, and how the shipping address is built from geolocation rather than collected in the popup. The form itself is on [[apps-fast-order-popup-flow]]; tracking is on [[apps-fast-order-tracking]].

## Where to find it

There is no separate screen for this logic — it runs server-side when a customer submits the Fast Order popup on the storefront. The COD provider is configured on [[settings-payment-providers]]; price limits on [[settings-cart]].

## What the merchant can do here

- Configure an active COD payment provider (required — otherwise Fast Order silently fails).
- Set the store-wide `checkout_min_price` / `checkout_max_price` that gate Fast Order submissions.
- Turn on `require_first_name` / `require_last_name` (on [[apps-fast-order-settings]]) when real names are needed for fulfillment.

## Settings & fields

- COD payment provider — must exist and be active in [[settings-payment-providers]].
- `checkout_min_price` / `checkout_max_price` — store-wide cart-price bounds from [[settings-cart]], both enforced on submit.

## Business rules

### Strictly COD — no online-payment support

The order is force-set to the COD payment provider. If COD isn't configured / active, the order doesn't get created. The merchant CANNOT use Fast Order with Stripe / PayPal / other online providers — the flow is hard-coded to COD. If the store has no active COD payment provider configured in [[settings-payment-providers]], Fast Order won't work.

### Payment flow: COD with full payment-gateway invocation

Even though the payment is COD, the platform still:
1. Creates a payment record from the gateway request.
2. Invokes the COD payment gateway's `purchase` step — COD's gateway just marks the payment as pending / manual.
3. Stores the payment_id + status from the gateway response.
4. Fires the `OrderCreated` event (which triggers downstream listeners: AdScout tracking, ERP push, email notifications, etc.).

If the COD gateway throws an exception, the order is auto-CANCELLED with the exception message stored in `note_administrator`. The merchant sees these failures in the [[orders]] list.

### Stripe / PayPal / other online providers — hard-blocked

The submission specifically queries for the active `cod` provider only. Even if the merchant has Stripe / PayPal / Borica activated, Fast Order won't use them. If COD isn't configured, the save-order step returns null silently — the customer sees the success-but-failed view.

### Plan-tier gate: `checkout` feature must be enabled

The Fast Order checkout controller requires the `checkout` plan feature. If the merchant's plan has checkout disabled (rare — typically a frozen / suspended account), opening the Fast Order panel throws an error *"Checkout disabled"*. This is the same gate that blocks the main checkout, so Fast Order is effectively unavailable whenever the regular checkout is.

### Cart minimum / maximum price enforced

Both `checkout_min_price` and `checkout_max_price` (from [[settings-cart]]) are enforced — fast orders below min or above max throw an error. The button is also hidden on product pages where the product price is below `checkout_min_price` (see [[apps-fast-order-popup-flow]]).

### Existing customer detection by email

When the form submits:
1. The platform looks up a customer by the entered email first.
2. If a customer exists, the order attaches to that customer (regardless of whether the user is logged in or not).
3. If no customer exists, a guest customer is created with the form data, falling back to `first_name = 'anonymous'` / `last_name = 'anonymous'` when those fields aren't required-on.

The guest customer is created BEFORE the order — so even an order that fails validation will leave behind a guest customer row.

### Required-field defaults: name fallback is "anonymous"

When the merchant has the `require_first_name` / `require_last_name` toggles OFF and the customer doesn't fill them in, the platform stores `first_name = 'anonymous'` and `last_name = 'anonymous'` on the new guest customer. This creates a pile of "anonymous anonymous" customers in [[customers]] for stores that only require email + phone. The merchant should turn ON these toggles if they need real names for fulfillment.

### Banned-customer block runs AFTER customer lookup

If the matched customer has `banned = true`, an error is thrown with the ban reason and date — Fast Order does NOT bypass the banned-customer protection. This check runs **after** the customer is found / created by email, so a guest customer created on the spot can't be banned (banned = false by default); only matched existing customers trigger this check. The error message includes the ban reason and date for transparency.

### Shipping address is built from geolocation, not collected in the form

The Fast Order popup itself only captures email + (optional) phone + (optional) first / last name. No street address, city, or postcode fields. On submit, the platform creates a shipping address using MaxMind GeoIP data:
- `country_iso2` + `country_name` from the visitor's IP country.
- `post_code` from the GeoIP postal lookup (when available).
- `latitude` + `longitude` from the GeoIP location (when available).
- `phone` from the form.
- `first_name` / `last_name` from the matched / created customer.

There is NO street / house-number / city captured up-front — the courier's pickup or delivery flow downstream is expected to capture the precise address (e.g., the courier calls the customer on the phone number provided, or COD-on-delivery confirms address at handover). Merchants using couriers that require a complete address before pickup (Econt, DPD Bulgaria, etc.) should NOT rely on Fast Order alone — the order will be created with only a country + post-code + lat / lng address.

## Related

- [[apps-fast-order]] — hub.
- [[apps-fast-order-settings]] — required-field toggles that drive the "anonymous" fallback.
- [[settings-payment-providers]] — COD provider must be active.
- [[settings-cart]] — `checkout_min_price` / `checkout_max_price`.
- [[customers]] — where guest / matched customers land.
- [[orders]] — auto-cancelled orders show here with the failure note.

## Open questions

None.
