---
type: feature
nav_path: "Products → Products"
route_name: products-index
route_path: /admin/products
aliases: ["Products", "Product list", "Product editor", "Catalog", "Продукти", "Каталог"]
tags: [products, catalog, editor, core]
plan_gates: ["products"]
created: 2026-05-21
updated: 2026-11-03
source_count: 14
---
# Products

## Purpose

The **core feature** of the entire admin panel — the merchant's full product catalog. The page has two modes: a paginated **List** view for finding, filtering, bulk-editing and managing products at scale (see [[products-list-view]]), and an **Edit** view that opens the full single-product editor (see [[products-editor]]).

Most merchants spend more time on this screen than anywhere else. It's also the most plan-gated screen — the merchant's plan caps how many products they can have, and the counter in the page header (*Products: `<used>` / `<max>`*, beside a Variants count) shows current consumption.

## Where to find it

Sidebar → Products → **Products**.

The page title reads "Products" and the address is `/admin/products`. On the Edit view the title is the product's name, with its first image beside it.

| Label | Where |
|-------|-------|
| Products list | Default view at `/admin/products`. |
| Edit product | `/admin/products/edit/:id` — opens when the merchant clicks a product. |

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[products-list-view]] — list mode: header counter, search and filter bar, list columns, per-row inline actions, Import / Add product entry points.
- [[products-editor]] — single-product editor (two-column layout): Details / Media / Product type settings / Categories / Metafields / Brand / Suppliers / SEO / Linked / Extend functionality + the Product Statuses / Vendors / Tags / Smart Collections / Sort number / Applied discounts aside + the save flow.
- [[products-variants-matrix]] — setting up variants, the **Edit Variant options** window, the **Edit Variant** side panel, the Inventory card on the editor, per-variant bulk actions, variant rename / merge cascades.
- [[products-bulk-actions]] — the list's **Tools** menu: bulk action catalogue, the bulk-action sub-popup mechanics, no-category guards on Publish, bulk duplicate.
- [[products-ai-content]] — ShopperPen by CloudIO side panel: description, short description and meta description generation, token cost, stored results with Keep / Copy text, RankMaster AI and VisionSense AI.
- [[products-change-log-link]] — how the Change log modal is launched from this screen; see [[products-change-log]] for the modal's contents.
- [[products-known-issues]] — by-design quirks and known-bugs catalogue specific to the Products list / editor.

## What the merchant can do here

- **Find**, **edit**, **bulk-edit**, AI-**generate** content, and **audit history** — each via its aspect page (see the Sub-pages list above).
- **Create** a new product via **Add product** (type-picker popup → name + category → editor).
- **Import** existing data via the **Import** button (CSV / XML Import / XML Sync / API import). The CSV path opens a 3-step import window; backend mechanics on [[apps-csv-import]].

## Settings & fields (top-level)

### Product states

| State | Meaning | On this screen |
|-------|---------|----------------|
| **Draft** | Saved but not yet published. Invisible to customers. | **Draft** badge beside the editor's title; pen icon in the list row. |
| **Published** | Visible to customers. | **Published** switch on the editor; arrow icon in the list row. |
| **Hidden** | Published but not shown on the storefront category listings. Customers can still reach it via direct URL. | **Hide from store** switch; eye icon in the list row. |
| **New** | For marketing promotion. | **Mark as new** switch; flame icon in the list row. |
| **Featured** | Surfaces on featured-products modules. | **Mark as featured** switch; thumbs-up icon in the list row. |
| **Out of stock** | Tracking is on and quantity reached 0. | The store shows the status picked under **Custom statuses** ([[products-statuses]]). |

### Plan gate

The merchant's `products` plan-feature quota caps the total product count; the header counter shows current vs max. When the cap is reached, **Add product** and **Import** open the plan-upgrade window straight away, with *"You have reached the maximum number of products you can create ({used} out of {current}). You must upgrade your plan to continue."* It lets the merchant upgrade or buy an add-on pack of extra product slots. Existing products keep working — only NEW additions block.

**Bundles are NOT counted** against the `products` quota — they have their own `bundles` quota (a merchant maxed out on products can still create bundles).

## Business rules (cross-cutting)

Aspect-specific rules live on the relevant sub-page. The three rules that span both list and editor:

- **Draft vs Hidden** — a Draft product is invisible *anywhere* on the storefront (even direct URL → 404). A Hidden product IS published but doesn't appear in listings / search — customers can still reach it via the direct product URL. Useful for private promotion campaigns. Merchants asking *"I sent the link but customer says it doesn't work"* should check both flags.
- **Category required** — only a draft can be stored without a main category. The editor asks for one on every save, with the **Published** switch on or off ([[products-editor]]). The [[products-bulk-actions|bulk Publish]] action silently drops uncategorised products from the batch.
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
- [[apps-csv-import]] — CSV import mechanics, shared by the import window on this page and `/admin/apps/csv_import`.
- [[apps-xml-import]] / [[apps-xml-sync]] — XML feed-based imports.
- [[apps-cloudio-overview]] — Cloudio AI overview (the engine behind the description generator).
- [[apps-google-shopping]] — feeds products to Google Shopping.
- [[inventory-tracking]] — the cross-cutting inventory model that this screen reads from / writes to.
- [[product-visibility]] — the Draft vs Hidden vs Active model + the "I sent the link but the customer can't open it" checklist.
- [[variants-model]] — the Parameter / Option / Variant model behind the variants matrix + the Inventory card.
- [[import-pipeline]] — the bulk-import model behind the cloud-upload Import (CSV / XML / API).
- [[seo-handling]] — the per-product **SEO Configuration** card (meta title / description / handle / structured data).
- [[metafields-definitions]] — the **Metafields** card on the editor.
- [[product]] / [[variant]] / [[category]] — entity pages.

## Open questions

None at the hub level. Aspect-specific open questions live on each sub-page.
