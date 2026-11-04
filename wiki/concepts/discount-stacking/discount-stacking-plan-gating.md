---
type: concept
nav_path: "Concept → Discount stacking → Plan gating"
aliases: ["Plan-gating per discount type", "discount_global counter", "discount_coupon counter", "discount_fixed counter", "discount_quantity counter", "discount-code-pro feature key", "discount-code-pro-generator cap", "discount_labels counter"]
tags: [marketing, discounts, stacking, plan-gates, concepts]
plan_gates: [discount_global, discount_coupon, discount_fixed, discount_quantity, discount-code-pro, discount-code-pro-generator, discount_labels]
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[discount-stacking]]. See the hub for the other aspects (code_apply toggle, evaluation order, cart code slots, uses counter, Cart Rules interaction, per-variant rows).

# Discount stacking — plan gating

## Definition

Per the [[plan-gates]] concept, discounts have plan-feature keys. The check runs when a discount is created, separately from the runtime stacking decision at checkout, and it differs by path:

- **Admin form** — on create only, checks whether that kind of discount is enabled on the plan (`discount-<type>`). If not: HTTP 403 *"This feature is not enabled for your plan. To access it, please upgrade your plan."* No numeric limit, and no greyed-out cards other than Code PRO.
- **JSON-API v2** — on create only, compares usage with `discount_global`, `discount_fixed` or `discount_coupon`, and returns **402 Payment Required**.
- **GraphQL `createDiscount`** — only Fixed and Quantity quotas are checked; updates are not.

Usage counts discounts whether active or not; only deleting lowers it. `total_discounts` is a displayed figure, not enforced.

## Scope

Covered:

- What each path checks on create, and the plan-feature keys involved.
- What `discount_global` and `discount_coupon` each count.
- The `discount-code-pro` boolean feature for Code PRO availability.
- The `discount-code-pro-generator` numeric cap on bulk code generation.
- The `discount_labels` counter for pure-visual rows.
- What the merchant sees when a check fails.
- The Countdown and Quantity limits, which are separate from the plan.

Not covered here:

- The runtime stacking toggle (`code_apply`) — see [[discount-stacking-code-apply]].
- The `uses` / `max_uses` per-discount counter — see [[discount-stacking-uses-counter]].
- The implicit evaluation chain across discount types — see [[discount-stacking-evaluation-order]].

## Contrasts

- **Plan-gating (creation-time) vs `code_apply` (runtime)** — plan checks decide whether a discount can be **created**. `code_apply` decides how existing discounts **interact at checkout**. They are independent layers.
- **Plan-gating (per-type) vs `max_uses` (per-discount)** — plan quotas compare a **count per type per store**. `max_uses` limits **redemptions per individual discount**.
- **`discount_global` vs `discount_coupon`** — `discount_global` counts no-code flat, percent and free-shipping discounts with `code_apply` off, which includes Countdown and Container discounts. `discount_coupon` counts only discounts holding their own code, so Container and Code PRO discounts are not in it.
- **Boolean feature key (`discount-code-pro`) vs numeric counter (`discount-code-pro-generator`)** — `discount-code-pro` is on/off for the entire Code PRO feature. `discount-code-pro-generator` is a numeric cap on how many codes the bulk generator can produce in a single run.

## Where it applies

- **Discount-create screens** (per-type sub-pages of [[marketing-discounts]]) — the create request runs the admin check above; editing runs none.
- **Bulk Code PRO generation** on [[marketing-discounts-code-pro-generator]] — capped by `discount-code-pro-generator`.
- **JSON-API v2 create** via [[api-discounts]] — the quota check above, separate from the admin check.
- **Storefront** — does not see plan gating; it only sees the discounts that the merchant was able to create.

### The plan-feature keys

| Plan-feature key | Discounts counted | Notes |
|---------------------|-------------------|-------|
| **`discount_global`** | No-code flat, percent and free-shipping discounts with `code_apply` off, which includes Countdown and Container discounts | Labels and banners do not count against it. |
| **`discount_coupon`** | Discounts holding their own code | Container and Code PRO discounts are not in it. |
| **`discount_fixed`** | Fixed-type discounts | Per-product price overrides. |
| **`discount_quantity`** | Quantity discounts | Tiered product discounts. |
| **`discount-code-pro`** (boolean) | Code PRO type availability | On / off enable for the entire Code PRO feature. |
| **`discount-code-pro-generator`** (numeric) | Max codes per bulk-generator run | Limits how many codes the merchant can generate at once. |
| **`discount_labels`** | Visual labels (banner / countdown UI) | Pure-visual rows, no price reduction. |

### Countdown and Quantity limits (separate from the plan)

- **Countdown discount** — a second one can be saved. Checkout uses the first active one found, and tries no other.
- **Per-product Quantity discount** — a product can be in only one Quantity discount, active or not. Validation: *"Product is already in use"*.

### What the merchant sees

In the admin form, a kind not enabled on the plan returns the 403 above and no discount is created. The Code PRO card can show an upgrade panel (*"To create a discount code, you need to upgrade your plan."*); see [[plan-features]].


## Related

- [[discount-stacking]] — hub.
- [[discount-stacking-code-apply]] — runtime stacking toggle (separate axis).
- [[discount-stacking-uses-counter]] — per-discount redemption cap (separate axis).
- [[discount-stacking-evaluation-order]] — once created, where each type lands in the chain.
- [[plan-gates]] — the concept that catalogues every plan-feature counter.
- [[plan-features]] — the upgrade-prompt surface.
- [[marketing-discounts]] — discounts CRUD; the create check runs here.
- [[marketing-discounts-flat]] / [[marketing-discounts-percent]] / [[marketing-discounts-shipping]] / [[marketing-discounts-fixed]] / [[marketing-discounts-quantity]] / [[marketing-discounts-countdown]] / [[marketing-discounts-code-pro]] / [[marketing-discounts-codes]] — per-type feature pages.
- [[marketing-discounts-code-pro-generator]] — bulk Code PRO generator; capped by `discount-code-pro-generator`.
- [[discount]] — entity.
- [[products-banners-labels]] — the visual-label rows counted by `discount_labels`.

## Open Questions

None.
