---
type: entity
nav_path: "Entity → Cart Rule → Evaluation"
aliases: ["Cart Rule evaluation", "Cart Rule matcher", "Cart Rule matches and notifications", "AI-assisted construction"]
tags: [entity, marketing, automation, discounts, rules-engine, evaluation]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Cart Rule — Evaluation

> Part of [[cart-rule]]. See the hub for related aspects (fields, rows-and-triggers, actions, stacking, lifecycle).

## Identity

When the [[cart-rule|Cart Rule]] matcher runs, what data it sees about the customer, what it outputs (matches + notifications), how analytics are derived, and the AI assistant that helps merchants compose rules.

## Aliases

- "Cart Rule evaluation" / "Cart Rule matcher" — the rule-engine pass that runs at every cart read.
- "Cart Rule matches and notifications" — the two output channels of one matcher pass.
- "AI-assisted construction" — the natural-language rule generator on the list page.

## Key Attributes

The matcher reads these inputs and emits these outputs:

- **Inputs (customer snapshot)** — `group_id`, total income across ALL orders, completed-orders count, total-orders count, `isGuest` boolean.
- **Inputs (cart)** — line items, totals (post-discount), variant / option metadata.
- **Outputs** — `matches` (rules that fire — contribute discounts) and `notifications` (rules that did NOT fire but have a non-empty message).
- **Stats derivation** — `withStats` scope joins `orders_modification` to produce used-count + total-discount per rule.

## Evaluation timing

Cart Rules are re-evaluated:

- Every time the cart is read (page load, AJAX refresh).
- After every cart modification (add item, remove item, change quantity).
- At checkout when the customer advances to the payment step.
- At order submit (final evaluation before the cart converts to an order).

This means the customer sees rules attach and detach in near-real-time as they shop. See [[checkout-flow-discounts-and-rules]] for the discount-then-rule ordering in the checkout pipeline and [[checkout-flow-submit-order-creation]] for the submit-time re-evaluation.

## Customer-segment input data — what the rule sees

The Cart Rule matcher evaluates customer-level conditions against snapshot values read at evaluation time:

- Customer `group_id` (membership in a [[customer-group|Customer Group]]).
- Total income across ALL orders (lifetime spend).
- Completed-orders count.
- Total-orders count.
- A boolean `isGuest` (true when the customer's group equals the platform's "guest group").

The matcher does NOT see browsing history, session age, referrer, or device type. Guest customers are treated as a real customer for matching purposes (with the guest group's `group_id`) — so a rule keyed off *"customer NOT in VIP group"* matches guests. See [[cart-rule-rows-and-triggers]] for the full customer-level trigger taxonomy.

## Matches + notifications outputs

When the matcher runs, it produces two outputs:

- **`matches`** — rules whose triggers fired. These contribute discounts to the cart.
- **`notifications`** — rules whose triggers did NOT fire but whose message field is non-empty. These tell the customer what they are MISSING to qualify.

The notifications path runs only for rules that come AFTER the highest-matching row of each rule by `sorting` order, so the cart shows next-tier nudges (*"add 6 EUR more for free shipping"*) but suppresses already-satisfied tiers (*"you got the 10% deal!"*). See [[cart-rule-actions]] for the message-slot UX.

## Performance stats via `withStats`

The `withStats` scope on the Cart Rule model joins against the `orders_modification` table to compute:

- **Used count** — count of DISTINCT `order_id` references in `orders_modification` joined on the rule.
- **Total discount** — sum of the modification value for amount-type rules, or `price * percent / 100` from the order product / order total for percent-type, or the shipping cost for free-shipping rules.

These power the per-rule analytics on the [[apps-cart-rules]] list. Soft-deleted rules still join correctly so historical-order analytics keep computing — see [[cart-rule-lifecycle]].

## AI-assisted construction

The list page has a **+ Generate with AI** button. The merchant types a natural-language description of the intended rule (*"give 10% off if cart has more than 3 Apple products and customer is in VIP"*) and AI constructs the rule structure (triggers + action) for the merchant to review before activating. This dramatically speeds up rule creation for non-technical merchants. See [[apps-cart-rules]] for the editor entry point.

## What flows downstream from a match

When a match fires at order submit, the resulting discount lines are snapshotted onto the [[order|Order]] (same as standard [[discount|Discounts]]). The discount on the order references the Cart Rule for reporting — so historical orders keep their context even if the rule is later soft-deleted (see [[cart-rule-lifecycle]] for `withStats` preservation).

## Where it appears

- [[apps-cart-rules]] — list + AI-assisted construction entry point.
- [[checkout-flow]] — when the matcher runs across the cart-to-order journey.
- [[checkout-flow-discounts-and-rules]] — concept page on the discount-then-rule ordering.
- [[cart]] — the entity the matcher reads at evaluation time.

## Related

- [[cart-rule]] — hub.
- [[cart-rule-rows-and-triggers]] — the trigger taxonomy the matcher evaluates.
- [[cart-rule-actions]] — what the matcher emits when triggers fire.
- [[cart-rule-stacking]] — how multiple matches combine before reaching the cart.
- [[cart-rule-lifecycle]] — soft-delete + `withStats` preservation.
- [[customer]] — entity providing the snapshot values for customer-level triggers.

## Open Questions

- ⏸️ Whether Cart Rule discounts count toward the discount usage counter on the resulting [[order|Order]] in the same way standard [[discount|Discount]] uses do — affects analytics and per-customer usage caps.
