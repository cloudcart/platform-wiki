---
type: storefront-page
route_name: checkout.return
route_path: /checkout/return/{status}/{payment_hash}
themes_using: [all]
tags: [storefront, checkout, payment, return, cart-cleanup, draft-order]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[checkout-return]]. See the hub for the other aspects (status-driven display, emails & conversion tracking).

# Checkout return — load flow, routing & cart cleanup

## Purpose

The server-side mechanics of the page customers land on after returning from an off-site payment gateway (Stripe Checkout, PayPal, Borica, iCard, ePay, etc.): how the request is routed, how the order-payment is looked up by hash, what cart cleanup runs, how the cancel branch redirects, and how a merchant's custom thank-you page overrides the generic template. It answers "what URL does the gateway send the customer back to?", "why did my cart disappear from other devices?", and "why was I bounced back to `/checkout` after cancelling?". The status-driven message is on [[checkout-return-status-display]]; the email + analytics side-effects are on [[checkout-return-emails-tracking]].

## URL & route

- **Route name**: `checkout.return`.
- **Route path**: `/checkout/return/{status}/{payment_hash}`.
- **Method**: GET.
- **Middleware**: inherits `XSS` and `cart_checkout` from the parent `/checkout/*` group.
- **`{status}`** — short-string from the gateway adapter, mapped to one of the order-payment status constants (`completed`, `cancelled`, `failed`, `timeouted`, `requested`, `pending`, `held`, `voided`, `chargebacked`, `refunded`, plus the special `cancel`).
- **`{payment_hash}`** — a secure hash that identifies the order-payment row. The hash is **the only authentication for this page** — anyone with the link sees the page; in practice it's used by the customer's browser only.

Distinct gateway-facing endpoints (not the customer-facing page):

- **`/payment/return/{paymentId}`** — `site.payment.return` — the server-side return-from-gateway endpoint that verifies the gateway response and forwards the customer here. This is the route gateway URLs are configured with.
- **`/payment/webhook/{paymentId}`** — `site.payment.webhook` — the server-to-server confirmation endpoint. Webhooks may arrive **before or after** the browser returns; final state depends on whichever fires first plus reconciliation.
- **`/payment/cancel/{paymentId}`** — `site.payment.cancel` — for some providers, an explicit cancel-URL.

## How it loads

1. The customer's browser returns from the gateway to a callback URL the platform constructed at order-creation time.
2. The per-provider return-handler processes the gateway response and redirects to `/checkout/return/{status}/{payment_hash}`.
3. **Crawler guard** — if the request is from a crawler, abort with 404 + `X-Robots-Tag: noindex`. Order pages must not be indexed.
4. Look up the order-payment by hash; if not found → 404 with `sf.global.err.order_no_longer_exists`.
5. Register the order-payment in the request registry under `checkout.order_payment` so modules (analytics pixel, Yotpo) can read it — see [[checkout-return-emails-tracking]].
6. **If `{status}` !== `cancel`**: clear the order's draft flag (`is_draft` meta key); if the session cart matches the order's `cart_key` meta, **delete that cart and any other carts owned by this user** (this hides the cart from the header bubble); if the Bumper Offer app is enabled, trigger its order-completion hook for attribution.
7. **If `{status}` === `cancel`** — see the cancel branch below.
8. Send transactional emails + set the analytics tracking flag — both on [[checkout-return-emails-tracking]].
9. **Membership app** — for digital `page`-type products, compute and attach `days` + `date_expired` so the page-access expiry shows in the receipt.
10. **Custom thank-you page override** — if a custom thank-you system page is configured, redirect there instead of rendering this template.
11. Render the platform code with the order, payment, and pre-rendered order-details fragment — see [[checkout-return-status-display]].

### The cancel branch

When `{status}` === `cancel`: compose a `cancel_message` (with extra cib_bank detail — TRID, RC, RT codes from `provider_data`), flash it into the session as `payment_canceled`, then redirect — to `/checkout/order/{order}/{hash}` (the draft-order view) if the order is a draft, otherwise back to `/checkout` where the cancelled-payment banner shows.

## What the customer sees

This aspect is about server-side load mechanics; the visible message is on [[checkout-return-status-display]]. The load flow produces one of three outcomes: the generic `return.tpl` renders (most common, non-cancel statuses); a configured custom system page is rendered instead and the generic template never shows; or on `cancel` the customer is redirected away — to `/checkout` (or the draft-order view if the order is a draft).

## Storefront behaviour

- **Cart deletion is per-user, not per-cart** — the cleanup deletes ALL carts owned by this user (including carts in other browsers / devices), not just the current one. By design.
- **Draft-order branch** — draft orders are admin-initiated invoices the customer pays via a link; on `cancel` they route to the draft-order view rather than back to `/checkout`.
- **Refresh-resistant** — refreshing does NOT re-charge or duplicate the order; the cart is already gone and the email/tracking idempotency guards ([[checkout-return-emails-tracking]]) prevent re-sends.

## JavaScript behaviour

The load flow is entirely server-side — no client JS participates in routing, cart cleanup, or the redirect decisions. The page renders inside the regular storefront layout (`the shared layout include` and `layout.footer`). The pixel-injection JS that runs after render is on [[checkout-return-emails-tracking]]; the Braintree dropin + layout JS is on [[checkout-return-status-display]].

## Customisations available to the merchant

- **Custom thank-you page** — admin → Pages → set a page as the "Thank you" system page; this load flow then bypasses the generic template and redirects there.
- **Draft orders** — admin-initiated invoices generate a draft-order link; the cancel branch routes drafts back to the draft-order view rather than `/checkout`.

Other customisations (per-status copy, Yotpo, AdScout, Membership) sit on the display and tracking aspects.

## Theme variations

The return template is **rarely overridden** per theme — most themes inherit it verbatim, so the load flow behaves identically across themes. Themes that customise the post-purchase experience usually do so via the Page Builder "Thank you" custom page, which bypasses this template at step 10.

## Known issues / by-design vs bug

- **Webhook vs return-URL race** — for some providers (Stripe, PayPal) the webhook can arrive **before** the browser returns; the order may already be `completed` when this page loads. The load flow still runs correctly because it reads the current order-payment status.
- **Cart-deletion is broad** — deletes ALL carts owned by this user, even on other devices. Some customers report "my other-device cart disappeared" — by design.
- **`{payment_hash}` is the only auth** — anyone with the URL can see the order. Secure enough in practice, but merchants who paste the URL into screenshots leak order details.
- **Cancel branch redirects, doesn't render the cancel template** — non-draft cancels bounce back to `/checkout` (with a `payment_canceled` flash); the `cancelled` template branch is mostly dead code (verify) — see [[checkout-return-status-display]].
- **Crawler 404** — by design.

## Related

- [[checkout-return]] — hub.
- [[storefront-architecture]] — request lifecycle, no-cache headers, layout inclusion.
- [[checkout]] — the page customers come from before being sent off to the gateway.
- [[checkout-complete]] — the alternative "thank you" landing (in-page-tokenizing gateways skip the return URL).
- [[cart-vs-order-lifecycle]] — Order-status transition on return.
- [[payment-provider-mechanism]] — how each provider's return URL is constructed.
- [[storefront-known-issues]] — cross-page bugs.

## Open questions

- Whether the `cancel` branch of the template ever actually renders, or whether the redirect-back-to-`/checkout` short-circuit catches all cases. (verify)
- Whether the `payment_hash` is rotated after first use, or remains valid forever (and therefore re-shareable). (verify)
