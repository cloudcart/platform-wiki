---
type: entity
nav_path: "Entity → Tax / Fee → VAT vs Fee discrimination"
aliases: ["VAT vs Fee", "Tax vs Fee", "vat flag", "Single-winner VAT", "Stacking Fees", "Fee VAT compounding"]
tags: [entity, taxes, fees, vat, type-discrimination]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax]]. See the hub for the other aspects (attributes, overrides, order snapshot, validation, business rules).

# Tax / Fee — VAT vs Fee discrimination

## Identity

How the platform distinguishes a Tax row from a Fee row, what changes between the two at the entity level (form fields, validators), and the radically different **runtime semantics** that follow from the locked-on-create `vat` flag. This is the single most-misunderstood split in [[settings-taxes]] — merchants routinely create a Fee thinking they're configuring VAT, or vice versa.

## Aliases

- **Tax vs Fee** — the canonical merchant-facing split in the Add modal.
- **`vat` flag** — the persisted column that records the pick.
- **Single-winner VAT** — runtime behaviour for `vat = yes` rules.
- **Stacking Fees** — runtime behaviour for `vat = no` rules.

## Key Attributes

| Aspect | Tax (`vat = yes`) | Fee (`vat = no`) |
|--------|-------------------|------------------|
| **Add modal** | Add Tax button | Add Fee button |
| **Rate type radio** | Hidden — percent-only via UI | Visible at top of form (Percent / Flat) |
| **`price_with_vat`** | Toggleable (`0` net, `1` gross) | **FORCED to `0`** at save validator |
| **`shipping`** | `yes` default — bucketing flag, no UI toggle | **FORCED to `no`** at save validator |
| **`oss_registration`** | Visible when target = `regions` | Not applicable |
| **`without_vat_reasons` / `_non_eu`** | Visible (max 64k chars each) | Not applicable |
| **`payment_active` / `payment_provider`** | Not applicable | Visible — Fee-only scoping switch |
| **`shipping_active` / `shipping_provider`** | Not applicable | Visible — Fee-only scoping switch |
| **`categories[]` overrides** | Available | Not applicable |
| **Uniqueness per zone** | Only ONE VAT rule per [[geo-zone]] | No uniqueness check — multiple Fees can target the same zone |
| **Locked at create?** | Yes — cannot convert to Fee by editing | Yes — cannot convert to Tax by editing |

## Why the `vat` flag is locked

The Vue form does send `vat` in the payload on edit, but the save controller hard-forces the value from the **original** entity-type pick — any submitted value is overwritten. The merchant's only path to "change a Fee into a Tax" or vice versa is delete + re-create.

This matters because Fees and Taxes obey completely different picking semantics at checkout (below), and silently allowing a flip would corrupt every historical order's snapshot interpretation.

## Runtime semantics — the load-bearing distinction

### VAT (`vat = yes`) picks ONE winner per order

The engine walks every `vat = yes` rule that matches the customer's resolved address, sorts by **regional-beats-rest-of-world** then **newest-zone-wins**, and returns exactly **one** rule. Three VAT rules that all match a Bulgarian order = ONE applied (the newest). See [[tax-rate-selection]] for the full filter chain.

### Fees (`vat = no`) ALL stack additively

Every Fee that matches its conditions applies. Each appears as a **separate line** on the order total / invoice. Three Fees that all match the order = three applied lines. See [[tax-fees-vs-vat]] for the full additive model.

### Country-only matching restriction is VAT-only

For VAT, the engine only evaluates **country-level rules** inside a [[geo-zone]] — city / region / polygon / distance / post-code rules are ignored. For Fees, the **full** geo-zone scope is honoured (all 11 zone-value operations). A merchant who builds a zone purely from polygons + post-codes will have it work for Fees but silently match NO VAT.

### Fee VAT does NOT compound

A Fee with `vat = yes` set in the payload (the flag is overwritten on save, so this scenario is mostly hypothetical, but for historical Fee rows persisted via direct DB writes or older code paths): VAT is computed on the **Fee amount only** — it does NOT compound on the cart's already-computed VAT. The Fee's VAT line appears as its own line on the invoice; there is no double-VAT calculation.

The flag does NOT control whether VAT is applied TO the fee's amount — see [[settings-taxes]] *"The `vat` flag on a fee does NOT control whether VAT is applied to the fee"*.

## Examples

**Scenario 1 — three VAT rules match a BG order:**

- Rule A: 20% standard VAT, [[geo-zone]] = "Bulgaria", created 2024-01-01
- Rule B: 22% VAT, [[geo-zone]] = "EU", created 2024-06-01
- Rule C: 18% rest-of-world VAT, target = `restofworld`

Result: Rule B wins (regional, newest). Rules A and C are discarded for this order.

**Scenario 2 — three Fees match a credit-card order shipped via Speedy:**

- Fee X: 5 BGN COD handling, `payment_active = target`, `payment_provider = cod`
- Fee Y: 2 BGN credit-card surcharge, `payment_active = target`, `payment_provider = stripe`
- Fee Z: 1 BGN insurance, `shipping_active = target`, `shipping_provider = speedy`

Result: Fee Y + Fee Z BOTH apply (Fee X is skipped — payment doesn't match). Two additive Fee lines on the order.

## Where it appears

- [[settings-taxes]] — the management screen carrying both Add Tax and Add Fee buttons.
- [[tax]] — entity hub.
- [[orders-details]] — order totals show one VAT line + N Fee lines.

## Related

- [[tax]] — hub.
- [[tax-entity-attributes]] — the form fields per sub-type.
- [[tax-rate-selection]] — VAT single-winner picker.
- [[tax-fees-vs-vat]] — Fee additive model.
- [[geo-zone]] — the zone container.
- [[settings-taxes]] — management screen.

## Open Questions

None.
