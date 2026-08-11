---
type: feature
nav_path: "Marketing → Cross-Sell & UpSell → Trigger events & targets"
route_name: admin.cross_sell.diagram
route_path: /admin/marketing-new/cross-sell/diagram/{id?}
aliases: ["Cross-Sell trigger events", "Cross-Sell events", "Cross-Sell targets", "Cross-Sell ALL_EVENTS", "Cross-Sell allowed targets", "add_to_cart event", "return_page event"]
tags: [marketing, cross-sell, events, targets, conditions]
plan_gates: ["cross_sells"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-cross-sell]]. See the hub for the other aspects (offer form, display modes & discounts, filters & limits, view tracking, engine comparison).

# Cross-Sell — trigger events & targets

## Purpose

Every Cross-Sell offer fires on exactly **one trigger event** and is scoped by a set of **target conditions** — the "when" and "against what" of the offer. This page is the authoritative catalogue of the 6 selectable events and the 4 allowed target types. These are configured in **Box 3 — Target conditions** of the [[cross-sell-offer-form]].

## Where to find it

Open a Cross-Sell offer (Sidebar → Marketing → **Cross-Sell & UpSell** → a row → diagram node → Edit). The **Target conditions** box (`cross_sell.label.target`) holds the **Event** dropdown + the conditions builder. The box is only shown when `$allow_event = true` (i.e. when the node is allowed to pick its own event — see Business rules).

## What the merchant can do here

### Pick a trigger event

The **Event** dropdown (`cross_sell[event]`) offers one of these, per the platform code:

- **`add_to_cart`** — fires when the customer adds the source product to cart.
- **`cart`** — fires when the customer is on the cart page.
- **`checkout`** — fires when the customer is at the checkout step.
- **`checkout_select_payment`** — fires when the customer selects a payment method.
- **`checkout_select_shipping`** — fires when the customer selects a shipping provider.
- **`return_page`** — fires on the Thank-You / order-confirmation page (post-purchase upsell).

`product_details` is defined in the constant but **commented out** in `ALL_EVENTS` — currently not exposed as a selectable trigger.

Events group by context: the five **cart-flow events** (`add_to_cart`, `cart`, `checkout`, `checkout_select_payment`, `checkout_select_shipping`) and the single **order event** (`return_page`).

### Build target conditions

The **Conditions list** (`cross_sell[targets]`) is a dynamic group-of-conditions builder (the same UI as cart-rule conditions). Each group is an AND-bound list; multiple groups are OR-bound. Per row: a type select, the matched item, and a comparison operator. The **+ Add group of conditions** link adds another OR group.

Per the platform code, an offer's trigger condition can match against:

- **Specific products** (`product`).
- **Specific product categories** (`category`).
- **Specific vendors** (`vendor`).
- **Smart-collection selections** (`selection`).

For cart-flow events, the row type select also exposes `cart` / `shipping` / `payment` operands.

## Settings & fields

| Field | Key | Values |
|---|---|---|
| Event | `cross_sell[event]` | `add_to_cart`, `cart`, `checkout`, `checkout_select_payment`, `checkout_select_shipping`, `return_page` |
| Target conditions | `cross_sell[targets]` | groups of `product` / `category` / `vendor` / `selection` rows |

## Business rules

- **Tags are NOT an allowed target.** To scope by tag, the merchant first builds a [[products-smart-collections|smart collection]] populated by tag, then picks that collection as the target (`selection`).
- **Event selection is constrained by the parent node.** When the parent is a Cross-Sell with `display_type = add_to_cart`, the event is hard-coded to `product_details` (hidden field). When the offer is a child of an UpSell parent with `action = no`, only the `add_to_cart` event is offered. See [[marketing-up-sell-diagram]].
- **`product_details` is internal-only.** It is reachable via the parent-constraint above but not from the open Event dropdown (commented out of `ALL_EVENTS`).
- **`return_page` is the post-purchase upsell** — it is the only `order`-context event; the other five are cart-flow events that fire before the order is placed.

## Related

- [[marketing-cross-sell]] — hub.
- [[cross-sell-offer-form]] — the form; Box 3 hosts these fields.
- [[cross-sell-display-discounts]] — display mode; `add_to_cart` display type constrains the event (see Business rules).
- [[products-smart-collections]] — the `selection` target type; the tag-scoping workaround.
- [[products-products]] / [[products-categories]] / [[products-vendors]] — the other target operands.
- [[marketing-up-sell-diagram]] — parent-node constraints on the event dropdown.

## Open questions

No outstanding questions.
