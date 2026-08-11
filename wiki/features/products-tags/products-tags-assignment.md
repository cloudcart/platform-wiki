---
type: feature
nav_path: "Products → Tags → Per-product assignment"
route_name: products.tags
route_path: /admin/products/products/edit/:id (Tags section)
aliases: ["Product tag assignment", "Tag picker", "Assign tags to product", "Tags aside", "Прикачи тагове", "Тагове на продукт"]
tags: [products, tags, classification, taxonomy]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 8
---

# Product Tags — assignment & UI

> Part of [[products-tags]]. See the hub for the other aspects (data model, lifecycle, consumers + API).

## Purpose

This aspect covers **how the merchant attaches tags to a product** — the inline tag picker on the product editor, what the merchant can and cannot do there, and the bulk-tagging shortcut on the product list. Tags are free-form labels attached as a lightweight cross-cutting classification; see the hub [[products-tags]] for what they are and [[products-tags-data-model]] for how they are stored.

## Where to find it

Per-product tags are managed from the **product edit page**: [[products-products]] → click a product → **Tags** section in the right sidebar (Aside).

There is **no standalone "Tags list" page** in the admin — tags are managed per-product. The platform auto-aggregates the global tag set from per-product assignments. (Contrast with [[marketing-blog-tags]], which DOES have a central admin list.)

## What the merchant can do here

### Per-product tag assignment (no modal — inline tag picker)

In the product editor's Tags aside section:

- **Type-to-add** — start typing a tag name in the inline input field. The platform auto-suggests existing tags (matching what's typed) via the `/admin/api/core/product-tags/search` endpoint.
- **Pick from suggestions** — click an existing tag in the dropdown to attach.
- **Create new** — when no existing tag matches, pressing Enter creates a new tag (it appears as a fresh tag chip with the typed name). No "Create tag" modal — the resolver auto-creates on the next product save (see [[products-tags-lifecycle]]).
- **Remove** — click the × on a tag chip to unattach.

There is **no standalone "Tags" admin page**, no Add Tag modal, no Edit Tag modal, no Merge Tags modal. The tag taxonomy is entirely emergent from per-product assignments.

### Bulk tagging (via [[products-products]] bulk actions)

Multi-select products on the [[products-products]] list + bulk action "Add tag" / "Remove tag" (verify exact labels). Useful for seasonal cleanup. Bulk add / remove tags via the list page is the closest thing to centralised tag management.

### What the merchant CANNOT do here

- See a global Tags-management page (no centralised tag CRUD — tags emerge from per-product assignments).
- Define tag hierarchies (tags are flat).
- Set tag-level metadata (description, SEO, etc.) — tags are just labels. See [[products-tags-data-model]] for the dormant SEO columns.
- Bulk-rename a tag across all products without a workaround (typically: re-tag each product, or use [[apps-csv-import]]).

## Settings & fields

The Tags aside has a single control: the **inline tag input** (a multi-select chip field). There are no per-tag option fields, no description, no colour — typing resolves against the existing tag set and either attaches an existing tag or queues a new one for auto-create on save.

The autocomplete/search endpoint backing the input is `/admin/api/core/product-tags/search`. It is **not** permission-gated — any signed-in admin user can read tags for autocomplete; only create / update / delete require the `products.tags` grant (see [[products-tags-consumers-api]]).

## Business rules

- **Auto-create on assignment** — when the merchant types a new tag name and confirms, the platform creates the tag record on the next product save. No separate "create tag first" step. The full resolver mechanics (lowercasing, wildcard stripping, caps, deadlock recovery) are on [[products-tags-lifecycle]].
- **Permission** — editing tags follows the product-edit permission grant (standard `products` / `products.tags` scopes).
- **Side effects on tag change** — Smart Collections that reference the tag re-evaluate; Cart Rules that match the tag re-evaluate at next cart load; the storefront filter recomputes (cached). The downstream consumers are catalogued on [[products-tags-consumers-api]].
- **Distinct from blog tags** — [[marketing-blog-tags]] is a separate system (different table, different filter UI). A `summer` product tag is unrelated to a `summer` blog tag.

## Related

- [[products-tags]] — hub.
- [[products-products]] — products that get tagged; the bulk-tag actions live on its list page.
- [[products-categories]] — different concept (hierarchical structure).
- [[products-vendors]] — different concept (1:1 manufacturer).
- [[marketing-blog-tags]] — separate tag system for blog articles (has a central admin page; product tags do not).

## Open questions

- Exact labels and availability of the bulk "Add tag" / "Remove tag" actions on the [[products-products]] list (verify).
