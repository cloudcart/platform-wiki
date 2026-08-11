---
type: feature
nav_path: "Plan → Feature pack → Plan-gate middleware + mappings"
route_name: admin.plan.feature
route_path: /admin/plan/feature/{mapping}
aliases: ["Plan-gate redirect", "Plan middleware", "AJAX plan-gate redirect", "Mapping alias", "omniship mapping", "cloudio mapping", "campaigns mapping"]
tags: [plans, plan-feature, feature-pack, middleware, redirect, mapping]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-features]]. See the hub for the other aspects (warning banners, pack list, purchase flow, restrictions & limits, subscription lifecycle, modern Vue grid).

# Plan features — plan-gate middleware + mapping aliases

## Purpose

The plan-feature screen at `/admin/plan/feature/{mapping}` is reached almost exclusively by **automatic redirect from the plan-feature middleware** — not by browsing. This page documents how the middleware decides to redirect, how it handles the difference between browser navigation and AJAX requests, and how some pack mappings are **aliased internally** before being handed to the subscription / app-activation step (e.g. `shipping_payment_sync` → `omniship`).

## Where to find it

- The middleware runs on **every admin-panel request**.
- It decides to redirect to `/admin/plan/feature/{feature_mapping}` whenever the requested URL requires a feature the merchant's plan doesn't allow or whose quota is exhausted.
- The merchant doesn't "find" this — they're sent here.

## What the merchant can do here

Nothing directly — this aspect is the redirect plumbing the merchant experiences as:

- Hitting *Add product* on a full plan → landing on `/admin/plan/feature/products`.
- Trying to enable a higher-tier feature → landing on the restriction banner (see [[plan-features-warning-banners]]).
- Submitting an AJAX form that exceeds quota → the SPA receives a JSON redirect payload and navigates client-side.

## Settings & fields

### Redirect contract (browser vs AJAX)

| Request type | Middleware response |
|--------------|--------------------|
| **Direct browser** | HTTP **302 redirect** to `/admin/plan/feature/{feature_mapping}` |
| **AJAX** | JSON `{"status": "success", "redirect": "/admin/plan/feature/{feature_mapping}"}` — the SPA navigates accordingly |

The same gating logic runs on both code paths — only the response shape differs.

### Mapping aliases (pack mapping → app mapping)

Some pack mappings are aliased before being handed to the app activation step:

| Public pack mapping | Internal app mapping |
|---------------------|----------------------|
| `shipping_payment_sync` | `omniship` |
| `cloudio_ai` | `cloudio` |
| `campaign.channels.messenger_message` | `campaigns` |
| `campaign.channels.email` | `campaigns` |
| `viber_messages` | `campaigns` |

This aliasing is **purely internal** — the public mapping is what appears in the URL `/admin/plan/feature/{mapping}` and on the pack rows. The alias only matters server-side so the right app's subscription handler is called when checkout completes.

### Demo plan resolves to Enterprise (verify)

When the platform resolves the merchant's effective plan for feature lookups:

- If `site('plan') == 'cc-demo'`, the resolver returns `config('plan.demo_restrictions_map')` = **`'enterprise'`**.
- Otherwise it returns the site's actual plan mapping.

So all feature-value lookups for demo sites resolve against the Enterprise plan's limits. The plan badge in the profile still says *Demo*, but every plan gate behaves as if the merchant were on Enterprise. Purely for evaluation / preview sites. (See [[plan-features-restrictions-limits]].)

## Business rules

### Plan-middleware redirects to this screen on quota-exhaustion

The admin-panel middleware checks each request against the feature-mapping table (config-driven). If the URL the merchant is requesting requires a feature their plan doesn't allow (or whose quota is exhausted), the middleware returns a redirect to `/admin/plan/feature/{feature_mapping}`. The merchant lands on this screen with the feature pre-selected based on what they tried to do — see [[plan-features-warning-banners]] for the message they see.

### AJAX gate returns JSON, not 302

For AJAX requests, the middleware **does not** issue a 302 — it returns `{"status": "success", "redirect": "/admin/plan/feature/<mapping>"}` so the SPA can navigate without breaking the request flow. Direct browser requests get a real 302. The gating logic is the same on both paths; only the response shape differs.

### Mapping aliases route pack → app subscription

When the merchant completes checkout for a pack with an aliased mapping:

1. The new subscription is created with `model_type = cloudcart_feature` and the **public** mapping as its key.
2. A post-subscription hook resolves the alias (e.g. `shipping_payment_sync` → `omniship`) and activates the underlying **app** subscription as well.
3. Both subscriptions (the plan-feature one + the app one) appear on [[subscriptions]] linked to the same checkout.

The merchant sees ONE pack on the pack list and ONE pack-purchase confirmation, but TWO subscription records — the second is the app activation that the plan-feature pack unlocks. See [[plan-features-subscription-lifecycle]] for the broader provisioning flow.

### Profile dropdown bypasses this redirect path

The "Choose plan" entry in the profile dropdown goes to [[plans]] (the catalog) — NOT to a per-feature URL. The feature-pack screen is reached **exclusively** through plan-gate redirects (the middleware) and warning links inside over-limit toasts / banners. There is no "browse feature packs" UI for merchants and no direct path into `/admin/plan/feature/{mapping}` from a regular menu.

### Restriction-by-plan banner uses a config-table lookup

The "Plans that support this functionality" banner pulls the list of allowed plans from the `plan.restrict.feature_purchase.{feature_mapping}` config entry. Plans listed are filtered to active + with details (so soft-deleted or country-restricted plans don't show). The merchant clicks through to one of them, which routes to [[plans-purchase]]. See [[plan-features-warning-banners]] for the banner UI and [[plan-features-restrictions-limits]] for the gate.

### Feature packs surface only via the middleware redirect path

This is intentional: packs are an **"exit ramp"**, not a browsable catalog. The middleware redirect is the ONLY way a merchant naturally encounters the per-feature pack URL. The modern Vue grid at [[plan-features-modern-vue-grid]] is the alternative browseable surface — it lists all features in cards — but the per-feature URL itself is reached only via gate.

## Related

- [[plan-features]] — hub.
- [[plan-features-warning-banners]] — what the merchant sees AFTER the redirect lands them here.
- [[plan-features-pack-list]] — pack list rendered on the redirect target.
- [[plan-features-subscription-lifecycle]] — pack → app activation hooks for aliased mappings.
- [[plan-features-restrictions-limits]] — `plan.restrict.feature_purchase` config that drives the restriction banner.
- [[plan-features-modern-vue-grid]] — the alternative browseable card surface.
- [[plan-gates]] — gating concept.
- [[subscriptions]] — where the resulting subscription(s) appear.

## Open questions

None.
