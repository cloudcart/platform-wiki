---
type: concept
nav_path: "Concept → Merchant subscription lifecycle → Support flow (where merchants self-serve)"
aliases: ["Subscription support flow", "Where do I see my subscription", "Profile dropdown billing entries", "Owner-only profile entries", "Subscription self-serve URLs", "12 merchant subscription questions", "Subscription support cheat sheet"]
tags: [billing, subscription, support, navigation, lifecycle, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[merchant-subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, expiration, cancellation, feature packs, payment methods, invoices).

# Subscription support flow (where merchants self-serve)

## Definition

A support-agent cheat sheet for "the merchant asked me something about their CloudCart subscription — where do I send them?". Every paid subscription surface is reached via the **top-right profile avatar dropdown** (owner-only entries) or a paywall redirect from an over-limit action. This page maps each of the 12 most-asked merchant questions to the exact URL + button label + screen-level wiki page so the support agent can guide the merchant precisely.

## Scope

What this page covers:

- The owner-only profile-dropdown entries + their exact URLs.
- The 12 most-asked merchant questions with one-line "where to send them" answers + cross-references to the in-depth aspect pages.
- Visibility rules (owner vs staff / moderator; partner-network merchants; LTA-contract merchants; DE-invoiced merchants).

What it does NOT cover:

- The mechanics of each surface — those live on the screen-level wiki pages and on the focused aspect pages of this cluster.
- The state machine + transition rules — see [[subscription-states]] + [[subscription-lifecycle]].

## Contrasts

- **Owner vs staff / moderator** — ONLY the store owner sees the billing entries in the profile dropdown. Staff / moderator accounts see only the current plan badge — none of *Choose plan / My subscriptions / Billing / Cards / Invoices / Offers / Merchant profile*. They must ask the store owner for anything subscription-related.
- **Partner-network merchants (e.g., UniCredit, `reseller_id = 157`)** — see ONLY partner-only plans (`type = unicredit`) on [[plans]]. The *Choose plan* entry is HIDDEN from their dropdown.
- **LTA-contract merchants** — are redirected from `/admin/plan` to their contract page (`/admin/contracts/{unique_id}`). They cannot shop the catalog or cancel subscriptions from the UI (Cancel rejects with *"This subscription has a related contract..."*). See [[subscription-cancellation]].
- **DE-invoiced merchants** — see only DE + global plans, with the free Start Up plan rebranded as *14-Tage-Test (Starter)*.

## Where it applies

### The owner-only profile dropdown — six paid-subscription entries

All gated on `serverSettings('user.is_owner')`:

| Dropdown entry | Routes to | What it shows |
|----------------|-----------|---------------|
| **Choose plan** | `/admin/plans` ([[plans]]) | Plan catalog with the period switcher + Choose buttons. |
| **My subscriptions** | `/admin/details/subscriptions` ([[subscriptions]]) | 9-column list of every paid recurring item — plan, packs, apps, services, themes. |
| **Billing / Cards** | `/admin/details/billing` ([[details-billing]]) | Transaction history (charge-by-charge); the *Payment method* button in the header opens the [[billing-cards|card panel]]. |
| **Invoices** | `/admin/details/invoices` | List of issued invoice PDFs with Download links. See [[subscription-invoices]]. |
| **Offers** | `/admin/offers` | Active commercial offers the account has received. |
| **Merchant profile** | merchant profile screen | Profile / preferences. |

### The 12 most-asked merchant questions — cheat sheet

The numbering matches the canonical 12 questions covered across the cluster.

1. **Where do I see my current subscription?** → Profile → **My subscriptions** → [[subscriptions]] (`/admin/details/subscriptions`). Legacy `/admin/subscriptions` redirects. Per-row drill-in opens [[subscriptions-detail]] + [[subscriptions-transactions]].

2. **How do I upgrade my plan?** → Profile → **Choose plan** → [[plans]] (`/admin/plans`). Click *Choose `{plan name}`* → [[plan-details]] side panel → *Proceed to checkout*. See [[subscription-renewal-retry]] for renewal mechanics.

3. **How do I add a feature pack?** → [[plan-features]] (`/admin/plan-features`), OR auto-redirect to `/admin/plan/feature/{key}` on paywall hit. See [[subscription-feature-packs]].

4. **How do I buy a paid app / service / theme?** → [[plan-apps]] (`/admin/plan-apps`); [[plan-services]] (`/admin/plan-services`); [[design-themes]].

5. **Where do I see my payment methods?** → Profile → **Billing / Cards** → [[details-billing]]; *Payment method* button opens [[billing-cards]] (also from [[billing-invoicing]] pencil or any Checkout panel). See [[subscription-payment-methods]].

6. **Where do I see my invoices?** → [[billing-invoicing]] (company info printed on invoices); `/admin/details/invoices` (issued PDFs); [[details-billing]] (transaction history + Download links). See [[subscription-invoices]].

7. **How does renewal work?** → Daily pipeline + `subscription.upcoming.payment` webhook 7 days ahead + manual **Renew** on [[subscriptions]]. See [[subscription-renewal-retry]].

8. **What happens if my card fails?** → 5-attempt retry with 2 / 3 / 4 / 5 day gaps; 1-month grace; [[expired-subscription]] takeover on day ~30 for plan subscriptions. See [[subscription-renewal-retry]] + [[subscription-expiration]].

9. **How do I cancel?** → [[subscriptions]] → **Cancel**. Soft — access kept until `next_billing_date`. No proration. See [[subscription-cancellation]].

10. **What happens when my plan expires?** → [[expired-subscription]] takeover; allowlist of accessible screens; recovery via Renew or new plan. See [[subscription-expiration]].

11. **How do I switch plans?** → [[plans]] → *Choose `{plan name}`* on the target card. No proration — full new term; feature packs survive — see [[subscription-feature-packs]]. LTA merchants cannot switch from the UI.

12. **Plan vs Feature pack vs App vs Service vs Theme?** → All five share the same lifecycle; differ in `model_type`, purchase entry, and Cancel side effects. See [[subscription-feature-packs]] + [[subscription-cancellation]].

### Visibility / carve-out summary

| Merchant type | What changes |
|---------------|--------------|
| **Staff / moderator** | No billing entries in the profile dropdown. Cannot reach any `/admin/details/*` or `/admin/plan*` URL. |
| **Partner-network (e.g., UniCredit)** | *Choose plan* hidden. [[plans]] shows only partner plans (`type = unicredit`). |
| **LTA-contract** | `/admin/plan` redirects to the contract. Cancel rejected on [[subscriptions]]. Auto-renewal excluded — see [[subscription-payment-methods]]. |
| **DE-invoiced** | [[plans]] shows DE + global plans only. Free Start Up rebranded as *14-Tage-Test (Starter)*. |
| **Free Start Up** | Subject to free-plan-inactivity expiry (30 days BG / 14 days DE) — see [[subscription-expiration]]. Auto-reactivation on login. |

### Screens accessible during the [[expired-subscription]] takeover

When the plan subscription is Expired, the merchant can ONLY reach: [[subscriptions]], [[details-billing]], [[billing-cards]], [[billing-invoicing]], `/admin/details/invoices`, `/admin/offers`, `/admin/details/contracts`, `/admin/settings/*`, `/admin/payment-providers/*`, the takeover itself, and sign-in / logout. Everything else (products, orders, customers, marketing, analytics, dashboard, apps) bounces back to the takeover. See [[subscription-expiration]] for the takeover mechanics.

## Related

- [[merchant-subscription-lifecycle]] — hub.
- [[subscription-states]] — the badge the merchant sees on each [[subscriptions]] row.
- [[subscription-renewal-retry]] — what to tell a merchant about renewals + the manual Renew button.
- [[subscription-expiration]] — what to tell an Expired-plan merchant.
- [[subscription-cancellation]] — what to tell a merchant who wants to cancel.
- [[subscription-feature-packs]] — what to tell a merchant who hit a feature limit.
- [[subscription-payment-methods]] — what to tell a merchant whose card is expiring / failing.
- [[subscription-invoices]] — what to tell a merchant who needs an invoice PDF.
- [[subscriptions]] / [[subscriptions-detail]] / [[subscriptions-transactions]] — the My subscriptions surfaces.
- [[plans]] / [[plan-details]] / [[plans-purchase]] — the plan catalog + checkout.
- [[plan-features]] / [[plan-feature]] — the feature-pack surfaces.
- [[plan-apps]] / [[plan-services]] / [[design-themes]] — the other purchase entry points.
- [[billing-cards]] / [[billing-invoicing]] / [[details-billing]] — the billing area.
- [[expired-subscription]] — the takeover screen with the full allowlist.

## Open Questions

None.
