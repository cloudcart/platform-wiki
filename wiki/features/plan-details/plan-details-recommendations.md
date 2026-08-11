---
type: feature
nav_path: "Plan → {Plan name} → Recommended services & apps"
route_name: plan-details
route_path: /admin/plans/:id
aliases: ["Plan recommended services", "Plan recommended apps", "Recommended add-ons on plan", "Plan bundle add-ons", "Препоръчани услуги към план", "Препоръчани приложения към план"]
tags: [plans, plan-details, plan-purchase, recommendations, subscription]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Plan details — recommended services & apps

## Purpose

> Part of [[plan-details]]. See the hub for the other aspects (billing cycle, checkout, access & variants).

Below the billing-cycle picker, the [[plan-details]] screen can show two optional blocks — *Recommended services* and *Recommended applications* — that let the merchant **add CloudCart-suggested add-ons to the same purchase**. Ticking an add-on puts it in the same cart the plan is bought through, so plan + services + apps are paid for in one checkout.

## Where to find it

The two blocks sit between the billing-cycle picker and the *Proceed to checkout* button on [[plan-details]]. They render only when CloudCart has flagged at least one service or app as recommended for this merchant's profile; otherwise both blocks are hidden and the merchant sees only the billing-cycle picker.

## What the merchant can do here

### See recommended services for the plan

If CloudCart has flagged any services as recommended for the merchant (centrally driven, not user-chosen), they appear under the billing-cycle picker as checkboxes — each with its name, price, period, and an expandable Markdown description. Ticking a service adds it to the same cart the plan will be purchased through. A service's price line follows the *<price> / <period>* pattern (e.g. *50.00 EUR / month*, *200.00 EUR / onetime*), and its description renders with *Show more* / *Show less*.

### See recommended apps for the plan

A parallel *Recommended applications* block lists paid CloudCart apps marked as recommended (centrally). Same checkbox + name + price pattern. App rows show only a name + price line (no description block). Apps in this list are tied to subscriptions that renew on their own cycles, separately from the plan.

## What the merchant cannot do here

- **Choose which items are recommended** — the lists are centrally curated by CloudCart, not editable by the merchant.
- **See recommendations on a non-default invoicing entity** — merchants invoiced through a non-default issuer company don't get these blocks at all (see *Recommendations only for the default issuer* below).
- **Add an arbitrary service / app not in the list** — only items CloudCart has flagged for this merchant appear. The full paid catalogs live on [[plan-services]] and [[plan-apps]].
- **Pay for a ticked add-on separately** — ticked items go into the same cart and are paid in the one checkout; see [[plan-details-checkout]].

## Settings & fields

| Field / Control | What it does | Default | Notes |
|-----------------|--------------|---------|-------|
| **Recommended services** (checkbox per service) | Adds a service to the same cart | Unchecked | Block visible only when at least one service is recommended for this merchant |
| **Recommended apps** (checkbox per app) | Adds an app to the same cart | Unchecked | Block visible only when at least one app is recommended for this merchant |
| **Service / app price** | Per-period price (excl. VAT) | — | Shown inline next to each checkbox row; services use *<price> / <period>* |
| **Service / app description** | Markdown-rendered description with *Show more* / *Show less* | Collapsed | Services only; app rows have no description block |

A horizontal rule separates consecutive service rows.

## Business rules

### Recommendation blocks are merchant-wide, not plan-wide

The recommended services / apps shown on this screen are NOT tied to the specific plan — they're CloudCart's central recommendations for THIS merchant's profile. The same list would appear on any plan-details page the merchant opens. The block is just "what CloudCart suggests for this merchant" in the context of a plan purchase.

### Recommendations only for the default issuer

The backend conditionally returns the recommendations only when the merchant's invoicing entity is the **default issuer company** (BG). Merchants invoiced through other entities (DE, etc.) don't see either block, even if recommended items exist for them. Currency on the price lines follows the same invoicing-entity rule — see [[plan-details-access-variants]].

### Ticked add-ons join the plan in one cart

Ticked services and apps are added to the same cart as the plan and submitted together. The detailed cart shape — one plan entry + N service entries + N app entries — and the checkout flow are on [[plan-details-checkout]].

## Related

- [[plan-details]] — hub.
- [[plan-services]] — the full recommended-services catalog (parallel to this block).
- [[plan-apps]] — the full paid-apps catalog (parallel to this block).
- [[plan-details-checkout]] — where ticked add-ons join the plan in the cart.
- [[plan-details-access-variants]] — the invoicing-entity rule that also gates these blocks.
- [[subscriptions]] — purchased services / apps appear here on their own renewal cycles.

## Open questions

(All resolved.)
