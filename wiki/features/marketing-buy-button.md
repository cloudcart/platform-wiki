---
type: feature
nav_path: "Marketing → Buy Button"
route_name: admin.embed
route_path: /admin/buy-button
aliases: ["Buy Button", "Buy button", "Embeddable buy button", "Embed module", "Checkout link", "Бутон за покупка", "Връзка за плащане"]
tags: [marketing, sales-channels, embed, headless, module]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# Buy Button

## Purpose

The **Buy Button** screen is the merchant's "sell anywhere" tool. It generates a small piece of JavaScript that the merchant copies into any external HTML page — a personal blog post, a partner site, a WordPress page, a landing page hosted on another platform, a Medium-style article — and the snippet renders a live **CloudCart product card** (image, title, price, description, quantity field, "Add to cart" button) right inside that external page, fed live from the merchant's CloudCart store. The customer never has to leave the external page to add the product to a cart, and when they're ready to pay, the snippet either opens a CloudCart cart panel right there or sends them straight to checkout — both ending in a real CloudCart order under this merchant's store.

The same screen also produces a **direct checkout link** — a short URL the merchant can paste into social-media posts, Viber/SMS messages, email signatures, or QR codes that takes the shopper directly to the CloudCart checkout page with the chosen product (and variant) already in their cart. This is the lightweight alternative when the merchant just wants a pasteable link instead of an embeddable module.

This page is the **hub** for the Buy Button cluster. The detailed mechanics live in the aspect sub-pages listed below; this hub carries only the overview, the navigation map, and the cross-cutting rules that don't belong to a single aspect.

## Where to find it

Sidebar → **Marketing** → **Sales Channels** → **Buy Button**.

The route is `/admin/buy-button`. The screen is rendered by the legacy Smarty `embed.index` view. The header breadcrumb reads "Create a Buy Button". The empty-state page invites the merchant to choose one of two flows: **Create a Buy Button** (generates the JS snippet — see [[buy-button-builder]]) or **Create a checkout link** (generates the URL — see [[buy-button-checkout-link]]).

## What the merchant can do here

The page presents two starting choices:

- **Create a Buy Button** — opens the product picker (modal). After selecting a product, the merchant is routed to `/admin/buy-button/builder/{product_id}` (the visual builder). Full detail in [[buy-button-builder]].
- **Create a checkout link** — opens a side panel with a product search; after picking a product (and a variant for products with variants), the panel shows a copy-ready URL. Full detail in [[buy-button-checkout-link]].

### What the merchant CANNOT do here

- Pick more than one product per Buy Button — each generated snippet targets exactly one product (one product ID baked into the JS).
- Embed an entire category, brand, or storefront listing — only single products.
- Customise the cart drawer copy / icon / labels per-button (those follow the storefront theme's wording).
- Track which external sites each button is embedded on — there is no per-button analytics dashboard in admin (see [[buy-button-attribution]]).
- Generate **bundle** product Buy Buttons via the checkout-link flow — the checkout-link autocomplete filters out bundle-type products. Bundle products are still selectable from the Buy Button builder flow itself (see [[buy-button-checkout-link]]).

## Sub-pages (in this cluster)

This feature is split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[buy-button-builder]] — the visual builder: three templates (Simple / Basic / Full), the **Action on click** dropdown (`cart` vs `checkout`), customization accordions, and the read-only generated-code screen.
- [[buy-button-checkout-link]] — the pasteable direct-checkout-link side-panel flow: `{site_url}/embed/{variant_id}` URL format, per-variant tile selection, and why bundles are excluded.
- [[buy-button-embed-runtime]] — the storefront-side embed runtime: the `<script>` snippet shape, CDN-served assets, the embedded cart panel, the admin-builder vs storefront-runtime split, CORS, and rate-limit posture.
- [[buy-button-parameters]] — the full customization-parameter reference table, the default-stripping (`array_filter`) behaviour, and the hidden `font` control.
- [[buy-button-attribution]] — where Buy Button orders surface and how they're attributed (`meta.referer = buy_button` / `checkout_link`), the no-persistence model, permissions, the headless angle, and stale-/deleted-product behaviour.

## Settings & fields

The Buy Button screen has **no stored settings**. Nothing about a generated button is persisted in CloudCart's database — all customisation state is encoded into the snippet's `parameters` object (builder flow) or into the URL (checkout-link flow). There is no "my saved Buy Buttons" list and no edit-by-button-ID flow; to change anything the merchant regenerates and re-pastes.

- The builder's editable fields (template, action, ~18 colour / font / display controls) are documented in [[buy-button-parameters]].
- The checkout-link's only "field" is the variant tile selector that builds the URL — see [[buy-button-checkout-link]].
- The product picker autocompletes only products with `active = 'yes'` — inactive / hidden products don't appear (see [[buy-button-attribution]] for what happens when a product is deactivated after generation).

## Business rules

### One Buy Button = one product (or one variant)

Every snippet targets a single product by ID. To sell five products on one blog post, the merchant generates five separate snippets and pastes them in five separate places. There's no way to render a list / carousel / grid of multiple products from a single Buy Button.

For products with variants, the generated `<script>` carries the **parent product ID**, not a specific variant — the embed module then renders the variant selector inline so the shopper picks. The checkout-link flow, in contrast, bakes a specific **variant ID** into the URL so it's pre-selected at checkout (see [[buy-button-checkout-link]]).

### Two flows, two surfaces

The builder flow produces an **embeddable module** (a live product card on the external page); the checkout-link flow produces a **pasteable URL** (a direct jump to CloudCart checkout). Both ultimately end in a real CloudCart order under this merchant's store — the purchase always happens on CloudCart, never on the third-party site. Where the shopper lands and how the order is attributed is documented in [[buy-button-attribution]]; the runtime endpoints that serve the embed are in [[buy-button-embed-runtime]].

### No plan-feature gate

There is **no plan-feature gate** on this screen — Buy Button is available on every plan that grants marketing access. Permission gating (the `marketing.saleschannels` staff permission) is covered in [[buy-button-attribution]].

## Related

- [[marketing]] — Marketing pillar.
- [[products-products]] — products that can be embedded.
- [[orders-products]] — where Buy Button orders surface.
- [[headless-storefront]] — broader headless commerce concept.
- [[analytics-sales-by-traffic-source]] — UTM-based attribution for Buy Button placements.
- [[product]] — Product entity.
- [[variant]] — Variant entity (used by the checkout-link flow).
- [[cart]] — Cart entity (the embedded drawer instantiates one).

## Open questions

No outstanding questions.
