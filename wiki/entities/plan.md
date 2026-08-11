---
type: entity
nav_path: "Entity → Plan (Subscription Tier)"
aliases: ["Plan", "Subscription tier", "Subscription plan", "Pricing tier", "Tariff plan", "CloudCart plan", "Store plan", "Plan tier", "План", "Тариф", "Тарифен план", "Абонаментен план"]
tags: [entity, billing, plans, pricing, subscription, gating]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---

# Plan (Subscription Tier)

## Identity

A **Plan** is a published subscription tier in the CloudCart catalog — Free / Start Up, Starter, Basic, Pro, Business, Enterprise, plus partner-network tiers (e.g., UniCredit) and demo / LTA-contract entries. Each Plan defines what the merchant's store is allowed to do: how many products / customers / segments / staff accounts they can create, what storage they get, which boolean features (SSL, storefront builder, Cloudio AI, Code PRO discounts) are unlocked, and at what price (per billing cycle: monthly / yearly / 2-year). The merchant has exactly ONE active Plan attached to their store at any time; the Plan is what every plan-gate check in the admin panel resolves against (see [[plan-gates]]).

A Plan is **catalog-defined by CloudCart staff** — merchants do NOT create, edit, or price plans; they only pick one from the published catalog on [[plans]] and purchase it via [[plans-purchase]]. The catalog is country / issuer-company aware: a Bulgarian merchant sees BG plans + global plans; a German merchant sees DE plans + global plans; partner-network merchants see only their partner catalog. Demo accounts (slug `cc-demo`) are routed internally as Enterprise for evaluation. Long-term-agreement (LTA) merchants have their plan replaced by the contract's negotiated terms.

A Plan is distinct from a **[[plan-feature]]** (the unit-level definition of WHAT each feature is — `products`, `discount-code-pro`, `ssl_certificate`, `xml_sync_limit`), from a **feature-pack subscription** (an add-on quota on top of the base plan — see [[plans-purchase]] / [[plan-features]]), and from the merchant's actual **subscription record** (the lifecycle entry that says *"the merchant currently owns this plan; it renews on this date"* — see [[subscription-lifecycle]]).

## Aliases

- **Plan** — the canonical term in admin UI and across the wiki.
- **Subscription tier** / **Pricing tier** — used in marketing copy and the catalog comparison matrix.
- **Tariff plan** — used in the Bulgarian admin labels.
- **Store plan** — used when distinguishing the CloudCart plan from the merchant's own customer-subscription products ([[orders-subscriptions]]).
- **CloudCart plan** — used in billing / invoicing contexts.
- **План** / **Тариф** / **Тарифен план** / **Абонаментен план** — Bulgarian equivalents.

## Sub-pages (in this cluster)

This entity is split into **6 aspect pages**, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[plan-entity-catalog-structure]] — slug / name / type / issuer-company; country + partner filtering; sort order (cheapest first); hidden-features matrix; per-language label overrides; the DE *Start Up → 14-Tage-Test (Starter)* re-label.
- [[plan-entity-billing-cycles]] — per-cycle price-detail variants (monthly / yearly / 2-year); per-variant active flag; currency bound to issuer company; soft-disable by deactivating all variants; no admin-side currency switcher.
- [[plan-entity-feature-restrictions]] — the three restriction shapes (unrestricted / boolean / numeric); plan-feature naming conventions; UI feature groupings; per-(plan, feature) `enable_feature_pack` flag; 1-week plan-feature value cache.
- [[plan-entity-lifecycle]] — catalog lifecycle (active → soft-disabled → hidden); merchant lifecycle (purchase → renew → cancel → expire → downgrade); existing data preserved on downgrade; one-active-plan-at-a-time rule.
- [[plan-entity-free-expiry-and-demo]] — free *Start Up* auto-expiry per issuer country (BG 30 days, DE 14 days); graduated warnings at thirds; sandbox-mode interaction; `cc-demo` slug → Enterprise gate resolution; legacy `trial` slug.
- [[plan-entity-overrides-lta-and-partner]] — LTA-contract override (gates fall back at `ends_at` with no grace); partner-network catalog (`unicredit` and similar reseller filters); profile-dropdown *Choose plan* link owner-gating.

## Key Attributes

The Plan is a multi-faceted record. The full per-field schema (slug, name, type, issuer, billing cycles, plan-features pivot, hidden-features, feature-pack flag, auto-expiry, sort order, per-language overrides) is documented across the aspect pages. The summary:

- **Catalog identity** (mapping/slug, name, type, issuer company, active-in-catalog flag, sort order, per-language overrides) — see [[plan-entity-catalog-structure]].
- **Pricing** (per-cycle price-detail variants, currency) — see [[plan-entity-billing-cycles]].
- **Feature restrictions** (plan-features pivot with unrestricted / boolean / numeric values; per-feature `enable_feature_pack` flag; UI groupings; hidden combinations) — see [[plan-entity-feature-restrictions]].
- **Auto-expiry thresholds** (per-issuer inactivity / sandbox windows for the free plan) — see [[plan-entity-free-expiry-and-demo]].

## Why it matters to the merchant

The Plan is the **single most-referenced gate** across the wiki: every numeric cap, every paywall, every "upgrade required" banner resolves against the merchant's current Plan. Five high-impact behaviours:

- **Exactly one active Plan at a time.** Switching plans replaces the old subscription with a new one (typically pro-rated at the purchase moment). See [[plan-entity-lifecycle]].
- **The catalog is country / partner-network filtered.** A merchant in DE cannot see BG-only plans; a UniCredit partner merchant cannot see the default catalog at all. See [[plan-entity-catalog-structure]] + [[plan-entity-overrides-lta-and-partner]].
- **Downgrades preserve existing data.** Over-quota products / customers / staff are kept; only new additions are gated by the lower cap. To recover headroom, prune data or buy a feature pack on [[plan-features]]. See [[plan-entity-lifecycle]].
- **Free plan auto-expires on inactivity.** BG 30 days, DE 14 days — for both "no admin login" and "sandbox mode on". After expiry, the merchant is redirected to [[expired-subscription]]. See [[plan-entity-free-expiry-and-demo]].
- **Plan-feature lookups are cached for 1 week.** Active feature-pack subscriptions are layered on top at lookup time. The cache flushes on plan / subscription changes. See [[plan-entity-feature-restrictions]].

## Where it appears

- [[plans]] — the catalog screen showing every available Plan as a price card + the feature comparison matrix.
- [[plans-purchase]] — per-plan purchase flow; the merchant picks billing cycle + any add-ons.
- [[plan-features]] — per-feature pack purchase flow (buying additional quota above the plan limit, e.g., +500 products beyond the cap).
- [[plan-details]] — read-only per-plan feature breakdown (deep-link to one plan).
- [[plan-services]] / [[plan-apps]] — paid services / app subscriptions purchased alongside plans.
- [[subscriptions]] — the merchant's My subscriptions list — shows the plan-type subscription with its lifecycle status.
- [[subscriptions-detail]] / [[subscription-details]] — per-subscription detail screen.
- Profile dropdown → Plan badge + *Choose plan* link — top-right user-account menu (owner-only — see [[plan-entity-overrides-lta-and-partner]]).
- [[expired-subscription]] — the takeover screen when the plan subscription has fully expired.
- [[contracts]] — long-term agreement plans negotiated directly with CloudCart; takes over [[plans]] when set.

## Related

### Related entities

- [[plan-feature]] — the per-feature catalog. Each Plan has many Plan Features (one row per feature, with the restriction value).
- [[site]] — the merchant's store record. Carries the active plan mapping.
- [[customer-group]] — separate concept (loyalty-tier grouping of customers). Distinct from Plan.

### Cross-cutting concepts

- [[plan-gates]] — the gating engine that consumes plan-feature values; the single most-referenced concept across the wiki.
- [[plan-vs-feature-pack]] — when to upgrade the Plan vs. buy a feature pack instead.
- [[subscription-lifecycle]] — the shared state machine for plan / feature-pack / app / service / theme subscriptions.
- [[merchant-subscription-lifecycle]] — merchant-question hub answering *"how do I upgrade / cancel / switch plan / what happens at expiry"*.

### Settings & webhooks

- [[details-billing]] — invoicing details applied to each plan renewal's invoice.
- [[billing-cards]] — saved card used for the plan's renewal charge.
- [[settings-hooks]] — subscription lifecycle events fire here (subscribed to via the webhook system); plan changes can trigger downstream sync.

## Open Questions

No outstanding questions on the hub — see individual aspect pages for any open items.
