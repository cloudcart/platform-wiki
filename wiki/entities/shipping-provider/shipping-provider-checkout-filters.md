---
type: entity
nav_path: "Entity → Shipping Provider → Checkout filters"
aliases: ["Shipping provider checkout filters", "Shipping method visibility", "Allowed payment methods filter", "Customer-group restrictions", "Geo zone scoping", "Default shipping selection", "Country-default shipping recommendations", "Cart rules shipping override", "Define payment methods", "Payment providers per courier", "Ships to", "Set custom shipping regions"]
tags: [entity, shipping, couriers, providers, checkout, filters, geo-zones, customer-groups, cart-rules]
created: 2026-06-10
updated: 2026-11-09
source_count: 2
---

> Part of [[shipping-provider]]. See the hub for the other aspects (attributes, lifecycle, pricing models, COD, delivery channels & waybill).

# Shipping Provider — Checkout filters

## Identity

At checkout, the platform takes the full list of installed shipping methods and **filters them down** to the candidates that match the customer's cart. The filters are layered: geographic scope, payment-method allow-list, customer-group restriction, country-default recommendations, plus any [[apps-cart-rules]] override. This page catalogues every filter that decides whether a configured Shipping Provider's methods appear (or are pre-selected) for a given customer.

## Aliases

- **Shipping method visibility** — what filtering produces.
- **Allowed payment methods filter** — payment-side scoping.
- **Customer-group restrictions** — group-side scoping.
- **Geo zone scoping** — geographic scoping.
- **Default selection** / **Auto-select shipping** — the pre-pick rule.
- **Cart Rules shipping override** — late-stage override.

## Key Attributes

### Geographic scope — Geo Zone vs carrier coverage

- **Custom methods** are scoped by [[settings-geo-zones|Geo Zones]] — each Custom method has ONE geographic scope (the whole world OR one Geo Zone).
- **Carrier-integration methods** can also be limited to one Geo Zone, on the courier's settings screen, box **Ships to** (switch **Set custom shipping regions**; not on Glovo). Addresses outside the zone get no such method, and its offices and lockers outside the zone are not listed. Within the zone, the carrier's API decides coverage: Econt decides which postcodes Econt serves. The "Deliver to" column on [[settings-shipping]] shows *"Regions are determined by the provider"* for every courier, zone or not ([[shipping-provider-mech-geo-routing]]).

### Allowed-payment-methods filter

Each shipping method, custom or courier, can carry a list of allowed payment methods. On a courier it is the **Payment providers** box of its **Settings** tab: the switch **Define payment methods** reveals a multi-select. Rules:

- **Switch off or list empty → every payment method is allowed.** Turning the switch off and saving empties the list.
- **List set → once the customer picks that shipping method, the payment step offers only the listed methods.** The shipping method itself is not hidden by the payment choice. Same for draft-order payment links.
- **A payment method installed later is not added** to any existing list; the merchant adds it, or checkout never offers it with that courier.
- Cash on delivery is also removed when the courier has COD off or its quote does not allow COD.

The courier's **Payments** tab (Econt, DPD Bulgaria) is something else: the log of the cash-on-delivery payout sync ([[orders-sync-cod]]).

### Customer-group restrictions

[[customers-custom-groups|Customer groups]] can restrict which shipping methods are visible to which group. Common pattern: wholesale customers see a different set (heavy / pallet-only) than retail customers.

Configured via:

- **Per-method allowed-customer-groups multi-select** — exposed on **Custom methods only**. Carrier-integration methods (Econt, Speedy, BoxNow, Cargus, DPD, etc.) do NOT have a per-method customer-group restriction.
- **Customer-group side allowed-methods config** — to restrict carrier-integration methods to specific customer groups, the merchant uses the [[customer-group|Customer Group]]'s own allowed-methods configuration instead.

### Default selection at checkout

The default shipping method auto-selected at the customer's checkout step is configured in [[settings-cart]] — NOT in [[settings-shipping]]. The setting picks both:

- **Default shipping TYPE** (carrier vs. custom).
- **Default PROVIDER** (specific carrier).

When [[settings-cart]]'s *"Automatically select shipping if only one is available"* toggle is ON and exactly one method matches the customer's cart, that method is pre-selected without showing the picker.

### Country-default recommendations

The platform tags certain shipping methods as **Recommended** based on the store's [[settings-general]] operation country. The "Browse shipping integrations" modal on [[settings-shipping]] filters its app list by that country:

- Bulgarian stores see Econt / Speedy / Bulgarian Posts.
- Romanian stores see Fan Courier / Cargus / DPD Romania.
- Etc.

The merchant cannot override this filter — to access integrations for other countries, they change the operation country in Settings → Store settings.

### Cart Rules can override the shipping line

[[apps-cart-rules]] can override the standard shipping pipeline:

- Force a specific shipping method on qualifying carts.
- Modify the shipping line (add / subtract / percent).
- Add / remove COD surcharges.

Cart Rules run **AFTER** discounts on the cart, so a free-shipping discount that already zeroed the line will see zero shipping when the Cart Rule runs. See [[shipping-calculation]] for the full arithmetic.

### Re-quoting on payment-method change is carrier-specific

- **Cargus** recalculates the quote when the payment method changes (COD vs card affects the cost).
- **Other carriers** (Econt, Speedy, DPD, GLS) re-quote only on cart-level changes (address change, weight change) — not on payment-method change.

To force re-quote on payment switch with other carriers, the merchant must configure a Custom method with COD-specific rate rows.

## Where it appears

- [[checkout-flow]] — where filters resolve to a visible list of methods.
- [[settings-shipping]] — per-method filter configuration (allowed payments, allowed customer groups for Custom methods).
- [[settings-cart]] — default selection + *"Automatically select shipping if only one is available"* toggle.
- [[settings-geo-zones]] — geographic scope for Custom methods.
- [[customers-custom-groups]] — customer-group side allowed-methods configuration.
- [[settings-general]] — operation country driving the Recommended filter.
- [[apps-cart-rules]] — late-stage override.

## Related

- [[shipping-provider]] — hub.
- [[shipping-provider-pricing-models]] — Custom-method status enables the per-method customer-group multi-select.
- [[checkout-flow]] — the cart-to-order transition where filtering happens.
- [[settings-shipping]] — central hub.
- [[settings-cart]] — defaults + auto-select.
- [[settings-geo-zones]] — Custom-method scope.
- [[customer-group]] / [[customers-custom-groups]] — group-side restrictions.
- [[apps-cart-rules]] — shipping-line override.
- [[payment-provider]] — sister filter dimension (allowed-payments list).
- [[geo-targeting]] — geographic gating used by Custom methods.
- [[settings-general]] — operation country.

## Open Questions

- Whether the *"Automatically select shipping if only one is available"* toggle considers a single carrier with multiple channels (address vs office) as "one method" or several `(verify)`.
