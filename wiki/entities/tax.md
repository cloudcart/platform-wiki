---
type: entity
nav_path: "Entity → Tax / Fee"
aliases: ["Tax", "Fee", "VAT", "Tax rate", "VAT rate", "Surcharge", "Handling fee", "Данък", "ДДС", "Такса", "Данъчна ставка"]
tags: [entity, taxes, fees, vat, finance, invoicing]
plan_gates: []
created: 2026-05-24
updated: 2026-06-10
source_count: 1
---

# Tax / Fee

## Identity

A **Tax / Fee** is a rate or charge the platform applies to an order at checkout based on the customer's country, the products in the cart, and (for Fees) the selected payment / shipping method. The two share a single management screen — [[settings-taxes]] — and a single storage table, but they answer two different merchant questions:

- A **Tax** (*"how much VAT should I withhold from this sale?"*) is a jurisdiction-bound charge that picks **ONE winner per order**.
- A **Fee** (*"what surcharge should I add for this payment / shipping method?"*) is an additive surcharge where **ALL matching rules stack**.

Each rule carries a name, a rate (percent or flat amount), a target scope (rest-of-world fallback or specific [[geo-zone]]), a VAT flag, and optional per-region / per-category overrides. Once an order is placed, the engine snapshots the applied tax lines onto the order so historical invoices stay accurate even when the merchant later edits the rate — see [[tax-entity-snapshot]] for the snapshot lifecycle and [[tax-computation]] for the full picker logic.

A Tax is distinct from a [[discount]] (a merchant promotion subtracted from the total) and from a [[shipping-provider|shipping cost]] (a courier charge) — though VAT can apply on top of shipping via the rule's `shipping` bucketing flag.

## Aliases

- **Tax** / **Fee** — the canonical merchant-facing terms in the admin UI ([[settings-taxes]] page title: *"Taxes and fees"*).
- **VAT** / **VAT rate** — used when the rule is specifically a value-added-tax line (`vat = yes`).
- **Surcharge** / **Handling fee** — informal merchant phrasing for Fees (e.g., *"COD handling fee"*, *"credit-card surcharge"*).
- **Данък** / **ДДС** / **Такса** / **Данъчна ставка** — Bulgarian terms; *"ДДС"* specifically refers to VAT, *"Такса"* to a Fee.

## Sub-pages (in this cluster)

Six aspect pages — drill into the one that matches the question:

- [[tax-entity-attributes]] — full attribute catalogue + save-time normalization (`saving` hook) + persistence quirks (no parent timestamps; integer-cent rate storage).
- [[tax-entity-vat-vs-fee]] — Tax-vs-Fee discrimination; **locked-on-create `vat` flag**; single-winner VAT vs additive Fees; country-only-matching restriction for VAT; Fee VAT does not compound.
- [[tax-entity-overrides]] — per-region + per-category override mechanics; precedence ladder; primary-category-only matching; maps-API-key dependency.
- [[tax-entity-snapshot]] — three lifecycle phases (Defined → Applied → Snapshotted); why historical invoices stay accurate; mid-order recompute uses CURRENT rules (mixed-rate orders).
- [[tax-entity-vat-validation]] — VIES, APIS Trade Register, HMRC, CH manual; fail-soft synchronous validation; reverse-charge mechanics; how validation feeds `isWithVat`.
- [[tax-entity-business-rules]] — `invoicing_address` choice; settings cache flush; no bulk import; no delete protection; no tax-breakdown CSV; OSS threshold is manual; per-zone VAT uniqueness; validator quirks; invented legacy terms to avoid.

## Key Attributes

Quick reference — the **full table** with all per-field notes is on [[tax-entity-attributes]]. Top-level shape:

| Attribute | Type | Tax | Fee |
|-----------|------|-----|-----|
| `name` | string, max 100 | required | required |
| `tax` (rate) | numeric — stored as cents | required, percent cap 90 | required |
| `type` | enum `percent` / `flat` | percent-only via UI | radio at top of form |
| `vat` (sub-type discriminator) | enum `yes` / `no` | `yes` (locked) | `no` (locked) |
| `target` | enum `restofworld` / `regions` | both | both |
| `geo_zone_id` | FK → [[geo-zone]] | required when target = `regions` | same |
| `price_with_vat` | bool | toggleable | **forced to `0`** |
| `shipping` (bucketing) | enum `yes` / `no` | default `yes`, no UI toggle | **forced to `no`** |
| `oss_registration` | bool | visible when target = `regions` | n/a |
| `regions[]`, `categories[]` | repeatable | both available | n/a |
| `without_vat_reasons`, `_non_eu` | string, max 64,000 | available | n/a |
| `payment_active`, `payment_provider` | transient + nullable FK | n/a | available |
| `shipping_active`, `shipping_provider` | transient + nullable FK | n/a | available |

## Relationships

A Tax / Fee:

- **Belongs to** at most one [[geo-zone|Geo Zone]] via `geo_zone_id` — required only when `target = regions`. Country rules inside the zone drive VAT matching; richer zone operations are ignored for tax (used only by [[shipping-calculation]]).
- **References** zero-or-more product categories via `categories[]` (Tax only) — see [[tax-entity-overrides]].
- **References** at most one payment provider via `payment_provider` and at most one shipping provider via `shipping_provider` (Fee only). No per-provider rate-override map.
- **Is snapshotted onto** every [[order|Order]] at create time — see [[tax-entity-snapshot]].
- **Is printed on** every [[invoice|Invoice]] and [[credit-note|Credit Note]] from the order snapshot, not the current rule.

A Tax / Fee is **distinct from** [[discount]] (subtractive promotion vs additive / contained charge).

## Where it appears

- [[settings-taxes]] — the master management screen (list + create + edit).
- [[settings-geo-zones]] — the zone the rule targets; country rules inside the zone drive tax matching.
- [[settings-cart]] — `invoicing_address` decides which customer address the engine reads; `checkout_validate_company_vat` toggles VIES validation.
- [[settings-general]] — `operation_country` is the default VAT jurisdiction when OSS is off.
- [[settings-invoicing]] — invoice and credit-note templates print the tax breakdown + *"without VAT reasons"* wording.
- [[orders-details]] — every order's totals section displays the per-line and total tax breakdown.
- [[orders-invoice]] — the issued invoice carries the snapshotted tax values.
- [[orders-credit]] — credit notes carry the same tax values.
- [[orders-receipt]] — cash receipts include the tax breakdown.
- [[checkout-flow]] — where the engine fires for the customer's cart.

## Related

- [[tax-computation]] — concept page on how the engine picks the applied tax, snapshots it, and reverses it on credit notes.
- [[geo-zone]] — the zone entity; tax matching uses ONLY country rules in zones.
- [[order]] — every order carries a tax snapshot.
- [[invoice]] — issued against an order; prints the tax breakdown.
- [[credit-note]] — issued against an order; reverses the tax line in the accounting trail.
- [[discount]] — a merchant promotion that subtracts from the total.
- [[product]] — product pricing is entered in the chosen pricing model.
- [[category]] — per-category overrides reference categories.
- [[payment-provider]] — Fees can target specific payment providers.
- [[shipping-provider]] — Fees can target specific shipping methods.
- [[multi-currency]] — concept page on currency conversion for flat-amount Fees.
- [[checkout-flow]] — where the tax engine fires.
- [[geo-targeting]] — concept page on geo-scoping mechanics.
- [[discount-stacking]] — discounts interact with the post-tax total.
- [[settings-payment-providers]] — referenced by Fees with `payment_active = target`.
- [[settings-invoicing]] — invoice / credit-note template + numbering.
- [[billing-invoicing]] — concept page on the merchant's OWN platform-billing invoices (separate from store-side invoicing).

## Open Questions

None — all previously-flagged items resolved or distributed to sub-pages.
