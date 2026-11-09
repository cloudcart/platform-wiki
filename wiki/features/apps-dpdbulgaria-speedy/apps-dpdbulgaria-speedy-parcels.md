---
type: feature
nav_path: "Apps → DPD Bulgaria (Speedy) → Settings → General settings → Parcels"
route_name: apps.dpdbulgaria.settings
route_path: /admin/shipping/dpdbulgaria/settings
aliases: ["DPD several boxes", "DPD multi-parcel", "Speedy several packages", "Submit product sizes", "Delivery boxes", "Package type by default", "Вид на пакета", "Брой пакети", "DPD international address", "The shipping method has no matching rate", "Методът на доставка няма съвпадаща стойност", "Спиди няколко пакета"]
tags: [apps, shipping, courier, bulgaria, parcels, boxes, international]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[apps-dpdbulgaria-speedy]]. See the hub for channels, pricing and the other settings.

# DPD Bulgaria (Speedy) — parcels, boxes and foreign addresses

## Purpose

How an order is turned into parcels for DPD Bulgaria (Speedy): **Delivery boxes**, **Submit product sizes**, **Package type by default**, how the price is quoted for several parcels, and how a foreign address is matched.

## Where to find it

Apps → **DPD Bulgaria** → **Settings** → the general settings box. Per order: the waybill form on the order ([[orders-shipping-waybill]]).

## What the merchant can do here

- Pick **Delivery boxes** from the boxes defined in [[settings-boxes]].
- Turn **Submit product sizes** on or off.
- Set **Package type by default** and the default weight and sizes of one item.
- Change **Package type** and **Number of packages** on each waybill.

## Settings & fields

- **Delivery boxes** (`boxes`) — a multi-select of the store's boxes. Only the boxes selected here are used for DPD. A box has sizes and weights but no price: CloudCart adds no packaging fee. Whether DPD charges for packaging, and to which payer, is DPD's tariff (verify with DPD).
- **Submit product sizes** (`item_sizes`) — help text: *"When this option is enabled, the dimensions of the products will be submitted and {app} will calculate their volumetric weight. Each product in the cart will be marked as a separate package."*
- **Package type by default** (`packing`, required) — free text naming the packaging (e.g. Carton), sent to DPD as the shipment's package type. It is not a box and carries no price. The waybill form shows it as **Package type** / *"Вид на пакета"*, hint *"In case the shipment is bulky and does not fit in one package, you can write in free text, the type of package. For example: Carton"* / *"…Например: Кашон"*.
- **Default weight / width / depth / height for one item** — used for an item that has no weight or size of its own.

A product's own size is set in the product editor under **Dimensions** (switch *"Define product dimensions like width, height, length"*, then **Length**, **Width**, **Height** in millimetres; simple and multi-variant products), next to the **Not for parcel lockers** switch ([[shipping-provider-mech-locker-fit]]). On Admin GraphQL it reads as the product's `shippingSize` (`width`, `height`, `depth`, `noLocker`) and is written with `width`, `height`, `depth`, `no_locker` on the product input.

## Business rules

### How the parcels are built

1. **Boxes selected** → the items, one unit at a time, are packed into the selected boxes. Each packed box is one parcel with the box's outer size and the weight of what it holds. This happens whether **Submit product sizes** is on or off.
2. **An item fits no box** → the whole packing is dropped (not only that item) and the next step applies.
3. **No boxes, Submit product sizes on** → every product is a separate parcel with its own size; a product sold in whole units becomes one parcel per unit.
4. **No boxes, Submit product sizes off** → no parcels are listed: DPD gets the total weight as one shipment.
5. **Destination outside Bulgaria** → sizes are always sent; when steps 1–4 give no parcel, one parcel is built ([[apps-dpdbulgaria-speedy-waybill-price]]).

### One price and one waybill for all parcels

The quote sends all parcels in one request, and DPD returns one price per service for the whole shipment; the platform does not add up prices per parcel. A waybill is likewise one DPD shipment carrying all the parcels built above, not one waybill per box. When no parcels were built and **Number of packages** / *"Брой пакети"* on the waybill form is more than 1, the weight is split evenly into that many parcels; otherwise the shipment is one parcel. Whether a given DPD service (for example DPD ECONOMY) accepts more than one parcel is DPD's rule (verify with DPD).

### Which countries and addresses DPD is asked about

The app keeps no fixed country list of its own. The address is matched against DPD's own country list; the town is found from the postcode and town name in DPD's postcode list, which DPD provides only for some countries. On a store whose language is neither Bulgarian nor English, and with a Google Maps key, the address is first rewritten in English through Google (for Greece the town is then looked up at DPD). A destination is offered when DPD returns a price for one of the selected **Services**; the merchant's **Ships to** zone limits it further ([[shipping-provider-checkout-filters]]). Size and weight limits for a destination are DPD's.

### "The shipping method has no matching rate"

When an order's shipping is priced again from the order page (adding or editing a product, changing the shipping method) and DPD returns no price and no error text, the admin shows *"The shipping method has no matching rate"* / *"Методът на доставка няма съвпадаща стойност"*. When DPD does return an error, its message is shown instead. At checkout the customer sees the general no-method message ([[shipping-calc-cascade]]).

## Related

- [[apps-dpdbulgaria-speedy]] — hub.
- [[settings-boxes]] — the boxes and their sizes.
- [[shipping-provider-mech-locker-fit]] — product dimensions and the locker fit check.
- [[orders-shipping-waybill]] — the waybill form.

## Open questions

- Which DPD services accept several parcels on one shipment, DPD's size and weight limits per destination, and any DPD packaging charge.
- The Bulgarian labels of these settings, which come from the admin translations database.
