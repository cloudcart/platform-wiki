---
type: feature
nav_path: "Apps → Cloudio → Settings"
route_name: apps.cloudio.settings
route_path: /admin/apps/cloudio/settings
aliases: ["Cloudio Settings", "Cloudio config", "AI settings"]
tags: [apps, ai, cloudio, settings]
plan_gates: ["cloudio_ai"]
created: 2026-05-22
updated: 2026-06-11
source_count: 3
---
# Cloudio → Settings

## Purpose

The **Cloudio Settings** page is where the merchant configures which AI skills are active for the store, monitors token balance, and adjusts per-skill defaults. For the engine overview + complete skill catalogue, see [[apps-cloudio-overview]].

## Where to find it

Sidebar → Apps → Cloudio → **Settings tab**.

The route is `/admin/apps/cloudio` with a wildcard sub-path; the settings tab is `/admin/apps/cloudio/settings`.

## What the merchant can do here

- **Toggle individual skills** active/inactive. Each skill has its own switch:
  - `shopper_pen` / `shopper_pen_advanced` / `shopper_pen_category` — content generators.
  - `rank_master` — keyword + description ranking helper.
  - `vision_sense` — image analysis.
  - `shopper_sense` (free) — behaviour analysis.
  - `update_master` (free) — catalog suggestions.
  - `translator` — language conversion.
- **See token balance** — current `cc_tokens` and what they convert to in usable AI calls.
- **Buy more tokens** — opens the token-purchase modal (banner appears when balance is low).
- **Per-skill settings** — some skills (`shopper_pen_advanced`, `translator`) have a `settings: true` flag, meaning they expose ADDITIONAL config (e.g., target language, output length, tone).

### What the merchant CANNOT do here
- Use a skill that's plan-locked (some skills require higher plan tiers).
- Save settings for skills that don't have `settings: true` — those run with platform defaults only.
- Manually set the upstream AI provider (model selection is platform-managed).

## Settings & fields

### Per-skill flags (from skill catalogue)

| Field | Notes |
|---|---|
| `isFree` | When true, no tokens are consumed (currently `shopper_sense` + `update_master`). |
| `log` | Internal log identifier — drives where the skill's history appears. |
| `multiply` | Token cost multiplier (numeric OR an object for skills with sub-outputs like `rank_master`). |
| `min_tokens` | Minimum token balance required to enqueue the skill. |
| `settings` | When true, the skill has its own dedicated settings UI in this page. |
| `is_visible` | When false, the skill is hidden from the merchant (still callable via API). |

### Skills with `settings: true`

These show extra config sections in this page:

- **`shopper_pen_advanced`** (`min_tokens: 3000`) — bulk-generation parameters. Its dedicated panel exposes:
  - **Product detail checkboxes** — pick which product fields feed the prompt: name (always on), short description, long description, category (always on), properties, variants, vendor, tags.
  - **Companion skills** — toggles to include `vision_sense`, `rank_master`, and `shopper_sense` in the advanced flow.
  - **Output languages** — multi-select from the platform's full locale list.
  - **Product filter** — search/select by selection / products / vendors / categories (same search as the bulk-edit flows).
  - **Token balance + buy link** — remaining `cloudio_ai` tokens with a deep link to the upgrade page.

  The panel does NOT expose tone, output-length cap, or target-audience persona — those are platform-managed (see [[apps-cloudio-details]] about hidden prompts).
- **`translator`** — target languages. The target must be one of the platform's standard locale codes (Bulgarian, English, Romanian, Greek, Hungarian, German, Spanish, French, Italian, Serbian, Macedonian, Albanian, Finnish, Polish, etc.). The merchant cannot add custom languages — the list is fixed to the platform's locale registry.

### Defaults at install

After install, exactly TWO skills are auto-enabled: `shopper_pen` (product description generator) and `update_master` (free catalog suggestions). The other six (`shopper_pen_advanced`, `shopper_pen_category`, `rank_master`, `vision_sense`, `shopper_sense`, `translator`) are OFF and must be toggled on individually. This default set is the same on every plan tier — it is not plan-dependent.

## Business rules

### Min-tokens gating

Some skills (like `shopper_pen_advanced` at 3000 min tokens) refuse to start unless the merchant's `cc_tokens` balance exceeds the minimum. This protects the merchant from starting a job that would fail partway through due to running out of tokens.

### The Settings tab is effectively a multi-switch

Each skill activation is a single boolean store-level setting (e.g., `vision_sense = true`). Apart from the dedicated `shopper_pen_advanced` and `translator` panels, there are NO additional per-skill fields here — tone, length, prompt flavour, and output-language defaults all live in the per-skill flow or use platform defaults.

### Skill activation persists across sessions

Toggling a skill changes the store-level setting; all admins inherit the same configuration. There's no per-admin skill state.

### Free skills don't deplete tokens

Activating `shopper_sense` / `update_master` is essentially free — they consume zero `cc_tokens` per call (still subject to rate-limiting / concurrent-job caps).

### Buy more tokens is a one-time purchase, not auto-renewing

The "Buy more tokens" CTA links to the [[plan]] page for `cloudio_ai`, where the merchant picks a feature pack. Each purchase is **one-time** — N tokens are added to the balance and consumed by skill invocations. There is no auto-top-up subscription; when the balance runs out the merchant must return to the upgrade page manually.

### Toggling a skill off does not cancel running jobs, and toggling back on does not retry failures

If the merchant toggles a skill off, jobs enqueued before the toggle keep running (they don't auto-cancel); new jobs are blocked. Toggling the skill back on does NOT auto-retry previously-failed jobs — only jobs waiting on tokens get rebuilt when tokens refill (see [[apps-cloudio-history]]). Toggle-driven failures must be restarted manually per entry.

### Auto-translate runs every 8 hours, not in real time

Configuring `auto_translate` with target languages (a non-empty setting) starts a recurring background task on an 8-hour interval. It scans for new/changed content in the source language and queues translations. So there is up to an 8-hour lag between editing a product description and the translation appearing — for immediate results the merchant invokes the Translator skill manually. Emptying the `auto_translate` setting stops the task on its next run.

### Permission

Standard apps permission scope.

## Related

- [[apps-cloudio-overview]] — engine overview + complete skill catalogue.
- [[apps-cloudio-details]] — per-skill detail page.
- [[apps-cloudio-history]] — job history.
- [[plan]] — plan tiers that gate skill access + token allocations.

## Open questions
