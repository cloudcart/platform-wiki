---
type: feature
nav_path: "Apps → Cloudio → Details"
route_name: apps.cloudio.details.tokens
route_path: /admin/apps/cloudio/:type/details/:logId
aliases: ["Cloudio Details", "Cloudio skill details", "AI skill info"]
tags: [apps, ai, cloudio, details]
plan_gates: ["cloudio_ai"]
created: 2026-05-22
updated: 2026-05-28
source_count: 2
---
# Cloudio → Details

## Purpose

The **Cloudio Details** view is a per-skill information page. When the merchant clicks a skill from the [[apps-cloudio-settings]] catalogue, this page opens with the skill's description, capabilities, expected output, and example usage. For the engine + skills overview, see [[apps-cloudio-overview]].

## Where to find it

Sidebar → Apps → Cloudio → click any skill in the catalogue → opens the Details view.

Route: GET `/api/cloudio/skill/{type}` fetches the skill's info data (e.g., `/api/cloudio/skill/shopper_pen`).

## What the merchant can do here

Per skill, the page shows:

- **Skill name + icon** — e.g., "Shopper Pen" with the `far fa-magic` icon.
- **Description** — what the skill does in plain language.
- **Cost** — token cost per typical use (based on the skill's `multiply` value + min_tokens floor).
- **Best for** — typical merchant use cases.
- **Expected output** — example of what the skill produces.
- **Activation toggle** — turn the skill on/off.
- **Try it** — quick test action (where applicable).

### What the merchant CANNOT do here
- Test the skill without spending tokens (the "Try it" action consumes tokens like any normal use).
- Modify skill internals / prompts (platform-managed).
- See or edit the prompt template used by the skill (internal, not exposed).

## Settings & fields

The fields on this page are READ-ONLY views of the skill's configuration. The toggle is the only writeable action. The actual skill configuration (active/inactive) is persisted via the same POST `/api/cloudio/skills/status` endpoint used by [[apps-cloudio-settings]].

## Business rules

### Per-skill cost preview

The Details page typically shows an estimated token cost for one invocation based on the skill's `multiply` value:
- `shopper_pen`: 1× (low cost per call).
- `vision_sense`: 1500× per image (expensive — image processing is compute-heavy).
- `rank_master`: 50/100/400 for keywords/addition/description respectively.

This helps the merchant decide whether to invoke the skill, especially for high-cost skills like Vision Sense.

### Permission

Standard apps permission scope.

## Related

- [[apps-cloudio-overview]] — engine overview + skill catalogue.
- [[apps-cloudio-settings]] — skill activation settings.
- [[apps-cloudio-history]] — past runs of skills.

## How it works (verified against backend)

### Skill details fetch is endpoint-driven

The details endpoint returns one of the skill catalogue entries with these merchant-visible fields:
- `key` (skill identifier).
- `icon` (Font Awesome icon class).
- `title` (translated label).
- `description` (long description).
- `description_short` (short description).
- `isActive` (current activation state).
- `isFree` (boolean — free skills don't consume tokens).
- `history` (the log identifier — drives where this skill's history is found).
- `settings` (whether the skill has its own settings UI).
- `comming_soon` (boolean — surfaces "coming soon" badge for unfinished skills).

**This answers the "example outputs" question — Details shows static description text from translations, NOT live sample outputs.** The merchant tests with their own data using "Try it."

### Prompts are NOT exposed to merchants

Prompt templates live inside the platform's code (e.g., the "You are a creative copywriter writing in {language} language..." template for the product-description generator). They are NOT exposed via any API or UI surface. **Merchants cannot view or edit the underlying prompts** — Cloudio's prompts are platform-managed.

### No dry-run / preview mode — every invocation consumes tokens

Every successful skill invocation creates an application-tokens log row and deducts the calculated `cc_tokens` amount. There is no dry-run flag, no sandbox endpoint that returns sample output without billing. The "Try it" action on the Details page goes through the same execution path as a normal run — **the merchant pays tokens to test a skill**. The only no-cost preview is the static description text on the Details page itself (which comes from translations, not live AI output).

### Cost preview shown per skill — not parameterized by input length

The Details page shows the skill's `multiply` value as a fixed number (e.g., 1500 for Vision Sense). For most skills the actual cost = `multiply × tokens_used` where tokens_used depends on the input length. So the headline cost is a per-call multiplier, NOT an absolute estimate of what one invocation will cost — the merchant cannot pre-compute "I will spend X tokens on this product." The actual cost is only known after the job completes and lands in the History tab.

### `min_tokens` is a HARD lower bound — Shopper Pen Advanced minimum is 3000

For the `shopper_pen_advanced` skill, the platform requires the merchant's `cc_tokens` balance to be **at least 3000** before they can enqueue a task. The Details page surfaces this as a min-tokens warning; if the merchant tries to start with less, the request is rejected. Other skills have `min_tokens = 1` — effectively no floor, just non-zero.

### Coming soon skills surface a `comming_soon` flag (note: typo in source = "comming")

For skills that are wired up but not production-ready (currently `landing_page_copy` is commented out entirely), the Details API exposes a `comming_soon` boolean — note the typo in the field name. The Details UI uses this to display a "Coming soon" badge and disable the activation toggle.

## Open questions

