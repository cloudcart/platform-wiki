---
type: feature
nav_path: "Marketing → Buy Button → Builder"
route_name: admin.embed.builder
route_path: /admin/buy-button/builder/{product_id}
aliases: ["Buy Button builder", "Buy Button visual builder", "Generate code", "Embed builder", "Buy Button templates", "Конструктор на бутон за покупка"]
tags: [marketing, sales-channels, embed, builder, module]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Buy Button — Visual builder

> Part of [[marketing-buy-button]]. See the hub for the other aspects (checkout link, embed runtime, parameters, attribution).

## Purpose

The **visual builder** is the configurator surface of the [[marketing-buy-button]] flow. It is where the merchant picks an embed **template**, decides what happens **on click**, styles the colours and font, and then generates the final copy-to-clipboard `<script>` snippet. It is the "Create a Buy Button" branch of the hub's empty-state (the "Create a checkout link" branch is the lighter [[buy-button-checkout-link]] flow instead).

The builder is purely a client-side configurator: it does not save anything — every choice is encoded into the snippet's `parameters` object at the end (see [[buy-button-parameters]] for the full list of what's encoded and how defaults are stripped).

## Where to find it

Reached from the hub: Sidebar → **Marketing** → **Sales Channels** → **Buy Button** → **Create a Buy Button** → pick a product in the modal product picker → routed to `/admin/buy-button/builder/{product_id}`.

The builder is rendered by the legacy Smarty builder view. The product picker for this flow opens as a **modal** (the checkout-link flow uses a side panel instead).

## What the merchant can do here

The builder is a left-hand panel of customization controls + a right-hand **live preview iframe** that re-renders as the merchant edits.

### Template variants

Three template variants set how much of the product is shown:

| Template | Label | What it renders |
|----------|-------|-----------------|
| `button` | **Simple** | Just a styled "Add to cart" button — no product info displayed. Smallest footprint. |
| `basic` | **Basic** (default) | Button + price line. |
| `enhanced` | **Full** | Full product card: image, title, SKU, properties, description, quantity selector, price, button. |

### Action on click

The **Action on click** dropdown picks the post-click behaviour:

- **Adds product to cart** (`cart`) — the embedded cart drawer slides in on the external page. The shopper continues shopping or clicks Checkout, which then routes them to the CloudCart checkout. The drawer is served by the storefront-side runtime — see [[buy-button-embed-runtime]].
- **Directs customers to checkout** (`checkout`) — clicking the button jumps the shopper directly to `/embed/checkout` on the CloudCart-hosted checkout — no cart drawer step.

### Customization controls (accordion panels)

- **Button** — text colour, background colour, font size (slider, px).
- **Product** — toggles for *Display SKU*, *Display Properties*, *Display description*, *Display quantity*; colours for title, text, background, price, input text, input background.
- **Cart** (only shown when `action = cart`) — text colour, background colour, input text colour, input background colour.

Clicking **Generate code** routes to `/admin/buy-button/build/{product_id}`, which renders the snippet (see below).

### The generated-code screen (`admin.embed.build`)

Shows the produced `<script>` block in a **read-only** textarea with a **Copy code** button. Tooltip text: *"Paste this code into the site's HTML where you'd like the product to appear."* Click feedback toast: *"Copied"*.

This is a one-shot output surface with no editable fields. To change any customisation, the merchant goes back to the builder (the breadcrumb provides the navigation). There's no "save" / "regenerate" — every visit produces the same snippet because all customisation state is encoded into the URL query string that brought the merchant here. The exact shape of the snippet is documented in [[buy-button-embed-runtime]].

### What the merchant CANNOT do here

- Pick more than one product — each builder session targets exactly one product ID.
- Re-open a previously generated button to tweak it by ID — there is no persistence (see the hub [[marketing-buy-button]]). Restyling means rebuilding and re-pasting.

## Settings & fields

The builder's editable fields map one-to-one onto the snippet's customization parameters. The two structural choices are:

| Key | Type | Values |
|-----|------|--------|
| `template` | string | `button` (Simple), `basic` (Basic, default), `enhanced` (Full) |
| `action` | string | `cart` (default), `checkout` |

Invalid values for `template` and `action` silently fall back to `basic` and `cart` respectively (server-side defaulting). The colour / font / display-toggle fields are listed exhaustively in [[buy-button-parameters]] — they are encoded into the snippet only when non-default.

## Business rules

### State lives in the URL, not the database

Because the generated-code screen reads its entire configuration from the URL query string, the builder is **stateless on the server**. Two merchants who configure the same product the same way get byte-identical snippets. There is no draft, no autosave, and no list of previously built buttons.

### Live preview reflects the storefront runtime

The right-hand preview iframe renders the same embed code the shopper would see, using the storefront-side runtime ([[buy-button-embed-runtime]]). The **Cart** accordion only appears when `action = cart`, because the cart-drawer colours have no effect under the `checkout` action.

### Bundles are allowed in the builder

Unlike the [[buy-button-checkout-link]] flow (which filters bundles out), the builder flow **does** work for bundle products — the embed renders the bundle's normal product page with its component picker. The snippet carries an `is_bundle: 1` flag so the runtime knows to render the bundle UI (see [[buy-button-embed-runtime]]).

## Related

- [[marketing-buy-button]] — hub.
- [[buy-button-embed-runtime]] — the snippet the builder emits + how it renders on the external page.
- [[buy-button-parameters]] — full customization-parameter reference.
- [[buy-button-checkout-link]] — the lighter URL-only alternative flow.
- [[products-products]] — products that can be embedded.
- [[product]] — Product entity.

## Open questions

No outstanding questions.
