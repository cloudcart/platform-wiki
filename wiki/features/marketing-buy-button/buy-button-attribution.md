---
type: feature
nav_path: "Marketing → Buy Button → Attribution & lifecycle"
route_name: admin.embed
route_path: /admin/buy-button
aliases: ["Buy Button attribution", "Buy Button orders", "Buy Button referer", "Buy Button permission", "Buy Button persistence", "Buy Button deleted product", "Атрибуция на бутон за покупка"]
tags: [marketing, sales-channels, embed, attribution, headless, permissions]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Buy Button — Attribution & lifecycle

> Part of [[marketing-buy-button]]. See the hub for the other aspects (builder, checkout link, embed runtime, parameters).

## Purpose

This page answers the "after the sale" and "who can use this" questions for the [[marketing-buy-button]]: where Buy Button orders show up, how they're attributed, what (if anything) is stored, the staff permission that gates the screen, the headless angle, and what happens when the embedded product is deactivated or deleted.

## Where to find it

There is no dedicated attribution screen. Buy Button orders surface on the merchant's [[orders-products]] list like any other order. The Buy Button admin screen itself lives at Sidebar → **Marketing** → **Sales Channels** → **Buy Button** (`/admin/buy-button`) — see the hub [[marketing-buy-button]].

## What the merchant can do here

- See Buy Button orders in [[orders-products]] alongside normal storefront orders.
- Use UTM parameters on the external page URL and read them out of [[analytics-sales-by-traffic-source]] for per-placement attribution.

### What the merchant CANNOT do here

- See a per-Buy-Button analytics surface — there is no "this button on this domain produced X orders" report in admin.
- Edit or restyle a previously generated button — nothing is persisted (see Business rules).

## Settings & fields

There are **no stored settings** for attribution. The only attribution data CloudCart writes is a single referer tag on the cart at checkout (see below). Everything else (per-placement insight) must be layered on by the merchant via UTM parameters and [[analytics-sales-by-traffic-source]].

## Business rules

### Where the customer ends up at checkout

This trips up most merchants the first time. The Buy Button is a **storefront-side embed** — when the shopper clicks Add to cart, the cart lives on the external page (served via the [[buy-button-embed-runtime]] `/embed/cart-panel` route). When they click Checkout from that drawer, they're sent to `/embed/checkout` on the CloudCart-hosted domain — not the external page. So the final purchase always happens on the merchant's CloudCart store, never on the third-party site, and the order record lands in [[orders-products]] like any other order. The [[buy-button-checkout-link]] flow skips the drawer and goes straight to checkout from the first click.

### The only stored attribution — `meta.referer`

When a customer clicks "Checkout" inside the embedded cart drawer, the platform tags the cart with `meta.referer = 'buy_button'` before redirecting to the CloudCart-hosted checkout. The [[buy-button-checkout-link]] flow tags `meta.referer = 'checkout_link'` instead. This is the **only** stored attribution — there is NO per-button ID, NO source domain stored, NO unique snippet identifier. Merchants doing per-placement analysis must add UTM parameters or referer-URL handling on top, then read them via [[analytics-sales-by-traffic-source]].

### No save / no persistence

Unusually for a Marketing screen, nothing about a generated Buy Button is **stored** in CloudCart's database. The builder is a fully client-side configurator (see [[buy-button-builder]]) — the colours and toggles are encoded into the snippet's `parameters` object and live forever inside whatever HTML the merchant pastes them into. There's no "my saved Buy Buttons" list, no edit-by-button-ID flow, and no way to retroactively restyle a previously embedded button. To change the look, the merchant regenerates the snippet and re-pastes it.

### Active-only product selector

The product picker autocompletes products with `active = 'yes'` — inactive / hidden products don't appear. If the merchant **deactivates** a product after generating a snippet, the snippet still loads but the embed renders an "out of stock / unavailable" state on the external site.

### Stale-snippet behaviour (deleted product)

If the merchant **deletes** the embedded product entirely (not just deactivates), the snippet still resolves but the storefront responds with a **404** carrying the message *"This product is no longer available"* (translation key `sf.store.err.product_no_longer_exists`). The merchant should remove the snippet from the external page once a product is fully deleted.

### Headless implications

The Buy Button is the platform's **lightweight headless** path: the merchant keeps their existing marketing site (blog, partner page, landing page on another CMS) as the visible UI, but sells through CloudCart as the commerce backend. No SDK / API key is required — the snippet is fully self-contained and authenticates against the store by `STORE_URL` only. The external site doesn't need to know anything about the customer — login state, cart state, currency, language, shipping options are all owned and managed by CloudCart inside the embedded iframe / drawer. See [[headless-storefront]] for the broader concept.

### Permission

The Buy Button page sits under the **Sales Channels** dropdown inside the Marketing pillar. The parent Marketing pillar is shown when the staff role grants any of: `marketing`, `marketing.*`, `marketing.saleschannels`, plus the usual sub-permissions (see [[marketing]]). A staff role without marketing permissions never sees this screen.

There is **no plan-feature gate** on this screen — Buy Button is available on every plan that grants marketing access.

## Related

- [[marketing-buy-button]] — hub.
- [[orders-products]] — where Buy Button orders surface.
- [[analytics-sales-by-traffic-source]] — UTM-based attribution for placements.
- [[buy-button-embed-runtime]] — the checkout hand-off where `meta.referer` is set.
- [[buy-button-checkout-link]] — sets `meta.referer = 'checkout_link'`.
- [[headless-storefront]] — broader headless commerce concept.
- [[marketing]] — Marketing pillar + permission model.

## Open questions

No outstanding questions.
