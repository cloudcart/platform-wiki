---
type: concept
nav_path: "Concept → Shipping calculation → Checkout cascade"
aliases: ["Shipping checkout cascade", "Shipping method filter chain", "Why don't I see shipping at checkout", "Zero matching shipping methods", "Auto-select shipping if only one", "Касетка за филтриране на доставки", "Защо не виждам метод за доставка"]
tags: [shipping, checkout, debugging, cascade, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-24
source_count: 4
---

> Part of [[shipping-calculation]]. See the hub for the other aspects (rate models, geo gating, carrier integrations, COD surcharge, discounts + Cart Rules, persistence).

# Shipping — the checkout cascade

## Definition

The **shipping cascade** is the deterministic 8-step pipeline the platform walks at checkout to decide which shipping methods the customer sees and which is pre-selected. Every method on [[settings-shipping]] is evaluated against every gate; any failure silently drops the method from the candidate list. The customer never sees an explanation of *why* a method is missing — only the survivors.

```
Step 1 Collect candidate methods (active = yes)
Step 2 Filter by geographic scope (target = restofworld OR matching geo_zone)
Step 3 Compute the quote per method (custom rate-row lookup OR carrier getQuotes)
Step 4 Apply category-rate split (custom methods only, when enabled)
Step 5 Apply COD surcharge (when payment = COD)
Step 6 Filter by allowed-payment-method (method's payment allow-list includes customer's choice)
Step 7 Filter by customer-group (per-customer-group restrictions)
Step 8 Present matching methods (auto-select / collapse if only one)
```

Steps 9 and 10 — Discounts + Cart Rules, and persistence — happen AFTER the cart's method is chosen and are documented on [[shipping-calc-discounts-rules]] and [[shipping-calc-persistence]] respectively.

## Scope

Covered:

- The full Step 1–8 sequence with the responsibility of each step.
- What "silently dropped" means at each step.
- The auto-select-if-only-one rule on [[settings-cart]].
- The zero-matching-methods debug procedure.
- Why the cascade is order-sensitive (rate computation must precede COD surcharge; allowed-payment filter must precede final presentation).

Not covered here:

- The arithmetic of Step 3 (custom rate-row lookup) — see [[shipping-calc-rate-models]].
- The arithmetic of Step 3 (carrier `getQuotes`) — see [[shipping-calc-carrier-integrations]].
- The geo-gating details of Step 2 — see [[shipping-calc-geo-gating]].
- The COD surcharge mechanics of Step 5 — see [[shipping-calc-cod-surcharge]].
- Discount + Cart-Rule layering of Step 9 — see [[shipping-calc-discounts-rules]].
- Cart / order persistence of Step 10 — see [[shipping-calc-persistence]].

## Contrasts

- **Silent drop vs. explicit error** — every cascade gate fails silently. The customer sees only the survivors. The merchant has no log of which gate dropped which method. This is the cascade's single biggest support-ticket source.
- **"Match" vs. "auto-select"** — survival means the method shows at checkout. Auto-selection means it's the pre-selected radio. The default-shipping-type on [[settings-cart]] picks the auto-select among survivors.
- **Active gate vs. installed-but-misconfigured** — `active = no` (Step 1) drops cleanly; **installed-but-misconfigured carrier integration** drops at Step 3 because `getQuotes` rejects the request. Both look identical to the customer.
- **Allowed-payment filter vs. customer-group filter** — both are explicit allow-lists per method, but they apply at different steps (6 and 7). A method can pass one and fail the other.

## Where it applies

### Step 1: collect candidate methods

The platform reads every method on [[settings-shipping]] with `active = yes`. Inactive methods are hidden from the customer at checkout.

The list includes both **custom merchant-defined methods** AND **carrier-integration methods** the merchant has installed AND configured. An installed-but-misconfigured carrier integration survives Step 1 but fails Step 3 — see below.

### Step 2: filter by geographic scope

Each candidate is checked against the customer's shipping address. See [[shipping-calc-geo-gating]] for the full details (`target = restofworld` always passes; `target = geo_zone` requires at least one zone-rule match).

### Step 3: compute the quote per method

- **Custom methods** look up the matching rate row by subtotal / weight / both — see [[shipping-calc-rate-models]]. If no row matches, the method is **dropped**.
- **Carrier integrations** call `getQuotes` — see [[shipping-calc-carrier-integrations]]. If the carrier's API rejects the request (invalid credentials, no service in range, weight cap exceeded), the method is **dropped**.

This is the step where installed-but-misconfigured carriers silently disappear.

### Step 4: apply category-rate split (custom methods only)

If the method has "Different price for categories" turned on, the platform computes the rate from the category-specific table for matching lines and sums it with the default-table rate for the other lines. See [[shipping-calc-rate-models]] for the details.

### Step 5: apply COD surcharge

When the customer's payment method is **Cash on Delivery**, some shipping methods add a COD surcharge to the quote. Custom methods add a flat fee; carrier integrations have the surcharge baked into the carrier's quoted price. See [[shipping-calc-cod-surcharge]] for the mechanics and the 10,000 BGN cap for BG carriers.

### Step 6: filter by allowed-payment-method pair

Each method has a multi-select of allowed payment methods. Methods whose allow-list does NOT include the customer's currently-selected payment method are **dropped**.

Practical example: a merchant runs a "Cash on delivery" Econt method AND a "Card on delivery" Econt method as two separate rows. The first has only COD in its allowed-payments; the second has only card. The customer's choice of payment filters which Econt row shows up.

**Special case — when COD is the store's ONLY payment method.** On top of the per-method allow-list, the checkout applies one more filter: if the store has **exactly one configured payment provider and it is Cash on delivery**, only shipping methods that **actually support COD survive**. "Support COD" here is the *integration's own COD capability*, not the per-method allow-list — and **every** carrier integration gates that on its own *"Activate cash on delivery"* (`cd`) toggle plus the COD cap. So in a COD-only store, **any courier whose COD toggle is off is dropped entirely**, taking its destination types (locker / office) with it. This applies to all couriers (Econt, Speedy, DPD, Sameday, GLS, Cargus, BoxNow, …) — [[apps-boxnow|BoxNow]] is just the most visible because it is locker-only, so the symptom reads as "my lockers vanished". See [[shipping-provider-mech-cod]] for the per-provider toggle and the full rule. When the store also offers card / bank transfer / etc., this extra filter does **not** run.

### Step 7: filter by per-customer-group restrictions

If the merchant has configured customer-group restrictions (e.g., wholesale customers see a different set of shipping methods), those gates run here. Standard customers see one set, VIPs see another. Configured via [[customers-custom-groups]] — the per-method allowed-customer-groups multi-select (verify per-method UI).

### Step 8: present matching methods at checkout

The customer sees every method that survived Steps 1–7. Behaviour depends on [[settings-cart]]:

- The **default-shipping-provider** picks the initial selection among survivors.
- *"Automatically select shipping if only one is available"* — if ON and only one method survived, the platform pre-selects it and may collapse the picker entirely.
- If ZERO methods survived, the customer sees an error and cannot complete checkout — see the debug procedure below.

### Zero-matching-methods debug procedure

When the customer sees "no shipping method available" at checkout, the merchant walks the cascade in order:

1. **Step 1** — Are any methods `active = yes` on [[settings-shipping]]? If not, activate one.
2. **Step 2** — Does any active method's geo scope include the customer's country (or zone, polygon, distance)? If the only methods are `target = geo_zone` and the zone doesn't include the country, the customer sees nothing. Either add `target = restofworld` fallback or extend the zone via [[settings-geo-zones]].
3. **Step 3 (custom)** — Does any active method's rate table cover the cart's subtotal / weight? If the lowest row's `from` is above the cart subtotal, the method is dropped. Add a low-bracket row.
4. **Step 3 (carrier)** — Are the carrier's credentials valid on the carrier's app screen (e.g., [[apps-econt]], [[apps-dpdbulgaria-speedy|Speedy]])? Failed authentication drops the method silently.
5. **Step 6** — Does any active method allow the customer's selected payment method? If the only methods restrict to "card" and the customer picked COD, the customer sees nothing. **Also**: if the store's ONLY payment method is COD, **any** courier whose *"Activate cash on delivery"* (`cd`) toggle is OFF is dropped entirely — [[apps-boxnow|BoxNow]] is the most visible (locker-only), but Econt / Speedy / etc. vanish the same way. The relevant gate is the courier's own COD toggle (see the Step 6 special case above + [[shipping-provider-mech-cod]]).
6. **Step 7** — Has the customer been placed in a customer group that no method allows?

The platform does not surface which gate dropped which method. The merchant must work through this manually.

**Customer-side cause — a stale restored pickup point.** The steps above are all merchant configuration. One cause is on the customer's side instead: a **returning customer reusing a saved address that carries a previously-chosen office / locker**. The storefront restores that pickup point and pre-selects it; if the carrier has since decommissioned or removed it (or no longer serves it), resolution returns nothing and the *same* red error appears even though the typed address is perfectly valid — so the message's "check your address" hint is a red herring here. Re-opening the picker and choosing a current office / locker clears it. See [[shipping-provider-mech-pickup-points]] for the persistence mechanism.

**Locker-specific cause — parcel exceeds the compartment's size / weight.** A locker (or office) is dropped when the parcel is **heavier than that location's max weight** or **bigger than its max dimensions**. With the carrier's *"Submit product sizes"* (`item_sizes`, volumetric-weight) option ON, the **products' own dimensions** drive this and each product counts as a separate package — so a single product with wrong / oversized / missing dimensions (missing → the carrier's default size, e.g. 100 mm) can make lockers vanish or the order fail at waybill. When a locker "doesn't work" and volumetric weight is on, check the **actual product dimensions submitted** and the **selected delivery box** ([[settings-boxes]]). A locker also can't take a **multi-package** shipment, so an order that splits into several packages loses the locker option — the checkout now shows a locker-specific message saying exactly that (`widget.checkout.nfy.no_locker_method_available`), distinct from the office-specific and generic-address messages. See [[shipping-provider-mech-pickup-points]] for the size/weight limits and the multi-package rule.

### Auto-select rule recap

When only ONE method survives AND *"Automatically select shipping if only one is available"* is ON on [[settings-cart]], the platform pre-selects it and may hide the shipping picker entirely. This is helpful for stores with a single shipping option but confusing when a merchant adds a second method and the picker doesn't reappear immediately — clearing the cart / refreshing the checkout usually fixes the cached view.

## Related

- [[shipping-calculation]] — hub.
- [[shipping-calc-rate-models]] — Step 3 arithmetic for custom methods.
- [[shipping-calc-carrier-integrations]] — Step 3 arithmetic for live-API carriers.
- [[shipping-calc-geo-gating]] — Step 2 in detail.
- [[shipping-calc-cod-surcharge]] — Step 5 mechanics.
- [[shipping-calc-discounts-rules]] — Step 9 layering after the cascade.
- [[shipping-calc-persistence]] — Step 10 cart / order save.
- [[settings-shipping]] — method-list + active toggle (Step 1).
- [[settings-cart]] — default-shipping-provider + auto-select-if-only-one (Step 8).
- [[customers-custom-groups]] — customer-group restrictions (Step 7).
- [[checkout-flow]] — customer-facing screen presenting the surviving methods.

## Open Questions

None.
