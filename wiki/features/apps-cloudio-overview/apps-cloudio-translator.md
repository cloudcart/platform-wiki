---
type: feature
nav_path: "Apps → Cloudio → Translator"
route_name: apps.cloudio.overview
route_path: /admin/apps/cloudio
aliases: ["Cloudio translator", "Cloudio auto-translate", "Cloudio translation skill", "translator skill", "auto_translate", "Cloudio превод"]
tags: [apps, ai, cloudio, translation, multilang, plan-gated]
plan_gates: ["cloudio_ai"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-cloudio-overview]]. See the hub for the other aspects (skills, tokens/billing, execution model, upstream providers).

# Cloudio — Translator skill

## Purpose

The **Translator** skill (`translator`) auto-translates store content between languages. This page covers which languages it supports, how its per-character cost works, and the opt-in 8-hour auto-translate background job. The Translator is closely related to the [[apps-multilang]] app, which may consume this skill.

## Where to find it

Sidebar → Apps → **Cloudio** (`/admin/apps/cloudio`) → the **Translator** skill in the skill list. Its configuration (the `auto_translate` target-language array) lives in [[apps-cloudio-settings]].

## What the merchant can do here

- Activate / deactivate the Translator skill.
- Configure `auto_translate` — the set of target languages new/changed content should be translated into.
- Translate content on demand through the skill's surfaces.

## Settings & fields

### `auto_translate`

A non-empty **array** setting on the Cloudio app listing the target languages. When populated, the platform queues a repeatable auto-translate background job. When emptied, that job is destroyed and auto-translation stops.

### Supported languages — platform locales, not a separate registry

The Translator uses the platform's **master locale list** to resolve the target language — the same locales the storefront and admin support (bg / en / ro / el / hu / de / es / fr / it / sr / mk / sq / fi / pl, etc.). **The Translator covers the same languages the storefront UI supports** — it does NOT maintain a separate language registry. See [[settings-translations]] for the UI-label translation system (a distinct concept from content translation).

## Business rules

### Cost: 1 token per CHARACTER

The Translator's token cost = **the number of characters in the source text** — not per word, and not per upstream GPT token. Example: a 1000-character product description translated into 5 languages = 5000 `cc_tokens`. The "characters" metric is easier for the merchant to reason about, but it means very long descriptions translated into many languages can rapidly consume the plan's monthly `cc_tokens` budget. See [[apps-cloudio-tokens-billing]].

### Auto-translate is opt-in per skill setting

When the merchant configures `auto_translate` with at least one target language, the platform queues an auto-translate job that periodically translates new/changed content. If `auto_translate` is empty, the job is destroyed (no background translation runs).

### Auto-translate runs every 8 hours

The auto-translate job is a repeatable job with `interval: 28800` (8 hours / 28800 seconds). Each run checks for new/changed content and triggers translation. So newly added content can take up to ~8 hours to appear translated.

### Quota exhaustion halts auto-translate

When the merchant's plan quota for the `cloudio_ai` feature is exhausted, auto-translate halts and the queue is destroyed until quota refills (plan renewal or a token-pack purchase). On-demand translations are likewise rejected once tokens run out — see [[apps-cloudio-execution-model]].

### Side effects

- Translated content written back to the relevant entity's per-language fields.
- `cc_tokens` deducted per successful translation (character-count based).
- The repeatable auto-translate job created/destroyed as `auto_translate` is set/cleared.

### Permission

Standard apps permission scope.

## Related

- [[apps-cloudio-overview]] — hub.
- [[apps-cloudio-tokens-billing]] — per-character cost against the shared token pool.
- [[apps-cloudio-execution-model]] — translate jobs run through the same lifecycle + quota gate.
- [[apps-cloudio-skills-catalogue]] — the Translator's place in the skill catalogue.
- [[apps-multilang]] — multi-language app that may drive Translator runs.
- [[settings-translations]] — UI-label translations (distinct from content translation).

## Open questions

None.
