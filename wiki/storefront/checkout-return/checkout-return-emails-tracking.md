---
type: storefront-page
route_name: checkout.return
route_path: /checkout/return/{status}/{payment_hash}
themes_using: [all]
tags: [storefront, checkout, payment, return, email, analytics, conversion-tracking]
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---

> Part of [[checkout-return]]. See the hub for the other aspects (load flow & routing, status-driven display).

# Checkout return — transactional emails & conversion tracking

## Purpose

The two highest-stakes side-effects fired when the customer lands on the return page: the **transactional email cascade** (this is the **only** place the platform's order emails fire for orders that went through a gateway — the checkout page itself sends none) and the **conversion tracking** (this is the **only** place the `Purchase` analytics event fires for off-site-redirect gateways, so anything broken here breaks the merchant's ad-attribution numbers). This aspect answers "why didn't my customer get an order email?", "why is my Facebook/Google purchase count off?", and "does refreshing the page re-send the email?". The load sequence that gets here is on [[checkout-return-load-flow]]; the visible message is on [[checkout-return-status-display]].

## URL & route

Same route as the whole cluster — `checkout.return` — `/checkout/return/{status}/{payment_hash}` (GET, inherits `XSS` + `cart_checkout`). The email + tracking work runs as steps inside the load flow after the cart-cleanup step and before render — see [[checkout-return-load-flow]] for where it sits in the sequence. The `{payment_hash}` resolves the order-payment whose status drives which emails fire.

## How it loads

The email cascade runs only inside an idempotency guard — emails fire **only if `email_sent == 'no'`**, making a page reload safe:

1. **Always**: `sendCreateNewOrder` (new-order notification to customer).
2. If payment status ∈ {`authorized`, `completed`}: `sendCreateNewOrderCompleted`; and if the order contains any digital products, `sendOrderFilesDownloadLink`.
3. If payment status is NOT in {`authorized`, `completed`} AND provider isn't in {`bwt`, `cod`, `pop`} AND provider isn't a credit-group provider: `sendCreateNewOrderPaymentError`.
4. If status !== `cancel` AND order status !== `pending`: fire the `OrderStatusChangeReturn(order, 'pending')` event (wrapped in try/catch — failure is silently swallowed).
5. With `retry(5, ..., 100)` set `email_sent = 'yes'` (5 attempts, 100 ms backoff).

After the email block, the **analytics tracking flag** is set: `google_analitycs_tracking = 'track'` in the order's meta, so the rendered page knows to fire the `Purchase` pixel. The meta key is spelled `google_analitycs_tracking` — the typo (missing the second `c`) is in the data model and is the real stored key.

## What the customer sees

The customer doesn't see the email cascade directly — it produces the order-confirmation email in their inbox (and a payment-error email if the gateway didn't complete). On the page itself, the conversion-tracking side-effects are invisible (pixels) except where an app injects visible receipt content. The visible status message and order-details block are on [[checkout-return-status-display]].

Conversion-tracking elements rendered at the bottom of the page:

- **Yotpo conversion tracking** — the Yotpo manager's `conversionTracking($order)` injects the Yotpo pixel.
- **AdScout xml-feed app** — when installed, runs `window.AdScout.clearStorage(...)` to reset the customer's bumpcart attribution data on the success page.
- **Analytics pixels** — the `Purchase` event fires for Facebook / Google Analytics / Pinterest / TikTok / etc., reading the order from the request registry key `checkout.order_payment`.

## Storefront behaviour

- **Email cascade is idempotent** — emails fire only inside the `if (email_sent == 'no')` block, so running this page a second time doesn't re-send (the digital-files-link branch inside the template still renders the link, but no new email goes out).
- **GA tracking flag** — `google_analitycs_tracking` meta is set the first time the page renders for a non-cancel status. The pixel reads this meta to know whether to fire, so a merchant can clear it to force re-tracking if needed.
- **Pixel double-fire** — refreshing the page does not re-charge or re-email, but the analytics pixel may double-fire if the merchant's pixel config doesn't dedupe (most do).
- **Customers who never return** may receive the order email only via the webhook path (some providers fire their own email path); if the webhook never arrives, no email fires until manual reconciliation — see [[checkout-return-load-flow]] for the webhook race.

## JavaScript behaviour

The conversion-tracking JS is server-rendered and runs on page load:

- **Yotpo pixel injection** — server-rendered `<script>` tag.
- **AdScout reset** — `$(document).ready(function { window.AdScout.clearStorage(window.AdScout.storageDB, true); })` — fires only when the `app.xml_feed.ad_scout` app is installed.
- **Analytics `Purchase` pixels** — server-rendered per-provider snippets (Facebook, GA, Pinterest, TikTok) that read the order from the registry and fire on load.

The email cascade itself is purely server-side — no client JS participates.

## Customisations available to the merchant

- **Yotpo conversion tracking** — installable app; injects its own pixel on this page.
- **AdScout XML feed** — installable app; clears bumpcart attribution on success.
- **Membership** — installable app; attaches page-access expiry to digital-page products in the receipt (the data attached during load flow shows up in the receipt rendered by [[checkout-return-status-display]]).
- **Email content & recipients** — the transactional-email templates and the `Purchase`-pixel configuration are managed in their own admin areas (see Related).

## Theme variations

The email cascade and conversion-tracking blocks are theme-independent — they run in the shared global controller/template path regardless of which theme is active. A theme override of `return.tpl` that drops the trailing pixel block would break conversion tracking; themes that override the template must preserve the analytics + Yotpo + AdScout snippets verbatim.

## Known issues / by-design vs bug

- **The page is the email-trigger, not the checkout-submit handler** — checkout submit creates the order in `pending` status and hands off to the gateway; emails only fire when (a) the customer returns and lands here, or (b) the webhook arrives and fires its own email path. Customers who never return (closed the tab, lost connection) may get the email only via webhook; if the webhook never arrives, no email fires until manual reconciliation.
- **Meta key typo** — `google_analitycs_tracking` (missing the second `c`) is the actual stored meta key. Don't "fix" this without a migration — it would orphan all historical orders' tracking flags.
- **`email_sent` retry loop** — the platform code swallows update failures. If all 5 retries fail, the order will re-send emails next time the page is loaded.
- **`Purchase` pixel dedup across webhook + return** — whether the pixel is fully deduplicated when both the webhook and the return URL fire is unverified (verify).

## Related

- [[checkout-return]] — hub.
- [[notification-delivery]] — how the new-order / completed-order emails are queued.
- [[checkout-return-status-display]] — the receipt block where digital-file links and Membership expiry surface.
- [[order-status-workflow]] — the `OrderStatusChangeReturn(order, 'pending')` transition fired here.
- [[order-processing-pipeline]] — what fires server-side after the order is placed.
- [[abandoned-cart-recovery]] — what happens if the customer never reaches this page.
- [[storefront-known-issues]] — cross-page bugs.

## Open questions

- Whether the `Purchase` analytics pixel is fully deduplicated when both the webhook and the return URL fire. (verify via [[notification-delivery]] and the analytics manager)
- The exact set of providers in the credit-group that suppress the `sendCreateNewOrderPaymentError` email. (verify per provider)
