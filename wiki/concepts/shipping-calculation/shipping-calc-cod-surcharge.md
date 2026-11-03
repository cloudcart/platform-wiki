---
type: concept
nav_path: "Concept → Shipping calculation → COD surcharge"
aliases: ["COD surcharge on shipping", "Cash on delivery shipping fee", "COD cap Bulgaria", "10000 BGN COD cap", "COD re-quote on payment switch", "Наложен платеж надбавка", "Капак за наложен платеж 10000 лв"]
tags: [shipping, cod, payment, checkout, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-calculation]]. See the hub for the other aspects (rate models, geo gating, carrier integrations, the checkout cascade, discounts + Cart Rules, persistence).

# Shipping — COD surcharge

## Definition

A **COD surcharge** is an extra amount added to the shipping quote when the customer's payment method is **Cash on Delivery**. It exists because COD is more expensive for the carrier (the courier handles cash, returns it to the merchant's bank, takes on the risk of refusal) and the merchant typically passes that cost to the customer.

CloudCart applies COD surcharges at **Step 5 of the cascade** ([[shipping-calc-cascade]]), AFTER the rate-model quote (Step 3) and category-rate split (Step 4), BEFORE the allowed-payment filter (Step 6). The surcharge logic differs sharply between custom methods and carrier integrations:

- **Custom methods** ([[shipping-calc-rate-models]]) — the merchant sets a **flat COD fee** per method (often configured in [[settings-cart]] under the COD options, or in the method's per-method settings). The fee is added on top of the rate-row amount when payment = COD.
- **Carrier integrations** ([[shipping-calc-carrier-integrations]]) — the carrier's API includes the COD surcharge **directly in the quoted shipping price**. Speedy / Econt / Cargus add their COD margin to the base shipping rate. There is no separate "+ COD fee" line — the carrier-quoted number already contains it.

Switching payment from COD to online (card, bank transfer, etc.) triggers a **re-quote** on carrier integrations — the surcharge disappears because the next `getQuotes` call omits the COD amount. Custom methods recompute the same way: the flat fee is dropped from the quote.

## Scope

Covered:

- When COD surcharge applies (payment method = COD).
- Custom-method flat-fee vs. carrier-integration carrier-quoted surcharge.
- The 10,000 BGN COD cap enforced by Econt + Speedy for BGN stores.
- Re-quote on payment-method switch.
- Why the COD-with-Econt and COD-with-Speedy options silently disappear above the cap.
- COD-with-non-BGN-stores — no platform cap, carrier's server-side limits apply.

Not covered here:

- The list of supported payment methods generally — see [[settings-payment-providers]].
- The COD payment-method configuration itself — see [[settings-payment-providers]].
- The rate-model arithmetic that runs BEFORE the surcharge — see [[shipping-calc-rate-models]] / [[shipping-calc-carrier-integrations]].
- The allowed-payment-method filter that runs AFTER — see [[shipping-calc-cascade]].

## Contrasts

- **Custom-method flat fee vs. carrier-integration baked-in** — flat fee is a visible "+ X" on the merchant's method configuration; carrier-integration surcharge is invisible (rolled into the carrier's quoted price). The customer sees a single shipping number either way.
- **Re-quote on switch vs. cached quote** — switching payment from COD to card on a carrier integration triggers a re-quote of the carrier API (the surcharge disappears). On custom methods, the platform just recomputes the rate-row amount + drops the flat fee — no API call.
- **10,000 BGN COD cap (Bulgaria) vs. no platform cap elsewhere** — Econt + Speedy enforce a 10,000 BGN cap for BGN stores. Above this, the COD option drops silently. Non-BGN stores have no platform-side cap; the carrier's own server-side rules apply.
- **Surcharge vs. insurance** — both are extra amounts on top of base shipping, but insurance protects the parcel value (configured per-method or per-order) while COD surcharge compensates the carrier for cash handling. The carrier's API quotes them as separate fields; the platform stores them separately on the cart's shipping quote.

## Where it applies

### Custom-method COD fees

For custom methods (`type = price`, `weight`, `price_and_weight`, `marketplace`):

- The merchant configures a flat COD fee per method. The fee location is either:
  - In [[settings-cart]] under the COD options (store-wide default for all custom methods).
  - In the method's per-method settings on [[settings-shipping]] (override for one method).
- When the customer picks COD at checkout, the flat fee is added on top of the rate-row amount: `quote = rate_row.amount + cod_flat_fee`.
- When the customer switches away from COD, the flat fee is removed: `quote = rate_row.amount`.

The merchant sees the COD fee as a separate field; the customer sees the combined number.

### Carrier-integration COD baked-in

For carrier integrations (`type = integration`):

- The platform calls the carrier's `getQuotes` API with the COD amount in the request payload.
- The carrier returns a quoted price that **already includes** the COD margin. There is no separate "+ X" line.
- When the customer switches away from COD, the platform calls `getQuotes` again without the COD amount; the carrier returns a lower base price.

The merchant cannot edit the carrier's COD margin — it's the carrier's pricing.

### The 10,000 BGN COD cap (legacy — BGN-currency stores only)

The platform enforces a 10,000 COD cap (`BG_MAX_COD`) **only when the store currency is the literal `BGN`**. For such stores, carts with `subtotal > 10,000 BGN` where the customer picks COD will not get a quote — the platform silently drops the COD options at checkout. **A store on `EUR` — the new Bulgarian norm after the euro adoption — gets NO platform cap** (the condition still keys on the legacy `BGN` string); only the carrier's own server-side COD limit applies. See [[shipping-provider-mech-cod]] for the full rule.

Behaviour seen by the customer:

- Cart subtotal 9,000 BGN, COD selected → Econt + Speedy show normally.
- Cart subtotal 12,000 BGN, COD selected → Econt + Speedy disappear. Only methods that don't restrict to COD-only remain.
- Cart subtotal 12,000 BGN, card selected → Econt + Speedy show normally (the cap is COD-specific).

The customer must pay online instead. There's no on-screen message about the cap; the merchant must explain it via FAQ / help text.

For **non-BGN stores**, no platform-side cap applies. The carrier's own server-side limits apply — those are not documented in CloudCart and the merchant should consult the carrier directly.

### Re-quote on payment-method switch

When the customer changes payment method on the checkout form (COD → card or card → COD), the platform re-runs Steps 5–6 of the cascade:

- **Step 5** — the COD surcharge is added or removed depending on the new payment method. For carrier integrations, this is a fresh `getQuotes` call.
- **Step 6** — the allowed-payment-method filter re-runs. Methods whose allow-list no longer includes the new payment are dropped from the survivor list.

**Cargus** specifically performs automatic re-quote on payment-method switch — documented as a notable carrier behaviour on [[shipping-calc-carrier-integrations]].

### Why the COD path is operationally fragile

The COD path has more silent-failure modes than any other step in the cascade:

- 10,000 BGN cap → methods disappear above the cap.
- COD payment method not in a shipping method's allowed-payments → that method disappears.
- Carrier API outage → all carrier-integration COD options disappear.
- Misconfigured COD payment method in [[settings-payment-providers]] → COD doesn't appear as a payment option at all.

When a merchant reports "my COD doesn't work for big orders", the 10,000 BGN cap is the first suspect. When "COD works for my smaller carrier but not Econt", the carrier's API or credentials are the suspect.

## Related

- [[shipping-calculation]] — hub.
- [[shipping-calc-cascade]] — Step 5 sits inside the full cascade.
- [[shipping-calc-rate-models]] — custom methods that use the flat-fee path.
- [[shipping-calc-carrier-integrations]] — carrier integrations that bake the surcharge into the carrier's price.
- [[settings-cart]] — store-wide COD options (default flat fee).
- [[settings-shipping]] — per-method COD fee override.
- [[settings-payment-providers]] — COD payment-method configuration.
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-cargus]] — carrier-specific COD config.

## Open Questions

None.
