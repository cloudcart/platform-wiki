---
type: concept
nav_path: "Concept → Plan gates → LTA contract overrides"
aliases: ["LTA contract", "Long-term agreement", "LTA override", "Contract plan override", "LTA feature values", "Contract-locked plan", "Дългосрочен договор", "LTA договор", "Договорни лимити"]
tags: [billing, plans, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 1
---

> Part of [[plan-gates]]. See the hub for the other aspects (restriction shapes, enforcement points, trial / catalogs, feature naming).

# Plan gates — LTA contract overrides

## Definition

A **Long-Term Agreement (LTA contract)** holds a plan and often apps, feature packs and one-off services, each kept as one of the store's subscriptions for the term. Plan gates read those the same way as on any store, so an LTA merchant's effective caps are those of the plan and add-ons in the contract.

Two visible consequences for the merchant:

- The plan in the merchant's profile shows as their **LTA contract name** (not the underlying plan tier).
- The [[plans]] catalog redirects them to the **contract detail page** — they cannot shop for a different plan while under contract.

Once the contract has ended, the store keeps its items on regular billing ([[contracts]]), and the merchant can again browse and change plans normally.

## Scope

What this covers:

- What an LTA contract is in the context of plan gating.
- What gates read for a store on a contract.
- The two merchant-visible effects (profile shows contract name; can't shop for plans).
- What happens to plan browsing when the contract ends.

What it does NOT cover:

- The LTA-contract creation flow — see [[plans-purchase]]. End of term and the penalty invoice — see [[contracts]].
- The general restriction shapes — see [[plan-gates-restriction-shapes]].
- Feature packs and how they stack (packs are a separate per-feature add-on, not a contract) — see [[plan-vs-feature-pack]].
- Trial-plan expiry, which is a different mechanism from contract expiry — see [[plan-gates-trial-and-catalogs]].

## Contrasts

- **LTA contract vs. feature-pack add-on**: a feature pack *adds* quota on top of the plan's base value for ONE feature (see [[plan-vs-feature-pack-stacking]]); a contract is an agreement that can hold a plan and packs together.
- **LTA contract vs. plan upgrade**: a plan upgrade changes the merchant's tier and they can keep shopping plans; an LTA contract removes the ability to switch plans until it ends.
- **Contract completion vs. trial expiry**: a contract that completes returns the store to regular billing (no suspension); the free `startup` trial expiring suspends the storefront entirely. See [[plan-gates-trial-and-catalogs]] for the trial path.

## Where it applies

### The plan catalog redirect

A merchant under an active LTA who opens [[plans]] does not see the normal catalog of purchasable plans — the platform redirects them to their contract detail page. This prevents an LTA merchant from accidentally moving to a non-contract plan mid-term and breaking the agreed pricing. The same `/admin/plan` URL that renders plan cards for a normal merchant renders the contract view for an LTA merchant.

### What the gates read

Every plan-gate check (create-endpoint, path-access, boolean inline — see [[plan-gates-enforcement-points]]) uses the same `<feature, plan>` lookup described on [[plan-gates-restriction-shapes]], against the plan and add-ons the store holds. A contract's items are not editable in the admin UI (see [[plan-gates-feature-naming]] on where gates are configured).

## Related

- [[plan-gates]] — hub.
- [[plans]] — the plan catalog; redirects LTA merchants to their contract detail page.
- [[plans-purchase]] — the purchase / contract flow.
- [[contracts]] — the merchant's view of a contract, its end of term and the penalty invoice.
- [[plan]] — the Plan entity.
- [[expired-subscription]] — the takeover screen when a subscription fully expires.
- [[merchant-roles]] — the other gate that must also pass independently of the contract.

## Open Questions

None.
