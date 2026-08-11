---
type: concept
nav_path: "Concept → Plan gates → Enforcement points & paywall"
aliases: ["Plan gate enforcement", "Where the gate runs", "HTTP 402 plan limit", "Payment Required plan gate", "Plan limit reached", "Paywall redirect", "admin plan feature mapping", "Upgrade your quota from here", "Заключена функция redirect", "Достигнат лимит"]
tags: [billing, plans, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-gates]]. See the hub for the other aspects (restriction shapes, LTA contracts, trial / catalogs, feature naming).

# Plan gates — enforcement points & paywall

## Definition

A plan-feature is checked in **three different places** depending on what the merchant is trying to do. Knowing which enforcement point fired tells support what the merchant saw — a blocking modal, an automatic redirect, or an inline lock icon.

1. **Create-endpoint check** — when the merchant clicks *Save* on a new product / discount / customer / blog article, the create endpoint runs the gate as a pre-condition. If the quota is full, the response is **HTTP 402** with the feature key, the feature name, and the field being violated. The frontend renders the paywall modal with an *"Upgrade your quota from here"* link to `/admin/plan/feature/<mapping>`.

2. **Path-access check** — some URLs themselves are paywall-gated (e.g., `/admin/discounts/add/code` is locked when `discount_coupon` is exhausted). Visiting a locked URL redirects to the paywall screen automatically. This is how the platform locks deep-links: a merchant emailed a "create CSV import" link is redirected to the upsell when their plan doesn't support imports.

3. **Boolean inline check** — for features that show up as buttons or panels inside an existing screen, the page renders the locked element with a small lock icon + *"Upgrade"* link. Examples: the SSL Certificate row on [[settings-domains]], the "Variants in listing" toggle on [[variants-index-new]], the *Convert to recurring order* button on [[orders-subscriptions]]. The merchant CAN see the option exists, but clicking it routes to the upsell instead of doing the action.

## Scope

What this covers:

- The three enforcement points — create-endpoint check, path-access check, boolean inline check.
- The HTTP 402 "Plan limit reached" response payload.
- The `/admin/plan/feature/<mapping>` paywall screen behaviour.

What it does NOT cover:

- The three restriction shapes the gate compares against — see [[plan-gates-restriction-shapes]].
- The feature-pack catalog rendered on the paywall — see [[plan-features]].
- The specific per-feature quotas — runtime data on [[plans]] / [[plan-details]].

## Contrasts

- **HTTP 402 vs. HTTP 422**: a plan-gate failure returns 402 (Payment Required) with a paywall payload (the frontend renders the upgrade modal). A field-validation failure returns 422 with field-level messages (the merchant sees inline form errors). Different status, different modal, different recovery — see also the Contrasts on [[plan-gates]].
- **Create-endpoint block vs. path-access redirect**: the create-endpoint check blocks the *Save* action and keeps the merchant on the page with a modal; the path-access check redirects the whole navigation to the paywall before the screen even renders.
- **Numeric block vs. boolean inline lock**: a numeric gate trips only once the quota is exhausted (the button works up to the cap); a boolean inline lock is always present for un-entitled plans (the element renders locked from the start).

## Where it applies

### The HTTP 402 "Plan limit reached" response

When a numeric gate trips, the API returns HTTP 402 (Payment Required) with a payload carrying:

- `message` — the literal merchant-facing string, e.g., *"You reached the limit of feature **Products - 500**"*.
- `info.key` — the feature mapping (e.g., `products`, `customer_import`).
- `info.name` — the localised feature name (e.g., "Products", "Customer import").
- `type` — `feature`.
- `field` — the form field that failed (e.g., `code` when a discount-pro creation fails on the `discount-code-pro` gate).

The frontend's universal error handler reads this payload and renders the paywall modal. The modal's primary action redirects to `/admin/plan/feature/<mapping>` — the feature-pack upsell screen ([[plan-features]]).

### The `/admin/plan/feature/<mapping>` paywall

This is the single URL every numeric gate funnels to. It shows:

- A warning banner with the exact feature and current limit.
- A list of available **feature packs** for that feature (e.g., *+100 products*, *+500 products*, *+1000 products*).
- For some features, a **dynamic-pricing** picker — the merchant picks a custom quantity, sees the price scale.
- A *Buy* button per pack that seeds the admin checkout cart and redirects to `/admin/checkout`.

If the feature isn't available on the merchant's plan at ALL (not just exhausted), the screen replaces the pack list with: *"This feature is not enabled for your plan. To access it, please upgrade your plan."* + a list of plans that DO support it, e.g., *"Plans that support this functionality are: **Pro**, **Unicorn**"*.

The screen also surfaces the alternative path — the merchant can buy the pack OR upgrade the plan from here; the trade-off between the two is covered on [[plan-vs-feature-pack-cost-heuristic]].

## Related

- [[plan-gates]] — hub.
- [[plan-features]] — the `/admin/plan/feature/<mapping>` paywall screen the 402 redirects to.
- [[plan-gates-restriction-shapes]] — the values the gate compares against to decide whether to fire.
- [[plans]] / [[plans-purchase]] — the upgrade-plan alternative shown when a feature isn't on the plan at all.
- [[plan-vs-feature-pack-cost-heuristic]] — pack-vs-upgrade decision shown on the same paywall.
- [[settings-domains]] — `ssl_certificate` inline lock example.
- [[variants-index-new]] — `variants.listing` inline toggle lock example.

## Open Questions

None.
