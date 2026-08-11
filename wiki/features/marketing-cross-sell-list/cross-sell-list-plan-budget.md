---
type: feature
nav_path: "Marketing → UpSell & Cross-sell → Cross-Sell List → Model & plan budget"
route_name: admin.cross_sell.list
route_path: /admin/marketing-new/cross-sell
aliases: ["Cross-Sell plan budget", "Cross-Sell slot limit", "Cross-Sell master records only", "Cross-Sell vs UpSell model"]
tags: [marketing, cross-sell, list, plans, model]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-cross-sell-list]]. See the hub for the other aspects (grid & metrics, actions, validation).

# Cross-Sell List — model & plan budget

## Purpose

This aspect documents the **structural model** behind the list — why it shows master records only, how delete removes any attached legacy child offers, the **per-plan slot budget** enforced at save time, and the separation between Cross-Sell and UpSell as distinct features.

## Where to find it

These rules govern the list at `/admin/marketing-new/cross-sell` and the save endpoints reached from the offer editor. The merchant sees their consequences in the "(N remaining)" counter on the Add button and in the one-row-per-offer layout of the grid.

## What the merchant can do here

The merchant experiences these rules rather than configuring them: they see one row per offer, toggle each offer's status independently, and hit a plan-limit error when their slot budget is exhausted. Raising the slot budget means upgrading the plan (see [[plans]]).

## Settings & fields

There are no editable settings in this aspect. The relevant values are read-only signals:

- The **"(N remaining)"** slot counter on the Add button (from `admin.common.remaining/cross_sell`).
- The **`cross_sells`** per-plan feature counter that caps total active records.

## Business rules

### List shows master records only

The grid filters to master records (`parent = 1`) — so it shows one row per offer. Any legacy multi-step chain shows exactly **one** row (its root); the empty-state is driven by the master-only count.

### Each row opens the offer's diagram page

Clicking a row's title opens the offer's **diagram page** (its summary card + Edit modal) — that is the only path into the offer.

### Status is a single-record toggle

The Active switch updates only that offer's status — there is **no** chain / subtree cascade. Each offer is independent (see [[cross-sell-list-actions]] for the toggle UI).

### No duplicate action

There is no "duplicate offer" action. To make a similar offer the merchant creates a new one.

### Plan-tier slot count is a real gate, enforced at save time

`cross_sells` is a per-plan feature counter — each plan tier (free / starter / pro / unicorn) caps the **TOTAL** number of Cross-Sell records. Each offer counts as one slot (legacy multi-step chains also counted every descendant record, so an old 3-step chain consumed 3 slots). The "(N remaining)" label shows the current allowance; when 0, the server rejects new Cross-Sell creates with a plan-limit error. See [[plans]].

### Products limit max 10 — capped in validation

The `products_limit` (how many products surface in one popup) is hard-capped at 1-10 by the validator and is platform-wide, not a plan-tier setting — see [[cross-sell-list-validation]] for the rule.

### Side effects on save

- A new offer becomes live immediately if Active **and** within its `active_from` / `active_to` window.
- Targets, actions, and meta are wired in a single DB transaction in the Cross-Sell store endpoint — partial saves are impossible.
- The `views` / `added_to_cart` / `total_cancel` counters update in real time as customers interact with the popup (these feed the [[cross-sell-list-grid]] columns).

## How it works

### Cross-Sell vs UpSell — distinct list / model

Cross-Sell and UpSell are **separate features** with separate database tables (`cross_sell` and `up_sell`), separate REST endpoints (`/admin/api/core/marketing/cross-sell` vs `/up-sell`), and separate plan counters (`cross_sells` vs `upsells`). They share only the **page shape** — each has its own list page and its own `/diagram/:id` offer editor.

### Permission gate

The whole list is gated by the `cc_apps_purchase:up_cross_sell` middleware — the Up/Cross-Sell app (see [[apps-up-cross-sell]]) must be installed, the same gate UpSell uses.

## Related

- [[marketing-cross-sell-list]] — hub.
- [[plans]] — sets the per-plan `cross_sells` slot budget enforced at save time.
- [[apps-up-cross-sell]] — the gateway app whose middleware gates the list and save endpoints.
- [[marketing-up-sell-list]] — the sister feature this one is structurally distinct from.
- [[marketing-up-sell-diagram]] — the offer editor / diagram page (same page shape for Cross-Sell and UpSell).

## Open questions

No outstanding questions.
