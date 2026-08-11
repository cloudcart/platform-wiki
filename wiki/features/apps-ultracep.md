---
type: feature
nav_path: "Apps → Ultracep"
route_name: apps.ultracep.overview
route_path: /admin/shipping/ultracep
aliases: ["Ultracep", "Ultra C.E.P", "Ultra CEP", "Ultra C.E.P courier"]
tags: [apps, shipping, courier, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-06-11
source_count: 5
---
# Ultra C.E.P (Ultracep)

## Purpose

**Ultra C.E.P** courier integration. Connects to Ultra's API (`u-cep.com`) for live rate quotes, waybill generation, and country/city/zip data sync. It is part of the OmniShip courier family.

Three things set it apart from other OmniShip couriers:
- **Email-as-identifier** — the merchant signs in with their Ultra account EMAIL, not a separate username + password.
- **Always in test mode** — the integration is hard-coded to Ultra's dev/test endpoint (`u-cep.7thblock.dev`) regardless of any UI flag. A production endpoint exists but is not currently used.
- **Default SENDER pays** — the merchant is the default payer side (absorbs shipping into product price), the opposite of most COD-heavy setups. Can be overridden to receiver-pays per shipment.

## Where to find it

Sidebar → Apps → install → **Ultra C.E.P**. Standard OmniShip sub-pages:

| Sub-page | Route name |
|----------|------------|
| Overview | `apps.ultracep.overview` |
| Settings | `apps.ultracep.settings` |
| Shipments | `apps.ultracep.shipments` |
| Shipments return | `apps.ultracep.shipments-return` |

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials (email + password) in the Settings sub-page; saving validates them against Ultra's API.
- See real-time rate quotes at checkout once credentials are validated.
- Generate waybills + print labels per order.
- Pick which Ultra services to expose at checkout (multi-select loaded from the API service list).
- Add per-waybill options: comment, fragile flag, open-before-pay.
- Manage returns in the Shipments return sub-page.

### What the merchant CANNOT do here
- Use the integration without an Ultra contract / valid email + password.
- Generate waybills for destinations Ultra does not serve (the country list is synced FROM Ultra's API).
- Force production mode — the integration is hard-coded to the test endpoint.

## Settings & fields

The Settings page is the shared OmniShip courier form with a custom credentials card on top.

### Credentials card
| Field | Notes |
|-------|-------|
| **Email** (`email`) | Ultra account email — Ultra's primary identifier (no separate username). Error: "Invalid credentials". |
| **Password** (`password`) | Masked, with eye toggle. Error: "Invalid credentials". |

The `Connect` button validates email + password against Ultra's API; on success the rest of the form appears. There is NO test-mode toggle (the endpoint is fixed).

### Rest of the form
- **Visualization** — courier display name + logo upload.
- **Service-type cards** — `address` only (no locker / pickup-point for the recipient). The pencil opens the Service-type calculator modal: the 6 pricing modes (below) plus the Ultra services multi-select loaded from the API.
- **Ships to (Geo Zones)** — geo-zone allow-list (countries synced from Ultra's API).
- **Payment providers** — payment method multi-select.
- **Additional Settings box** (`parcel_and_waybill_settings`) — three switches only:
  - **Enable cash on delivery** (`cd`) — when ON, COD is offered (capped per OmniShip COD rules).
  - **Fragile Shipment** (`fragile`).
  - **View Shipment** (`open`) — open-before-pay; only valid when the payer side is SENDER (Ultra contract rule).

This box has NO default-weight field, NO send-method selector, NO comment input, and NO payer-side selector. Default weight (`default_weight`, the fallback when product weight is missing), send method (`method_send`), and payer side are derived from defaults; comment is a per-waybill field on the order's waybill form.

### Required-field validation messages
- *"Email address is required"* / *"Password is required"*.
- *"Weight is required"* — missing default weight.
- *"Client ID is required"* (legacy key — still in the language file).
- *"Delivery address is invalid"* — destination cannot be served.

### Waybill validation messages
- *"Please select the party that will pay for the shipment."* / *"The selected paying party is invalid."*
- *"Please choose a shipping service. Run \"Calculate\" first if no options are listed."*
- *"When cash on delivery is selected, you must enter an amount."* / *"The cash on delivery amount must be a number."* / *"The cash on delivery amount must be a positive number."*
- *"The order does not exist or has been deleted."*
- *"The order is not configured for UltraCep delivery."*
- *"A waybill cannot be issued for an archived order."*
- *"The order has no shipping address. Please add an address before generating a waybill."*
- *"The order does not contain any physical products for which a waybill can be issued."*
- *"The order already has a waybill. Please cancel it first if you want to issue a new one."*
- *"Cash on delivery cannot be enabled on an order that is already paid or completed."*

## Business rules

### Coverage countries (synced from Ultra's API)
**Multi-country.** Ultra C.E.P populates its country list from its own API on a sync job; the merchant cannot add countries — whichever ISO codes Ultra returns become available at checkout. Cities and ZIPs are also synced for the address picker.

### Pricing model (six options)
How the checkout price is computed:
- **Ultra C.E.P. calculator** (`calculator`) — real-time price quoted from Ultra's API.
- **Ultra C.E.P. calculator + processing fee** (`calculator_fixed`) — Ultra quote plus a fixed merchant surcharge.
- **Ultra C.E.P. calculator + free shipping** (`free`) — Ultra quote covered by the merchant; customer sees free shipping.
- **Fixed price without Ultra C.E.P. calculator** (`fixed_price`) — flat per cart-value tier.
- **Fixed value by weight** (`fixed_weight`) — flat per weight tier.
- **Fixed value by price and weight** (`price_and_weight`) — combined flat rules.

`calculator_fixed` reveals a **Parcel processing Fee** field; `free` reveals a **Minimum Order Value for Free Delivery** field; the `fixed_*` types reveal their from/to rate table. The calculator types also expose an optional **Fallback price** table; every type adds a **per-category** sub-table. Full field-by-type mechanics: [[shipping-calc-rate-card-fields]].

### Sending methods
- **d2d** (address-to-address) — Ultra picks up at the sender address, delivers at the recipient address.
- **p2d** (office-to-address) — sender drops off at an Ultra office, Ultra delivers to the recipient.

### Payer side & open-before-pay
The default side is SENDER (merchant pays); overridable per shipment to receiver (customer pays). Open-before-pay can only be enabled when the payer side is SENDER — Ultra's contract doesn't allow customer-pay shipments to be opened before payment.

### COD with cap and recalculation
COD is offered when `cd` is ON and the order is within the same OmniShip-family COD cap used by Econt / Speedex / etc. When COD is enabled, switching the order's payment method (COD ↔ online) triggers a shipping-cost recalculation.

### Side effects
- Saving Settings validates email + password against Ultra's API.
- A background sync task refreshes countries / cities / ZIPs / places from Ultra.
- Waybill creation calls Ultra's API; errors surface on the waybill form.

### Permission
Standard apps permission scope.

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- [[orders-sync-cod]] — COD reconciliation.

## Open questions

_None — behavior captured above._
