---
type: concept
nav_path: "Concept → Discount stacking → Plan gating"
aliases: ["Plan-gating per discount type", "discount_global counter", "discount_coupon counter", "discount_fixed counter", "discount_quantity counter", "discount-code-pro feature key", "discount-code-pro-generator cap", "discount_labels counter"]
tags: [marketing, discounts, stacking, plan-gates, concepts]
plan_gates: [discount_global, discount_coupon, discount_fixed, discount_quantity, discount-code-pro, discount-code-pro-generator, discount_labels]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, cart code slots, uses counter, Cart Rules interaction, cooldown / attachments).

# Discount stacking — plan gating

## Definition

Per the [[plan-gates]] concept, each discount type counts against a **separate plan-feature counter**. The merchant's plan caps how MANY of each type they can have — a creation-time gate, separate from the runtime stacking decision at checkout.

The split between codeless and code-based counters is the most consequential plan-gating axis for stacking. A merchant on a low plan with `discount_global = 1` and `discount_coupon = 10` can run unlimited codeless promos (well, 1) but lots of coupon campaigns.

## Scope

Covered:

- The 7 plan-feature counters that gate discount creation per type.
- The codeless (`discount_global`) vs. code-based (`discount_coupon`) split.
- The `discount-code-pro` boolean feature for Code PRO availability.
- The `discount-code-pro-generator` numeric cap on bulk code generation.
- The `discount_labels` counter for pure-visual rows.
- How reaching the cap surfaces in the admin UI (redirect to [[plan-features]]).
- The store-level uniqueness limits that interact with plan gating (one Countdown per store, one Quantity per product).

Not covered here:

- The runtime stacking toggle (`code_apply`) — see [[discount-stacking-code-apply]].
- The `uses` / `max_uses` per-discount counter — see [[discount-stacking-uses-counter]].
- The implicit evaluation chain across discount types — see [[discount-stacking-evaluation-order]].

## Contrasts

- **Plan-gating (creation-time) vs `code_apply` (runtime)** — plan gates limit how many discounts the merchant can **have**. `code_apply` limits how multiple existing discounts **interact at checkout**. They are independent layers.
- **Plan-gating (per-type) vs `max_uses` (per-discount)** — plan gates limit **count per type per store**. `max_uses` limits **redemptions per individual discount**.
- **Codeless `discount_global` vs code-based `discount_coupon`** — codeless promos (Global Flat / Percent, Countdown, no-code Shipping) are "always-on" banner-style — they count against `discount_global`. Code-based promos (Promo, Container, Code PRO) require the customer to type a code — they count against `discount_coupon`.
- **Boolean feature key (`discount-code-pro`) vs numeric counter (`discount-code-pro-generator`)** — `discount-code-pro` is on/off for the entire Code PRO feature. `discount-code-pro-generator` is a numeric cap (default 5000) on how many codes the bulk generator can produce in a single run.

## Where it applies

- **Discount-create / edit screens** (per-type sub-pages of [[marketing-discounts]]) — the create button validates against the matching counter; over-cap redirects to [[plan-features]].
- **Bulk Code PRO generation** on [[marketing-discounts-code-pro-generator]] — capped by `discount-code-pro-generator` (default 5000).
- **JSON-API v2 create** via [[api-discounts]] — the same plan checks apply server-side.
- **Storefront** — does not see plan gating; it only sees the discounts that the merchant was able to create.

### The 7 plan-feature counters — verbatim keys

| Plan-feature counter | Discounts counted | Notes |
|---------------------|-------------------|-------|
| **`discount_global`** | Codeless discounts: Global (flat / percent), Countdown, no-code Shipping | "Always-on" / banner-style discounts. |
| **`discount_coupon`** | All code-based discounts: regular Promo (flat / percent / shipping with a `code`), Container, Code PRO | The merchant types a code at checkout. |
| **`discount_fixed`** | Fixed-type discounts | Per-product price overrides. |
| **`discount_quantity`** | Quantity discounts | Tiered product discounts. |
| **`discount-code-pro`** (boolean) | Code PRO type availability | On / off enable for the entire Code PRO feature. |
| **`discount-code-pro-generator`** (numeric, default 5000) | Max codes per bulk-generator run | Limits how many codes the merchant can generate at once. |
| **`discount_labels`** | Visual labels (banner / countdown UI) | Pure-visual rows, no price reduction. |

### Store-level uniqueness limits (orthogonal to plan)

Two uniqueness limits exist independently of plan counters — they're hard-coded for visual / data-model reasons:

- **Countdown discount** — only ONE can exist per store regardless of plan. Validation: *"Countdown discount already exists"*.
- **Per-product Quantity discount** — only ONE active quantity discount can target any given product. Validation: *"A volume discount with this product already exists"*.

The Countdown limit means `discount_global` cap matters only for Global Flat / Percent + no-code Shipping (Countdown can never exceed 1 regardless of plan ceiling). The Quantity limit means `discount_quantity` cap effectively limits how many distinct products can carry a tiered ladder — not how many tiered ladders the same product can carry.

### Reaching the cap — admin UX

Reaching a counter cap during create / edit redirects to [[plan-features]] for that feature. The merchant sees the standard "upgrade your plan" surface; no discount is created.

## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — runtime stacking toggle (separate axis).
- [[discount-stacking-uses-counter]] — per-discount redemption cap (separate axis).
- [[discount-stacking-evaluation-order]] — once created, where each type lands in the chain.
- [[plan-gates]] — the concept that catalogues every plan-feature counter.
- [[plan-features]] — the upgrade-prompt surface.
- [[marketing-discounts]] — discounts CRUD; per-type counters checked here.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] / [[marketing-discounts-fixed]] / [[marketing-discounts-quantity]] / [[marketing-discounts-countdown]] / [[marketing-discounts-code-pro]] / [[marketing-discounts-codes]] — per-type feature pages.
- [[marketing-discounts-code-pro-generator]] — bulk Code PRO generator; capped by `discount-code-pro-generator`.
- [[discount]] — entity.
- [[products-banners-labels]] — the visual-label rows counted by `discount_labels`.

## Open Questions

None.
