---
type: feature
nav_path: "Products → Categories"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Categories", "Category tree", "Product categories", "Категории", "Категории на продуктите"]
tags: [products, categories, taxonomy, navigation]
plan_gates: ["categories", "category_properties"]
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---

# Categories

## Purpose

The screen where the merchant defines the **category hierarchy** that organises every product in the store. Categories are the merchant's primary navigation taxonomy — the structure customers browse on the storefront, the filter that scoping rules (taxes, discounts, payment methods, shipping methods) reference, and the grouping the merchant uses to find products in the admin.

The page has two tabs — a **List** view for create / edit / delete and a **drag-and-drop Organize** tree — sharing one Add-category modal that covers name, description, image, parent, Google Shopping taxonomy, per-category payment / shipping overrides, technological delivery time, and SEO fields. Underneath the screen, a 6-level depth cap, a sibling-scoped name-uniqueness rule, a materialised-path table, a delete-blocked-when-products-remain safety rule, and a JSON-API v2 surface that mirrors the admin behaviour all enforce the same model. Each of these is its own page in the cluster below.

## Where to find it

Sidebar → Products → **Categories**.

The page's breadcrumb reads "Products → Categories". The route is `/admin/products/categories`. The header icon is the list-alt icon.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[products-categories-list-organize]] — the List + Organize tabs: table columns, filters, bulk-delete, tree-node controls, drag drop targets (`before` / `after` / `inside`).
- [[products-categories-edit-modal]] — the Add / Edit `xl` modal: General / Logo / Taxonomy / Cart rules / Advanced sections + full field map.
- [[products-categories-hierarchy-rules]] — the 6-level depth cap, sibling-scoped name uniqueness, tree drop validations (self / descendant / name-clash), atomicity of every drop, materialised-path mechanics.
- [[products-categories-cart-restrictions]] — `Define custom payment / shipping methods` toggles, the AND-combined intersection across cart products, `make_interval` lead-time for the checkout delivery-date picker.
- [[products-categories-seo]] — SEO title / description, URL handle (auto-suffix vs reject by source), 301-redirect on rename.
- [[products-categories-taxonomy]] — Google Shopping `taxonomy_id` mapping + the standalone Define-taxonomy modal from the List tab.
- [[products-categories-deletion-rules]] — delete blocked when products remain, XML-import lock, discount cascade, orphaned image, CloudCart-staff-only `category:path-rebuild` support tool.
- [[products-categories-api-validation]] — JSON-API v2 surface, server-side the request validator rules (simple-create vs full-edit, Shipping-Hours conditional rule), plan gates (`categories` numeric, `category_properties` boolean), side-effects parity across UI / API / CSV.

## What the merchant can do here

At the cluster level the merchant can:

- See and manage the full category tree (List + Organize tabs).
- Create / edit any category from a single modal.
- Reorder and re-parent via drag-and-drop within the 6-level cap.
- Override which payment / shipping methods are offered for orders containing products from a category.
- Set SEO fields, URL handle, and Google Shopping taxonomy per category.
- Bulk-delete categories that have no products and no active XML-import lock.
- Manage the same data programmatically via [[api-categories]] under [[json-api-v2]].

Per-aspect actions live on the sub-pages.

## Settings & fields

Every field surfaced on this screen is documented on the relevant aspect page. The split is:

| Field group | Aspect page |
|------------|-------------|
| List-table columns, Organize-tab tree controls, drop-target indicators | [[products-categories-list-organize]] |
| General / Logo / Taxonomy / Cart rules / Advanced field map (modal) | [[products-categories-edit-modal]] |
| Parent category + drop position rules | [[products-categories-hierarchy-rules]] |
| `Define custom payment / shipping methods`, `make_interval` | [[products-categories-cart-restrictions]] |
| SEO title / description, URL handle | [[products-categories-seo]] |
| Google Shopping taxonomy (feeds + search) | [[products-categories-taxonomy]] |
| Delete confirmation + error messages | [[products-categories-deletion-rules]] |
| the request validator server-side validation rules + JSON-API endpoints | [[products-categories-api-validation]] |

## Business rules

Each rule below is documented in full on the linked aspect — the merchant-facing summary:

- **6-level depth cap** — see [[products-categories-hierarchy-rules]]. Validated as `parent-count-from-root + max-child-depth-of-moved-subtree`.
- **Sibling-scoped name uniqueness** — same name allowed under different parents; rejected under the same parent. See [[products-categories-hierarchy-rules]].
- **AND-combined cart restrictions** — when a cart contains products from multiple restricted categories, the **intersection** of allowed methods is offered; an empty intersection means no methods at checkout. See [[products-categories-cart-restrictions]].
- **Delete blocked when products remain (no auto-reassign)** — including products in any descendant subcategory. XML-import lock also blocks. Successful delete cascades scoped discounts. See [[products-categories-deletion-rules]].
- **URL handle duplicate-behaviour split** — admin form + JSON-API v2 **reject** with 422; CSV / XML import **silently auto-suffixes**. URL-handle change records a 301 redirect. See [[products-categories-seo]].
- **SEO fields do NOT inherit from parent** — child categories with blank SEO fields fall back to **their own** name / description, not the parent's. See [[products-categories-seo]].
- **Side-effects parity** — every save / API write fires search re-index, cart-cache flush, materialised-path rebuild on parent change, and the `product.updated` / category-change-log entries. See [[products-categories-api-validation]].
- **Plan gates** — `categories` numeric cap (per-plan, add-on packs available) + `category_properties` boolean (URL access for `/admin/category/property/create`). See [[products-categories-api-validation]] and [[plan-features]].

### Permission

The Categories screen requires the products / categories permission section. Moderators without it cannot see the sidebar entry.

## Related

- [[products]] — parent hub.
- [[products-products]] — products are assigned to categories from the product editor.
- [[products-property]] — properties (specifications) attached to categories.
- [[settings-payment-providers]] — installed payment methods that per-category restrictions pick from.
- [[shipping]] — installed shipping providers.
- [[settings-cart]] — store-wide cart and checkout settings that restrictions overlay.
- [[settings-files]] — where category images live (orphaned on delete).
- [[apps-google-shopping]] — consumes the Google Shopping taxonomy assignment.
- [[apps-seo-spinner]] — bulk SEO content generation; sets `seo_generated_through_spinner`.
- [[apps-shipping-hours]] — consumes `make_interval`; required for the field's server-side validation.
- [[apps-csv-import]] — bulk-import categories; auto-suffixes duplicate URL handles.
- [[marketing-discounts]] — discounts scoped to a deleted category cascade-delete.
- [[api-categories]] — JSON-API v2 resource.
- [[api-properties]] / [[api-property-options]] — properties / property-options API surface.
- [[json-api-v2]] — authentication, rate-limit, side-effects principle.
- [[settings-api-keys]] — JSON-API v2 token management.
- [[plan-features]] / [[plan-gates]] / [[plan-vs-feature-pack]] — plan-gating model.
- [[category]] — entity page.
- [[product]] — entity page.

## Open questions

None at the hub level — all previously-flagged items resolved or distributed to sub-pages.
