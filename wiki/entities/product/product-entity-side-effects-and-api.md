---
type: entity
nav_path: "Entity → Product → Side effects and API"
aliases: ["Product save side effects", "Product webhooks", "product.created", "product.updated", "product.deleted", "Product API", "Product hard-delete cascade", "Product search re-index"]
tags: [entity, catalog, products, webhooks, api, side-effects]
plan_gates: ["products", "bundles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[product]]. See the hub for the other aspects (attributes, lifecycle, business rules, relationships).

# Product — Side effects and API

## Identity

Everything that happens when a [[product|Product]] is saved, deleted, or written through JSON-API v2 — the webhooks fired, the search-index refresh, the smart-collection re-evaluation, the cache invalidation, and the hard-delete cascade. This is the page to consult when a merchant asks *"Why didn't my webhook fire?"*, *"Why is the storefront still showing old data?"*, or *"What gets deleted when I delete a product?"*.

## Aliases

- **Save side effects** — what fires on every product save.
- **Hard-delete cascade** — the chain of cleanups on permanent deletion.
- **`product.*` webhooks** — `product.created`, `product.updated`, `product.deleted` events.
- **JSON-API v2 product resource** — programmatic access.

## Key Attributes

The triggering fields are documented in [[product-entity-attributes]]. The lifecycle states whose transitions drive side effects are in [[product-entity-lifecycle]].

## Save side effects (every product save)

Every save call — admin save, "Save and publish", inline edit, Bulk Edit, JSON-API v2 POST / PATCH, CSV / XML import — runs through the same product-save pipeline. The side effects:

- **Search re-index** — the storefront search index re-indexes the affected product chunked through the platform's search-sync job so storefront search reflects the change. The catalog and filter pages read from the search index, not the primary database, so the storefront reflects the change only after the search-sync queue processes the affected product. See [[storefront-architecture]] + [[background-queue-inventory]].
- **`product.created` / `product.updated` webhook** — webhooks subscribed via [[settings-hooks]] receive the payload. `product.updated` is **chatty** — fires on ANY field change (including stock decrement post-order). Receivers must be idempotent.
- **Smart-collection re-evaluation** — rule-based [[smart-collection|Smart Collections]] re-evaluate membership.
- **Cache invalidation** — product detail, containing-category listings, and search-result pages are invalidated.
- **Change-log entry** — every field change records into the per-product [[products-change-log|Change log]] with timestamp + Initiator (admin user / `api2` / import source / "Edit from order #N"). See [[inventory-debugging-playbook]].

## Webhook events (admin-panel changes only)

The `product.*` webhooks fire ONLY for admin-panel changes:

- `product.created` — on first save.
- `product.updated` — on any field change. **Chatty** — receivers must be idempotent.
- `product.deleted` — on hard-delete (after the 10-day soft-delete window expires, or on immediate permanent delete).

**Webhook caveat.** JSON-API v2 saves and the order-driven stock decrements **bypass** these webhook events. Receivers that need full coverage must combine the admin webhooks with API-side polling or inventory-specific signals. (verify)

See [[settings-hooks]] for subscription management.

## Hard-delete cascade

When a product is hard-deleted (either via the 10-day soft-delete window expiring or via immediate permanent delete), the platform:

- Deletes attached files.
- Deletes all variants.
- Deletes digital-file records.
- Deletes the product's image directory.
- Removes cart bundles where the product was the bundle parent.
- Clears change-log entries.
- Cancels pending queued jobs targeting this product.
- Fires `product.deleted` to subscribed webhooks.

See [[product-entity-lifecycle]] for the soft-delete window mechanics that precede this cascade.

## JSON-API v2 access

The Product entity can also be read, created, updated, or deleted via **JSON-API v2** — see [[api-products]] for the resource (name, type, descriptions, publish window, category / vendor references, SEO, tags, and the lifecycle states from [[product-entity-lifecycle]]). Variants nested under the product are exposed via [[api-variants]] — SKU, barcode, price, and quantity live there (NEVER on the Product itself), so most stock and pricing operations target the variant resource.

**Same side effects apply.** Every save through JSON-API v2 — POST / PATCH / DELETE — fires the same save-time pipeline documented above: search re-index always runs, smart-collection re-evaluation runs, the plan-feature `products` / `bundles` counter is checked at create, cache invalidation cascades to product / category / search pages, and the change-log records `api2` as the actor for support-ticket investigation.

**All hard caps enforce on the API path too:**

- 3 variant parameters per product (4th silently ignored).
- 500 variants per product on save.
- 100 tags per product, each ≤ 191 characters.
- 250,000-char description.
- 191-char name.
- Soft-delete 10-day window.
- The `physically` filter alias (filter-only, not a stored type).

See [[json-api-v2]] for authentication, rate limit, pagination, and the side-effects principle that applies to all resources.

## Plan-cap enforcement

At create time (admin or API), the plan-feature counter is checked:

- `products` counts all non-bundle products against the merchant's plan cap.
- `bundles` counts bundle-type products against a separate cap.

When the count hits the plan cap, the create call fails with a plan-upgrade prompt. Existing products continue to work — only NEW additions are blocked. See [[plan-gates]] + [[product-entity-business-rules]] for the merchant-facing behaviour.

## Where it appears

- [[products-products]] — admin save / create / delete flows.
- [[products-change-log]] — the audit trail showing every save's Initiator.
- [[settings-hooks]] — webhook subscription management for `product.*` events.
- [[api-products]] / [[api-variants]] — JSON-API v2 resources.
- [[apps-csv-import]] / [[apps-xml-sync]] — bulk-import paths that hit the same side-effect pipeline.

## Related

- [[product]] — hub.
- [[product-entity-attributes]] — fields whose changes trigger the side effects.
- [[product-entity-lifecycle]] — state transitions that drive create / delete events.
- [[product-entity-business-rules]] — validation that runs **before** side effects fire.
- [[settings-hooks]] — `product.created` / `product.updated` / `product.deleted` subscriptions.
- [[smart-collection]] — re-evaluated on every save.
- [[products-change-log]] — per-product audit log; cited in [[inventory-debugging-playbook]].
- [[api-products]] / [[api-variants]] / [[json-api-v2]] — programmatic-access resources and shared principles.
- [[storefront-architecture]] — why the storefront search can lag after a save.
- [[background-queue-inventory]] — the search-sync queue.
- [[plan-gates]] — `products` / `bundles` count caps checked at create.

## Open Questions

- Confirm exactly which JSON-API v2 endpoints **do** fire `product.*` webhooks vs which bypass them (verify — current claim is that admin-only fires).
- Confirm whether stock-decrement-only saves (no merchant-driven field change) skip the `product.updated` webhook or include it in the chatty stream (verify).
