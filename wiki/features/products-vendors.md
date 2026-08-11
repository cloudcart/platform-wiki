---
type: feature
nav_path: "Products → Vendors"
route_name: vendors
route_path: /admin/products/vendors
aliases: ["Vendors", "Manufacturers", "Brands (manufacturers)", "Производители", "Доставчици", "Брандове"]
tags: [products, vendors, manufacturers, brands]
plan_gates: ["vendors"]
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---
# Vendors

## Purpose

The screen where the merchant maintains the list of **manufacturers** (also called "vendors" or "brands" depending on the merchant's terminology) that supply the store's products. Each vendor has a name, description, logo, and SEO settings — the merchant assigns one vendor to each product (on the product editor), and the platform builds a vendor landing page on the storefront so customers can browse all products from a given manufacturer.

This is independent from the [[brand-model]] app (which adds device-compatibility metadata like "iPhone 13") and from the supplier app (which is about purchase-side procurement). Vendors here are the merchant's **public, customer-facing manufacturer list**.

This page is a slim hub. The detailed mechanics live in three aspect sub-pages (below) — drill into the one that matches the question rather than reading all three.

## Where to find it

Sidebar → Products → **Vendors**.

The page's breadcrumb reads "Products → Vendors". The route is `/admin/products/vendors`. The header icon is the user-tie icon.

## Sub-pages (in this cluster)

- [[products-vendors-list]] — the vendor list table: columns (ID / Name / Created / Updated / Products count), sorting, the **Has products** filter, name search, bulk-select + bulk-delete, the cleanup workflow, and the no-native-merge gap.
- [[products-vendors-editor]] — the Add / Edit modal: General / Logo / Advanced (SEO) cards, the field map, validation caps + uniqueness, URL-handle auto-derivation, logo upload + storage, and the backend-only AI description endpoints (no UI button).
- [[products-vendors-rules]] — business rules + backend behaviour: one-vendor-per-product, the storefront landing page, deletion blocking (has-products / has-XML-import), listing-engine propagation on name change, lifecycle events, save side-effects, the permission gate, the `vendors` plan cap, and JSON-API v2 parity.

## What the merchant can do here

- **List + browse** vendors in a paginated, sortable table; filter by **Has products**; search by name — full detail on [[products-vendors-list]].
- **Add a vendor** via the + Add vendor modal; **edit** an existing one by clicking its row — the modal (General / Logo / Advanced cards) is documented on [[products-vendors-editor]].
- **Bulk-select + bulk-delete** vendors (blocked per-row when a vendor still has products) — see [[products-vendors-list]] and the deletion rules on [[products-vendors-rules]].

### What the merchant CANNOT do here

- See which specific products are assigned to a vendor from THIS page — the Products count is informational only. To list a vendor's products, use [[products-products]] with the Vendor filter.
- Reassign products from one vendor to another — done from [[products-products]] via the Change vendor bulk action.
- Merge two vendors — no one-click merge; reassign products then delete the empty vendor (see [[products-vendors-list]]).
- Import vendors from CSV from this page — use [[apps-csv-import]] or a dedicated app.

## Settings & fields

The list has five sortable columns (ID, Name, Created at, Updated at, Products) plus per-row Edit / Delete — see the column table on [[products-vendors-list]]. The Add / Edit modal exposes Name + Description (General), Brand logo (Logo), and SEO title / SEO description / URL handle (Advanced) — see the field map + validation caps on [[products-vendors-editor]].

## Business rules

Each product is assigned **exactly one** vendor; the platform auto-generates a `/vendor/<url-handle>` storefront landing page; deletion is **blocked** while products (or active XML-import tasks) reference the vendor; a vendor **name** change re-syncs every linked product in the listing engine. All of these — plus lifecycle events, save side-effects, the permission gate, and the `vendors` plan cap — are detailed on [[products-vendors-rules]].

## Related

- [[products]] — parent hub.
- [[products-products]] — products are assigned a vendor here; the vendor filter and Change vendor bulk action live there.
- [[products-categories]] — categories and vendors are independent taxonomies; a product has one vendor AND one or more categories.
- [[brand-model]] — separate richer brand+model metadata system (when installed), distinct from the vendor list here.
- [[settings-files]] — vendor logos stored here.
- [[apps-csv-import]] — bulk-create vendors via CSV.
- [[apps-xml-import]] — XML-import tasks that reference vendors block their deletion.
- [[api-vendors]] — JSON-API v2 vendor resource.
- [[vendor]] — entity page.
- [[product]] — entity page.

## Open questions

None.
