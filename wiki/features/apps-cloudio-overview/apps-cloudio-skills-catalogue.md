---
type: feature
nav_path: "Apps → Cloudio → Skills"
route_name: apps.cloudio.overview
route_path: /admin/apps/cloudio
aliases: ["Cloudio skills", "Cloudio AI skills", "Cloudio skill catalogue", "shopper_pen", "rank_master", "vision_sense", "Cloudio умения"]
tags: [apps, ai, cloudio, content-generation, plan-gated]
plan_gates: ["cloudio_ai"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-cloudio-overview]]. See the hub for the other aspects (tokens/billing, execution model, upstream providers, translator).

# Cloudio — skills catalogue

## Purpose

Cloudio's intelligence is exposed as discrete **"skills"** — each a separate AI capability the merchant can enable, configure, and consume independently. This page catalogues the skills, what each does, its token-cost multiplier, and how skills are activated or hidden. The token model behind the multipliers lives on [[apps-cloudio-tokens-billing]]; which upstream service runs each skill is on [[apps-cloudio-upstream-providers]].

## Where to find it

Sidebar → Apps → **Cloudio** (`/admin/apps/cloudio`) → the **Skill list** on the settings page. Each skill row shows its status and a toggle; opening a skill shows its per-skill detail ([[apps-cloudio-details]]). Per-skill info is served by GET `/api/cloudio/skill/{type}`.

## What the merchant can do here

- See every available skill with its current Active / Inactive status.
- Toggle an individual skill on or off via POST `/api/cloudio/skills/status`.
- Open a skill to read its description, expected output, and cost per use.

### The skills

| Skill (`key`) | What it does | Icon | Free? | Multiplier per use |
|---|---|---|---|---|
| **shopper_pen** | Generate product description from the product's existing fields | `far fa-magic` | No | 1× |
| **shopper_pen_advanced** | Bulk / advanced description generation across many products | `far fa-magic` | No | 1× (min 3000 tokens per task) |
| **shopper_pen_category** | Generate category description | `far fa-magic` | No | 1× |
| **rank_master** | Generate keywords / additions / descriptions for ranking — DIFFERENT multipliers per sub-output: keywords=50, addition=100, description=400 | `far fa-chart-line` | No | Variable |
| **vision_sense** | Image analysis (detect content, classify, tag) | `far fa-image` | No | 1500× per image |
| **shopper_sense** | Customer behaviour analysis | `far fa-radar` | **Yes** (free) | — |
| **update_master** | Auto-suggest catalog updates | `far fa-comment-alt-smile` | **Yes** (free) | — |
| **translator** | Auto-translate content between languages | `far fa-language` | No | Per-character (see [[apps-cloudio-translator]]) |

**Commented-out (coming soon):** `landing_page_copy` — generate landing-page marketing copy.

## Settings & fields

### Skills metadata (per skill, in code)

Each skill carries:

- `key` — the skill identifier (used by the merchant-facing `apps.cloudio.api.skill.{type}.info` endpoint).
- `multiply` — token cost multiplier (different per skill; sub-keyed for `rank_master`).
- `min_tokens` — minimum balance required to enqueue.
- `isFree` — boolean (`shopper_sense` + `update_master` are free).
- `is_visible` — boolean (hides a skill from the merchant UI).
- `settings` — boolean (whether the skill has its own settings UI in Cloudio Settings).
- `log` — mapping to the per-skill log identifier.

### Skill visibility + activation

After install, the platform's `afterInstall` step auto-enables a default set of skills (`SKILL_DEFAULT` per skill key). The merchant then toggles individual skills via POST `/api/cloudio/skills/status`.

Activation is a **simple boolean on the app's settings** — there's no dedicated activation table. Toggling, e.g., `vision_sense = true` flips the setting; the Cloudio engine checks `skillIsActive($key)` (reads `getSetting($skill, false)`) before every run. Deactivating a skill flips the boolean to `false` but **leaves historical logs and token consumption intact**.

## Business rules

- **Free vs paid** — exactly two skills consume **no** tokens: `shopper_sense` (customer behaviour analysis) and `update_master` (auto-suggested catalog updates). They run without depleting the budget. Every other skill is paid.
- **Skill-specific multipliers** — `rank_master` has THREE sub-outputs with different multipliers: `keywords` = 50, `addition` = 100, `description` = 400. This reflects that generating a long description costs more compute than generating keyword lists.
- **`shopper_pen_advanced` minimum** — bulk description generation charges a minimum of 3000 tokens per task regardless of input size.
- **Active-skill gate** — an active-skill check gates all skill execution; an inactive skill cannot be run even with tokens available. See [[apps-cloudio-execution-model]].

### Side effects

- Toggling a skill writes a boolean to the Cloudio app settings only — no log, no token movement.
- Running a paid skill decrements the shared `cloudio_ai` token pool — see [[apps-cloudio-tokens-billing]].

### Permission

Standard apps permission scope.

## Related

- [[apps-cloudio-overview]] — hub.
- [[apps-cloudio-tokens-billing]] — what the multipliers cost.
- [[apps-cloudio-upstream-providers]] — which service runs each skill.
- [[apps-cloudio-translator]] — the Translator skill in depth.
- [[apps-cloudio-details]] — per-skill detail view.
- [[apps-cloudio-settings]] — per-skill settings UI.
- [[products-products]] — Shopper Pen exposed in the product editor.
- [[products-categories]] — category description skill.

## Open questions

- Translator multiplier shown as "per-character" — confirm the exact `multiply` value vs the per-character logic in [[apps-cloudio-translator]] (verify).
