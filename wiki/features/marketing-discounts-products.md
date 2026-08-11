---
type: feature
nav_path: "Marketing → Discounts → Products"
route_name: discounts-products
route_path: /admin/marketing-new/discounts/products/:id
aliases: ["Discount products", "Fixed discount product list", "Product picker for fixed discount", "Продукти в отстъпката", "Продукти за фиксирана цена"]
tags: [marketing, discounts, fixed, products, product-picker]
plan_gates: ["discount_fixed"]
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---

# Discount products (product list for Fixed discount)

## Purpose

The **Discount products** page is the merchant's product-management surface for a **Fixed-type discount** — the list of every product currently attached to the discount, plus the per-product price-edit modal. It bridges the parent Fixed discount's settings (date window, customer groups, MSRP mode) and the per-product per-variant price overrides stored against it.

The merchant uses this page to see every product on the discount, add a product (via the **Discount product modal** with Common or Multiple pricing modes), edit prices, toggle per-row active state, remove single or bulk products, and filter / sort the list. For the per-variant price-storage model, MSRP mode, customer-group fan-out, and storefront read path, see [[marketing-discounts-fixed]] — that page documents the deeper Fixed-discount mechanics. This hub points at the **list / picker UI** layer on top.

This topic is split into 5 aspect pages — drill into the one that matches the question.

## Sub-pages (in this cluster)

- [[discounts-products-list-view]] — list columns, filters, sorting, row toggle / remove, bulk actions, paging.
- [[discounts-products-modal-flow]] — Add / Edit modal sequence (picker, pricing-mode radio, three pricing-table variants, save / close cleanup).
- [[discounts-products-fields]] — fields reference (list columns, modal inputs, validation messages, toast strings).
- [[discounts-products-save-replace]] — full-replace save semantics, the DB-transaction order, the events fired (`ProductUpdated`, the search re-index).
- [[discounts-products-business-rules]] — type guard, picker source, MSRP-mode savings display, default Fixed discount singleton, customer-group + date inheritance, the silent-drop behaviour for `fixed_price >= variant.price`.

## Where to find it

From the [[marketing-discounts]] list, the **Products** link on any **Fixed**-type discount row opens this page. The breadcrumb reads "Marketing → Discounts → Products". The route is `/admin/marketing-new/discounts/products/:id` where `:id` is the parent discount's id. The modern Vue page replaces the legacy products listing; the legacy URL `/admin/discounts/products/{discount_id}` continues to drive the same underlying API.

## What the merchant can do here

- See every product attached to this discount, with the original-vs-discounted price formatted inline. See [[discounts-products-list-view]].
- Add a product via the **Discount product modal**, picking **Common price** (one price for all variants) or **Multiple price** (per-variant prices). See [[discounts-products-modal-flow]].
- Edit prices by clicking a row — the same modal opens pre-filled. See [[discounts-products-modal-flow]].
- Toggle a product's discount active / inactive inline; bulk-toggle status via the table action bar. See [[discounts-products-list-view]].
- Remove a single product, or bulk-delete selected products. See [[discounts-products-list-view]].
- Filter by Active = Yes / No; sort by Price or Active. See [[discounts-products-list-view]].

What the merchant cannot do here:

- Add a product already on this Fixed discount (validator rejects with *"Variant already exists in discount."*).
- Set a fixed price ≥ the variant's catalog price — rejected per-variant with *"Price must be at least 1 and less than <variant.price>"*. See [[discounts-products-fields]].
- Bulk-import prices — the modal is one product at a time; for mass-price changes, use the Products listing's price-import workflow.

## Settings & fields

The list shows **Product Name** (image thumbnail + name), **Price** (struck-through original / new fixed price, with the EUR-to-EUR dual display when active), **Active** toggle, and a **Remove** action. Filterable by **Active** = Yes / No. Sortable by **Price** and **Active**. Bulk actions: *"Set status active"*, *"Set status unactive"*, and the default delete. The Discount product modal exposes a Product picker (add mode), a Pricing-type radio (multi-variant products), a read-only **Price in store** column, and a **New price** input per variant or shared. See [[discounts-products-fields]] for the full reference.

## Business rules

The parent Fixed discount drives almost everything here. The list-page is plan-gated by `discount_fixed` (inherited); all CRUD endpoints sit under the standard `marketing.discounts` permission; the controller hard-filters to `type = fixed` (404 otherwise); per-variant rows fan out from each modal save; the **save flow is a full replace per `(discount_id, product_id)`** — pre-filling all variants in the modal mitigates accidental drops. Customer-group fan-out, date inheritance, and the MSRP-mode "Save X EUR" display all derive from the parent discount, not from this page. See [[discounts-products-business-rules]] for the full catalogue and [[discounts-products-save-replace]] for the transaction order.

## Related

- [[marketing-discounts]] — parent feature; the Fixed-type discount opens to here via the "Products" link.
- [[marketing-discounts-fixed]] — the deeper per-variant attachment / pricing model, MSRP mode, customer-group fan-out, storefront read path. **Read together** with this page for the full picture.
- [[marketing-discounts-codes]] — Container-type code list (the analogue for code-based discounts).
- [[marketing-discounts-code-pro]] — Code PRO multi-code campaigns (another code-based discount type).
- [[discount]] — entity page for the parent Fixed discount.
- [[products-products]] — the products attached to the Fixed discount; the picker queries this catalog.
- [[customers-custom-groups]] — customer groups on the parent Fixed discount drive per-group row fan-out at save time.
- [[settings-hooks]] — `discount.updated` event fires on each save / toggle / delete here.
- [[apps-cart-rules]] — Cart Rules see Fixed-discount prices as the "after discounts" amount on cart lines.
- [[analytics-top-order-product-discounts]] — analytics dashboard surfacing top product-discount usage.

## Open questions

No outstanding questions.
