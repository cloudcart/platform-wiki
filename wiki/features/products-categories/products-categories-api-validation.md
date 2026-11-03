---
type: feature
nav_path: "Products → Categories → JSON-API & validation"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Category JSON-API", "Category server-side validation", "Category validation rules", "Категории API", "Категория — валидация"]
tags: [products, categories, taxonomy, api, json-api-v2, validation, plan-gates]
plan_gates: ["categories", "category_properties"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[products-categories]]. See the hub for the other aspects (list & organize, edit modal, hierarchy rules, cart restrictions, SEO/taxonomy, deletion rules).

# Categories — JSON-API & validation

## Purpose

Everything that runs **server-side** when a category is created, updated, or deleted — whether from the admin form or from an external integration: the field-length caps, the conditional validation rules (simple-create vs full-edit, plus the Shipping-Hours-app extra rule), the JSON-API v2 surface that mirrors the admin behaviour, the **plan-feature gating** (`categories` numeric cap and `category_properties` boolean access), and the **side-effects parity rule** — every API write fires the same hooks as a UI save. This is the page to cite for *"why was my API call rejected?"* and *"what's my plan limit on categories?"*.

## Where to find it

- **Admin form validation** — surfaces inline next to fields in the Add / Edit modal at Sidebar → Products → **Categories** → +Add category / Edit. See [[products-categories-edit-modal]].
- **Plan-gate upsell** — surfaces when the merchant hits the `categories` numeric cap on create or tries to open `/admin/category/property/create` without the `category_properties` feature. Pack-purchase upsell at [[plan-features]].
- **JSON-API v2 endpoint** — `/api/v2/categories` (see [[api-categories]]).

## What the merchant can do here

- Create / update / delete categories programmatically via [[api-categories]] using a JSON-API v2 token from [[settings-api-keys]].
- Read categories with full attribute set, including `parent_id`, `display_child`, `taxonomy_id`, `make_interval`, SEO fields, and per-category payment / shipping restrictions.
- Manage **Category Properties** attached to categories via [[api-properties]] and [[api-property-options]].
- Purchase the `categories` per-plan add-on pack at [[plan-features]] when hitting the numeric cap (see [[plan-vs-feature-pack]]).

### What the merchant CANNOT do here

- Bypass the depth / sibling-uniqueness / deletion-block rules through the API — same validations as the admin form.
- Use duplicate URL handles through the API — admin behaviour applies (rejected with 422); only the CSV / XML import path auto-suffixes.
- Open `/admin/category/property/create` without the `category_properties` plan feature — the URL is access-gated.
- Exceed the `categories` numeric cap without buying the per-plan add-on pack.

## Settings & fields

### JSON-API v2 endpoint summary

| Method | Path | Notes |
|--------|------|-------|
| GET | `/api/v2/categories` | List with `?include=`, `?filter[*]=`, `?sort=`, pagination. |
| POST | `/api/v2/categories` | Create. Honours the `categories` plan cap. |
| GET | `/api/v2/categories/{id}` | Single category. |
| PATCH | `/api/v2/categories/{id}` | Update. Same validations as the admin form. |
| DELETE | `/api/v2/categories/{id}` | Delete. Same blocks as the admin form. |

See [[api-categories]] for the full attribute / relationship surface.

### Server-side validation rules

Validation runs in TWO modes depending on whether the merchant submitted a **simple** create (the quick "Add subcategory" inline action) or the full **edit** form.

**Simple-create mode** (just a name in the inline create row):

- `name` — **required**, max **191 chars**, must be unique within the same parent (scoped by `parent_id`). Error: *"Category name is already taken"*.

**Full-edit mode** (the edit modal submitting the entire category record):

- `description` — rich-text HTML, max **250,000 chars** (hard cap regardless of plan). Error: *"The category description must not exceed 250000 characters"*.
- `all_shipping` — **required**, must be `0` or `1`. Drives whether the per-category shipping restriction list is honored or ignored.
- `all_payment` — **required**, must be `0` or `1`. Same idea for payment methods.
- `taxonomy_id` — **required**, integer, must exist in `apps.google_product_category` table. Picking a deleted / unknown taxonomy node fails with *"The selected taxonomy is invalid"*.
- `shipping` — array, **required when `all_shipping = 0`**. If the merchant turns OFF "All shipping methods" they must explicitly pick at least one method.
- `payment` — array, **required when `all_payment = 0`**. Same idea for payment methods.

**Conditional rule (Shipping Hours app)** — when the [[apps-shipping-hours]] app is installed, an extra rule activates:

- `make_interval` — **required**, integer, min 0. The per-category production lead-time in hours. Without the app installed, the field is not validated.

In full-edit mode `name`, `parent_id`, `url_handle`, `seo_title`, `seo_description`, `image`, and per-category dimensions are validated separately — see [[products-categories-hierarchy-rules]] and [[products-categories-seo]] for that wording.

### Category record fields (21 verified)

Each category stores: `name`, `order`, `description`, `parent_id`, `seo_title`, `seo_description`, `url_handle`, `color`, `icon`, `icon_data`, `max_thumb_size`, `bnp_type_id`, `ucf_cop`, `make_interval` (production lead time in hours — see [[products-categories-cart-restrictions]]), `taxonomy_id`, `seo_generated_through_spinner` (set by [[apps-seo-spinner]]), `display_child`, `background`, `width`, `height`, `image_processed`, `image` (uploaded through the dedicated image pipeline, not editable inline).

## Business rules

### Side-effects parity — API writes fire the same hooks as the UI

A POST / PATCH / DELETE through JSON-API v2 fires the same hooks as the admin save:

- Search re-index queued.
- Customer-cart cache flushed.
- Materialised path-table rebuilt for the subtree (on parent change).
- URL-handle-change 301-redirect entry recorded (on `url_handle` change).
- Discount cascade fires on successful delete (see [[products-categories-deletion-rules]]).
- The category change-log records `api2` as the actor when the change came from JSON-API v2.

### Same structural rules apply on the API path

The **6-level depth cap**, **sibling-scoped name uniqueness**, and **deletion-blocked-while-products-remain** rules all enforce on the API path too — invalid payloads return **422** with the same error messages documented across [[products-categories-hierarchy-rules]] and [[products-categories-deletion-rules]].

### One behavioural difference between admin / API / CSV-XML — duplicate URL handles

- **Admin form** — REJECTED with a validation error. Merchant must pick a unique slug or rely on auto-derivation from the name.
- **JSON-API v2** — same as admin: duplicate handles return **422**.
- **CSV / XML import** ([[apps-csv-import]]) — silently auto-suffixed (`-1`, `-2`, …) so the bulk import doesn't fail mid-batch.

See [[products-categories-seo]] for the full URL-handle discussion.

### Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `categories` | Numeric (max categories) | Per-plan cap on the total number of `Category` records the merchant can own. Counted toward the cap on the Add-category create endpoint; hitting it surfaces the pack-purchase upsell. Per-plan add-on packs are available via [[plan-features]]. |
| `category_properties` | Boolean (URL access) | The `/admin/category/property/create` URL is access-gated. Without the feature, the merchant cannot open the property-create flow from [[products-property]] (which is where category-bound specifications are defined). The Properties sidebar entry stays visible but new creates redirect to the upsell. |

**Behaviour:**

- Hitting the `categories` numeric cap surfaces the per-feature upsell modal at [[plan-features]].
- The `category_properties` boolean redirects to a plan-upgrade panel when the merchant tries to open the create flow.

See [[plan-vs-feature-pack]] for the pack-vs-upgrade decision.

### Authentication + rate limit
Standard JSON-API v2 — see [[json-api-v2]] for authentication, rate-limit, and the side-effects principle. Tokens are managed at [[settings-api-keys]].

### Permission
Programmatic CRUD requires a JSON-API v2 token whose scope includes the categories resource — see [[settings-api-keys]].

## Related

- [[products-categories]] — hub.
- [[api-categories]] — the JSON-API v2 resource page.
- [[api-properties]] / [[api-property-options]] — properties attached to categories.
- [[json-api-v2]] — authentication, rate-limit, side-effects principle.
- [[settings-api-keys]] — JSON-API v2 token management.
- [[plan-features]] / [[plan-gates]] / [[plan-vs-feature-pack]] — gating model + pack-vs-upgrade decision.
- [[products-property]] — category-bound specifications create flow gated by `category_properties`.
- [[apps-shipping-hours]] — conditional `make_interval` validation rule.

## Open questions

- Whether the `bnp_type_id` and `ucf_cop` fields are merchant-facing on any screen, or backend-only (verify).
- Whether the `background` field is the same upload pipeline as `image` or a separate one (verify).
- Whether the `categories` plan-cap counts soft-deleted (trashed) categories or only live ones (verify).
