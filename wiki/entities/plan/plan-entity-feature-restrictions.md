---
type: entity
nav_path: "Entity → Plan → Feature restrictions"
aliases: ["Plan feature restrictions", "Plan feature values", "Plan restriction shapes", "Plan-feature pivot", "Plan-feature cache", "enable_feature_pack"]
tags: [entity, billing, plans, features, gating]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[plan]]. See the hub for the other aspects (catalog structure, billing cycles, lifecycle, free-plan expiry + demo, LTA + partner overrides).

# Plan — Feature restrictions

## Identity

The **feature-restriction layer** of a [[plan|Plan]] — the pivot from Plan to [[plan-feature|Plan Feature]] where every plan stores exactly ONE value per feature (unrestricted / boolean / numeric). This is the actual data the [[plan-gates|gate engine]] reads at every "can the merchant do X?" check across the admin panel.

This page documents the three restriction shapes, the plan-feature naming conventions, the per-(plan, feature) `enable_feature_pack` flag, and the 1-week value cache.

## Aliases

- **Plan-feature value** — the restriction stored per (plan, feature) pair.
- **Plan-feature pivot** — the relation that holds the restriction.
- **Feature cap** — informal merchant phrasing for a numeric restriction (e.g., *"my product cap is 500"*).
- **Feature paywall** — informal phrasing for a boolean lock (e.g., *"Code PRO discounts are locked on Starter"*).
- **`enable_feature_pack`** — the per-(plan, feature) flag that decides if a feature pack can top up this Plan's value.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Plan features pivot** | The restriction values | For every feature in the catalog (~200 features), this Plan stores ONE value: unrestricted (null), boolean on/off, or a numeric cap. The platform's plan-feature lookup helpers read this at gate-check time. |
| **`enable_feature_pack`** | yes / no per feature | Per-plan-feature flag — does this Plan allow buying a feature pack for this feature on top? Some features explicitly disallow pack add-ons even on plans that have them as numeric caps. |
| **Hidden features** | Per-plan + per-feature exclusion list | Specific (feature × plan) combinations can be hidden from the comparison matrix on [[plans]] when a feature simply doesn't apply to a given plan. See [[plan-entity-catalog-structure]] for the matrix-side handling. |

## Business rules

### Three restriction shapes per feature

For any plan-feature mapping, the Plan stores ONE of three values:

- **Unrestricted** (no row / null) — feature open with no cap. Example: `email_unlimited` on Enterprise.
- **Boolean** (true = locked / false = unlocked) — flat on/off paywall. Example: `discount-code-pro: true` on Starter (locked); `false` on Pro (unlocked).
- **Numeric** (integer) — quota the platform compares used-vs-cap. Example: `products: 500` on Starter; `products: 5000` on Pro; `products: -1` (unlimited) on Enterprise.

The shape is determined by the feature itself (each feature is one-shape — boolean features can never be numeric and vice versa) — see [[plan-feature]] for the feature catalog.

### Plan-feature naming conventions

Plan-feature mappings follow consistent prefixes:

- **Entity counters**: bare noun — `products`, `customers`, `vendors`, `categories`, `administrators`.
- **App-specific**: app-key prefix — `mailchimp`, `cloudio_ai`, `viber_messages`, `xml_sync_limit`, `multi-warehouse`.
- **Per-discount-type**: `discount_*` — `discount_global`, `discount_coupon`, `discount_fixed`, `discount_quantity`.
- **Boolean toggles**: descriptive — `ssl_certificate`, `storefront_builder`, `subscriber_forms`, `abandoned_notification`, `authorize_payment`, `support_meetings`.
- **Reports**: `*_report` — `sale_report`, `product_report`, `payment_report`, `customer_report`.

### Plan-feature values are cached for 1 week

Every gate check (does this plan allow feature X?) is cached for 1 week per `<feature, plan>` pair. Active feature-pack subscriptions are layered on top — if the merchant bought a `+100 products` pack, that pack's value adds to the Plan's base value at lookup time. The cache is tagged `plan` and flushes automatically on plan / subscription changes.

This means: a CloudCart-staff edit to a plan-feature value typically takes effect for the merchant within a few seconds on plan-mutation flushes, but a feature-value adjustment made WITHOUT a plan-side change can take up to a week to propagate. CloudCart staff trigger a manual cache flush when the plan-feature mutation is silent (no merchant-side write to invalidate the cache).

### `enable_feature_pack` is per-(plan, feature)

The `enable_feature_pack` flag is stored as a pivot value on the plan-restrictions row. It is per-(plan, feature) combo, not a feature-level absolute — each Plan's restrictions row explicitly opts each feature in or out of pack-add-on. For a specific feature's pack-eligibility, the merchant should check the [[plan-features]] purchase flow — only pack-eligible features expose a purchase option.

Concretely: a feature can be `products: 500` on Starter with `enable_feature_pack = yes` (the merchant can buy a +500 products pack) while the same feature is `products: 5000` on Pro with `enable_feature_pack = no` (the merchant must upgrade further to break the cap, not buy a pack). See [[plan-vs-feature-pack]] for when each makes sense.

### Feature packs layer on top, they don't replace

A merchant on Pro with `products: 5000` who buys a `+1000 products` pack has an effective cap of **6000** — the values add. The Plan's base value is not mutated; the pack subscription contributes additively at lookup time. When the pack expires, the cap reverts to the Plan's base value.

### Unrestricted vs boolean-false vs numeric-`-1`

Three different ways a feature can effectively be "unlimited":

- **Unrestricted** (null / missing row) — gate engine treats as fully open.
- **Boolean `false`** — explicitly unlocked (the feature is paywalled by default; this plan unlocks it).
- **Numeric `-1`** — explicit unlimited value (most often used for Enterprise on numeric quotas like `products: -1`).

The three resolve identically at the gate (all = "yes, allowed") but encode different intents in the catalog. `-1` is the canonical Enterprise marker for numeric features.

## Where it appears

- [[plans]] — the per-plan comparison matrix renders these restriction values as checkmarks, caps, or feature names. Hidden combinations are absent.
- [[plan-details]] — read-only per-plan breakdown shows the same data on a single-plan page.
- [[plan-features]] — pack purchase flow shows ONLY features where the merchant's current Plan has `enable_feature_pack = yes` for that feature.
- Plan-gate banners across the admin panel — *"Upgrade to Pro to unlock X"*, *"You've reached your 500-product limit"* — resolve against the active Plan's restriction values.

## Related

- [[plan]] — hub.
- [[plan-feature]] — the per-feature catalog (one row per feature definition).
- [[plan-gates]] — the gating engine that consumes these restriction values.
- [[plan-vs-feature-pack]] — when to upgrade the Plan vs. buy a pack instead.
- [[plan-features]] — pack purchase flow gated by `enable_feature_pack`.
- [[plan-details]] — per-plan feature breakdown.

## Open Questions

None.
