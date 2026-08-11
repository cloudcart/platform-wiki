---
type: feature
nav_path: "Details → Contracts"
route_name: contracts
route_path: /admin/details/contracts
aliases: ["Contracts", "LTA", "Long-term agreement", "LTA contract", "Договори", "Дългосрочен договор", "Договор с CloudCart"]
tags: [base, details, contracts, plans, lta]
plan_gates: []
created: 2026-05-21
updated: 2026-06-11
source_count: 1
---
# Contracts

## Purpose

The **Contracts** screen lists the **long-term agreements (LTAs)** the merchant has signed directly with CloudCart. An LTA is a bespoke commercial agreement — negotiated with CloudCart rather than self-served from the [[plans]] catalogue — that fixes the merchant's feature set, limits, and price for a contracted period. Merchants without an LTA see an empty list here; this screen only matters to accounts onboarded onto a negotiated contract.

## Where to find it

**Details → Contracts** (`/admin/details/contracts`), in the account/details area alongside [[details-billing]] and [[subscription-details]].

## What the merchant can do here

- See each active and past long-term agreement on the account.
- Open an individual contract to review its terms and any signed documents (read-only).
- Reach the same contract from the plan flow: a merchant on an active LTA who opens **Choose plan** is redirected to the contract preview instead of the self-serve catalogue — see [[plans-contract-lta-override]].

## Settings & fields

This screen is **read-only** — there are no editable fields. Each contract row surfaces its headline data (the negotiated plan, the contract period / end date, and the agreed feature values). The authoritative term list lives on the individual contract page (`/admin/contracts/{id}`).

## Business rules

- **An LTA overrides the standard plan.** While a contract is active, its negotiated feature limits and price replace the underlying plan's values for the duration of the contract window — see [[plan-entity-overrides-lta-and-partner]].
- **An LTA blocks the self-serve purchase flow.** A merchant on an active LTA cannot buy or change a plan from [[plans-purchase]]; the catalogue redirects them to the contract page (see [[plans-contract-lta-override]]).
- **LTA charges appear in billing.** Transactions under a contract show in [[details-billing]] under the merchant's standard view.
- **Onboarded by CloudCart, not self-served.** Contracts are created during a staff-assisted onboarding; regular self-serve merchants never see this surface populated.

## Related

- [[plans]] — the self-serve plan catalogue an LTA replaces.
- [[plans-contract-lta-override]] — how an active LTA redirects the plan flow to the contract preview.
- [[plan-entity-overrides-lta-and-partner]] — how contract feature values override the base plan.
- [[details-billing]] — billing transactions, including LTA charges.
- [[subscription-details]] — the subscription tied to the account.
- [[account-plan]] — the current plan / subscription summary.

## Open questions

- The full field list on the individual `/admin/contracts/{id}` contract page (verify against the live contract view).
