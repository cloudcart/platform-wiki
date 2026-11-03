---
type: feature
nav_path: "Profile → Choose plan → {Plan} → Purchase → Recommended add-ons"
route_name: admin.plan.purchase
route_path: /admin/plan/{mapping}/purchase
aliases: ["Recommended services", "Recommended apps", "Plan add-ons", "Bundle add-ons", "Plan recommended block", "Препоръчани услуги", "Препоръчани приложения", "Препоръки към план"]
tags: [plans, purchase, recommendations, services, apps, upsell]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans-purchase]]. See the hub for the other aspects (billing cycle, plan detail view, checkout panel, business rules, subscription outcomes, discount codes).

# Plans purchase — recommended add-ons

## Purpose

Two optional blocks on the purchase screen let the merchant bundle additional purchases into the same checkout transaction: **Recommended services** (themed setup help, custom development, one-off integrations) and **Recommended apps** (paid subscriptions for individual CloudCart apps — newsletter, ERP integrations, etc.). Each ticked add-on becomes its own line on the resulting invoice and its own subscription, paid for in a single transaction with the plan.

## Where to find it

Inside the purchase flow at `/admin/plan/{mapping}/purchase`, directly below the billing-cycle radio block. Both blocks are conditional — they only render when CloudCart's central marketing layer has flagged at least one service or app as recommended for this merchant **and** the merchant is on the default issuer company (BG).

If nothing is recommended for the merchant, both blocks are hidden and the screen shows only the billing-cycle picker + totals.

## What the merchant can do here

- Tick / untick individual recommended services to add them to the same cart.
- Tick / untick individual recommended apps to add them to the same cart.
- Read each add-on's full description via *Show more* / *Show less* (Markdown-rendered).
- See the running total update live as add-ons are toggled — no page refresh.

## Settings & fields

### Recommended services block

| Field / Control | What it does | Default | Notes |
|-----------------|--------------|---------|-------|
| **Service checkbox** | Adds the service to the cart | Unchecked | Adds the service price to the running subtotal client-side. |
| **Service name** | Translated service title | — | Localised per merchant language. |
| **Price + period** | Right-aligned per row | — | Format e.g. `50.00 EUR / month`. |
| **Service description** | Markdown body below the row | Collapsed | Rendered through `EllipsisWithMarkdown` with *Show more* / *Show less* toggle. |

### Recommended applications block

| Field / Control | What it does | Default | Notes |
|-----------------|--------------|---------|-------|
| **App checkbox** | Adds the app subscription to the cart | Unchecked | Adds the app price to the running subtotal client-side. |
| **App name** | Translated app title (`app.name` label key) | — | The value reference is `applications[app.key]`. |
| **Price + period** | Right-aligned per row | — | Same format as services. |
| **App description** | Markdown body below the row | Collapsed | Same `EllipsisWithMarkdown` component as services. |

### Block-level visibility flags

| Condition | Effect |
|-----------|--------|
| Merchant has zero recommended services in active-period window | Recommended services block hidden entirely. |
| Merchant has zero recommended apps in active-period window | Recommended apps block hidden entirely. |
| Merchant `issuer_company` is NOT the default (BG) | BOTH blocks hidden regardless of recommendations. |
| Merchant `isGermanyBased` | The whole PlanPanel is bypassed — the checkout panel opens directly (the merchant never sees add-ons on this path). |

## Business rules

### Recommendations are centrally-flagged

The *Recommended services* and *Recommended apps* lists are pulled from CloudCart's central catalog of items marked as `recommended` and currently active in their active-period window. The merchant doesn't choose what's recommended — CloudCart's marketing layer decides per audience.

### Bundling boosts the single checkout

The blocks exist so the merchant can buy plan + add-ons in one transaction instead of two separate checkouts later. Each ticked item gets its own line on the resulting invoice and becomes its own subscription — they're individually billable, just paid for in one go.

### German-based merchants bypass this UI

When the merchant is `isGermanyBased`, clicking *Choose* on a plan card sets `planGermany` and opens the Checkout panel directly ~200 ms later — the PlanPanel (and therefore the recommended blocks) is never rendered. DE merchants on this path cannot bundle CloudCart-recommended services or apps with their plan purchase.

### Cart-shape entries

As checkboxes are toggled, the local `buy` state map grows / shrinks:

- `buy['service-<id>'] = { type: 'cloudcart_service', mapping: <service_id> }` — service ticked.
- `buy['app-<key>'] = { type: 'cloudcart_app', mapping: <app_key> }` — app ticked.

Untick removes the entry (`null`). The Proceed-to-Checkout button filters out null values before passing the array onward — see [[plans-purchase-checkout-panel]] for what happens next.

### Add-ons survive cart reset

When the merchant submits the purchase form, the bulk-cart endpoint clears any existing cart contents first, then adds the selected plan + ticked services + ticked apps fresh. So a returning merchant cannot accidentally combine items left over from a previous flow with the new add-on selection — see [[plans-purchase-business-rules]] for the full cart-reset rule.

## Related

- [[plans-purchase]] — hub.
- [[plans-purchase-billing-cycle]] — the variant picker the merchant sees above this block.
- [[plans-purchase-checkout-panel]] — where ticked add-ons appear as cart-item lines.
- [[plan-services]] — directory of all purchasable CloudCart services (and feature-specific service flows).
- [[plan-apps]] — directory of all paid CloudCart apps.
- [[subscriptions]] — once purchased, each add-on becomes its own subscription record alongside the plan.

## Open questions

None.
