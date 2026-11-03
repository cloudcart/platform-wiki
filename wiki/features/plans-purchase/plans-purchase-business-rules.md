---
type: feature
nav_path: "Profile → Choose plan → {Plan} → Purchase → Business rules"
route_name: admin.plan.purchase
route_path: /admin/plan/{mapping}/purchase
aliases: ["Plan purchase rules", "Plan purchase cart-reset", "Plan LTA override", "Plan downgrade behaviour", "Plan proration rule", "Промяна на план — правила", "LTA правила", "Право на върнато време"]
tags: [plans, purchase, business-rules, lta, downgrade, proration]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[plans-purchase]]. See the hub for the other aspects (billing cycle, recommended add-ons, plan detail view, checkout panel, subscription outcomes, discount codes).

# Plans purchase — business rules

## Purpose

This page catalogues the **non-obvious behaviours** that govern entry into and exit from the plan-purchase flow — cart reset on entry, single-variant constraint, LTA-contract overrides, German free-plan record swap, no-proration on billing-cycle switch, downgrade gating semantics, and centrally-flagged recommendations. These are the rules the support LLM cites when a merchant says *"I switched to yearly and lost my unused monthly time — is that normal?"* or *"Why can't I open the upgrade flow?"*.

## Where to find it

The rules apply across `/admin/plan/{mapping}/purchase` and `/admin/plan/{mapping}` — see [[plans-purchase-billing-cycle]] + [[plans-purchase-plan-detail-view]] for the screens they govern.

## What the merchant can do here

This page is not a screen — it's the rule catalogue. Use it to look up what *happens* when the merchant does X (clicks *Upgrade now*, switches billing cycles, downgrades to a smaller plan, etc.).

## Settings & fields

(No fields — this page documents behavioural rules, not a settings form. See the linked screen pages for the actual controls.)

## Business rules

### Cart is reset on entry

When the merchant submits the PlanPanel, the bulk-cart promo endpoint **clears any existing cart contents first**, then adds the selected plan + ticked services + ticked apps fresh. The merchant cannot accidentally combine items left over from a previous flow (e.g. an abandoned plan-feature pack purchase) — every entry into the purchase flow starts a clean cart.

### Only ONE billing-cycle variant per purchase

The variant picker is radio (not checkbox). The merchant cannot buy *both* monthly *and* yearly at once — the cart accepts a single `plan_details` ID per cart. To switch later, they re-enter the purchase flow.

### LTA contract overrides this flow

If the merchant is on an active **LTA contract**, the [[plans]] catalog redirects to the contract page before this screen is reached. A merchant on LTA effectively cannot visit the purchase flow at all — their plan is governed by the contract. See [[contracts]] for the LTA contract management surface.

### LTA-bundle cart-conflict check

If the merchant has an active LTA contract AND tries to add a non-LTA item that conflicts with their contract terms (e.g. buying a plan when the contract already covers one), the confirm step throws *"Your cart conflicts with your active contract"* (HTTP 422). This protects LTA merchants from double-paying for items already covered. See [[plans-purchase-subscription-outcomes]] for the full confirm-step error surface.

### Free-plan record swap for DE

When a German merchant clicks the free **Start Up** plan card, the detail / purchase URL still says `/admin/plan/startup`, but the platform internally swaps the plan record to the DE Starter plan (ID 60 — *(verify)*) and re-labels it as *14-Tage-Test (Starter)* — i.e. the "free plan" detail view shows the 14-day-trial Starter feature breakdown instead. The free-plan upgrade for other countries is unchanged.

DE merchants also bypass the PlanPanel entirely — see [[plans-purchase-recommended-addons]] for the `isGermanyBased` direct-to-Checkout path.

### Pricing comes from the catalog — no override

Every figure shown (price, original price, discount, period text, currency, VAT) is read from the `plan_details` catalog row. The merchant cannot override any value — the only choice is *which* variant to pick.

### Currency = invoicing-country default

The currency sign + decimal formatting are determined by the merchant's invoicing setup, NOT by their store currency. So a merchant whose store sells in BGN but is invoiced by the BG entity sees plan prices in BGN; a DE-invoiced store sees EUR. See [[billing-invoicing]] for managing the invoicing country.

### Recommendations are centrally-flagged

The *Recommended services* and *Recommended apps* blocks pull from CloudCart's central catalog of items marked as `recommended` and currently active in their active-period window. The merchant doesn't choose what's recommended — CloudCart's marketing layer decides per audience. See [[plans-purchase-recommended-addons]].

### Bundling boosts the checkout

The *Recommended* blocks exist so the merchant can buy plan + add-ons in a single transaction instead of doing two separate checkouts later. Each ticked item gets its own line on the resulting invoice — they're individual subscriptions, just paid for in one go.

### Google Tag Manager fires a checkout event

When the merchant clicks the Checkout button, a `checkout` event is pushed to the `dataLayer` with each ticked item's product data (plan, services, apps). This drives CloudCart's own analytics; it's not exposed to the merchant.

### Submit redirects to admin checkout

The PlanPanel posts to an internal bulk-cart promo endpoint that returns a JSON success response with `redirect: /admin/checkout` after seeding the cart. The merchant is then on the standard admin checkout (see [[plans-purchase-checkout-panel]]) to pick a payment method and confirm. The actual money movement + subscription creation happen during checkout — not on the PlanPanel.

### Switching billing cycles — no proration

There is NO proration logic when switching between Monthly and Yearly. When a merchant on Pro Monthly switches to Pro Yearly through the **Current plan** option on the purchase screen, they pay a FULL new term and their old monthly subscription is cancelled. Any unused monthly time is NOT credited back. The merchant should switch at the end of a billing cycle to avoid losing time.

### Downgrade outcomes — data preserved, gates take effect immediately

There is NO downgrade-specific data cleanup. When a merchant downgrades to a plan with lower limits:

- Existing over-quota records (products / customers / etc.) ARE preserved on disk.
- The plan gates (see [[plan-gates]]) take effect IMMEDIATELY — the merchant can VIEW their existing records but cannot CREATE new ones beyond the new lower limit.
- To restore normal create / edit flow, the merchant must either delete excess records to drop below the new limit, OR upgrade back to the higher plan.

## Related

- [[plans-purchase]] — hub.
- [[plans]] — catalog of plans (the entry point that may redirect to LTA contract).
- [[plans-purchase-billing-cycle]] — the variant picker affected by the no-proration rule.
- [[plans-purchase-recommended-addons]] — the centrally-flagged add-ons + DE bypass.
- [[plans-purchase-subscription-outcomes]] — the confirm-step rules (invoice/card required, LTA conflict, per-item success).
- [[plan-gates]] — the limit-reached / feature-not-enabled screens that funnel merchants here.
- [[contracts]] — long-term agreement plans that override this purchase flow.
- [[expired-subscription]] — merchants funnelled here when their plan-detail subscription is past-due or expired.
- [[merchant-subscription-lifecycle]] — merchant-question hub for upgrade / switch-cycle / downgrade questions.

## Open questions

None.
