---
type: feature
nav_path: "Profile → Choose plan"
route_name: plans
route_path: /admin/plans
aliases: ["Plans", "Choose plan", "Pricing", "Tariff plans", "Plan list", "Plans catalog", "Plan picker", "Тарифни планове", "Изберете план", "Цени", "Планове"]
tags: [plans, pricing, billing, subscription]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---
# Plans

## Purpose

The **Plans** screen is the main pricing / catalog page in the admin panel. It shows every CloudCart SaaS plan available to the merchant's account (Free, Starter, Pro, Business, Enterprise, etc.) as side-by-side price cards, followed by a feature-comparison matrix that lines up each plan's limits against every other plan. From here the merchant chooses a plan to purchase or upgrade to — clicking a price card takes them into the [[plans-purchase]] flow. The merchant's *current* plan is marked **Current plan** (greyed) so they can see where they stand.

The plans list is **country / issuer-company aware** and **partner-network aware** — a German merchant sees DE plans, a Bulgarian merchant sees BG plans, UniCredit-onboarded merchants see a partner-only catalog. Long-term-agreement (LTA) merchants don't see the catalog at all — the screen redirects to their contract.

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[plans-catalog-display]] — visual layout: price card, per-month rate, billing-cycle tab switcher, **POPULAR** ribbon, **Unicorn / Custom** card, button states, feature-comparison matrix accordions, display formatters (bool / storage / fee / int / Unlimited).
- [[plans-country-partner-filter]] — how the catalog is filtered by invoicing country (issuer-company), the UniCredit partner-only catalog, the DE **14-Tage-Test (Starter)** rebrand of the global Start Up free plan.
- [[plans-contract-lta-override]] — what happens when the merchant has an active long-term-agreement contract; redirect to contract details + LTA preview component.
- [[plans-free-expiry]] — Free Start Up plan expiry rules (30-day BG / 14-day DE thresholds), two-tier warning notifications, the path to [[expired-subscription]].
- [[plans-downgrade-behavior]] — downgrade flow goes through the same Upgrade button; no proration, over-quota records preserved, lower gates take effect immediately.
- [[plans-cache-and-demo]] — plan-feature value caching (1-week TTL, tagged `plan`, flushed on plan / subscription change) and the `cc-demo` slug → enterprise-tier mapping.

## Where to find it

- **Profile dropdown** (top-right) → **Choose plan** — visible only to the **Store owner** (staff roles do not see this link).
- **Profile dropdown** → the **Plan** badge + **Upgrade** button (owner only) — links to the same URL.
- Many in-app upsell prompts also link here: order-amount limit counters, [[expired-subscription]], the sandbox banner, plan-feature gate errors per [[plan-gates]].

URL: `/admin/plans` (no slug). `/admin/plan` redirects to `/admin/plans`.

## What the merchant can do here

- **Browse every plan** available for their country / partner network, side-by-side, with prices for each billing cycle.
- **Switch the headline billing cycle** via the **Monthly / Annually / Biennially** tab bar — all cards re-price live; default tab is *Annually*.
- **Compare plans feature-by-feature** in the comparison matrix below the cards (grouped accordions: Resources, Branding, Reports, Support, Synchronizations, Themes, Subscriptions, Domains).
- **Click a plan card** to open the [[plan-details]] side-panel with the selected cycle preselected, then continue to [[plans-purchase]] checkout. (DE merchants skip the side-panel and open checkout directly.)
- **Contact CloudCart sales** via the *Unicorn / Custom* card (non-DE only).

## What the merchant cannot do here

- **Edit plans, prices, limits, or features** — the catalog is centrally managed by CloudCart staff.
- **See plans not available for their country / partner network** — see [[plans-country-partner-filter]].
- **Choose a plan when locked into an LTA contract** — the screen redirects to the contract page. See [[plans-contract-lta-override]].
- **Compare across currencies** — each card shows prices in the merchant's country currency. No currency picker on this screen.

## Settings & fields

This is a read-only catalog screen — no input fields. The merchant sees per plan:

| Field shown | What it represents |
|-------------|--------------------|
| **Plan name** | Display label (*Start Up*, *Pro*, *Business*, *Enterprise*, etc.) — localised |
| **Headline per-month price** | The per-month equivalent for the selected billing cycle |
| **Full-period total** | The actual cycle total (e.g. *199.00 EUR / year*) shown below the headline |
| **Billing-cycle savings** | Parenthetical *(save X.XX CURRENCY)* on longer cycles when cheaper than monthly |
| **VAT disclaimer** | *"The quoted prices are exclusive of VAT"* under every card |
| **CTA button** | *Choose `{plan name}`* (other plans) or *Current plan* (greyed, on the merchant's existing plan) |
| **Feature comparison matrix** | Grouped feature list × plans grid, with bool / storage / fee / int formatting per feature |

For full display rules + formatting (incl. how `null` and `0` render, hidden feature × plan combinations, accordion behaviour, period switcher defaults), see [[plans-catalog-display]].

## Business rules

The core business rules — country / partner filtering, LTA redirect, free-plan expiry, downgrade semantics, feature-cache flushing — live in dedicated aspect pages so each rule can be cited precisely:

- **Country / issuer-company catalog filtering** + DE Starter rebrand + UniCredit partner catalog — see [[plans-country-partner-filter]].
- **LTA contract takes over the screen** — see [[plans-contract-lta-override]].
- **Free Start Up plan expiry** (30-day BG / 14-day DE) + warning notification tiers — see [[plans-free-expiry]].
- **Downgrade does not prorate or clean up data**; over-quota records are preserved but new creates are blocked immediately — see [[plans-downgrade-behavior]].
- **Plan-feature lookups are cached for one week** + flushed on any plan / subscription change; `cc-demo` slug uses enterprise restrictions — see [[plans-cache-and-demo]].

### Visibility of the "Choose plan" link in the profile dropdown

The link is gated:

- The logged-in admin must be the **Store owner**. Other staff roles cannot see it.
- The site must NOT be on a partner reseller (UniCredit-onboarded sites don't see the link — they negotiate plans through the partner). See [[plans-country-partner-filter]].

### Plan sort order in the catalog

Plans are sorted **by lowest billing-cycle price ascending** — the cheapest plan appears first. Plans without any active billing-cycle variants are filtered out entirely (this is how CloudCart soft-disables a plan — remove all price-detail rows and it becomes invisible without a hard delete).

### CTA opens the side-panel on most countries, the checkout panel on DE

Clicking the card or matrix-row CTA opens the [[plan-details]] side-panel using the shared `PlanPanel` component (see [[plans-purchase]] for the panel breakdown). The URL stays on `/admin/plans`. On Germany-based merchants the button skips the details panel and opens the checkout panel directly with the plan + month pre-seeded.

## Related

- [[plans-purchase]] — the per-plan purchase flow this screen links to via each card CTA.
- [[plan-details]] — the per-plan details side-panel that opens on card click.
- [[plan-features]] — per-feature purchase flow (buying additional quota above the plan limit).
- [[plan-gates]] — concept page on how plan limits and feature restrictions are enforced across the admin panel.
- [[subscriptions]] — list of the merchant's active subscriptions, including the plan-detail subscription created on purchase.
- [[billing-cards]] — saved payment cards used during plan checkout.
- [[expired-subscription]] — screen merchants are redirected to when their subscription is expired / past due.
- [[contracts]] — long-term agreement (LTA) plans negotiated directly with CloudCart.
- [[details-billing]] — billing details + invoicing setup.
- [[orders-subscriptions]] — the merchant's own customer subscriptions (different concept).
- [[merchant-subscription-lifecycle]] — merchant-support hub answering "how do I upgrade my plan / switch billing cycle / what happens to my packs when I switch?".

## Open questions

(All resolved.)
