---
type: storefront-page
route_name: checkout.return
route_path: /checkout/return/{status}/{payment_hash}
themes_using: [all]
tags: [storefront, checkout, payment, return, thank-you, order-details]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[checkout-return]]. See the hub for the other aspects (load flow & routing, emails & conversion tracking).

# Checkout return — status-driven display & order details

## Purpose

What the customer actually reads on the return page: the per-status title + body message (success, failure, pending, refunded, etc.), the order-details receipt block, and the provider-specific extras (UBB receipt header, bank-transfer instructions). This aspect answers "why does my customer see 'we're processing your payment' instead of 'thank you'?", "where do bank-transfer payment instructions show?", and "what's in the order summary on the thank-you page?". The server load sequence that picks the template is on [[checkout-return-load-flow]]; the emails and pixels that fire alongside are on [[checkout-return-emails-tracking]].

## URL & route

Same route as the cluster — `checkout.return` — `/checkout/return/{status}/{payment_hash}` (GET, inherits `XSS` + `cart_checkout`). The `{status}` path segment is what drives every message branch on this page; the template the theme templates switches on it. The order-details fragment is the shared the theme templates.

## How it loads

By the time this template renders, the load flow ([[checkout-return-load-flow]]) has already resolved the order-payment, run cart cleanup, and fired emails/tracking ([[checkout-return-emails-tracking]]). The template's only job is presentation: it reads the order-payment's current status, selects the matching title + body translation keys, and renders the order-details fragment beneath. The status it switches on is the **current** order-payment status (which may already be `completed` if a webhook beat the customer's browser back).

## What the customer sees

Status-driven message (verified in `_global/templates/checkout/return.tpl`):

- **`completed`** — Title `sf.checkout.header.status_completed`, body `sf.checkout.succ.status_completed`. If the order has digital files → link to `site.account.files`. If digital `page`-type → link to `site.account.pages`.
- **`cancelled`** — Title `sf.checkout.header.status_cancelled`, body `sf.checkout.err.status_cancelled`. (Note: cancel status normally redirects back to `/checkout` before this template renders — see [[checkout-return-load-flow]]; this branch is for explicit cancel-status-arrived-here cases.)
- **`failed`** — Title `sf.checkout.header.status_failed`, body `sf.checkout.err.status_failed`.
- **`timeouted`** — Title `sf.checkout.header.status_timeouted`, body `sf.checkout.err.status_timeouted`.
- **`requested`** — For providers NOT in {`cod`, `bwt`} and not leasing: "We're processing your digital payment" (the payment is queued for processing — typical for some bank-transfer adapters). For `cod` / `bwt` / leasing: standard "Thank you" with the provider's configuration HTML (e.g. bank-transfer details).
- **`pending`** — "Thank you" + body `sf.checkout.succ.status_pending`.
- **`held`** — Title `sf.checkout.header.status_held`, body `sf.checkout.err.status_held`.
- **`voided`** — Title `sf.checkout.header.status_voided`, body `sf.checkout.err.status_voided`.
- **`chargebacked`** — Title `sf.checkout.header.status_chargebacked`, body `sf.checkout.succ.status_chargebacked`.
- **`refunded`** — Title `sf.checkout.header.status_refunded`, body `sf.checkout.succ.status_refunded`.

Below the status message:

- **UBB-specific block** — when `status === 'completed'` AND `provider === 'ubb'`, an additional `order_info.tpl` block from the UBB integration is rendered (UBB requires displaying the receipt header).
- **Order details block** — the theme templates — full order summary: number, date, line items, totals, shipping address, billing address, payment method, shipping method, "Track shipment" link (using the `TRACK17` constant for the 17track URL pattern). Digital-file download links and Membership page-access expiry (attached during the load flow) surface here too.

## Storefront behaviour

- **Status is read live** — the message reflects the order-payment's current status at render time, so even if a webhook flipped the order to `completed` before the browser returned, the correct "thank you" copy renders.
- **The `requested` status is overloaded** — same status, two completely different messages depending on provider (happy thank-you for `cod`/`bwt`/leasing vs "processing your digital payment" for everything else).
- **Digital products** — the `completed` branch adds account links to files / pages; the details block also renders the download links for digital items.
- **No add-to-cart UI** — the page does NOT include the cart drawer, header bubble, or any add-to-cart UI; by design, the customer has just completed their purchase.

## JavaScript behaviour

This page is mostly server-rendered, with limited interactive JS:

- **Braintree dropin script** — `<script src="https://js.braintreegateway.com/web/dropin/1.37.0/js/dropin.min.js">` is conditionally loaded (set up at checkout, persists to return). Not used on the return page itself unless the gateway didn't tokenize earlier.
- **Standard layout JS** — the page renders inside the regular storefront layout (`the shared layout include` and `layout.footer`), so the theme's nav / footer / cookie-banner JS runs as usual.

The conversion-pixel and Yotpo / AdScout JS that also run on this page are documented on [[checkout-return-emails-tracking]].

## Customisations available to the merchant

- **Per-status copy** — translations for `sf.checkout.header.status_*` and `sf.checkout.succ.status_*` / `sf.checkout.err.status_*` are translatable (admin → Languages). This is how a merchant rewords any of the status messages above.
- **Bank-transfer / COD instructions** — the provider configuration HTML rendered in the `requested`/thank-you branch for `bwt` / `cod` is edited in that payment provider's settings.
- **Custom thank-you page** — when a custom system page is configured this template is bypassed entirely (see [[checkout-return-load-flow]]); the merchant designs the full receipt experience in the Page Builder instead.

The page **does not** have its own Theme Editor module — its layout is hard-coded in `_global/templates/checkout/return.tpl`.

## Theme variations

- The return template lives in the theme templates and is **rarely overridden** per theme. Most themes inherit the global template verbatim.
- The order-details fragment (`return/order/details.tpl`) is also shared across themes.
- Themes that customise the post-purchase experience usually do so via the Page Builder "Thank you" custom page (which bypasses this template).

## Known issues / by-design vs bug

- **The `requested` status overload** — for `cod` / `bwt` / leasing this is the "happy thank you" branch; for everything else it's the "processing your digital payment" branch. Same status, different copy. By design but confusing.
- **Cancel branch is mostly dead code** — when `{status}` === `cancel` the load flow redirects away before this template renders (see [[checkout-return-load-flow]]), so the `cancelled` branch of the template rarely renders in practice (verify).
- **Webhook-beat-browser** — when the webhook flips the order to `completed` before the browser returns, the message still renders correctly because it reads the live status (not the `{status}` URL segment as the sole source of truth).

## Related

- [[checkout-return]] — hub.
- [[storefront-architecture]] — request lifecycle, no-cache headers, layout inclusion.
- [[checkout-complete]] — the alternative "thank you" landing (in-page-tokenizing gateways skip the return URL).
- [[order-status-workflow]] — the order state machine behind the status the message reflects.
- [[orders-details]] — the admin-side order detail; the same order summary the customer sees in miniature here.
- [[shipping-provider-mechanism]] — how the "Track shipment" 17track link is built.
- [[storefront-known-issues]] — cross-page bugs.

## Open questions

- The full list of per-provider status mappings (which gateway statuses map to which displayed message) isn't documented in one place. (verify per provider)
- Whether the `cancelled` branch of the template ever actually renders, or whether the redirect short-circuit catches all cases. (verify — see [[checkout-return-load-flow]])
