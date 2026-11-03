---
type: feature
nav_path: "Apps → Wolt Drive"
route_name: apps.wolt.settings
route_path: /admin/shipping/wolt/settings
aliases: ["Wolt", "Wolt Drive", "Wolt delivery", "Same-day delivery", "On-demand courier", "Wolt venue ID", "Send to Wolt", "Доставка с Wolt", "Волт", "Изпрати към Wolt", "Доставка в същия ден", "Бърза доставка"]
tags: [apps, shipping, on-demand, last-mile, omniship]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 2
---

# Wolt Drive (on-demand delivery)

## Purpose

**Wolt Drive**: *"Same-day courier delivery by Wolt — from your venue to the customer, usually within an hour."* A Wolt courier picks the parcel up at the merchant's Wolt venue and brings it to the customer's door. Checkout shows Wolt's live price and estimated delivery time, the courier is ordered automatically or by hand, and the order follows Wolt's delivery status.

## Where to find it

Sidebar → **Settings → Shipping** (`/admin/shipping`) → **+ View more Shipping methods** → install **Wolt Drive** → open its settings. Permission `settings` or `store.shipping`.

| Tab | Path | Route name |
|---|---|---|
| Overview | `/admin/shipping/wolt/` | `apps.wolt.overview` |
| Settings | `/admin/shipping/wolt/settings` | `apps.wolt.settings` |
| Payments | `/admin/shipping/wolt/payments` | `apps.wolt.payments` |
| Shipments | `/admin/shipping/wolt/shipments` | `apps.wolt.shipments` |

## What the merchant can do here

- Connect the store's Wolt venue, for test and for live.
- Choose how the courier is ordered, and how the delivery is priced for the customer.
- Send an order to Wolt by hand from the order page, seeing Wolt's price first.
- See the shipments on the Shipments tab.

## Settings & fields

### Credentials

Field **Mode**: Live or Test (`test_mode`). Each store holds two sets of **API key**, **Merchant ID** and **venue ID**: `live_api_key`, `live_merchant_id`, `live_venue_id`, and the same with `test_`. The form shows only the set of the selected mode, and only that set is required.

- *"Enter the:mode API key, merchant ID and venue ID."*
- *"The:mode credentials are incomplete — fill in the API key, merchant ID and venue ID, or leave all three empty."*

**Summary under the Credentials title**, visible when the box is collapsed:

- The venue name and pickup address returned by Wolt, stored per mode on Connect, Save and settings load.
- *Test environment* or *Live environment*.
- **Delivery status updates**: Enabled or Not set up. When not set up: *"Orders will not follow the Wolt delivery status. Save the settings to try again."*

### General settings

| Label | Key | Rule |
|---|---|---|
| **Order the courier** | `dispatch_mode` | **Automatically, when the order is paid** (default) or **Manually, from the order**. |
| **Enable cash on delivery** | `cd` | Wolt enables this per merchant: *"Cash on delivery is not enabled for this Wolt merchant. Ask Wolt to enable it, or turn cash on delivery off in the Wolt settings."* |
| **Preparation time before pickup** | `min_preparation_time` | 0 to 60 minutes. |
| **Default weight for one item** | `default_weight` | Required, above 0. |
| **Contactless delivery (leave at the door)** | `is_no_contact` | Switch. |
| **Send the customer an SMS with the Wolt tracking link** | `sms_notifications` | Switch. |
| **Mark the order as completed when Wolt delivers it** | `complete_on_delivery` | Switch. |
| **Note for the courier at pickup** | `pickup_comment` | Up to 500 characters. |

### Channel and pricing

Address delivery only. **Pricing** (`pricing_address`):

| Option | Bulgarian |
|---|---|
| Wolt Drive price | Цена на Wolt Drive |
| Wolt Drive price + handling fee | Цена на Wolt Drive + такса обработка |
| Wolt Drive price + free shipping | Цена на Wolt Drive + безплатна доставка |
| Own price list by distance | Собствена ценова таблица по разстояние |

The price list uses kilometre bands from the venue, with at least one row and no overlap: *"Add at least one distance range with a price."*

## Business rules

### Checkout

The method shows Wolt's live price and *"Estimated delivery ~ :time"* / *"Очаквана доставка ~ :time"*. It is shown when:

- the address is inside Wolt's delivery area;
- the venue and the area are open, within delivery hours;
- the address has a house number or an exact map location.

An address Wolt refused is remembered for 10 minutes.

### Ordering the courier

- **Automatically:** when the order becomes paid. A cash-on-delivery order is sent when it is placed.
- **By hand:** **Send to Wolt** / **Изпрати към Wolt** on the order shows *Wolt price now*, *Paid by the customer*, *Cash to collect at the door*, *Estimated delivery* and *Distance*.
- The price is quoted fresh at this moment, so it can differ from checkout. Wolt's price against the customer's goes to the order history.
- A failed automatic send does not refund. The order stays unshipped, with an alert: *"Order #:order could not be sent to Wolt automatically: :reason. Send it from the order page when possible."*
- The store works from one venue, and a delivery leaves as soon as it is ready after the preparation time.

### Delivery status

Status arrives by webhook from Wolt, set up on Save. The order history records the courier receiving, picking up and delivering the order.

- **Wolt cancels:** the order returns to not shipped: *"Wolt cancelled the delivery of order #:order (:reason). You can send the order again from the order page."*
- **Customer not there:** an alert: *"The Wolt courier could not hand over order #:order — the customer did not show up."*
- **Taking back a fulfilment** cancels at Wolt, unless the courier is already on the way: *"The courier is already on the way — the delivery can no longer be cancelled here. Please contact Wolt support."*

### Billing

Paid yearly with a 15-day trial. The price is on the app's page.

## Related

- [[shipping]] — shipping landing.
- [[apps-glovo]] — the other on-demand courier.
- [[shipping-provider-mechanism]] — the common courier pattern.
- [[orders-shipping-waybill]] — the waybill flow.
- [[shipping-calc-rate-models]] — rate-table semantics.
- [[apps]] — App Store.

## Open questions

- The app's current price (verify).
