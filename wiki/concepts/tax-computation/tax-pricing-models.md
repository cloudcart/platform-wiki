---
type: concept
nav_path: "Concept → Tax computation → Pricing models"
aliases: ["Pricing models", "Gross vs net pricing", "VAT-inclusive vs VAT-exclusive", "price_with_vat", "Price includes VAT", "Price excludes VAT", "GROSS pricing", "NET pricing"]
tags: [taxes, vat, finance, pricing, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax-computation]]. See the hub for the other aspects (rate selection, overrides, OSS, address resolution, order snapshot, fees-vs-VAT).

# Tax — pricing models (GROSS vs NET)

## Definition

The **`price_with_vat`** flag on each [[settings-taxes]] VAT rule decides whether the product prices the merchant enters already contain VAT (GROSS) or sit below VAT (NET). The flag drives both how the storefront displays the price AND how the engine extracts vs adds the tax portion at checkout.

- **`price_with_vat = 1`** — GROSS. Common in EU consumer stores.
- **`price_with_vat = 0`** — NET. Common in US and B2B EU stores.

The flag is **per VAT rule**, not store-wide — though in practice merchants set it the same way across all their rules.

## Scope

Covered:

- Both flag values and the arithmetic each triggers.
- Storefront display difference (gross vs net).
- Invoice-rendering implication.
- Interaction with the per-product price entry in the [[product]] catalog.

Not covered here:

- Which VAT rule was picked — see [[tax-rate-selection]].
- How the resulting amount snapshots onto the order — see [[tax-order-snapshot]].
- Multi-currency conversion of flat fees — see [[multi-currency]].
- B2B reverse-charge zero-rating (separate flow from gross/net) — see [[tax-oss-semantics]].

## GROSS (`price_with_vat = 1`)

The product price the merchant enters (e.g., `24.00 BGN`) ALREADY includes VAT.

At checkout the engine computes the tax portion **backwards**:

- At 20% VAT: net = `24.00 / 1.20 = 20.00 BGN`, VAT = `24.00 − 20.00 = 4.00 BGN`.
- The storefront shows `24.00 BGN`.
- The invoice shows both gross AND the implied tax.

This is the typical EU consumer pattern — shoppers see the price they pay, and the breakdown only appears on the invoice.

## NET (`price_with_vat = 0`)

The price the merchant enters (e.g., `20.00 BGN`) is the **net** amount, exclusive of VAT.

At checkout the engine **adds VAT on top**:

- At 20% VAT: VAT = `20.00 × 0.20 = 4.00 BGN`, gross = `24.00 BGN`.
- The storefront shows `20.00 BGN` (or `20.00 BGN + VAT`, theme-dependent).
- The customer sees tax appear as a **separate line** at checkout.

This is the typical US B2C pattern (no all-in pricing) and the typical EU B2B pattern (advertise net, the buyer adds VAT for their own accounting).

## Contrasts

- **GROSS vs NET** — the entire pricing-display layer hinges on this flag. Switching it after the catalog is built effectively re-prices every product on the storefront.
- **Per-rule vs store-wide** — the flag is on each VAT rule, so theoretically a store could have a GROSS rule for retail customers and a NET rule for wholesale. In practice merchants align all rules.
- **GROSS storefront vs GROSS invoice** — the storefront shows one number; the invoice shows the implied breakdown. Customers occasionally complain *"the invoice shows 4.00 VAT but my checkout said 24.00, did I get charged extra?"* — no, the invoice is just decomposing the same 24.00.

## Where it applies

- [[product]] — every product price is entered in the merchant's chosen pricing model.
- [[settings-taxes]] — the `price_with_vat` flag lives on each VAT rule row.
- [[checkout-flow]] — the engine extracts or adds VAT according to the flag.
- [[orders-invoice]] / [[settings-invoicing]] — the invoice rendering decomposes the gross total when needed.

## Worked examples

### Bulgarian gross-priced store (most common BG merchant)

Setup:

- One VAT rule: `name = "VAT 20%"`, `rate = 20`, `type = percent`, `vat = yes`, `price_with_vat = 1`, `target = restofworld`, `oss_registration = 0`.
- Merchant enters product prices INCLUDING VAT (e.g., `24.00 BGN`).

Result:

- Storefront shows `24.00 BGN`.
- Invoice shows: net `20.00`, VAT `4.00`, total `24.00`.
- All customers — Bulgarian and non-Bulgarian — see 20% VAT applied. (Without OSS, even cross-border EU sales are taxed at 20% BG VAT — see [[tax-oss-semantics]].)

### NET-pricing B2B store

Setup:

- One VAT rule: `rate = 20`, `price_with_vat = 0`.
- Merchant enters net prices (e.g., `20.00 BGN`).

Result:

- Storefront shows `20.00 BGN` (or `20.00 BGN + VAT`, theme-dependent).
- Checkout adds `4.00 BGN` VAT line → total `24.00 BGN`.
- For B2B buyers with valid VIES VAT numbers, the reverse-charge flow kicks in and the VAT line goes to 0 — see [[tax-oss-semantics]].

## Related

- [[tax-computation]] — hub.
- [[settings-taxes]] — the `price_with_vat` flag lives here.
- [[product]] — product price entry uses the merchant's pricing model.
- [[orders-invoice]] / [[settings-invoicing]] — invoice rendering uses the model to decompose the displayed total.
- [[multi-currency]] — currency conversion (percentage taxes are currency-independent; flat fees aren't).

## Open Questions

None.
