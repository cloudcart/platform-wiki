---
type: feature
nav_path: "Products → Categories → Add / Edit modal"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Add category modal", "Edit category modal", "Category form", "Категория — създай", "Категория — редактирай"]
tags: [products, categories, taxonomy, navigation, modal]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-categories]]. See the hub for the other aspects (list & organize, hierarchy rules, cart restrictions, SEO/taxonomy, deletion rules, JSON-API/validation).

# Categories — Add / Edit modal

## Purpose

The single full-form modal where the merchant creates a new category or edits an existing one. It is the canonical place to set the **name, description, parent, image, Google Shopping taxonomy, per-category payment / shipping restrictions, technological delivery time, and SEO fields**. Opened from the +Add category button on either tab of [[products-categories-list-organize]], from any row's Edit action, or from clicking a node on the Organize tree. The merchant's "quick path" for taxonomy-only edits is a separate, smaller modal — covered in [[products-categories-taxonomy]].

## Where to find it

Sidebar → Products → **Categories** → +Add category (or any row's Edit button, or a tree-node click on the Organize tab).

Modal title: *"Add category"* on create, *"Edit - {name}"* on edit. Modal size: `xl`.

## What the merchant can do here

- Fill in the **Category name** (required) — used as the display name everywhere.
- Add a **Description** via the rich-text editor — shown on the storefront category landing page.
- Pick a **Parent category** from a searchable dropdown — leave empty for a top-level category.
- Toggle **Display subcategories** — controls recursive inclusion of subcategory products on the storefront listing.
- Upload a **Category image** — single image, drag-or-click; used on category cards and some marketing surfaces.
- Assign a **Google Shopping taxonomy** node — used by feed-generating apps (see [[products-categories-taxonomy]]).
- Turn on **Define custom payment methods for this category** — pick a subset of installed payment providers that are allowed when the cart contains a product from this category (see [[products-categories-cart-restrictions]]).
- Turn on **Define custom shipping methods for this category** — same pattern for shipping providers.
- Set the **Technological delivery time in hours** — production lead time for products in this category (visible only when the store-wide `enabled_delivery_time` flag is on; affects the customer-facing delivery-date picker at checkout).
- Expand **Advanced settings** to set **SEO title**, **SEO description**, and **URL handle** — see [[products-categories-seo]].
- Save (`Save` button) or close without saving.

### Modal load behaviour

On edit, the modal **pre-fetches the full record** (parent dropdown options, payment / shipping providers, delivery-time flag) when it opens — a loader shows briefly. On create, the modal opens immediately with empty defaults.

## Settings & fields

### Field map

| Section | Field | What it does |
|---------|-------|--------------|
| General | **Category name** | Required. Free text. Used as the display name everywhere. Max 191 chars; must be unique within the same parent — see [[products-categories-hierarchy-rules]]. |
| General | **Description** | Rich-text. Shown on the storefront category landing page (top of the product list). Max 250,000 chars. |
| General | **Parent category** | Optional. Picks the parent in the hierarchy. Searchable dropdown of all other categories. |
| General | **Display subcategories** | Toggle. When ON, the storefront listing includes products from all subcategories (recursive). When OFF, only direct-child products show. |
| Logo | **Category image** | Single image upload, drag-or-click. Stored alongside other store assets — see [[settings-files]]. Delete button shown when an image is set. NOT auto-deleted when the category is deleted (becomes orphan). |
| Taxonomy | **Google Shopping taxonomy** | Optional. Tree-search picker; sets `taxonomy_id` to a node in the `apps.google_product_category` table (verify). Used by [[apps-google-shopping]] and similar feed generators. Informational only — does NOT restrict which products can go in the category. |
| Cart rules | **Define custom payment methods** | Toggle (`all_payment = 0` when ON). When OFF, all installed payment methods work for products in this category. When ON, only the methods the merchant picks are offered — see [[products-categories-cart-restrictions]]. |
| Cart rules | **Payment methods** (when above is ON) | Multi-select tags from installed providers — see [[settings-payment-providers]]. Required when `all_payment = 0`. |
| Cart rules | **Define custom shipping methods** | Toggle (`all_shipping = 0` when ON). Same pattern as payment. |
| Cart rules | **Shipping methods** (when above is ON) | Multi-select tags of installed shipping providers — see [[shipping]]. Required when `all_shipping = 0`. |
| Cart rules | **Technological delivery time** | Integer hours. Visible only when the store's `enabled_delivery_time` flag is on. Backed by the category's `make_interval` field — see [[products-categories-cart-restrictions]] for the checkout effect. |
| Advanced | **SEO title** | `<title>` tag value when the category page is shown. Falls back to the category name if blank. |
| Advanced | **SEO description** | `<meta name="description">` value. Falls back to a truncation of the description if blank. |
| Advanced | **URL handle** | URL slug. Prefixed with `/category/`. Auto-generated from the name if blank. Unique across all categories — duplicate handles are rejected at save with a validation error. See [[products-categories-seo]] for the 301-redirect history. |

### Save behaviour

- On create: POST → new category with a fresh ID; the List tab and Organize tab refresh.
- On edit: PATCH → existing category updated; the table cache for that row is updated immediately.
- On any save: search re-index queued; storefront cart cache flushed; the "categories were modified" flag is set.
- Validation errors surface inline next to the offending field with the messages documented under [[products-categories-api-validation]].

## Business rules

### Save fires search re-index + cache flush
- **Search index re-build** — changing a category name or hierarchy triggers a background task so storefront search reflects the new structure (expected delay: up to a few minutes).
- **Customer-cart cache flush** — cart restrictions change immediately; the platform flushes the cart cache so the next storefront request applies the new rules.

### SEO fields do NOT inherit from parent
The SEO fields (and `taxonomy_id`, `make_interval`) are **stored per category** and are NOT cascaded from the parent. A child category with empty `seo_title` falls back to its own name, not the parent's. See [[products-categories-seo]].

### Image is NOT auto-deleted on category delete
The uploaded category image stays in [[settings-files]] as orphan storage when the category is deleted.

### Standalone taxonomy modal is a separate, faster path
The List tab's Taxonomy column cell opens a focused **Define taxonomy** modal containing only the taxonomy picker — NOT the full edit modal. See [[products-categories-taxonomy]] for the bulk-taxonomy assignment workflow.

### Permission
This modal requires the products / categories permission section to be granted. Moderators without it cannot reach the Categories screen.

## Related

- [[products-categories]] — hub.
- [[products-categories-list-organize]] — where the modal is opened from.
- [[products-categories-hierarchy-rules]] — parent / depth / name-uniqueness rules enforced at save.
- [[products-categories-cart-restrictions]] — what the Cart-rules section actually does.
- [[products-categories-seo]] — SEO fields + URL handle.
- [[products-categories-taxonomy]] — taxonomy assignment + the standalone taxonomy modal.
- [[products-categories-api-validation]] — server-side validation messages (the inline errors in this modal).
- [[settings-files]] — where the category image lives.
- [[settings-payment-providers]] — providers picked for per-category payment restrictions.
- [[shipping]] — installed shipping providers.

## Open questions

- Exact `enabled_delivery_time` flag location (store-level setting page or a platform-only flag) (verify).
