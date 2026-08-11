---
type: storefront-page
route_name: checkout.return
route_path: /checkout/return/{status}/{payment_hash}
themes_using: [all]
tags: [storefront, checkout, payment, return, thank-you, conversion]
created: 2026-06-08
updated: 2026-06-10
source_count: 6
---

# Checkout return page

## Purpose

The page customers land on after returning from an off-site payment gateway (Stripe Checkout, PayPal, Borica, iCard, ePay, etc.). This page **interprets the gateway's outcome** — `{status}` ∈ {`completed`, `cancelled`, `failed`, `timeouted`, `requested`, `pending`, `held`, `voided`, `chargebacked`, `refunded`} — renders the appropriate message, completes the cart-to-order transition (cleanup + email + tracking), and either becomes the thank-you page or bounces back to `/checkout` so the customer can retry.

Two facts make this page disproportionately important, and both have their own aspect page:

- It is the **only** place the platform's transactional emails fire for orders that went through a gateway — the checkout page itself sends none. See [[checkout-return-emails-tracking]].
- It is the **only** place the `Purchase` analytics event fires for off-site-redirect gateways, so anything broken here breaks the merchant's ad-attribution numbers. Also [[checkout-return-emails-tracking]].

Because the page covers distinct concerns — routing/cleanup, emails/tracking, and the status-driven message — the detail is split into three aspect pages. Drill into the one that matches the question rather than reading all three.

## Sub-pages (in this cluster)

- [[checkout-return-load-flow]] — the `/checkout/return/*` route, the gateway-facing `/payment/*` endpoints, the server-side load sequence, the per-user cart cleanup, the cancel-branch redirect, and the custom thank-you-page override.
- [[checkout-return-emails-tracking]] — the transactional-email cascade with its `email_sent == 'no'` idempotency guard + retry-5, the `google_analitycs_tracking` flag, and the `Purchase` / Yotpo / AdScout conversion-tracking pixels.
- [[checkout-return-status-display]] — the per-status title + body messages, the order-details receipt block, the UBB receipt header, and the overloaded `requested` status copy.

## URL & route

- **Route name**: `checkout.return`. **Route path**: `/checkout/return/{status}/{payment_hash}` (GET, inherits `XSS` + `cart_checkout`).
- **`{status}`** — short-string from the gateway adapter, mapped to an order-payment status constant.
- **`{payment_hash}`** — secure hash identifying the order-payment row; the only authentication for this page.
- Distinct gateway-facing endpoints — `/payment/return/{paymentId}`, `/payment/webhook/{paymentId}`, `/payment/cancel/{paymentId}` — are catalogued on [[checkout-return-load-flow]].

## How it loads

At a high level: crawler guard (404 for bots) → look up the order-payment by hash → register it for the pixel modules → on non-cancel, clear the draft flag and delete the user's carts → fire emails + set the tracking flag → optionally redirect to a custom thank-you page → render `return.tpl`. The full step-by-step sequence (and the cancel branch that redirects away) is on [[checkout-return-load-flow]].

## What the customer sees

A status-driven title + body (thank-you / failure / pending / refunded / processing), then the order-details receipt block (number, line items, totals, addresses, payment + shipping method, "Track shipment" link), plus provider extras like the UBB receipt header. The complete per-status copy table is on [[checkout-return-status-display]].

## Storefront behaviour

Refresh-resistant (no re-charge, no duplicate email); cart deletion is per-user (wipes carts on other devices too); a configured custom thank-you page bypasses this template entirely; the GA tracking flag is set on first non-cancel render. The cleanup/redirect details are on [[checkout-return-load-flow]]; the email + pixel idempotency is on [[checkout-return-emails-tracking]].

## JavaScript behaviour

Mostly server-rendered inside the standard storefront layout (`the shared layout include` / `layout.footer`). A conditionally-loaded Braintree dropin script may persist from checkout (see [[checkout-return-status-display]]); the conversion pixels and the AdScout `$(document).ready(function { window.AdScout.clearStorage(window.AdScout.storageDB, true); })` reset are on [[checkout-return-emails-tracking]]. The page has no cart drawer / header bubble / add-to-cart UI — by design.

## Customisations available to the merchant

- **Custom thank-you page** — set a Page Builder page as the "Thank you" system page to bypass this template — see [[checkout-return-load-flow]].
- **Per-status copy** — `sf.checkout.header.status_*` / `sf.checkout.succ.status_*` / `sf.checkout.err.status_*` are translatable — see [[checkout-return-status-display]].
- **Yotpo / AdScout / Membership** — installable apps that inject conversion tracking or receipt extras — see [[checkout-return-emails-tracking]].

The page **does not** have its own Theme Editor module — its layout is hard-coded in `return.tpl`.

## Theme variations

The return template and the order-details fragment (`return/order/details.tpl`) are **rarely overridden** per theme — most themes inherit them verbatim. Post-purchase customisation usually goes through the Page Builder "Thank you" custom page instead. More detail on [[checkout-return-status-display]].

## Known issues / by-design vs bug

- **The page is the email-trigger, not the checkout-submit handler** — customers who never return may get the email only via webhook — see [[checkout-return-emails-tracking]].
- **Webhook vs return-URL race** — the webhook can arrive before the browser returns; the page still renders correctly because it reads live status — see [[checkout-return-load-flow]].
- **Cart deletion is broad** — wipes all carts of the user, even on other devices — see [[checkout-return-load-flow]].
- **`google_analitycs_tracking` meta-key typo** — the stored key is misspelled; don't "fix" it without a migration — see [[checkout-return-emails-tracking]].
- **Cancel branch redirects, doesn't render the cancel template** — the `cancelled` template branch is mostly dead code (verify) — see [[checkout-return-load-flow]].
- **Crawler 404** — by design.

## Related

- [[storefront-architecture]] — request lifecycle, no-cache headers, layout inclusion.
- [[checkout]] — the page customers come from before being sent off to the gateway.
- [[checkout-complete]] — the alternative "thank you" landing (in-page-tokenizing gateways skip the return URL).
- [[cart-vs-order-lifecycle]] — Order-status transition on return.
- [[order-processing-pipeline]] — what fires server-side after the order is placed.
- [[order-status-workflow]] — the order state machine; this page transitions to `pending` then to `paid` / `completed` / `failed`.
- [[payment-provider-mechanism]] — how each provider's return URL is constructed.
- [[notification-delivery]] — how the new-order / completed-order emails are queued.
- [[abandoned-cart-recovery]] — what happens if the customer never reaches this page.
- [[storefront-known-issues]] — cross-page bugs.

## Open questions

- The full list of per-provider status mappings (which gateway statuses map to which order-payment status) isn't documented in one place. (verify per provider — see [[checkout-return-status-display]])
- Whether the `cancel` branch of the template ever actually renders. (verify — see [[checkout-return-load-flow]])
- Whether the `Purchase` analytics pixel is fully deduplicated when both the webhook and the return URL fire. (verify — see [[checkout-return-emails-tracking]])
- Whether the `payment_hash` is rotated after first use, or remains valid forever. (verify — see [[checkout-return-load-flow]])
