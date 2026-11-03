---
type: entity
nav_path: "Entity → Bundle → Lifecycle"
aliases: ["Bundle lifecycle", "Bundle states", "Bundle draft to active", "Bundle deactivation", "Bundle deletion", "Bundle out of stock state"]
tags: [entity, catalog, products, bundles, lifecycle, states]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[bundle]]. See the hub for the other aspects (attributes, relationships, component overrides, stock + activation, app + storefront).

# Bundle — Lifecycle

## Identity

The state machine a Bundle record passes through — from Draft creation, through Active publishing, through derived Out-of-stock (when a constituent runs out), through Auto-deactivated (when a constituent is unpublished), through Inactive (manual toggle), all the way to Deleted. Also documents the **asymmetric** one-way auto-deactivation cascade and what happens to active carts when a Bundle is deleted.

## Aliases

- **Bundle states** — the six named states a Bundle can occupy.
- **Bundle activation** / **deactivation** — the `is_active` toggle transitions.
- **Auto-deactivation cascade** — the constituent → Bundle propagation.

## Key Attributes

The six merchant-controlled states:

| State | How to recognise | What it means |
|-------|------------------|---------------|
| **Created (Draft)** | `is_active = false`, freshly created | The merchant has clicked **+ Create bundle** on [[bundles-list]], filled name + image + price + components + description + SEO, saved. The Bundle exists in the catalogue but is invisible on the storefront. |
| **Active** | `is_active = true` AND all constituents in stock (or "Continue selling" enabled) AND all constituents active+non-draft | Visible on the storefront, addable to cart. |
| **Out of stock (derived)** | `is_active = true` BUT at least one constituent has `quantity = 0` AND `continue_selling = no` | The Bundle disappears from the storefront / shows as unavailable. The Bundle's own `is_active` flag is STILL `true`; only the derived availability flipped. Once the constituent is restocked, the Bundle reappears automatically. |
| **Auto-deactivated** | `is_active = false`, flipped by the platform | A constituent product was deactivated. The platform auto-flipped this Bundle's `is_active` to false. **NOT symmetric**: re-activating the constituent does NOT auto-re-activate the Bundle. The merchant must manually toggle it back on. |
| **Inactive** | `is_active = false`, set manually by the merchant | Invisible on the storefront, cannot be added to cart. Existing carts containing the Bundle keep it until checkout. |
| **Deleted** | Record removed from `bundles-list` | Active carts have the Bundle line removed (the constituent items are NOT auto-added as separate lines). Customers see it disappear on next page load. The Bundle URL returns the storefront's 404. |

### The asymmetric one-way deactivation cascade

When the merchant deactivates a constituent product (sets `is_active = false` on the product editor), the platform automatically flips `is_active = false` on every Bundle that includes that product as a component. This prevents a Bundle from being purchasable when one of its components is no longer being sold.

**The reverse is NOT symmetric**: re-activating the constituent does NOT auto-re-activate the Bundle. The merchant must manually flip the Bundle's `is_active` back on. The intent: re-activating one component doesn't necessarily mean the merchant wants the Bundle re-listed — the merchant explicitly opts in.

The asymmetry is the single most-confusing part of the lifecycle for support tickets — *"I un-archived the product, why is my Bundle still hidden?"* — the answer is always: open the Bundle and toggle it active again.

### Auto-deactivation propagation runs on every Product save

The constituent → Bundle cascade does NOT require an explicit Bundle save — it runs as a side effect of the constituent product's save whenever `active` changes. The merchant editing a regular product sees the side effect after the save (Bundles dropped from the storefront listing) without any UI confirmation. See [[bundle-entity-stock-and-activation]] for the full active-scope SQL that also factors `draft` state.

### Cart cleanup on Bundle delete

When the merchant deletes a Bundle from [[bundles-list]], the platform removes all Bundle cart-items for that Bundle from active carts. Customers with the Bundle in their cart see it disappear on next page load — the constituent items are NOT auto-added as separate lines. The merchant should warn customers (or accept silent disappearance) when retiring a popular Bundle.

This differs from the [[product|Product]] delete behaviour: deleting a regular product removes its cart lines too, but a Bundle delete also leaves no breadcrumb of the constituents (because the constituents themselves still exist; the customer just lost the bundled-price packaging).

### Constituent deletion vs constituent deactivation

These two are **NOT** equivalent for the Bundle:

- **Constituent deactivation** (`is_active = false` on the constituent) — auto-deactivates the parent Bundle as above.
- **Constituent deletion** (constituent removed from the catalogue) — does NOT delete the parent Bundle. The Bundle survives with a now-dangling component reference; storefront stock derivation fails for that component and the Bundle is shown as unavailable. The merchant must manually edit the Bundle to remove the deleted component or delete the Bundle itself.

This means cleaning up stale Bundles is a manual chore after a product cull. There's no admin warning when deleting a product that is part of an active Bundle `(verify)`.

### Out-of-stock is recoverable, Auto-deactivated requires a manual click

The key practical difference: an Out-of-stock Bundle **self-recovers** when its worst-stocked constituent is restocked. An Auto-deactivated Bundle does NOT self-recover even when every constituent is back to active state — the merchant must manually click the active toggle on the Bundle. Merchants should not assume "re-activating the products brings the Bundles back".

## Where it appears

- [[bundles-list]] — shows the Bundle's `is_active` toggle and lets the merchant flip it manually.
- [[products-products]] — Bundles appear here too (they're Products); deactivating a constituent product fires the auto-deactivation cascade from this screen.
- [[cart]] — Bundle cart-items are removed when the Bundle is deleted.

## Related

- [[bundle]] — hub.
- [[bundle-entity-stock-and-activation]] — the full active-scope SQL (`active AND non-draft` constituents) + the dangling-component edge case.
- [[product]] — the constituent-side `is_active` toggle that triggers the cascade.
- [[cart]] — Bundle cart-item cleanup on Bundle delete.
- [[bundles-list]] — primary admin lifecycle controls.

## Open Questions

- ⏸️ Whether the admin shows any warning when deleting a constituent product that participates in active Bundles `(verify)`.
