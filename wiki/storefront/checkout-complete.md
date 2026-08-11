---
type: storefront-page
route_name: (no dedicated route — served via the return URL or a custom system page)
route_path: /checkout/return/completed/{payment_hash} (default) OR custom page URL when configured
themes_using: [all]
tags: [storefront, checkout, thank-you, post-purchase, conversion, tracking]
created: 2026-06-08
updated: 2026-06-08
source_count: 5
---

# Checkout complete (thank-you page)

## Purpose

The page the customer sees **after a successful order placement** — the "Thank you, your order is confirmed" landing. It is **not a dedicated `/checkout/complete` route**. It has two forms:

1. **Default** — the `/checkout/return/{status}/{payment_hash}` URL renders a thank-you message when `{status}` is `completed` / `requested` / `pending` (see [[checkout-return]] for the full status table).
2. **Merchant-customised** — when a Page Builder page is marked as the `thank_you` system page, the return-URL handler **redirects to that custom page** (same order context), which becomes the canonical "Order completed" page.

For in-page-tokenizing gateways (Braintree, Mokka, custom inline forms) the customer never leaves `/checkout`; the JS receives success and navigates to the return URL.

This page is the **anchor for advertising attribution** — where Facebook Pixel `Purchase`, Google Analytics `purchase`, TikTok `CompletePayment`, and Pinterest `checkout` events fire. Anything broken here breaks the merchant's CPA / ROAS numbers.

## URL & route

- **Default URL** — `/checkout/return/completed/{payment_hash}` (the `completed` status on the `checkout.return` route).
- **Custom URL** — when a Page Builder page has `system_page = 'thank_you'`, the system redirects to it.
- **Method**: GET only.
- **Auth**: the `{payment_hash}` is the only authentication (same as [[checkout-return]]).

No `checkout.complete` route name exists — it is conceptually a status branch of the return URL.

## How it loads

**Default template** — the browser lands on `/checkout/return/completed/{payment_hash}` (see [[checkout-return]]); the handler does cart cleanup, the email cascade, and analytics tagging, then renders the `completed`-status branch of the return template.

**Custom thank-you page** — same arrival flow, but the handler resolves the active page where `system_page = 'thank_you'`, runs it through the Page Builder with the order injected, and returns that HTML directly — the default template is bypassed.

To configure it: Admin → Pages → create a page, design it, then mark it "Use as: Thank-you page" (`system_page = thank_you`). Modules can reference the order context (number, total, items, email).

## What the customer sees

**Default template** (`completed` branch):

- Title: `sf.checkout.header.status_completed` (e.g. "Order completed").
- Body: `sf.checkout.succ.status_completed` (e.g. "Thank you for your order. We'll send you a confirmation email shortly.").
- **Digital files link** — for `file`-type products, a link to `site.account.files`; passes `order_product_ids` so only this order's files list.
- **Digital pages link** — for `page`-type products, a link to `site.account.pages` (Membership app access-granted pages).
- **UBB block** — provider-specific receipt header when `payment_provider === 'ubb'`.
- **Order details** — full summary: number, date, line items with images, totals, shipping/billing address, payment + shipping method, "Track shipment" link via the `17track.net` pattern.

**Custom page** — whatever the merchant designed. Common modules: Order summary, cross-sell carousel, subscribe-to-newsletter, free-form HTML, Bumper Offer upsell, pixel injection.

## Storefront behaviour

- **Refresh-safe** — refreshing does NOT re-charge or duplicate-email; the order exists, the cart is deleted, and the email cascade fires once via the `email_sent` idempotency flag (see [[checkout-return]]).
- **Back-button** — returns to the gateway success screen or an empty `/checkout`; the order cannot be re-submitted.
- **Cart bubble empty** — the header cart icon shows 0 items (cart deleted on arrival).
- **Customer session** — a guest keeps their `guest` record with the order attached; a registered customer has it on their account.
- **Membership side effect** — for `page`-type products the access expiry (`date_expired`) is set on this render (`days` × quantity), unlocking the "My pages" section.
- **Tracking pixels fire once per page-load** — most SDKs dedupe on `transaction_id`, but the in-page `<script>` tags run on every render.

## JavaScript behaviour

Mostly server-rendered. JS that runs here:

- **Pixel SDKs** — Facebook Pixel `Purchase`, Google Analytics 4 `purchase`, Google Ads conversion tag, TikTok `CompletePayment`, Pinterest `checkout`, Microsoft Ads UET, Snap Pixel — injected from the merchant's configured pixels (admin → Online sales → Sales channels → Online sales → Tracking).
- **GA enhanced ecommerce** — order items and totals are serialised into a `dataLayer.push` call.
- **Yotpo conversion tracking** — when the Yotpo app is installed, its conversion script is injected.
- **AdScout** — when the `app.xml_feed.ad_scout` app is installed, clears storage on success (`window.AdScout.clearStorage(window.AdScout.storageDB, true)`).
- **Page Builder modules** — on a custom page, each module runs its own JS.

No add-to-cart UI. No custom `cc.*` events fire — terminal state.

## Customisations available to the merchant

- **Custom thank-you page** (the big one) — create a Page Builder page, mark `system_page = thank_you`, and it auto-replaces the default via redirect. Order context available to modules.
- **Per-status copy** (default template) — all `sf.checkout.header.status_*` and `sf.checkout.succ.status_*` strings are editable (admin → Languages).
- **Pixel / tracking** — admin → Online sales → Tracking → configure Facebook Pixel ID, GA4 measurement ID, Google Ads conversion ID; these inject into the page `<head>`.
- **Apps adding UI here** — Yotpo ("Write a review" prompt), Bumper Offer (attribution finalised), Membership (digital-page expiry), AdScout (clears bumpcart attribution).

The default page has no Theme Editor module — its layout is hard-coded. To customise it the merchant overrides the return template, or (more commonly) uses the custom thank-you Page Builder page.

## Theme variations

The default template is **rarely overridden** per theme; the order-details fragment is shared. A custom Page Builder thank-you page is wrapped by the theme's header + footer like any other Page Builder page.

## Known issues / by-design vs bug

- **There is NO `/checkout/complete` URL** — any doc referencing it means the conceptual page; the real URL is the return URL with `completed` status (or the custom page). (verify — no `checkout.complete` route exists.)
- **Pixel firing depends on this page rendering** — if a custom page omits the pixel snippet, `Purchase` will NOT fire. Common "conversions aren't tracked" ticket — check for a custom page first.
- **Custom page bypasses ALL default-page logic** — the digital-files link, digital-pages link, UBB receipt block, and order-details template are NOT auto-rendered; the merchant adds equivalent modules.
- **Order can be `pending` when this page renders** — gateways with `requested` / `pending` final status show a thank-you message while the order is still `pending`; the merchant ships nothing until the webhook flips it to `paid`. Customers may see "Thank you" then a "Payment failed" email. By design.
- **Cart already deleted** — any "you also bought" carousel relying on cart contents falls back to general recommendations.
- **`google_analitycs_tracking` meta typo** — the meta key is misspelled (missing the second `c`). Don't "fix" without migration.
- **Webhook-vs-return race** — the page may render before the webhook (`pending`) or after (`completed`); the message is identical (see [[checkout-return]]).

## Related

- [[storefront-architecture]] — request lifecycle.
- [[checkout-return]] — the URL that renders this page (or redirects to the custom one).
- [[checkout]] — where customers come from.
- [[cart-vs-order-lifecycle]] — Cart → Order transition completes here.
- [[order-status-workflow]] — `pending` → `paid` → `completed`.
- [[order-processing-pipeline]] — server-side actions after placement.
- [[notification-delivery]] — the post-order email cascade.
- [[page]] — Page Builder pages, the substrate for custom thank-you pages.
- [[apps-bumpcart]] — bumper-offer finalisation.
- [[storefront-known-issues]] — cross-page bugs.

## Open questions

- Whether `Purchase` pixel events dedupe when both this page renders and the webhook fires. (verify per provider)
- Whether the `payment_hash` is single-use or permanent. (verify)
- Whether in-page-tokenizing gateways (Braintree, Mokka inline) reliably navigate to the return URL, or sometimes leave the customer on `/checkout`. (verify)
- The full list of `system_page` slugs recognised beyond `thank_you`. (verify)
