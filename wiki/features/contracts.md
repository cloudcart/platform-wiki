---
type: feature
nav_path: "Details → Contracts"
route_name: contracts
route_path: /admin/details/contracts, /admin/details/contracts/:id
aliases: ["Contracts", "LTA", "Long-term agreement", "LTA contract", "Договори", "Дългосрочен договор", "Договор с CloudCart"]
tags: [base, details, contracts, plans, lta]
plan_gates: []
created: 2026-05-21
updated: 2026-11-03
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

- **A contract bills its items together.** A contract holds a plan and often apps, feature packs and one-off services. Each item becomes one of the store's subscriptions on a monthly cycle at its instalment price, for the term — see [[plan-entity-overrides-lta-and-partner]].
- **An LTA blocks the self-serve purchase flow.** A merchant on an active LTA cannot buy or change a plan from [[plans-purchase]]; the catalogue redirects them to the contract page (see [[plans-contract-lta-override]]).
- **LTA charges appear in billing.** Transactions under a contract show in [[details-billing]] under the merchant's standard view.
- **Onboarded by CloudCart, not self-served.** Contracts are created during a staff-assisted onboarding; regular self-serve merchants never see this surface populated.

## End of term

### With automatic renewal

An Active contract with automatic renewal on is extended by another term when `ends_at` arrives, and billing continues.

### Without automatic renewal

A contract with automatic renewal off, status Active or Past due and `ends_at` passed is **completed** by the daily renewal run, before that day's renewals, if every cycle inside the term is paid.

- **What counts as inside the term:** a billing cycle starting within 7 days of `ends_at`, or later, is past the term. It is never billed at the contract instalment.
- **On completion:** the contract becomes Expired and the store is released from it; its status follows the plan. Plans, apps and feature packs return to their own billing cycle and list price from the first cycle after the term. One-off services paid by instalments are not billed again.
- **A cycle inside the term is unpaid:** the contract is not completed. Renewal keeps retrying, and the expiry sweep below handles giving up.

No penalty invoice is raised for a contract that completes.

### Cancel and expiry

Cancelling or expiring a contract also gives each item its own cycle and price back, so a later renewal does not bill the instalment.

The daily expiry sweep selects by `next_billing_date`, not by `ends_at`: a contract that is Canceled and due, or anything else overdue by a month.

### Penalty invoice

At most one per contract, for the sale price minus the contract's invoices (excluding VAT) at the moment of issue. None when nothing is left, so a contract paid off early is not billed again. The expiry sweep raises it, and CloudCart staff can raise it too. It is a bank-transfer invoice sent by e-mail.

## Related

- [[plans]] — the self-serve plan catalogue an LTA replaces.
- [[plans-contract-lta-override]] — how an active LTA redirects the plan flow to the contract preview.
- [[plan-entity-overrides-lta-and-partner]] — how a contract sits on top of the plan catalogue.
- [[details-billing]] — billing transactions, including LTA charges.
- [[subscription-details]] — the subscription tied to the account.
- [[account-plan]] — the current plan / subscription summary.

## Open questions

- The full field list on the individual `/admin/contracts/{id}` contract page (verify against the live contract view).
