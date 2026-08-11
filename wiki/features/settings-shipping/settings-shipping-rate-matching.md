---
type: feature
nav_path: "Settings → Shipping → Rate matching"
route_name: admin.shippingProviders
route_path: /admin/shipping
aliases: ["Shipping rate matching", "Shipping bracket matching", "Cheapest rate wins", "Shipping checkout visibility", "Shipping methods at checkout", "Provider list order at checkout"]
tags: [settings, shipping, rate-matching, checkout, brackets]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-shipping]]. See the hub for the other aspects (list & Add modal, Custom rate types, edit panel, lifecycle, API & permissions).

# Shipping — rate matching at checkout

## Purpose

The merchant configures rate **brackets** on the edit panel (see [[settings-shipping-edit-panel]]) — but **which** bracket fires at checkout, **how** overlaps resolve, and **which** methods show up to the customer is decided by a deterministic backend matcher. This aspect documents the matcher's rules and the storefront-visibility cascade.

## Where to find it

This logic lives in the storefront [[checkout-flow]] when computing which shipping options to render. The merchant cannot tune it directly — they tune the **rate rows** on the edit panel and the **zone** + **allowed payment methods** that gate eligibility.

## What the merchant can do here

The rate-matcher behaviour is not a setting — it is the *contract* the merchant configures rate rows against. Three rules drive every cart-to-rate decision:

### Rule 1 — Both ends are inclusive

A rate row applies whenever `from <= cart value <= to` (or `to` is empty). Both ends are inclusive. A value sitting exactly on a boundary matches **BOTH** brackets touching it.

### Rule 2 — Cheapest matching rate wins on overlap

When multiple rate rows of the same method match, the platform sorts by `amount` (lowest first) and picks the cheapest. The matcher is NOT "earliest" or "latest" or "longest-prefix" — it is purely "cheapest matching".

Worked example — a price-based method with three rate rows:

| Row | from | to | amount |
|-----|------|----|--------|
| 1 | 0 | 50 | 5 BGN |
| 2 | 50 | 100 | 3 BGN |
| 3 | 100 | _(blank)_ | 0 BGN (free) |

Cart subtotal outcomes:

| Subtotal | Matches | Result |
|---------|---------|--------|
| 30 BGN | row 1 only | 5 BGN shipping |
| 50 BGN | rows 1 and 2 (boundary inclusive both sides) | 3 BGN (cheaper of 5 / 3) |
| 99.99 BGN | row 2 only | 3 BGN |
| 100 BGN | rows 2 and 3 (boundary inclusive) | free (cheaper of 3 / 0) |
| 250 BGN | row 3 only | free |

The merchant does NOT need to micromanage the gap between brackets to avoid charging customers more on round-number subtotals — the cheapest rate is always served. Tooltip on the edit panel's Rate rows header confirms this: *"Both boundaries are inclusive — when an order value sits on a boundary, the cheaper rate is chosen"*.

### Rule 3 — Blank `to` means "no upper bound"

The last bracket can extend to infinity by leaving `to` empty. The auto-fill quirk on **+ Add row** preserves this (see [[settings-shipping-edit-panel]]).

### Storefront-visibility cascade — the four gates

The shipping methods shown at checkout are the **intersection** of:

1. Methods with `active = yes` on the Shipping list.
2. Methods whose zone matches the customer's shipping address (country / region / city / postcode).
3. Methods whose allowed payment methods include the customer's selected payment option (or `payments_all = yes`).
4. Methods compatible with the order's content — the cart's total weight / price falls inside the method's rate brackets.

If a customer at checkout sees no shipping options, the merchant should check these four gates **in order**. The first gate (`active = yes`) is the most common cause.

### Multi-method display vs choice

When several configured shipping methods all qualify (zone matches + rate brackets match + allowed payment methods include the chosen payment), the storefront shows **ALL** of them and the customer chooses. There is no platform-level "auto-pick the cheapest method" gate — that toggle is only "Automatically select if only one is available" (in [[settings-cart]]).

### Provider list order at checkout

Active shipping methods are returned without an explicit `ORDER BY` on the providers query — the database insertion order (ascending id) determines the sequence the customer sees at checkout. There is **no UI** for the merchant to drag-and-drop reorder methods.

The default method picked at checkout (when "auto-select if only one is available" doesn't apply) is the one configured as **Default shipping provider** in [[settings-cart]] — independent of list position.

## Settings & fields

This aspect has no per-page settings — it describes how the fields configured on [[settings-shipping-edit-panel]] resolve at runtime. Inputs:

| Configured on | Drives |
|---------------|--------|
| Per-row `active` (Shipping list) | Gate 1 — visibility. |
| `provider[target]` / `provider[geo_zone_id]` ([[settings-shipping-edit-panel]]) | Gate 2 — address match. |
| `payments_all` / `payments_providers[]` ([[settings-shipping-edit-panel]]) | Gate 3 — payment match. |
| Rate rows + `type` ([[settings-shipping-custom-rates]] / [[settings-shipping-edit-panel]]) | Gate 4 — content match. |
| **Default shipping provider** ([[settings-cart]]) | Initial selection at checkout. |
| **Automatically select shipping if only one is available** ([[settings-cart]]) | One-shipping-option auto-pick. |

## Business rules

- **No "auto-pick cheapest method"** at platform level. The "auto-select" toggle in [[settings-cart]] applies only when exactly one method qualifies.
- **No reorder UI.** Method order at checkout = creation order (ascending id). Merchants who care about ordering need to recreate methods in the desired sequence (subject to the orders-attached delete protection — see [[settings-shipping-lifecycle]]).
- **"Cheapest on overlap" is not configurable.** The merchant cannot pick "first match wins" or "highest match wins" — it is always cheapest. This is intentional: it lets merchants overlap brackets without accidentally charging customers extra on boundary subtotals.
- **All four gates must pass.** A method satisfying three gates but failing one does not appear at checkout. Diagnose in order: `active` → zone → allowed payments → bracket fit.

## Related

- [[settings-shipping]] — hub.
- [[settings-shipping-edit-panel]] — where the rate rows / zone / allowed-payments are configured.
- [[settings-shipping-custom-rates]] — the four Custom `type` keys.
- [[settings-shipping-lifecycle]] — `active` toggle + delete protection.
- [[settings-cart]] — Default shipping provider + "auto-select if only one is available".
- [[settings-geo-zones]] — zone definitions consumed by gate 2.
- [[settings-payment-providers]] — payment providers consumed by gate 3.
- [[checkout-flow]] — the storefront step that runs the gates.

## Open questions

_None._
