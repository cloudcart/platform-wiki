---
type: feature
nav_path: "Profile → Choose plan → (LTA contract override)"
route_name: plans
route_path: /admin/plans
aliases: ["LTA contract override", "Long-term agreement plans", "Plans contract redirect", "ContractInfoPreview", "Custom contract plans", "LTA преглед", "Договорни планове"]
tags: [plans, pricing, contracts, lta]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[plans]]. See the hub for the other aspects (catalog display, country / partner filtering, free-plan expiry, downgrade behavior, plan-feature cache).

# Plans — LTA contract override

## Purpose

This page documents what happens at `/admin/plans` when the merchant has an **active long-term agreement (LTA) contract** with CloudCart — a custom multi-year deal negotiated directly with the CloudCart sales team. In that case the public catalog is **not relevant** to the merchant: their pricing, feature limits, and billing terms are all set by the contract itself, not by any plan in the standard catalog. So the screen suppresses the cards + comparison matrix and instead renders a **read-only contract preview**, with a link to the full contract details page.

## Where to find it

Same URL as the regular catalog: `/admin/plans`. The redirect is transparent — the merchant clicks **Choose plan** from the profile dropdown, expects the catalog, and instead gets the contract preview component on the same page. The full contract page lives at `/admin/contracts/{unique_id}` (see [[contracts]]).

## What the merchant can do here

- See a **read-only preview** of the contract terms — usually plan name, billing period, total amount, contract dates.
- Click through to the full contract page ([[contracts]]) for the complete terms + signed documents.
- Contact CloudCart sales if a renegotiation is needed.

## What the merchant cannot do here

- **Switch plans through the catalog** — the LTA contract IS the plan. Changing it requires renegotiating with CloudCart, not clicking a card.
- **See the public plan cards or comparison matrix** — they're hidden under LTA.
- **Use the period switcher** — billing cycle is fixed by the contract.

## Settings & fields

This is a read-only preview. The fields shown are the same as the contract's own headline data — see [[contracts]] for the authoritative list. Typical fields previewed here:

| Field | Meaning |
|-------|---------|
| **Contract plan name** | The custom plan name agreed in the contract (often "Enterprise — Custom" or a per-merchant name). |
| **Billing period** | Contract term, e.g. *24 months*. |
| **Period start / end dates** | Calendar window the contract covers. |
| **Contract value** | Total amount agreed for the period. |
| **Link to contract details** | Opens the full contract page. |

The exact preview fields are owned by the `ContractInfoPreview` component — see [[contracts]] for what the full contract view exposes.

## Business rules

### Detection — array vs object payload

When `PlansList` loads at `/admin/plans`, it requests the plan / contract data from the backend. If the response is the **plans payload** (the normal catalog), the component renders cards + matrix. If the response is an **array of contract data** instead, the component knows the merchant is on an LTA contract and switches to rendering `ContractInfoPreview` for that contract. (verify) — the array-vs-object discriminator is the implicit signal; there is no explicit `isLTA` flag in the response.

### LTA wins over partner / country filtering

The LTA check runs **first** in the catalog decision tree. Even if the merchant is on a partner reseller (UniCredit etc.) or in a specific country, an active LTA contract takes precedence — the merchant sees the contract preview, not the partner catalog or the country-filtered catalog. See [[plans-country-partner-filter]] for the rest of the decision tree.

### The catalog is unreachable while LTA is active

There is no "browse the catalog anyway" option for LTA merchants. Visiting `/admin/plans`, `/admin/plan`, or any in-app upsell link that points here lands on the contract preview. To actually browse the catalog, the merchant would need the LTA contract to end or be removed by CloudCart staff.

### LTA merchants don't see the "Choose plan" upgrade prompts

Most upsell prompts in the admin (the orders report limit counters, the sandbox banner, plan-feature gate errors per [[plan-gates]]) link to `/admin/plans`. For LTA merchants those links still resolve to the contract preview — there's no separate "your contract is overpaid for this" surface. The merchant is expected to manage feature unlocks through their account manager, not through the in-app upsell flow.

### LTA does not replace the feature-cache + plan-gate system

The LTA contract still maps to a backing plan record for gate evaluation purposes — feature limits are still looked up via the standard plan-gate pipeline (see [[plan-gates]] and [[plans-cache-and-demo]]). The LTA preview only changes what `/admin/plans` *displays*; the rest of the admin panel evaluates features as if the contract's backing plan were the merchant's plan.

## Related

- [[plans]] — hub.
- [[contracts]] — the full contract page the preview links to.
- [[plans-country-partner-filter]] — the rest of the catalog decision tree (LTA wins over both signals).
- [[plans-catalog-display]] — the catalog UI that's suppressed under LTA.
- [[plan-gates]] — feature-restriction enforcement still runs for LTA plans.
- [[plans-cache-and-demo]] — the plan-feature cache layer that LTA contracts use the same way.
- [[merchant-subscription-lifecycle]] — broader merchant-support hub for plan / billing questions.

## Open questions

(All resolved.)
