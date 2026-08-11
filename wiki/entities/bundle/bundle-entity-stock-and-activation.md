---
type: entity
nav_path: "Entity → Bundle → Stock and activation"
aliases: ["Bundle stock derivation", "Bundle decrement", "Bundle active scope", "Bundle constituent decrement", "Bundle availability", "Bundle worst-stocked component"]
tags: [entity, catalog, products, bundles, stock, activation]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[bundle]]. See the hub for the other aspects (attributes, relationships, lifecycle, component overrides, app + storefront).

# Bundle — Stock and activation

## Identity

How a Bundle's availability and stock-decrement behaviour work. A Bundle has no `quantity` column of its own — its sellability is derived from the constituents at storefront-render time and at cart-add time. When a customer buys a Bundle, each constituent product's stock decrements; restock / cancel returns stock per constituent. The active-scope SQL on the storefront filters Bundles by the `active AND non-draft` state of EVERY constituent, independent of the Bundle's own `is_active` flag.

This aspect catalogues the derivation rule, the per-constituent decrement on checkout, the active-scope SQL, and the dangling-component edge case after constituent deletion.

> **See also [[inventory-bundle-stock]]** — the canonical inventory-side aspect for the min-across-children rule and the child-flag-wins behaviour. This page is the Bundle-entity-side view of the same mechanics, focused on activation cascades and order-time decrement.

## Aliases

- **Bundle availability** — the storefront in-stock / out-of-stock decision.
- **Worst-stocked component rule** — the minimum-quantity-across-components calculation.
- **Active-scope SQL** — the storefront query that filters Bundles by constituent state.
- **Constituent decrement** — the per-component stock drop on checkout.

## Key Attributes

### Stock is derived, never independent

A Bundle has no `quantity` column of its own. Its availability is computed at storefront-render time and at cart-add time as the **lowest available quantity** across constituents, accounting for the per-component `qty`:

```
bundle_units_available = min( constituent_quantity / per_bundle_qty ) across all constituents
```

So a Bundle that needs 2 cameras + 1 lens has `min(cameras / 2, lenses / 1)` units available. If ANY constituent is at zero AND "Continue selling" is off on that constituent, the Bundle is unavailable.

The storefront does NOT display a numeric "X Bundles available" anywhere — the check is **binary** (in stock / out of stock). The merchant who wants a numeric count has to compute it manually from the constituent stocks. See [[inventory-bundle-stock]] for the full inventory-side semantics.

### Buying a Bundle decrements EACH constituent

When a customer checks out with a Bundle, the order decrements EACH constituent product's stock by the Bundle's per-component `qty` × the order line quantity. The order line records the Bundle as the parent SKU plus internal references to the components. The merchant's [[orders|Orders]] view shows the Bundle as one line; [[orders-ordered-products]] expands it to show the constituent breakdown.

The decrement follows the standard [[inventory-decrement-timing]] rules — whether it happens on `paid` or `pending` is controlled by the store-wide setting, the same as for non-bundled products. Cancel / refund returns each constituent's stock per [[inventory-restock]].

### Active-Bundle scope requires every constituent to be Active AND non-Draft

The storefront query that decides whether a Bundle is "live" runs a SQL subquery counting the Bundle's constituent products and comparing that count against the count of constituents where `active = yes` AND `draft = no`. If even one constituent fails either check (deactivated, soft-deleted, or never published), the Bundle is excluded from the active-Bundles set on the storefront — **independently** of the Bundle's own `is_active` flag.

So a merchant who toggles a single component to "Draft" effectively kills every Bundle that uses it, even if the Bundle row still shows `is_active = yes` in the admin. This is a common source of *"my Bundle disappeared from the storefront but I didn't touch it"* support tickets — the merchant changed the constituent's draft / active state and the Bundle silently dropped from the listing.

### Auto-deactivation propagation runs on every Product save

When the merchant deactivates a constituent product (sets `is_active = false`), the platform automatically flips `is_active = false` on every Bundle that includes that product as a component. This cascade runs as a side effect of the constituent product's save whenever `active` changes — **no explicit Bundle save is required**. The merchant sees the side effect after the save (Bundles dropped from the storefront listing) without any UI confirmation.

The cascade is **one-way**: re-activating the constituent does NOT auto-re-activate the Bundle. See [[bundle-entity-lifecycle]] for the full state-transition catalogue and the asymmetry rationale.

### Constituent deletion does NOT auto-delete the parent Bundle

Deactivation of a constituent product auto-deactivates the parent Bundle (above), but **deletion** of a constituent does NOT delete the parent. The Bundle survives with a now-dangling component reference; storefront-render-time stock derivation fails for that component and the Bundle is shown as unavailable.

The merchant must manually edit the Bundle to remove the deleted component or delete the Bundle itself. Until then, the Bundle exists in a broken state — visible in the admin list with `is_active = yes`, but never sellable on the storefront. There is no admin warning at constituent-delete time `(verify)`.

### Child-flag-wins for `continue_selling`

Even if the Bundle parent has `continue_selling = yes`, a child with `tracking = yes`, `continue_selling = no` and `quantity = 0` makes the Bundle out-of-stock. **The child flag wins** — the opposite of how merchants usually expect Bundle aggregation to work. See [[inventory-bundle-stock]] for the full rule.

Common merchant confusion: *"I turned on Continue selling on my Bundle but it still shows out-of-stock — why?"* — answer: at least one constituent has `continue_selling = no` AND has run out.

### Bundle as a Product means standard product features apply (stock-wise too)

Because the Bundle is technically a Product record, Bundles **DO** count toward catalogue plan gates that count products (XML-sync row caps, category-listing scans, the search index indexing), they are NOT exempt. The dedicated `bundles` plan cap (see [[bundle-entity-app-and-storefront]]) limits HOW MANY Bundles the merchant can create, but does NOT exempt those Bundles from other product-related caps further down the pipeline.

## Where it appears

- Storefront product card / detail page — runs the stock-derivation check at render time.
- Storefront cart / checkout — re-validates each constituent has enough stock when the customer adds a Bundle or submits an order.
- [[orders-details]] — fulfilment status changes that hit the decrement-timing trigger fire per-constituent decrements.
- [[products-products]] — deactivating a constituent product from this screen fires the auto-deactivation cascade silently.
- [[bundles-list]] — Bundle list reflects `is_active` but does NOT reflect derived out-of-stock state (that's a storefront-render concern).

## Related

- [[bundle]] — hub.
- [[bundle-entity-lifecycle]] — the six named states, the asymmetric cascade, the cart-cleanup-on-delete behaviour.
- [[inventory-bundle-stock]] — canonical inventory-side aspect: min-across-children + child-flag-wins.
- [[inventory-decrement-timing]] — when constituent stock actually drops (paid vs pending).
- [[inventory-restock]] — symmetric stock return on cancel / refund / void.
- [[inventory-oversell]] — `continue_selling` semantics at the per-constituent level.
- [[product]] — the constituent-side `active` and `draft` flags that feed the active-scope SQL.
- [[orders-ordered-products]] — per-order constituent breakdown.

## Open Questions

- ⏸️ Whether the admin shows a warning when deleting a constituent product that participates in active Bundles `(verify)`.
- ⏸️ Whether the active-scope SQL also accounts for `is_archived` or only `active` + `draft` `(verify)`.
