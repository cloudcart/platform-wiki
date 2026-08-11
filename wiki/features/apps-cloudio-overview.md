---
type: feature
nav_path: "Apps → Cloudio"
route_name: apps.cloudio.overview
route_path: /admin/apps/cloudio
aliases: ["Cloudio", "Cloudio AI", "CloudCart AI", "AI assistant", "AI helper", "Облачо", "no enable disable button", "app has no active toggle"]
tags: [apps, ai, cloudio, content-generation, plan-gated]
plan_gates: ["cloudio_ai"]
created: 2026-05-22
updated: 2026-08-06
source_count: 7
---
# Cloudio (CloudCart AI assistant)

## Purpose

**Cloudio** is CloudCart's **AI brand** — a token-metered AI assistant that powers content generation, image analysis, translation, ranking, and product-data enrichment across the platform. Cloudio's intelligence is exposed as **"skills"** (separate AI capabilities the merchant can enable, configure, and consume independently).

Cloudio is the underlying engine behind:
- AI rule generation in [[apps-cart-rules]] (natural language → rule structure).
- Content variation in [[apps-seo-spinner]].
- Auto-translation in [[apps-multilang]] (verify).
- Per-product AI features (descriptions, meta tags, images, related products).

The merchant pays in **tokens** — Cloudio consumes `cc_tokens` (CloudCart's billing currency) AND `original_tokens` (upstream AI provider tokens, e.g., GPT). Different skills cost different amounts. The full billing mechanics, free-vs-paid skills, and the way prices are derived from plan feature packs are covered in [[apps-cloudio-tokens-billing]].

This page is the **hub** for the Cloudio cluster. It gives the overview; each aspect of how Cloudio works lives on its own sub-page below.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> Individual Cloudio **skills** are activated / hidden separately — that is the real switch, see [[apps-cloudio-skills-catalogue]].

## Where to find it

Sidebar → Apps → install → **Cloudio**.

Top-level route: `/admin/apps/cloudio` → `apps.cloudio` (settings hub).
API routes under `/api/cloudio/*` (info / skills / tokens / per-skill operations).

Once installed, Cloudio's capabilities also surface contextually — e.g., the Cloudio side panel on the product editor ([[products-products]]) and the category description generator on [[products-categories]].

## Sub-pages (in this cluster)

This topic is split into 5 aspect pages. Drill into the one that matches the question rather than reading all of them.

- [[apps-cloudio-skills-catalogue]] — the 8 skills (`shopper_pen`, `rank_master`, `vision_sense`, `translator`, etc.), what each does, multipliers, free-vs-paid, and how skills are activated / hidden.
- [[apps-cloudio-tokens-billing]] — the `cc_tokens` vs `original_tokens` model, how prices are derived from the `cloudio_ai` plan feature pack, the per-call accounting log, and the shared single-pool quota.
- [[apps-cloudio-execution-model]] — the skill-run lifecycle (enqueue → run → deduct → rate), the 5-attempt retry policy, cancel behaviour, auto-retry of token-starved jobs, and how failures surface to the merchant.
- [[apps-cloudio-upstream-providers]] — which external services power each skill (OpenAI GPT-5 family, Astica AI, RankMath), the mini-vs-full model split, OpenAI lock-in, and timeout behaviour.
- [[apps-cloudio-translator]] — the Translator skill: supported languages (platform locales), per-character cost, and the opt-in 8-hour auto-translate background job.

## What the merchant can do here

On this Cloudio settings page (`/admin/apps/cloudio`):

- **Tokens dashboard** — see current token balance (GET `/api/cloudio/tokens`).
- **Skill list** — see all available skills with their status; toggle each on/off. See [[apps-cloudio-skills-catalogue]].
- **Per-skill info** — open a skill to see its description, expected output, cost per use (GET `/api/cloudio/skill/{type}`). See [[apps-cloudio-details]].
- **Buy more tokens** — when balance is low, purchase additional token packs. See [[apps-cloudio-tokens-billing]].
- **Job history** — see past AI runs across all skills. See [[apps-cloudio-history]].
- **Restart failed jobs** — POST `/api/cloudio/restart` for retry attempts. See [[apps-cloudio-execution-model]].
- **Cancel an in-flight job** — POST `/api/cloudio/cancel`.
- **Rate AI output** — GET `/api/cloudio/rating/{log_id}/{rating}` — feedback for improving skill quality.

### What the merchant CANNOT do here

- Use Cloudio AI features without remaining tokens — the platform rejects the request when the balance is exhausted (see [[apps-cloudio-tokens-billing]]).
- Bypass plan-gating — `cloudio_ai` is a plan feature (some plans get baseline tokens; higher plans get more / unlimited).
- Force a specific AI model (e.g., GPT-4 vs Claude) — model selection is platform-managed. See [[apps-cloudio-upstream-providers]].

## Settings & fields

The merchant-facing settings on this hub are minimal — it is mainly a dashboard + skill toggle list. The substantive configuration belongs to individual aspects:

- **Token balance** — read-only; sourced from the `cloudio_ai` plan feature counter. See [[apps-cloudio-tokens-billing]].
- **Per-skill Active / Inactive toggle** — a simple boolean per skill key (e.g., `vision_sense = true`); flipping it doesn't touch historical logs. See [[apps-cloudio-skills-catalogue]].
- **`auto_translate`** — the only multi-value setting; an array of target languages that drives the auto-translate job. See [[apps-cloudio-translator]].
- Detailed per-skill settings UI lives on [[apps-cloudio-settings]].

## Business rules

The Cloudio cluster's core business rules, each detailed on its aspect page:

- **Token-metered execution** — every paid AI call costs tokens; running out rejects new requests but lets in-flight (reserved) jobs complete. See [[apps-cloudio-tokens-billing]].
- **Plan-gating under `cloudio_ai`** — plans define baseline monthly tokens, per-skill access, and concurrent-job limits. See [[apps-cloudio-tokens-billing]] + [[plan]].
- **Free vs paid skills** — `shopper_sense` and `update_master` are free; all others consume tokens. See [[apps-cloudio-skills-catalogue]].
- **Skill-specific multipliers** — e.g., `rank_master` has three sub-output multipliers (keywords 50 / addition 100 / description 400). See [[apps-cloudio-skills-catalogue]].
- **Job ratings improve quality** — low ratings feed back into prompt tuning. See [[apps-cloudio-execution-model]].
- **Provider lock-in** — every skill runs on platform-chosen upstream services; the merchant cannot pick a model or provider. See [[apps-cloudio-upstream-providers]].

### Side effects

- Token balance decremented per successful job; reserved tokens released on cancel.
- A per-call accounting row is written (the source of the [[apps-cloudio-history]] tab). See [[apps-cloudio-tokens-billing]].
- Job result written to the relevant entity (product description updated, category description set, etc.).
- No webhooks fire automatically per Cloudio job (verify).

### Permission

Standard apps permission scope.

## Related

- [[apps]] — App Store hub.
- [[apps-cloudio-skills-catalogue]] — the AI skills catalogue (aspect).
- [[apps-cloudio-tokens-billing]] — token model + billing (aspect).
- [[apps-cloudio-execution-model]] — execution lifecycle + retry (aspect).
- [[apps-cloudio-upstream-providers]] — upstream AI services (aspect).
- [[apps-cloudio-translator]] — Translator skill (aspect).
- [[apps-cloudio-settings]] — settings sub-page (config detail).
- [[apps-cloudio-details]] — per-skill detail view.
- [[apps-cloudio-history]] — job history.
- [[apps-cart-rules]] — uses Cloudio for AI rule generation (`apps.cart-rules.ai`).
- [[apps-seo-spinner]] — content variation; likely Cloudio-powered.
- [[apps-multilang]] — auto-translation; may use Cloudio's translator skill.
- [[products-products]] — Cloudio side panel exposed per-product (description, meta, related products generation).
- [[products-categories]] — category description skill.
- [[settings-translations]] — UI label translations (separate concept from Cloudio's content translation).
- [[plan]] — plan tiers that gate Cloudio access.

## Open questions

None.
