---
type: entity
nav_path: "Entity → Category → Side effects and API"
aliases: ["Category side effects", "Category webhooks", "Category JSON-API v2", "Category cascade cleanup", "Category path table rebuild", "Tree reorder atomicity"]
tags: [entity, catalog, categories, side-effects, api, json-api-v2]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[category]]. See the hub for the other aspects (attributes, lifecycle, relationships, business rules).

# Category — Side effects and API

## Identity

What fires when a [[category|Category]] is created, updated, reorganised (via drag-drop or parent edit), or deleted — the **transaction-bound** tree-reorder sequence, the materialised `category_paths` rebuild that keeps subtree queries fast, the cascade cleanup on delete, the downstream events (search re-index, customer-cart cache flush, SEO cache invalidation, `category.*` webhook fire), and the JSON-API v2 surface that exposes the same operations programmatically. This is the page the AI Assistant cites when a merchant asks *"What happens when I move a category?"* or *"Why did my checkout cart restrictions update right after I edited the category?"*.

## Aliases

- **Category side effects** — the chain of events fired on save / delete.
- **Tree reorder atomicity** — the transaction-bound drag-drop sequence on the Organize tab.
- **Materialised path rebuild** — the `category_paths` sync on parent change.
- **`category.*` webhooks** — `category.created` / `category.updated` / `category.deleted` events to [[settings-hooks]] subscribers.

## Key Attributes

### Tree-reorder atomicity (Organize tab drag-drop)

Each drop triggers a transaction-bound sequence:

1. **Validate** — target exists, target is not the moved category itself, target is not a descendant of the moved category, resulting depth ≤ 6, name unique in destination sibling group.
2. **Bump destination siblings' sort `order`** to make room for the dropped category.
3. **Update the moved category's `order` + `parent_id`**.
4. **Renumber** the sort `order` for ALL siblings of both the source parent AND the destination parent to keep numbering contiguous (1, 2, 3, ...).
5. **Rebuild the materialised path table** for the moved category AND every descendant (recursive).

Any failure rolls back the whole drop — the tree appears unchanged and the merchant sees an inline error. Same validation enforces on the JSON-API v2 path — see below.

### Materialised category path rebuilt on create + update

The platform maintains a denormalised `category_paths` table holding every ancestor → descendant pair (used by the storefront for fast subtree-product queries — e.g. "show me everything under Electronics" without walking the `parent_id` chain). Two save-time triggers keep this table in sync:

- **On create** — ancestor rows for the new category are inserted in one batch. A child appearing under "Electronics → Phones" gets paths for "Electronics" and for "Phones" inserted.
- **On parent change** — when the merchant moves a subtree (`parent_id` changes), the platform re-walks the affected branch and rewrites every descendant's path table to reflect the new ancestry chain.

Both triggers also fire the `category.created` / `category.updated` webhook event and dispatch the dedicated the application framework events for downstream listeners (cache flush, search reindex, smart-collection recompute). See [[settings-hooks]].

### Cascade cleanup on category delete

When a category row is deleted (after the deletion guard's "has products?" check passes — see [[category-entity-lifecycle]]), four cleanups run:

- **Fire `category.deleted`** event AND the dedicated the application framework event (downstream listeners: storefront cache flush, search index sync, smart-collection invalidation, redirect cascade).
- **Delete every `category_paths` row** referencing this category (both as ancestor and as descendant).
- **Delete every restriction row** (per-category payment / shipping rules) tied to this category.
- **Propagate the `category.deleted` webhook** to [[settings-hooks]] subscribers.

What is **NOT** cascade-cleaned:

- The **category image file** — orphan in [[settings-files]] storage. See [[category-entity-lifecycle]].
- The **products** that were assigned to the category — the deletion guard requires them to be re-assigned manually first, so by the time delete runs there are zero products to worry about.
- The **301 redirect entries** in [[marketing-seo-301-redirects]] for any past URL-handle rename — they remain, so external bookmarks of the renamed handle still forward (though to a now-404 final destination).

### Save-time side effects

Every save (create / update) — whether from the Add / Edit modal, the drag-drop reorder on the Organize tab, CSV / XML import, or JSON-API v2 — triggers:

- **Storefront search-index rebuild** for the affected categories, so search reflects the new name / hierarchy.
- **Customer-cart cache flush** so cart-rule restrictions change immediately (the cached "allowed payment methods" / "allowed shipping methods" lists are invalidated).
- **SEO cache invalidation** for the category page.
- **`category.created` / `category.updated` webhook event** to [[settings-hooks]] subscribers.
- **301-redirect entry creation** in [[marketing-seo-301-redirects]] when `url_handle` changes.

## Programmatic access (JSON-API v2)

The Category entity can also be read, created, updated, or deleted via **JSON-API v2** — see [[api-categories]] for the resource (name, parent_id, description, image, `taxonomy_id`, `display_child`, `make_interval`, SEO fields, URL handle, and the M2M payment / shipping provider attachments).

**Same side effects apply.** A POST / PATCH / DELETE through JSON-API v2 fires the same lifecycle work as the admin Save:

- Search-index rebuild.
- Customer-cart cache flush.
- Materialised path-table rebuild for the moved subtree (when `parent_id` changes).
- `category.*` webhook fire to [[settings-hooks]] subscribers.
- 301-redirect entry creation when `url_handle` changes.

**Same validation.** The transaction-bound drag-drop reorder validations (target exists, not self, not own descendant, depth ≤ 6, sibling-scoped name uniqueness) all enforce on the API path too — invalid payloads return 422 with the same error messages.

**One difference from the admin form**: duplicate `url_handle` is REJECTED with a validation error on the admin Add / Edit modal but SILENTLY auto-suffixed (`-1`, `-2`, ...) on the CSV / XML import path. JSON-API v2 mirrors the **admin behaviour** — duplicate handles return 422, not auto-suffixed. See [[category-entity-business-rules]] for the full duplicate-handle matrix.

**Deletion is BLOCKED while products remain inside the category** — the API returns 422 with the *"Cannot delete category. The category has products"* error, identical to the admin block. The same XML-import lock applies. Multi-language naming, the 6-level depth cap, and the orphan-image-on-delete behaviour all apply on both paths.

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Webhook chattiness considerations

- `category.updated` fires on **every** save — including drag-drop reorders that touch many siblings. Receivers must be idempotent.
- `category.created` and `category.deleted` are once-per-event (no double-fire on transactional rollback — the events emit only after commit).
- Webhook subscribers see the new state in the payload but must read related entities (products in the category, attached properties) via separate API calls if needed.

## Where it appears

- [[products-categories]] — the Add / Edit modal + drag-drop on the Organize tab triggers everything above.
- [[settings-hooks]] — where merchants subscribe to `category.*` events.
- [[api-categories]] — JSON-API v2 endpoint definition.
- [[json-api-v2]] — programmatic-access hub.
- [[marketing-seo-301-redirects]] — receives URL-handle rename entries.
- [[apps-csv-import]] — the import path that triggers the same side effects (with the duplicate-handle auto-suffix exception).
- [[settings-files]] — where the orphan category image remains after delete.

## Related

- [[category]] — hub.
- [[category-entity-lifecycle]] — the deletion guard runs **before** the cascade cleanup described here.
- [[category-entity-business-rules]] — duplicate-handle behaviour (manual vs CSV/XML vs API).
- [[category-entity-attributes]] — `category_path.level` field driven by the materialised path table.
- [[category-entity-relationships]] — the entities cascade-cleaned on delete (path rows + restriction rows).
- [[api-categories]] — JSON-API v2 resource.
- [[json-api-v2]] — programmatic-access hub.
- [[settings-hooks]] — webhook subscription management.
- [[marketing-seo-301-redirects]] — URL-handle rename history.

## Open Questions

- Confirm whether `category.updated` fires once per Organize-tab drag or per sibling renumber within the same transaction (verify).
