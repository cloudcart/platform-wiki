---
type: feature
nav_path: "Apps → Multilang → Stores → Configuration modal"
route_name: apps.multilang.stores
route_path: /admin/apps/multilang/stores
aliases: ["Multilang per-sister configuration", "Sister site configuration modal", "Multilang translate toggles", "Multilang price transform", "Multilang URL manipulation"]
tags: [apps, administration, multilang, stores, sister-sites, translation]
plan_gates: [multilang_product_copy, multilang_product_translate]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-multilang-stores]]. See the hub for the other aspects (sister-sites table, network mechanics).

# Multilang → Stores — per-sister Configuration modal

## Purpose

The per-row **Configuration** action on the [[apps-multilang-stores-table|Stores table]] opens a right-side modal where the merchant controls everything about how one sister site is fed from the master: whether new master products are copied at all, which fields get AI-translated, how the price is transformed at copy time, the approval method, and how URLs inside descriptions are rewritten. **This is the ONLY surface where the merchant configures per-sister translation behaviour after the create wizard.** The same fields can also be tweaked at the master level via [[apps-multilang-settings]] to set master-default values.

## Where to find it

Sidebar → Apps → Multilang → **Stores tab** → a sister-site row's **Configuration** action. Route context: `/admin/apps/multilang/stores`. The modal loads via `GET /admin/api/multilang/site-settings/{site_id}` and persists via `POST /admin/api/multilang/site-settings/{site_id}`.

## What the merchant can do here

- Turn copying of newly-added master products to this sister on or off.
- Enable AI translation and choose which product fields are translated (9 per-field toggles).
- Apply a per-product price multiplier and a marketing-rounding rule at copy time.
- Choose `manual` vs `automatic` product approval.
- Enable automatic cascade-delete when a master product is deleted.
- Set the per-sister storefront language-switcher visibility.
- Choose how URLs inside copied descriptions are handled.

## Settings & fields

| Field | What it controls |
|---|---|
| **Copy newly added products from {main_site} to {this_site}** (`settings.products`) | Master toggle. When OFF, the modal collapses the translate / price / approval sub-fields. Requires `multilang_product_copy` plan quota — "additional service" link opens the per-feature upsell. |
| **AI translation** (`settings.translate.active`) | Sub-toggle (only visible when `products = 1`). Requires `multilang_product_translate` plan quota. When OFF, products are copied verbatim without translation. |
| **Translate title** (`settings.translate.title`) | Per-field translation toggle. |
| **Translate description** (`settings.translate.description`) | Per-field translation toggle. |
| **Translate category** (`settings.translate.category`) | Per-field translation toggle. |
| **Translate variants** (`settings.translate.variety`) | Per-field translation toggle. |
| **Translate meta title and description** (`settings.translate.meta`) | SEO meta tags. |
| **Translate product tags** (`settings.translate.product_tags`) | Tags. |
| **Translate product characteristics** (`settings.translate.properties`) | Product properties. |
| **Translate product tabs** (`settings.translate.tabs`) | Product description tabs. |
| **Translate alt tags** (`settings.translate.alt_tags`) | Image alt text. |
| **Copy price** (`settings.price`) | When on, exposes the two price-transform fields below. |
| **Multiply the original price by** (`settings.price_change`, number 0-99, step 0.01) | Per-product price multiplier applied at sync time (e.g., `1.10` adds 10%). |
| **Round price up to** (`settings.price_round`, number 0-99) | Marketing-price rounding (e.g., set to 95 → BGN 94.30 becomes BGN 94.95). |
| **Approval method** (`settings.method`) | Dropdown: `manual` (default — new master products NOT auto-copied; merchant approves each via [[apps-multilang-products]]) or `automatic` (auto-copy on master create). |
| **Automatic product deletion** (`settings.delete`) | When ON, deleting a master product cascades the delete to this sister. |
| **Display the language version on the site** (`settings.show_version`) | The per-sister storefront language-switcher visibility — same flag as the footer toggle on [[apps-multilang-stores-table]], but settable per sister site from this modal. |
| **Manipulating URLs in descriptions** (`settings.url_manipulation`, 3 options) | 1 = Remove the URLs from the description, 2 = Do not change the URLs at the description, 3 = Try to change the URLs with the new domain. |
| **If the system can not identify the right URL remove the link from the description** (`settings.url_remove`, default 1) | Sub-toggle visible only when `url_manipulation = 3` — fallback behaviour when URL rewrite can't find a sister-side match. |

## Business rules

### The products master toggle gates everything below

When **Copy newly added products** (`settings.products`) is OFF, the modal collapses the AI-translation, price, approval, and deletion sub-fields — the sister's catalog stays manually curated. The `multilang_product_copy` plan quota gates the toggle itself; `multilang_product_translate` gates the **AI translation** sub-toggle separately. Hitting a quota surfaces an "additional service" upsell link rather than silently failing.

### Save is INSTANT — no separate "publish" step

Clicking Save persists the settings JSON to the sister's `@app_multylanguage_sites` row immediately. The next master-side product save triggers the new behaviour (copy / translate / price transform / etc.) for that sister site. There is **no "Apply to existing products" button** — historical products on the sister keep their existing translations until the merchant explicitly re-runs sync from [[apps-multilang-products]].

### URL fallback only matters in option 3

`settings.url_remove` is meaningful only when `settings.url_manipulation = 3` ("Try to change the URLs with the new domain"). It decides what happens when the rewrite can't find a matching sister-side URL: by default (`1`) it strips the link from the description.

## Related

- [[apps-multilang-stores]] — hub.
- [[apps-multilang-stores-table]] — the list view this modal opens from.
- [[apps-multilang-products]] — per-product approval / manual sync; where historical re-sync is triggered.
- [[apps-multilang-settings]] — master-level defaults for these same fields.
- [[apps-multilang]] — Multilang feature hub; translation queue tasks.
- [[plan-gates]] — `multilang_product_copy` + `multilang_product_translate` quotas.

## Open questions

- Confirm exact rounding semantics of `price_round` for sub-unit prices.
