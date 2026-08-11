---
type: entity
nav_path: "Entity → Category → Lifecycle"
aliases: ["Category lifecycle", "Category states", "Category deletion", "Category depth cap", "Category save transitions"]
tags: [entity, catalog, categories, lifecycle, states]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[category]]. See the hub for the other aspects (attributes, relationships, business rules, side effects and API).

# Category — Lifecycle

## Identity

The named states a [[category|Category]] moves through during its life — from Draft (the merchant has opened the Add modal but not saved) through Active (saved, visible, holding products) to Deleted (the row is removed). Includes the **6-level depth cap** that blocks deeper nesting, the **deletion-blocked-while-products-remain** guard, and the save-time transitions that trigger search-index rebuild + URL-handle 301 redirects. Lifecycle state is **merchant-controlled** — there is no automatic expiry, scheduled-publish, or soft-delete window for categories.

## Aliases

- **Category lifecycle** / **Category states** — the named transitions.
- **Category deletion guard** — the "Cannot delete category. The category has products" block.
- **Depth cap** — the hard 6-level limit.

## Key Attributes

The lifecycle states (merchant-controlled, no automatic transitions):

| State | What it means | How to reach it |
|-------|---------------|-----------------|
| **Draft / In-creation** | The merchant has opened the create modal on [[products-categories]] but not yet saved. | Click "Add category" — the modal opens. |
| **Active** | Saved with at least a name. Appears in the admin list, is selectable when assigning products, and is visible on the storefront if at least one published product is assigned to it (otherwise it shows as empty / hidden depending on theme). | Save the create modal with a name filled in. |
| **Reorganised** | The merchant moves the category to a different parent via the Organize tab (drag-and-drop) or edits the parent on the edit form. The hierarchy is updated immediately; products inside come along. | Drag in Organize tab, or edit parent on the edit form. |
| **Renamed (URL handle change)** | The merchant changes the URL handle. The platform generates a 301 redirect entry from the old URL to the new one (see [[marketing-seo-301-redirects]]). Search engines and bookmarks continue to work. | Edit the URL handle and save. |
| **Deleted** | The category row is removed. Deletion is BLOCKED if the category still has products inside OR an active XML-import task is using it — see below. | Click Delete on a category with no products and no active import lock. |

## Save-time transitions

- **Search-index rebuild** — the storefront search index is rebuilt for the affected categories (so search reflects the new name / hierarchy).
- **Customer-cart cache flush** — any open customer carts have their cached cart-rule restrictions flushed, so per-category payment / shipping restrictions change immediately.
- **SEO cache invalidation** — the storefront SEO cache for the category page is invalidated.
- **URL-handle uniqueness** is enforced — the platform either appends a number suffix or rejects the save with a validation error if the slug already exists. The behaviour depends on entry path — see [[category-entity-business-rules]].
- **Hierarchy depth cap of 6 levels** — the `category_max_level = 6` constant blocks save when the move would push any descendant deeper. Error: *"Max depth is 6"*. See below.

For the full transactional sequence (validate → bump sort order → update parent → renumber siblings → rebuild path table → fire events), see [[category-entity-side-effects-and-api]].

## The 6-level depth cap

The platform enforces a **maximum nesting depth of 6 levels**. Attempting to create a 7-level subtree (via drag-drop on the Organize tab, the parent dropdown on the edit modal, or programmatic creation through CSV / XML import or [[api-categories]]) fails with *"Maximum depth is 6"*.

The depth check is `parent-count-of-target + max-child-count-of-moved-subtree`, so moving a 3-level subtree under a 4-level parent (3+4 = 7) is rejected even though each side individually fits the limit. Most stores naturally use 2-3 levels for storefront-UX reasons; the 6-level cap is a generous platform-side guard rail.

## Deletion is BLOCKED while products remain

Deleting a category with **products inside** is REJECTED with the error *"Cannot delete category. The category has products"*. The merchant must first re-assign every product out of the category (via bulk-edit on [[products-products]] with a category filter, or per-product) before the delete succeeds.

The same block also fires when an **active XML-import task** is using the category — the merchant must wait for the task to finish or remove the category from the task first. There is no built-in **merge** action ("transfer all products from category A to B then delete A") — the merchant must reassign products individually (or via bulk-edit) before deleting.

**Bulk-delete** has the same guard: bulk-deleting a category that contains products fails with the same error. The block applies regardless of whether the category has a parent — the platform never silently re-parents products. Bulk-delete via [[api-categories]] returns 422 with the same message.

## Image cleanup on delete

When a category row is deleted, the category's image file is **NOT** automatically deleted — the file becomes orphan in [[settings-files]] storage. Other cascade cleanup (path-table rows, restriction rows, webhook fire, downstream cache flush) IS automatic — see [[category-entity-side-effects-and-api]].

## URL-handle history (renames)

Each URL-handle rename writes a redirect entry into [[marketing-seo-301-redirects]]. There is no in-product UI to view the full history of past handles on a single category — the merchant inspects the SEO Redirects screen instead. Multiple renames stack: A → B → C means both `A → C` and `B → C` redirects exist (the platform forwards the chain).

## Where it appears

- [[products-categories]] — Add / Edit modal (create), Delete button (delete with guard), Organize tab (reparent / reorder).
- [[products-products]] — bulk-edit category re-assignment, which is the merchant's tool for emptying a category before delete.
- [[marketing-seo-301-redirects]] — where URL-handle rename redirects appear.
- [[settings-files]] — where orphan category images linger after delete.
- [[apps-csv-import]] — CSV / XML imports respect the 6-level cap and the deletion guard on the API path.
- [[api-categories]] — JSON-API v2 enforces the same lifecycle rules — see [[category-entity-side-effects-and-api]].

## Related

- [[category]] — hub.
- [[category-entity-business-rules]] — URL-handle 301 redirects, duplicate-handle behaviour (manual rejects, CSV / XML auto-suffixes).
- [[category-entity-side-effects-and-api]] — the transaction-bound reorder sequence + cascade cleanup on delete + JSON-API v2 parity.
- [[category-entity-relationships]] — what entities link to the category (and must be cleared / cascade-cleaned on delete).
- [[product]] — products must be re-assigned before category delete.
- [[marketing-seo-301-redirects]] — where URL-handle renames register.
- [[settings-files]] — orphan image file lives here after delete.

## Open Questions

- Confirm whether the depth-cap error message is exactly *"Max depth is 6"* vs *"Maximum depth is 6"* — the i18n key is `category.err.max_depth_is_6` but the surfaced label depends on locale (verify).
