---
type: concept
nav_path: "Concept → Plan gates and limits"
route_name: ""
route_path: ""
aliases: ["Plan gates", "Plan limits", "Plan restrictions", "Plan feature gates", "Feature gating", "Plan paywall", "Plan-feature paywall", "Quota", "Ограничения на плана", "Лимит на плана", "Платена функция", "Заключена функция"]
tags: [billing, plans, gating, concepts]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Plan gates and limits

## Definition

A **plan gate** is the rule that decides — for every action the merchant takes in the admin panel — whether their current subscription plan allows that action, blocks it outright, or allows it only up to a quota. CloudCart's entire feature set is split into ~200 named **plan-features** (e.g., `products`, `customers`, `discount-code-pro`, `xml_sync_limit`, `cc_analytics`, `customer_export`, `customer_import`, `ssl_certificate`, `storefront_builder`, `cloudio_ai`, `multi-warehouse`, `abandoned_notification`, `video_slider_widget`, `variants.listing`, `subscriber_forms`, `support_meetings`), and every plan in the catalog ([[plans]]) specifies, per feature, either *unrestricted*, *boolean enabled/disabled*, or *a numeric cap*. When the merchant clicks a button, opens a screen, or imports a file, the platform looks up the relevant plan-feature, compares it against the plan's restriction (and any feature-pack add-ons or LTA-contract overrides the merchant has bought), and either lets the action through, redirects to a paywall, or shows an upgrade prompt.

Plan gates are how CloudCart monetises the platform: a Starter plan merchant can create 500 products and zero Code-PRO discounts; a Pro merchant can create 5,000 products and unlimited Code-PRO discounts; an Enterprise merchant has no caps. The same rules govern paid services (support meetings, machine translation), bandwidth-style caps (XML sync limit, storage), and pure on/off features (storefront builder, SSL certificates).

## Sub-pages (in this cluster)

This concept is split into 5 aspect pages. Drill into the one that matches the question rather than reading every page.

- [[plan-gates-restriction-shapes]] — the three shapes a restriction can take (*unrestricted* / *boolean* / *numeric*); the 1-week-cached `<feature, plan>` lookup; how feature-pack add-ons sum on top of the plan's base value.
- [[plan-gates-enforcement-points]] — the three places a gate runs (create-endpoint HTTP 402, path-access redirect, boolean inline lock); the 402 payload shape; the `/admin/plan/feature/<mapping>` paywall screen.
- [[plan-gates-lta-contracts]] — Long-Term Agreement contracts that override the plan's feature values for the contract duration; why LTA merchants can't shop for a different plan.
- [[plan-gates-trial-and-catalogs]] — the free `startup` plan auto-expiry conditions by issuer country; the `cc-demo` evaluation plan mapped to enterprise limits; per-issuer-country plan catalogs.
- [[plan-gates-feature-naming]] — the plan-feature mapping naming conventions (entity counters, app prefixes, `discount_*`, `cart_rules_*`, `*_report`); where the merchant configures gates (they don't — catalog-defined by CloudCart staff).

## Scope

What this concept covers (across the 5 sub-pages): restriction shapes and the cached lookup, the enforcement points and the **`/admin/plan/feature/<mapping>`** paywall screen ([[plan-features]]), LTA-contract overrides, trial-plan expiry / catalogs, and the feature-key naming scheme. See the **Sub-pages** list above for the one-line summary of each.

What it does NOT cover:

- The pricing of each plan or the exact numeric values per plan — those live in the catalog on [[plans]] and the per-plan detail pages ([[plan-details]]).
- The feature-pack catalog (which packs exist for which features) — that lives on [[plan-features]]; the plan-vs-pack decision lives on [[plan-vs-feature-pack]].
- LTA-contract creation / billing flow — see [[plans-purchase]].
- Storefront-side gating (what features are available on the customer-facing site) — this concept is admin-panel only.

## Contrasts

- **Plan gates vs. role permissions**: plan gates restrict what the *store* can do (based on what was paid for). Role permissions ([[merchant-roles]]) restrict what an individual *staff member* can do (based on their assigned role). A Pro-plan store with a "Stock manager" staff role: the plan allows discounts, the role does not allow that staff member to edit them. Both gates must pass for the action to succeed.
- **Plan gates vs. feature flags / app installation**: plan gates are paywalls (paid services), while feature flags / apps are install-toggles. A feature can be both — e.g., the Multi-warehouse app must be installed *and* the plan must have `multi-warehouse: true`. Apps without plan gates work on every plan; gated apps redirect to the paywall when installed on a non-supporting plan.
- **Plan gates vs. trial / sandbox restrictions**: a plan-gate failure says "this isn't included in your plan, upgrade or buy a pack." A trial / sandbox restriction says "your free Start Up plan is about to expire because you haven't logged in for 30 days" — a different message, a different recovery path. See [[plan-gates-trial-and-catalogs]].
- **Plan gates vs. cart-rule restrictions / discount stacking**: those are storefront-side promotion rules (see [[discount-stacking]]). Plan gates are admin-side paywalls — they decide whether the merchant can even *create* a Code-PRO discount, not whether one will stack at checkout.
- **Plan gates vs. validation errors**: a plan-gate response is HTTP 402 (Payment Required) with a paywall payload — the frontend renders the "Upgrade your quota from here" link. A validation error is HTTP 422 with field-level messages. The merchant sees a different modal for each. See [[plan-gates-enforcement-points]].

## Where it applies

Plan gates are the most-referenced concept in the wiki — they touch virtually every feature page. Every feature page that lists `plan_gates` in its frontmatter is gated (e.g. [[marketing-discounts-code-pro]] by `discount-code-pro`, [[customers-import]] by `customer_import`, [[settings-ssl]] by `ssl_certificate`, [[apps-mailchimp]] by `mailchimp`). The four landing points:

- **The paywall** — [[plan-features]] (the `/admin/plan/feature/<mapping>` upsell screen, destination of every quota-exhausted redirect), backed by the [[plans]] catalog and the [[plans-purchase]] flow.
- **Numeric quotas** — pages that show "X of Y used": [[products]], [[customers]], [[orders]], [[settings-staff]], [[settings-files]], [[marketing-segments]], the XML apps, etc. The per-feature key for each (e.g. `products`, `customers`, `orders_amount` / `orders_revenue`, `xml_sync_limit`) follows the naming scheme catalogued on [[plan-gates-feature-naming]].
- **Boolean on/off features** — [[settings-ssl]] (`ssl_certificate`), [[design-theme-editor]] (`storefront_builder`), [[apps-cloudio-overview]] (`cloudio_ai`), [[customers-import]] / [[customers-export]], [[orders-abandoned]] (`abandoned_notification`), [[analytics-pipeline]] (`cc_analytics`), and similar.
- **Service / consumable quotas** (deplete-as-used) — [[marketing-channels-viber]] (`viber_messages`), [[apps-multilang-stores]] (`machine_translation`).

The full per-prefix key catalogue (entity counters, `discount_*`, `cart_rules_*`, `<erp>_total_products`, boolean toggles, `*_report`) lives on [[plan-gates-feature-naming]]. The per-discount-type counters specifically (`discount_global` for codeless, `discount_coupon` for code-based, `discount_fixed`, `discount_quantity`, plus the `discount-code-pro` boolean and its `discount-code-pro-generator` cap) split as explained on [[discount-stacking]].

## Related

- [[plans]] — the plan catalog screen.
- [[plans-purchase]] — the purchase flow for changing plan.
- [[plan-features]] — the feature-pack upsell screen (`/admin/plan/feature/<mapping>`).
- [[plan-details]] — read-only per-plan feature breakdown.
- [[plan-vs-feature-pack]] — when to upgrade the plan vs. buy a feature pack.
- [[plan-services]] / [[plan-apps]] — paid services / app subscriptions purchased alongside plans.
- [[plan]] — the Plan entity carrying restrictions.
- [[plan-feature]] — the Plan-Feature entity catalog.
- [[site]] — the Site entity carries the current plan mapping.
- [[expired-subscription]] — the expiry screen merchants land on when their plan is auto-suspended.
- [[merchant-roles]] — staff role restrictions; both gates must pass.
- [[discount-stacking]] — explains how `discount_global` vs. `discount_coupon` counters split.
- [[cart-vs-order-lifecycle]] — orders count toward the `orders_amount` / `orders_revenue` numeric quotas.
- [[checkout-flow]] — `users_traffic` and `orders_amount` accumulate via this flow.
- [[order-status-workflow]] — only orders in counted statuses (`paid` / `completed`) drive the revenue cap.
- [[backups-and-restore]] — `backups` plan-feature governs backup retention / count.
- [[notification-delivery]] — admin alerts include plan / subscription warnings.
- [[marketing-discounts]] — discount counts gate-split by codeless vs. code-based.
- [[orders-abandoned]] — `abandoned_notification` gate.
- [[design-theme-editor]] — `storefront_builder` boolean gate.

## Open Questions

No outstanding questions — all previously-flagged items resolved or distributed to sub-pages. (Per-merchant quota values, feature-pack availability, and tier-specific behaviour are runtime data the AI Assistant resolves via GraphQL queries against the merchant's account — not static wiki content.)
