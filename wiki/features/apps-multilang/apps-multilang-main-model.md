---
type: feature
nav_path: "Apps → Multilang → Master/sister model"
route_name: apps.multilang.overview
route_path: /admin/apps/multilang
aliases: ["Multilang master site", "Multilang sister sites", "Master vs sister", "Multilang sync direction", "Re-translate overwrite", "Multilang conflict resolution"]
tags: [apps, administration, multi-language, storefront, sync]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-multilang]]. See the hub for the other aspects (translation engine, SEO & domains).

# Multilang — master/sister model

## Purpose

This page documents **how Multilang structures a multilingual store**: one **master** site holds the canonical catalog, and each language gets its own **sister** site that receives synced + translated content from the master. It also covers the **direction** of that sync (master → sister only), what happens when the merchant edits a sister directly, and how re-translating a product overwrites sister-side edits. For the translation engine itself see [[apps-multilang-main-translation-engine]]; for hreflang / domains see [[apps-multilang-main-seo-domains]].

## Where to find it

Sidebar → Apps → install → **Multilang**. The master/sister relationships are managed from the **Stores** tab — see [[apps-multilang-stores]]. Route: `/admin/apps/multilang`.

## What the merchant can do here

- Designate ONE site as the master (primary language); every translation target is a sister site.
- Sync the master catalog (products, categories, blog articles, pages, custom fields) out to each sister site.
- Edit a sister-site entity directly for final polish — knowing the master will not pick that edit up.
- Switch into a sister site's admin from the master without re-authenticating (cross-site login token).
- Re-trigger translation per product from [[apps-multilang-products]] (overwrites the sister copy — see Business rules).

### What the merchant CANNOT do here

- Push a sister-side edit back up to the master — there is no automatic sister → master sync.
- Treat a sister copy as a parallel canonical edit — re-translation will discard it.
- Translate orders / customer data — orders stay in the source language; only catalog content is translated.

## Settings & fields

- **Master vs sister flag** — each site identifies whether it is the master or a sister (the master's flag is empty; sisters point at the master's site_id). This flag drives `x-default` hreflang selection (see [[apps-multilang-main-seo-domains]]) and which side a sync runs from.
- **Site relationships** — the platform stores, per entity (product / category / article), the link between the master record and its sister-site version, so it knows which translated record corresponds to which master record.
- **Cross-site login token** — a one-time login code generated for cross-site admin navigation (default target `/apps/multilang/create/step/2`). It authenticates the merchant against the sister site so they can switch admins without re-entering credentials.
- **Site activation lifecycle** — when a sister site completes its install handshake, the master's setting is updated to mark that site as active in the network.

## Business rules

### Master → sister is one-way; relationships are persistent

The platform stores a many-to-one relationship from each sister-site entity to the master entity. When the merchant edits the master product, the sync tasks (`multilang_product_translate` / `multilang_product_copy`) push the change to sister sites. **There is no automatic sister → master push.** When the merchant edits a sister-site entity directly, that change stays local to the sister; the master does not pick it up. The merchant must treat the master as the canonical source of truth for content.

### Conflict resolution: re-translate OVERWRITES sister-side edits

When the merchant triggers re-translation for a product, the platform queues a fresh translation that REPLACES the existing sister-side content. Any manual edits the merchant made on the sister copy are LOST when they re-run the translator on the same product. The merchant should treat sister-side edits as final-step polish AFTER the auto-translation completes, not as a parallel canonical edit.

### URL handle (slug) is per-site — sisters keep their own slugs

Each translated entity has its OWN URL handle on the sister site. The merchant CAN have `/product/laptop` on the English site and `/produkt/laptop` on a Bulgarian sister site. The relationship table maps master `primary_slug` ↔ sister `secondary_slug` so the language switcher's "View this same product in English" button works even when slugs differ. (Slug auto-deduplication is handled by the translation engine — see [[apps-multilang-main-translation-engine]].)

### Stores app vs Multilang — different concerns

Multilang is the engine for language-specific sister sites driven from one master admin. [[apps-stores]] (separate app) is a multi-storefront feature where different stores have potentially DIFFERENT catalogs and operate as independent businesses. **Multilang is for "one catalog, many languages"; Stores is for "many catalogs / many businesses."** They are separate apps with separate data models — both CAN be active, but the merchant typically picks one model depending on whether they want translated copies of one catalog or independent sister stores.

### Per-language overrides

Each sister site can override product names, descriptions, categories, custom fields; pricing (different EUR / RON / etc. prices); payment / shipping providers; and templates / themes. This is what makes a sister a real localised storefront rather than a mirror.

### Permission

Standard apps permission scope.

## Related

- [[apps-multilang]] — Multilang feature hub.
- [[apps-multilang-stores]] — where master/sister sites are managed.
- [[apps-multilang-products]] — per-product translation status + re-trigger.
- [[apps-multilang-create-step]] — sister-site setup wizard.
- [[apps-stores]] — multi-storefront app (many catalogs), contrasted above.
- [[settings-translations]] — UI label translations (separate from content translation).

## Open questions

None.
