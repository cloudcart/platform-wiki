---
type: concept
nav_path: "Concept → Shipping provider mechanism → Pickup points"
aliases: ["Pickup point selection", "Office picker", "Locker picker", "To office vs to locker", "Econtomat", "BoxNow locker", "Speedy APT", "Карта на офиси", "Избор на офис", "Избор на локер"]
tags: [shipping, couriers, providers, checkout, pickup-points, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-24
source_count: 4
---

> Part of [[shipping-provider-mechanism]]. See the hub for the other aspects (configuration, pricing models, waybill, COD, geo routing, status tracking).

# Shipping provider mechanism — Pickup points

## Definition

**Pickup-point selection** is the checkout-time step where a customer who chose a "to office" or "to locker" delivery channel picks a *specific* carrier-owned location to collect from. The storefront calls the carrier's offices API, renders the nearby locations on a map / list, and stores the chosen pickup point on the cart so the waybill (issued later via [[shipping-provider-mech-waybill]]) knows the exact destination.

This is the moment the customer commits to "Econt office #42 in Sofia Mladost", "BoxNow locker on Vitosha Blvd", or "Speedy APT 27 in Plovdiv". For "to address" channels the picker is skipped entirely — the customer's saved delivery address is used directly.

## Scope

Covered:

- When the picker appears and when it's skipped.
- The carrier's offices API + server-side cache window.
- Per-carrier network coverage (Econt, Speedy, BoxNow, Cargus).
- How the chosen pickup point is stored on the cart and surfaces in the waybill.

Not covered:

- The pricing of each delivery channel — see [[shipping-provider-mech-pricing-models]].
- The waybill API call that ships *to* the chosen pickup point — see [[shipping-provider-mech-waybill]].
- Local-store pickup ([[apps-stores]]) — that's the merchant's own store, not a carrier-owned location.

## Contrasts

- **To address vs. to office / branch vs. to locker**: most Bulgarian / Romanian carriers expose three delivery channels. To address = home delivery (the courier brings the package to the customer's door — no picker). To office / branch = the customer picks up at a specific carrier office staffed during business hours (picker shows office list with working hours). To locker = the customer picks up at a 24/7 self-service locker — Econtomat, BoxNow locker, Speedy APT (picker shows locker list with addresses + size hints). Each channel may have a different price; the customer picks one at checkout. BoxNow is locker-only (no "to address" option).
- **Office vs. locker**: offices are staffed during business hours and accept any package size the carrier supports. Lockers are self-service 24/7 but have hard size + weight limits per compartment — see *Locker / office size + weight limits* below for how the parcel size is computed (incl. the "Submit product sizes" / volumetric-weight setting) and when a locker is hidden vs. rejected.
- **Pickup point on the carrier vs. Local Pickup**: pickup-point selection on a carrier (Econt office, BoxNow locker) is part of the carrier's network — the customer chooses which carrier-owned location to receive at. Local Pickup ([[apps-stores]]) is the merchant's own physical store — the customer picks one of the merchant's locations from the catalogue and there's no carrier involved.

## Where it applies

### The picker at checkout

When the customer picks a delivery channel that requires a specific pickup point (to office or to locker), the storefront's office / locker picker calls the carrier's offices API. The picker shows nearby carrier-owned locations with addresses, working hours (for offices), and any locker-specific notes (e.g., maximum parcel size). The customer picks one; the chosen pickup point is stored on the cart and travels with the order through to [[orders-shipping-waybill]].

For the "to address" channel the picker is skipped — the customer's saved delivery address (or the address they typed) is used directly.

### Per-carrier network coverage

Each carrier offers different pickup network coverage:

- **Econt**: thousands of Econt offices + Econtomat lockers across Bulgaria + Romania.
- **Speedy**: thousands of Speedy offices + Speedy APT lockers across Bulgaria + Romania.
- **BoxNow**: locker-only network across Bulgaria, Romania, Greece, Cyprus, Croatia.
- **Cargus**: home delivery + office network across Romania.
- **DPD / DHL / GLS**: home delivery + limited pickup point networks in some markets (verify per carrier).

The merchant doesn't manage these networks — they belong to the carrier. The carrier updates its own office / locker registry; CloudCart reads it via the carrier's API.

### Locker / office size + weight limits — the volumetric-weight debug angle

Every office and locker in a carrier's registry carries **hard limits** that CloudCart reads alongside its address: a **maximum parcel weight** (kg) and **maximum parcel dimensions** (width × height × length, cm). Lockers are physical compartments, so these limits bite hardest there. At checkout the office/locker filter **drops any location whose max weight is below the cart's parcel weight**, and the carrier **rejects a waybill whose package width / height / depth exceeds the chosen location's limits** (validation strings `shipping.err.office_max_weight` / `shipping.err.office_max_dimensions`). So an over-limit parcel makes a locker either silently disappear from the picker (weight filter) or fail later when the order's waybill is issued (dimension check).

**What "parcel size" means depends on the carrier setting "Submit product sizes" (`item_sizes`)** — exposed on [[apps-dpdbulgaria-speedy|Speedy]], [[apps-dpdbulgaria-speedy]], [[apps-dpdromania]], [[apps-sameday]], [[apps-pigeonexpress]], [[apps-nextlevel]] and others:

- **Off** — the order is treated as a single piece using the carrier's default per-item weight, so only cart weight really drives the locker filter.
- **On** — each product's **own dimensions** are submitted, the carrier computes **volumetric weight**, and **each product becomes a separate package**. Now the individual product dimensions directly decide whether a locker fits.

This is the key fact when **debugging "a specific locker doesn't work"** (it never appears, or it's offered but the order then fails) and the courier has volumetric weight switched on: investigate the **actual dimensions submitted for the products in the cart**. A product with wrong, oversized, or missing dimensions is the usual culprit — and a product with **no dimensions set falls back to the carrier's default** width / height / depth (`default_width` / `default_height` / `default_depth`, e.g. 100 mm each on Speedy), which can itself be larger than a small compartment. Correcting the product's real dimensions (or the carrier defaults) is what makes the locker eligible again.

The packaging side of the same calculation lives on the **Delivery boxes** screen ([[settings-boxes]]): the merchant defines each box's outer / inner dimensions, empty weight, and max content weight there, and a carrier's *Delivery boxes* multi-select chooses which of those boxes it may pack the order into. Those box dimensions also feed the parcel volumetric weight — so when the submitted size looks wrong, both the **product's own dimensions** and the **selected delivery box** are worth checking.

**Multi-package orders lose the locker option — and the checkout now says so.** Lockers accept a **single package**; when an order resolves into more than one package — for example with *"Submit product sizes"* (`item_sizes`) on, where each product becomes its own package, or when the items won't fit one box — the locker channel can return no method. In that case the picker shows a **locker-specific** message: *"No locker delivery method is available for this order. If the order contains more than one product, it may be a multi-package shipment, which cannot be delivered to a locker. Please choose office or address delivery…"* (lang `widget.checkout.nfy.no_locker_method_available`). It is distinct from the office-specific `widget.checkout.nfy.no_office_method_available` and from the generic address-level `no_shipping_method_available` — so a customer who can't pick a locker for a bigger / multi-item order is told the actual reason rather than being sent to re-check their address.

### Server-side cache window

The list of offices / lockers shown at checkout is server-side cached (Econt's list is cached for 1 day; similar pattern across other carriers). When a carrier adds or closes a location, merchants and customers see the change within the cache window without anyone on the merchant side doing anything. This is intentional — calling the offices API per checkout would be both slow (network round-trip) and rate-limited by carriers.

For "stale-office" support tickets ("I picked an office that turned out to be closed"), the answer is almost always that the carrier closed the office within the cache window and the customer caught the registry mid-update. (verify — exact cache TTL per carrier.)

### The chosen pickup point persists on the saved address — and a stale one can block checkout

The office / locker a customer picks is stored on their **saved shipping address** (`office_id` plus an `office_type` flag — `0` = office, `1` = locker), not only on the live cart. For a logged-in customer this means the choice **survives across sessions**: when they come back and start a new order, the storefront restores the most recent saved address that carries a pickup point and **pre-selects that same office / locker** in the picker (it loads the latest saved address whose `office_id` is set).

That restore is normally a convenience, but it has a failure mode. If the **restored pickup point is no longer valid** — the carrier decommissioned that locker / closed that office, dropped it from its current registry, or changed coverage so no active courier serves it — the shipping-method resolution for the restored address can come back **empty**, and the customer is blocked on the shipping step with the generic red error:

> *"Не можем да открием подходящ метод за доставка за посочения от вас адрес. Моля, променете адреса си …"*

(lang `widget.cart.nfy.no_shipping_method_available` / `widget.checkout.nfy.no_shipping_method_available`). The message asks the customer to recheck the **address** they typed, so the address itself is the obvious suspect — but in this case the typed address is fine; it is the **restored pickup point** that no longer resolves. Re-opening the office / locker picker and choosing a currently-valid pickup point clears the error and lets checkout continue. This is not locker-specific (an office can go stale the same way) and not carrier-specific — it surfaces on whichever courier the stale pickup belonged to.

### How the chosen pickup point flows downstream

Once chosen at checkout:

- Stored on the cart as the office / locker identifier (carrier-specific code).
- Surfaces on [[orders-details]] in the shipping section, alongside the carrier and delivery channel.
- Passed to the carrier's `createBillOfLading` / `createAWB` / equivalent API when [[orders-shipping-waybill]] runs — the carrier uses it to route the package internally.
- Visible to the customer in the order-confirmation email + their account's order page.

## Related

- [[checkout-step-shipping-pickup]] — storefront UI of the office/locker picker; Google-Maps-vs-no-Maps fallback; the typeahead search that always works.

- [[shipping-provider-mechanism]] — hub.
- [[shipping-provider-mech-waybill]] — the per-order action that uses the chosen pickup point.
- [[shipping-provider-mech-pricing-models]] — per-channel pricing differences.
- [[shipping-provider-delivery-channels-waybill]] — sister entity-side documentation of the delivery channels and how they map to waybill API calls.
- [[shipping-provider-checkout-filters]] — what gates whether a channel is even offered at checkout.
- [[shipping-calc-cascade]] — the "no shipping method available" diagnostic cascade; a stale restored pickup point (above) is the customer-side cause of that same red error.
- [[settings-boxes]] — the Delivery boxes screen where packaging dimensions + weights are defined; feeds the volumetric-weight calc that decides whether a parcel fits a locker.
- [[checkout-flow]] — the cart-to-order transition where the picker appears.
- [[orders-details]] — per-order edit hub; shows the chosen pickup point.
- [[orders-shipping-waybill]] — per-order waybill action.
- [[apps-stores]] — merchant-owned Local Pickup (distinct from carrier offices).
- [[apps-econt]] / [[apps-dpdbulgaria-speedy|Speedy]] / [[apps-boxnow]] / [[apps-cargus]] — top carriers with per-carrier pickup networks.

## Open Questions

- ⏸️ Exact cache TTL for the offices / lockers list varies per carrier. Econt is documented at 1 day; others not yet verified.
