---
type: concept
nav_path: "Concept → Shipping provider mechanism → Cash on delivery"
aliases: ["Cash on delivery", "COD", "COD surcharge", "10000 BGN cap", "COD-paid sync", "Auto mark paid", "Карта при доставка", "Наложен платеж", "Изплащане при доставка", "Лимит наложен платеж", "Activate cash on delivery", "cd toggle", "courier missing at checkout", "courier disappeared from checkout", "COD-only store", "shipping method hidden when only COD", "cod_manual", "COD amount on waybill", "COD amount editable", "COD amount wrong on label", "сума наложен платеж", "COD amount does not match order total"]
tags: [shipping, couriers, providers, payments, cod, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-07-23
source_count: 1
---

> Part of [[shipping-provider-mechanism]]. See the hub for the other aspects (configuration, pricing models, pickup points, waybill, geo routing, status tracking).

# Shipping provider mechanism — Cash on delivery (COD)

## Definition

**Cash on delivery (COD)** is the payment mode where the customer pays the carrier at the moment of delivery (in cash, or via a card terminal the courier carries), and the carrier remits the collected amount back to the merchant. The carrier collects on the merchant's *behalf* — this requires a separate contractual setup between the merchant and the carrier's bank, and a configured COD-account number per carrier in CloudCart.

Three things distinguish a COD order from a normal online-paid order on CloudCart:

- A **COD surcharge** is added to the shipping price (the carrier's cost of collecting + remitting cash).
- A **currency-specific COD cap** (10,000 BGN, applied **only** to stores still on the legacy `BGN` currency) may hide the COD option at checkout for high-value carts — a store on **EUR** (the new Bulgarian norm) gets **no** platform cap.
- An **automatic paid-sync** flips the order's payment to `completed` once the carrier reports the cash collected — the merchant doesn't have to mark it paid manually.

This page documents the carrier-integration variant of COD. Standalone COD without a carrier integration ([[payment-providers-cod]]) is a different mechanism — the merchant collects the cash themselves.

## Scope

Covered:

- COD surcharge models (integration vs. custom-method).
- The 10,000 BGN cap and how it's currency-aware.
- The auto paid-sync flow.
- COD account configuration + carrier-side validation.
- Pre-conditions for COD to work end-to-end.

Not covered:

- Standalone COD without carrier integration — see [[payment-providers-cod]].
- The full payment provider mechanism — see [[payment-provider-mechanism]].
- The mark-paid UI on the order — see [[orders-sync-cod]].

## Contrasts

- **COD via carrier integration vs. standalone COD**: with a carrier integration, the carrier collects the cash + remits to the merchant + reports the collection back to CloudCart (automatic paid-sync). Standalone COD ([[payment-providers-cod]]) means the merchant collects the cash themselves (e.g., personal handoff, own delivery driver) and marks the order paid manually.
- **Integration COD surcharge vs. custom-method COD fee**: integration methods bake the COD margin into the carrier-quoted rate (Speedy / Econt return a higher number when COD is selected). Custom methods let the merchant set a flat COD fee that's added on top of the rate-row price.
- **COD cap (BGN store) vs. no cap (non-BGN store)**: the 10,000 BGN cap is a platform-side rule applied only when the store currency is BGN. Non-BGN stores don't get a platform-side cap — the carrier's own server-side limits apply.

## Where it applies

### COD surcharge model

The carrier adds a COD-handling fee to the shipping price (the cost of collecting and remitting cash). The shape varies by pricing model:

- **For carrier-integration methods** (live API quote), the surcharge is *included* in the carrier's quoted shipping price. Speedy, Econt, etc. bake their COD margin into the rate they return — the customer sees a single shipping number that already includes COD overhead.
- **For custom methods** (merchant-defined rate rows), the merchant sets a *flat COD fee* that the platform adds on top of the rate-row price when the customer picks COD as the payment method.

### Currency-aware COD cap

A platform-side **10,000 BGN cap on COD per order** applies **only when the store currency is the literal `BGN`** (the `BG_MAX_COD` platform constant). The cap is checked against the **order subtotal** — so it is **per-order, not per-package** (verified: the comparison reads the order subtotal and hides the COD option when it exceeds the cap; multiple parcels / split shipments don't each get their own allowance). The customer must then pay online.

For **any other currency**, no platform-side cap applies (an "unlimited" sentinel; the carrier's own server-side limits apply). The condition keys on the literal currency string `site('currency') == 'BGN'`, so it is **legacy**: a Bulgarian store that has switched to **EUR** (the new norm after the euro adoption) falls on the no-cap side and gets **no** platform COD cap — only the carrier's own limit. (The platform constant has not been re-denominated to EUR — verify if/when it is.) See [[multi-currency]].

**Per-courier lower cap (`cd_max`):** each courier can set its own `cd_max` COD ceiling; when set above 0, the effective cap is `min(cd_max, platform-cap)` — so a courier can offer COD only up to a lower amount than the 10,000 BGN platform limit.

### The per-provider COD toggle (`cd`)

**Every carrier integration has its own "Activate cash on delivery" toggle.** A courier reports COD support only when its contract allows COD, the merchant has turned the **`cd`** toggle ON in *that* courier's settings (EuShipment / Sendcloud store it as `settings.cod`), AND the order is within the COD cap. Toggle OFF → no COD for that courier even if the contract allows it. Identical across all couriers (Econt, Speedy, DPD, Sameday, GLS, BoxNow, …).

### A COD-only store hides every non-COD method at checkout

When the store's **only** payment provider is Cash on delivery, checkout keeps only methods that currently support COD (see [[shipping-calc-cascade]] → Step 6 special case). A courier with its `cd` toggle **off** is then dropped **entirely** — the whole method plus any locker / office destinations, not just its COD option. This hits **every** courier; [[apps-boxnow|BoxNow]] is the most visible (locker-only → "my lockers vanished"). When the store also offers card / bank transfer, the filter doesn't run.

### How the collected COD amount is determined

The amount collected at the door is **not always the live order total**. The waybill's COD field is pre-filled with a **computed COD total** that depends on three things — the courier's **pricing / calculation model**, the **payer side** chosen on the waybill (who pays the courier for the delivery: *Изпращач* / sender, or *Получател* / receiver), and whether the order has **free shipping**:

- **The payer side decides whether the delivery fee is folded into the COD** (for couriers priced by a live quote / calculation model):
  - **Sender pays (Изпращач):** the merchant fronts the delivery fee to the courier and **recoups it from the customer**, so the COD is the **full order total — shipping INCLUDED**. (The delivery is billed to the sender, but its cost is still collected from the receiver through the COD.)
  - **Receiver pays (Получател):** the customer settles the delivery with the courier **directly**, so the COD is the **order total WITHOUT shipping** (shipping excluded).
- **Free shipping:** the shipping cost is 0, so the COD is just the goods total — no delivery fee is collected either way.
- **Flat-rate couriers** (fixed-price / fixed-weight calculation) pre-fill the **full order total** regardless of payer side.
- **Completed / paid orders** pre-fill the **full order total** (minus any returned-item value).
- **Returns:** the value of items already sent back via completed returns is **deducted** from the computed COD, so the label collects only what actually ships.

> The direction is the opposite of the intuitive reading: it is **not** "the sender pays, so shipping is left out". When the **sender** is the payer side, the shipping **is** in the COD (the merchant is recouping the fee it paid the courier); shipping is left out of the COD only when the **receiver** is the payer side, or when shipping is free.

- **Editable at generation:** the merchant can change it in the waybill form (`waybill.total`).
- **Sticky (`cod_manual`):** once an amount is entered at generation it is stored as the `cod_manual` meta and re-used on every later waybill — it does **not** auto-track later order-total changes.

So a label's COD figure can differ from the current order total (payer side, free shipping, prepayment, post-waybill edit, returns) — the default follows the computed COD total above, and once a manual amount is entered it follows `cod_manual` / the form value, not the live total.

### Automatic paid-sync — the [[orders-sync-cod]] flow

When the carrier collects the cash from the customer at delivery, the carrier's API reports the COD-collected event back to CloudCart. The platform automatically marks the order's payment as `completed` via the [[orders-sync-cod]] flow. The merchant doesn't have to mark it paid manually unless the carrier's sync is misconfigured (or the carrier doesn't support COD sync — some don't).

This is the "Automatically set order status to paid when we get information from shipping provider with Cash on delivery" toggle in the carrier's app settings. When OFF, the merchant must mark the order paid manually after confirming the remittance with the carrier.

### Pre-conditions for end-to-end COD

For COD to work end-to-end, the merchant must:

1. **Have the carrier's COD agreement** — a contractual setup with the carrier's bank that authorises the carrier to collect cash on the merchant's behalf and remit it via bank transfer.
2. **Configure the COD agreement number in the carrier's settings** (e.g., Econt's `cod_account` field, Speedy's equivalent).
3. **Enable the COD-sync toggle** in the carrier's app settings (the "automatically set order status to paid…" option).
4. **Test with a real order** — the carrier's COD account is validated against the merchant's registered carrier-side clients before each quote — outdated configs are silently dropped to prevent failed transactions.

### Carrier-side COD-account validation

Econt and Speedy verify the configured COD account against the merchant's registered carrier-side clients before each quote. If the account number is invalid, expired, or doesn't match the carrier credentials, the COD option is **silently dropped at checkout** — the customer never sees it. This is intentional: better to lose a sale than to ship goods the carrier won't collect cash for. (verify — exact silent-drop behaviour for non-BG carriers.)

For "COD missing at checkout" support tickets, the answer is almost always one of: (a) cart total above 10,000 BGN in a BGN store, (b) COD account number not configured or invalid, (c) carrier didn't return a COD-capable rate for the destination, (d) Cart Rules ([[apps-cart-rules]]) explicitly hide the COD option for this cart, or (e) the courier's own **"Activate cash on delivery" (`cd`) toggle is OFF**. Note the knock-on effect of (e): if COD is the store's *only* payment method, a courier with its COD toggle off does not just lose COD — it disappears from checkout **entirely** (see "A COD-only store hides every non-COD method" above).

## Related

- [[shipping-provider-mechanism]] — hub.
- [[shipping-provider-cod]] — sister entity-side documentation of the COD attributes per provider row.
- [[orders-sync-cod]] — the COD-sync sub-flow that marks the order paid.
- [[shipping-provider-mech-waybill]] — waybill API call carrying the COD amount + currency.
- [[order-pipeline-recalculation]] — frozen-vs-live model; why a `cod_manual` amount can differ from the current order total.
- [[shipping-provider-mech-pricing-models]] — how the surcharge attaches to the priced line.
- [[payment-providers-cod]] — standalone COD payment provider (no carrier collection).
- [[payment-provider-mechanism]] — sister concept for payment integrations.
- [[multi-currency]] — currency rules that make the 10,000 BGN cap currency-aware.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-dpdbulgaria-speedy]] — top carriers with COD support in BGN.
- [[apps-cart-rules]] — Cart Rules can hide / add the COD surcharge.

## Open Questions

- ✅ Resolved: the 10,000 BGN cap is checked against the **order subtotal** (converted to BGN), so it is **per-order**, not per-package — multiple parcels / split shipments share the one order-level allowance.
- ⏸️ Per-carrier behaviour on COD-account validation — Econt + Speedy verified; others not yet verified.
