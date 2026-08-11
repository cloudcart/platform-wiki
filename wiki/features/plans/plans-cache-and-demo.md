---
type: feature
nav_path: "Profile → Choose plan → (plan-feature cache + demo accounts)"
route_name: plans
route_path: /admin/plans
aliases: ["Plan feature cache", "Plan cache TTL", "Plan cache flush", "Demo plan", "cc-demo enterprise", "Plan-gate cache", "Кеш на план"]
tags: [plans, pricing, cache, plan-gates, demo]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans]]. See the hub for the other aspects (catalog display, country / partner filtering, LTA override, free-plan expiry, downgrade behavior).

# Plans — feature cache + demo accounts

## Purpose

This page documents two backend behaviours that surface as merchant-visible effects on the [[plans]] / [[plan-gates]] system: (1) the **plan-feature value cache** — a one-week TTL cache layered with active subscriptions, flushed on any plan / subscription change — that makes plan-gate checks fast across the admin panel; (2) **demo accounts** with the `cc-demo` plan slug, which are internally resolved against the **Enterprise tier** so demo / preview sites can evaluate every feature unlocked.

Both topics share the same "lookup pipeline" — they describe how the platform answers the question "does this merchant's plan allow feature X?" — so they're documented together.

## Where to find it

Neither has a dedicated screen — both run server-side and surface as effects across the admin panel:

- The cache is invisible to the merchant. They notice it only when a newly-purchased plan / pack is effective **immediately** with no stale-cache window.
- Demo accounts show **Demo** as the plan label in the profile dropdown but behave like Enterprise — every plan-gated feature is unlocked.

## What the merchant can do here

- Nothing directly. The cache + demo mapping are platform-managed.
- Purchase a paid plan or feature pack and see the new entitlement take effect on the next click — no waiting for cache expiry.
- Browse the demo site at full feature unlock (for `cc-demo` sites).

## Settings & fields

These are backend behaviours — no merchant-editable fields. The pipeline data points are:

| Signal | Source | Effect |
|--------|--------|--------|
| **Cached plan-feature value** | Per (feature, plan) pair, TTL **1 week** | Returned by gate-check lookups; layered with active subscriptions |
| **Plan cache tag** | All plan-feature cache entries are tagged `plan` | Flushed via the platform code on any change |
| **Active feature subscription** | Per-feature pack subscriptions from [[plan-features]] | Added on top of base plan value at lookup time |
| **`cc-demo` plan slug** | Site record's plan field | Internal feature lookup uses Enterprise restrictions; profile dropdown still shows *Demo* |

## Business rules

### Plan-feature value cache (1-week TTL)

When the admin panel checks "does this merchant's plan allow feature X?", the answer is cached for **one week** per (feature, plan) pair. The cache lives in the platform-wide cache store and is tagged with the `plan` tag.

The lookup flow is:

1. Check cache for `(plan_id, feature_key)`.
2. On hit, return the cached value.
3. On miss, compute from the plan catalog + active feature subscriptions, write to cache, return.

This is why plan-gate checks across the admin panel are fast — the gate runs on every product create, every page load that's plan-gated, etc., and a 1-week-cached lookup keeps it cheap.

### Active subscriptions layer on top of base plan value

If the merchant has bought a **feature pack** ([[plan-features]]) for additional quota above the plan's base limit, the pack's value is **added** to the base value at lookup time. Example:

- Base plan: 500 products.
- Active "products pack +500" subscription: +500 products.
- Effective limit: 1000 products.

The cache stores the **base plan value** only; the active-subscription delta is computed at lookup time (it depends on the merchant's current subscription state, not the plan record).

### Cache flushes on any plan / subscription change

When a merchant's plan changes — purchase, downgrade, cancellation — OR any subscription is created / updated / cancelled, the **entire `plan` cache tag is flushed** (the platform code). All cached feature values for that merchant become invalid and the next gate-check recomputes from the catalog + active subscriptions.

This is why a newly-purchased plan or pack is **effective immediately** — there's no stale-cache window the merchant has to wait through. The next click after checkout sees the new entitlement.

### Demo accounts (`cc-demo`) → Enterprise tier internally

Sites with the plan slug `cc-demo` are routed through **Enterprise-tier restrictions internally** — every plan-gated feature behaves as if the merchant were on Enterprise. The plan label in the profile dropdown still reads *Demo* (not *Enterprise*), but the gate-evaluation pipeline resolves Enterprise's values.

The catalog screen itself still shows the public plans; demo accounts can browse the same list. See [[plan-gates]] for the gating logic.

### Demo accounts can still purchase

A `cc-demo` site can still go through [[plans-purchase]] and convert to a paid plan. The conversion clears the demo-Enterprise mapping and uses the purchased plan's actual entitlements. Until the conversion, the demo site keeps full Enterprise unlock.

### Cache is per-site, not global

The plan-feature cache is **per-merchant-site**, not a global plan cache. Each site's cache entries are independent. Flushing one merchant's cache doesn't affect any other merchant.

This also means CloudCart-staff changes to the plan catalog (price tweaks, feature limit changes) don't immediately propagate to merchants — they propagate as each merchant's cache entries expire individually (after 1 week) or get flushed by a plan / subscription change on that site. (verify)

### LTA contracts use the same pipeline

LTA-contract merchants (see [[plans-contract-lta-override]]) still go through the standard plan-feature cache + gate pipeline. The contract maps to a backing plan record for gate evaluation, and that backing plan's feature values are cached the same way. The LTA contract only changes what `/admin/plans` *displays*, not how features are resolved underneath.

## Related

- [[plans]] — hub.
- [[plan-gates]] — the gate-enforcement model the cache feeds.
- [[plan-features]] — feature packs that layer on top of the base plan value.
- [[plan-features-subscription-lifecycle]] — pack lifecycle that triggers cache flushes.
- [[plans-purchase]] — purchase flow that triggers the cache flush on the new subscription.
- [[plans-downgrade-behavior]] — downgrade also triggers a cache flush so new gates take effect immediately.
- [[plans-contract-lta-override]] — LTA contracts use the same cache + gate pipeline.
- [[subscriptions]] — list of the merchant's active subscriptions (incl. feature packs).

## Open questions

(All resolved.)
