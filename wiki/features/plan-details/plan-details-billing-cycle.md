---
type: feature
nav_path: "Plan → {Plan name} → Billing cycle"
route_name: plan-details
route_path: /admin/plans/:id
aliases: ["Plan billing cycle", "Plan billing variant", "Plan period picker", "Monthly yearly 2-year plan", "Plan period radio", "Цикъл на плащане на план"]
tags: [plans, plan-details, plan-purchase, billing-cycle, subscription]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Plan details — billing cycle picker

## Purpose

> Part of [[plan-details]]. See the hub for the other aspects (recommendations, checkout, access & variants).

The billing-cycle picker is the top block of the [[plan-details]] screen. It lets the merchant choose **how long a term** they buy the plan for — Monthly, Yearly, or Every 2 years — and shows the price and savings for each. The chosen cycle is what goes into the cart for the plan slot.

## Where to find it

The picker is the first `b-card` on the [[plan-details]] screen, above the recommendation blocks and the *Proceed to checkout* button. It renders the same whether the screen is reached as a full page (`/admin/plans/{mapping}`) or as a side-panel from the [[plans]] catalog — see [[plan-details-access-variants]] for the entry points.

## What the merchant can do here

### Pick a billing cycle

The screen lists each active billing variant of the chosen plan as a stacked radio option. Typical variants:

- **Monthly** — base rate, billed every month.
- **Yearly** — discounted rate, billed every 12 months. The savings vs monthly are displayed inline (e.g. *(Save 24.00 EUR)*).
- **Every 2 years** — deepest discount, billed every 24 months.

The merchant's selection determines what goes into the cart. The **last** option (typically the longest cycle with the biggest discount) is **pre-selected by default** on open.

### Read the variant label

Each billing-cycle label includes the plan name, the price (without VAT), the period in human language, and the savings note — e.g. *Plan Pro — 199.00 EUR per year (Save 49.00 EUR)*. The period text maps as: 1 → *per month*, 12 → *per year*, 24 → *per 2 years*, any other N → *{N} months*.

## What the merchant cannot do here

- **Pick more than one cycle** — the radio is mutually exclusive; one variant is always selected.
- **Buy a plan with no priced variants** — if every billing variant of the plan is inactive, the plan is unreachable and the URL returns *Not Found*. See [[plan-details-access-variants]].
- **Edit the price or savings** — every figure is read from the catalog row; there is no inline editing.
- **Switch cycle without paying a full new term** — see *Switching billing cycle ≠ proration* below.

## Settings & fields

| Field / Control | What it does | Default | Notes |
|-----------------|--------------|---------|-------|
| **Billing-cycle radio** (per variant) | Selects which billing-cycle variant to buy | The LAST variant (deepest discount) is pre-selected | Variants are stacked vertically; each shows price + period + savings |
| **Variant label** | *<plan-name> <price-without-vat> <period> (Save <amount>)* | — | Built from the catalog row; price excludes VAT |
| **Period text** | Maps the cycle length to human language | — | 1 → *per month*, 12 → *per year*, 24 → *per 2 years*, other → *{N} months* |

## Business rules

### Pre-select the deepest discount

The default billing cycle is the LAST option in the catalog's variant list — typically the longest period (e.g. 2 years) with the biggest discount. This nudges the merchant toward the long commitment. The merchant can still pick a shorter cycle. Pre-selection happens after the plan data loads; switching the radio re-binds the plan slot in the cart to the matching variant for the new cycle, and the total in the checkout panel header updates accordingly. The new selection is carried into the cart at checkout — see [[plan-details-checkout]].

### Switching billing cycle ≠ proration

Like [[plans-purchase]], there is **NO proration**. When a merchant switches from Monthly to Yearly through this screen, they pay a FULL new term and the old monthly subscription is cancelled. Unused monthly time is forfeit. The merchant should switch at the end of a cycle to avoid losing paid time.

### Variants come from the catalog, not from code

Every variant, price, and savings figure is read from the plan's catalog row. There is no per-plan code path; adding or removing a billing cycle is a catalog change. A plan with all variants soft-deleted has no rows here and is treated as unreachable.

## Related

- [[plan-details]] — hub.
- [[plans]] — the catalog where the merchant picks the plan.
- [[plans-purchase]] — legacy purchase route; also has no proration.
- [[plan-details-checkout]] — where the selected cycle is turned into a cart and bought.
- [[plan-details-access-variants]] — why a plan with no active variants 404s.
- [[subscriptions]] — the plan subscription created from the chosen cycle.

## Open questions

(All resolved.)
