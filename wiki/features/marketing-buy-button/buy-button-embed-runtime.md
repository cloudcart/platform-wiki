---
type: feature
nav_path: "Marketing → Buy Button → Embed runtime"
route_name: (storefront) checkout_link / embed.cart-panel / embed.cart-add / embed.remove / embed.checkout
route_path: /embed/...
aliases: ["Buy Button embed runtime", "Embed snippet", "CloudCartEmbed", "Embed cart panel", "Buy Button script", "Embed endpoints", "Рънтайм на бутон за покупка"]
tags: [marketing, sales-channels, embed, storefront, runtime, headless]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Buy Button — Embed runtime

> Part of [[marketing-buy-button]]. See the hub for the other aspects (builder, checkout link, parameters, attribution).

## Purpose

The **embed runtime** is the storefront-side machinery that actually renders a Buy Button on a third-party page and processes the shopper's actions. The [[buy-button-builder]] is the admin-side configurator that *emits* a `<script>` snippet; this page covers what that snippet looks like and what happens when it boots inside an external HTML page: the live product card, the embedded cart panel, add-to-cart / remove / bulk-update, and the hand-off to CloudCart checkout.

## Where to find it

There is no admin screen for the runtime — it runs in the **shopper's browser** on the external page, hitting CloudCart's storefront `/embed/...` endpoints from inside the embedded `<iframe>` after the snippet boots. Merchants reach it indirectly by pasting the snippet from the [[buy-button-builder]]'s generated-code screen into their own HTML.

## What the merchant can do here

Nothing directly — this is a runtime, not a screen. What the merchant controls (via the builder snippet) is which product loads, the template, the click action, and the styling. The runtime then handles everything the shopper does on the external page: viewing the card, changing quantity, adding to cart, opening the cart drawer, and proceeding to checkout.

## Settings & fields

### Embed-script format (output of "Generate code")

The generated `<script>` block is a self-executing function that injects a placeholder `<div>` plus the CloudCart embed CSS + JS, then instantiates `CloudCartEmbed`:

```
<script>
  (function {
    document.write('<div id="cc-product-component-{PRODUCT_ID}"></div>');
    var ccJs = document.createElement("script"),
        ccStyle = document.createElement("link");
    ccStyle.rel="stylesheet";
    ccStyle.type="text/css";
    ccStyle.href="{CDN_URL}global/css/embed.min.css";
    document.head.appendChild(ccStyle);
    ccJs.type ="text/javascript";
    ccJs.async = true;
    ccJs.src = "{CDN_URL}global/js/Embed.min.js";
    ccJs.onload = function {
        new CloudCartEmbed({
            url: '{STORE_URL}',
            product: {PRODUCT_ID},
            is_bundle: {0_or_1},
            parameters: {/* customization options */}
        }).init;
    };
    document.head.appendChild(ccJs);
  });
</script>
```

The `parameters` object carries the builder's choices — see [[buy-button-parameters]] for the full key list and how defaults are stripped.

### Storefront embed endpoints

The runtime calls these storefront routes from the iframe:

- `/embed/cart-panel` — renders the embedded cart drawer on the external page.
- `/embed/cart-add` — adds the chosen variant + quantity to the embedded cart.
- `/embed/remove` — removes a line from the embedded cart.
- `/embed/checkout` — hands off to the CloudCart-hosted checkout.
- `/embed/{variant_id}` — the checkout-link entry point (see [[buy-button-checkout-link]]).

## Business rules

### Two surfaces — admin builder + storefront runtime

There are two surfaces: the **admin-side builder** ([[buy-button-builder]]) handles product selection, the builder UI, and code generation. The **storefront-side embed runtime** (this page) serves the embedded product card, cart panel, add-to-cart, remove, bulk update, and checkout endpoints. Both surfaces share the same parameter-normalisation logic — defaults invalid templates to `basic`, invalid actions to `cart`, fills missing colour keys with empty strings.

### Assets come from CDN config

The CSS (`embed.min.css`) and JS (`Embed.min.js`) are loaded from the platform's image / static CDN. The merchant's external site loads these directly, no proxying — which is why the snippet works on any HTML page that allows third-party scripts.

### Bundle detection on instantiation

The embed constructor receives an `is_bundle: 0|1` flag — the embed JS uses it to render the bundle component picker UI when the embedded product is a bundle. For non-bundles it's `0`. (The [[buy-button-builder]] flow is the only one that supports bundles; [[buy-button-checkout-link]] excludes them.)

### No rate limit on the embed routes (default)

The `/embed/cart-add`, `/embed/cart-panel`, `/embed/remove`, `/embed/checkout` routes don't carry post-throttle middleware in the platform default (unlike the storefront cart routes, which often have throttles in front). This is because the embed iframe is intentionally lightweight — but it means a malicious external page could in principle hammer add-to-cart on behalf of a victim. The risk is moderate, since the cart simply fills up; checkout still requires shopper interaction.

### Final purchase always lands on CloudCart

When the shopper clicks Add to cart under the `cart` action, the cart lives on the external page via `/embed/cart-panel`. Clicking Checkout from that drawer sends them to `/embed/checkout` on the CloudCart-hosted domain — not the external page. The order record always lands in the merchant's [[orders-products]]; how it's tagged and attributed is documented in [[buy-button-attribution]].

## Related

- [[marketing-buy-button]] — hub.
- [[buy-button-builder]] — the admin configurator that emits this snippet.
- [[buy-button-parameters]] — the `parameters` object encoded into the snippet.
- [[buy-button-attribution]] — where the resulting orders surface + the `referer` tag set at checkout.
- [[headless-storefront]] — broader headless commerce concept.
- [[cart]] — Cart entity (the embedded drawer instantiates one).
- [[orders-products]] — where Buy Button orders surface.

## Open questions

No outstanding questions.
