---
type: feature
nav_path: "Plan → Plan features (Vue grid)"
route_name: plan-features
route_path: /admin/plan-features
aliases: ["PlanFeaturesList", "FeatureCard grid", "Feature cards page", "Plan features list (Vue)", "Buy feature card", "Upgrade feature card"]
tags: [plans, plan-feature, feature-pack, vue, grid, cards]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-features]]. See the hub for the other aspects (warning banners, pack list, purchase flow, restrictions & limits, subscription lifecycle, middleware mappings).

# Plan features — modern Vue card grid

## Purpose

The modern Vue tab at `/admin/plan-features` renders a grid of **per-feature cards** — one card per plan-feature row — letting the merchant browse all their gated features in one place, see live usage / quota for each, and open the pack-purchase panel for any feature directly. This is the "browseable" cousin of the per-feature URL `/admin/plan/feature/{mapping}` (which is exit-ramp-only). Cards expose a *Buy feature* / *Upgrade* / *Cancel* action that opens the [[plan-feature]] side-panel for the actual checkout.

## Where to find it

- Direct URL: `/admin/plan-features` (modern Vue route, distinct from the legacy `/admin/plan/feature/{mapping}` upsell page documented at [[plan-features]]).
- Reached from the Plan area sidebar.

## What the merchant can do here

- Browse every plan-feature their account has, paginated 25 per page (URL-synced via `?page=N&perpage=N`).
- Search features by name with the **SearchInResults** input (re-paginates from page 1 with `filters[query]=<term>`).
- See per-feature **usage / quota** with a progress bar for numeric and storage features.
- Click *Buy feature* to open the [[plan-feature]] panel for that feature's packs.
- Click *Upgrade* on a purchased feature to add more quota.
- Click *Cancel* on a purchased boolean-feature card to deep-link to [[subscriptions]] filtered to that pack.

## Settings & fields

### Top bar

| Control | Behaviour |
|---------|-----------|
| **SearchInResults** input | Emits `start-search` on submit; `getData(search)` re-paginates from page 1 with `filters[query]=<term>` in the query string |
| **Top pagination** (`DataTablePagination`) | Standard list pagination |

### Footer

| Control | Behaviour |
|---------|-----------|
| **Bottom pagination** | Mirrors the top pagination control |
| **Results label** | *Results X - Y of Z* entries label with a per-page selector |

### Loading / empty states

- `CardGhostLoader` is rendered in place of the cards while data loads.
- a not-found error shown when the search returns zero rows.

### Per-feature card (`FeatureCard`)

| Element | Behaviour |
|---------|-----------|
| **App icon** | When the feature is tied to an app (e.g. an XML-feed app's products feature), the app's icon is pulled from `useSharedAppsInfo` (verify) |
| **Service icon** | Generic `fa-regular fa-gear` icon when no app match |
| **Feature name** | Translated string from `name_translated` |
| **`cast === 'int'` usage** | *`used` / `featureValue`* + a `b-progress` bar (variant `success`). `featureValue` is **Unlimited** when `remaining_value === true`, the formatted total otherwise, or **0** when not purchased |
| **`cast === 'storage'` usage** | *`used_formatted` / `total_formatted`* (human-readable bytes) + progress bar from `feature.storage.used` over `feature.storage.total` |
| **Cancel button** (`btn-ghost`) | Visible only for `cast === 'bool'` features AND when already purchased; routes to `subscriptions-list` filtered by mapping |
| **Upgrade button** (`btn-ghost`) | Visible when purchased AND `hasUnlimited === false`; opens the [[plan-feature]] panel |
| **Buy feature button** (`btn-white`) | Visible when NOT purchased OR not-unlimited; opens the [[plan-feature]] panel |

### Cancel deep-link query shape (boolean features only)

For boolean features that are currently Active, the *Cancel* button is a `router-link` to:

```
{ name: 'subscriptions-list', query: { 'filters[mapping][]': [feature.mapping], page: 1, perpage: 25 } }
```

The merchant lands on [[subscriptions]] pre-filtered to that pack's subscription and cancels from there. The cancel takes effect at the pack's `next_billing_date` — see [[plan-features-subscription-lifecycle]].

### Data endpoint

- `GET /admin/api/core/plan-feature` paginated (default 25 per page).
- Pagination URL-synced: `?page=N&perpage=N`.
- Search filter: `filters[query]=<term>`.

## Business rules

### Post-purchase in-place quota update — no refetch

When the [[plan-feature]] panel emits `success`, `handleAfterPay(result)` runs on the parent:

1. Iterates `result.status[]` items.
2. For each item, sets the local clone's `usage.remaining` and `usage.total` to:
   - **`true`** for `cast === 'bool'` features (active subscription = feature enabled).
   - **`Number(remaining) + Number(item.value)`** for numeric features (additive).
3. Replaces the feature in the `features[]` array by mapping match — the affected card re-renders with the new state **without a refetch**.

The Plan-area cache for that feature is also flushed server-side at purchase time — so any other admin screen the merchant navigates to picks up the new effective quota immediately. See [[plan-features-subscription-lifecycle]].

### Cancel is a deep-link, not an in-place cancel

The *Cancel* button on a boolean-feature card does NOT cancel the subscription in place — it navigates to [[subscriptions]] pre-filtered to the pack, and the merchant completes the cancel there. This is intentional: the cancel itself goes through the same subscription-cancel flow as every other subscription, with the same `next_billing_date` semantics (see [[plan-features-subscription-lifecycle]]).

### Cards inherit gate visibility from the API

The card grid only shows features the merchant's plan EXPOSES — features fully restricted by `plan.restrict.feature_purchase` (see [[plan-features-restrictions-limits]]) don't render a card. The merchant can't browse to packs for a feature their plan doesn't allow.

### Search filter is server-side

The `filters[query]=<term>` parameter is applied server-side on the `GET /admin/api/core/plan-feature` endpoint — the search isn't a client-side filter of an already-loaded list. Pagination is reset to page 1 on every search submit.

### `PlanFeature` panel is opened, not navigated

Clicking *Buy feature* / *Upgrade* opens the [[plan-feature]] side-panel **as a modal** over the grid — the merchant doesn't lose their place. See [[plan-feature]] for the panel content (pack table + restriction banner + checkout). Closing the panel (or completing purchase) keeps the grid in view with the updated card.

## Related

- [[plan-features]] — hub (legacy `/admin/plan/feature/{mapping}` page + the cluster overview).
- [[plan-feature]] — the per-feature pack-purchase panel this grid opens.
- [[plan-features-subscription-lifecycle]] — what happens when a card purchase succeeds; the cancel deep-link target.
- [[plan-features-restrictions-limits]] — which features get a card at all.
- [[subscriptions]] — Cancel deep-link target for boolean-feature cards.
- [[plan-gates]] — gating concept.

## Open questions

None.
