---
type: feature
nav_path: "Profile → Billing → Payment method → HTTPS & throttle"
route_name: admin.billing.card
route_path: /admin/billing/card
aliases: ["HTTPS prerequisite", "Insecure domain warning", "Card-add throttle", "3 attempts per 24 hours", "AJAX-only", "Service temporary disabled", "Too many card validations"]
tags: [billing, payment-method, https, ssl, throttle, rate-limit, prerequisites]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[billing-cards]]. See the hub for the other aspects (Stripe flow, Braintree flow, 3DS + security, replacement, renewal, display summary).

# Payment cards — HTTPS, throttle & access prerequisites

## Purpose

Before the merchant can open the gateway module at all, the **Payment method** panel enforces three gate conditions:

1. The store's primary domain must use **HTTPS** — otherwise the panel shows a warning and the module is never loaded.
2. The card-validation attempt count must be under the **3-attempts-per-24-hours** throttle — otherwise the platform refuses to even call the gateway.
3. The request must come in via AJAX from inside the admin — direct URL access returns 404.

This aspect documents all three gates and the merchant-visible messages each one produces.

## Where to find it

- The HTTPS warning is shown inside the `/admin/billing/card` panel itself, in place of the gateway module, via the `card/add_modal_warn.blade.php` template.
- The throttle error surfaces inline in the panel on save attempts.
- The AJAX-only behaviour is invisible — direct navigation to `/admin/billing/card` returns 404.

## What the merchant can do here

- Fix the HTTPS prerequisite by either switching the primary domain to the store's main `*.cloudcart.com` subdomain (HTTPS by default), or installing an SSL certificate via [[settings-domains]] / [[apps-lets-encrypt]] and then re-setting their custom domain as primary.
- Wait out the throttle window — the oldest of the 3 attempts must age past 24 hours before the next attempt is allowed.
- Re-open the panel from inside the admin (Profile dropdown → Billing → pencil icon) rather than via direct URL.

What the merchant **cannot** do here: bypass the HTTPS check, ask support to lift the throttle (it's a self-healing counter), or open the panel via direct URL (the AJAX guard blocks it).

## Settings & fields

There are no editable settings on this screen — the three gates are enforced unconditionally by the backend.

Verbatim insecure-domain warning text shown inside the panel when the primary domain is `http://`:

> *"Your primary domain `<primary_host>` uses insecure (http) connection! To manage your payment method the primary domain should use a secure (https) connection. You can switch to domain `<main_host>` or add SSL certificate from: Settings -> Domains"*

Verbatim throttle error shown when the merchant exceeds 3 card-validation attempts in 24 hours:

> *"Service temporary disabled. Too many card validations."*

## Business rules

### HTTPS on the primary domain is a hard block

When the merchant's store primary domain is `http://` (no SSL certificate), the panel refuses to load the gateway module entirely. Instead the `card/add_modal_warn.blade.php` template renders:

- Header — same localised *Payment provider* label as the gateway variants, but **no Save button**.
- Body — yellow `.alert-warning` box with the warning text quoted above. No `<div id="payment-element">`, no `<div id="dropin-container">`, no JS includes for either gateway.

The merchant cannot proceed — must fix HTTPS first. The same warning is also shown on the [[settings-domains]] / [[settings-general]] screens when the merchant tries to open the panel from there.

The backend route handler (`addCard`) picks `add_modal_warn.blade.php` based on the primary-domain HTTPS check — independent of which gateway the merchant is on (Stripe or Braintree) — see [[billing-cards-stripe-flow]] and [[billing-cards-braintree-flow]].

### Card-add throttle: 3 attempts per 24 hours, rolling window

The platform counts card-validation requests per merchant account in a 24-hour rolling window. After **3 attempts within 24 hours**, further attempts are blocked with the *"Service temporary disabled. Too many card validations."* error.

The throttle exists to protect against **automated card-testing** — a common fraud pattern where an attacker enumerates stolen cards through a victim site, using the site's verification endpoint to validate which cards are still live. The 3-per-24h limit makes the site useless as a card-testing vector.

A merchant who has legitimately hit this limit must wait until the oldest of their 3 attempts ages past 24 hours. There is no support override.

### Throttle counts EVERY attempt — success or failure

The `braintree_verify_card` usage counter is incremented **unconditionally** after the Braintree payment-method create call, **BEFORE** checking whether the response was successful. So a merchant who:

1. Successfully adds a card (counts as 1 attempt)
2. Replaces it with a new one (counts as 2 attempts)
3. Replaces it again (counts as 3 attempts)

is now at the limit — even though every single attempt succeeded. The throttle treats success and failure identically.

The usage-counter window is 24 hours for the throttle decision; the counter entries themselves expire from the usage log after 3 days.

### AJAX-only route access

If the merchant types `/admin/billing/card` directly into the browser address bar (a GET that is not an AJAX request), the platform returns **404**. The card panel is only reachable through the in-app links described in [[billing-cards]] — Profile dropdown → Billing, the pencil on [[billing-invoicing]], the [[subscriptions]] header, or the [[services]] purchase flow.

This is a defensive measure — a merchant who bookmarks or shares the URL gets a 404 rather than a stranded panel, and any link that leaks out (e.g. into an email) is non-functional.

### HTTPS prerequisite holds for the Vue Checkout variant too

The same HTTPS check applies to the inline `FormStripe.vue` / `FormPayments.vue` editors inside Checkout (see [[plans-purchase]]). A merchant on an `http://` primary domain cannot register a card from Checkout either — the same warning is shown in place of the inline form.

## Related

- [[billing-cards]] — hub.
- [[settings-domains]] — where the merchant installs SSL and switches the primary domain.
- [[apps-lets-encrypt]] — the free SSL app most merchants use to unblock HTTPS.
- [[billing-cards-stripe-flow]] — gateway loaded when HTTPS is OK.
- [[billing-cards-braintree-flow]] — gateway loaded when HTTPS is OK.
- [[billing-cards-replacement-and-deletion]] — context for why merchants often hit the throttle (replace, replace, replace).

## Open questions

None.
