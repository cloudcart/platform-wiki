---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → UpSell List"
route_name: admin.up_sell.list
route_path: /admin/marketing-new/up-sell
aliases: ["UpSell list", "UpSell offers", "Списък UpSell", "Списък оферти UpSell", "Замяна с по-добър продукт"]
tags: [marketing, upsell, cross-sell, list, offers]
plan_gates: ["upsells"]
created: 2026-05-23
updated: 2026-06-10
source_count: 4
---
# UpSell List

## Purpose

The **UpSell List** is the merchant's catalog of **product-replacement offers** — rules that, at the moment a customer adds Product X to cart, fire a popup proposing they swap X for a **better / pricier alternative** Y. Each row is one offer; clicking it opens the offer's editor ([[marketing-up-sell-diagram]]). The list shows **master records only** (a backend `master` scope) — new offers are standalone; multi-step chains are a legacy concept the current editor no longer builds (see [[marketing-up-sell-diagram]]).

UpSell is distinct from [[marketing-cross-sell-list]] in three key ways:

1. **Trigger model**: UpSell triggers on a single event — *"customer added the trigger product/variant to cart"*. Cross-Sell triggers on six configurable events (cart view, checkout, payment-method selection, etc.).
2. **Action model**: UpSell offers exactly **one** alternative variant to **replace** the trigger variant (1-to-1 swap). Cross-Sell offers up to **10 complementary products** alongside the cart contents.
3. **Pricing model**: UpSell expresses the offer as the **price difference** between trigger and offer (the *"only X more"* framing). Cross-Sell expresses it as a flat discount or free-product gift.

## Where to find it

Sidebar → Marketing → **UpSell** (`up_sell.header.title` = *"UpSell"*). Direct URL: `/admin/marketing-new/up-sell`. The middleware gating all admin UpSell routes is `cc_apps_purchase:up_cross_sell` — the merchant must have the Up/Cross-Sell app installed (see [[apps-up-cross-sell]]).

The page provides the offer table, the Status and Event filter dropdowns, bulk delete, and the "Add UpSell" button that opens the offer editor.

## What the merchant can do here

- **Browse the offer table** — a grid showing one row per offer (master records), with aggregate-metric columns (sales, views, success rate, in-stock, active toggle). See [[upsell-list-table]] for the full column reference.
- **Create a new offer** — the **Add UpSell** button opens the offer editor ([[marketing-up-sell-diagram]]) for a new offer. See [[upsell-list-actions]].
- **Edit an existing offer** — clicking a row's title link opens that offer's diagram page (a single-offer summary + Edit modal). See [[upsell-list-actions]].
- **Toggle active per row** — the Active column switch flips **that offer's** status inline (single record — no chain cascade). See [[upsell-list-actions]].
- **Delete offers** — per-row, or in bulk via the checkbox column. There is no activate / deactivate / duplicate bulk action. See [[upsell-list-actions]].
- **Filter by Status** — the only exposed filter (All / Active / Inactive). See [[upsell-list-table]].

The merchant **cannot** open an inline create form here, filter by trigger / offer product, bulk-edit offer fields, or see per-row trigger / offer product columns — see [[upsell-list-table]].

## Sub-pages (in this cluster)

This feature is split into 5 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[upsell-list-table]] — the offer grid: eight aggregate-metric columns; the 3-4 per-row SQL subqueries (sales-generated, total-sales, success-rate, in-stock-offer) and their performance cost; the Status filter; the empty state; what the table deliberately does NOT show.
- [[upsell-list-actions]] — create (opens the offer editor), edit (modal), per-row Active toggle (single record), and bulk **delete**; how delete removes any attached legacy child offers; no duplicate action.
- [[upsell-list-validation]] — the create / edit form fields and their validation (title lengths, hex colors, date-window rules) and the bundle-exclusion rule (`not_bundle`).
- [[upsell-list-storefront-firing]] — when the popup actually shows to a customer: the in-stock-offer gate, the already-in-cart filter, and the no-dedupe view counter; how `views` / `added_to_cart` / `total_cancel` are incremented storefront-side and cannot be reset by the merchant.
- [[upsell-list-plan-budget]] — the `upsells` plan-feature counter, the **(N remaining)** slot budget shown on the Add button, what happens at the cap, and the separate `cc_apps_purchase:up_cross_sell` app gate.

## Settings & fields

The list view itself has no top-level settings — each offer owns its own copy of the fields (internal title, offer title, trigger / offer variant, popup copy, colors, date window). The field-by-field breakdown and validation live on [[upsell-list-validation]]. The per-row metric columns and their data sources live on [[upsell-list-table]].

## Business rules

Each rule is documented in full on its aspect page:

- **List shows master records only** (`parent = 1`) — any legacy multi-step chain appears as ONE row. See [[upsell-list-table]].
- **Each row is interactive two ways** — title opens the diagram, the Active switch toggles inline. See [[upsell-list-actions]].
- **Status is a single-record toggle** (no cascade); **delete** also removes any attached legacy child offers; there is **no duplicate** action. See [[upsell-list-actions]].
- **Sales metrics attribute per-record** — each offer's row reflects only its own acceptances. See [[upsell-list-table]].
- **Bundles cannot be trigger or offer** — enforced at request validation. See [[upsell-list-validation]].
- **The popup only fires when the offer variant is in stock (or `continue_selling`) AND not already in the cart.** See [[upsell-list-storefront-firing]].
- **Plan-tier slot budget** — each offer counts against the `upsells` cap (legacy chains also counted every descendant). See [[upsell-list-plan-budget]].
- **Permission** — all routes gated by the Up/Cross-Sell app middleware. See [[upsell-list-plan-budget]].

## Related

- [[marketing-up-sell-diagram]] — every row opens into this; the Add button routes here directly.
- [[marketing-cross-sell-list]] — sister list for cross-sell offers (different trigger / action model).
- [[marketing-cross-sell]] — Cross-Sell engine details (events, targets, actions).
- [[apps-up-cross-sell]] — gateway app gating all UpSell admin routes.
- [[products-products]] — products picked as trigger / offer variants.
- [[plans]] — sets the `remaining` slot budget.
- [[apps-cart-rules]] — sister conditional rule engine (fires DISCOUNTS, not product swaps).

## Open questions

No outstanding questions.
