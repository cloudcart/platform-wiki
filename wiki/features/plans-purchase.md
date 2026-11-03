---
type: feature
nav_path: "Profile → Choose plan → {Plan} → Purchase"
route_name: admin.plan.purchase
route_path: /admin/plan/{mapping}/purchase
aliases: ["Plan purchase", "Plan checkout", "Upgrade plan", "Buy plan", "Plan details", "Plan detail", "Закупуване на план", "Промяна на план", "Детайли на плана", "Покупка на план"]
tags: [plans, pricing, billing, subscription, checkout, smarty]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---

# Plan purchase

## Purpose

The **plan-purchase** flow is the side-panel checkout the merchant lands on after picking a plan from the [[plans]] catalog. It lets them choose a **billing cycle** (monthly / yearly / 2-year), optionally bundle **recommended services** + **recommended apps** into the same transaction, and proceed to the Checkout side-panel where they pay for everything in one invoice. A separate read-only URL — the **plan detail** page — shows the full feature breakdown for a single plan (no purchase form) and is accessible from the *Plan* badge in the profile dropdown.

Both routes share the same Smarty templating + currency / VAT formatting, so they're documented under this one hub. The hub catalogues the screen-level orientation + URL patterns; each aspect page below covers one well-scoped slice.

## Where to find it

- **From [[plans]]** — clicking *Upgrade now* on any plan card opens the purchase flow for that plan at `/admin/plan/{mapping}/purchase`.
- **From the profile dropdown** — the *Plan* badge (*"Plan: <current-plan-name>"*) links to the plan-detail page at `/admin/plan/{mapping}` — see [[plans-purchase-plan-detail-view]].
- **From the catalog's *Current plan* button** — clicking *Current plan* on the merchant's own card also routes into the purchase flow (lets them switch billing cycle without changing tier).

URL patterns:

- Purchase flow: `/admin/plan/{mapping}/purchase` — e.g. `/admin/plan/cc-pro/purchase`, `/admin/plan/business/purchase`, `/admin/plan/startup/purchase`.
- Read-only detail: `/admin/plan/{mapping}` — same mapping, no `/purchase` suffix.

The `{mapping}` segment is the plan's URL slug — stable identifiers: `startup`, `basic`, `cc-pro`, `business`, `enterprise`, `unicorn`.

## What the merchant can do here

- Pick a billing-cycle variant (radio) — see [[plans-purchase-billing-cycle]].
- Tick optional recommended services / apps — see [[plans-purchase-recommended-addons]].
- View the read-only feature breakdown of a plan — see [[plans-purchase-plan-detail-view]].
- Pay the cart total + 3DS challenge handling — see [[plans-purchase-checkout-panel]].
- Apply discount / promo codes — see [[plans-purchase-discount-codes]].

What the merchant **cannot** do here:

- Combine multiple plans in one cart (radio, not checkbox — single `plan_details` ID per cart).
- Choose a billing cycle that isn't published.
- Edit prices, VAT, or currency.
- Buy a plan with no active billing variants (the URL returns 404).
- Visit the purchase flow while on an active **LTA contract** (the catalog redirects them to the contract page — see [[contracts]]).

## Sub-pages (in this cluster)

This feature is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[plans-purchase-billing-cycle]] — the billing-variant radio (monthly / yearly / 2-year), pre-selected middle option, live total computation, no-proration rule on cycle switch.
- [[plans-purchase-recommended-addons]] — *Recommended services* + *Recommended applications* blocks, centrally-flagged marketing recommendations, DE-bypass behaviour, cart-shape entries.
- [[plans-purchase-plan-detail-view]] — `/admin/plan/{mapping}` read-only feature breakdown, hidden-features filter, DE Starter record swap, side-panel chrome hiding.
- [[plans-purchase-checkout-panel]] — Checkout side-panel structure (Order overview / Invoice details / Payment method / Discount / Totals), Stripe + Braintree gateways, 3DS mid-flight challenge, per-item success confirmation card.
- [[plans-purchase-business-rules]] — cart reset on entry, single-variant constraint, LTA-contract override, DE free-plan record swap, no-proration on cycle switch, downgrade gating semantics, recommendations centrally-flagged, GTM checkout event.
- [[plans-purchase-subscription-outcomes]] — confirm-step validation (invoice details + card required), per-item success / partial-success, `MODE_UPDATE` subscription reuse on re-purchase, LTA-bundle `createLtaContract` path, LTA-cart-conflict 422.
- [[plans-purchase-discount-codes]] — session-seeded promo codes via marketing landing URLs, Discount card on the Checkout panel, `cart.hide_discount` flag, first-cycle-only discount handling.

## Settings & fields

This hub only catalogues the screen-level orientation. For specific controls, drill into the aspect:

- **Billing-cycle radio**, **Variant label**, **VAT disclaimer** → [[plans-purchase-billing-cycle]].
- **Recommended services / apps checkboxes** → [[plans-purchase-recommended-addons]].
- **Feature groups / Feature rows / Breadcrumb (detail view)** → [[plans-purchase-plan-detail-view]].
- **Order overview / Invoice details / Payment method / Totals / Pay now** → [[plans-purchase-checkout-panel]].
- **Discount code input + Apply / Remove** → [[plans-purchase-discount-codes]].

### Side-panel UX (cross-cutting)

Both the purchase + detail screens render as a **side panel** (open-from-right overlay) over the admin panel rather than full-page navigation. The (×) header button returns the merchant to `/admin` (dashboard). The standard sidebar nav, top-bar nav, breadcrumb-bar, user-account dropdown, and help button are hidden while the panel is open. The Vue path uses the modal overlay naturally; the legacy Smarty path achieves the same via extra CSS hiding `.js-page-sidebar`, `.topbar-js`, `.page-breadcrumb`, etc.

## Business rules

The cross-cutting rules are catalogued on [[plans-purchase-business-rules]]. The most-cited ones at hub level:

- **LTA contract overrides this flow** — merchants on LTA are redirected away from `/admin/plan/{mapping}/purchase` before they can reach it.
- **Free-plan record swap for DE** — German merchants requesting `/admin/plan/startup` see the DE Starter plan (re-labelled *14-Tage-Test (Starter)*) instead of the standard Start Up record.
- **Cart is reset on entry** — every PlanPanel submit clears any existing cart contents before re-seeding.
- **Only ONE billing-cycle variant per purchase** — the cart accepts a single `plan_details` ID.
- **No proration on billing-cycle switch** — switching Monthly → Yearly cancels the unused monthly time without credit.
- **Pricing + currency are read-only** — every figure comes from the plan-details catalog + the merchant's invoicing-country setup.
- **Subscription is created on checkout success, NOT on PlanPanel submit** — see [[plans-purchase-subscription-outcomes]] for the confirm step.

## Related

- [[plans]] — the catalog screen where the merchant picks the plan that leads here.
- [[plan-features]] — per-feature purchase flow (buying extra quota beyond the plan's limit).
- [[plan-feature]] — individual feature entity.
- [[plan-gates]] — concept of plan gating; explains how limit-reached / feature-not-enabled screens funnel merchants here.
- [[subscriptions]] — once purchased, the plan creates a `plan_details` subscription visible in the subscriptions list.
- [[plan-details]] — entity carrying per-variant pricing rows.
- [[plan-services]] — directory of purchasable CloudCart services.
- [[plan-apps]] — directory of paid CloudCart apps.
- [[billing-cards]] — saved payment cards used during the redirect-to-checkout step.
- [[billing-invoicing]] — billing details + invoicing-country setup that determines the displayed currency.
- [[details-billing]] — high-level billing settings hub.
- [[expired-subscription]] — merchants funnelled here when their plan-detail subscription is past-due or expired.
- [[contracts]] — long-term agreement (LTA) plans that replace this purchase flow for LTA-onboarded merchants.
- [[account-plan]] — alternative entry into plan management.
- [[merchant-subscription-lifecycle]] — merchant-question hub for upgrade / switch billing cycle / cancellation questions.

## Open questions

(All resolved — distributed to sub-pages.)
