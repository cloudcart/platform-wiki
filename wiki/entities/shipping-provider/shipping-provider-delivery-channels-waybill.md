---
type: entity
nav_path: "Entity → Shipping Provider → Delivery channels & waybill"
aliases: ["Shipping provider delivery channels", "To address", "To office", "To locker", "Pickup point selection", "Office locker picker", "Waybill generation", "Bill of Lading", "AWB", "Shipping label", "Multi-package shipment", "Split shipment", "Shipping status tracking", "Webhook vs poll tracking"]
tags: [entity, shipping, couriers, providers, delivery-channels, waybill, awb, tracking, webhooks]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[shipping-provider]]. See the hub for the other aspects (attributes, lifecycle, pricing models, checkout filters, COD).

# Shipping Provider — Delivery channels & waybill

## Identity

A Shipping Provider exposes the customer to one or more **delivery channels** at checkout (to the door, to a carrier office, to a 24/7 locker). Once the order is paid, the merchant generates a **waybill** (carrier tracking document) and the platform then receives status updates back from the carrier as the parcel moves. This page catalogues the channels, the pickup-point picker, the waybill flow, the per-carrier status-tracking modes, and the multi-package edge case.

## Aliases

- **Delivery channels** — the umbrella term for `to_address` / `to_office` / `to_locker`.
- **Pickup point** / **Office / locker picker** — the per-channel sub-selector.
- **Waybill** / **Bill of Lading** / **AWB** / **Shipping label** — the post-payment fulfilment document.
- **Multi-package shipment** / **Split shipment** — when one order needs multiple parcels.
- **Webhook vs poll tracking** — how status updates reach CloudCart.

## Key Attributes

### Three delivery channels (per carrier)

Most Bulgarian / Romanian / Greek carriers expose three delivery channels:

- **To address** (`to_address`) — home delivery; courier brings the parcel to the customer's door.
- **To office / branch** (`to_office`) — customer picks up at a specific carrier office, staffed during business hours.
- **To locker** (`to_locker`) — customer picks up at a 24/7 self-service locker (Econtomat, BoxNow locker, Speedy APT).

Each channel may have a different price. The customer picks one at checkout. **BoxNow is locker-only** — no "to address" option.

**Econt's office delivery has a 1,000 kg weight cap** above which only address delivery is offered.

### Pickup-point selection at checkout

When the customer picks a delivery channel that requires a specific pickup point (to office or to locker), the storefront's office / locker picker calls the carrier's offices API and shows nearby pickup locations with addresses + working hours. The customer picks one; the chosen pickup point is stored on the cart.

Each carrier offers different network coverage:

- **Econt** — thousands of Econt offices + Econtomat lockers across Bulgaria + Romania.
- **Speedy** — thousands of Speedy offices + Speedy APT lockers across Bulgaria + Romania.
- **BoxNow** — locker-only network across Bulgaria, Romania, Greece, Cyprus, Croatia.
- **Cargus** — home delivery + office network across Romania.

The pickup-point list is server-side cached per provider (Econt cache window is 1 day — see [[shipping-provider-attributes]]).

### Waybill generation — per-order action after payment

After the order is paid, the merchant generates a waybill (also called Bill of Lading, AWB, or shipping label) via [[orders-shipping-waybill]]. The platform calls the carrier's waybill-creation API with:

- Sender address book entry (see [[shipping-provider-attributes]]).
- Recipient + delivery channel + pickup point (from the cart).
- Dimensions + weight (from [[settings-boxes]] + line-item weights).
- COD amount + insurance (see [[shipping-provider-cod]]).
- Additional services (signature-required, fragile, etc.).

The carrier returns a tracking number; the platform stores it on the order and surfaces it in [[orders-details]] + the customer's order-confirmation page. The order's [[shipping-status]] flips to `fulfilled` (or the carrier's equivalent). The merchant prints the label (PDF / ZPL) and attaches it to the parcel.

Some carriers offer **"return waybills"** for customer-initiated returns — managed under each carrier's app sub-page.

### Status tracking — carrier webhooks update shipping status

After waybill generation, the carrier's API can push status updates back to CloudCart at key delivery events: picked up, in transit, out for delivery, delivered, failed / returned. Each update flips the order's [[shipping-status]] enum. [[settings-statuses]] Shipping tab lets the merchant rename labels and toggle customer-notification emails per status.

For carriers without webhooks, the platform polls the carrier's tracking API on a periodic schedule.

### Webhook vs poll tracking is mixed across providers

- **Webhook-driven** (carrier pushes status events to CloudCart's callback URL): **Econt, Speedy, DHL, DPD**.
- **Poll-based** (CloudCart queries the carrier's tracking API on a schedule): **BoxNow, Cargus, Sameday, Fan Courier**.

The merchant doesn't see the distinction in the admin panel — tracking events show up the same way regardless. For poll-based carriers there can be a longer delay between the carrier-side event and the CloudCart-side status flip.

### Multi-package / split-shipment is not native

Most carrier integrations treat each waybill as ONE package — the cart's aggregate dimensions feed a single quote, and one waybill is generated per Order. A few carriers (Econt, Speedy) support multi-package waybills via their advanced API, but the **standard CloudCart flow does NOT split a cart into per-package quotes**. Merchants needing true split shipments must place separate orders.

### No consolidated coverage matrix

A single table of "which couriers support which delivery channels in which countries" is **not** built into the wiki. Each carrier's per-app page documents its own coverage. For a quick cross-reference, the merchant should consult the country-default recommendations in the **Browse shipping integrations** modal on [[settings-shipping]] — that modal filters carrier visibility by the store's operation country (see [[shipping-provider-checkout-filters]]).

## Where it appears

- [[orders-shipping-waybill]] — the per-order action that calls the carrier's waybill API.
- [[orders-details]] — shows chosen channel + pickup point + tracking number + current shipping status.
- [[shipping-status]] — canonical enum every carrier's tracking events map into.
- [[checkout-flow]] — where the customer picks a channel + pickup point.
- [[settings-statuses]] — Shipping tab: rename labels + toggle per-status customer-notification emails.
- [[settings-boxes]] — package-dimension defaults feeding waybill calls.
- Per-carrier app pages — Econt's 1,000 kg office cap, BoxNow's locker-only network, Cargus's RO coverage, etc.

## Related

- [[shipping-provider]] — hub.
- [[shipping-provider-attributes]] — sender address book + allowed-channel toggles + pickup-point cache window.
- [[shipping-provider-cod]] — COD amount + insurance flow into the waybill call.
- [[shipping-provider-pricing-models]] — the channel's quoted price comes from the active pricing model.
- [[orders-shipping-waybill]] — the per-order waybill action.
- [[orders-details]] — order-level view of channel + waybill.
- [[shipping-status]] — the canonical status enum.
- [[checkout-flow]] — channel + pickup-point selection.
- [[settings-statuses]] — shipping status labels + notification toggles.
- [[settings-hooks]] — shipping-status changes are part of the `order.updated` webhook payload.
- [[settings-boxes]] — package-dimension defaults.

## Open Questions

- The exact polling frequency for poll-based carriers (BoxNow / Cargus / Sameday / Fan Courier) `(verify)`.
- Whether Econt's 1,000 kg office cap is configurable per-merchant or carrier-side fixed `(verify)`.
