---
type: feature
nav_path: "Apps → ELS Logistic"
route_name: apps.elslogistic.overview
route_path: /admin/shipping/elslogistic
aliases: ["ELS Logistic", "ELS courier"]
tags: [apps, shipping, courier, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 4
---
# ELS Logistic

## Purpose

**ELS Logistic** courier integration (North Macedonia). Standard OmniShip courier with address + office delivery channels.

## Where to find it

Sidebar → Apps → install → **ELS Logistic** OR direct routes. Standard OmniShip sub-pages.

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
| **Username** (`username`) | API username — required. |
| **Password** (`password`) | API password — required. |

These are the ONLY merchant-facing credentials. The Manager honours an optional `base_url` override behind the scenes (defaults to `https://api.els.mk`), but it is NOT exposed in the merchant UI — only staff / seed data can set it.

## Business rules

Standard OmniShip pattern — quote → waybill → tracking.

## How it works (verified against backend)

### North Macedonia courier (default endpoint api.els.mk)

ELS Logistic is a **North Macedonia** courier — the fallback allowed-countries list covers MK only, and the default API endpoint is `https://api.els.mk`. Cross-border shipments are not supported via this integration.

### Address + office delivery channels

Supported delivery channels: **Address** + **Office** — the customer can choose door delivery OR pickup from an ELS office. No locker channel.

## Settings page — full layout (shared OmniShip form + custom sender)

ELS Logistic uses `SettingsFormShippings` with a custom **Sender Data slot**:

### Credentials card (shared `UsernamePasswordCredentials`)
- **Username** (text, required).
- **Password** (text, required).
- `Connect` button — validates against ELS's API.

### Sender Data card (custom `#senderData` slot)

| Field | Input | Required |
|-------|-------|----------|
| Sender name (`sender_name`) | Text | Yes |
| Sender's phone number (`sender_phone`) | Text | No (error if missing on save) |
| Pickup method (`send_type`) | Radio: **Client's address** (`address`) OR **Office** (`office`) | Yes |
| Choose office (`office_id`) | Searchable ajax select against `/admin/api/elslogistic/autocomplete/offices` | Yes — only when `send_type === 'office'` |
| Choose a location (`sender_city`) | Searchable ajax select against `/admin/api/elslogistic/autocomplete/cities` | Yes — only when `send_type === 'address'` |
| Enter an address (`sender_address`) | Text | Yes — only when `send_type === 'address'` |

The radio toggle (`address` vs `office`) controls which of the bottom three fields are visible:
- `address` → city autocomplete + street address text input.
- `office` → office autocomplete (only).

Sender Data is exposed via the standard `SettingRow` pattern (preview + slide-open edit) so the merchant clicks the pencil to expand.

### Remaining shared cards
- **Visualization** — courier display name + logo upload.
- **Service-types cards** — per delivery channel (`address`, `office`), pencil opens the **Service-type calculator modal** with the 6 pricing modes + rate rows + categories.
- **Ships to (Geo Zones)** — geo-zone allow-list.
- **Payment providers** — payment method multi-select.
- **Additional Settings box** (`general_settings`) — actual fields:
  - **Who pay the shipping cost** (`side`) — radio (Sender / Receiver options).
  - **Consignment type** (`type_product`) — select: Package / Envelope.
  - **Default weight for one item** (`default_weight`) — required, unit kg.
  - **Enable cash on delivery** (`cd`) — switch.
  - **Insurance** (`insurance`) — switch.
  - **Back documents** (`return_documents`) — switch.

  There is NO Base URL field, NO default-dimensions fields in this box.

## Related

- [[shipping-calc-rate-models]] — rate-table semantics: when a method uses a from/to rate table (по тегло / по цена), an **empty upper bound (`до` / `to`) means no upper limit — the bracket runs to infinity** (both bounds inclusive). A blank top row is intended, not invalid, and never hides the method at checkout.
- [[apps]] — App Store.
- [[shipping]] — shipping landing.
- [[orders-shipping-waybill]] — waybill flow.

## Open questions
