---
type: concept
nav_path: "Concept → Shipping calculation → Rate-card fields"
aliases: ["Delivery price calculation fields", "Rate card fields", "Courier pricing fields", "Parcel processing fee", "Minimum order value for free delivery", "Fallback price", "Fixed value by price", "Fixed value by weight", "Free delivery service", "Полета за изчисление на доставка", "Такса обработка", "Резервна цена"]
tags: [shipping, carriers, omniship, rate-card, pricing, concepts]
plan_gates: []
created: 2026-06-26
updated: 2026-06-26
source_count: 1
---

> Part of [[shipping-calculation]]. See the hub for the other aspects (rate models, geo gating, the checkout cascade, COD surcharge, discounts + Cart Rules, persistence).

# Shipping — rate-card fields by calculation type

## Definition

Every courier-integration **channel** (to **address** / to **office** / to **locker**) is configured by its own **rate card**, opened from the courier's Settings page. Each rate card has one **"Delivery price calculation"** select, and **picking a type reveals a specific set of fields**. This page catalogues those fields and how they behave. The set is **shared** across every OmniShip courier ([[apps-econt]], [[apps-dpdbulgaria-speedy|DPD Bulgaria]], [[apps-sameday]], [[apps-cargus]], [[apps-fancourier]], …); only **which** types each courier offers, and a couple of courier-specific extras, vary (see "Which types each courier offers" below). The from/to rate-row table semantics live on [[shipping-calc-rate-models]]; the live-quote path on [[shipping-calc-carrier-integrations]].

## Scope

Covered: the **"Delivery price calculation"** select on each per-channel rate card, the inline field each of the six types reveals, the free-delivery service selects, the fallback-price switch, the per-category sub-table, the office/locker country select, and which couriers offer which types. **Not** covered: the from/to rate-row lookup arithmetic ([[shipping-calc-rate-models]]), the live `getQuotes` call ([[shipping-calc-carrier-integrations]]), and each courier's credentials / sender / waybill settings (the per-courier Settings pages).

## The calculation types and the field each one shows

The setting key on the channel is `price_calculator_<channel>` (a.k.a. `pricing_<channel>`); the value is one of:

| Type (setting value) | What the merchant sees when it is selected | Where the price comes from |
|---|---|---|
| `calculator` | **No extra inline field** — the courier's live quote is the price. | Live courier quote |
| `calculator_fixed` | A **Parcel processing Fee** currency field (`fixed_price_<channel>`) added on top of the quote. | Live quote **+** the fee |
| `free` | A **Minimum Order Value for Free Delivery** currency field (`free_shipping_total_<channel>`). Below the threshold the customer pays the live quote; at/above it, delivery is free. *(Some couriers also show the free-service selects below.)* | Live quote, **free** above the threshold |
| `fixed_price` | A **Fixed value by price** rate table — rows keyed by **cart subtotal** (`from` / `to` / `amount`). The courier quote is ignored. | The table |
| `fixed_weight` | A **Fixed value by weight** rate table — rows keyed by **total weight**. | The table |
| `price_and_weight` | A combined matrix keyed by **both cart subtotal and weight**. | The matrix |

Each rate-table row is **from / to / amount**; a **blank upper bound (`to`) means unbounded** (the bracket runs to infinity) — full lookup rules on [[shipping-calc-rate-models]]. The key for the free type is literally **`free`** (not `calculator_free`); its option label is usually "Free shipping".

## Free-delivery service selects — `free` only, multi-service couriers only

Couriers that quote **several services** add, under the minimum-order-value field, selects that pick **which service fulfils each free leg**: **Select Free Delivery Service within the City** (`free_method_city_<channel>`), **Select Intercity Delivery Service** (`free_method_intercity_<channel>`), and (DPD only) **Select International Delivery Service** (`free_method_international_<channel>`, multi-select). These appear only for **[[apps-fancourier|Fan Courier]], [[apps-dpdromania|DPD Romania]], [[apps-dpdbulgaria-speedy|DPD Bulgaria]], and [[apps-sameday|Sameday]]**. Single-service couriers show only the minimum-order-value field.

## Fallback price — calculator types only

For `calculator`, `calculator_fixed`, and `free`, the card also shows a **"Fallback price for `<channel>` delivery"** switch. When ON it reveals a **price + weight rate table** the platform uses **only when the live quote can't return a price** (carrier API error, address out of coverage) — so the channel still offers *something* instead of silently disappearing at checkout. The `fixed_*` types have **no** fallback switch — their table already *is* the price.

## Category-condition sub-table — every type

Every type exposes a **"Set different pricing conditions for products in category/ies for `<channel>` delivery"** sub-switch. When ON it reveals a **parallel rate table that applies only to carts containing products in the chosen categories** — letting the merchant charge a different rate for specific categories. For the calculator types this sits inside the Fallback block; for the `fixed_*` types it sits directly under the main table.

## Office / locker country select

On the **office** and **locker** channels, **[[apps-dpdromania|DPD Romania]]** and **[[apps-dpdbulgaria-speedy|DPD Bulgaria]]** add a **country** multi-select (`<channel>_countries`) that controls which countries' offices / lockers are shown to the customer.

## Which types each courier offers

The available options are **server-driven per courier** (each courier declares its own type list). Three patterns cover almost all of them:

- **All six** (`calculator`, `calculator_fixed`, `free`, `fixed_price`, `fixed_weight`, `price_and_weight`) — Acs Courier, Albanian Courier, [[apps-cargus|Cargus]], [[apps-dhl|DHL]], [[apps-dhlexpress|DHL Express]], [[apps-dpdbulgaria-speedy|DPD Bulgaria]], [[apps-dpdromania|DPD Romania]], [[apps-eushipment|EuShipment]], [[apps-evropat|Evropat]], [[apps-fancourier|Fan Courier]], Next Level, Pigeon Express, [[apps-sameday|Sameday]], [[apps-sendcloud|SendCloud]], Ultracep.
- **No `calculator_fixed`** (so: `calculator`, `free`, `fixed_price`, `fixed_weight`, `price_and_weight`) — **[[apps-econt|Econt]]**.
- **Fixed tables only** (`fixed_price`, `fixed_weight`, `price_and_weight`; no live calculator at all, so no `calculator` / `calculator_fixed` / `free`) — **[[apps-boxnow|BoxNow]]**, [[apps-dexpress|D Express]], [[apps-gls|GLS]], MikMik, NTC Logistics, TCS Courier.

Two outliers: **Speedex** offers `calculator` + the three `fixed_*` types (no `calculator_fixed` / `free`); **[[apps-glovo|Glovo]]** offers only the calculator types (`calculator`, `calculator_fixed`, `free`) and no fixed tables.

## Contrasts

- **Calculator types vs `fixed_*` types** — `calculator` / `calculator_fixed` / `free` take the price from the **live courier quote** (any rate table is only a *fallback*); `fixed_price` / `fixed_weight` / `price_and_weight` **ignore the quote** and read the price straight from the merchant's table.
- **Fallback table vs fixed table** — the same from/to rate editor, opposite role: a fallback fires **only when the quote fails**; a fixed table **is** the price every time.
- **Processing fee vs minimum-order-value** — `calculator_fixed` *adds* a fee on top of the quote; `free` *removes* the charge above a threshold.

## Where it applies

- The per-courier **Settings → rate-card editor** on every OmniShip courier ([[apps-econt]], [[apps-dpdbulgaria-speedy|DPD Bulgaria]], [[apps-sameday]], [[apps-cargus]], [[apps-fancourier]], [[apps-boxnow]], [[apps-dpdromania]], [[apps-gls]], [[apps-glovo]], …).
- [[settings-shipping]] — where the configured courier method then appears alongside custom methods.
- [[checkout-flow]] — where the resulting price (live quote, fee-adjusted, free, or table value) is shown to the customer.

## Related

- [[shipping-calculation]] — hub.
- [[shipping-calc-rate-models]] — the from/to rate-row table semantics these fields write into.
- [[shipping-calc-carrier-integrations]] — the live-quote path the calculator types feed.
- [[settings-boxes]] — package dimensions feeding the weight used by `fixed_weight` / `price_and_weight`.
- per-courier Settings pages: [[apps-econt]], [[apps-dpdbulgaria-speedy|DPD Bulgaria]], [[apps-sameday]], [[apps-cargus]], [[apps-fancourier]], [[apps-boxnow]], etc.

## Open Questions

None.
