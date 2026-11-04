---
type: concept
nav_path: "Concept → Discount stacking → Cart code slots"
aliases: ["discount_code slot", "discount_container_code slot", "Cart code mutual exclusivity", "Container code pool", "Highest Container total wins", "Stand-alone vs Container codes", "One stand-alone code at a time"]
tags: [marketing, discounts, stacking, container-codes, cart, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, uses counter, plan gating, Cart Rules interaction, per-variant rows).

# Discount stacking — cart code slots

## Definition

The [[cart|Cart]] entity has **two independent code slots**:

- **`discount_code`** — a single string column holding ONE stand-alone code (a regular Promo or a Code PRO code).
- **`discount_container_code`** — an array column holding many Container code strings.

These two slots are **mutually exclusive at the cart level**. Setting one clears the other automatically:

- Entering a stand-alone code (typed at checkout): `discount_code` = new string, `discount_container_code` = `[]` (any Container codes removed).
- Entering a Container code: appended to `discount_container_code`, `discount_code` set to `null`.

A cart can hold several Container codes, but not a Container code together with a regular Promo or Code PRO code — typing a Promo code wipes the Container codes; adding a Container code wipes the Promo code. The customer never sees an error; the platform silently clears the conflicting slot.

## Scope

Covered:

- The two cart-level code slots and their mutual exclusivity.
- The "one stand-alone code at a time" rule (a second typed stand-alone code replaces the first).
- How Container codes apply: one store-wide pool, all active Containers try them, the highest total wins.
- Container codes and `code_apply`.
- What a Container discount and a Container code each hold.

Not covered here:

- The `code_apply` 0 / 1 toggle mechanics themselves — see [[discount-stacking-code-apply]].
- The Container codes auto-generation and storefront listing — see [[marketing-discounts-codes]].
- The Code PRO multi-code campaign structure — see [[marketing-discounts-code-pro]].
- How the `uses` counter behaves for Container discounts — see [[discount-stacking-uses-counter]].

## Contrasts

- **`discount_code` vs `discount_container_code`** — single-slot string vs. array. Stand-alone codes overwrite; Container codes append.
- **Stand-alone code overwrite vs Container code append** — a second stand-alone code typed at checkout **replaces** the first (it doesn't add). A second Container code typed at checkout is **added** to the array.
- **Several codes in one cart — only with Container codes** — the customer types each code; nothing attaches automatically. A merchant who wants the customer to combine "Code A AND Code B" should use Container codes, not two independent codes.
- **Container codes and `code_apply`** — a Container code is never refused for this. The Container's default is on, and its form has no such switch.

## Where it applies

- **Storefront cart code entry** — the customer types a code. Promo, barcode and Code PRO codes are looked up together; Container codes are tried only if none match.
- **Storefront cart sync** — adding / removing items, refreshing the cart applies the codes in the cart again.
- **Admin order edit** on [[orders-details]] — re-applying / removing codes re-evaluates the slot rules.
- **JSON-API v2** — the same slot semantics apply to API-driven cart updates. See [[api-discounts]], [[api-discount-codes]], [[api-discount-codes-pro]].

### How Container codes apply

Container codes are **one store-wide pool, attached to no Container**. All active Containers for the customer's region try the entered codes; the highest total wins, so with two active Containers a code can land on either. A code applies only if it fits what remains of that Container's value, so the Container's own amount acts as the cap. Codes that do not fit stay in the cart's list, unapplied.

An order does not use a code up: it stays reusable until turned off or deleted. Turning a code off stops typing it.

A cart that mixes `flat` and `percent` codes takes the `type` of the last code in the list for the whole Container total. A flat Container targeted at specific products gives no reduction.

### One stand-alone code at a time

The cart holds **one** stand-alone `discount_code` value at a time. A second stand-alone code typed at checkout **replaces** the first.

### What a Container discount and a Container code each hold

The Container discount holds: `code_apply`, `apply_regular_price`, its value (the cap), `force_save`, `is_container = 1`, `uses` (see [[discount-stacking-uses-counter]]).

Each Container code ([[discount-code]] entity) holds: the code string, unique in the pool, its `value`, its `type` and its `active` flag.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — `code_apply` toggle.
- [[discount-stacking-uses-counter]] — the Container discount's `uses`; a code has no counter.
- [[cart]] — the entity that carries the two slots.
- [[discount]] — Container discount (`is_container = 1`).
- [[discount-code]] — Container code entity.
- [[marketing-discounts-codes]] — store-wide Container codes screen.
- [[marketing-discounts-code-pro]] — Code PRO multi-code campaign (a stand-alone code; each code has its own terms).
- [[marketing-discounts-code-pro-generator]] — bulk generator for Code PRO codes.
- [[api-discount-codes]] / [[api-discount-codes-pro]] — JSON-API v2 endpoints with the same slot semantics.
- [[orders-discount-add]] — admin-side discount attachment; the picker lists no Container codes.

## Open Questions

None.
