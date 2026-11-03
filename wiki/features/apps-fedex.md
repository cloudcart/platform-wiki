---
type: feature
nav_path: "Apps → FedEx (tracking only)"
route_name: n/a
route_path: n/a
aliases: ["FedEx", "Federal Express", "FedEx tracking"]
tags: [apps, shipping, courier, tracking-only, no-integration]
plan_gates: []
created: 2026-05-27
updated: 2026-05-27
source_count: 2
---
# FedEx (tracking-link stub — NOT a full integration)

## Purpose

**FedEx is NOT a real shipping integration on CloudCart.** Unlike Econt / Speedy / DHL / DHL Express, there is no FedEx app, no Settings page, no Vue component, no API connection, and no waybill generation. FedEx exists in the platform purely as a **tracking-link template** so a merchant who ships via FedEx through other means (manual booking via fedex.com, third-party broker, etc.) can paste a FedEx tracking number into an order and the storefront / order email links the customer through to FedEx's own tracking site.

## Where to find it

There is no FedEx-specific admin page or App Store install tile. The FedEx tracking-link template is referenced internally when a FedEx tracking number is attached to an order — the formatted link surfaces in the order detail and customer-facing emails.

## Where it lives (in the codebase)

- A single config entry in `shipping_provider.php` (key: `fedex`, name: `FedEx`, `active: 0`, `integrity: false`).
- The `tracking_link` template: `http://www.fedex.com/Tracking?tracknumbers={$tracking_number}&action=track`.
- That's it. No App Store tile, no Apps → FedEx sidebar item, no provider page in the admin.

## What the merchant can do here

- On any order, if the merchant ships via FedEx outside CloudCart, they can manually attach a FedEx tracking number to the order; CloudCart formats the tracking URL using FedEx's tracking link template and surfaces it in the customer's order detail / email.
- Nothing else.

### What the merchant CANNOT do
- Install FedEx as a shipping provider — there is no install flow.
- Configure FedEx credentials in CloudCart — no Settings page exists.
- Get real-time FedEx quotes at checkout — no rate calculator.
- Generate FedEx waybills/labels from CloudCart — no waybill flow.
- See FedEx as a shipping option at checkout — `active = 0` and there's no shipping provider record to expose.

## Settings & fields

None — the merchant has no FedEx-specific UI in CloudCart.

## Business rules

### `active: 0`, `integrity: false`
The config record is deactivated and marked low-integrity — meaning this is a legacy / placeholder stub. The platform does NOT auto-enable FedEx anywhere.

### Tracking-link template only
The only reason FedEx exists in the codebase is to format `{$tracking_number}` into FedEx's public tracking URL — so that if a tracking number gets assigned (e.g., from a custom workflow or an admin-entered manual entry), the customer sees a clickable FedEx tracking link.

### No backend module
There is no the theme templates PHP module. There is no `vuejs-sitecp/src/CcModules/Shipping/Providers/fedex/` Vue directory. There is no FedEx omniship vendor package. CloudCart does NOT have a contractual / API relationship with FedEx for merchants.

## What the merchant should use instead

For real international parcel shipping with CloudCart:
- [[apps-dhlexpress]] — DHL Express (time-definite, worldwide).
- [[apps-dhl]] — DHL Parcel / eCommerce (standard worldwide).
- [[apps-sendcloud]] — Sendcloud aggregator (multi-carrier including DPD/UPS/PostNL).
- [[apps-eushipment]] — EuShipment aggregator (B2B / pallet focus).

For per-region domestic + cross-border, install the relevant courier app from the [[apps]] catalogue.

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store catalogue.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow (does NOT apply to FedEx).
- [[apps-dhl]], [[apps-dhlexpress]], [[apps-sendcloud]] — actual international integrations.

## Open questions

_None — the entry is a tracking-link stub by design; no integration is planned._
