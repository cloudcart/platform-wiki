---
type: concept
nav_path: "Concept → Tax computation → Fees vs VAT"
aliases: ["Tax vs fee", "vat flag fee", "vat=no fee", "VAT on fee", "Fee stacking", "Additive fees", "Cash-on-delivery fee", "Payment surcharge fee", "shipping flag tax.before tax.after"]
tags: [taxes, vat, finance, fees, stacking, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax-computation]]. See the hub for the other aspects (rate selection, pricing models, overrides, OSS, address resolution, order snapshot).

# Tax — fees vs VAT

## Definition

Fees and VAT rules share the **same** [[settings-taxes]] management UI and the same storage table, but at runtime they behave fundamentally differently. A row's **`vat`** flag is the discriminator:

- **`vat = yes`** → jurisdiction-bound VAT rule. **One winner per order** (the rate is a percentage applied to the taxable base). Picked by [[tax-rate-selection]].
- **`vat = no`** → fee. A flat or percentage surcharge bound to a payment / shipping method. **ALL matching fees stack additively.**

A second clarification this page documents: **VAT is applied to fees** REGARDLESS of their own `vat = no` setting — the flag means *"this is a fee, not a VAT rate"*, NOT *"this fee is VAT-exempt"*.

## Scope

Covered:

- The discriminating `vat` flag and what it actually means.
- VAT-on-fee correction — fees DO get VAT applied on top.
- Fee scoping fields (`payment_active`, `shipping_active`, geo zone).
- The "fees stack, taxes don't" asymmetry.
- The `shipping` flag bucketing (`tax.before` vs `tax.after`) — corrected.
- Common fee patterns (COD, payment surcharge, currency conversion).

Not covered here:

- The single-winner VAT picker — see [[tax-rate-selection]].
- How fee amounts snapshot onto the order — see [[tax-order-snapshot]].
- How `allow_modify_vat` on a shipping quote decides VAT-on-shipping — see [[shipping-calculation]].

## The `vat` flag — what it actually means

**Critical clarification.** The `vat` flag on a [[settings-taxes]] row does NOT mean *"is this row itself VATable"*. It means *"is this row a VAT rule or a fee"*. VAT is applied to fees **REGARDLESS** of their own `vat = no` setting — when the store has any active VAT rule for the customer's region (and the customer isn't B2B VAT-exempt). See [[settings-taxes]] for the verified behaviour.

Runtime semantics:

- `vat = yes` → row participates in the rate-selection ladder. One winner per order.
- `vat = no` → row is a fee. Every matching fee fires. **The fee amount itself is subject to VAT** if any VAT rule is active for the customer.

## Fees stack additively

ALL matching fees apply to every order — there's no winner-picking. Fees are scoped by:

- **Geo zone** (same `target` / `geo_zone_id` fields as VAT — but with the **full operation scope**, not VAT's country-only restriction).
- **Payment method** — `payment_active = global` OR `payment_active = target` + `payment_provider_values[]`.
- **Shipping method** — `shipping_active = global` OR `shipping_active = target` + `shipping_provider_values[]`.

Each matching fee appears as a **separate line** on the order total. Three fees that all match → three lines on the invoice.

### Common fee patterns

- **Payment surcharge** — 2% for credit-card payments. `payment_active = target`, `rate = 2`, `type = percent`.
- **Cash-on-delivery handling** — 5 BGN flat. `payment_active = target`, `rate = 5`, `type = flat`.
- **Non-EUR currency conversion fee** — 1% on orders in non-EUR currencies. `target = regions`, zone = "non-EUR countries", `rate = 1`, `type = percent`.

## Fees use the full geo-zone scope (unlike VAT)

The country-only restriction is for VAT. **Fees use the full geo-zone scope** — all 11 zone-value operations (country, region, city, polygon, distance, post-code, neighbourhood, etc.) — so a fee can target *"Sofia city only"* and it will fire when the customer's address resolves to a Sofia-area cart. This is a subtle but important asymmetry: a zone that's useless for VAT can still be used to scope a fee. See [[tax-rate-selection]] for the VAT country-only restriction.

## The `shipping` flag — `tax.before` vs `tax.after` bucketing

**Important clarification.** Older wiki phrasing framed the `shipping` flag as *"controls whether the same tax rate also applies to the shipping cost line"*. **That is misleading.** The flag's actual job is to decide WHEN in the totals pipeline the rule fires:

- **`shipping = no`** — fires in the **`tax.before`** bucket (before shipping is calculated). Standard for ordinary VAT rules and most fees.
- **`shipping = yes`** — fires in the **`tax.after`** bucket (after shipping is calculated). Used when the rule needs to see post-shipping totals.

**Whether VAT applies to the shipping line itself is a SEPARATE mechanism** — driven by the shipping quote's own `allow_modify_vat` flag (set by each shipping provider integration), not by the Tax row's `shipping` flag. See [[shipping-calculation]]. For most merchants this distinction is invisible — domestic VAT rules use `shipping = no` (the default) and shipping is taxed via the provider's own VAT handling.

## Contrasts

- **Fees stack additively vs VAT picks one winner** — three fees all match → all three apply, three invoice lines. Three VAT rules all match → ONLY ONE applies. This asymmetry surprises merchants — the VAT picker is singular, the fee picker is additive.
- **`vat = no` on a fee ≠ "fee is VAT-exempt"** — it just means "this row is a fee, not a VAT row". VAT is still computed against the fee amount and added on top (or extracted from inside the fee in GROSS stores — see [[tax-pricing-models]]).
- **Fee's full-scope geo-zone vs VAT's country-only geo-zone** — fees can target city / polygon / post-code, VAT cannot.
- **`shipping = yes`/`no` (bucketing) vs `allow_modify_vat` (VAT-on-shipping decision)** — two unrelated mechanisms. The `shipping` flag picks the pipeline bucket; `allow_modify_vat` decides whether the shipping line itself gets VAT.

## Worked example — cash-on-delivery fee with VAT on top

Setup:

- Fee rule: `name = "COD handling"`, `rate = 5`, `type = flat`, `vat = no`, `payment_active = target`, `payment_provider_values = [COD provider id]`.
- Store has an active VAT rule for Bulgaria at 20% (`vat = yes`, `price_with_vat = 0` NET, customer is Bulgarian B2C).

Result:

- Carts paid by COD get a `5.00 BGN` handling fee added. Other payment methods skip it. The fee shows as a separate line on the order.
- **VAT IS ALSO applied to this fee** because the customer's region has an active VAT rule and the customer isn't B2B VAT-exempt. Older wiki phrasing claimed *"Because `vat = no`, no VAT is added on top of the fee."* That was wrong — VAT is computed against the fee amount and added to the order's VAT line (or extracted from inside the fee in GROSS stores — see [[tax-pricing-models]]).

## Worked example — three fees stacking

Setup: Fee A (2% credit-card surcharge), Fee B (1% non-EUR conversion fee), Fee C (5 BGN flat handling for Speedy).

A customer pays by credit card, in BGN, with Speedy shipping → only A and C match. Two fee lines on the invoice. If the merchant ALSO defines a VAT rule for Bulgaria, both fees are taxed on top.

## Negative tax not allowed

The validator rejects negative tax rates both client-side (Zod schema: `tax: z.number.min(0)`) and server-side. To express a *"discount on tax"* the merchant must use a Discount rule (a [[marketing-discounts]] discount applied at checkout), not a negative tax or a negative fee.

## Where it applies

- [[settings-taxes]] — same management screen as VAT rules; `vat = no` rows are fees.
- [[settings-payment-providers]] — fees can scope to specific payment providers.
- [[settings-shipping]] — fees can scope to specific shipping methods.
- [[shipping-calculation]] — `allow_modify_vat` on a shipping quote drives VAT-on-shipping (separate from the `shipping` flag on a Tax row).
- [[orders-details]] — fee lines show separately in the order total.

## Related

- [[tax-computation]] — hub.
- [[settings-taxes]] — management screen.
- [[tax-rate-selection]] — VAT single-winner picker (contrast).
- [[tax-pricing-models]] — GROSS vs NET (decides whether VAT is added on top of or extracted from the fee).
- [[shipping-calculation]] — `allow_modify_vat` for VAT-on-shipping.
- [[settings-payment-providers]] / [[settings-shipping]] — provider scoping fields.
- [[marketing-discounts]] — the right tool for a *"discount on tax"* effect.

## Open Questions

None.
