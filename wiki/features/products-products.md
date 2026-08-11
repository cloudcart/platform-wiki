---
type: feature
nav_path: "Products → Products"
route_name: products-index.new
route_path: /admin/products/products-new
aliases: ["Products", "Product list", "Product editor", "Catalog", "Продукти", "Каталог"]
tags: [products, catalog, editor, core]
plan_gates: ["products"]
created: 2026-05-21
updated: 2026-06-10
source_count: 14
---
# Products

## Purpose

The **core feature** of the entire admin panel — the merchant's full product catalog. The page has two modes: a paginated **List** view for finding, filtering, bulk-editing and managing products at scale (see [[products-list-view]]), and an **Edit** view that opens the full single-product editor (see [[products-editor]]).

Most merchants spend more time on this screen than anywhere else. It's also the most plan-gated screen — the merchant's plan caps how many products they can have, and the count chip in the page header (`<used> of <max>`) shows current consumption.

## Where to find it

Sidebar → Products → **Products**.

The breadcrumb reads "Products". The route is `/admin/products/products-new` (the modern Vue version). On the Edit view the breadcrumb expands to "Products → `<product name>`".

| Label | Where |
|-------|-------|
| Products list | Default view at `/admin/products/products-new`. |
| Edit product | `/admin/products/products-new/edit/:id` — opens when the merchant clicks a product. |

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[products-list-view]] — list mode: header chip, filter sidebar, list columns, per-row inline actions, Import / Create-product entry points.
- [[products-editor]] — single-product editor (two-column layout): Details / Media / Categories / Brand / SEO / Linked / Required Apps + the Publish / Vendor / Tags / Smart Collections / Sorting / Discounts aside + the save flow.
- [[products-variants-matrix]] — the per-variant manage modal, variant detail side-panel, the Inventory card on the editor, per-variant bulk actions, variant rename / merge cascades.
- [[products-bulk-actions]] — list-page multi-select bulk action catalogue, the bulk-action sub-popup mechanics, draft-without-category guards, bulk duplicate.
- [[products-ai-content]] — Cloudio / ShopperPen AI side panel: description / SEO / handle generation, CC-token cost model, history + accept-reject flow, vision-augmented image picker.
- [[products-change-log-link]] — how the Change log modal is launched from this screen; see [[products-change-log]] for the modal's contents.
- [[products-known-issues]] — by-design quirks and known-bugs catalogue specific to the Products list / editor.

## What the merchant can do here

- **Find**, **edit**, **bulk-edit**, AI-**generate** content, and **audit history** — each via its aspect page (see the Sub-pages list above).
- **Create** a new product via **+ Add product** (type-picker popup → name + category → editor).
- **Import** existing data via the cloud-upload icon (CSV / XML Import / XML Sync / API import). The CSV path opens the 3-step modern Vue import wizard; backend mechanics on [[apps-csv-import]].

## Settings & fields (top-level)

### Product status badges

| Badge | Meaning |
|-------|---------|
| **Draft** | Saved but not yet published. Invisible to customers. |
| **Active** (no badge — default) | Published and visible to customers. |
| **Hidden** | Active but not shown on the storefront category listings. Customers can still reach it via direct URL. |
| **New** | The "🔥 New" badge — for marketing promotion. |
| **Featured** | The "⭐ Featured" badge — surfaces on featured-products modules. |
| **Out of stock** | Set automatically when tracking is on and quantity reaches 0 (or via the merchant's custom status — see [[products-statuses]]). |

### Plan gate

The merchant's `products` plan-feature quota caps the total product count; the header chip shows current vs max. When the cap is reached, **+ Add product** still opens, but the final save fails with a plan-upgrade prompt → the pack-purchase modal lets the merchant upgrade or buy an add-on pack of extra product slots. Existing products keep working — only NEW additions block.

**Bundles are NOT counted** against the `products` quota — they have their own `bundles` quota (a merchant maxed out on products can still create bundles).

## Business rules (cross-cutting)

Aspect-specific rules live on the relevant sub-page. The three rules that span both list and editor:

- **Draft vs Hidden** — a Draft product is invisible *anywhere* on the storefront (even direct URL → 404). A Hidden product IS published but doesn't appear in listings / search — customers can still reach it via the direct product URL. Useful for private promotion campaigns. Merchants asking *"I sent the link but customer says it doesn't work"* should check both flags.
- **Category required to publish** — a product cannot be published without at least one category assigned. Enforced at save time, not field-level. So a Draft can exist without a category; an Active product cannot. The [[products-bulk-actions|bulk Publish]] action silently drops uncategorised products from the batch.
- **Side effects on save fire on every save (admin OR API)** — search-index re-index, smart-collection re-evaluation ([[products-smart-collections]]), storefront cache flush. **EXCEPT** the merchant-visible `product.created` / `product.updated` webhooks fire ONLY from admin-panel saves — REST API v2 saves, background imports (CSV / XML / ERP), smart-collection re-evaluation and storefront stock decrement DO NOT fire them. See [[settings-hooks]] and [[products-known-issues]] for the coverage gap.

### Permission

The `products` permission section is required. Moderators without it cannot access the Products sidebar entry. Granular per-category restrictions can be applied via [[settings-staff]] to limit which products a moderator can edit; the list view filters their visible products automatically.

## Programmatic access

The data this screen manages can also be read / written via **JSON-API v2** — see [[api-products]], [[api-variants]], [[api-images]]. Same save side-effects apply (except merchant-visible webhooks — see the cross-cutting rule above). The change-log records `api2` as the actor for these writes — useful for *"the merchant didn't change anything"* tickets ([[products-change-log]]). See [[json-api-v2]] for auth + rate limits.

## Related

- [[products]] — parent hub.
- [[products-categories]] — categories required for publishing.
- [[products-vendors]] — vendor / manufacturer assignment.
- [[products-property]] — category-bound properties displayed on the Edit page when categories are picked.
- [[products-variants-options]] — variant parameter / option definitions screen.
- [[products-smart-collections]] — smart collections to which products can be assigned.
- [[products-inventory]] — inventory view focused on stock management.
- [[products-statuses]] — product status taxonomy (Available, Out of stock, custom).
- [[products-banners-labels]] — banners and labels overlaid on products on the storefront.
- [[products-favorite-products]] — customers' favorited products view.
- [[products-missing-product]] — subscribers waiting for back-in-stock notifications.
- [[products-change-log]] — Change log modal (per-field diff history).
- [[settings-cart]] — `order_status_for_quantity_decrease` controls when stock is decremented; `product_threshold` triggers low-stock notifications.
- [[settings-hooks]] — `product.created` / `product.updated` / `product.deleted` webhook events.
- [[settings-staff]] — staff permissions + per-category restrictions.
- [[apps-csv-import]] — CSV import backend mechanics (shared between the modern Vue wizard on this page and the legacy `/admin/apps/csv_import`).
- [[apps-xml-import]] / [[apps-xml-sync]] — XML feed-based imports.
- [[apps-cloudio-overview]] — Cloudio AI overview (the engine behind the description generator).
- [[apps-google-shopping]] — feeds products to Google Shopping.
- [[inventory-tracking]] — the cross-cutting inventory model that this screen reads from / writes to.
- [[product-visibility]] — the Draft vs Hidden vs Active model + the "I sent the link but the customer can't open it" checklist.
- [[variants-model]] — the Parameter / Option / Variant model behind the variants matrix + the Inventory card.
- [[import-pipeline]] — the bulk-import model behind the cloud-upload Import (CSV / XML / API).
- [[seo-handling]] — the per-product SEO section (meta title / description / handle / structured data).
- [[product]] / [[variant]] / [[category]] — entity pages.

## Open questions

None at the hub level. Aspect-specific open questions live on each sub-page.
