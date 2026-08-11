---
type: feature
nav_path: "Apps → Multilang"
route_name: apps.multilang.overview
route_path: /admin/apps/multilang
aliases: ["Multilang", "Multi-language", "Multilingual storefront", "Translations", "Многоезичен магазин", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, multi-language, storefront, sync]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 4
---
# Multilang (multilingual storefront)

## Purpose

**Multilang** enables **multiple language storefronts** managed from one CloudCart admin. The merchant designates one site as the master (primary language) and creates one or more **sister** sites (one per language); the platform syncs catalog data + translations from master → sisters.

Different from [[settings-translations]] (UI label translations) — Multilang is for FULL CONTENT translation: product names, descriptions, categories, blog articles, custom fields, etc. The storefront experience is fully localised per language.

Used by merchants who sell in multiple countries (Bulgaria + Romania + Greece), want SEO-optimised separate language sites (each with its own domain or sub-domain), or need per-language pricing / catalog / payment / shipping rules.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be paused is an individual **sister site** — each language store has its own status and can be paused or deleted from the Stores tab, see [[apps-multilang-stores]].

## Where to find it

Sidebar → Apps → install → **Multilang**. Route: `/admin/apps/multilang`. Sister sites are managed from the **Stores** tab ([[apps-multilang-stores]]).

Tab sub-pages (per existing wiki):

| Sub-page | Purpose |
|----------|---------|
| Overview | App status. |
| Settings ([[apps-multilang-settings]]) | Master-level configuration. |
| Stores ([[apps-multilang-stores]]) | Sister-site setup + management. |
| Products ([[apps-multilang-products]]) | Translation status per product. |
| Create step ([[apps-multilang-create-step]]) | Setup wizard. |
| Progress ([[apps-multilang-progress]]) | Sync progress tracker. |

## What the merchant can do here

- Set up sister language sites (each with its own domain / locale).
- Translate products from master → sister sites (Google Cloud Translation — see [[apps-multilang-main-translation-engine]]).
- Configure per-language pricing / payment / shipping overrides.
- Sync products from master to sister sites (manual or auto-trigger).

### What the merchant CANNOT do here

- Run Multilang without remaining plan quota for the translate / copy feature.
- Translate orders / customer data (orders stay in source language; only catalog content is translated).
- Push sister-side edits back to the master — sync is one-way (see [[apps-multilang-main-model]]).

## Sub-pages (in this cluster)

This topic is split into three aspect pages, each covering a distinct concept. The Assistant should drill into the aspect that matches the question, not read all three.

- [[apps-multilang-main-model]] — the master + sister-site model: one-way master → sister sync, no sister → master push, re-translate overwrites sister edits, per-site slugs, and how Multilang ("one catalog, many languages") differs from [[apps-stores]] ("many catalogs").
- [[apps-multilang-main-translation-engine]] — Google Cloud Translation API v3 (NOT Cloudio); `SYNC_TRANSLATE` / `SYNC_COPY` plan-feature quota gating; copy-vs-translate fallback; no review queue; 3-attempt retry; slug de-dup; in-body URL rewrite; internal cost accounting.
- [[apps-multilang-main-seo-domains]] — auto-generated `hreflang` SEO tags; new-sister provisioning at `<slug>.cloudcart.net` then custom-domain mapping; language switcher (`show_language`); force-stop / force-restart and `FREE_FOR` are CloudCart-internal-only.

## Settings & fields

The integration creates an `@app_multylanguage_sites` table (note the legacy "multylang" spelling in some module names) for site definitions. Two plan-feature keys gate sync:

- `SYNC_TRANSLATE = 'multilang_product_translate'` — translate-product operations.
- `SYNC_COPY = 'multilang_product_copy'` — copy-product operations (duplication without translation).

Field-level detail lives on the aspect pages: translation engine + quota on [[apps-multilang-main-translation-engine]]; `show_language` switcher + create-wizard subdomain slug on [[apps-multilang-main-seo-domains]]; the per-sister Configuration modal on [[apps-multilang-stores]].

## Business rules

- **One master, N sisters; sync is one-way.** The master controls the canonical catalog; sisters receive synced data + translations. There is no automatic sister → master push, and re-translating overwrites sister-side edits. See [[apps-multilang-main-model]].
- **Two distinct sync tasks** — `multilang_product_translate` (translates fields) and `multilang_product_copy` (copies verbatim, no translation). Both run on background queues; the merchant watches [[apps-multilang-progress]]. See [[apps-multilang-main-translation-engine]].
- **Each sister can override** product content, pricing, payment / shipping providers, and templates / themes — making it a real localised storefront.
- **SEO hreflang is auto-generated** across the network; the master gets `x-default`. See [[apps-multilang-main-seo-domains]].
- **Multilang ≠ Stores.** Multilang is "one catalog, many languages"; [[apps-stores]] is "many catalogs / many businesses." Both can be active. See [[apps-multilang-main-model]].

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store.
- [[multi-language]] — the platform-wide content-translation concept this app implements (layers, sister-site model, sync + fallback).
- [[apps-multilang-main-model]] — master/sister model + sync direction.
- [[apps-multilang-main-translation-engine]] — Google translation engine + quota.
- [[apps-multilang-main-seo-domains]] — hreflang, domains, language switcher.
- [[apps-multilang-settings]] — settings sub-page.
- [[apps-multilang-stores]] — sister-site setup + management.
- [[apps-multilang-products]] — per-product translation status.
- [[apps-multilang-create-step]] — setup wizard.
- [[apps-multilang-progress]] — sync progress.
- [[settings-translations]] — UI labels (separate from content translation).
- [[settings-domains]] — domain configuration for sister sites.
- [[apps-cloudio-overview]] — separate OpenAI-based AI app (NOT used by Multilang translation).
- [[apps-stores]] — multi-storefront concept; contrasted with Multilang.

## Open questions

None — uncertainties distributed to the aspect pages.
