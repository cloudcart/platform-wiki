---
type: feature
nav_path: "Plan → Feature"
route_name: plan-feature-packs
route_path: /admin/plan/feature/:id
aliases: ["Plan feature packs", "Feature pack buy panel", "Buy feature pack (Vue)", "Plan feature dialog", "Купи пакет за функция", "Допълнителен пакет"]
tags: [plans, plan-feature, feature-pack, upsell, billing, subscription, vue]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# Feature

## Purpose

The **plan-feature-packs** screen is the modern Vue version of the per-feature buy dialog — where a merchant lands after clicking *Buy feature* on a card in [[plan-features]], or when the platform redirects them after a plan-gate hit. It lists every available pack for **one** feature (e.g. *+100 products*, *+500 products*, dynamic-priced steps like *1000 / 2000 products*) and lets the merchant pick one to buy through the standard checkout.

This is the merchant-facing entry point for **buying extra quota on a single feature** without changing their entire plan tier. It is also where the platform funnels merchants when a feature isn't enabled on their plan at all (they then see a restriction banner explaining which plans support it).

A close sibling cluster (legacy Smarty) is documented at [[plan-features]] — both describe the same buy flow but render in different shells.

This page is the **hub**. It is intentionally slim — each behaviour lives on a dedicated aspect page (see *Sub-pages* below). Drill into the aspect that matches the question rather than reading everything.

## Where to find it

- **Automatic redirect** from any place in the admin where the merchant hits a feature limit (e.g. adding the 501st product on a 500-product plan, importing a CSV that would exceed the customer cap). The middleware sends the merchant to `/admin/plan/feature/<feature-mapping>` for that specific feature.
- **From [[plan-features]]** — clicking *Buy feature* / *Upgrade* on a feature card opens this screen (or its panel variant) for the chosen feature.
- **From over-limit warning toasts / banners** — the *Upgrade your quota from here* link routes here.

URL pattern: `/admin/plan/feature/{id}` — where `{id}` is the feature mapping (e.g. `products`, `customers`, `storage`, `discount-code-pro`, `support_meetings`). The screen renders as a full Vue page when reached at the URL directly, or as a `b-modal` side panel when opened from [[plan-features]] — the content is identical, only the chrome differs.

## What the merchant can do here

- **Browse the available packs** for the one feature, then pick and buy a single pack — see [[plan-feature-detail-pack-list]].
- **Run the standard checkout** for the chosen pack via a side panel, after which the calling card updates its quota in place — see [[plan-feature-detail-buy-flow]].
- **Read a restriction banner** (or get auto-routed to the upgrade-plan modal) when the feature isn't available on their plan — see [[plan-feature-detail-restrictions]].

What the merchant **cannot** do here is buy a pack for a feature their plan disables, exceed the feature's `max_value` cap, set a custom quantity outside the dynamic-pricing ladder, or combine multiple packs in one checkout. Those constraints are detailed on the aspect pages below.

## Sub-pages (in this cluster)

- [[plan-feature-detail-pack-list]] — the pack table (Name / Price / Buy), fixed vs dynamic-pricing rows, one-pack-at-a-time rule, mapping URL key.
- [[plan-feature-detail-restrictions]] — restriction banner, empty-packs auto-redirect, `max_value` cap, the server-side dynamic-pricing formula.
- [[plan-feature-detail-buy-flow]] — Buy → checkout side panel, per-open usage recompute, dynamic-pricing pack id, post-purchase in-place quota refresh + cache flush.
- [[plan-feature-detail-pack-lifecycle]] — pack subscription creation, cancel flow, survival through plan-tier downgrade, app-activation mapping aliases.

## Settings & fields

This is a buy / browse screen — no editable fields of its own. The merchant sees, per pack row, a **Name**, a per-cycle **Price** (excluding VAT), and a **Buy** button. The current-usage context (used / total, progress bar) lives on the calling card in [[plan-features]], not here. Full field tables are on [[plan-feature-detail-pack-list]].

## Business rules

The detailed business rules live on the aspect pages. The headline rules:

- **Packs are filtered by `dynamic_pricing` match** — fixed and dynamic-pricing packs never mix on one screen. See [[plan-feature-detail-pack-list]].
- **Restriction by plan hides the table** — sourced from `plan.restrict.feature_purchase.<mapping>`; empty packs auto-open the upgrade-plan modal. See [[plan-feature-detail-restrictions]].
- **`max_value` caps the buy** — an over-cap purchase is rejected with `plan.plan_limit`. See [[plan-feature-detail-restrictions]].
- **Successful purchase updates the parent card in place + flushes the gate cache** — see [[plan-feature-detail-buy-flow]].
- **Packs are independent subscriptions** — they survive a plan-tier downgrade and are cancelled from [[subscriptions]]. See [[plan-feature-detail-pack-lifecycle]].

## Related

- [[plans]] — full plan catalog (used by the *View prices* / upgrade-plan path).
- [[plans-purchase]] — the shared checkout flow this screen hands off to.
- [[plan-features]] — the cards screen (one card per feature) that opens this panel.
- [[plan-gates]] — the gating concept that funnels merchants here on a limit hit.
- [[subscriptions]] — purchased packs appear here; cancellation happens here.
- [[merchant-subscription-lifecycle]] — the broader subscription state machine.
- [[billing-cards]] — saved card used during the redirect-to-checkout step.
- [[expired-subscription]] — when a pack subscription's payment fails.

## Open questions

None.
