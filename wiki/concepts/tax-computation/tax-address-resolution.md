---
type: concept
nav_path: "Concept → Tax computation → Address resolution"
aliases: ["Tax address resolution", "Billing vs shipping address", "invoicing_address", "Address snapshot", "Tax address priority", "Tax address fallback"]
tags: [taxes, vat, finance, address, snapshot, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[tax-computation]]. See the hub for the other aspects (rate selection, pricing models, overrides, OSS, order snapshot, fees-vs-VAT).

# Tax — address resolution + the per-order address snapshot

## Definition

The matcher in [[tax-rate-selection]] needs **one** address — billing or shipping — to test against `geo_zone_id`. The platform reads it through a priority + fallback rule controlled by the **`invoicing_address`** setting on [[settings-cart]]. That setting is **captured per-order at creation time** as a meta field on the order row, so later changes to the store-wide setting don't retroactively flip which address an existing order's tax matched against.

## Scope

Covered:

- The two values of `invoicing_address` (`BillingAddress` vs `ShippingAddress`, default).
- The mandatory fallback when the preferred address is empty.
- The per-order address-priority snapshot rule (the under-documented one).
- How order-edit re-computations stay consistent.

Not covered here:

- The frozen rates/amounts snapshot itself — see [[tax-order-snapshot]].
- Which VAT rule wins for the resolved address — see [[tax-rate-selection]].
- B2B reverse charge based on the VAT number found on that address — see [[tax-oss-semantics]].

## The priority rule

The platform reads the customer's address through this priority:

- If [[settings-cart]] → `invoicing_address = BillingAddress`: try billing first, fall back to shipping.
- If `invoicing_address = ShippingAddress` (the **default**): try shipping first, fall back to billing.

The **fallback always happens** when the preferred address is empty — so a customer who only filled in a shipping address gets tax matched against the shipping address even on a store configured for billing-first. There is no "fail closed" — VAT will always match against *some* address if at least one is present.

## The per-order snapshot rule (the under-documented one)

The `invoicing_address` setting is **captured per-order at creation time** as a meta field on the order row. Later changes to the store-wide setting do NOT affect the tax address used by **existing** orders — they keep matching against whichever address was preferred at the moment the order was placed.

This guarantees that a re-computation of an existing order's tax (e.g., when an admin edits the line items on a `pending` order) uses the same address-priority rule the order was created under. Without this carve-out, flipping the store-wide setting from Shipping → Billing would silently re-tax every editable open order against a different address, breaking VAT consistency.

(This is separate from the **rates/amounts snapshot** that freezes the computed tax onto the order itself — see [[tax-order-snapshot]] for that mechanism.)

## Contrasts

- **Billing-first vs shipping-first** — the merchant picks one as the default, but both stores fall back gracefully.
- **Per-order address-priority snapshot vs store-wide setting** — existing orders use their captured priority; new orders use the current store-wide setting.
- **Address-priority snapshot vs rates snapshot** — two distinct freezings, both protect historical accuracy. See [[tax-order-snapshot]] for the rates side.
- **Tax engine vs shipping engine** — both use the same `invoicing_address` priority, but the [[shipping-calculation]] engine sees the FULL geo-zone rule set (city, polygon, post-code) while [[tax-rate-selection]] only sees country rules.

## Worked example — fallback in action

Setup:

- Store: `invoicing_address = ShippingAddress` (default).
- Customer: only filled in **billing** address (some checkout flows allow this for digital goods).

Result:

- Engine tries shipping first → empty.
- Falls back to billing → matches against the billing country.
- The order's tax line uses the country found on the billing address.
- The per-order snapshot records `invoicing_address = ShippingAddress` at the time of creation; any later edit of the line items repeats the same shipping-first-then-billing dance.

## Worked example — flipping the store-wide setting

Setup:

- Store starts with `invoicing_address = ShippingAddress`. 1000 open `pending` orders.
- Merchant flips to `BillingAddress`.

Result:

- The 1000 existing orders keep their `invoicing_address = ShippingAddress` per-order capture. Editing one of them still resolves the tax address shipping-first.
- New orders placed after the flip use `BillingAddress` priority.
- No mass re-computation, no surprise VAT changes on historical orders.

## Where it applies

- [[settings-cart]] — the `invoicing_address` store-wide setting lives here.
- [[orders-details]] — the per-order capture is visible on the order's meta fields.
- [[checkout-flow]] — the priority + fallback rule fires when the engine first reads the customer's address.

## Related

- [[tax-computation]] — hub.
- [[tax-rate-selection]] — what the engine does with the resolved address.
- [[tax-order-snapshot]] — the rates/amounts snapshot (separate from this address-priority snapshot).
- [[settings-cart]] — `invoicing_address` setting.
- [[checkout-flow]] — where the resolution fires.
- [[shipping-calculation]] — uses the same address-priority rule but a richer geo-zone scope.

## Open Questions

None.
