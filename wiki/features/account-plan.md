---
type: feature
nav_path: "Plan"
route_name: plan
route_path: /admin/plan
aliases: ["Plan area", "Plans area", "Pricing area"]
tags: [plan, hub]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 5
---
# Plan

## Purpose

Hub page for the **Plan** area of the CloudCart admin panel. Lists the screens that live under this section: the pick-a-plan catalog, the per-feature buy screen, the recommended apps tab, and the recommended services tab.

## Where to find it

Plan (top-level sidebar entry, owner-only) → opens to the same screens as the *Profile → Choose plan* dropdown link.

## What the merchant can do here

- Navigate to any sub-screen listed in `## Related`.

## Settings & fields

Not applicable — this is a navigation hub, not a screen with its own settings.

## Business rules

### Auto-redirect to the catalog

`/admin/plan` does NOT render its own UI — the router immediately redirects to `/admin/plans` (the [[plans]] catalog). The four tab labels (*Plans*, *Apps*, *Feature packages*, *Services*) are then shown at the top of every sub-screen.

### Owner-only visibility

The sidebar / profile-dropdown entry for this area is hidden for non-owner staff users. Staff with restricted roles can see the *current plan* badge in their profile dropdown but cannot navigate into this hub.

### Partner-network sites do not see the Plan link

Sites flagged with a partner reseller (e.g. UniCredit-onboarded merchants, `reseller_id = 157`) do not see this hub at all — their plan is governed by the partner contract, not by the public catalog. Visiting the URL on those sites also redirects them straight to [[plans]] which then shows only their partner catalog.

### LTA-contract override

If the merchant's site has an active long-term agreement contract, the catalog and the tabs are bypassed — the merchant is redirected to the contract details page instead. See [[plans]] for details.

## Related

- [[plans]] — pick-a-plan catalog (the default tab).
- [[plan-apps]] — paid CloudCart apps available as add-ons.
- [[plan-features]] — feature-pack cards for extending plan limits.
- [[plan-services]] — recommended professional services (one-off / managed).
- [[plan-feature]] — per-feature buy screen (the funnel target when a plan gate is hit).
- [[plans-purchase]] — the per-plan purchase flow.
- [[plan-gates]] — concept page on how plan limits + feature restrictions are enforced.
- [[subscriptions]] — list of the merchant's active CloudCart subscriptions.

## How it works (verified against backend)

### Four tabs across the Plan area

The hub renders a tabbed wrapper with these four entries (visible to the merchant as buttons at the top of each sub-screen):

1. **Plans** — [[plans]] — the side-by-side plan cards + feature-comparison matrix.
2. **Apps** — [[plan-apps]] — the paid-apps grid available to add to the plan.
3. **Feature packages** — [[plan-features]] — the cards for buying additional quota on individual features (e.g. +1000 products).
4. **Services** — [[plan-services]] — the cards for buying recommended professional services.

The current tab is determined by the URL — `/admin/plans`, `/admin/plan-apps`, `/admin/plan-features`, `/admin/plan-services` respectively. The four URLs share the same outer container (header + tab bar) and only swap the body.

### Title changes with the tab

The page title (in the header bar) is set per active tab: *Pick a plan*, *Apps*, *Plan features*, *Plan services*. The icon is always the calendar-star icon.

### Hub is just routing — no extra data

The hub itself loads no data; it's a thin wrapper that mounts whichever child component matches the URL. Plan / app / feature / service data is loaded by the children when they mount.

## Modals & sub-flows in the Plan area

The Plan area's four tabs ([[plans]], [[plan-apps]], [[plan-features]], [[plan-services]]) share a common set of overlay surfaces that ANY tab can trigger:

### `PlanPanel` (shared plans side-panel)

Opens from any [[plan-features]] *No pack available* path (via the shared `useSharedPlanPanelState` composable) AND from clicking *View prices* on a feature restriction banner. Renders the full plans catalog + comparison matrix as a side modal (size `xl`/`xll`), with optional `<slot name="message">` for an upgrade-context info banner at the top. Inside the panel, choosing a plan opens the same `Checkout` side-panel as the standalone flows.

### `Checkout` (shared checkout side-panel)

The single component used for ALL purchases initiated from any tab in the Plan area — plan purchase, feature-pack purchase, service purchase, app purchase. See [[plans-purchase]]#Checkout-side-panel-`CheckoutPanel` for the full layout. The Plan area's tabs each open this panel via slightly different prop shapes (`record` vs `records` vs `cartId`).

### `PlanFeature` panel ([[plan-feature]])

Opens from a *Buy feature* / *Upgrade* button on a [[plan-features]] card. Renders the pack table OR the feature-restricted banner (see [[plan-feature]] for the full layout).

### Book-a-meeting flow (Custom / Unicorn card)

Clicking the **Custom**-tier card (Unicorn) on [[plans]] opens the **Book a meeting** sales flow (`useSharedBookMeeting.handleMeetOpen`) instead of checkout. This is the sales-contact path for enterprise / custom-tier deals. Not shown on Germany-based merchants (different partner-sales path).

## Open questions

(All resolved.)
