---
type: concept
nav_path: "Concept → Cart vs Order lifecycle → Cart-to-order handoff"
aliases: ["Cart to order handoff", "Place order snapshot", "Order creation pipeline", "PreOrderCreated", "OrderCreated", "PostOrderCreated", "Currency freeze", "Locale freeze", "Address snapshot", "Order events sequence", "Banned-IP auto-cancel", "Прехвърляне на количка към поръчка"]
tags: [cart, order, lifecycle, state-machine, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-08-06
source_count: 3
---

> Part of [[cart-vs-order-lifecycle]]. See the hub for the other aspects (cart / order state machines, abandonment, restore).

# Cart-to-order handoff

## Definition

The **handoff** is the single moment at which a [[cart|Cart]] becomes an [[order|Order]] — the customer's click on **Place order** at the checkout page. Before that click, only a Cart exists. After it, an Order exists; the Cart persists but is no longer modifiable by the customer (referenced as the order's `cart_id` for audit / abandoned-cart attribution).

The transition is **irreversible** (no "uncheck out" affordance) and triggers a deterministic snapshot pipeline (detailed under *Where it applies*). Many merchant-facing facts about orders — currency immutability, frozen prices, frozen tax, the order's `abandoned = 1` recovery flag — are decided at this exact moment.

## Scope

Covered: the 9-step Place-order pipeline; currency / locale immutability and the one-way BGN → EUR conversion on [[orders-details]]; the cart-vs-order data-shape diff; address snapshot semantics; the `abandoned = 1` flag set only by the restore-link handler; draft-order handoff with `order.created` webhook suppression until commit; banned-IP auto-cancel for offline payments.

Not covered here: cart data shape + cart states ([[cart-state-machine]]); order statuses + status-gated mutability ([[order-state-machine]]); the stock-decrement matrix per status × setting ([[inventory-tracking]]); abandoned-cart sweep / recovery email ([[cart-abandonment]] + [[cart-restore]]).

## Contrasts

- **Cart conversion vs Cart recovery**: Conversion = customer placed an order from their cart (normal flow). Recovery = customer clicked a restore link from an abandoned-cart email, then placed an order — flagged `abandoned = 1` with `restore_source` set. Recovery is a special case of conversion. See [[cart-restore]].
- **Currency on Cart vs Currency on Order**: the cart inherits the store's CURRENT currency and changes if the setting changes; the order's `currency` is snapshotted at creation and is immutable.
- **Storefront submit vs Draft commit**: both run the same post-creation pipeline. Storefront submit transitions a real cart → order with `cart_id` populated; draft commit clears the `is_draft` flag on an admin-created order that has no cart (see [[order-state-machine]]).
- **`order.created` vs `cart.created` webhook**: both fire, but `cart.*` is high-volume — most merchants subscribe only to `order.*` events.

## Where it applies

**The Place-order pipeline.** When the customer clicks **Place order**:

1. **Final validation** — required fields filled, totals within caps, stock available (if `pending` decrement-timing — see [[inventory-tracking]]).
2. **Discount re-evaluation** — all matching discounts re-attach against the FINAL cart state. A discount valid during the session but expired (or capped) by submit time drops off. The order's discount snapshot reflects what was ACTIVE at submit, not what was DISPLAYED 10 minutes earlier.
3. **Cart Rules re-evaluation** — [[cart-rule|Cart Rules]] fire AFTER discounts on the post-discount total.
4. **Order row created** with `status = pending`, `status_fulfillment = not_fulfilled`.
5. **Child rows created** — Order Products (one per cart line: snapshot price + quantity + options + per-line discount), Order Addresses (shipping + billing), Order Payment (initially `initiated`), Order Discounts (one per discount).
6. **Currency, locale, `unit_system` frozen** from the cart's session values; immutable thereafter.
7. **Stock decrement** (if `order_status_for_quantity_decrease = pending`) — Variant quantities decremented immediately. If the setting is `paid`, stock decrements later when payment clears. See [[inventory-tracking]].
8. **Order-created event fires** — fanning out to the confirmation email, per-order analytics, the `order.created` webhook ([[settings-hooks]]), and any app listeners. Guest-to-customer conversion runs at the start of this fan-out if `guest_to_customer` is ON.
9. **Customer redirected** to the payment provider (or the "Thank you / awaiting payment" page for offline methods).

**Draft order does NOT emit `order.created` webhook on initial save.** Admin-created draft orders ([[orders-add]] with `is_draft = 1`) bypass the webhook entirely. It fires only when the merchant clicks **Create order**, which clears the draft flag and runs the normal post-create pipeline. Integrations subscribed to `order.created` see exactly one event per order — at storefront submit (non-draft) or at the draft-commit click. See [[order-state-machine]].

**Banned-IP auto-cancel — offline payments only, IP-only.** The auto-cancel rule on [[settings-banned-ip]] runs after order creation, gated by `is_online_payment`: only OFFLINE providers (cash-on-delivery, bank transfer, ePay-style methods) hit the banned-IP check. Online providers (Stripe, PayPal, Borica, etc.) skip it, on the assumption the gateway is the fraud filter. The match is by request IP — there is no banned-email / banned-customer table; IP is the only banned dimension in the admin.

**Cart → Order data-shape diff.** Similar but NOT identical:

| Aspect | Cart | Order |
|--------|------|-------|
| Mutability | Fully mutable by customer anytime | Gated by status; many fields immutable after creation |
| Currency | Inherits store's CURRENT setting; changes with store | Snapshotted at creation; immutable forever |
| Locale | Inherits storefront's active language | Snapshotted; immutable |
| Customer | Optional — guests have no customer record | Snapshot of name + email + group at submit |
| Line item prices | Dynamic — re-evaluated vs current prices on load | Frozen — what the customer saw at checkout |
| Discounts | Live — attached / detached by current conditions | Frozen at submit; later changes don't affect existing |
| Cart Rules | Live | Frozen |
| Tax | Live — recomputed on every cart change | Frozen at submit; later rate changes don't affect existing |
| Shipping | Live — recomputed on address / cart changes | Frozen — the cost paid |
| Status | Active / Abandoned / Recovered / Converted (cart-internal) | 11 canonical statuses + fulfillment status |
| Audit log | None | Full history on [[orders-history]] |
| Invoice / receipt | Cannot issue | Can issue ([[orders-invoice]]) |
| Visible in [[orders]] | NO | YES |

**Address snapshot — not propagated back.** The order's addresses are a SNAPSHOT taken at checkout, independent of the customer's saved profile addresses. Editing via [[orders-address-edit]] does NOT update the saved profile, and editing the saved profile does NOT change existing orders.

**Currency and locale lock — historical integrity.** A locked `currency` and `locale` keep the confirmation email in the language the customer saw, the invoice in the agreed currency, and historical totals consistent — a 2024 BGN order is still 100 BGN after the store moves to EUR. The one exception is the BGN → EUR transition: the **"Convert prices to EUR"** button in the [[orders-details]] sidebar **permanently rewrites** the order's amounts at the fixed rate and sets its currency to EUR. It cannot be undone, and it is **refused once the order has an invoice number**. See [[orders-details-actions]].

**The `abandoned = 1` flag is set only by the restore-link handler.** An abandoned cart the customer revisits and submits directly (no link click) produces `abandoned = 0`; the flag is NOT set retroactively. Direct-revisit submits are normal orders with no recovery attribution, excluded from the [[orders]] *Recovered source* filter. See [[cart-restore]].

## Related

- [[cart-vs-order-lifecycle]] — hub.
- [[cart-state-machine]] — pre-handoff cart states.
- [[order-state-machine]] — post-handoff order states.
- [[checkout-flow]] — cross-entity view of the same transition.
- [[order-processing-pipeline]] — side-effects per lifecycle event.
- [[order-status-workflow]] — after creation.
- [[inventory-tracking]] — stock decrement timing (`paid` vs `pending`).
- [[discount-stacking]] — discount re-evaluation at submit.
- [[multi-currency]] — currency freeze.
- [[multi-language]] — locale freeze.
- [[notification-delivery]] — transactional emails + webhooks.
- [[cart-rule]] — Cart Rules fired AFTER discounts.
- [[settings-hooks]] — `order.created` webhook.
- [[settings-banned-ip]] — banned-IP auto-cancel.
- [[orders-add]] — admin-side draft order creation.
- [[orders-details]] — per-order edit hub ("Create order" for drafts).
- [[orders-address-edit]] — address snapshot edits.
- [[orders-invoice]] — invoice issuance.

## Open Questions

None.
