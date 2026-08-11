---
type: feature
nav_path: "Plan → Feature pack → Restrictions & limits"
route_name: admin.plan.feature
route_path: /admin/plan/feature/{mapping}
aliases: ["enable_feature_pack flag", "plan.restrict.feature_purchase", "max_value cap", "Feature pack restriction", "Dynamic pricing formula", "Volume discount"]
tags: [plans, plan-feature, feature-pack, restrictions, max-value, dynamic-pricing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-features]]. See the hub for the other aspects (warning banners, pack list, purchase flow, subscription lifecycle, modern Vue grid, middleware mappings).

# Plan features — restrictions & limits

## Purpose

Three independent restrictions decide whether the merchant can actually buy a pack: the **`enable_feature_pack`** flag (per plan × feature), the **`plan.restrict.feature_purchase`** config (per feature → plan tier), and the **`max_value`** ceiling (per feature). The dynamic-pricing **volume-discount formula** decides the price ladder for features that allow custom quantities. This page documents all four — they together govern what the pack list shows and what the purchase action accepts.

## Where to find it

- Enforced on every visit to `/admin/plan/feature/{mapping}` (see [[plan-features-pack-list]] for the screen).
- Enforced on every *Buy* click (see [[plan-features-purchase-flow]] for the redirect path).

## What the merchant can do here

Nothing directly — these are server-side rules the merchant only experiences as outcomes:

- An empty pack list (when `enable_feature_pack` is OFF).
- A restriction banner instead of packs (when the feature is plan-restricted).
- An inline error after clicking *Buy* (when `max_value` would be exceeded).
- A specific ladder of quantity steps (when dynamic pricing is in effect).

## Settings & fields

| Restriction | Where it lives | Effect when ON |
|-------------|---------------|----------------|
| `enable_feature_pack` | Per plan × per feature restriction record | If OFF, the pack list is **empty** — even though packs exist in the catalog, they don't surface. Merchant must upgrade their plan. |
| `plan.restrict.feature_purchase.{mapping}` | Config table | Gates entire features to specific plan tiers (e.g. `custom_hostname` restricted to *Pro* / *Unicorn*). A lower-plan merchant sees the restriction banner — see [[plan-features-warning-banners]] |
| `max_value` | Per feature | Absolute maximum allowed quota even after packs (e.g. *100000 products*). Enforced on the *Buy* click; *Buy* is rejected when `current + pack > max_value` |
| `dynamic_pricing` | Per feature | Decides whether the ladder is a fixed set of packs (=0) or a server-generated volume-discount ladder (=1). The pack list filters by matching flag — see [[plan-features-pack-list]] |

### Max-value error message (verbatim)

When the *Buy* click would exceed `max_value`:

> *"Your package allows **<max_value>** <postfix>"*

The merchant stays on the feature screen — the redirect to checkout never happens. Uses the localised `plan.plan_limit` string.

## Business rules

### Feature-pack purchase can be disabled per-plan via `enable_feature_pack`

Each plan has an `enable_feature_pack` flag per restriction it carries. If the flag is OFF for the merchant's current plan × this feature, the pack list is **empty** — even if packs exist in the catalog, they don't surface. The merchant must upgrade to a plan where the flag is ON. This is how CloudCart says "you can't extend products on the Free plan — upgrade to Starter to unlock pack purchases".

### Feature restricted by plan tier via `plan.restrict.feature_purchase`

A **separate** restriction (`plan.restrict.feature_purchase` in config) gates entire features by plan: e.g. `custom_hostname` is restricted to *Pro* and *Unicorn* plans. A merchant on a lower plan visiting `/admin/plan/feature/custom_hostname` doesn't see packs — they see the restriction banner with the list of qualifying plans + a button to upgrade. The "Plans that support this functionality" list is pulled from this config entry, filtered to active + with details (so soft-deleted or country-restricted plans don't show). See [[plan-features-warning-banners]] for the banner UI.

### Max-value cap is enforced live (before cart re-seed)

Before placing a pack in the cart, the platform reads:

1. The plan's base value for the feature.
2. The merchant's already-purchased active subscriptions for the same feature.
3. The pack's `value` (or the dynamic `{value}` URL param).

If `(1) + (2) + (3) > max_value`, the *Buy* click is **rejected**. The merchant stays on the feature screen with an inline error toast using the `plan.plan_limit` localised string. See [[plan-features-purchase-flow]] for the redirect path that's blocked.

### Dynamic-pricing formula — non-linear volume discount

For dynamic-pricing packs, the algorithm starts at the pack's base (`value`, `price`), then for each multiple of the base value computes a discounted per-step price using:

> `floor((price/value × current) × (0.9 − 1.5 × current/value / 100))`

with a rounding step of **0.50**. The ladder continues until either the per-unit price stops decreasing (flat curve) or the feature's `max_value` is reached. The merchant sees discrete steps (e.g. *500*, *1000*, *2000*, ...) — NOT a free-form slider.

### the platform code substitutes demo with enterprise (verify)

When the platform resolves the merchant's effective plan for feature lookups, demo sites are treated as Enterprise:

- If `site('plan') == 'cc-demo'`, the resolver returns `config('plan.demo_restrictions_map')` = `'enterprise'`.
- Otherwise it returns the site's actual plan mapping.

So all feature-value lookups for demo sites resolve against the Enterprise plan's limits. The plan badge in the profile still says *Demo*, but every plan gate behaves as if the merchant were on Enterprise. This is purely for evaluation / preview sites.

### the platform code caches `null` as `'@@@'` sentinel (verify)

Internal detail: the cached form of "feature is not restricted at all" returns `null`, but the application framework's cache `remember` would treat null as "miss" and re-query forever. To avoid that, the platform caches the string `'@@@'` to represent null. On read, `'@@@'` is converted back to `null`. The merchant never sees the sentinel — it's an internal cache marker ensuring unrestricted features stay cached for the full 1-week TTL. See [[plan-features-subscription-lifecycle]] for the cache lifecycle.

### Bank-transfer unpaid invoices grace period varies by reseller (verify)

For sites that pay via bank transfer (not card), an unpaid bank-transfer invoice has a grace period before causing problems:

- **Standard merchants**: 30 days of unpaid bank-transfer invoices before the platform considers them as a problem.
- **Reseller-onboarded merchants** (when `reseller_id` is set): 90 days of grace.

The check is the platform code — it scans for bank invoices in UNPAID status older than the threshold. The merchant doesn't see the threshold directly; its effect can surface as a warning banner or as an access restriction depending on how long the bank invoice has been unpaid.

## Related

- [[plan-features]] — hub.
- [[plan-features-warning-banners]] — the restriction banner this `plan.restrict.feature_purchase` config drives.
- [[plan-features-pack-list]] — the `dynamic_pricing` flag filters this list.
- [[plan-features-purchase-flow]] — the `max_value` check that blocks the *Buy* redirect.
- [[plan-features-subscription-lifecycle]] — the 1-week feature-value cache.
- [[plan-gates]] — the gating concept that funnels merchants to these checks.
- [[plans]] — upgrade target for plan-restricted features.

## Open questions

None.
