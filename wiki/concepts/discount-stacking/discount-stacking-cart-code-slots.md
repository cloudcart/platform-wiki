---
type: concept
nav_path: "Concept → Discount stacking → Cart code slots"
aliases: ["discount_code slot", "discount_container_code slot", "Cart code mutual exclusivity", "Container code consumption", "total_value cap", "Sequential Container redemption", "Stand-alone vs Container codes", "One stand-alone code at a time"]
tags: [marketing, discounts, stacking, container-codes, cart, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, uses counter, plan gating, Cart Rules interaction, cooldown / attachments).

# Discount stacking — cart code slots

## Definition

The [[cart|Cart]] entity has **two independent code slots**:

- **`discount_code`** — a single string column holding ONE stand-alone code (a regular Promo or a Code PRO code).
- **`discount_container_code`** — an array column holding many Container code strings against a **single Container parent**.

These two slots are **mutually exclusive at the cart level**. Setting one clears the other automatically:

- Entering a stand-alone code (typed at checkout): `discount_code` = new string, `discount_container_code` = `[]` (any Container codes removed).
- Entering a Container code: appended to `discount_container_code`, `discount_code` set to `null`.

In practice the merchant should communicate that Container codes can be combined **within the same campaign**, but they cannot mix Container codes with a regular Promo or Code PRO code in the same cart — typing a Promo code wipes the Container codes; adding a Container code wipes the Promo code. The customer never sees an error; the platform silently clears the conflicting slot. (verify)

## Scope

Covered:

- The two cart-level code slots and their mutual exclusivity.
- The "one stand-alone code at a time" rule (a second typed stand-alone code replaces the first).
- Container child-code sequential consumption against the parent's `total_value` cap.
- The parent's `code_apply` flag governing child-code reject-on-conflict.
- The Container parent / child relationship in attribute propagation (`type_value`, `codes[]`, `type` last-wins).

Not covered here:

- The `code_apply` 0 / 1 toggle mechanics themselves — see [[discount-stacking-code-apply]].
- The Container codes auto-generation and storefront listing — see [[marketing-discounts-codes]].
- The Code PRO multi-code campaign structure — see [[marketing-discounts-code-pro]].
- How the `uses` counter behaves for Container parent vs. children — see [[discount-stacking-uses-counter]].

## Contrasts

- **`discount_code` vs `discount_container_code`** — single-slot string vs. array. Stand-alone codes overwrite; Container codes append (until the cap or array limit).
- **Stand-alone code overwrite vs Container code append** — a second stand-alone code typed at checkout **replaces** the first (it doesn't add). A second Container code typed at checkout is **added** to the array — provided it belongs to the same parent campaign.
- **Stacking multiple codes — only via Container** — Stacking multiple codes in one cart is **only possible through a Container discount**. The parent code attaches and its children apply automatically. A merchant who wants the customer to combine "Code A AND Code B" should configure a Container discount, not two independent codes.
- **Parent `code_apply` vs child `code_apply`** — when a child Container code is redeemed, the platform evaluates the **parent's** `code_apply` flag for the reject-on-conflict check, not the child's. So if the parent has `code_apply = 0` and the cart already carries a discount, the child redemption is rejected even if the child itself would have allowed stacking. The child's other attributes (per-child target, per-child value) are still respected.

## Where it applies

- **Storefront cart code entry** — the customer types a code; the platform decides whether it lands in `discount_code` or `discount_container_code` based on the discount's `is_container` flag.
- **Storefront cart sync** — adding / removing items, refreshing the cart re-runs Container consumption against the current `total_value` cap.
- **Admin order edit** on [[orders-details]] — re-applying / removing codes re-evaluates the slot rules.
- **JSON-API v2** — the same slot semantics apply to API-driven cart updates. See [[api-discounts]], [[api-discount-codes]], [[api-discount-codes-pro]].

### Container code consumption — sequential redemption with `total_value` cap

When a Container discount applies at checkout, the platform iterates the cart's `discount_container_code` array and consumes codes **sequentially** until either:

1. All codes are consumed, OR
2. The running total of consumed code values reaches the parent's `total_value` cap.

Each code's value is added to the running `type_value` total on the parent discount as it's consumed, and the code string is appended to the discount's `codes` array (which becomes part of the order's discount snapshot). Codes that would exceed the cap remain in the cart's array **un-consumed** — they stay available for the customer's next eligible cart. This sequential-consumption pattern is what enables a customer to "stack" multiple Container codes against a single Container campaign. (verify)

The `type` field on each Container code is also written to the parent discount during application (the last consumed code's type wins) — so a Container campaign that mixes `flat` and `percent` codes will display the type of whichever code was last consumed in the cart preview.

### One stand-alone code at a time

The cart holds **one** stand-alone `discount_code` value at a time. A second stand-alone code typed at checkout **replaces** the first.

### Container parent vs. child attribute split

The parent Container discount holds: `code_apply`, `apply_regular_price`, `total_value`, `force_save`, `is_container = 1`, `uses` aggregate (see [[discount-stacking-uses-counter]]).

Each Container child code ([[discount-code]] entity) holds: the code string, its individual `value`, its `type` (`flat` / `percent`), its eligibility window, and (typically) `active = 1` until consumed.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — `code_apply` toggle; parent's flag governs child redemption.
- [[discount-stacking-uses-counter]] — parent `uses` aggregates redemptions across children.
- [[cart]] — the entity that carries the two slots.
- [[discount]] — parent Container discount (`is_container = 1`).
- [[discount-code]] — Container child-code entity.
- [[marketing-discounts-codes]] — per-discount Container codes screen.
- [[marketing-discounts-code-pro]] — Code PRO multi-code campaign (also stand-alone, but each child has full Discount fields).
- [[marketing-discounts-code-pro-generator]] — bulk generator for Code PRO codes.
- [[api-discount-codes]] / [[api-discount-codes-pro]] — JSON-API v2 endpoints with the same slot semantics.
- [[orders-discount-add]] — admin-side discount attachment runs the same slot rules.

## Open Questions

None.
