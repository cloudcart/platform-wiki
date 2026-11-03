---
type: feature
nav_path: "Apps → Multilang → Translation engine"
route_name: apps.multilang.overview
route_path: /admin/apps/multilang
aliases: ["Multilang translation engine", "Google Cloud Translation", "Multilang copy vs translate", "Multilang retry policy", "Multilang quota", "machine_translation feature pack"]
tags: [apps, administration, multi-language, storefront, sync]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-multilang]]. See the hub for the other aspects (master/sister model, SEO & domains).

# Multilang — translation engine

## Purpose

This page documents **how Multilang actually translates content**: which engine it calls, the copy-vs-translate fallback, the plan-feature quota that gates sync, the per-record retry policy, slug de-duplication, the in-body URL rewrite, and the (internal) cost accounting. The structural master/sister model lives on [[apps-multilang-main-model]]; hreflang / domains on [[apps-multilang-main-seo-domains]].

## Where to find it

Sidebar → Apps → Multilang. Translations are triggered from the catalog / [[apps-multilang-products]] page and run on background queues; the merchant watches progress on [[apps-multilang-progress]]. Route: `/admin/apps/multilang`.

## What the merchant can do here

- Translate catalog content (products, categories, blog articles, pages) from master → sister automatically.
- Choose **copy** instead of **translate** when they do not want auto-translation (duplicates source text verbatim).
- Re-trigger a failed or pending record's translation from [[apps-multilang-products]].
- Consume their plan's translate / copy quota; sync halts when the quota for the period is exhausted.

### What the merchant CANNOT do here

- Send a translation through an approval / review gate before it goes live — there is no review queue (see Business rules).
- See Google's wholesale per-character cost — only their own plan-feature quota balance.
- Opt out of the in-body master-URL rewrite during translation.

## Settings & fields

- **`SYNC_TRANSLATE` = `multilang_product_translate`** — plan-feature key + queue task for translating product fields.
- **`SYNC_COPY` = `multilang_product_copy`** — plan-feature key + queue task for copying products WITHOUT translation (duplication only).
- **Underlying queue task names** — beyond the plan-feature keys, the workers are named `multylang_copy` (initial bulk copy + setup) and `multylang_translate` (per-record translation); Translate runs on the `translate` queue lane, and sister-site setup queues a `multylang_sites` task. These are merchant-invisible. (Note the legacy "multylang" spelling in some module names.)
- **`machine_translation` plan-feature pack** — sets `cc_price`, what CloudCart charges the merchant per translated symbol.

## Business rules

### Translation engine: Google Cloud Translation API (NOT Cloudio)

Multilang's AI translation calls **Google Cloud Translation API v3**, authenticated via a bundled service-account credential (project ID `cloudcart-144219`). **This is independent from [[apps-cloudio-overview]] / OpenAI** — Multilang does NOT use Cloudio's translator skill or GPT for catalog translation. The merchant's `cloudio_ai` token balance is separate from Multilang's translation quota (`multilang_product_translate` is its own plan-feature key). Multilang translates products, categories, blog articles, and pages independently with Google's engine.

### Plan-feature-driven sync gating

A sister-site sync is active when the merchant's plan has remaining quota for the relevant feature. Plan features track REMAINING quota — the plan grants a quota of translate-operations + copy-operations per period; when exhausted, the feature is gated until the quota refreshes and sync halts.

### Copy without translation puts source-language text on the sister site

When the merchant chooses "copy" instead of "translate" (or when their translation quota is exhausted), the platform copies the source-language text verbatim to the sister site (via the `multilang_product_copy` queue task). **The sister site displays the source language for that entity** — not a "translation pending" placeholder. The merchant can manually edit afterwards. There is no automatic "show source language on missing translation" runtime fallback at storefront render time — the actual sister-site record holds whatever was copied or translated.

### No built-in translation review queue

There is no `/api/multilang/review` or "pending approval" workflow. Translations sync directly into the sister site (status pending while the job runs, completed once it lands). The merchant CAN inspect translations after the fact via [[apps-multilang-products]] and edit per product, but there is no gate that holds translations in a review state before they go live.

### Retry policy: 3 attempts per translation record, then dropped

Each translation record (a product, category, etc.) has an `attempts` counter. The Translate job retries up to **3 times** if Google returns empty. After the third failed attempt, the record is left in pending state and stops being retried. The merchant can re-trigger via [[apps-multilang-products]] but the retry counter persists.

### Translation slugs auto-deduplicate

When the platform translates an entity's name and generates a fresh URL handle for the sister site, it checks whether that slug already exists on the target table; if so, the slug becomes `<translated-slug>-<id>` to avoid collisions. The sister site's slugs are independent from the master's but always unique within the sister. (Per-site slug semantics: see [[apps-multilang-main-model]].)

### Anti-redirect rewrite: master URLs in product description bodies get rewritten

When translating a product `description` or `short_description`, the Translate job rewrites any in-body URL that points to the master site to point to the equivalent sister-site URL. This prevents a translated EN page from linking back to the BG master mid-paragraph. The merchant cannot opt out — the rewrite is automatic.

### Internal cost accounting: Google's $20 per million characters

Every successful translation chunk creates an internal token-log entry recording: `cc_tokens` (symbol count translated), `cc_price` (what CloudCart charges the merchant for those symbols, per the `machine_translation` plan-feature pack), `original_tokens` (same symbol count), and `original_price` (what Google charges CloudCart at the hardcoded internal rate of **$20 per 1,000,000 characters**). This is internal accounting; the merchant does not see Google's wholesale cost — only their own plan-feature quota balance.

### Permission

Standard apps permission scope.

## Related

- [[apps-multilang]] — Multilang feature hub.
- [[apps-multilang-main-model]] — master/sister model + per-site slugs.
- [[apps-multilang-products]] — per-product translation status + re-trigger.
- [[apps-multilang-progress]] — sync progress tracker.
- [[apps-cloudio-overview]] — separate OpenAI-based AI app (NOT used by Multilang translation).
- [[apps-multilang-settings]] — master-level feature toggles.

## Open questions

None.
