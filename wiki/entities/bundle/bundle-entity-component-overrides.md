---
type: entity
nav_path: "Entity → Bundle → Component overrides"
aliases: ["Bundle component overrides", "Bundle per-item overrides", "Bundle optional component", "Bundle individual price", "Bundle override title", "Bundle visibility scopes", "Bundle hide thumb"]
tags: [entity, catalog, products, bundles, overrides]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[bundle]]. See the hub for the other aspects (attributes, relationships, lifecycle, stock + activation, app + storefront).

# Bundle — Component overrides

## Identity

Each constituent row in a Bundle's component list supports more than just "product + quantity". A rich set of per-row override columns lets the merchant change a constituent's displayed title, price, description, and visibility independently per Bundle context — so the same product can appear as "Premium Camera Body" in one Bundle and "Canon EOS R5" on its own product page. This aspect catalogues every per-row override the merchant can configure.

The overrides are scoped to the **Bundle context only** — they do not affect the constituent's own standalone product page, cart line (when bought solo), or order line (when bought solo). They only change how the constituent appears when seen as part of THIS Bundle.

## Aliases

- **Per-component overrides** — the merchant-facing label.
- **Pivot row override fields** — the underlying per-row columns.
- **Bundle item overrides** — used interchangeably.

## Key Attributes

Each constituent row in the Bundle's component list supports these per-row overrides:

| Per-item override | What it controls |
|-------------------|------------------|
| **qty** | How many of this component the Bundle contains. Drives both the stock decrement (see [[bundle-entity-stock-and-activation]]) and the "savings vs individual" display calculation. |
| **optional** | Whether the customer can opt out of this component at checkout (e.g., "Buy the laptop + optional warranty"). |
| **individual_price** + **individual_price_enabled** | Override the displayed price of this component INSIDE the Bundle context (different from its standalone price on its own product page). |
| **discount** | Per-item discount displayed inside the Bundle. |
| **override_title** / **title** | Override the displayed name for this component in the Bundle context (e.g., "Premium Camera Body" vs the standalone "Canon EOS R5"). |
| **override_short_description** / **short_description** | Override the displayed description for this component in the Bundle context. |
| **hide_thumb** | Hide this component's thumbnail in the Bundle layout (useful for "free gift" items). |
| **visible_product_details** | Show / hide this component on the Bundle's product-detail page. |
| **visible_cart** | Show / hide this component in the cart line breakdown. |
| **visible_order_details** | Show / hide this component on the order-detail page (admin + customer email). |
| **price_visible_product_details** / **price_visible_cart** / **price_visible_order_details** | Independent toggles for hiding the per-item price separately from the item itself. |

### Three independent visibility scopes

The three `visible_*` fields target the three customer-facing surfaces where a constituent might appear, and they are **independent** — the merchant can show a constituent on the product-detail page but hide it from the cart and order-detail. Typical patterns:

- **Free gift hidden everywhere** — `visible_product_details = no`, `visible_cart = no`, `visible_order_details = no`, `hide_thumb = yes`. The constituent decrements stock and ships with the order but is invisible to the customer.
- **Mystery component (revealed at order time)** — `visible_product_details = no`, `visible_cart = no`, `visible_order_details = yes`. The customer doesn't know what's in the box until the confirmation email.
- **Full transparency** — all three `visible_*` flags `yes` (the default). The customer sees every component on every screen.

The three `price_visible_*` flags work in parallel — the merchant can show the component but hide its per-item price, useful when the Bundle's headline price is what the customer should focus on.

### The `optional` flag — and the flat-price gotcha

The per-component `optional` flag lets the customer opt out of a component at checkout (e.g., "Buy the laptop + optional warranty"). Toggling `optional` does **NOT** dynamically deduct the optional component's price from the Bundle total — the Bundle's headline price is flat.

To express "remove warranty to save 50 BGN", the merchant has two options:

1. **Expose `individual_price_enabled` per component** with explicit per-component pricing. The storefront then shows the per-component sum and the savings vs the Bundle headline. Removing the optional component visually reduces the per-component sum but does NOT reduce the Bundle headline.
2. **Build two separate Bundles** (with / without the optional component) at distinct headline prices.

Most merchants who reach for `optional` end up needing the two-Bundle pattern instead, once they realise the headline price doesn't dynamically adjust.

### `override_title` and `override_short_description` — Bundle-context names

Each pair of fields stores BOTH a "use override" toggle AND the override value:

- `override_title` (boolean) + `title` (string) — when `override_title = yes`, the Bundle's display uses `title`; otherwise the constituent's own product name is used.
- `override_short_description` (boolean) + `short_description` (rich text) — same pattern for the description.

This lets the merchant rename a product within a Bundle ("Premium Camera Body" instead of the technical SKU name) without altering the constituent's own product page. Subsequent edits to the constituent's product name do NOT propagate into the Bundle's override.

### `hide_thumb` for free-gift presentation

`hide_thumb` is a focused convenience flag — it suppresses the constituent's image in the Bundle layout WITHOUT also hiding the title or description. Common pattern: a "free gift" component with `hide_thumb = yes` so the layout focuses on the main product but the line "+ Free gift: branded tote bag" still shows under it.

When the merchant wants to hide the gift entirely (not even mention it on the product-detail page), `visible_product_details = no` is the broader flag — `hide_thumb` becomes redundant in that case.

### Per-Bundle defaults vs store-wide defaults

Some of these overrides have a corresponding store-wide default on [[apps-bundles-settings-new]] — show savings on the Bundle page, show constituent prices, customer-facing label localisation. When the per-row override is set, the per-row value wins; otherwise the store-wide default applies.

This is why a merchant who flips a store-wide toggle and sees only some Bundles change is not seeing a bug — the unchanged Bundles have per-row overrides that win against the new global default. Editing those Bundles row-by-row is the only way to bring them back under the global default.

## Where it appears

- [[bundles-list]] — opening a Bundle for edit exposes the per-row override controls under each constituent in the component list.
- [[apps-bundles-settings-new]] — store-wide defaults for the visibility / price-display behaviour that the per-row overrides take precedence over.
- Storefront product-detail / cart / order-detail surfaces — apply the `visible_*` and `price_visible_*` flags at render time.

## Related

- [[bundle]] — hub.
- [[bundle-entity-attributes]] — the pivot-row shape that hosts these override columns.
- [[bundle-entity-stock-and-activation]] — `qty` drives stock decrement; `optional` is documented here for the price-flatness gotcha.
- [[apps-bundles-settings-new]] — store-wide defaults that per-row overrides win against.

## Open Questions

None.
