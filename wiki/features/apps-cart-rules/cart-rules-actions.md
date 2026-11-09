---
type: feature
nav_path: "Apps → Cart Rules → Actions"
route_name: ""
route_path: ""
aliases: ["Cart rule actions", "Cart rule action types", "Cart rule action triggers", "Cart rule discount action", "Free shipping action", "Action triggers", "Then", "On", "Cart rule target", "Buy 3 pay 2"]
tags: [apps, cart-rules, marketing, promotions, actions, discounts]
plan_gates: ["cart_rules_actions"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[apps-cart-rules]]. See the hub for the other aspects (conditions, scoping, stacking, cooldowns, examples, known issues).

# Cart Rules — Actions

## Purpose

An **action** is the *then* in *if-this-then-that*. Every row has exactly **one** action, which fires when all the row's [[cart-rules-conditions|conditions]] match. The action defines **what** the discount is (`value_type`) and **how big** (`value`); its own **action-triggers** narrow **which cart lines** receive it — independent of the row-triggers that decided whether the rule fires at all.

The `action_type` is currently fixed to `"discount"` — no auto-add-free-product, upgrade-shipping-tier, or send-notification action (see [[apps-cart-rules]] under *What the merchant CANNOT do here*).

## Where to find it

Inside the **rule editor** ([[apps-cart-rules-rules-editor]]), each row's **Then** block, below its **When** conditions: the discount type, its value, and the **On** target with its **Where** filters.

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

Cart-level ranking compares the stored values across units, so a **percent-off rule usually outranks an amount-off rule** even when it saves less — see [[cart-rules-stacking]].

### The target — **On**: Cart or Product(s)

- **Cart** — one discount on the cart. Free shipping is always this.
- **Product(s)** — a discount on each targeted line. **Add action condition** adds **Where** filters.

On product lines a percent comes off each targeted line in full. An amount comes off each targeted line **once, not per unit**, and only where the line's unit price is at least the amount. A rule applies once per cart: *"buy 3, pay 2"* frees the cheapest line once, so with 6 units it still frees one line, and a line holding 2 units is freed whole.

### A cart condition inside the action's list

A cart entry in the action's list that carries a filter (cart amount, quantity or product count, or a customer filter) **gates** the action. Outside its range the row counts as not matched: no discount, the next row is tried, and the row's message can show as a nudge. It measures the lines matched by the row's product conditions if there are any, else the whole cart. The editor never writes such an entry, and shows one as a plain **Cart** target with the range hidden; it comes from the AI generator or the API. To clear it, switch **On** to **Product(s)** and back to **Cart**, then save (verify).

### Action triggers — extras beyond row triggers

Action triggers use the same filter taxonomy as [[cart-rules-conditions|row triggers]], **plus** these extras (action-triggers only):

| Filter (`filter_type`) | What it does |
|---|---|
| `product_lowest_price` | The N cheapest matching lines by unit price (N = its value, default 1). Use for *"get the cheapest free"*. |
| `product_highest_price` | The N most expensive matching lines, likewise. |
| `product_from_condition` | Limit to products that matched the row's own triggers — e.g. row filters *"contains Brand X"* but only those Brand X items get the discount, not the whole cart. |
| `product_not_from_condition` | The INVERSE — discount applies to every line that did NOT match the row's triggers. Used for **"buy X, get Y free"**; often paired with `product_lowest_price`. |

When an action-trigger uses a `record_type` of product / vendor / category / tag / selection, it requires `operator` (in/not_in) + `records` (array of IDs) and forbids `value` / `value_type` — same as row-triggers. When the action targets product lines and several match, it applies to **every** matching line.

## Business rules

### `free_shipping` action does NOT mark the order "has free shipping"

A Cart Rule `free_shipping` zeroes the shipping line, but unlike the [[marketing-discounts-shipping|Native Free shipping discount]] it does not set the order's free-shipping flag. So on couriers with a **receiver-pays** option (DPD, Speedy, Econt, GLS, Sendcloud, …) the waybill still offers *receiver pays*, and picking it makes the courier collect from the customer. For *"sender always pays"* use the native discount; the Cart Rule suits cases where the receiver may still pay (e.g. B2B). Other ways receiver-pays is hidden are on [[marketing-discounts-shipping]].

### `value=0` fires a real modification

A cart rule with action `value=0` (0% off, or 0 EUR off) **still fires** when its triggers match: it applies a zero-value modification and the rule's `used` counter increments, so merchants may see `used` tick up for rules they expected to be no-ops. See [[cart-rules-known-issues]]. Legitimate uses: cart-rule-driven free shipping (`value` is irrelevant with `value_type=free_shipping`), or experimental rules left active before getting a real value.

### Action stats — real money math, not estimates

The per-rule "Discounted amount" stat is the **real money** lost to the rule, computed from modifications actually applied to placed orders (not an estimate); for `free_shipping` rules it counts the actual shipping cost waived. Scoped by the page's date-range picker.

### How applied modifications surface on the order detail screen

On [[orders-details]], a product-level modification shows under the line as *"−{amount} ({rule title})"*, and a cart-level one as a negative totals line named after the rule. Nothing distinguishes them visually from regular [[marketing-discounts|Discounts]] except the name; the webhook payload does (`group: discount` vs `group: modification`).

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
