---
type: feature
nav_path: "Payment Providers → BNP Paribas Personal Finance → Market positioning"
route_name: apps.bnp.settings
route_path: /admin/payment-providers/bnp
aliases: ["BNP positioning", "BNP vs Fibank vs DSK", "Bulgarian consumer credit providers", "BNP credit grouping", "BNP plan tier", "which credit provider", "Postbank lending partner"]
tags: [paymentproviders, payment-providers, bnp, bulgaria, credit, positioning, postbank]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-bnp]]. See the hub for the other aspects (credit flow, settings & fields, eligibility & promotions).

# BNP — market positioning

## Purpose

This page answers "**which** Bulgarian consumer-credit provider should I enable, and where does BNP fit?". It explains why CloudCart ships three competing credit providers, how the merchant picks between them, and how BNP is grouped as a `credit`-type payment (distinct from regular card / bank payments) in the admin and storefront. It is the page to read for "BNP vs Fibank vs DSK" comparison questions.

## Where to find it

The credit-provider choice is made on the global payment-providers list (Sidebar → **Payment Providers**) where each provider is installed or uninstalled — see [[settings-payment-providers]]. BNP's own panel is at `/admin/payment-providers/bnp`.

## What the merchant can do here

- **Pick the one credit provider that matches the merchant's bank contract** (BNP / Fibank / DSK / UCF) and install only that one.
- **Offer an installment / BNPL option** on the cart through the chosen provider.
- **Rely on the `credit` payment grouping** so credit orders are visually distinguished from regular card / bank-transfer orders.

## Settings & fields

This aspect carries no fields of its own — positioning is reflected in the provider grouping rather than in a settings form. The relevant behaviour:

| Aspect | Behaviour |
|--------|-----------|
| **Payment group** | BNP is in the `credit` group, not `regular`. |
| **Order colour class** | Credit orders render with `order-payment-color-credit`. |
| **Storefront grouping** | BNP is grouped with other credit / financing options at checkout, separate from card / bank-transfer methods. |
| **Plan-tier gate** | None declared (`plan_gates: []`). Any plan that can install payment providers can install BNP. |

## Business rules

### Credit-payment grouping

BNP is a credit-payment type — group = "credit" rather than "regular". This is reflected in the order's color class (`order-payment-color-credit`) and in the storefront grouping. The order does not follow the standard card-payment status flow; the underwriting outcome drives the final status — see [[bnp-credit-flow]].

### Bulgarian-credit positioning (verified)

CloudCart ships three Bulgarian-market consumer-credit providers because Bulgarian merchants typically have a contract with one (and only one) bank. The right pick depends entirely on which bank already underwrites the merchant:

- **BNP Paribas Personal Finance** (this provider) — for merchants whose lending partner is Postbank.
- **[[payment-providers-fibank-bnpl|Fibank E-Credit]]** — for merchants whose lending partner is Fibank.
- **[[payment-providers-dsk-bnpl|DSK Mig Credit]]** — for merchants whose lending partner is DSK Bank.

All three solve the same merchant problem (offer an installment / BNPL option on cart) but route the underwriting through different banks. The merchant enables exactly the one their bank contract points at. A fourth option, [[payment-providers-smart-ucf|Smart / UCF]] (UniCredit Bulbank-affiliated), exists for merchants whose lending partner is UCF.

## Related

- [[payment-providers-bnp]] — hub.
- [[bnp-credit-flow]] — why BNP doesn't follow the standard card-payment status flow.
- [[payment-providers-fibank-bnpl]] — Fibank consumer credit (BNPL flavour).
- [[payment-providers-dsk-bnpl]] — DSK consumer credit.
- [[payment-providers-smart-ucf]] — UniCredit Bulbank-affiliated credit provider (UCF).
- [[settings-payment-providers]] — global list where the chosen provider is installed.
- [[payment-provider]] — entity definition.
- [[payment-status]] — credit-flow status mapping.

## Open questions

(none)
