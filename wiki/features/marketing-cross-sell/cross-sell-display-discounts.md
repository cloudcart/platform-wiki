---
type: feature
nav_path: "Marketing → Cross-Sell & UpSell → Display modes & discounts"
route_name: admin.cross_sell.diagram
route_path: /admin/marketing/cross-sell/diagram/{id?}
aliases: ["Cross-Sell display type", "Cross-Sell popup vs add to cart", "Cross-Sell discount type", "Cross-Sell free product", "Cross-Sell free shipping offer", "Cross-Sell action conditions"]
tags: [marketing, cross-sell, display, discounts, actions]
plan_gates: ["cross_sells"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[marketing-cross-sell]]. See the hub for the other aspects (offer form, trigger events, filters & limits, view tracking, engine comparison).

# Cross-Sell — display modes & discounts

## Purpose

Once an offer's trigger fires, two things decide what the customer experiences: **how** the offered products are surfaced (popup vs silent auto-add) and **what discount** rides along with them. This page documents **Box 4 — Action conditions** (display type + offered products) and **Box 6 — Discounts** of the [[cross-sell-offer-form]].

## Where to find it

Open a Cross-Sell offer → the **Action conditions** box (`cross_sell.label.actions`) holds the display type + offered-products builder; the **Discounts** box holds the discount type + value. Both are on the same edit form reached via the diagram side-panel (see [[cross-sell-offer-form]]).

## What the merchant can do here

### Box 4 — Action conditions

- **Display type** dropdown (`cross_sell[display_type]`) — **Display popup** vs **Add matched to cart**.
- **Products limit** dropdown (`cross_sell[products_limit]`) — values 1 through 10 (hard-capped — see [[cross-sell-filters-limits]]).
- **Display popup** dropdown (`cross_sell[meta][display_popup]`) — Yes / No. It matters only with **Add matched to cart**: Yes shows a closable popup of the products just added; No adds them silently, unless the offer has a follow-up ("yes") offer, whose popup then opens. A **Display popup** display type always shows its popup, whatever this says. Per event: [[cross-sell-trigger-events]].
- **Offered products list** (`cross_sell[actions]`) — a dynamic group builder identical in shape to the targets list. The merchant picks specific products / categories / vendors / smart-collections to OFFER when the trigger fires.

### Box 6 — Discounts

- **Type** dropdown (`cross_sell[type]`) — `simple` or `extended`. **Extended** unlocks the discount fields below.
- **Discount type** dropdown (`cross_sell[discount_type]`) — `fixed` / `percent` / `shipping` / `free_product`.
- **Discount value** input (`cross_sell[discount_percent]`) — currency-masked when type = `fixed`, percent-masked when type = `percent`, hidden when type = `shipping`.

### Display modes compared

| Display type | UX |
|---|---|
| **Popup** | Modal with the offered products + Add-to-cart buttons. Customer can dismiss. |
| **Add matched to cart** | Auto-adds the offered product to cart without asking. Aggressive — use for free-gift offers, not generic recommendations. |

## Settings & fields

| Field | Key | Values |
|---|---|---|
| Display type | `cross_sell[display_type]` | popup / add_to_cart |
| Products limit | `cross_sell[products_limit]` | 1-10 |
| Display popup | `cross_sell[meta][display_popup]` | Yes / No |
| Offered products | `cross_sell[actions]` | product / category / vendor / selection groups |
| Type | `cross_sell[type]` | `simple` / `extended` |
| Discount type | `cross_sell[discount_type]` | `fixed` / `percent` / `shipping` / `free_product` |
| Discount value | `cross_sell[discount_percent]` | currency / percent / hidden by type |

## Business rules

### Discount auto-flags

The four discount types are wired through the single `discount_type` field, and two of them silently set additional flags:
- Picking **`shipping`** auto-sets `free_shipping = 1` (free shipping on the offered product).
- Picking **`free_product`** auto-sets `free_products = 1` (the offered product is free).

The merchant does NOT manually toggle `free_shipping` / `free_products` — they follow from the discount type.

### Real catalog discount, not virtual

The discount belongs to the **cart line added through the offer**, not to the popup. It is worked out again on every cart read and shows as a line discount named after the offer's title. So:

- Closing the popup without choosing adds nothing and gives no discount; the same product added another way gets none either.
- A line added through the offer keeps its discount after the popup closes, while the cart still holds the product that triggered the offer. Remove that product and the discount drops. Offers targeting the whole cart, post-purchase offers and auto-add offers at checkout skip this check.
- The discount does not re-check the offer's status or dates; it ends only if the offer is deleted.

### Auto-add bypasses customer choice

The "Add matched to cart" display type silently injects the offered product into the cart. It should be reserved for free-gift / bundled-freebie scenarios. Most merchants pick popup.

### Auto-add force-locks the hide filters

When `display_type = add_to_cart`, the saving hook silently sets `hide_out_of_stock = 1` and `hide_cart_products = 1` regardless of what the merchant ticked — to prevent auto-adding an out-of-stock or already-in-cart product, which would break the cart flow. See [[cross-sell-filters-limits]].

### Auto-add has no accept / decline step

A `display_type = add_to_cart` Cross-Sell offer drops the product straight into the cart instead of showing an accept/decline popup, so there is no "decline" path for the customer to take.

## Related

- [[marketing-cross-sell]] — hub.
- [[cross-sell-offer-form]] — the form; Box 4 + Box 6 host these fields.
- [[cross-sell-filters-limits]] — the hide filters that auto-add force-locks; the `products_limit` cap.
- [[cross-sell-trigger-events]] — `add_to_cart` display type constrains the event to `product_details`.
- [[marketing-discounts]] — the catalog discount machinery the offer attaches to.
- [[marketing-up-sell-diagram]] — the offer editor / diagram page (same page shape for Cross-Sell and UpSell).

## Open questions

None.
