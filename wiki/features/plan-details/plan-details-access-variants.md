---
type: feature
nav_path: "Plan → {Plan name} → Access & variants"
route_name: plan-details
route_path: /admin/plans/:id
aliases: ["Plan details access", "Plan details side panel", "Plan details full page", "Plan details 404", "DE Starter plan substitution", "LTA plan redirect", "Plan currency by country", "Достъп до детайли на план"]
tags: [plans, plan-details, plan-purchase, access, subscription]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Plan details — access & variants

## Purpose

> Part of [[plan-details]]. See the hub for the other aspects (billing cycle, recommendations, checkout).

This aspect covers **how the [[plan-details]] screen is reached and which form it takes** — the entry points (catalog card, direct URL, plan badge, gate redirect), the side-panel vs full-page chrome, the currency rule, and the edge cases that change or block the screen (DE free-plan substitution, LTA-contract redirect, and the 404 on plans without active billing variants).

## Where to find it

- **From [[plans]]**, clicking the **Choose** button on a plan card opens this screen as a side-panel (the URL doesn't change in panel mode).
- **Direct URL** — `/admin/plans/{mapping}` opens the same view as a full page (e.g. `/admin/plans/cc-pro`, `/admin/plans/business`).
- **From the profile dropdown's *Plan* badge** — the badge label "Plan: <current-plan>" links here for the merchant's current plan, where they can change billing cycle without changing plan.
- **From plan-gate redirects** that need a plan-level upgrade (some funnels send the merchant straight to a specific plan's purchase page).

URL pattern: `/admin/plans/{mapping}`, with the side-panel variant opened from the catalog using the same component.

## What the merchant can do here

### Open the same screen two ways

When reached as `/admin/plans/{mapping}` (full URL) the screen is a normal page; when opened from [[plans]] via *Choose* the SAME component renders inside a side panel with the URL unchanged. The body — billing-cycle picker, recommendation blocks, checkout button — is identical in both; only the wrapper chrome (close button, header) differs.

### Change billing cycle on the current plan

Reaching the screen via the *Plan* badge for the current plan lets the merchant change billing cycle without changing plan — they land on their own plan's detail view.

## What the merchant cannot do here

- **Compare plans in panel mode** — the side-panel only shows one plan's details; to compare, go back to [[plans]].
- **Pick a currency** — currency is fixed by the company's invoicing entity (see below).
- **Reach a plan with no active billing variants** — the URL returns *Not Found* (see below).
- **Reach this screen organically as an LTA merchant** — the catalog redirects LTA-contract sites to the contract page first (see below).

## Settings & fields

| Field / Control | What it does | Default | Notes |
|-----------------|--------------|---------|-------|
| **Screen wrapper** | Full-page vs side-panel chrome | Full page on direct URL; side panel from catalog | Body identical; only the wrapper differs |
| **Plan header** | Plan title (e.g. *Plan Pro*) + calendar-star icon | — | No close button on the full-page route; the side panel has its own close |
| **Currency** | Display currency for all prices | Set by invoicing entity | Not selectable by the merchant |

## Business rules

### Currency follows the merchant's invoicing country

Prices are displayed in the currency configured for the merchant's invoicing entity (BGN for BG-invoiced, EUR for DE-invoiced, etc.). The merchant cannot pick a currency — it's fixed by their company setup, the same setup that gates the recommendation blocks on [[plan-details-recommendations]].

### Free-plan special-case for DE

When a German merchant requests the Start Up plan (the free plan), the platform substitutes the DE Starter plan and re-labels it as *14-Tage-Test (Starter)* — the screen renders the DE Starter feature breakdown under the *Start Up* URL. See [[plans]] for the full DE branding override.

### LTA contracts override this screen

If the merchant's site has an active long-term agreement (LTA) contract, the [[plans]] catalog redirects to the contract details page before this screen is reached. The plan-detail URL still works directly but isn't reached organically by LTA merchants.

### 404 on plans without active variants

When the merchant requests a plan that has no active priced billing variants (all soft-deleted or inactive), the screen redirects to the error-404 route. This is how CloudCart soft-disables a plan: removing all billing variants makes it both invisible on the catalog AND unreachable here. The billing-variant list itself is documented on [[plan-details-billing-cycle]].

### Hidden features filter the breakdown view

When the merchant uses this screen to *browse* a plan's feature breakdown (reached via the plan badge → "What does my plan include?"), features flagged as hidden for that plan in the central catalog don't render — instead of showing as a disabled ✗. Plan-tier enforcement of those features is on [[plan-gates]].

## Related

- [[plan-details]] — hub.
- [[plans]] — the catalog; source of the DE override and LTA redirect.
- [[plan-details-billing-cycle]] — the variant list whose absence causes the 404.
- [[plan-details-recommendations]] — recommendation blocks gated by the same invoicing entity.
- [[plan-gates]] — plan-tier feature enforcement behind the breakdown view.
- [[billing-invoicing]] — invoicing entity that fixes the display currency.
- [[subscriptions]] — where the purchased plan lands after checkout.

## Open questions

(All resolved.)
