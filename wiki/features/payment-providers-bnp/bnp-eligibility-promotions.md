---
type: feature
nav_path: "Payment Providers → BNP Paribas Personal Finance → Eligibility & promotions"
route_name: apps.bnp.promo
route_path: /admin/payment-providers/bnp
aliases: ["BNP promotions", "BNP promotion management", "BNP good categories", "BNP good types", "BNP financing schemes", "BNP type ID", "BNP eligibility", "BNP minimum order price", "BNP POS ID 2", "BNP two POS IDs"]
tags: [paymentproviders, payment-providers, bnp, bulgaria, credit, promotions, eligibility, postbank]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-bnp]]. See the hub for the other aspects (credit flow, settings & fields, market positioning).

# BNP — eligibility & promotions

## Purpose

This page covers **what BNP can be offered on and on what terms** — the minimum order price below which BNP is hidden, the two-POS-ID routing that sends BNP-branded-card schemes through a separate POS, and the promotions page where the merchant manages financing schemes and tags products / categories with their BNP type ID. It is the page to read for "why doesn't BNP show on this order / product?" and "how do I set up installment plans?".

## Where to find it

Minimum price + the two POS IDs are configured on the main BNP settings panel (Sidebar → **Payment Providers** → **BNP Paribas Personal Finance**) — see [[bnp-settings-fields]]. The financing-scheme and good-type management lives on a separate admin page at `route('admin.bnp.promo')`.

## What the merchant can do here

- **Set the minimum order price** (`min_price`) below which BNP is hidden from checkout.
- **Configure the second POS ID** (`pos_id2`) used for BNP-branded-card schemes.
- **Define / select BNP good categories and good types** on the promo page.
- **Configure promotional financing schemes** (month counts, interest, down payment).
- **Tag products and categories** with the matching `bnp_type_id` so BNP underwrites each item correctly.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Minimum price** (`configuration.min_price`) | Order total below which BNP is hidden from checkout. | 75 BGN | Required. Lives on the main settings panel — see [[bnp-settings-fields]]. |
| **POS ID 2** (`configuration.pos_id2_test`, `pos_id2_live`) | Separate POS used for BNP-branded-card schemes. | Empty | Optional. |
| **BNP good categories** | High-level financing-product categories Postbank offers. | — | Managed on the promo page (`admin.bnp.promo`). |
| **BNP good types** | Drilldown product types within each category; each has a `GoodTypeId`. | — | Maps to `bnp_type_id` on products / categories. |
| **Promotional financing schemes** | Month counts (6, 9, 12, 18, 24, etc.), interest rates, down-payment requirements. | — | Surfaced to the customer at checkout. |
| **`bnp_type_id`** (on products / categories) | Tag that links a product / category to a BNP good type. | Empty | Set via the BNP type ID columns on products and categories. |

## Business rules

### Minimum order price

BNP financing only applies to orders above a configurable minimum (`min_price`, default **75 BGN**). Below this, BNP is hidden from the checkout entirely. This matches Postbank's underwriting minimums — BNP doesn't underwrite tiny loans for transaction-cost reasons.

### Two POS IDs — pos_id and pos_id2

The integration supports two parallel POS IDs:

- **`merchant_id` / `merchant_id_live`** — the merchant's main POS, used by default.
- **`pos_id2`** — a separate POS used specifically for **BNP-branded cards** (a BNP credit card product). When the customer's session has `bnp_pos2=true` set (the storefront sets this when the chosen scheme is a BNP-card scheme), the integration switches the POS ID to `pos_id2` at request time.

This dual-POS arrangement is dictated by Postbank's product split — BNP cardholders get different underwriting limits / interest rates than non-cardholders, and Postbank routes the two via separate POS IDs.

### BNP promotion management

A separate admin page at `admin.bnp.promo` manages:

- **BNP good categories** — the high-level financing-product categories Postbank offers.
- **BNP good types** — drilldown product types within each category. Each type has a `GoodTypeId` that maps to a `bnp_type_id` on the merchant's products and categories.
- **Promotional financing schemes** — month counts (6, 9, 12, 18, 24, etc.), interest rates, down-payment requirements. Surfaced to the customer at checkout.

Merchants tag their products and categories with the appropriate `bnp_type_id` so BNP can underwrite each item correctly. The scheme the customer picks at checkout drives the financial parameters sent to BNP — see [[bnp-credit-flow]] for what is submitted at order placement.

## Related

- [[payment-providers-bnp]] — hub.
- [[bnp-settings-fields]] — where `min_price` and the two POS IDs are entered.
- [[bnp-credit-flow]] — how the chosen scheme + tagged products are submitted to BNP at checkout.
- [[payment-provider]] — entity definition.
- [[checkout-flow]] — storefront checkout where the scheme dropdown appears.

## Open questions

(none)
