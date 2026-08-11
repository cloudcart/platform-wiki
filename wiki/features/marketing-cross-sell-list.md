---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → Cross-Sell List"
route_name: admin.cross_sell.list
route_path: /admin/marketing-new/cross-sell
aliases: ["Cross-Sell list", "Cross-Sell offers", "Списък кръстосани продажби", "Списък оферти Cross-Sell", "Свързани продукти списък"]
tags: [marketing, cross-sell, upsell, list, offers]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# Cross-Sell List

## Purpose

The **Cross-Sell List** is the merchant's catalog of **conditional product-recommendation offers** — rules that fire at one of six cart/checkout/order moments to surface complementary products with optional discounts. Each row is the **root** of a Cross-Sell chain; clicking the row opens the chain in the visual diagram editor ([[marketing-up-sell-diagram]], which serves both UpSell and Cross-Sell trees).

Cross-Sell is the *"customers who buy X also buy Y"* engine — distinct from [[marketing-up-sell-list]] (which replaces a single variant with a better one) and from [[apps-cart-rules]] (which fires discounts at cart, not product recommendations).

This page is the **LIST view** — it shows aggregate records. For the rule engine itself (events, targets, actions, discount types) see [[marketing-cross-sell]]. This hub is slim; the per-aspect detail lives in the sub-pages below.

## Sub-pages (in this cluster)

- [[cross-sell-list-grid]] — the offer grid: the columns, per-row data sources, and how sales metrics are scoped to the individual offer record.
- [[cross-sell-list-actions]] — everything the merchant DOES from the list: Add, edit, per-row Active toggle, bulk delete, status / event filters, empty state, plus the full UI-surface / confirmation audit.
- [[cross-sell-list-validation]] — the required-field set when creating / editing an offer (titles, type, event, targets, actions, limits, discount, date window).
- [[cross-sell-list-plan-budget]] — master-only list model, single-record status, no duplicate, the per-plan slot budget, the `products_limit` 1-10 cap, and the Cross-Sell-vs-UpSell separation.

## Where to find it

Sidebar → Marketing → **Cross-Sell** (`cross_sell.header.title` = *"Cross Sell"*). Direct URL: `/admin/marketing-new/cross-sell`. Middleware: `cc_apps_purchase:up_cross_sell` — the Up/Cross-Sell app must be installed (see [[apps-up-cross-sell]]).

## What the merchant can do here

The list is a read-only grid of offers (master records) with row-level and bulk operations layered on top. At a glance the merchant can:

- **Browse** the paginated offer table with per-offer performance metrics (views, added-to-cart, success rate, attributed sales) — see [[cross-sell-list-grid]].
- **Create** a new offer via the "Add Cross Sell" button (opens the offer editor), **edit** an existing one by clicking its title, **toggle** it active per row, **bulk delete** selected rows, and **filter** by status or event — see [[cross-sell-list-actions]].

What the merchant CANNOT do here: open an in-page create form, filter by target product / date range, see an offer's targets at a glance, bulk-edit content fields, bulk activate / deactivate / duplicate, or export the list. Full list in [[cross-sell-list-actions]].

## Settings & fields

The list grid itself has no editable settings — every field is configured inside the diagram editor. The required-field set the editor validates (internal title, offer title, type, event, targets, actions, products limit, max user views, discount type, active window) is documented in [[cross-sell-list-validation]]. The per-row data-source subqueries that feed the grid columns are in [[cross-sell-list-grid]].

## Business rules

The list-level rules are split across the aspect pages:

- **List shows master records only** (`parent = 1`); any legacy multi-step chain shows ONE row. **Status is a single-record toggle** (no cascade); **delete** removes any attached legacy child offers; there is **no duplicate** action. See [[cross-sell-list-plan-budget]].
- **Sales metrics are scoped to the individual offer record** — each offer's row reflects only its own conversions. See [[cross-sell-list-grid]].
- **Plan-tier slot budget is a real gate** enforced at save time, and **`products_limit` is hard-capped at 1-10**. See [[cross-sell-list-plan-budget]].
- **Cross-Sell and UpSell are separate features** (separate tables, separate endpoints) that share only the diagram route. See [[cross-sell-list-plan-budget]].

## Related

- [[marketing-cross-sell]] — Cross-Sell engine details (events, targets, actions, display types, hide-cart-products filter, discount integration).
- [[marketing-up-sell-list]] — sister list for UpSell offers (different trigger / action model).
- [[marketing-up-sell-diagram]] — visual flow builder that hosts both UpSell and Cross-Sell trees.
- [[apps-up-cross-sell]] — gateway app gating all admin routes.
- [[products-products]] / [[products-categories]] / [[products-vendors]] / [[products-smart-collections]] — record types referenced by Cross-Sell targets and actions.
- [[marketing-discounts]] — discount records attached to offers via the `discount_percent` / `discount_type` fields.
- [[plans]] — sets the per-plan slot budget.
- [[apps-cart-rules]] — sister conditional engine (DISCOUNTS, not recommendations).

## Open questions

No outstanding questions.
