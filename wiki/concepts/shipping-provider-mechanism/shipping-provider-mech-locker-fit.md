---
type: concept
nav_path: "Concept → Shipping provider mechanism → Locker fit"
aliases: ["Locker fit check", "Cart does not fit a locker", "Product too big for a locker", "Locker hidden at checkout", "Not for parcel lockers", "no_locker", "Locker size limits", "Compartment sizes", "Не е за автомат", "Продуктът не влиза в автомат", "Размери на автомат", "Автоматът не се показва", "Скрий доставка до автомат"]
tags: [shipping, couriers, checkout, pickup-points, lockers, products, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

> Part of [[shipping-provider-mechanism]]. See the hub for the other aspects (configuration, pricing models, pickup points, waybill, COD, geo routing, status tracking).

# Shipping provider mechanism — Whether a cart fits a locker or office

## Definition

At checkout every office and locker is checked against the cart, and a point the cart does not fit is not offered. The merchant steers the check through two things on the product: its **dimensions** and the **Not for parcel lockers** switch.

The check runs on the map, the search and the autocomplete, when a point is selected, and again when the shipping quote is taken and the order is submitted. The theme checkout and the headless checkout apply the same rules.

## Scope

Covered: the fit rules, the limits per locker network, the product switch and how to set it in bulk, what the customer sees, and how "Submit product sizes" relates to all this.

Not covered: the picker itself ([[checkout-step-shipping-pickup]]) and how a chosen point is stored and restored ([[shipping-provider-mech-pickup-points]]).

## Contrasts

- **Office vs. locker.** An office is checked item by item, because it can receive several parcels. A locker takes one parcel, so the whole cart has to pack into one compartment.
- **Fit check vs. "Submit product sizes" (`item_sizes`).** The fit check reads each product's own dimensions whatever `item_sizes` says. `item_sizes` decides what is sent to the courier for pricing and the waybill. Off: the order is one piece at the carrier's default per-item weight. On: each product's own dimensions are submitted, the carrier computes **volumetric weight**, and each product becomes a separate package; a product with no dimensions uses the carrier's defaults (`default_width` / `default_height` / `default_depth`). The setting appears on [[apps-dpdbulgaria-speedy]], [[apps-dpdromania]], [[apps-sameday]], [[apps-pigeonexpress]], [[apps-nextlevel]] and others.
- **Size vs. the switch.** Size removes the points the cart does not fit. **Not for parcel lockers** removes locker delivery altogether, for every courier, whatever the size.

## Where it applies

### The fit rules

In this order:

1. **Locker and a flagged product:** refused.
2. **Cart weight above the point's maximum:** refused. The maximum is converted to the unit of the store's cart weight first.
3. **Any item bigger than the point's largest parcel:** refused. Sides are compared sorted, so an item may be turned.
4. **Locker only:** all items must pack together into one compartment, by total volume and then by 3D packing in any orientation.
5. **An item without all three dimensions** counts by weight and flag only. Digital items are ignored.

### Locker limits

The largest compartment decides.

| Network | Compartments, height × width × length (cm) | Max weight |
|---|---|---|
| [[apps-boxnow]] | 8 / 17 / 36 × 45 × 60 | 20 kg |
| [[apps-econt]] Econtomat | 8 / 18 / 37 × 44 × 61 | 20 kg |
| [[apps-dexpress]] | 14 / 29 / 44 × 44 × 47 | 20 kg |
| [[apps-sameday]] easybox | 10 / 20 / 39 × 44.5 × 47 | 20 kg |
| [[apps-pigeonexpress]] | 8 / 20 / 34 × 44 × 61, unless Pigeon's own data gives the point's limits | 30 kg |
| [[apps-dpdbulgaria-speedy]] | Per-point limits from DPD | Per point |

The other networks ([[apps-fancourier]], [[apps-cargus]], [[apps-dpdromania]], the aggregators) are judged by what their point data carries.

Econt offices take up to 1000 kg with no size limit ([[econt-coverage-and-caches]]).

### Not for parcel lockers

A switch under **Dimensions** in the product editor ([[products-editor]]), help text: *"Delivery to a parcel locker is not offered at checkout when this product is in the cart"*. Stored as product meta `no_locker`. A cart holding such a product gets no locker delivery from any courier, and the locker tab is hidden. Offices and address delivery are unaffected.

### Setting the switch in bulk

| Route | How |
|---|---|
| CSV import ([[apps-csv-import-mapping-fields]]) | Column **Not for parcel lockers** (`product.meta_no_locker`). `yes`, `1` or `true` sets it, any other non-empty value clears it, an empty or unmapped column leaves the product as it is. |
| JSON-API v2 ([[api-products]]) | `no_locker` inside the product's `meta`. |
| Admin GraphQL ([[admin-graphql-api]]) | `no_locker` on product create, update and bulk create, with `width`, `height`, `depth` in millimetres (0 to 100000, null clears). Read through `Product.shippingSize` (`width`, `height`, `depth`, `noLocker`). |

### What the customer sees

- A point the cart does not fit is simply not listed.
- With no flagged product and no locker that fits, the locker tab still shows, with an empty map.
- The cart can change after a point was picked, so the point is re-checked at the quote and at order submit. A refusal shows `sf.widget.checkout.nfy.no_shipping_method_available`.
- Point lists are cached for 1 day, so changed limits show after that.
- Lockers take a **single package**. When an order resolves into more than one package, for example with `item_sizes` on, the locker channel can return no method, and the picker says: *"No locker delivery method is available for this order. If the order contains more than one product, it may be a multi-package shipment, which cannot be delivered to a locker. Please choose office or address delivery…"* (`widget.checkout.nfy.no_locker_method_available`). This is separate from the office message (`widget.checkout.nfy.no_office_method_available`) and the address message (`no_shipping_method_available`).

### After checkout

Some couriers also check their limits when the waybill is issued, with `shipping.err.office_max_weight` / `shipping.err.office_max_dimensions`, using the sizes in the waybill form. The packaging side lives on **Delivery boxes** ([[settings-boxes]]): box dimensions and weights feed the volumetric weight sent to the courier when a carrier's *Delivery boxes* setting selects them.

## Related

- [[shipping-provider-mechanism]] — hub.
- [[shipping-provider-checkout-filters]] — the other gates on whether a channel is offered.
- [[shipping-calc-cascade]] — the "no shipping method available" diagnostic.
- [[products-editor]] — dimensions and the switch.
- [[settings-boxes]] — delivery boxes.

## Open Questions

None.
