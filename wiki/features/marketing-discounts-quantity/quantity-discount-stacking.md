---
type: feature
nav_path: "Marketing → Discounts → Quantity → Stacking"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/quantity
aliases: ["Quantity discount stacking", "Quantity vs Fixed discount", "Quantity + promo code", "Quantity discount priority", "code_apply Quantity"]
tags: [marketing, discounts, quantity, stacking, priority, cart]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-discounts-quantity]]. See the hub for the other aspects (form, tier evaluation, uniqueness constraint, plan gating, storefront display).

# Quantity discount — stacking and priority at cart-time

## Purpose

This aspect documents what happens at cart-time when a Quantity-tier line **also** has another discount source — a per-variant Fixed discount, an up-sell / cross-sell / bundle override, or a promo code. It covers which discount source wins per line and whether a promo code can apply on top of a Quantity-tier price.

## Where to find it

Stacking behaviour is cart-side; there is no admin UI screen that toggles it. The relevant inputs sit on different discount surfaces — Quantity tiers on the form at `/admin/marketing-new/discounts/create/quantity` (see [[quantity-discount-form]]), Fixed discounts on [[marketing-discounts-fixed]], promo codes on [[marketing-discounts-codes]] / [[marketing-discounts-code-pro]], and Cart Rules at [[apps-cart-rules]].

## What the merchant can do here

The merchant cannot configure stacking directly on the Quantity form — `code_apply` is not exposed and there is no priority dial. Practical levers:

- **Choose between Quantity and Fixed** for the same product knowing the Quantity tier wins at and above the smallest threshold; the Fixed price applies as fallback below it.
- **Configure the promo code's `code_apply`** on the code-based discount (Container or Code PRO) — this decides whether the code applies on top of a tier-priced line.
- **Avoid up-sell / cross-sell / bundle conflicts** with Quantity tiers on the same products if predictable per-unit pricing matters — those overrides win above Quantity.

## Settings & fields

This aspect has no merchant-tunable fields on the Quantity form itself. The relevant fields live on **other** discount records that the Quantity tier interacts with:

| Field | Lives on | What it does at stacking-time |
|-------|----------|-------------------------------|
| `code_apply` | The promo-code discount (Container / Code PRO) | If `1`, the code applies on top of the Quantity-tier price; if `0`, the code is blocked when the cart has a Quantity-tier line. |
| `code_apply` | The Quantity discount itself | Defaults to `0`; not exposed on the Quantity form (see [[quantity-discount-form]]). When `1`, the cart subtracts the variant's existing `save` from the tier price before promo-code allocation. Mostly dormant. |
| `discount_value` (per tier) | The Quantity discount's tier rows | The replacement unit price the tier sets. |
| Up-sell / cross-sell / bundle override flags | The Cart Rule or up-sell config | Take priority over the Quantity tier — see [[apps-cart-rules]]. |

## Business rules

### Per-line discount-priority resolver

When a cart line has BOTH a per-variant [[marketing-discounts-fixed]] price AND an active Quantity tier, the platform's per-line discount-priority resolver picks **one source** in this order (highest priority first):

1. **Up-sell override** — if the line was added via an up-sell trigger.
2. **Cross-sell override**.
3. **Bundle override** — when the line is part of a cart-bundle.
4. **Quantity tier** (this feature).
5. **Per-variant Fixed discount**.

So if a product has BOTH a Fixed discount AND a Quantity discount, **the Quantity tier wins** once its threshold is met. Below the smallest tier's threshold, the Fixed-discount price applies as fallback. This is the most subtle stacking interaction merchants miss — and it holds the same whether viewed from the product line or from the variant: the Quantity check runs before the variant's Fixed-discount fallback.

### Quantity + promo-code stacking — controlled by the promo code's `code_apply`, not the Quantity discount

Whether a promo code applies on top of a Quantity-tier line is decided by the **external code-based discount's own `code_apply` setting** — the one the merchant configures on the [[marketing-discounts-codes]] / [[marketing-discounts-code-pro]] / Container discount they create:

- **Quantity-tier line + external code with `code_apply = 0`** → the code is **blocked** (the Quantity tier counts as a "cart has a discounted line" condition).
- **Quantity-tier line + external code with `code_apply = 1`** → the code applies **on top of** the Quantity-tier price (line-level allocation).

The Quantity discount also has its own `code_apply` flag, but it is **not exposed** on the Quantity form (see [[quantity-discount-form]] for the omitted-fields list), defaults to `0`, and so is **dormant** for any discount saved through the admin. It only ever changes behaviour if an integrator sets it on the Quantity discount programmatically — and even then the admin UI does not surface the result. When set, it makes the cart subtract the variant's existing Fixed-discount saving from the tier price before the code's amount is allocated, so the code does not double-discount an already-reduced unit price. For practical merchant workflows this branch never fires.

### Quantity discounts have no code field, never code-based

Quantity discounts are **always automatic**. There's no code field on the form (see [[quantity-discount-form]]). The tier activates purely from the cart-line quantity matching the threshold — the customer never types anything to trigger it.

Code-based stacking is therefore always **between** a Quantity discount and a separate code-based discount the merchant created elsewhere, not within the Quantity discount itself.

### Tier is applied at the storefront cart, not in the admin

The tier is evaluated and applied only at the storefront cart; it then persists onto the order. The merchant viewing or editing the order in the admin does NOT see the Quantity tier re-applied — so adjusting an order's quantity in the admin does NOT switch tiers on the saved line. See [[quantity-discount-tier-evaluation]] for the same behaviour from the tier-matching angle.

## Related

- [[marketing-discounts-quantity]] — hub.
- [[quantity-discount-tier-evaluation]] — the matched-tier resolution that this aspect's priority resolver picks between.
- [[quantity-discount-form]] — confirms `code_apply` is NOT a merchant-exposed field on the Quantity form.
- [[marketing-discounts-fixed]] — the per-variant Fixed discount that is bypassed when a Quantity tier matches.
- [[marketing-discounts-codes]] — Container-discount child codes; one source of the external `code_apply` promo codes that interact with Quantity tiers.
- [[marketing-discounts-code-pro]] — Multi-code campaign discounts; another source of external `code_apply` codes.
- [[apps-cart-rules]] — Cart Rules can compose multi-product promotions Quantity discount cannot express; rules-side discounts also evaluate in the same per-line priority resolver.

## Open questions

None.
