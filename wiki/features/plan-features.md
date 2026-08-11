---
type: feature
nav_path: "Plan → Feature pack"
route_name: admin.plan.feature
route_path: /admin/plan/feature/{mapping}
aliases: ["Feature pack", "Buy feature pack", "Feature add-on", "Plan feature purchase", "Plan extension", "Купи пакет", "Допълнителен пакет", "Пакет за функция", "Закупуване на функция"]
tags: [plans, plan-feature, feature-pack, upsell, billing, subscription, smarty]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---
# Plan feature packs

## Purpose

The **plan-feature** screen at `/admin/plan/feature/{mapping}` is the **per-feature upsell page** — where a merchant lands when they've hit a plan limit (e.g. *Maximum number of products for your current plan reached*) but don't want to upgrade their entire plan. Instead they buy a one-off **feature pack** that extends just that one limit (e.g. *+500 products*) on top of their existing plan. Some features also support **dynamic pricing**, where the merchant picks a custom quantity (e.g. *2000 products*, *5000 products*) and sees the recalculated price live.

The companion route — `admin.feature.purchase` at `/admin/plan/feature/{id}/purchase/{value?}` — is the action behind each pack's *Buy* button: it doesn't render a separate screen, it just seeds a checkout cart with the chosen pack and redirects to the standard admin checkout.

This screen is what plan-gate enforcement throughout the admin panel funnels merchants into when they cross a numeric limit. See [[plan-gates]] for the gating concept.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[plan-features-warning-banners]] — the warning note + restriction banner at the top; *"You reached the limit of feature **<feature> - <limit>**"*; *"Plans that support this functionality are: ..."*; "Disabled" rendering for boolean features; postfixes.
- [[plan-features-pack-list]] — the pack-list table (Pack name / Price / Buy); fixed-price packs vs the dynamic-pricing ladder; the `dynamic_pricing` flag-match filter; mapping URL examples (`products`, `customers`, `storage`, `discount-code-pro`, `support_meetings`, `custom_hostname`).
- [[plan-features-purchase-flow]] — the `/admin/plan/feature/{id}/purchase/{value?}` action; cart reset on every *Buy*; side-panel layout + close (×) = browser-back; one pack per checkout.
- [[plan-features-restrictions-limits]] — `enable_feature_pack` (per plan × feature), `plan.restrict.feature_purchase` (per feature → plan tier), `max_value` cap with the *"Your package allows X products"* error; the volume-discount formula; demo-as-enterprise; `'@@@'` null sentinel; bank-transfer grace (30 / 90 days).
- [[plan-features-subscription-lifecycle]] — pack creates a subscription (`model_type = cloudcart_feature`); 1-week feature-value cache flush; cancel preserves records but blocks new creates; cancel takes effect at `next_billing_date`; packs survive plan downgrade; boolean-feature pack = feature enabled.
- [[plan-features-modern-vue-grid]] — the modern Vue tab at `/admin/plan-features` (component `PlanFeaturesList`); `FeatureCard` grid; usage progress bars; *Buy feature* / *Upgrade* / *Cancel* actions; post-purchase in-place quota update; `GET /admin/api/core/plan-feature` data endpoint.
- [[plan-features-middleware-mappings]] — plan-gate middleware that redirects to this screen (302 for browser, JSON `{redirect: ...}` for AJAX); the pack→app mapping aliases (`shipping_payment_sync` → `omniship`, `cloudio_ai` → `cloudio`, messenger / email / viber → `campaigns`).

## Where to find it

- **Automatic redirect** when the merchant hits a feature limit anywhere in the admin panel — adding a 501st product on a 500-product plan, importing a CSV that would exceed the customer limit, enabling a feature gated to higher tiers, etc. The platform redirects to `/admin/plan/feature/{mapping}` for that specific feature.
- **From plan-feature warning toasts / banners** — e.g. *"Your package allows 500 products. Upgrade your quota from here"* — the **Upgrade your quota from here** link goes to this screen.
- The screen is **deep-linkable** by feature mapping but is not on the main sidebar — merchants reach it via warnings, not by browsing. See [[plan-features-middleware-mappings]] for the redirect plumbing.

URL pattern: `/admin/plan/feature/{mapping}` — e.g. `/admin/plan/feature/products`, `/admin/plan/feature/customers`, `/admin/plan/feature/storage`, `/admin/plan/feature/discount-code-pro`, `/admin/plan/feature/support_meetings`.

The purchase action URL is `/admin/plan/feature/{id}/purchase/{value?}` — see [[plan-features-purchase-flow]].

## What the merchant can do here

- See **why** they were redirected (feature name + current limit) — see [[plan-features-warning-banners]].
- Pick a **feature pack** from the list and click *Buy* to go through checkout — see [[plan-features-pack-list]] and [[plan-features-purchase-flow]].
- For dynamic-pricing features, pick from a **continuous price ladder** of quantity steps with volume discounts — see [[plan-features-pack-list]] and [[plan-features-restrictions-limits]].

What the merchant **cannot** do here:

- Combine multiple packs in one checkout (one pack per click; cart is reset each time) — see [[plan-features-purchase-flow]].
- Exceed the feature's `max_value` ceiling — see [[plan-features-restrictions-limits]].
- Set a custom price, enter a discount code, or mix fixed + dynamic packs — see [[plan-features-pack-list]].
- Buy a pack for a feature their plan doesn't allow — restriction banner shown instead (see [[plan-features-warning-banners]]).
- Browse packs for features they haven't hit yet — packs are an "exit ramp", reached only via gate redirect or via the alternative card grid at [[plan-features-modern-vue-grid]].

## Settings & fields

The screen is composed of three regions, each documented on its own aspect page:

| Region | Aspect |
|--------|--------|
| Warning note + restriction banner at the top | [[plan-features-warning-banners]] |
| Pack-list table (Pack name / Price / Buy) | [[plan-features-pack-list]] |
| Side-panel chrome + close (×) + Buy → checkout redirect | [[plan-features-purchase-flow]] |

The modern alternative surface (browseable card grid) is documented on [[plan-features-modern-vue-grid]].

## Business rules

The cross-cutting rules are documented on the relevant aspect:

- **Feature-pack purchase can be disabled per-plan** via `enable_feature_pack` — see [[plan-features-restrictions-limits]].
- **Plan-tier-restricted features** (`plan.restrict.feature_purchase`) get the restriction banner — see [[plan-features-warning-banners]] + [[plan-features-restrictions-limits]].
- **`max_value` cap is enforced live** before redirect — see [[plan-features-purchase-flow]] + [[plan-features-restrictions-limits]].
- **Dynamic-pricing volume-discount formula** generates the ladder server-side — see [[plan-features-restrictions-limits]].
- **Boolean features show "Disabled"** instead of a number; buying a pack flips them ON via subscription — see [[plan-features-warning-banners]] + [[plan-features-subscription-lifecycle]].
- **Cart is reset on entry**; one pack per checkout — see [[plan-features-purchase-flow]].
- **Packs create subscriptions** (not one-shots); their value is added to plan value at gate-check time; the 1-week feature-value cache is flushed on purchase — see [[plan-features-subscription-lifecycle]].
- **Cancelling a pack** preserves existing records, blocks new creates; takes effect at `next_billing_date` — see [[plan-features-subscription-lifecycle]].
- **Packs survive plan downgrade** — independent subscription, must be cancelled separately — see [[plan-features-subscription-lifecycle]].
- **Pack mapping aliases** route to the right app activation (`omniship`, `cloudio`, `campaigns`) — see [[plan-features-middleware-mappings]].
- **Demo sites resolve as Enterprise** for plan-feature lookups (verify) — see [[plan-features-restrictions-limits]].
- **Profile dropdown does NOT link here** — packs are reached only via gate redirect — see [[plan-features-middleware-mappings]].

## Related

- [[plans]] — full plan catalog; the upgrade-instead alternative to buying a pack.
- [[plans-purchase]] — per-plan purchase flow; same side-panel chrome.
- [[plan-feature]] — modern Vue pack-purchase panel opened from [[plan-features-modern-vue-grid]] cards.
- [[plan-gates]] — the gating concept that funnels merchants here.
- [[plan-vs-feature-pack]] — pack-vs-upgrade decision merchants face.
- [[subscriptions]] — where purchased packs appear as active subscriptions.
- [[billing-cards]] — saved cards used during the redirect-to-checkout step.
- [[details-billing]] — billing details + invoicing setup.
- [[expired-subscription]] — when a pack-subscription's payment fails.
- [[merchant-subscription-lifecycle]] — merchant-question hub for pack vs plan vs cancel.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
