---
type: entity
nav_path: "Entity → Plan → Catalog structure"
aliases: ["Plan catalog structure", "Plan slug", "Plan mapping", "Plan name", "Plan type", "Plan issuer company", "Plan country filter", "Plan sort order", "Plan hidden features"]
tags: [entity, billing, plans, catalog, gating]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[plan]]. See the hub for the other aspects (billing cycles, feature restrictions, lifecycle, free-plan expiry + demo, LTA + partner overrides).

# Plan — Catalog structure

## Identity

The catalog-level identity of a [[plan|Plan]] — the fields that decide **whether the plan exists in the catalog at all**, **who can see it**, **what label renders**, and **in what order it sorts on [[plans]]**. These are the attributes CloudCart staff set when adding a plan record; merchants never edit them.

The slug (mapping) is the stable identifier the gating engine reads when resolving plan-feature lookups; the name is the display label; the type + issuer-company decides catalog visibility per merchant.

## Aliases

- **Plan slug** / **Plan mapping** — the stable internal identifier (`startup`, `starter`, `basic`, `pro`, `business`, `enterprise`, `unicredit`, `cc-demo`, etc.).
- **Plan name** — display label, possibly localised per country.
- **Plan type** — `default` vs `unicredit` (or per-partner reseller code).
- **Issuer company** — the invoicing entity binding (BG, DE, etc.); decides who sees the plan.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Mapping** (slug) | Stable identifier | Used internally to resolve plan-feature lookups. The slug `cc-demo` is special — gates resolve as Enterprise (see [[plan-entity-free-expiry-and-demo]]). The legacy slug `trial` is not actively issued today. |
| **Name** | Display label (*Start Up*, *Pro*, *Business*, *Enterprise*, *14-Tage-Test (Starter)* for DE free plan, etc.) | Stored WITHOUT per-language translation — localisation is hard-coded per country via override mappings. Merchant-visible on [[plans]] cards and in the profile dropdown badge. |
| **Type** | `default` / `unicredit` / per-partner | Filters which merchants see this plan. `default` is the standard catalog; `unicredit` (or other partner types) shows only to partner-network merchants. See [[plan-entity-overrides-lta-and-partner]]. |
| **Issuer company** | Country / invoicing-entity binding | Set to a single issuer-company ID (BG, DE, etc.) for country-specific plans, OR empty for global plans visible everywhere. Drives the catalog filter on [[plans]]. |
| **Active in catalog** | yes / no | Catalog-level published flag — when no, the plan is filtered out of [[plans]] regardless of price-detail status. |
| **Sort order** | Effective sort key | Plans are ordered on [[plans]] by **lowest billing-cycle price ascending** — the cheapest first, the most expensive last. Plans with no active price-detail variants are filtered out entirely (see [[plan-entity-billing-cycles]]). |
| **Feature groupings** | UI-only grouping in the comparison matrix | Resources, Branding, Reports, Support, Synchronizations, Themes, Subscriptions, Domains. Determines how the [[plans]] comparison table layouts features. |
| **Hidden features** | Per-plan + per-feature exclusion list | Specific feature × plan combinations can be hidden from the comparison matrix (when a feature simply doesn't apply to a given plan). Hidden rows don't render at all (not shown as ✗). |
| **Per-language overrides** | Country-specific re-labels | E.g., the *Start Up* free plan re-labelled as **14-Tage-Test (Starter)** for DE merchants. Hard-coded per country. |

## Business rules

### The catalog is country / issuer-company aware

[[plans]] is filtered by the merchant's invoicing country (issuer company). Each plan is either:

- **Country-specific** — issuer-company set; visible only to merchants invoiced through that entity.
- **Global** — no issuer-company set; visible to all non-partner merchants.

A merchant in DE sees only DE plans + global plans; a BG merchant sees BG plans + global plans. They cannot see each other's local-only plans.

### Plans are sorted by lowest billing-cycle price ascending

The cheapest plan appears first; the most expensive last. Plans without any active price-detail variants are filtered out entirely (a soft-disable mechanism — see [[plan-entity-billing-cycles]]).

### Free *Start Up* plan special handling for DE

Germany's invoicing-entity merchants see the global *Start Up* free plan re-labelled as **14-Tage-Test (Starter)** and pointed at the DE Starter plan record. This is a per-country branding override — the free plan effectively becomes a 14-day trial of Starter in Germany. Other countries use *Start Up* unchanged.

### Plan name localization is hard-coded per country

Plan names are stored WITHOUT per-language translation in the catalog row. Localisation is hard-coded per country via helper overrides (e.g., the DE `startup → 14-Tage-Test (Starter)` mapping). There is **no merchant-controlled translation UI** for plan names. For broader localisation, CloudCart staff add per-country override mappings.

### Hidden features render as gaps, not ✗

Hidden feature-row × plan-column cells in the comparison matrix on [[plans]] simply don't render — they appear as a blank cell, not as a crossed-out indicator. Hidden is "this feature is not applicable to this plan" rather than "this plan locks this feature".

### `trial` plan slug is legacy

`trial` is a legacy slug, NOT actively issued today. The active free-entry plan is `startup` (with the DE override re-pointing to `starter`). Trial appears in historical Site records but is not assigned to new merchants. See [[plan-entity-free-expiry-and-demo]] for current free-plan behaviour.

## Where it appears

- [[plans]] — the catalog filtered by issuer + type; cards rendered in price-ascending order; hidden features absent from the comparison matrix.
- [[plan-details]] — deep-link to a single plan's feature breakdown.
- [[plan-features]] / [[plan-apps]] / [[plan-services]] — companion catalogs for pack / app / service purchases, filtered by the same issuer.
- Profile dropdown → Plan badge — shows the current Plan's localised display name.

## Related

- [[plan]] — hub.
- [[plan-feature]] — the per-feature catalog the Plan's restrictions pivot to.
- [[plans]] — the merchant-facing catalog feature page.
- [[plan-details]] — per-plan detail screen.
- [[site]] — carries the merchant's active plan-mapping.

## Open Questions

None.
