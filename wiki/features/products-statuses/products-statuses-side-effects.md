---
type: feature
nav_path: "Products → Product statuses"
route_name: product-statuses-index
route_path: /admin/products/statuses
aliases: ["Product status save side effects", "Status delete cascade", "Status name unique", "Status cache flush", "Product status plan gate", "Product status permission"]
tags: [products, statuses, stock, customer-facing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---
# Product statuses — save / delete side effects, plan & permission

## Purpose

This aspect documents what happens **behind the scenes** when the merchant saves or deletes a product status: the storefront cache flush, the delete cascade that NULLs product references, the implicit normalisations on save, and the globally-unique name constraint. It also covers the plan gating (none) and the permission scope.

> Part of [[products-statuses]]. See the hub for the related aspects (list tables, modal, operators/actions, evaluation).

## Where to find it

These effects fire on Save / Delete actions on the Product statuses screen (Sidebar → Products → **Product statuses**).

## What the merchant can do here

- Save a status and have it apply to the storefront within one page load (no manual cache step).
- Delete a status; products that referenced it fall back to Conditional matching automatically.

## Settings & fields

### Globally-unique status name

The **Name** field has a UNIQUE constraint across all product statuses on the site. Two statuses cannot share the same name (case-insensitive). This makes the name usable as a stable key — when the merchant changes the displayed name, the storefront theme can rely on the name as that key.

## Business rules

### Implicit normalisations on save

The platform normalises a few fields automatically when a status is saved, so the merchant's modal choices store cleanly:

- If the operator dropdown is empty, the status is written as **Non-conditional** (the operator stores its non-conditional sentinel value).
- If the operator is one of the special non-value operators (**Not tracked** / **Continue selling**), the Quantity field is forced to NULL.
- If the Action type is NOT "Show as request" or "Show as subscribe for quantity", the Button text is forced to NULL.

### Storefront cache flush on save

There is a 1-day cache of the entire status list (cache key `product.status.new.2`). On every status **save or delete**, this cache is flushed — the new rules apply on the next storefront page load. The merchant does not need to take any cache action manually.

### Delete cascade — product references reset to NULL

When a status is deleted, **all products that had it as their manual in-stock (`status_id`) or out-of-stock (`out_of_stock_id`) reference are reset to NULL** for that field. Those products fall back to Conditional matching. This is silent — the merchant is not warned which products were affected, so deleting a widely-assigned status quietly changes many products' badges.

### Sort assignment on create

A new Conditional status is appended to the bottom of the sorted list (highest existing sort value + 1); the merchant drags it into place afterward. Non-conditional statuses get sort `0` and ignore the priority field — see [[products-statuses-list-tables]].

### No webhook fires directly

Status changes do NOT fire a webhook directly. The underlying **stock** change that triggers a status re-evaluation fires `product.updated` (see [[settings-hooks]]) — but editing the status taxonomy itself does not emit an event.

## Plan gates

This feature has **no plan-feature gate** — all plans (including the free / Start Up tier) can create unlimited Conditional and Non-conditional product statuses. The screen is governed only by the merchant's `products.statuses` permission scope.

Related plan-features influence WHAT a status can do, but not whether the screen is reachable:

- The **Continue selling** operator applies only to products whose product has the "Continue selling when sold out" flag ON, which is itself not plan-gated.
- The **Hide Buy button** action does not interact with the `hidden_products` plan feature (a per-product `hidden` flag governing whether the product appears in the storefront at all — see [[products-inventory]]).
- The **Show as subscribe for quantity** action depends on the back-in-stock subscription system ([[products-missing-product]]), which is also not plan-gated for read/write of subscriptions.

See [[plan-gates]] for the gating concept; [[plan-vs-feature-pack]] for the pack-vs-upgrade decision when a related product-side gate trips.

### Permission

This page requires the products / statuses permission section (`products.statuses`). Moderators without it cannot see the Product statuses sidebar entry.

## Related

- [[products-statuses]] — hub.
- [[products-statuses-modal]] — where the normalised values are entered.
- [[products-statuses-list-tables]] — sort assignment on create.
- [[products-statuses-evaluation]] — how the deleted-status fallback re-applies Conditional rules.
- [[products-missing-product]] — back-in-stock subscription system referenced by the Subscribe action.
- [[products-inventory]] — the `hidden` flag + "Continue selling" flag.
- [[settings-hooks]] — `product.updated` webhook fires on the underlying stock change.
- [[plan-gates]] — plan-gating concept.
- [[plan-vs-feature-pack]] — pack-vs-upgrade decision.
- [[product-status-lifecycle-management]] — the data-model lifecycle (create → delete) view.

## Open questions

None.
