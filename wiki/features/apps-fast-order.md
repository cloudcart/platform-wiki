---
type: feature
nav_path: "Apps → Fast Order"
route_name: apps.fast_order.overview
route_path: /admin/apps/fast_order
aliases: ["Fast Order", "Quick Order", "One-click order", "Бърза поръчка"]
tags: [apps, others, conversion, checkout, conversion-rate]
plan_gates: ["checkout"]
created: 2026-05-22
updated: 2026-06-10
source_count: 5
---
# Fast Order (one-click order button)

## Purpose

**Fast Order** integration — adds a **"Fast Order" button** to the storefront product detail page. The button replaces the standard cart-add → checkout flow with a streamlined **single-form, single-click order**: the customer fills a short popup (email + optionally phone + name) and submits. The full checkout is skipped entirely.

Used by merchants who:
- Sell to customers who don't trust full e-commerce checkouts (cash-on-delivery culture in Bulgaria / Romania / Balkans).
- Want to reduce abandoned cart rate by removing checkout friction.
- Run impulse-purchase categories (1-product carts typical).

The merchant configures the button title and a few popup options; the underlying flow is otherwise platform-defined. This page is the **hub** — the mechanics are split across three aspect sub-pages (see below).

## Where to find it

Sidebar → Apps → install → **Fast Order**. The configuration tab is documented on [[apps-fast-order-settings]].

## What the merchant can do here

- Configure the storefront button title and the in-popup confirm-button title.
- Choose which fields the popup requires (phone / first name / last name); email is always required.
- Add a custom rich-text description shown at the top of the popup.
- Pick which Facebook Pixel events fire for Fast Order (see [[apps-fast-order-tracking]]).
- Activate / deactivate the app.

### What the merchant CANNOT do here
- Use Fast Order with online payment providers — the flow is hard-coded to COD (see [[apps-fast-order-payment-cod]]).
- Collect a full street address in the popup — only a geolocation-derived address is stored (see [[apps-fast-order-payment-cod]]).
- Apply countdown discounts to a Fast Order cart — they are explicitly disabled (see [[apps-fast-order-tracking]]).
- Set per-language button titles — the titles are single-string fields (see [[apps-fast-order-popup-flow]]).

## Settings & fields

Configuration lives on the settings tab. The headline fields:
- `button_title` — storefront button label (required when active; default fallback `fast_order.info.title`).
- `finish_button_title` — the confirm-order button inside the popup (required when active).
- `require_phone` / `require_first_name` / `require_last_name` — per-field requirement toggles.
- `fast_order_description` — rich-text intro text shown at the top of the popup.
- Facebook Pixel start / complete event selectors.

Full field-by-field detail is on [[apps-fast-order-settings]]; the runtime form behaviour is on [[apps-fast-order-popup-flow]].

## Business rules

- **Single-form bypass.** The customer fills minimal fields and submits; the platform creates a COD order in the Pending state without forcing account creation (guest checkout). Mechanics on [[apps-fast-order-popup-flow]].
- **Strictly COD.** The order is force-set to the COD provider; if no active COD provider exists, the order is not created. Online providers (Stripe / PayPal / Borica) are never used. See [[apps-fast-order-payment-cod]].
- **Orders are flagged for filtering.** Every Fast Order gets `fast_order = true` in its meta, powering the **Fast order** filter on the [[orders]] list. See [[apps-fast-order-tracking]].
- **Plan-tier gate.** Submission requires the `checkout` plan feature — the same gate that blocks the main checkout. See [[apps-fast-order-payment-cod]].
- **Permission.** Standard apps permission scope.

## Sub-pages (in this cluster)

This feature is split into three aspect pages. Drill into the one that matches the question:

- [[apps-fast-order-popup-flow]] — the popup form (configurable required fields, button titles, description text, GDPR consent, no built-in CAPTCHA, quantity passthrough) and the ephemeral cart lifecycle (created on panel open, force-deleted on success).
- [[apps-fast-order-payment-cod]] — the COD-only payment path, full payment-gateway invocation, online-provider hard-block, plan gate, min/max cart price, guest-vs-existing customer creation, banned-customer block, and the geolocation-derived shipping address.
- [[apps-fast-order-tracking]] — Facebook Pixel event configuration, the `fast_order` meta flag + orders-list filter, and the explicit disabling of countdown discounts.

## Related

- [[apps]] — App Store.
- [[apps-fast-order-settings]] — settings sub-page.
- [[apps-fast-order-popup-flow]] — popup form + cart lifecycle aspect.
- [[apps-fast-order-payment-cod]] — COD payment + customer + address aspect.
- [[apps-fast-order-tracking]] — Pixel events + meta flag + countdown aspect.
- [[orders]] — Fast order filter on the list.
- [[settings-cart]] — cart settings interact with the flow (min/max price, quantity caps).
- [[settings-payment-providers]] — COD must be configured for Fast Order to work.

## Open questions

None — all previously-flagged questions resolved across the aspect pages.
