---
type: entity
nav_path: "Entity → Bundle → Relationships"
aliases: ["Bundle relationships", "Bundle associations", "Bundle and constituents", "Bundle cart item type", "Bundle is a product"]
tags: [entity, catalog, products, bundles, relationships]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[bundle]]. See the hub for the other aspects (attributes, lifecycle, component overrides, stock + activation, app + storefront).

# Bundle — Relationships

## Identity

How a Bundle connects to the rest of the catalogue: which entities it owns, which entities own it, how it appears as a special line in carts and orders, and which patterns are explicitly NOT supported. The Bundle entity sits on top of [[product|Product]], so it inherits product-level relationships AND adds the constituent-pivot relationship on top.

## Aliases

- **Bundle associations** — the entities a Bundle references or is referenced by.
- **Bundle cart-item** — the special cart row a Bundle becomes when added to a cart.
- **Bundle order line** — the consolidated order line a Bundle becomes after checkout.

## Key Attributes

A Bundle:

- **Has many** constituent [[product|Products]] via a pivot table — multi-select with per-item quantity, plus rich per-item overrides (catalogued in [[bundle-entity-component-overrides]]).
- **Is itself a** [[product|Product]] — the parent record has `type = 'bundle'`. It carries its own image, price, description, SEO, category assignments, vendor, tags, custom fields.
- **Belongs to** zero-or-more [[category|Categories]] — same category model as regular products. Bundles can be browsed under category pages.
- **Has many** [[file-asset|File Assets]] — main image plus optional gallery images.
- **Belongs to** one Bundles-app installation (the app must be installed for Bundles to exist; uninstalling does NOT auto-delete existing Bundles but hides the admin screens — see [[bundle-entity-app-and-storefront]]).
- **References** [[variant|Variants]] indirectly — when a constituent product has variants, the Bundle's pivot row specifies which variant (or accepts any). Stock derivation uses the specific variant's quantity.
- **Appears in** [[cart|Carts]] as a special Bundle cart-item type — a single cart line that internally holds references to all constituent products, NOT as N separate cart lines.
- **Appears in** [[order|Orders]] as one parent order line with a snapshot of the constituent breakdown; [[orders-ordered-products]] expands that breakdown for the admin.

A Bundle does NOT:

- Have its own independent stock count — availability is derived from constituents. See [[bundle-entity-stock-and-activation]].
- Support per-customer-group bundle pricing — single price per Bundle for all customers. To approximate per-group pricing, the merchant creates separate Bundles or uses a [[discount|Discount]] targeted at the customer group.
- Auto-generate from product associations — manual setup only. There is no "frequently bought together → make a Bundle" automation.
- Mix bundle stock with non-bundled stock independently — there's no separate "reserved for Bundles" inventory pool.

### How the Bundle appears in the Cart

When a customer adds a Bundle to the cart, it becomes a **single cart line** of the Bundle cart-item type — NOT N separate cart lines for the constituents. The cart line carries:

- The Bundle parent SKU + name + image + price.
- A nested list of the constituents with the per-row visibility flags applied (`visible_cart`, `hide_thumb`, `price_visible_cart`).
- A single quantity selector that scales every constituent together.

Changing the cart line's quantity from 1 to 2 doubles the stock consumed by every constituent — see [[bundle-entity-stock-and-activation]] for the decrement rule. Removing the cart line removes ALL constituents at once; the customer cannot remove one constituent from a Bundle (unless the merchant marked it `optional` — see [[bundle-entity-component-overrides]]).

### How the Bundle appears in the Order

After checkout, the Bundle persists as one parent order line with constituent rows snapshotted underneath. The admin [[orders-details]] screen shows the Bundle as a single line; [[orders-ordered-products]] expands it to show:

- Each constituent product (subject to `visible_order_details`).
- Each constituent's per-Bundle quantity × the order line quantity.
- Each constituent's snapshotted unit price.

The order snapshot freezes the Bundle's composition at order time, so later edits to the Bundle (adding / removing constituents, changing prices) do NOT alter past orders.

### Cross-entity relationships not via Product

A Bundle does NOT have first-class relationships to:

- [[customer]] / [[customer-group|Customer Groups]] — no per-group pricing or visibility filters at the Bundle level. Discount-code targeting via [[discount]] is the workaround.
- [[discount-code|Discount Codes]] — a discount code can still apply to the Bundle if its scope rule matches (because the Bundle is a Product), but there is no "Bundles-only" toggle on the discount-code side.
- **Subscriptions** — a Bundle is not natively a subscribable product. Subscription-box use cases reuse the Bundle entity for the merchandising layer but the recurring billing is handled by a separate app (see [[subscriptions]]).

## Where it appears

- [[bundles-list]] — primary admin list where the merchant manages the constituent multi-select per Bundle.
- [[cart]] — Bundle cart-item type with nested constituents.
- [[orders]] — Bundle parent line.
- [[orders-ordered-products]] — expanded constituent breakdown in admin.
- [[products-products]] — Bundles appear in the master product list (subject to per-screen filter).

## Related

- [[bundle]] — hub.
- [[product]] — Bundle inherits Product's schema and relationships.
- [[variant]] — constituents with Variants are referenced indirectly via the pivot.
- [[file-asset]] — Bundle gallery files.
- [[category]] — Bundle categorisation.
- [[cart]] — Bundle cart-item type.
- [[order]] / [[orders-ordered-products]] — Bundle order line + constituent breakdown.
- [[bundle-entity-component-overrides]] — per-row override columns that drive cart / order visibility.
- [[bundle-entity-stock-and-activation]] — how a Bundle cart-line's quantity scales constituent decrement.

## Open Questions

None.
