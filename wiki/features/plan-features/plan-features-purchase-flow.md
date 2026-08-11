---
type: feature
nav_path: "Plan → Feature pack → Purchase flow"
route_name: admin.feature.purchase
route_path: /admin/plan/feature/{id}/purchase/{value?}
aliases: ["Buy feature pack action", "Feature pack purchase action", "Cart re-seed", "Side-panel close button", "Browser back close"]
tags: [plans, plan-feature, feature-pack, checkout, purchase]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plan-features]]. See the hub for the other aspects (warning banners, pack list, restrictions & limits, subscription lifecycle, modern Vue grid, middleware mappings).

# Plan features — purchase flow

## Purpose

The **purchase action** at `/admin/plan/feature/{id}/purchase/{value?}` is what each *Buy* button on [[plan-features-pack-list]] triggers. It is NOT a screen the merchant browses — it's a server action that validates the purchase, seeds the checkout cart with the chosen pack + quantity, and redirects to the standard admin checkout. The screen chrome around it is a **side panel** with a close (×) button that returns the merchant to where they came from via *browser back*.

## Where to find it

- Triggered only by clicking *Buy* on a row in [[plan-features-pack-list]] (or on a card on [[plan-features-modern-vue-grid]]).
- Not deep-linkable for browsing — the URL only makes sense as the target of a Buy click.

URL pattern: `/admin/plan/feature/{id}/purchase/{value?}`.

## What the merchant can do here

- Confirm a pack purchase by clicking *Buy* on a pack row.
- Get redirected to `/admin/checkout` with the pack already in the cart.
- Close the side panel via the (×) button to return to the screen they were on when they hit the limit.

## Settings & fields

### Purchase-action parameters

| Parameter | What it represents |
|-----------|--------------------|
| `{id}` | The pack ID being purchased |
| `{value}` (optional) | The quantity, when the pack supports dynamic pricing (e.g. `2000` for *2000 products*) |

### Outcomes

| Outcome | Behaviour |
|---------|-----------|
| **Success** | Cart re-seeded with the pack + redirect to `/admin/checkout` |
| **Max-value exceeded** | Redirect back to the feature page with an inline error: *"Your package allows **<max_value>** <postfix>"* (e.g. *"Your package allows **100000** products"*) — see [[plan-features-restrictions-limits]] |
| **Feature restricted by plan** | Restriction banner shown instead of pack list — Buy never reached. See [[plan-features-warning-banners]] |
| **`enable_feature_pack` OFF on plan** | Pack list empty — Buy never reached. See [[plan-features-restrictions-limits]] |

### Side-panel layout (same as plan purchase)

| Element | Behaviour |
|---------|-----------|
| **Standard chrome** | Hidden — no sidebar, no topbar, no user-account menu while the panel is open |
| **Header** | Feature name + a close (×) button |
| **Close (×) button** | Runs `window.history.go(-1)` — returns the merchant to the screen they were on when they hit the limit (NOT to a fixed *home* URL) |

The side-panel pattern is identical to the plan-purchase flow ([[plans-purchase]]).

## Business rules

### Cart is reset on every Buy click

When *Buy* is clicked, the checkout cart is **cleared first**, then seeded with the chosen pack. The merchant can't accumulate multiple packs across multiple clicks — every click replaces the cart. To buy several packs, the merchant must complete each checkout one at a time.

### Cannot combine multiple packs in one checkout

By extension of the cart-reset rule, only **ONE pack** is in the cart at any time. There's no multi-select on [[plan-features-pack-list]]. A merchant who wants to buy *+100 products* AND *+5 GB storage* must complete two separate checkouts.

### Max-value cap is enforced before the redirect

Before adding the pack to the cart, the platform computes:

1. The plan's base value for the feature.
2. The merchant's already-purchased active subscriptions for the same feature.
3. The pack's `value` (or the dynamic `{value}` URL param).

If `(1) + (2) + (3) > max_value`, the *Buy* click is rejected and the merchant stays on the feature screen with an error toast using the `plan.plan_limit` localised string. See [[plan-features-restrictions-limits]] for the full max-value logic.

### Close button preserves task context

The (×) button uses `window.history.go(-1)` — so a merchant who hit the cap while editing a product on [[products-products]] returns to that product, not to a generic dashboard. This is intentional and consistent with [[plans-purchase]].

### Profile dropdown does NOT link to this action

The *Choose plan* entry in the profile dropdown routes to the plan catalog at [[plans]] — NOT to a per-feature pack screen. The pack purchase flow is reached **exclusively** through plan-gate redirects, warning links, and *Buy feature* / *Upgrade* clicks on [[plan-features-modern-vue-grid]]. There is no "browse feature packs" UI.

### Feature packs are an "exit ramp", not a browsable catalog

This is intentional: packs surface to the merchant only when they hit a limit. There is no aggregated *browse all packs* page anywhere in the admin. To see all available packs the merchant must either hit the corresponding limit on each feature, or ask their account manager.

## Related

- [[plan-features]] — hub.
- [[plan-features-pack-list]] — the *Buy* button this action is wired to.
- [[plan-features-warning-banners]] — what's shown when the action is blocked.
- [[plan-features-restrictions-limits]] — the `max_value` cap enforced before redirect.
- [[plan-features-subscription-lifecycle]] — what happens AFTER `/admin/checkout` succeeds (subscription provisioning + cache flush).
- [[plans-purchase]] — sibling plan-purchase flow with the same side-panel layout.
- [[billing-cards]] — saved cards used during the redirect-to-checkout step.

## Open questions

None.
