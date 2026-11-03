---
type: concept
nav_path: "Concept → Shipping calculation → Persistence on cart and order"
aliases: ["Shipping quote persistence", "cart_shipping_quotes", "Frozen shipping on order", "Recalculate shipping", "Shipping quote saved on order", "Замразена цена за доставка", "Преизчисли доставка"]
tags: [shipping, cart, order, persistence, recalculation, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-calculation]]. See the hub for the other aspects (rate models, geo gating, carrier integrations, the checkout cascade, COD surcharge, discounts + Cart Rules).

# Shipping — persistence on cart and order

## Definition

After the [[shipping-calc-cascade|cascade]] decides which methods are available, the customer picks one, and the [[shipping-calc-discounts-rules|discount + Cart Rule layer]] modifies the line, the platform saves the chosen method + its quote in two places: first on the **cart** (in the `cart_shipping_quotes` row), then on the **order** when the customer completes checkout. This is **Step 10** — the final step of the calculation pipeline.

The two persistence stages serve different purposes:

- **Cart-stage** — mutable. The customer can still change shipping method, address, or payment method; each change re-runs Steps 1–9 and overwrites `cart_shipping_quotes`. There can be multiple quote rows during the cart's lifetime as the customer iterates on the checkout form.
- **Order-stage** — frozen. Once the order is created, the chosen shipping line is locked, recording the carrier name, quote amount, and any related COD / insurance / exchange-rate fields. Re-quoting requires the explicit **"Recalculate shipping"** action on [[orders-details]].

The freeze is intentional: it guarantees the order's financials match what the customer agreed to at checkout, even if rates change before fulfilment.

## Scope

Covered:

- The mutable cart-stage `cart_shipping_quotes` row and what it saves.
- The cart-to-order copy at checkout completion, including currency snapshotting (see [[multi-currency]]).
- The frozen order-side shipping record.
- The "Recalculate shipping" action on [[orders-details]] for explicit re-quote, and what happens when the merchant edits the order's address WITHOUT recalculating (the quote stays at the old value; the order can become inconsistent).
- What the order detail page shows for the shipping line.

Not covered here: the cascade itself (Steps 1–8, see [[shipping-calc-cascade]]); discount + Cart-Rule layering (Step 9, see [[shipping-calc-discounts-rules]]); waybill generation, the downstream per-order action that turns the saved quote into a carrier-side dispatch (see [[orders-shipping-waybill]]); order-level FX conversion details (see [[multi-currency]]).

## Contrasts

- **Cart-stage (mutable) vs. order-stage (frozen)** — at the cart level, every form change re-runs the cascade and overwrites the saved quote. At the order level the quote is locked; changing the address after checkout does NOT reprice unless the merchant clicks "Recalculate shipping".
- **Implicit re-quote vs. explicit "Recalculate shipping"** — implicit re-quote happens during cart-stage form iteration; explicit re-quote is the merchant-initiated action on [[orders-details]] for post-checkout corrections.
- **Frozen quote vs. live carrier rate** — the order's saved quote is what the customer agreed to pay. The carrier's current rate may differ (rates change, address changed, weight changed). "Recalculate shipping" pulls the live carrier rate; the order then reflects the new number.
- **Quote persistence vs. waybill creation** — the saved quote is the agreed price; the waybill commits the parcel to the carrier and gets a tracking number (see [[orders-shipping-waybill]]). A quote can exist without a waybill (order paid but not yet shipped); a waybill cannot exist without a quote.

## Where it applies

### Cart-stage persistence

When the customer selects a shipping method at checkout, the platform saves a row on the cart's `cart_shipping_quotes` collection. The row captures:

- **Chosen method** — the shipping-method identifier (custom method or carrier integration).
- **Price** — the final shipping amount after discounts + Cart Rules.
- **Tax** — VAT on the shipping line, if applicable per [[tax-computation]].
- **COD amount** — when payment is COD, the amount the courier will collect on delivery.
- **Insurance amount** — when insurance is configured per-method or per-order.
- **Exchange rate** — for multi-currency [[shipping-calc-carrier-integrations|carrier integrations]], the FX rate converting the carrier's billing currency back to the store currency (see [[multi-currency]]).
- **Currency** — the store currency the customer sees.

Every form-level change (different shipping method, address, or payment method) re-runs Steps 1–9 of the cascade and overwrites this row. There can be multiple historical quote rows during the cart's lifetime (verify retention).

### Cart-to-order copy at checkout completion

When the customer completes the order, the cart's chosen shipping quote is **copied** to the order's shipping record. After the copy the order's currency is **snapshotted** (see [[multi-currency]] for the FX implications), the shipping line becomes visible on the order detail, and the cart's `cart_shipping_quotes` row may be cleared or kept for analytics (verify retention). The shipping quote is then frozen on the order.

### What "frozen" means

After order creation, the shipping line does NOT change automatically. Editing the order's **shipping address** on [[orders-details]] does NOT reprice it (the merchant sees the new address but the old quote); adding / removing **line items** does NOT reprice it; and a change in the carrier's rates does NOT propagate to existing orders. This is by design — the order's financials must match what the customer agreed to.

### Explicit "Recalculate shipping" action

On [[orders-details]], the merchant can click **"Recalculate shipping"** to re-run the cascade against the (possibly updated) order data. The action re-walks Steps 1–8 of the [[shipping-calc-cascade|cascade]] using the order's current address + line items, re-quotes carrier-integration methods against the carrier with the current parameters, replaces the order's shipping line with the new quote, and logs the change in the order history.

When to use it:

- The merchant corrected a typo in the customer's address and wants the quote to reflect the new location.
- The merchant added a line item that pushes the cart into a different weight bracket.
- The merchant switched the customer's payment from card to COD (or vice versa) and wants the surcharge updated.

When NOT to use it: after the waybill has been generated. Re-quoting an order that already has a waybill can produce inconsistency between the order line and the waybill the carrier holds — the merchant should void the waybill first, then recalculate, then regenerate.

### What the order detail page shows

The order's [[orders-details|detail page]] surfaces the saved shipping quote as a line in the totals breakdown:

- **Shipping method name** — carrier name + service option (e.g., "Speedy — Office delivery").
- **Quote amount** — the agreed price.
- **COD line** and **Insurance line** — when applicable.
- **Discount offset** — if a free-shipping discount applied, the negative line is shown alongside the carrier's positive quote.
- **Frozen indicator** (verify) — the merchant can typically tell the quote is frozen because the "Recalculate shipping" action is available.

The order also surfaces the carrier-side reference (waybill / tracking number) once issued — see [[orders-shipping-waybill]].

## Related

- [[shipping-calculation]] — hub.
- [[orders-details]] — order detail page surfacing the frozen quote + the "Recalculate shipping" action.
- [[orders-shipping-waybill]] — downstream waybill issuance that uses the saved quote.
- [[multi-currency]] — currency snapshot mechanics on the order.
- [[tax-computation]] — VAT on the shipping line.
- [[order-processing-pipeline]] — broader order pipeline that surrounds shipping persistence.
- [[cart-vs-order-lifecycle]] — broader cart-to-order handoff semantics.

## Open Questions

- (verify) **Retention of historical `cart_shipping_quotes` rows.** Whether the platform keeps prior quotes for analytics or clears them on each cart-stage re-quote.
- (verify) **Frozen indicator on the order detail page.** Whether the order detail shows an explicit "frozen quote" marker or only the implicit availability of "Recalculate shipping".
