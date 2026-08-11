---
type: feature
nav_path: "Products → Products → Known issues"
route_name: ""
route_path: ""
aliases: ["Products known issues", "Products by-design quirks", "Product edge cases", "Product webhook coverage gap", "Product hard delete cascade", "Product duplicate quirks", "Известни проблеми с продукти"]
tags: [catalog, products, known-issues, edge-cases, support]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-products]]. See the hub for the other aspects (list view, editor, variants matrix, bulk actions, AI content, change log).

# Products — Known issues + by-design quirks

## Purpose

This page is the support agent's catalogue of **by-design quirks** and **known bugs** specific to the Products list / editor. Most surface during triage as "why doesn't this work the way I expect?" — the answer is usually *"by design, here is why"*. A few are genuine bugs worth flagging. Entries are grouped by sub-aspect (list view, editor, variants, save side-effects, deletion, sort ordering).

## Where to find it

Referenced from every other aspect when a rule is "weird but intentional". The support agent reads this page to confirm a behaviour is expected before escalating.

## What the merchant can do here

Nothing — this is a support-agent reference page. The behaviours described below cannot be toggled or worked around from the admin UI unless a workaround is explicitly listed.

## Settings & fields

### Webhooks fire ONLY when changes originate from the admin panel

The `product.created` and `product.updated` webhooks fire from **admin-panel-originated changes only**. **REST API saves**, **background jobs** (XML / CSV / ERP imports, smart-collection re-evaluation), and **storefront-side mutations** (stock decrement on checkout) **DO NOT fire the merchant-visible webhooks**.

The internal search re-index fires from every save regardless of source — so the storefront stays in sync even from ERP imports — but the merchant's webhook receivers (configured in [[settings-hooks]]) see only admin-panel changes.

**Workaround for full coverage:** combine `product.*` webhooks (admin-only) with order-status / inventory webhooks, or poll the JSON-API v2.

### Webhook payload is chatty

`product.updated` is **chatty** — it fires on ANY field change, including minor ones (stock decrement after an order, smart-collection membership change). **Webhook receivers must be idempotent.**

### Bundles are NOT counted against the `products` plan quota

The *"Products used / max"* chip in the [[products-list-view]] header counts only catalog products (simple, multi-variant, digital). **Bundle-type products are NOT counted** — they have a separate `bundles` plan quota, so a merchant maxed out on products can still create bundles. The Variants counter beside the chip is product-only too; bundle component lines aren't counted.

### Sort order tie-break is implicit ID ASC

The storefront orders by `sort_order` ascending. When two products share the same `sort_order`, the tie-break falls back to insertion order (typically `id` ASC) — there's no explicit secondary ordering. This applies to category listing pages too. **For deterministic ordering, the merchant should set distinct `sort_order` values.**

### `/product/` URL prefix is HARDCODED

The storefront URL pattern is `/product/{slug}/{cart_key?}`. The prefix `/product/` is **HARDCODED** — there's no merchant-configurable prefix setting, so the merchant CANNOT change it to `/p/` or anything else without code changes.

A legacy redirect handles `/products/{id}` (plural with numeric ID) — it 301-redirects to the canonical `/product/{slug}`, ignoring publish-state filters so it works for inactive products too.

### Image dimensions cap is platform-managed

Product images are served at `/image/product/{product_id}/{size}`, resized on demand to common sizes. **The dimensions cap is platform-managed, not merchant-configurable** — a merchant can't add a custom size that isn't in the preset list.

### Variant count caps (data-model)

- **Max 3 variant parameters per product** (e.g. Color + Size + Material) — hard cap (`p1`/`p2`/`p3` and `v1`/`v2`/`v3` slots).
- **Max 500 variants per product** — the SKU matrix can't exceed 500 rows. Beyond this the save fails with a *"max allowed exceeded"* error (e.g. 50 sizes × 11 colors = 550 → rejected). Stores needing more must split into multiple parent products.
- **Per-variant `quantity` capped at 50,000,000.** Higher values fail at validation.

### Product duplicate — verified specifics

When duplicating (single or bulk via [[products-bulk-actions]]):

- Copy's name and URL handle = original + `"-Copy"` (each truncated at 191 chars).
- Copy is set to **Draft** (`active = no`) — never auto-publishes.
- Copy carries `app_import = duplicate_product-<original-id>` — searchable via the "Imported with" filter on [[products-list-view]] to find or undo duplications.
- Variants are deduplicated by their `(v1, v2, v3)` combination — older databases with duplicate variant rows get cleaned up in the copy.
- Categories, tags, tabs, files, brand-model links, smart-collection memberships, and category-property values are all copied.
- Product files in S3 are server-side-copied in a single round-trip, so duplicating 50 files takes a fraction of a second.

### URL handle suffixing for collisions

When the merchant doesn't supply a URL handle:

1. The handle is slugified from the product name and trimmed to 180 characters.
2. Suffixed `-1`, `-2`, ... if a duplicate URL handle exists.
3. **For very large catalogs** the suffix becomes a **6-digit random number** to avoid suffix-collision lookups (so the merchant may see e.g. `red-shirt-481732` instead of `red-shirt-1`).
4. The old URL handle is saved to redirect history — when the merchant edits a slug on a published (non-draft) product, the old slug 301-redirects to the new canonical URL.

### Product delete is HARD delete (no soft-delete / trash)

Product deletion is a **hard delete cascading** to:

- Files attached to the product, variants (and their images), and digital file records.
- Image directories on S3 (the platform queues the deletion).
- Bundle relationships — if the deleted product is part of a bundle, **the bundle gets deactivated**.
- Discount cart-item rules and quantity discounts attached to the product.
- The product's own change-log entries.

**Queued tasks referencing the deleted product are pulled out too,** so an in-flight job doesn't fail with a missing-record error.

**This is irreversible — the merchant must restore from backup.** The Delete confirmation modal warns *"This action cannot be undone."*

### `description` / `short_description` show as `"To long"` in the Change log

To keep entries compact, the Change log records long-text fields with the placeholder `"To long"` instead of the value — the merchant does NOT see the full rich-text body in the log. See [[products-change-log]].

### Cloudio AI generation does NOT auto-save

When the merchant uses [[products-ai-content|Cloudio]] to generate a description / SEO field, the proposal appears in the editor field but isn't persisted until the merchant saves manually. The merchant can edit Cloudio's output before saving.

### Linked products are NOT auto-derived

Linked products (the manual cross-sell list on [[products-editor]]) are 100 % merchant-curated. There's no smart suggestion — for *"also recommended"* on every product, the merchant picks each linked product manually, or uses a [[products-smart-collections|smart collection]] on the storefront instead.

### Discounts panel on the editor is read-only

The Discounts aside section on [[products-editor]] LISTS the discounts currently applying to this product. It does NOT create or assign discounts — to add a discount targeting this product, the merchant uses the separate Discounts feature.

## Business rules

The entries above ARE the business rules — this is a known-issues catalogue. Cross-cutting rules spanning multiple aspects live here so the support agent has one place to look.

## Related

- [[products-products]] — hub.
- [[products-list-view]] — bundles-not-counted, sort tie-break.
- [[products-editor]] — URL prefix, image dimensions, Linked products, Discounts panel.
- [[products-variants-matrix]] — variant count caps.
- [[products-bulk-actions]] — bulk-duplicate specifics, bulk-delete cascade.
- [[products-ai-content]] — Cloudio auto-save behaviour.
- [[products-change-log]] — `"To long"` placeholder for long-text fields, cascade-on-delete.
- [[settings-hooks]] — `product.*` webhook coverage gap.
- [[inventory-debugging-playbook]] — the 6-step diagnostic for unexpected stock changes (uses the Change log + Initiator column).

## Open questions

None.
