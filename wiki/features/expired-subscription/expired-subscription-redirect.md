---
type: feature
nav_path: "Expired Subscription → Redirect & allowlist"
route_name: expired-subscription
route_path: /admin/expired-subscription
aliases: ["Expired subscription redirect", "Plan middleware redirect", "Admin access blocked allowlist", "402 Payment Required redirect", "Блокиран достъп — пренасочване", "Изключения от блокировката"]
tags: [base, core, expired-subscription, subscriptions, billing, blocking-screen]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Expired Subscription — redirect & allowlist

> Part of [[expired-subscription]]. See the hub for related aspects (paid-plan timing, free Start Up plan, data lifecycle).

## Purpose

This aspect explains **how a merchant ends up on the takeover screen** and **which admin areas stay reachable** while the store is in an unpaid state. The merchant never navigates here intentionally — the platform's plan middleware redirects almost every admin URL to `/admin/expired-subscription` whenever the store's plan subscription has lapsed, and only a short hardcoded allowlist of billing-related paths is exempt so the merchant can diagnose and fix the problem.

## Where to find it

The merchant is **redirected** here automatically. The redirect fires on every admin request when EITHER:

- The site record's `plan_expired` flag is set, OR
- The site's overall status is `Past due` (2) or `Expired` (3) AND a plan-type subscription is in Past due / Expired.

For AJAX requests (the modern Vue SPA), the platform returns HTTP **402 (Payment Required)** with the JSON payload `{"redirect": "expired-subscription"}` so the SPA can navigate there client-side. Direct browser requests get a real **302** redirect.

## What the merchant can do here

The merchant can still reach a short allowlist of paths so they can log out, view subscriptions / billing, update their card, view invoices, and reach the contracts area:

| Allowed area | Examples |
|--------------|----------|
| Subscription / billing screens | `/admin/details/subscriptions`, `/admin/details/billing`, `/admin/details/invoices`, `/admin/billing/*` |
| Subscription management APIs | `/admin/api/core/subscriptions`, `/admin/api/core/billing`, `/admin/api/core/checkout`, `/admin/api/core/transactions`, `/admin/api/core/invoice`, `/admin/api/core/applications/details` |
| Offers / contracts | `/admin/offers/*`, `/admin/api/core/offers`, `/admin/api/core/contracts` |
| Settings / payment providers | `/admin/settings/*`, `/admin/payment-providers/*` |
| The expired-subscription screen itself | `/admin/expired-subscription` |
| Sign-in / logout | `/admin/login-request*` |

Everything else — products, orders, customers, marketing, analytics, dashboard, apps — redirects back to the takeover.

## Settings & fields

This aspect has no settings of its own. The allowlist is **hardcoded** in the plan middleware and is identical for every merchant — it is not configurable. It is designed to give the merchant exactly the access they need to diagnose and fix the unpaid state (subscriptions, billing cards, invoices, settings so they can switch the primary domain to HTTPS if needed for card entry, and the logout link).

## Business rules

### Two distinct triggers for the takeover

The plan middleware checks two conditions to decide whether to redirect:

1. **`plan_expired` flag is set on the site record** — true after the daily site-expiry sweep flips the site to `Expired`.
2. **Site status is `Past due` or `Expired` AND a plan-type subscription is `Past due` / `Expired`** — true during the dunning window between the first failed renewal and the eventual site-level Expired flip.

Either condition triggers the redirect. The second one is what catches merchants during the grace window — even though the site hasn't yet been swept to Expired, the plan subscription's Past due status alone is enough to gate access. See [[expired-subscription-paid-timing]] for the full timing ladder.

### The redirect runs before any controller

The plan middleware checks the unpaid state on every admin request **before** the controller runs. If the merchant is in the unpaid state AND the request is NOT for an allowlisted path, the middleware short-circuits with a 302 redirect (or a 402 JSON response for AJAX) — the underlying screen's logic never runs. This is why the merchant cannot "sneak in" by deep-linking to a non-allowlisted URL: every request runs the middleware first.

### Subscription list still shows everything during the takeover

Because the [[subscriptions]] list is on the allowlist, the merchant can still see WHICH subscription failed, the failed-attempts count, the Status badge, the next billing date, and the Cancel / Renew action buttons. The takeover doesn't blind the merchant — it just prevents them from doing anything ELSE until they fix billing.

### Invoice downloads still work during the takeover

Invoice download URLs (`/admin/api/core/invoice/download/...`) are scoped to the merchant's own site but NOT gated by the unpaid state. Merchants can still pull historical invoice PDFs even while the takeover is in effect — important for accounting (the merchant may need their last CloudCart invoice to reconcile their books even when they cannot pay the next one).

### Reseller (partner-network) merchants on the free plan are redirected elsewhere

If a merchant is on the free `startup` plan AND their site is flagged with a partner reseller (e.g., `reseller_id = 157` = UniCredit), the middleware redirects to [[plans]] instead of this screen — partner-network merchants don't see the takeover at all because their plan is governed by the partner contract. See [[expired-subscription-free-plan]] for the rest of the free-plan behaviour.

## Related

- [[expired-subscription]] — hub.
- [[subscriptions]] — the allowlisted list the merchant lands on to Renew; still fully visible during the takeover.
- [[plans]] — redirect destination for reseller-onboarded free-plan merchants.
- [[plan-gates]] — the platform's broader paywall engine; the takeover is the top-level case where ALL gates fail because there's no active plan.
- [[subscription-lifecycle]] — the state machine that drives the Past due → Expired transitions feeding the redirect conditions.

## Open questions

(All resolved.)
