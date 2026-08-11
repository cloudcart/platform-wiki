---
type: feature
nav_path: "Apps → D-Express"
route_name: apps.dexpress.overview
route_path: /admin/shipping/dexpress
aliases: ["D-Express", "D Express", "DExpress courier"]
tags: [apps, shipping, courier, balkans, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 5
---
# D-Express

## Purpose

**D-Express** integration — Serbian / Balkan courier service operating in Serbia and adjacent markets.

## Where to find it

Sidebar → Apps → install → **D-Express** OR direct routes. Standard OmniShip sub-pages.

## What the merchant can do here

- Install / activate / deactivate the integration.
- Configure credentials in the Settings sub-page.
- View generated waybills / shipments in the Shipments sub-page.
- Manage returns in the Shipments return sub-page.
- See real-time quotes at checkout once credentials are validated.

### What the merchant CANNOT do here
- Use the integration without an active courier contract + valid API credentials.
- Generate waybills for destinations the courier does not serve.

## Settings & fields

| Field | Notes |
|-------|-------|
| **Client ID** | D-Express customer identifier. |
| **Username** | API username. |
| **Password** | API password. |

### Pricing models

Three pricing models — the merchant picks ONE:

- **Fixed price** — flat fee per shipment.
- **Fixed weight** — weight-based pricing.
- **Price and weight** — combination model.

No live-rate calculator option — D-Express's API doesn't provide real-time quotes, so the merchant builds their own rate table.

### Additional services (per-waybill)

When generating a waybill the merchant can request these add-ons (each is a contract-dependent add-on charged by D-Express):

| Service | Meaning |
|---------|---------|
| **24h** | Delivery within 24 hours. |
| **Declared value** | Declared-value declaration (declared amount required). |
| **Saturday delivery** | Delivery on Saturday. |
| **AOS** | Shipment delivery after recipient verification. |
| **CS1** | Recipient phone notification. |
| **FDS** | Recipient notification and delivery choice. |
| **FSS** | Recipient SMS notification and delivery choice. |
| **PSS** | Pickup from sender's address. |
| **TGS** | Compensation for CO₂ emissions caused by the shipment delivery. |
| **POD** | Proof of delivery. |
| **Return documents** | Return documents to sender. |
| **Additional return shipment** | Add a return shipment. |

### Type of delivery

| Value | Meaning |
|-------|---------|
| **Regular delivery** | Standard. |
| **Urgent delivery** | Delivered today. |

## Business rules

Standard OmniShip pattern (quotes → waybill → tracking). See [[orders-shipping-waybill]] and [[shipping-provider-mechanism]] for the general flow.

## Per-channel delivery pricing

D Express delivers to **address** and to **locker** — each of its **2** delivery channels (to **address** and to **locker**) is a separate rate card with its own enable toggle (`to_address` / `to_locker`) and a **Delivery price calculation** type. When the merchant picks a type, the rate card reveals these fields:

- `fixed_price` — a **Fixed value by price** rate table: rows keyed by **cart subtotal** (`from` / `to` / `amount`); the courier quote is ignored.
- `fixed_weight` — a **Fixed value by weight** rate table: rows keyed by **total weight**.
- `price_and_weight` — a combined table keyed by **both cart subtotal and weight**.

Each `fixed_*` type's table **is** the price (there is no live calculator on D Express, so no fallback). **Every** type also adds a **per-category** sub-table ("Set different pricing conditions for products in category/ies") for charging chosen categories differently. Full field mechanics + rate-row semantics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.
- (Sister Balkan couriers: Sameday, Cargus, FanCourier.)

## How it works (verified against backend)

### Serbia-only

Fallback allowed country is Serbia — strictly Serbian-domestic. Cross-border shipments via this integration are NOT supported.

### Address + locker

Supported delivery channels are address (door delivery) and locker. No office channel.

### PDF waybill via D-Express API

D-Express returns waybill PDFs directly. The merchant clicks Print waybill on an order; the platform fetches the PDF from D-Express.

### Default: receiver pays

The default payer is the receiver — by default the customer pays the courier (typical for COD-heavy markets like Serbia).

### Simpler 3 pricing models

Three pricing models only — Fixed price, Fixed weight, and Price+weight — no calculator-based pricing. The merchant configures their own rate table.

### No real-time calculator pricing — merchant builds the rate table

D-Express's three pricing models are Fixed price, Fixed weight, and Price+weight. There's no live-rate calculator from D-Express's API, so the merchant configures their own price-per-weight or per-shipment table in CloudCart, matching whatever rates their D-Express contract specifies.

### Max package size enforced

A maximum package envelope is enforced when generating the waybill — 20 kg, 47 cm long, 44 cm wide, 44 cm tall. Above any dimension the waybill is rejected.

### Sender drop-off-point option

When the sender drop-off-point setting is on, the merchant leaves the package at a D-Express drop-off location (instead of arranging a courier pickup at the merchant's address).

## Settings page — full layout (shared OmniShip form + custom credentials + custom sender)

D-Express uses `SettingsFormShippings` with TWO custom slots:

### Credentials card (custom `#credentials`)
| Field | Input | Required | Notes |
|-------|-------|----------|-------|
| Client ID (`client_id`) | Text | Yes | Error: "Invalid credentials" / "Client ID required" |
| Username (`username`) | Text | Yes | "Username required" |
| Password (`password`) | Text (`type="password"`) | Yes | "Password required" |

`Connect` button → validates against D-Express's API.

### Sender data card (custom `#senderData`)
| Field | Input | Required |
|-------|-------|----------|
| Contact name (`sender_name`) | Text | Yes |
| Contact phone number (`sender_phone`) | Phone input | No (error if missing) |
| City (`sender_city_id`) | Ajax-search select against `/admin/api/dexpress/cities` | Yes |
| Street (`sender_street`) | Text | Yes |
| Street number (`sender_street_number`) | Text | Yes |
| "I will leave the package at the Drop off point." (`sender_drop_off_point`) | Switch toggle | — |

Drop-off point toggle controls whether the merchant brings packages to a D-Express drop-off location vs. having D-Express collect from the merchant's address.

### Remaining shared sections
- **Visualization** — courier display name + logo upload.
- **Service-type cards** — `address` + `locker` channels exposed. Pencil opens the **Service-type calculator modal** with the 3 D-Express pricing modes (Fixed price, Fixed weight, Price+weight — no calculator mode) + rate rows + categories.
- **Ships to (Geo Zones)** — geo-zone allow-list (Serbia-only in practice).
- **Payment providers** — payment method multi-select.
- **Additional Settings** (two boxes):
  - `general_settings`: **Default weight for one item** (`default_weight`), **Default width** (`default_width`, mm), **Default depth** (`default_depth`, mm), **Default height** (`default_height`, mm), **Choose a content description** (`order_content`: Product name / SKU / Barcode).
  - `parcel_and_waybill_settings`: **Who pay the shipping cost** (`side`, radio), **How the parcel transport service will be paid** (`payment_type`: Cash / Invoice), **Enable cash on delivery** (`cd`), **Bank account number where COD will be paid** (`bank_account`, visible when `cd` is ON), **Declared value** (`declared_value`).

  The per-waybill `Type of delivery` (Regular / Urgent) and the additional-service flags (24h, Saturday delivery, AOS, CS1, FDS, FSS, PSS, TGS, POD, Return documents, Additional return shipment) are surfaced at WAYBILL creation time — not on the Settings page.

## Open questions
