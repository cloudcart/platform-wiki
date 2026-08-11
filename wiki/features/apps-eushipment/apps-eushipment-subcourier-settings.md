---
type: feature
nav_path: "Apps → EuShipment → (sub-courier) Settings"
route_name: apps.eushipment.external
route_path: /admin/shipping/eushipment/external/:id
aliases: ["EuShipment sub-courier settings", "EuShipment courier settings", "EuShipment Additional Settings", "EuShipment per-courier settings", "EuShipment настройки на куриер"]
tags: [apps, shipping, b2b, europe, omniship, aggregator, eushipment, settings]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-eushipment]]. See the hub for the other aspects (credentials & sub-courier framework, pricing modes).

# EuShipment — sub-courier settings page

## Purpose

Once a courier is installed from the EuShipment Settings picker (see [[apps-eushipment-credentials-couriers]]), it becomes its OWN shipping method with its own `external_id`, and gets a dedicated settings page. This page is where the merchant configures everything about that one courier — enabling delivery channels, restricting geo zones and payment methods, and setting the per-courier operational options (who pays the shipping, default weight, return documents, fragile, fulfillment, COD, insurance, Saturday delivery, etc.).

The page exposes the standard shipping provider settings — the same UI shape as Econt / Speedy / Cargus when installed independently (see [[shipping-provider-mechanism]]). The capability-gated parts of the page appear only when the underlying courier's contract permits them.

## Where to find it

Sidebar → Apps → EuShipment → **Settings** → click an installed courier's **Settings** link (or its name) → the sub-courier page at `apps.eushipment.external/:id` (`/admin/shipping/eushipment/external/:id`).

## What the merchant can do here

- Enable / disable this individual sub-courier.
- Rename it and override its synced logo; toggle "Show in store".
- Activate / deactivate each delivery channel (Address / Office / Locker) and open the rate calculator per channel — see [[apps-eushipment-pricing-modes]].
- Restrict this courier to specific Geo Zones (independent of the parent app and other sub-couriers).
- Restrict which payment methods are allowed with this courier.
- Configure the per-courier operational options in the Additional Settings box.

## Settings & fields

**Top status section** — Enable / Disable button for the sub-courier (toggles `provider.active`). The badge in the right-hand toolbar reflects current status.

**Visualization card** — Name (text), Logo upload (override the synced EuShipment logo), "Show in store" toggle.

**Service-types section** — for each enabled delivery channel (`address`, `office`, `locker`), a card with an Active/Inactive status badge (toggles `to_<type>`) and a pencil that opens the rate calculator modal. The six pricing modes, rate rows, allowed services, available countries, and category restrictions all live in that modal — documented in [[apps-eushipment-pricing-modes]].

**Geo Zones card** — geo-zone allow-list for THIS sub-courier (independent of parent app + other sub-couriers).

**Payment providers card** — payment-method allow-list. Toggle: "All payment's" vs "Selected providers".

**Additional Settings box** (`general_settings`) — the field list is built dynamically against the sub-courier's `options`.

Always-visible fields:

| Field | Notes |
|---|---|
| **Who pays the shipping cost** (`side`) | Radio (Sender / Receiver / etc.). |
| **Operation country for provider** (`operation_country`) | Required, only shown when target is `restofworld`. |
| **Default weight for one item** (`default_weight`) | Required, unit `kg`. |
| **Primary Account** (`default_company`) | Select populated from the merchant's EuShipment company list. |
| **Return documents** (`return_documents`) | None / Waybill / Document. |
| **Choose a content description** (`order_content`) | Product name / SKU / Barcode. |
| **Fragile shipment** (`fragile`) | Switch. |
| **Enable Fulfillment** (`fullfilment`) | Switch; plus `fullfilment_compare` (SKU / Barcode) and `fullfilment_documents` (No documents / Goods receipt / Invoice — last two depend on store settings). |
| **Price Adjustment** (`price_adjustment`) | Percentage applied on top of the API price. |

Capability-gated switches (rendered only when the sub-courier's `options` flag is set — see the contract-controlled capability rule on [[apps-eushipment-credentials-couriers]]):

| Field | Visible when |
|---|---|
| **Cash on Delivery** (`cod`) | `options.cod` is set. |
| **Insurance** (`insurance`) + **Declared value** (`declared_value`) | `options.insurance` is set. |
| **View package** (`open_package`) | `options.open` is set. |
| **Delivery on saturday** (`saturday_delivery`) | `options.saturday` is set. |

**Submit changes bar** — sticky bottom bar; posts to `/admin/api/eushipment/settings/:id` with the full per-sub-courier state.

## Business rules

### Each sub-courier is fully independent

Geo zones, payment-method allow-list, delivery channels, and Additional Settings are configured per sub-courier. Two installed couriers from the same EuShipment contract can have completely different geo coverage, payment restrictions, and pricing.

### "Open before pay" requires the SENDER to pay the shipment

There is NO standalone "Open before pay" switch — the toggle is labelled **View package** (`open_package`) in the UI. Per the in-app help: *"The Open before you pay option can only be used if the payer of the shipment is the SENDER"* — meaning the merchant must be paying the shipment (not the customer at delivery). If the merchant configured COD where the customer pays the shipment, open-before-pay is silently disabled regardless of the sub-courier's capability flag.

### Pallet vs parcel comes from the underlying courier

Each EuShipment-aggregated courier exposes its own `to_office` / `to_address` flags and its own service tiers. Whether a shipment moves as a parcel or a pallet depends on the chosen sub-courier's contract — the EuShipment integration itself has no pallet/parcel switch.

### COD has a cap

When COD is enabled on the sub-courier, COD applies only when the merchant's COD setting is on AND the order is within the COD cap. For BGN stores the cap is 10000 BGN.

### Background fulfillment + return documents

Enabling Fulfillment changes what documents the courier produces and how line items are matched (by SKU or Barcode). Return-document selection (`return_documents`) decides whether a waybill or document accompanies returns.

## Related

- [[apps-eushipment]] — hub.
- [[shipping-provider-mechanism]] — the common shipping provider settings pattern this page follows.
- [[settings-shipping]] — Suppliers list where this sub-courier appears as its own method.
- [[orders-shipping-waybill]] — waybill generation that consumes these settings.

## Open questions

None.
