---
type: feature
nav_path: "Apps → OLX → Products"
route_name: apps.olx.products
route_path: /admin/apps/olx/products
aliases: ["OLX Products", "OLX products to publish", "OLX product list"]
tags: [apps, olx, marketplace, products, publishing]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---
# OLX → Products

## Purpose

The **Products** tab is where the merchant picks **which CloudCart products to publish as OLX adverts** and tracks the publication status of each. It is the **outgoing pipeline** view — products selected for publishing, in-progress publishes, validation flags, and per-product status. This contrasts with the [[apps-olx-adverts]] tab, which lists adverts ALREADY live on OLX.

This hub is a navigation pivot. The mechanics are split across four aspect pages — drill into the one that matches the question rather than reading all of them. For the whole OLX feature set (settings, taxonomy mapping, OAuth), see [[apps-olx]].

## Sub-pages (in this cluster)

- [[apps-olx-products-pipeline]] — the Products tab UI: data-table columns, filters, empty state, the **+ Add advert** multi-product picker modal, the bulk-publish loop, and what the merchant can / cannot do here.
- [[apps-olx-products-validation]] — pre-publish validation rules, per-product OLX state fields, the Add-advert autocomplete pre-filter (price + image + mapped category + not-already-published), the missing-price mid-publish error, and how failures surface in [[apps-olx-history]].
- [[apps-olx-products-sync]] — stock / status / delete auto-sync, the manual price re-sync (**Sync prices** + per-row Sync), advert lifecycle / expiry, and why expired-advert re-publish is a manual step.
- [[apps-olx-products-formatting]] — how the advert payload is auto-built: title capitalization + 70-char truncation + variant suffix, the description concatenation + character-stripping regex, image pass-through, BG/RO condition+currency forcing, and the `merge_product` per-variant split.

## Where to find it

Sidebar → Apps → OLX → **Products tab**. Route: `/admin/apps/olx/products` (`route_name: apps.olx.products`). The Vue uses `app-name="olx"` for the data-table state.

## What the merchant can do here

Each row shows a product + its OLX state (Pending / Created / Failed / Rejected with reason). From the Products tab the merchant can:

- Add new products to the OLX-publishing pipeline via **+ Add advert** — see [[apps-olx-products-pipeline]].
- Re-try / re-sync failed or expired publishes — see [[apps-olx-products-sync]].
- View per-product validation status and fix the underlying issue — see [[apps-olx-products-validation]].
- Pause / resume / delete OLX listings for specific products.
- Bulk-trigger price re-sync to push current CloudCart prices to OLX.

## Settings & fields

The Products tab itself carries no app-level settings — those live on [[apps-olx-settings]] (`sync_quantity`, `sync_status`, `sync_delete`, `is_discount`, `merge_product`, `title_trim`). The per-product OLX state fields (OLX advert ID, External ID, Status, Created date, Validation errors) are documented on [[apps-olx-products-validation]]. Category + parameter + value mappings (prerequisites for any publish) live on [[apps-olx-configuration]], [[apps-olx-parameters]], and [[apps-olx-parameters-values]].

## Business rules

- **Each product publishes as a SEPARATE OLX advert.** There is no native batch endpoint — a bulk Upload action loops the selected product IDs and hits OLX once per product. See [[apps-olx-products-pipeline]].
- **Adverts have a finite lifetime on OLX** (typically 30 days). After expiry the Status field shows Expired and re-publish is manual. See [[apps-olx-products-sync]].
- **Publish is blocked until validation passes** — a product can be added but stays un-publishable while the Valid column shows X. See [[apps-olx-products-validation]].
- **The OLX advert always uses the CloudCart product's own data** — there is no separate OLX title / description / image override per product. See [[apps-olx-products-formatting]].
- **Permission**: standard apps permission scope.

## Related

- [[apps-olx]] — OLX hub (whole feature set).
- [[apps-olx-adverts]] — active adverts on OLX (sister view).
- [[apps-olx-configuration]] — category mapping (required for publish).
- [[apps-olx-parameters]] — parameter setup (required for publish).
- [[apps-olx-parameters-values]] — value mapping (required for publish).
- [[apps-olx-settings]] — the sync + formatting toggles.
- [[apps-olx-history]] — operation log / per-product error detail.
- [[apps-olx-products-pipeline]] — Products tab UI + Add-advert modal.
- [[apps-olx-products-validation]] — validation rules + autocomplete pre-filter.
- [[apps-olx-products-sync]] — stock / status / price / delete sync.
- [[apps-olx-products-formatting]] — advert payload build.
- [[products-products]] — source CloudCart products.

## Open questions

- Per-country OLX daily publish-limit / rate limits (verify).
