---
type: concept
nav_path: "Concept → Plan gates → LTA contract overrides"
aliases: ["LTA contract", "Long-term agreement", "LTA override", "Contract plan override", "LTA feature values", "Contract-locked plan", "Дългосрочен договор", "LTA договор", "Договорни лимити"]
tags: [billing, plans, gating, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[plan-gates]]. See the hub for the other aspects (restriction shapes, enforcement points, trial / catalogs, feature naming).

# Plan gates — LTA contract overrides

## Definition

When a merchant signs a **Long-Term Agreement (LTA contract)**, the contract carries its OWN set of feature values that **override the underlying plan's values for the contract's duration**. The gating engine reads the contract's feature values instead of the plan's whenever a gate is checked, so an LTA merchant's effective caps are whatever was negotiated in the contract — not whatever the plan in their profile would otherwise grant.

Two visible consequences for the merchant:

- The plan in the merchant's profile shows as their **LTA contract name** (not the underlying plan tier).
- The [[plans]] catalog redirects them to the **contract detail page** — they cannot shop for a different plan while under contract.

When the LTA expires, the feature values fall back to the underlying plan, and the merchant can again browse and change plans normally.

## Scope

What this covers:

- What an LTA contract is in the context of plan gating.
- How contract feature values override the plan's values for the contract duration.
- The two merchant-visible effects (profile shows contract name; can't shop for plans).
- The fall-back-to-underlying-plan behaviour on expiry.

What it does NOT cover:

- The LTA-contract creation / billing flow — see [[plans-purchase]].
- The general restriction shapes the contract values use — see [[plan-gates-restriction-shapes]].
- Feature packs and how they stack (packs are a separate per-feature add-on, not a contract) — see [[plan-vs-feature-pack]].
- Trial-plan expiry, which is a different mechanism from contract expiry — see [[plan-gates-trial-and-catalogs]].

## Contrasts

- **LTA override vs. feature-pack add-on**: a feature pack *adds* quota on top of the plan's base value for ONE feature; an LTA contract *replaces* the plan's feature values wholesale for the contract's duration. Packs stack additively (see [[plan-vs-feature-pack-stacking]]); contracts override. Both can be in force at once — packs still stack on top of the contract's values.
- **LTA override vs. plan upgrade**: a plan upgrade changes the merchant's tier and they can keep shopping plans; an LTA contract freezes them onto the negotiated values and removes the ability to switch plans until expiry.
- **Contract expiry vs. trial expiry**: an LTA expiring simply falls the merchant back to the underlying plan's values (no suspension); the free `startup` trial expiring suspends the storefront entirely. See [[plan-gates-trial-and-catalogs]] for the trial path.

## Where it applies

### The plan catalog redirect

A merchant under an active LTA who opens [[plans]] does not see the normal catalog of purchasable plans — the platform redirects them to their contract detail page. This prevents an LTA merchant from accidentally moving to a non-contract plan mid-term and breaking the agreed pricing. The same `/admin/plan` URL that renders plan cards for a normal merchant renders the contract view for an LTA merchant.

### Where the override is read

Every plan-gate check (create-endpoint, path-access, boolean inline — see [[plan-gates-enforcement-points]]) reads the contract's feature values when an LTA is active, via the same `<feature, plan>` lookup described on [[plan-gates-restriction-shapes]] — the lookup simply resolves to the contract's values rather than the bare plan's. Because the contract values are negotiated rather than catalog-defined, they are not directly editable in the admin UI (see [[plan-gates-feature-naming]] on where gates are configured).

## Related

- [[plan-gates]] — hub.
- [[plans]] — the plan catalog; redirects LTA merchants to their contract detail page.
- [[plans-purchase]] — the purchase / contract flow.
- [[plan]] — the Plan entity; the underlying plan the contract overrides and falls back to.
- [[expired-subscription]] — the takeover screen when a subscription fully expires.
- [[merchant-roles]] — the other gate that must also pass independently of the contract.

## Open Questions

None.
