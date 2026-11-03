---
type: entity
nav_path: "Entity → Vendor → Lifecycle"
aliases: ["Vendor lifecycle", "Vendor states", "Vendor delete blocked", "Vendor has products", "Vendor active flag", "Vendor webhooks", "Vendor events"]
tags: [entity, catalog, vendors, brands, lifecycle]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[vendor]]. See the hub for the other aspects (attributes, relationships, business rules).

# Vendor — Lifecycle

## Identity

The states a [[vendor|Vendor (Brand)]] moves through — Created, Live, Empty, Pre-delete, Deleted — and the two facts that surprise merchants most: there is **no Active / Inactive toggle** on the Vendor record, and **deletion is blocked at the model layer** while any product still references the vendor. This page also documents the save / delete events the platform fires so integrations can keep an external PIM / DAM in sync. The Assistant cites this page for *"Why can't I delete this brand?"*, *"How do I temporarily hide a vendor?"*, and *"Does deleting a brand notify my integration?"*.

## Aliases

- **Vendor lifecycle** / **Vendor states** — the Created → Live → Empty → Pre-delete → Deleted progression.
- **Cannot delete vendor — has products** — the merchant-facing error when deleting a vendor that still has products.
- **Vendor webhooks / events** — the `vendor.*` hook events fired on save / delete.

## Key Attributes

A Vendor moves through these states:

1. **Created** — the merchant clicked **+ Add vendor** on [[products-vendors]], filled in the Add modal, saved. The vendor becomes available in the product editor's vendor picker. Fires `vendor.created` webhook + `VendorCreated` internal event.
2. **Live** — the default state. The vendor's storefront landing page ([[storefront-vendor]]) is live; the brand surfaces on every assigned product's storefront page and product card. There is no Active / Inactive toggle in the data model — the vendor is either present in the catalog or not.
3. **Empty (zero products)** — the vendor exists but no [[product|Products]] currently reference its `vendor_id`. Identifiable via the **Has products: No** filter on [[products-vendors]]. Safe to delete (see [[vendor-entity-business-rules]] for bulk cleanup).
4. **Pre-delete (with products)** — the merchant clicks Delete on a vendor that still has products. The model-layer `deleting` hook **throws** *"Cannot delete vendor — has products"*. The merchant must first reassign every product to another vendor (or clear `vendor_id`) before the delete succeeds.
5. **Deleted** — the merchant successfully removed the now-empty vendor. Fires `vendor.deleted` webhook + `VendorDeleted` internal event. Products that had previously referenced the vendor are unaffected because they were reassigned before the delete.

### No `active` flag on the Vendor model

The Vendor record has **no `active` / `is_active` column** — there is no merchant-facing toggle to deactivate a vendor while keeping it in the database. The Vendor exists or it is deleted. Merchants who want to "hide" a vendor temporarily must either delete it (which requires reassigning all referencing products first — see deletion rule below) or rename it to mark it as deprecated. (Earlier wiki text implied an `active = no` soft-disable; that does not exist in the data model.)

### Delete is BLOCKED while products reference the vendor

The Vendor model's `deleting` hook **throws an error** when any [[product|Product]] still references the vendor — error key `vendor.err.cannot_delete_vendor_has_products`. The merchant cannot delete a vendor that still has products attached. The required flow:

1. Re-assign every product currently using this vendor to a different vendor (or clear the vendor reference).
2. Then delete the now-empty vendor.

The platform does **not** silently `SET NULL` the `vendor_id` on referencing products — the model-level guard fires first, before any FK cascade could run. The reassign-first workflow is documented in detail in [[vendor-entity-business-rules]].

### Lifecycle events + webhooks

Vendor save / delete fires three events to [[settings-hooks]] via the hook dispatcher AND three internal the application framework events:

| Event | When |
|-------|------|
| `vendor.created` (hook) + `VendorCreated` (internal) | New vendor saved. |
| `vendor.updated` (hook) + `VendorUpdated` (internal) | Vendor edited. |
| `vendor.deleted` (hook) + `VendorDeleted` (internal) | Vendor removed (only after the empty-vendor check passes). |

Useful for syncing the merchant's external PIM / DAM with the brand list. Because the `deleted` event fires only after the empty-vendor check passes, an integration listening to `vendor.deleted` never sees a delete that left orphaned product references.

## Where it appears

- [[products-vendors]] — where the merchant creates, edits, and (after reassigning products) deletes vendors; the **Has products** filter surfaces the Empty state.
- [[settings-hooks]] — the screen where the merchant subscribes an endpoint to `vendor.created` / `vendor.updated` / `vendor.deleted`.
- [[product]] — reassigning a product's vendor (the prerequisite for deletion) happens on the product editor.
- [[api-vendors]] — JSON-API v2 DELETE is subject to the same model-layer guard.

## Related

- [[vendor]] — hub.
- [[product]] — products must be reassigned off a vendor before it can be deleted.
- [[settings-hooks]] — the `vendor.*` webhook events fire here.
- [[seo-redirect]] — renaming a vendor (an alternative to deletion for "hiding") generates a 301 redirect.

## Open Questions

None.
