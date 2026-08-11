---
type: feature
nav_path: "Marketing → Buy Button → Checkout link"
route_name: admin.checkout_link
route_path: /admin/buy-button (checkout-link side panel)
aliases: ["Checkout link", "Direct checkout link", "Buy Button checkout link", "Pasteable checkout URL", "Връзка за плащане", "Директна връзка за плащане"]
tags: [marketing, sales-channels, embed, checkout-link, module]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Buy Button — Checkout link

> Part of [[marketing-buy-button]]. See the hub for the other aspects (builder, embed runtime, parameters, attribution).

## Purpose

The **checkout link** is the lightweight alternative to the embeddable [[buy-button-builder]]. Instead of generating a `<script>` to render a live product card, it produces a single short **URL** the merchant can paste into a social-media post, a Viber/SMS message, an email signature, or a QR code. Clicking the link sends the shopper directly to the CloudCart checkout with the chosen product (and a specific variant, if it has variants) already in their cart.

This is the right tool when the merchant just wants a pasteable link, not an embeddable module — for example, "buy now" buttons in an email blast or a link-in-bio.

## Where to find it

Reached from the hub: Sidebar → **Marketing** → **Sales Channels** → **Buy Button** → **Create a checkout link**. This opens a **side panel** (the builder flow uses a modal instead).

The admin side-panel route is `admin.checkout_link`. The link it produces points at the storefront-side `checkout_link` route under the `/embed/` prefix.

## What the merchant can do here

- Type a product name into an **autocomplete** search; the panel reloads to show the matched product.
- For products **with variants**: pick a variant tile (the active tile is highlighted) — the URL below updates live to bake in that variant.
- Copy the **URL** field, which shows the pasteable checkout link. Tooltip text: *"This link will send shoppers directly to this product's checkout page."*

### What the merchant CANNOT do here

- Generate a checkout link for a **bundle** product — the autocomplete filters bundle-type products out (`whereTypeNotBundle`). Bundles must use the [[buy-button-builder]] flow instead.
- Style anything — the checkout link carries no colours / templates (those belong to the builder, see [[buy-button-parameters]]).
- Combine multiple products into one link — one link targets one variant.

## Settings & fields

### Checkout-link URL format

For products **without variants**:

```
{site_url}/embed/{variant_id}
```

For products **with variants**: the URL is built incrementally — `{site_url}/embed/` plus the active variant ID — and updates each time the merchant clicks a different variant tile.

The `/embed/` prefix maps to the storefront `checkout_link` route, which the storefront treats as "add this variant to a fresh cart, then jump to checkout". The only "field" on this screen is the variant tile selector that determines `{variant_id}`.

## Business rules

### Variant is pre-selected (unlike the builder)

The checkout link bakes a specific **variant ID** into the URL, so the variant is already chosen when the shopper lands at checkout. This is the opposite of the [[buy-button-builder]] embed, which carries the **parent product ID** and lets the shopper pick the variant inline. A merchant who wants the shopper to choose should use the builder; a merchant who wants a fixed SKU should use the checkout link.

### Direct to checkout — no cart drawer

The checkout-link flow sends the shopper straight to CloudCart's checkout from the first click — there is no embedded cart-drawer step (that step exists only in the `cart` action of the builder, see [[buy-button-embed-runtime]]). The order then surfaces and is attributed exactly as documented in [[buy-button-attribution]] (these checkouts are tagged `meta.referer = 'checkout_link'`).

### Bundles excluded — and why

The checkout-link autocomplete excludes bundle-type products because a bundle can't be turned into a direct checkout link: bundle components require per-component variant selection on the storefront product page, which the one-shot link can't capture. The [[buy-button-builder]] flow still works for bundles (the embed renders the bundle's normal product page with its component picker).

### Active-only products

Like the builder picker, the checkout-link autocomplete only surfaces products with `active = 'yes'`. If a product is deactivated after the link is shared, the storefront renders an unavailable state; if it's deleted entirely, the link 404s — see [[buy-button-attribution]] for the deleted-product behaviour.

## Related

- [[marketing-buy-button]] — hub.
- [[buy-button-builder]] — the embeddable-module alternative flow.
- [[buy-button-attribution]] — where these orders surface + the `checkout_link` referer tag.
- [[variant]] — Variant entity; its ID is baked into the URL.
- [[product]] — Product entity.

## Open questions

No outstanding questions.
