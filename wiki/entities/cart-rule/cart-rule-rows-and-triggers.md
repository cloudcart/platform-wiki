---
type: entity
nav_path: "Entity → Cart Rule → Rows and triggers"
aliases: ["Cart Rule rows", "Cart Rule triggers", "Cart Rule conditions", "Trigger taxonomy"]
tags: [entity, marketing, automation, discounts, rules-engine, triggers]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---

# Cart Rule — Rows and triggers

> Part of [[cart-rule]]. See the hub for related aspects (fields, actions, stacking, lifecycle, evaluation).

## Identity

A [[cart-rule|Cart Rule]] holds **rows**, and each row carries a set of **triggers**. This page documents how rows compose and the verbatim trigger taxonomy the cart engine evaluates.

## Aliases

- "Cart Rule rows" / "Cart Rule triggers" / "Cart Rule conditions" — merchant-facing terms.
- "Trigger taxonomy" — the catalogue of `condition_type` + `filter_type` combinations.

## Key Attributes

Each row carries:

- **`sorting`** — integer; rows evaluate highest-to-lowest within a rule.
- **Triggers** — N records, each with `condition_type` (`cart` / `product` / `customer`) → `filter_type` → operator → value. ANDed inside a row.
- **Action** — fixed to discount; see [[cart-rule-actions]].
- **Message** — optional customer-facing string; see [[cart-rule-actions]].

## Rows are an OR-fallback tier ladder (NOT accumulating deals)

A single Cart Rule can hold many rows, each a separate trigger-set + action + message. **But within a rule, only the FIRST matching row fires** — multiple rows of the same rule do NOT accumulate. Rows are an OR-fallback chain, not a stack.

The engine processes rows in **reverse `sorting` order** (highest sorting first): row with `sorting=2` evaluates first, then `sorting=1`, then `sorting=0`. The first row whose triggers all match wins the rule and the engine moves to the next rule. Other rows of the same rule are skipped.

The intended pattern is **tiered fallbacks** for the same kind of deal — *"buy 3 → 10% off; buy 5 → 15% off; buy 10 → 20% off + free shipping"* expressed as three rows of one rule with the highest-volume tier on the highest-sorting row. The customer always lands on the highest tier they qualify for; rows with lower sorting are the gracefully degraded fallback. See [[cart-rules-conditions]] for the editor UX and the common-mistake warning (putting the more generous tier on `sorting=0` so the less generous tier on `sorting=1` always wins).

To stack different KINDS of deals on the same cart (e.g., *"5% category-wide discount + 3% loyal-customer bonus + free shipping"*), use **multiple rules**, each one carrying its specific deal, and rely on **product-level** stacking — see [[cart-rule-stacking]] (cart-level matches are winner-takes-all).

## Triggers within a row use AND

Within one row, every trigger must be true for the row to fire. This is strict AND semantics — there is no OR within a row. To express OR (*"VIP customer OR cart > 200"*), the merchant creates two rows of the same rule (or two separate rules), each with one of the conditions.

## Trigger types are fixed

The trigger taxonomy is hard-coded into the cart-rule engine — three `condition_type` families with these filter types per family (verify — recorded from `_mapping_condition_methods` 2026-06-02):

- **Cart-level** (`condition_type=cart`): `cart_amount` (total subtotal post-discounts), `cart_quantity` (total units), `cart_products_count` (distinct product lines).
- **Product-level** (`condition_type=product`): 14 filters in total — record-set matches (`product`, `category`, `vendor`, `tag`, `selection`), per-line numeric filters (`product_amount`, `product_line_amount`, `product_quantity`), boolean flags (`product_new`, `product_featured`, `product_sale`), text filter (`product_title`), and variant/option value filters (`product_variant`, `product_option`).
- **Customer-level** (`condition_type=customer`): `customer_group` (group membership — and the platform-managed Guests group acts as the registered-vs-guest proxy since there is no separate flag), `order_amount` (lifetime spend — **completed orders only**), `order_count` (lifetime order count — **completed orders only**).

**Action-only filter types** (available inside an action's own triggers but NOT as row triggers): `product_from_condition`, `product_not_from_condition`, `product_lowest_price`, `product_highest_price`. Used to narrow which cart lines actually receive the discount — see [[cart-rule-actions]].

Each trigger has `condition_type` → `filter_type` → operator → value. Multiple triggers in a row combine with AND.

## Date filtering is rule-level, not trigger-level

The rule's `active_from` / `active_to` window is the only date gate — there is no per-row "if today is between X and Y" trigger. For more complex date logic (e.g., *"weekends only"*, *"between 18:00 and 22:00"*), the merchant must split into multiple rules and toggle their Active status manually OR via external automation. See [[cart-rule-fields]] for the date-window field semantics.

## What the merchant CANNOT trigger on

Out of scope of the trigger taxonomy: browsing history, session duration, time-of-day, IP-based geo, device, referrer, campaign source, or which marketing channel brought the customer. See the *"Customer filters cannot check"* notes on [[cart-rules-conditions]] for workarounds (using [[marketing-segments|Segments]] mapped to customer groups for some of these).

## Where it appears

- [[cart-rules-conditions]] — per-row trigger editor and the full filter UX.
- [[cart-rules-examples]] — common multi-row patterns.
- [[apps-cart-rules]] — list + editor.

## Related

- [[cart-rule]] — hub.
- [[cart-rule-fields]] — top-level rule attributes that gate row evaluation.
- [[cart-rule-actions]] — what fires when a row's triggers match.
- [[cart-rule-stacking]] — how multiple rules' matching rows combine.
- [[cart-rule-evaluation]] — when and how often row triggers re-run.
- [[product]] / [[category]] / [[vendor]] / [[customer-group]] — entities triggers reference.

## Open Questions

None.
