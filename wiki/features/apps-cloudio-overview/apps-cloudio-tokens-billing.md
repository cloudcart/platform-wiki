---
type: feature
nav_path: "Apps → Cloudio → Tokens & billing"
route_name: apps.cloudio.overview
route_path: /admin/apps/cloudio
aliases: ["Cloudio tokens", "Cloudio billing", "cc_tokens", "original_tokens", "Cloudio token pricing", "Buy more tokens", "Cloudio токени"]
tags: [apps, ai, cloudio, billing, plan-gated]
plan_gates: ["cloudio_ai"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-cloudio-overview]]. See the hub for the other aspects (skills, execution model, upstream providers, translator).

# Cloudio — tokens & billing

## Purpose

Cloudio is **token-metered**: every paid AI run costs tokens, and the merchant buys tokens through their plan or ad-hoc packs. This page covers the two-token accounting model, how prices are derived from the `cloudio_ai` plan feature pack, the per-call accounting log, and the single shared quota pool.

## Where to find it

Sidebar → Apps → **Cloudio** (`/admin/apps/cloudio`) → the **Tokens dashboard** (current balance via GET `/api/cloudio/tokens`) and the **Buy more tokens** banner/modal when the balance is low.

## What the merchant can do here

- See the current token balance.
- Purchase additional token packs via the "Buy more tokens" modal when low.
- Read each run's token cost in [[apps-cloudio-history]].

## Settings & fields

### Token model — two counters per job

| Token field | What it stores |
|---|---|
| `cc_tokens` | CloudCart-billed tokens — the merchant's billing currency. Calculated from input × `singlePriceCC` × 100. |
| `original_tokens` | Upstream AI provider tokens (e.g., GPT) — calculated from input × `singlePriceGpt` × 100. |

Both are logged per job for audit / billing reconciliation. **The merchant pays in `cc_tokens`; CloudCart consumes `original_tokens`** on its upstream API.

### Per-call accounting log

Each AI call inserts a row in the application-tokens table:

- `record_id` + `record_type` — which app made the call (useful for cross-app spend reporting).
- `cc_tokens` + `cc_price` — merchant-side accounting.
- `original_tokens` + `original_price` — CloudCart-side accounting.
- `log_id` — references the per-skill log entry.

This is the source of the [[apps-cloudio-history]] tab's data.

## Business rules

### Token-metered execution

Tokens are paid upfront via plan tier OR ad-hoc purchase. When the merchant runs out:

- New skill requests immediately fail (the platform rejects with a tokens-unavailable error).
- In-flight jobs complete — their tokens were **reserved** when enqueued.
- The merchant sees a "Buy more tokens" banner in the Cloudio side panel.

### Plan-gating under `cloudio_ai`

Cloudio is gated by the `cloudio_ai` plan feature. Different plans get:

- Baseline tokens per month (regenerate monthly).
- Per-skill access (some skills locked to higher tiers).
- Concurrent job limits.

### Single shared quota — not per-skill

All skill executions check the SAME single `cloudio_ai` feature counter. Activating Vision Sense does NOT grant a separate Vision quota — everything pulls from one shared `cloudio_ai` token pool. Heavy use of one skill (e.g., bulk Shopper Pen Advanced) drains the same balance that Vision Sense or Rank Master would tap.

### Token pricing — derived from the plan feature pack

The `cc_tokens` price = feature-pack price ÷ feature-pack token count, where the feature pack is keyed by `cloudio_ai`. The merchant's per-token rate in their displayed currency depends on the pack they purchased (different packs have different prices and different included token counts).

**CloudCart can adjust the rate card by editing the feature pack without code changes** — the published rate the merchant sees in the "Buy more tokens" modal is the source of truth for what they're charged. This lets CloudCart sell tokens in customer-friendly packs (e.g., "10000 tokens for 5 BGN") while the actual upstream cost varies per token, with CloudCart absorbing the difference.

### GPT-side cost is hardcoded at 0.00002 per token

The `singlePriceGpt` rate CloudCart uses to track its upstream OpenAI spend is **hardcoded to 0.00002** in the manager — NOT pulled from any config or environment variable. All GPT-token accounting on the `original_price` side uses this single fixed rate. If OpenAI raises prices, this constant needs a code change.

### Token rollover and expiry — driven by Plan, not Cloudio

Cloudio's `cc_tokens` are consumed against the `cloudio_ai` plan feature; Cloudio itself doesn't store balances. When the plan period resets, the feature counter resets per the plan's renewal rules. Ad-hoc packs bought via "Buy more tokens" are separate purchases. The merchant should check their plan's feature-pack documentation to know whether unused tokens carry over month-to-month or expire at renewal. See [[plan]].

### Free skills don't deplete the budget

`shopper_sense` and `update_master` are free and run without consuming `cc_tokens`. See [[apps-cloudio-skills-catalogue]].

### Side effects

- Token balance decremented on **successful** job completion.
- Reserved tokens released back on cancel — see [[apps-cloudio-execution-model]].
- A per-call accounting row written (mapping = `cloudio`).

### Permission

Standard apps permission scope.

## Related

- [[apps-cloudio-overview]] — hub.
- [[apps-cloudio-skills-catalogue]] — multipliers that drive `cc_tokens` cost.
- [[apps-cloudio-execution-model]] — when tokens reserve vs deduct.
- [[apps-cloudio-history]] — per-call accounting rows surfaced to the merchant.
- [[plan]] — plan tiers + feature-pack renewal that gate token quota.

## Open questions

None.
