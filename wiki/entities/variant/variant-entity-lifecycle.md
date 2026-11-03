---
type: entity
nav_path: "Entity → Variant → Lifecycle"
aliases: ["Variant lifecycle", "Variant states", "Variant creation", "Variant deletion", "Variant hide / show", "No per-Variant active flag"]
tags: [entity, catalog, variants, lifecycle]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[variant]]. See the hub for the other aspects (attributes, relationships, business rules, side effects and API).

# Variant — Lifecycle

## Identity

The full lifecycle of a [[variant|Variant]] record — how it gets created, the six states it transitions through, how it gets deleted, and the **no-per-Variant-active-flag** rule that forces the merchant to use indirect mechanisms (delete the Parameter Option, or `quantity = 0` with `tracking + no-continue-selling`) to hide a single combination from the storefront picker.

Variant lifecycle is largely **tied to the parent Product's lifecycle** — Variants are created and destroyed as a side effect of merchant actions on the Product (adding / removing Parameter Options, deleting the Product, etc.). The Variant itself is not directly created or destroyed from a dedicated screen.

## Aliases

- **Variant states** — the six configurations a Variant can occupy (Created, In stock, Out of stock, Oversellable, Always in stock, Deleted).
- **Variant deletion** — hard-delete; tied to Parameter Option removal or Product cascade.

## Key Attributes

The six states a Variant can occupy:

| # | State | Conditions | Storefront effect |
|---|-------|-----------|-------------------|
| 1 | **Created** | Row written. Either (a) auto-created as the single backing Variant when the merchant creates a simple product, or (b) auto-generated when the merchant adds a new Parameter Option to an existing parameter (one new Variant per combination involving that option). | N/A — initial state. |
| 2 | **In stock** | `quantity > 0` OR parent Product `tracking = no`. Default state. | Listable, buyable. Counted in [[product|Product]] `price_from` / `price_to`. Decremented when an order claims it (per [[inventory-decrement-timing]]). |
| 3 | **Out of stock** | Product `tracking = yes`, Product `continue_selling = no`, Variant `quantity = 0`. | Still appears in the picker with the out-of-stock label, but cannot be added to cart. Customer can join the back-in-stock waitlist (see [[products-missing-product]]). |
| 4 | **Oversellable** | Product `tracking = yes`, Product `continue_selling = yes`, Variant `quantity = 0`. | Remains buyable. The merchant tracks "how many units we owe" via outstanding paid orders, NOT a negative Variant count — see [[inventory-oversell]]. |
| 5 | **Always in stock** | Product `tracking = no`. Variant's `quantity` is ignored entirely. | Always buyable. Typical for digital products and services. |
| 6 | **Deleted** | Variant is removed — typically by removing a Parameter Option that was its identity, or by Product cascade-delete. | Hard-deleted alongside the Parameter Option removal. Order line items that referenced it keep their snapshotted SKU + label; `variant_id` may dangle (set NULL — see [[variant-entity-business-rules]]). |

## How a Variant gets created

- **Single backing Variant on simple products** — when the merchant creates a Product with no parameters, the platform auto-writes exactly one Variant row to carry `sku`, `barcode`, `quantity`, `price`, `weight`, etc. The merchant never sees this "Variant" in the UI — they just edit "the Product" — but the row exists.
- **Auto-generation from a new Parameter Option** — when the merchant adds an option (e.g., "XL") to an existing parameter ("Size") on a multi-variant Product, the platform auto-generates the new Variants for every combination involving "XL". For a 3-color × 2-size product becoming 3-color × 3-size, 3 new Variants appear.
- **Bulk via CSV import** — [[apps-csv-import]] can create Variants in bulk; the SKU column is the join key. The bulk path skips duplicate-SKU rows silently rather than failing the whole import (see [[variant-entity-business-rules]]).
- **Via JSON-API v2** — POST under a parent product (no standalone create). See [[variant-entity-side-effects-and-api]].

## How a Variant gets deleted

- **Parameter Option removal** — when the merchant deletes a Parameter Option, every Variant referencing that option ID is hard-deleted. The Variant's child tables (`ImageVariant`, external-meta-data rows) are removed first via the model's `deleting` hook — see [[variant-entity-business-rules]].
- **Product cascade-delete** — when the parent Product is hard-deleted, every Variant under it goes too.
- **Direct delete via JSON-API v2** — possible; same cascade behaviour as Parameter Option removal.

In all cases, **historical order line items survive**: the order's `variant_id` foreign key is set to NULL via `ON DELETE SET NULL`, and the order retains the snapshotted SKU + label text so the order remains readable. See [[variant-entity-business-rules]].

## No per-Variant `active` flag — the hide workarounds

The Variant table has **no `active` column** (verify — confirmed: there is no per-Variant visibility toggle). To hide a single combination from the storefront picker, the merchant has two indirect mechanisms:

1. **Delete the Parameter Option** — removes the Variant entirely. Destructive; affects every Product that uses that option. Use only when the option is genuinely retired catalogue-wide.
2. **Set `quantity = 0` with `tracking = yes` and `continue_selling = no`** — non-destructive. The Variant still appears in the picker but greyed out / unavailable, and a customer can join the back-in-stock waitlist for it. Restocking later restores buyability automatically.

Setting the parent Product's `active = no` is a different operation — it hides EVERY Variant of the product (the Product becomes a Draft, the storefront URL returns 404).

## Where it appears

- [[products-variants-options]] — Parameter Option management; option add / delete is the indirect Variant-create / Variant-delete trigger.
- [[products-products]] — the Product editor's Variants tab; per-Variant edits here.
- [[products-inventory]] — per-Variant `quantity` edits drive the In-stock / Out-of-stock / Oversellable transition.
- [[products-missing-product]] — back-in-stock waitlist; the restock from Out-of-stock back to In-stock triggers the waitlist email batch (see [[variant-entity-business-rules]]).

## Related

- [[variant]] — hub.
- [[product]] — parent record; Product lifecycle drives Variant lifecycle in the cascade direction.
- [[product-option]] — Parameter Option; adding / deleting options is the indirect Variant-create / Variant-delete trigger.
- [[inventory-tracking]] — the full inventory model; states 2–5 above are determined by the three master switches plus per-Variant `quantity`.
- [[inventory-variant-model]] — the per-Variant `quantity` rule + the `tracking` / `continue_selling` / `threshold` switches.
- [[inventory-decrement-timing]] — when stock decrements drive a Variant from state 2 → state 3 / 4.
- [[inventory-restock]] — when stock returns drive a Variant from state 3 / 4 back to state 2.

## Open Questions

None.
