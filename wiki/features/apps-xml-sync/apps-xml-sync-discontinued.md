---
type: feature
nav_path: "Apps → XML Sync → Discontinued handling"
route_name: apps.xml_sync
route_path: /admin/apps/xml_sync (disable_missings + cross-feed scoping)
aliases: ["XML Sync discontinued products", "XML Sync disable_missings", "XML Sync missing items", "XML Sync deactivate missing", "XML Sync re-activate returned", "XML Sync imports relation", "XML Sync imports_active", "XML Sync cross-feed scoping"]
tags: [apps, imports, xml, sync, recurring, deactivation, discontinued]
plan_gates: ["xml_sync_limit"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-xml-sync]]. See the hub for the other aspects (job pipeline, update policy, fetch transport, side effects).

# XML Sync — discontinued / missing-product handling

## Purpose

When a supplier drops a product from their feed, the merchant needs to decide what happens to the matching CloudCart product. XML Sync's answer is the **`disable_missings`** opt-in: products whose `product_map` value is no longer in the feed get **deactivated** (not deleted). This page documents that behaviour, the deactivate-vs-keep choice, the symmetric "re-activate when it returns" logic, and the `imports` / `imports_active` relations that scope deactivation so one supplier's sync never disables another supplier's products.

## Where to find it

- The **"Disable missing items"** toggle (`disable_missings`) is set on Step 1 of the [[apps-xml-sync]] wizard.
- The cross-feed linkage (`imports` / `imports_active`) is also configured on Step 1, but only appears when the merchant has linked [[apps-xml-import]] tasks in the same store.
- Resulting deactivations are visible in [[products-products]] (the product flips inactive) and in the run stats on [[apps-xml-sync-status]].

## What the merchant can do here

- Choose **Deactivate** (opt-in via `disable_missings`) or **Keep** (default) for products that vanish from the feed.
- Scope deactivation to specific linked import feeds so a sync only ever disables products it "owns".
- Have products **automatically re-activate** when they reappear in the feed (subject to the same scoping).

What the merchant **cannot** do here:

- Choose a **Delete** outcome — there is **no built-in "Delete"** for missing products. The only outcomes are Deactivate (opt-in) and Keep (default).
- Deactivate products belonging to a different (unlinked) supplier feed — the `imports` scoping prevents cross-feed collateral damage.

## Settings & fields

| Field | Where | Effect |
|-------|-------|--------|
| `disable_missings` | Step 1 toggle | When ON, products whose `product_map` value is absent from the latest feed are deactivated (variant inventory zeroed, parent product flipped inactive). When OFF (default), missing products are left untouched. |
| `imports` | Step 1 relation | Which [[apps-xml-import]] tasks the `disable_missings` deactivation is scoped to — only products that came from the LINKED import tasks can be deactivated. |
| `imports_active` | Step 1 relation | Which import tasks the "re-activate returned products" logic is scoped to — a returning product is reactivated only if it belongs to one of the linked imports. |

## Business rules

### `disable_missings` — opt-in deactivate, never delete

When enabled, after each run the platform sweeps products whose `product_map` column value is **not** in the latest feed and **deactivates** them: the variant inventory is zeroed out and the parent product is flipped inactive (hidden from the storefront). When the flag is OFF, missing SKUs are **left untouched** in CloudCart. There is **no Delete outcome** — the choice is Deactivate (opt-in) or Keep (default). Each deactivation is a product save and carries the usual downstream cost — see [[apps-xml-sync-side-effects]] for the search index / storefront-lag implications.

### Cross-feed scoping via `imports` / `imports_active`

When the merchant runs both [[apps-xml-import]] and XML Sync, a sync task can be **linked** to one or more import tasks:

- **`imports`** — scopes `disable_missings` deactivation so it only affects products that originated from the linked import tasks. Without this, a sync that didn't see SKU Y in its feed could wrongly deactivate SKU Y even though Y came from a different supplier.
- **`imports_active`** — scopes the **re-activation** of returned products. When a product reappears in the feed it is reactivated, but only if it belongs to one of the linked imports.

The linkage is the safeguard that lets a multi-supplier merchant run several feeds without one feed's "missing items" sweep clobbering another feed's catalog. It is configured on Step 1 when the linked tasks exist in the store.

### Symmetric re-activation

The deactivation is reversible by the feed itself: when a previously-missing product **returns** to the feed on a later run, it is reactivated automatically (scoped by `imports_active`). So a supplier temporarily dropping then restoring a product results in CloudCart deactivating then reactivating it — no manual intervention required, as long as `disable_missings` stays on and the scoping links are set.

## Related

- [[apps-xml-sync]] — hub.
- [[apps-xml-sync-update-policy]] — what a run changes on products that ARE present (the other half).
- [[apps-xml-sync-side-effects]] — the search index re-index + storefront lag triggered by each deactivation.
- [[apps-xml-sync-status]] — run stats showing how many products were deactivated.
- [[apps-xml-import]] — the import tasks that `imports` / `imports_active` link to.
- [[apps-xml-import-wizard]] — the sibling import's `disable_missings` toggle.
- [[products-products]] — products deactivated / reactivated.
- [[inventory-tracking]] — inventory model; variant inventory is zeroed on deactivation.

## Open questions

_None._
