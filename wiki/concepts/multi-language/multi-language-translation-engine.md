---
type: concept
nav_path: "Concept → Multi-language → Translation engine"
aliases: ["Translation engine", "Google Cloud Translation API", "multilang_product_translate", "multilang_product_copy", "Translation quota", "Multilang translation plan-gate", "Translate vs copy"]
tags: [i18n, multi-language, multilang, translation, plan-gates, concepts]
plan_gates: [multilang_product_translate, multilang_product_copy]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[multi-language]]. See the hub for the other aspects (three layers, customer/order locale, Multilang app, sister-site model, sync/fallback, SEO + switcher).

# Multi-language — translation engine

## Definition

The Multilang app uses **Google Cloud Translation API v3** as its sole machine-translation backend, authenticated via a bundled service-account credential at the platform level. Content sync from master to sister runs through two distinct queue tasks:

- **`multilang_product_translate`** — runs the entity's translatable fields through Google's API, writes the translated text to the sister site's record.
- **`multilang_product_copy`** — copies the entity verbatim from master to sister WITHOUT translation (used when the merchant wants source-language text on the sister site — e.g., product codes / SKUs / brand names that shouldn't be translated).

Both tasks are plan-gated through their own quota counters. Exhausting either quota stops new tasks of that type until the period refreshes or the merchant upgrades.

## Scope

Covered:

- Translation engine = Google Cloud Translation API v3 (not Cloudio / OpenAI).
- The two queue tasks: `multilang_product_translate` vs `multilang_product_copy`.
- Plan-feature quotas: `multilang_product_translate`, `multilang_product_copy` — how exhaustion behaves.
- What gets auto-translated alongside content (SEO meta, slugs).
- Lack of a translation review workflow — translations land live immediately.

Not covered here:

- The Multilang app itself, sister-site provisioning, cross-site SSO — see [[multi-language-multilang-app]].
- One-way sync semantics and re-translation overwrite — see [[multi-language-sync-fallback]].
- The CloudCart-internal cost margin over Google's $20/M-character wholesale rate — not merchant-facing.
- Cloudio AI translator (separate system, separate plan-gate, separate token balance) — see [[apps-cloudio-overview]].

## Contrasts

- **`multilang_product_translate` vs `multilang_product_copy`** — translate runs Google's API; copy bypasses translation entirely. Quotas are independent — exhausting one does not affect the other.
- **Multilang's translation quota vs Cloudio's `cloudio_ai` token balance** — completely separate. The merchant's Cloudio tokens do NOT subsidise Multilang. Multilang has its own plan-feature `multilang_product_translate` with its own quota counter; Cloudio's OpenAI tokens are billed against `cloudio_ai`.
- **Auto-translate vs manual edit on the sister** — auto-translate writes a fresh translation; manual edit on the sister site is a polish step that **does not** consume the translate quota but **does** get overwritten by a subsequent auto-translate. See [[multi-language-sync-fallback]].
- **Translation engine vs translation review workflow** — there is no "pending approval" queue. Translations land directly on the sister site. The merchant can inspect / edit after the fact via [[apps-multilang-products]] but there is no gate that holds them.

## Where it applies

### What gets translated

Per entity, Multilang's translate task runs Google's API on every translatable field. Typical coverage:

- Product: name, description, short description, SEO title, SEO description, SEO keywords.
- Category: name, description, SEO title, SEO description.
- Blog article: title, body, excerpt, SEO title, SEO description.
- Custom field: per-field translatable content where the custom-field definition flagged it as translatable.
- CMS page: page title, body.

SEO meta is translated **alongside** content — the merchant doesn't have to separately translate meta tags. URL slugs are also auto-generated per language using Google's transliteration / translation; the merchant can override the resulting slug per sister via the per-sister product editor (see [[multi-language-sync-fallback]] for the per-site slug rule).

### How a translate task runs

The merchant triggers translation in one of three places:

- **Per product** — [[apps-multilang-products]] → per-product "Translate" / "Copy" buttons.
- **Bulk** — [[apps-multilang-products]] → multi-select → "Translate selected" / "Copy selected".
- **On master save (auto-sync)** — if the sister is configured to auto-sync new entities, master-side creates / updates queue a translate task automatically.

The task lands on the sync queue; progress is visible in [[apps-multilang-progress]]. For a catalog of a few hundred products this typically completes in tens of minutes — the wall-clock time depends on catalog size, current queue depth, and the merchant's remaining quota.

The translation is **automatic** — there is no merchant-facing tuning of the translation model, no glossary upload, no per-term preferred translation. Google's general-purpose translation model is what runs.

### Plan-feature quotas

Both queue tasks are gated by their own plan-feature quotas:

- **`multilang_product_translate`** — counter of translated entity-fields the merchant has consumed in the current quota period. When exhausted, new translate tasks are blocked until the period refreshes (typically monthly — verify per plan) or the plan upgrades.
- **`multilang_product_copy`** — counter of copy operations. Same exhaustion behaviour.

Exhausted quota does **not** roll back already-translated content; it only blocks new tasks. The merchant sees their remaining quota on [[apps-multilang-products]] and [[apps-multilang-progress]] and on [[plan-gates]].

### Translate vs copy — when to use which

- **Translate** — default for descriptive content: product names that are common nouns, descriptions, category labels, SEO copy.
- **Copy** — preferred for content that shouldn't be translated: brand names ("iPhone 15 Pro Max"), SKUs, model codes, technical part numbers, content the merchant wants verbatim across languages (e.g., a legal disclaimer that must stay in the source language for compliance reasons).

The merchant can pick translate or copy on a **per-entity** basis — there's no global "always copy this field" rule.

### No translation review workflow

Translations created by the Multilang app's translation engine land **directly** on the sister site — there's no "pending approval" queue where the merchant can review before they go live. The merchant inspects translations after the fact via [[apps-multilang-products]] and can edit them, but there's no gate that holds them.

Practical implication: for a launch where translation quality matters, the merchant should treat translate as "draft generation" and follow up with a manual polish pass on the sister before promoting the sister's URL publicly. Be aware of the overwrite rule when re-translating — see [[multi-language-sync-fallback]].

## Related

- [[multi-language]] — hub.
- [[multi-language-multilang-app]] — Multilang app overview, master/sister mechanics.
- [[multi-language-sync-fallback]] — one-way sync + re-translation OVERWRITES sister-side manual polish.
- [[apps-multilang-products]] — where translate / copy is triggered + per-entity quota visibility.
- [[apps-multilang-progress]] — sync queue progress tracker.
- [[plan-gates]] — `multilang_product_translate`, `multilang_product_copy` quota definitions.
- [[apps-cloudio-overview]] — Cloudio AI (separate from Multilang; Multilang uses Google, not Cloudio).

## Open Questions

- (verify) exact quota refresh cadence per plan tier (monthly vs per-billing-cycle).
- (verify) whether a partial-batch translate (e.g., merchant runs translate on 200 products but quota only covers 150) processes the first 150 and stops, or rejects the whole batch upfront.
