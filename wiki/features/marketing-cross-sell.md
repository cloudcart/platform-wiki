---
type: feature
nav_path: "Marketing → Cross-Sell & UpSell"
route_name: admin.cross_sell.list
route_path: /admin/marketing-new/cross-sell
aliases: ["Cross Sell", "Cross-Sell", "UpSell", "Cross Sell & UpSell", "Cross sell offers", "Свързани продукти", "Кръстосани продажби"]
tags: [marketing, cross-sell, upsell, recommendations, offers]
plan_gates: ["cross_sells"]
created: 2026-05-22
updated: 2026-06-10
source_count: 8
---
# Cross-Sell & UpSell

## Purpose

The **Cross-Sell & UpSell** module is the merchant's tool for **conditional product recommendations** at key purchase moments. Different from [[apps-cart-rules]] (which applies discounts conditionally), Cross-Sell shows **product offers** to customers based on triggers like "added a specific product to cart" or "reached checkout".

The two terms in the title:
- **Cross-sell**: "Customers who bought X also bought Y" — suggest COMPLEMENTARY products (e.g., laptop → laptop bag).
- **UpSell**: "Consider this BETTER version of X" — suggest HIGHER-TIER alternatives (e.g., 128GB phone → 256GB version).

Both run through the same engine — the merchant declares offers + the platform surfaces them at the configured trigger moment.

This is the **hub page** for the Cross-Sell cluster. It carries the high-level definition + plan gates; the configurable fields, trigger model, display modes, discounts, filters, and view-tracking mechanics each live in their own aspect page (see below). The [[apps-up-cross-sell]] gateway app redirects merchants here.

## Sub-pages (in this cluster)

This module is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read the whole cluster.

- [[cross-sell-offer-form]] — the 7-box create/edit form (titles, visual settings, conditions, product settings, discounts, date range) + the diagram-editor entry point.
- [[cross-sell-trigger-events]] — the 6 selectable trigger events (`add_to_cart` … `return_page`) + the four allowed target types (product / category / vendor / selection).
- [[cross-sell-display-discounts]] — Popup vs Add-to-cart display modes; the four discount types (`fixed` / `percent` / `shipping` / `free_product`) + the flags they auto-set.
- [[cross-sell-filters-limits]] — hide-cart-products / hide-out-of-stock filters; the 1-10 `products_limit` cap; `max_user_views = 0` = unlimited; the auto-add force-lock.
- [[cross-sell-view-tracking]] — cookie-based per-browser view cap, dismissal cookie, popup randomisation, the per-render view counter, on-delete cart cleanup.
- [[cross-sell-vs-cart-rules]] — how the engine compares to [[apps-cart-rules]]; the plan gates (`cross_sells`); the gateway app + middleware.

The **list view** (columns, filters, bulk actions, empty state) lives on its own page: [[marketing-cross-sell-list]].

## Where to find it

Sidebar → Marketing → **Cross-Sell & UpSell** (`Cross Sell & UpSell` per `header.install`). Direct URL: `/admin/marketing-new/cross-sell`.

The module now runs as a **Vue app under `/admin/marketing-new/cross-sell`** (the sidebar entry is the default; there is no separate legacy screen to switch to). Its screens are the offer **list view** ([[marketing-cross-sell-list]]), the create / edit **offer form** ([[cross-sell-offer-form]]), the visual **offer editor / diagram page** ([[marketing-up-sell-diagram]] documents the same page shape), and the customer-facing popup (styled from the offer form). The module is gated on the **Up/Cross-Sell app being installed** — the install gateway at `/admin/apps/up_cross_sell` opens this manager (see [[apps-up-cross-sell]]).

The "Add Cross Sell" button routes to the visual **offer editor** (the diagram page) at `/admin/marketing-new/cross-sell/diagram/:id` — the same page shape UpSell uses, see [[marketing-up-sell-diagram]].

## What the merchant can do here

- **Create / edit offers** through the 7-box form — internal + customer-facing titles, visual styling, trigger conditions, offered products, product settings, discounts, and an active date range. Full breakdown on [[cross-sell-offer-form]].
- **Pick a trigger event + targets** — choose one of 6 events and scope it to products / categories / vendors / smart-collection selections. See [[cross-sell-trigger-events]].
- **Pick a display mode + discount** — show a popup or silently auto-add to cart, and optionally attach a discount to the offered product. See [[cross-sell-display-discounts]].
- **Tune filters + limits** — hide already-in-cart / out-of-stock products, cap how many products show, cap how many times a customer sees the offer. See [[cross-sell-filters-limits]].
- **Manage the list** — activate / deactivate / delete in bulk, read per-row performance metrics. See [[marketing-cross-sell-list]].

What the merchant CANNOT do here (cluster-wide gaps):
- **No JSON-API access** — Cross-Sell offers are admin-only.
- **No multi-language preview** — the offer title / description is single-language; storefront language switching reuses the same text.
- **No analytics dashboard** beyond the list-row metrics.
- **No priority field** — when several offers match the same event, the winner is picked at random (see [[cross-sell-view-tracking]]).

## Settings & fields

The full field set is documented per-aspect. The 7 form boxes map to aspect pages as follows:

| Form box | Aspect page |
|---|---|
| Box 1 — Product (titles, description) | [[cross-sell-offer-form]] |
| Box 2 — Visual settings (colours, buttons, confetti) | [[cross-sell-offer-form]] |
| Box 3 — Target conditions (event + targets) | [[cross-sell-trigger-events]] |
| Box 4 — Action conditions (display type + offered products) | [[cross-sell-display-discounts]] + [[cross-sell-offer-form]] |
| Box 5 — Product settings (hide filters, max views) | [[cross-sell-filters-limits]] |
| Box 6 — Discounts (`discount_type`, value) | [[cross-sell-display-discounts]] |
| Box 7 — Date range (`active_from` / `active_to` / `no_expire` / timer) | [[cross-sell-offer-form]] |

### Validation per `error.validation.*`
- Offer title required: *"Моля, въведете заглавие на офертата."*
- Offer title min: *"Заглавието на офертата трябва да бъде минимум X знака."*
- Offer title max: *"Заглавието на офертата трябва да бъде по-малко от X знака."*

## Business rules

- **Trigger-action structure** mirrors [[apps-cart-rules]] — a Trigger (target) condition list + an Action (offered products) condition list — but Cross-Sell fires RECOMMENDATIONS, not discounts. See [[cross-sell-vs-cart-rules]].
- **Cross-Sell and UpSell are separate engines with the same style of offer editor** — each offer is edited on its own diagram page ([[marketing-up-sell-diagram]] for UpSell; the Cross-Sell equivalent at `/admin/marketing-new/cross-sell/diagram/:id`). There is no shared multi-step tree — each offer stands alone.
- **Per-offer plan cap** — UpSell and Cross-Sell offers count against **separate** numeric counters (`cross_sells` vs `upsells`). See [[cross-sell-vs-cart-rules]] + [[marketing-up-sell-list]].
- The detailed engine-level rules (event list, target types, discount auto-flags, filter force-locks, view-cap cookie semantics, randomisation, on-delete cleanup) live on the aspect pages linked above.

## Related

- [[cross-sell-offer-form]] — the create/edit form (aspect).
- [[cross-sell-trigger-events]] — events + targets (aspect).
- [[cross-sell-display-discounts]] — display modes + discounts (aspect).
- [[cross-sell-filters-limits]] — filters + limits (aspect).
- [[cross-sell-view-tracking]] — view-cap + randomisation (aspect).
- [[cross-sell-vs-cart-rules]] — engine comparison + plan gates (aspect).
- [[marketing-cross-sell-list]] — the list view (columns, filters, bulk actions).
- [[marketing-up-sell-list]] — sister UpSell list; separate `upsells` cap.
- [[marketing-up-sell-diagram]] — the offer editor / diagram page (same page shape for Cross-Sell and UpSell).
- [[apps-up-cross-sell]] — gateway app; redirects merchants here.
- [[apps-cart-rules]] — sister conditional rule engine (discounts vs recommendations).
- [[marketing-discounts]] — discount records that may be referenced.
- [[products-products]] / [[products-categories]] / [[products-vendors]] / [[products-tags]] / [[products-smart-collections]] — record types referenced in conditions.
- [[marketing-segments]] — segment membership can trigger offers.

## Plan gates

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `cross_sells` | Numeric | Per-plan cap on the number of Cross-Sell offers (counted against the platform code). Also listed in `restrict.creating` — when the cap is hit, the platform's standard plan-limit error blocks new creates. Extendable via feature pack. UpSell offers count against the **separate** `upsells` counter (see [[marketing-up-sell-list]]). |

When over the cap, the merchant is redirected to the per-feature upsell at [[plan-features]]. The whole [[apps-up-cross-sell]] gateway app must also be installed — the middleware `cc_apps_purchase:up_cross_sell` is a separate non-plan gate. See [[cross-sell-vs-cart-rules]] for the full gate stack.

## Open questions

No outstanding questions.
