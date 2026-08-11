---
type: feature
nav_path: "Settings → Api keys → Upgrade (feature packs)"
route_name: api_keys.settings
route_path: /admin/settings/api_keys
aliases: ["API requests feature pack", "Upgrade API rate limit", "api_requests pack", "Закупуване на пакет API заявки"]
tags: [settings, api-keys, plan-features, feature-pack, upsell]
plan_gates: ["api_requests"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Api keys — Feature packs (Upgrade flow)

> Part of [[settings-api-keys]]. See the hub for related aspects (overview, rate limits, modal, delete protection, security).

## Purpose

The **Upgrade** button in the API rate-limit banner above the keys table — what it does, which modal it opens, and how the `api_requests` plan-feature combines a per-plan base value with stackable feature packs to set the effective rate limit. Read [[settings-api-keys-rate-limits]] first for what the cap actually means; this page is about how the merchant raises it without changing plans.

## Where to find it

[[settings-api-keys-overview]] → API rate-limit info banner → **Upgrade** button. The button itself only renders when `meta.api_requests_feature_exists` is true on the page payload.

## What the merchant can do here

- Click **Upgrade** to open the appropriate upsell modal (in-product pack purchase OR generic plan-upgrade panel, depending on plan).
- Pick a pack step (for dynamic-pricing packs) and see live price recalculation.
- Confirm the purchase and have the new cap take effect immediately on the next API request.

## Settings & fields

The Upgrade button branches by `meta.api_requests_has_packs`:

| Branch | Modal opened | When |
|--------|-------------|------|
| **Has packs (`true`)** | `<PlanFeature>` modal targeted at `mapping: 'api_requests'` | When the merchant's plan permits buying `api_requests` packs (typically Starter Pack and above with `enable_feature_pack=ON`). |
| **No packs (`false`)** | Shared `planModal` (the generic CloudCart plan-upgrade panel from `useSharedPlanPanelState`) | When the merchant is on a plan that doesn't permit `api_requests` packs — they must change plans entirely (typical for Baby Pack). |

The `PlanFeature` modal is the standard pack-purchase flow documented in [[plan-features]] / [[plan-vs-feature-pack]].

## Business rules

### Two pack pricing models

Per [[plan-features]], `api_requests` packs can be configured as either:

- **Fixed-price packs** — single quantity at a single price (e.g. *+25 req/min @ X EUR / month*).
- **Dynamic-pricing packs** — a continuous ladder of step-quantities priced by a volume-discount formula. The merchant picks a step (e.g. 25 / 50 / 100 / 200 req/min) and sees the recalculated price live before confirming.

### Effective rate limit = plan base + sum of active feature-pack values

Packs **stack** on top of the per-plan base from [[settings-api-keys-rate-limits]]:

- Effective cap = `<plan base req/min>` + Σ active pack values.
- Packs survive plan upgrades / downgrades — the merchant keeps the extended quota for the pack's remaining billing period (see [[plan-vs-feature-pack]] for the survives-plan-change rule).

### `enable_feature_pack` gating

The per-plan-restriction `enable_feature_pack` flag controls whether the merchant's current plan even permits buying `api_requests` packs:

- **OFF** — the upsell modal shows a banner pointing the merchant to a plan that does permit it (typically the higher tiers).
- **ON** — the merchant can buy packs without changing their plan.

The flag is part of the standard three plan-restriction shapes (unrestricted / boolean on-off / numeric cap) — see [[plan-gates]].

### Newly-purchased pack takes effect immediately

The edge layer respects the new cap on the next request — the 1-week plan-feature cache is flushed on subscription change (see [[plan-vs-feature-pack]]). The merchant does not need to wait for a daily cron to roll over.

### Applies to ~200 numeric plan-features

This same mechanism applies to ALL numeric plan-features (products, customers, storage, newsletter messages, etc.) — `api_requests` is just one of them. The full taxonomy is in [[plan-gates]].

### When the in-product flow is not enough

For caps higher than what packs allow, the merchant must contact CloudCart support for a per-domain raise — see [[settings-api-keys-rate-limits]]. Custom raises bypass the plan-feature system and are set at the edge layer directly.

## Related

- [[settings-api-keys]] — hub.
- [[settings-api-keys-rate-limits]] — the cap this flow raises.
- [[settings-api-keys-overview]] — where the Upgrade button lives.
- [[plan-features]] — the per-pack purchase screen.
- [[plan-vs-feature-pack]] — stacking + survives-plan-change rules.
- [[plan-gates]] — three restriction shapes + the `enable_feature_pack` flag.

## Open questions

- Confirm exact `api_requests` pack ladder values currently configured (verify against latest plan config).
