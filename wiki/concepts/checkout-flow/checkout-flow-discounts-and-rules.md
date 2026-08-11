---
type: concept
nav_path: "Concept → Checkout flow → Discounts & Cart Rules"
aliases: ["Discount attach", "Discount snapshot", "Cart Rule order", "Post-discount pricing", "discounts_used_statuses", "Counted statuses"]
tags: [orders, checkout, discounts, cart-rules, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[checkout-flow]]. See the hub for the other aspects (cart entity, abandoned detection, submit-to-order, guest vs registered, lifecycle overview, events & webhooks).

# Checkout flow — Discounts & Cart Rules

## Definition

Two distinct pricing-modifier systems run during the checkout flow: **Discounts** ([[discount]]) — promotional pricing tied to discount entities, evaluated continuously during the cart phase, snapshotted at submit — and **Cart Rules** ([[cart-rule]]) — custom condition→action rules from the app, evaluated AFTER discounts on the post-discount cart total. The ordering is deterministic: Discount first, Cart Rule second. The `uses` counter on a discount increments only when the order reaches a **counted status** (`discounts_used_statuses` setting on [[settings-statuses]], default `paid` / `completed` / `fulfilled`).

## Scope

Covered:

- When discounts attach during the cart phase + how they fix at submit.
- The Cart-Rule-runs-after-discounts ordering rule.
- Post-discount line-price input semantics for Cart Rules.
- The `discounts_used_statuses` counted-status setting and how negative-branch orders escape the counter.

Not covered here:

- Discount-vs-discount stacking semantics + `code_apply` / `force_save` flags — see [[discount-stacking]].
- Discount type catalogue (flat / percent / shipping / fixed / quantity / code / etc.) — see [[marketing-discounts]].
- Cart-rule condition / action catalogue — see [[apps-cart-rules]].
- Tax recomputation when discounts change line prices — see [[tax-computation]].

## Contrasts

- **Discount eligibility (during cart) vs discount snapshot (at submit)** — eligible discounts attach and re-evaluate on every cart change. At submit, the attached set is snapshotted into per-order-discount rows; further cart changes after submit no longer affect the order's discounts.
- **Discounts evaluated FIRST vs Cart Rules SECOND** — Cart Rules always run on the post-discount cart state. A "Cart total > 100 BGN" Cart Rule sees the discounted subtotal, not the pre-discount catalog subtotal.
- **Counted status vs non-counted status** — only orders in `discounts_used_statuses` (default `paid` / `completed` / `fulfilled`) increment the discount's `uses` counter. Cancelled / refunded / failed orders NEVER count, so a customer who places + cancels can re-use a "1 per customer" discount.

## Where it applies

### Discounts attach during cart, fix at submit

While the cart is open, the matching-discounts evaluator runs on every cart change. Any [[discount]] whose target + conditions match the current cart state attaches automatically. See [[discount-stacking]] for the interaction rules between codeless discounts, code-based discounts, Cart Rules, and the `code_apply` / `force_save` flags.

At the moment of order submission (step 2 of [[checkout-flow-submit-order-creation]]), the discounts that were attached are re-evaluated against the final cart state then **snapshotted** into per-order-discount rows. From then on, the discount's `uses` counter increments only when the order reaches one of the **counted statuses** (default: `paid`, `completed`, `fulfilled` — configured in the `discounts_used_statuses` setting on [[settings-statuses]]). Cancelled / refunded orders never increment.

### Cart Rule pricing — sees post-discount line prices

Cart Rules run AFTER discounts during cart re-evaluation and order submit (step 3 of [[checkout-flow-submit-order-creation]]). When both a Cart Rule and a discount target the same line, the Cart Rule's input is the line price AFTER the discount has been applied — the Cart Rule sees the post-discount price, never the catalog / pre-discount price.

Concrete consequences:

- A Cart Rule that **adds 5 BGN** to a discounted line stacks on top of the discount.
- A Cart Rule that **sets the line to 10 BGN** overrides the discount's effect (the line ends at 10 BGN regardless of what the discount produced).
- A Cart Rule **percentage** is applied to the post-discount price.

This ordering is non-configurable — Cart Rules are by design "the last word" on per-line pricing within the checkout pipeline.

### `discounts_used_statuses` counted-status setting

| Setting | Location | Default | Effect |
|---|---|---|---|
| `discounts_used_statuses` | [[settings-statuses]] | `paid`, `completed`, `fulfilled` | Discount's `uses` counter increments only when the order enters one of these statuses. |

Merchants can add custom statuses to this list — useful when a custom sub-status (e.g. "Out for delivery") should also count.

### Discount-uses sync side-effects

The discount-uses counter is updated both **inline** during the `OrderStatusChange` event AND via a fallback **`DiscountUsageSync`** job queued with a 10-second delay on the same transition — see [[checkout-flow-events-and-webhooks]] for the full status-change side-effect sequence. The dual-path design guarantees the counter is reconciled even if the inline path deadlocked.

## Related

- [[checkout-flow]] — hub.
- [[checkout-flow-submit-order-creation]] — where steps 2 (discount re-eval) and 3 (Cart Rule re-eval) live.
- [[checkout-flow-events-and-webhooks]] — the `DiscountUsageSync` 10-second delayed sync.
- [[discount]] — Discount entity.
- [[cart-rule]] — Cart Rule entity.
- [[discount-stacking]] — discount-vs-discount interaction rules.
- [[marketing-discounts]] — discount catalogue + editor.
- [[apps-cart-rules]] — Cart Rule editor.
- [[settings-statuses]] — `discounts_used_statuses` configuration.
- [[tax-computation]] — taxes recomputed after discount + Cart Rule pricing.

## Open Questions

- Confirm Cart Rules can target the same line as a discount with no merge conflict (the "override" wording above is the observed behaviour) (verify).
- Confirm whether the snapshot at submit re-runs targeting (re-attaches new matches) or only re-evaluates already-attached discounts (verify).
