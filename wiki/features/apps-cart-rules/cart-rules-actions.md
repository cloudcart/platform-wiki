---
type: feature
nav_path: "Apps → Cart Rules → Actions"
route_name: ""
route_path: ""
aliases: ["Cart rule actions", "Cart rule action types", "Cart rule action triggers", "Cart rule discount action", "Free shipping action", "Action triggers"]
tags: [apps, cart-rules, marketing, promotions, actions, discounts]
plan_gates: ["cart_rules_actions"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-cart-rules]]. See the hub for the other aspects (conditions, scoping, stacking, cooldowns, examples, known issues).

# Cart Rules — Actions

## Purpose

An **action** is the *then* in *if-this-then-that*. Every row has exactly **one** action, which fires when all the row's [[cart-rules-conditions|conditions]] match. The action defines **what** the discount is (`value_type`) and **how big** (`value`); its own **action-triggers** narrow **which cart lines** receive it — independent of the row-triggers that decided whether the rule fires at all.

The `action_type` is currently fixed to `"discount"` — no auto-add-free-product, upgrade-shipping-tier, or send-notification action (see [[apps-cart-rules]] under *What the merchant CANNOT do here*).

## Where to find it

Inside the **rule editor** at `/admin/apps/cart-rules/rules/create` (or `/edit/{id}`), each row has an *Action* block beneath its *Triggers* list, exposing the `value_type` selector, the numeric `value` input, and the *Action triggers* sub-list.

## What the merchant can do here

- Pick one of three discount types — **Amount off** (fixed EUR), **Percent off**, **Free shipping** — and set its magnitude (value).
- Add up to `cart_rules_actions` action-triggers to narrow which cart lines receive the discount (default fallback: 5).
- Use action-trigger extras like `product_lowest_price` for BOGO patterns.

## Settings & fields

### Core action fields

| Field | Notes |
|---|---|
| `action_type` | Currently always `"discount"` |
| `value_type` | `"amount"` (fixed EUR off), `"percent"` (% off), or `"free_shipping"` |
| `value` | For `amount`: the money-off in store currency, **stored as cents ×100** (10 EUR → `1000`). For `percent`: the whole percent 0–100 (you enter `10` for 10%), **also stored ×100** (10% → `1000`, 50% → `5000`). For `free_shipping`: must be **null** (any value is rejected). |
| `triggers` | Action-triggers narrowing WHICH cart lines get the discount |

**Both `amount` and `percent` are stored ×100** (cents for money, percent×100 for percent) — so a percent's raw stored value (50% → `5000`) is usually a **bigger number** than a modest amount's cents (10 EUR → `1000`). Cart-level ranking compares this raw `value` across the two units, so a **percent-off rule typically outranks an amount-off rule** even when its actual money-off is smaller. See [[cart-rules-stacking]].

### Action triggers — extras beyond row triggers

Action triggers use the same filter taxonomy as [[cart-rules-conditions|row triggers]], **plus** these extras (action-triggers only):

| Filter (`filter_type`) | What it does |
|---|---|
| `product_lowest_price` | Apply only to the cart's CHEAPEST matching line. Use for BOGO ("get cheapest free"). |
| `product_highest_price` | Apply only to the MOST EXPENSIVE matching line. |
| `product_from_condition` | Limit to products that matched the row's own triggers — e.g. row filters *"contains Brand X"* but only those Brand X items get the discount, not the whole cart. |
| `product_not_from_condition` | The INVERSE — discount applies to every line that did NOT match the row's triggers. Used for **"buy X, get Y free"**; often paired with `product_lowest_price`. |

When an action-trigger uses a `record_type` of product / vendor / category / tag / selection, it requires `operator` (in/not_in) + `records` (array of IDs) and forbids `value` / `value_type` — same as row-triggers. When the action targets product lines and several match, it applies to **every** matching line.

## Business rules

### `free_shipping` action does NOT mark the order "has free shipping" (waybill keeps receiver-pays)

A Cart Rule with `value_type=free_shipping` zeroes the shipping line on the order total, but through a **different mechanism** than the [[marketing-discounts-shipping|Native Free shipping discount]]: the Native discount sets the *"this order has free shipping"* flag, while the Cart Rule only nullifies the cost and leaves the flag false.

**Merchant-visible consequence:** for orders where free shipping came from a Cart Rule, every courier that supports a **receiver-pays** option (the `PAYER_RECEIVER` waybill side — DPD, Speedy, Econt, GLS, Omniship-integrated couriers, Sendcloud, Eushipment, etc.) **still shows the receiver-pays choice** on the waybill side selector. The customer saw 0 EUR shipping at checkout, but picking *"receiver pays"* makes the courier collect from the customer at delivery.

**Which mechanism to pick:** for *"customer never pays, sender always pays"* (waybill auto-hides receiver-pays), use the [[marketing-discounts-shipping|Native Free shipping discount]]; for *"discount shipping but keep both waybill side options"* (e.g. B2B where the receiver still pays), use the Cart Rule `free_shipping` action. Other ways receiver-pays gets hidden are on [[marketing-discounts-shipping]] — most commonly when the shipping provider's own per-method **Free shipping threshold** is reached.

### `value=0` fires a real modification

A cart rule with action `value=0` (0% off, or 0 EUR off) **still fires** when its triggers match: it applies a zero-value modification and the rule's `used` counter increments, so merchants may see `used` tick up for rules they expected to be no-ops. See [[cart-rules-known-issues]]. Legitimate uses: cart-rule-driven free shipping (`value` is irrelevant with `value_type=free_shipping`), or experimental rules left active before getting a real value.

### Defensive guard on amount-off

Product-level amount-off is **silently dropped** on a line if it would push the per-unit price below zero. Percent-off is always allowed (it can't go below zero).

### Action stats — real money math, not estimates

The per-rule "Discounted amount" stat is the **real money** lost to the rule, computed from modifications actually applied to placed orders (not an estimate); for `free_shipping` rules it counts the actual shipping cost waived. Scoped by the page's date-range picker.

### How applied modifications surface on the order detail screen

Applied cart-rule modifications appear on [[orders-details]] in two places, **without any visual distinction from regular [[marketing-discounts|Discounts]]**:

- **On each affected product line** — small red text below the product name shows *"−{amount} ({Cart Rule title})"* (the cart rule's `title`), styled like a per-product discount.
- **In the order totals list** — order-level modifications appear as a separate negative line labeled with the rule's name, styled like a manual order discount.

No badge, icon, or separator distinguishes them in the admin UI; the only way to tell a cart-rule modification from a Discount is the rule's name. The webhook payload distinguishes them (`group: discount` vs `group: modification`) but this is not surfaced visually.

### Removing applied modifications from a placed order

| Flow | Where | What it does |
|---|---|---|
| **Per-line removal** | Each product row's cog (⚙) dropdown → *"Remove order modifications"*, shown only when that line has modifications. | Removes ONE per click (the first by default; a picker appears when a line has several). |
| **Bulk order-level removal** | The order's top *"+"* actions dropdown → *"Remove order modifications"*, shown when the order has cart-level modifications. | Removes ALL cart-level modifications at once. |

Both flows are **blocked on archived orders** (error *"order.err.cannot_perform_this_operation_on_archived_order"* — un-archive first) and both trigger the `order.updated` webhook. The success toast reuses the discount-removal key, so the merchant sees *"order.succ.order_product_discount_removed"* even for a cart-rule modification.

### How modifications render on invoice and credit-note PDFs

On product line rows the line subtotal already reflects the modification — **no separate sub-row** appears. In the totals breakdown each modification gets ONE negative row labeled with the rule's name (for percent, the percentage shows in brackets, e.g. *"Промоция (-10%)"*) — again visually identical to a manual order discount; credit-notes render the same way. Cart-rule modifications are NOT `hide_in_invoice`-flagged, so they always render; there is no merchant toggle to suppress them.

## Related

- [[apps-cart-rules]] — hub.
- [[cart-rule]] — Cart Rule entity; action fields live on `cart_rule_row_action`.
- [[cart-rules-conditions]] — row triggers; action triggers reuse this taxonomy with extras.
- [[cart-rules-scoping]] — scoping the discount to specific products / vendors / categories.
- [[cart-rules-stacking]] — how multiple actions resolve on the same line; the cents-vs-percent quirk.
- [[cart-rules-known-issues]] — `value=0` still fires; defensive guard on amount-off.
- [[marketing-discounts-shipping]] — Native Free shipping discount (the `free_shipping` mechanism that DOES mark the order).
- [[orders-details]] — where applied cart-rule modifications surface on placed orders.

## Open questions

None.
