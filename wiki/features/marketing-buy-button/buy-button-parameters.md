---
type: feature
nav_path: "Marketing → Buy Button → Parameters"
route_name: admin.embed.builder
route_path: /admin/buy-button/builder/{product_id}
aliases: ["Buy Button parameters", "Embed customization parameters", "Buy Button colours", "Embed parameters reference", "Buy Button font", "Параметри на бутон за покупка"]
tags: [marketing, sales-channels, embed, parameters, customization]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Buy Button — Customization parameters

> Part of [[marketing-buy-button]]. See the hub for the other aspects (builder, checkout link, embed runtime, attribution).

## Purpose

This is the **reference page** for every customization parameter the [[buy-button-builder]] can set on a Buy Button. These ~18 keys are gathered from the builder's accordion controls (template, action, colours, font, display toggles) and encoded into the `parameters` object inside the generated snippet (see [[buy-button-embed-runtime]] for where the object sits). The page also documents how defaults are stripped to keep the snippet readable, and the one control that exists in code but is hidden from the UI today.

## Where to find it

These parameters are set from the [[buy-button-builder]] at `/admin/buy-button/builder/{product_id}` and end up baked into the snippet on the generated-code screen (`/admin/buy-button/build/{product_id}`). There is no separate "parameters" screen — this page is a documentation reference, not a UI.

## What the merchant can do here

The merchant sets these parameters indirectly via the builder accordions; the values then ride along in the snippet. The full set:

### Customization parameters

| Key | Type | Values |
|-----|------|--------|
| `template` | string | `button` (Simple), `basic` (Basic, default), `enhanced` (Full) |
| `action` | string | `cart` (default), `checkout` |
| `text_color`, `background_color` | colour | Hex string (e.g. `#ff0000`) |
| `font_size` | number (px) | Slider value |
| `font` | string | Font family — UI element exists in code but is hidden behind `{if 0}`, not exposed today |
| `cart_text_color`, `cart_background_color`, `cart_input_color`, `cart_background_input_color`, `cart_font` | colour / string | Cart drawer styling — only emitted when `action = cart` |
| `product_title_color`, `product_text_color`, `product_background_color`, `product_price_color`, `product_input_color`, `product_background_input_color` | colour | Product-card styling |
| `display_sku`, `display_properties`, `display_description`, `display_quantity` | bool | `1` to show, omitted to hide |

Invalid values for `template` and `action` silently fall back to `basic` and `cart` respectively (server-side defaulting).

## Settings & fields

The parameters group by builder accordion:

- **Button** accordion → `text_color`, `background_color`, `font_size` (+ the hidden `font`).
- **Product** accordion → the four `display_*` toggles + the six `product_*_color` keys.
- **Cart** accordion (shown only when `action = cart`) → `cart_text_color`, `cart_background_color`, `cart_input_color`, `cart_background_input_color`, `cart_font`.

The two structural keys, `template` and `action`, come from the top-level builder controls rather than an accordion.

## Business rules

### Defaults are stripped from the generated snippet

Any parameter whose value is empty / falsy is dropped from the `parameters` object before the snippet is rendered (via `array_filter`). A merchant who leaves all colour pickers at default sees a near-empty `parameters: {template: 'basic', action: 'cart'}`, not all ~18 keys with empty strings. A merchant who only changes the template type gets a 2-key snippet `parameters: {template: 'enhanced'}`. This is what allows the pasted snippet to stay a single-line readable script even with many controls available.

### Cart-styling keys only emit under the `cart` action

The five `cart_*` keys have no effect when `action = checkout` (there is no embedded cart drawer in that mode — see [[buy-button-embed-runtime]]). Accordingly the **Cart** accordion only appears in the builder when `action = cart`, and the cart keys are stripped from the snippet otherwise.

### The `font` parameter exists but is hidden (`{if 0}`)

The customization template has a `font` field gated behind `{if 0}` (always-false in Smarty), so the font-family picker is present in the code but not rendered in the UI today. If exposed, it would emit a `font` key on the snippet. This is a soft-deprecated control surface — listed here for completeness but not part of the current builder experience.

### Both surfaces normalise identically

The admin builder and the storefront [[buy-button-embed-runtime]] share the same normalisation logic: invalid `template` → `basic`, invalid `action` → `cart`, missing colour keys filled with empty strings (then stripped on output). So a hand-edited snippet with a garbage `template` still renders as `basic` rather than breaking.

## Related

- [[marketing-buy-button]] — hub.
- [[buy-button-builder]] — the accordions that set these parameters.
- [[buy-button-embed-runtime]] — the snippet's `parameters` object where these keys live.
- [[buy-button-checkout-link]] — the alternative flow, which carries no styling parameters.

## Open questions

No outstanding questions.
