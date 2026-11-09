---
type: entity
nav_path: "Entity → Product → Lifecycle"
aliases: ["Product lifecycle", "Product states", "Product draft", "Product hidden", "Product expired", "Product soft-delete", "Product scheduled publish"]
tags: [entity, catalog, products, lifecycle]
plan_gates: ["products"]
created: 2026-06-10
updated: 2026-11-09
source_count: 2
---

> Part of [[product]]. See the hub for the other aspects (attributes, business rules, relationships, side effects and API).

# Product — Lifecycle

## Identity

The set of merchant-controlled states a [[product|Product]] moves through from creation to permanent removal, the flags that distinguish each state, and the save-time transitions that flip between them. This is the page to consult when a merchant asks *"Why does my product not show on the storefront?"* or *"My deleted product is still in the list — what now?"*.

## Aliases

- **Product lifecycle** / **Product states** — the named states (Draft, Scheduled, Visible, Hidden, Expired, Out of stock, Soft-deleted, Hard-deleted).
- **Publish window** — the `publish_date` + `active_to` pair that defines visibility timing.
- **Temporary product** — an auto-created product, purged 10 days after it was created.

## Key Attributes

The driving fields are documented in [[product-entity-attributes]]. The state of a product is determined by the **combination** of these flags:

| State driver | Field(s) | Where it lives |
|---|---|---|
| Publish master switch | `active` | Product |
| Work-in-progress marker | `draft` | Product |
| Listing exclusion | `is_hidden` | Product |
| Future publish | `publish_date` (store timezone) | Product |
| Expiry | `active_to` (store timezone) | Product |
| Sellability at 0 stock | `tracking` + `continue_selling` + Variant `quantity` | Product + Variant |
| Soft-delete marker | `deleted_at` | Product |

## The eight states

1. **Draft** — `active = no`, `draft = yes`. Fully editable in admin. Storefront returns 404 on direct URL. Searchable in admin with the Draft filter. Can exist **without** a category.
2. **Scheduled** — `active = yes`, `publish_date` set in the future. Behaves as Draft on the storefront (excluded by the publish-date scope) until the scheduled time, then auto-flips to Visible.
3. **Visible (Active + Published)** — `active = yes`, `is_hidden = 0`, `publish_date` past, `active_to` not yet reached. The standard live state — discoverable via category browsing, search, and filters.
4. **Hidden** — `active = yes`, `is_hidden = 1`. Listed nowhere on the storefront but reachable via direct URL. Useful for private promotion campaigns where the merchant emails a direct link. See [[product-entity-business-rules]] for the Hidden vs Draft distinction.
5. **Expired** — `active_to` has passed. Excluded from storefront listings exactly like Draft. The merchant can extend by editing `active_to` to a future date.
6. **Out of stock** — `tracking = yes`, `continue_selling = no`, all variant `quantity = 0`. The product still appears on the storefront with the out-of-stock label + button, but cannot be added to cart. The merchant can override with a custom [[product-status|Status]] (e.g., "Notify me when back in stock"). See [[inventory-oversell]] for clamping at 0 (Variant `quantity` never goes negative).
7. **Deleted, awaiting removal** — `deleted_at` set and inactive. Removed from all listings AND admin views until the queued delete task removes it permanently.
8. **Hard-deleted** — Permanently removed. Triggers cascade cleanup — see [[product-entity-side-effects-and-api]].

## Publish window: `publish_date` + `active_to`

Both dates are interpreted in the **store's timezone**, normalised to UTC at minute precision before comparison.

- `publish_date` in the future → product behaves as Draft until that time, then auto-flips Visible.
- `active_to` set → product auto-flips out of Visible when that time passes (Expired).

The storefront product-detail page is hardened against direct-URL traffic outside the window — both Scheduled and Expired return 404 just like Draft.

## Save-time transitions

- Saving a product fires search re-index, `product.updated` webhook, smart-collection re-evaluation, and cache invalidation — see [[product-entity-side-effects-and-api]] for the full effect catalogue.
- The **"Save and publish"** button on Edit auto-flips Draft → Visible in one action; to save without publishing, the merchant must explicitly toggle Active OFF first.
- **Duplicating** a product clones content but resets the copy to `active = no` (Draft) by default — the duplicate never auto-republishes.
- **Bulk Publish** on [[products-products]] detects category-less drafts in the selection and forces the merchant to pick a category in a popup before the bulk publish proceeds — because publish requires at least one category (see [[product-entity-business-rules]]).
- **Bundle auto-deactivation** — flipping a regular product's `active` to `no` silently auto-deactivates every Bundle that includes it as a component, in the same save. Re-activating the product later does NOT auto-re-activate the Bundles — the merchant must explicitly toggle each Bundle's `active` back on. See [[product-entity-business-rules]].

## URL-handle changes generate 301 redirects

When the merchant edits `url_handle`, the previous handle is kept for **30 days** in a hidden history (not as an entry on the 301 Redirects screen); within that window the old URL 301-redirects to the new one ([[seo-301-redirects-auto-tracking]]). For longer, add a rule ([[seo-redirect]]).

## Deleting a product

Deleting from the admin (one product or many) immediately makes the product inactive and marks it deleted, which hides it everywhere; a queued background task then removes it permanently, with its images. A single delete through the Admin GraphQL API removes it at once. There is no trash, retention window or restore screen (the confirmation says the action cannot be undone); the only way back is a backup restore ([[settings-backups-partial-restore]]), which brings the record back but not its images. The **10-day** auto-delete applies only to *temporary* products, the auto-created ones the list marks with a clock icon and the tooltip *"Temporary product. Created on `<date>`. This product is auto deleted on `<delete_date>`."*

## Hard-delete cascade

Detailed in [[product-entity-side-effects-and-api]] — files, variants, image directory, cart bundles where the product was bundle parent, change-log entries, queued jobs targeting this product, and the `product.deleted` webhook.

## Where it appears

- [[products-products]] — list view, with filters for Draft, Hidden, Expired, and "Imported with".
- [[products-editor]] — the Active / Hidden / publish-date controls.
- [[products-bulk-actions]] — Bulk Publish + the category-picker popup for category-less drafts.
- [[products-change-log]] — every state change is recorded in the per-product Change log.

## Related

- [[product]] — hub.
- [[product-entity-attributes]] — the fields that drive each state.
- [[product-entity-business-rules]] — Hidden vs Draft, publish-requires-category, bundle auto-deactivation.
- [[product-entity-side-effects-and-api]] — what fires on each save / publish / delete transition.
- [[seo-redirect]] — the 301-redirect record created on URL-handle change.
- [[products-change-log]] — audit trail for lifecycle changes.
- [[inventory-oversell]] — Out-of-stock state semantics + 0-clamping.

## Open Questions

- Confirm whether Scheduled products surface on the **storefront sitemap** before `publish_date` arrives (verify).
