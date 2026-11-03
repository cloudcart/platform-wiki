---
type: feature
nav_path: "Plan → {Plan name}"
route_name: plan-details
route_path: /admin/plans/:id
aliases: ["Plan details", "Plan breakdown", "Plan info", "Plan summary", "Plan preview", "Детайли на план", "Преглед на план"]
tags: [plans, plan-details, plan-purchase, subscription]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---
# Plan details

## Purpose

The **Plan details** screen is the full-page view of a single plan — it lists the billing-cycle options for that one plan, optionally surfaces *Recommended services* and *Recommended apps* blocks tied to it, and offers a *Proceed to checkout* button to buy the plan together with any ticked add-ons in one transaction.

This is the merchant-facing companion to the [[plans]] catalog: while the catalog shows ALL plans side by side, this screen drills into ONE plan to choose billing cycle + bundle services/apps before checkout. It's also reached as a side-panel from the catalog (clicking a plan card opens the same component as a modal).

The same screen renders for any plan mapping (Start Up, Basic, Pro, Business, Enterprise, Unicorn, etc.) — the content is driven by the catalog row, not by code per plan.

This page is a **hub**. Each merchant-facing aspect of the screen is documented on its own sub-page (below). Drill into the aspect that matches the question rather than reading every page.

## Sub-pages (in this cluster)

- [[plan-details-billing-cycle]] — the billing-cycle radio picker; variant labels (price / period / savings); pre-selection of the deepest discount; period-text mapping; switching cycle = full new term, no proration.
- [[plan-details-recommendations]] — the *Recommended services* + *Recommended apps* checkbox blocks; why they're merchant-wide (not plan-specific); the default-issuer-only visibility condition.
- [[plan-details-checkout]] — *Proceed to checkout*: cart shape (one plan + N services + N apps), the bulk-cart reset, the checkout side-panel, subscriptions created only at confirm, success → dashboard redirect.
- [[plan-details-access-variants]] — how the screen is reached (catalog card, direct URL, plan badge, gate redirect); side-panel vs full-page chrome; currency follows invoicing country; DE free-plan substitution; LTA override; 404 on plans without active variants.

## Where to find it

- **From [[plans]]**, clicking the **Choose** button on a plan card opens this screen as a side-panel (the URL doesn't change in panel mode).
- **Direct URL** — `/admin/plans/{mapping}` opens the same view as a full page (e.g. `/admin/plans/cc-pro`, `/admin/plans/business`).
- **From the profile dropdown's *Plan* badge** — the badge label "Plan: <current-plan>" links here for the merchant's current plan, where they can change billing cycle without changing plan.
- **From plan-gate redirects** that need plan-level upgrade (some funnels send the merchant straight to a specific plan's purchase page).

URL pattern: `/admin/plans/{mapping}`. The full breakdown of every entry point — plus the side-panel vs full-page distinction — is on [[plan-details-access-variants]].

## What the merchant can do here

- **Pick a billing cycle** — choose Monthly / Yearly / Every 2 years as a stacked radio; see [[plan-details-billing-cycle]].
- **See recommended services / apps** — tick centrally-flagged add-ons that go into the same cart; see [[plan-details-recommendations]].
- **Proceed to checkout** — buy the plan + ticked add-ons in one transaction via the standard checkout panel; see [[plan-details-checkout]].
- **Read about each option** — each billing-cycle label and each service/app card carries a full description (Markdown, *Show more* / *Show less*).

## What the merchant cannot do here

- **Buy without picking a billing cycle** — one variant is always pre-selected; the cart cannot be empty for the plan slot.
- **Combine two plans** — the radio variant is mutually exclusive. Switching plans means going back to [[plans]].
- **Edit prices** — every figure comes from the catalog. No coupon / promo-code field on this screen (promo codes are seeded by promotional landing URLs or entered on the standard checkout step).
- **See plans other than the one opened in panel mode** — the side-panel only shows one plan's details. To compare, go back to [[plans]].
- **Buy a plan without billing variants** — if the plan has no active priced details, the URL returns *Not Found*. See [[plan-details-access-variants]].

## Settings & fields

The screen has three stacked blocks plus a checkout button. Each block's fields are documented on the matching sub-page:

| Block | Fields | Sub-page |
|-------|--------|----------|
| Billing-cycle radio | one radio per variant (price + period + savings); last variant pre-selected | [[plan-details-billing-cycle]] |
| Recommended services | one checkbox per service + price/period + Markdown description | [[plan-details-recommendations]] |
| Recommended apps | one checkbox per app + price line | [[plan-details-recommendations]] |
| Proceed to checkout | submit button; disabled while the checkout panel is open | [[plan-details-checkout]] |

The header shows the plan title (e.g. *Plan Pro*, *Plan Business*) with the calendar-star icon.

## Business rules

- **Cart shape = one plan + N services + N apps** — the bulk-cart endpoint clears any existing cart first, then re-seeds it. See [[plan-details-checkout]].
- **Currency follows the merchant's invoicing country** — fixed by company setup, not selectable. See [[plan-details-access-variants]].
- **Recommendation blocks are merchant-wide, not plan-wide** — the same suggestions appear on any plan's detail page. See [[plan-details-recommendations]].
- **Pre-select the deepest discount** — the last (longest) cycle is selected by default. See [[plan-details-billing-cycle]].
- **Switching billing cycle ≠ proration** — a switch pays a full new term; the old subscription is cancelled and unused time is forfeit. See [[plan-details-billing-cycle]].
- **DE free-plan special-case + LTA override** — a German Start Up request renders the DE Starter breakdown; LTA-contract merchants are redirected before they reach this screen. See [[plan-details-access-variants]].
- **Downgrade preserves data** — no records are deleted; new (lower) gates take effect immediately for new creates/edits. See [[plan-gates]].

## Related

- [[plans]] — the catalog where the merchant picks the plan that leads here.
- [[plans-purchase]] — the legacy Smarty purchase route; this Vue screen is the modern variant.
- [[plan-features]] — buy quota on a specific feature without changing plan.
- [[plan-apps]] — paid apps catalog (parallel to the recommended-apps block).
- [[plan-services]] — recommended services catalog (parallel to the recommended-services block).
- [[plan-gates]] — plan-tier feature enforcement.
- [[subscriptions]] — purchased plan / services / apps appear here.
- [[billing-cards]] — saved card used during checkout.
- [[billing-invoicing]] — invoice details printed on the resulting invoice.
- [[expired-subscription]] — funnel target when the plan-detail subscription fails.

## Open questions

(All resolved.)
