---
type: feature
nav_path: "Apps → Sameday"
route_name: apps.sameday.overview
route_path: /admin/shipping/sameday, /admin/shipping/sameday/settings, /admin/shipping/sameday/shipments, /admin/shipping/sameday/shipments-return
aliases: ["Sameday", "Sameday Courier", "Sameday Romania", "Sameday EasyBox", "Sameday First Mile", "Ще оставя пратката в автомат", "Sameday price sync"]
tags: [apps, shipping, courier, romania, bulgaria, locker, omniship]
plan_gates: []
created: 2026-05-22
updated: 2026-11-09
source_count: 5
---
# Sameday (Romanian / Bulgarian courier)

## Purpose

**Sameday** integration — Romania's dominant courier service, also serving Bulgaria. Sameday offers three delivery channels: **traditional courier delivery** (to home / office), **office pickup**, AND **EasyBox lockers** (self-service pickup network). The app provides real-time quotes, waybill generation, sender configuration, and EasyBox locker selection at checkout.

## Where to find it

Sidebar → Apps → install → **Sameday** OR direct routes. Sameday exposes FOUR sub-pages — note there is **no Payments tab** (different from Econt / DPD); pair-with-payment-provider configuration lives only inside Settings.

| Sub-page | Route name | Path |
|----------|------------|------|
| Overview | `apps.sameday.overview` | `/admin/shipping/sameday/` |
| Settings | `apps.sameday.settings` | `/admin/shipping/sameday/settings` |
| Shipments | `apps.sameday.shipments` | `/admin/shipping/sameday/shipments` |
| Shipments return | `apps.sameday.shipments-return` | `/admin/shipping/sameday/shipments-return` |

Shipments and Shipments-return share one screen; bulk-print offers A4/A6 format select.

## What the merchant can do here

- Enter Sameday API credentials and pick the country instance (Settings).
- Enable one or more delivery channels: **To address**, **To EasyBox locker**, **To office**.
- Configure package defaults, COD, insurance, and return-waybill behaviour.
- Generate outbound and return waybills; bulk-print labels.

**What the merchant CANNOT do here:**
- Use a single Sameday account across multiple countries simultaneously — each country (RO, BG) needs its own credentials/contract; configure one country per install.
- Select a country other than Bulgaria or Romania — Hungary and other Sameday markets are not exposed.
- Generate waybills outside Sameday's served countries.

## Settings & fields

### Credentials box (`CourierCredentialsSection.vue`)
- **Username** (`username`) — Sameday API username; required.
- **Password** (`password`) — masked; required.
- **Country** (`country`) — select with TWO options: `Bulgaria (bg)` | `Romania (ro)`.

The sign-in token is obtained, cached and refreshed automatically. A "Connect" button shows until validated; invalid credentials show "Invalid credentials" on all three fields. The country picker drives the API endpoint, the service list, the locker network and the account's currency (see Business rules).

### Services / rate cards
The standard Services tags box is conditionally HIDDEN for Sameday — service tiers are managed per-channel inside the calculator instead. Each channel (address / office / locker) has its own rate card opened via the pencil. A Sameday-specific extra, **Type of services** (`allowed_methods_{channel}`), is a multi-tag select against `/admin/api/sameday/services?type={channel}` that picks which service tiers (e.g., NextDay / SameDay / 2H Express) offer that channel. Free-shipping service follow-ups (city / intercity) are available.

Geo zones and Payment providers boxes are standard. Name & logo (Visualization) is standard. Sameday's Vue defines no custom sender editor — the sender is chosen via `default_address` below.

### Additional settings — Box 1 (`general_settings`)
- **Default weight for one item** (`default_weight`) — required (100g default per item when unspecified).
- **Default width / length / height** (mm) — 10cm × 10cm × 10cm default per item.
- **Submit product sizes** (`item_sizes`) — switch. When OFF, all items ship as ONE package with default dimensions; when ON, each cart item ships as a separate package with its own dimensions, so Sameday calculates volumetric weight per package.
- **Choose a sender address** (`default_address`) — select; only populated while a session is active, lists sender addresses returned by Sameday's API.
- **Package Type** (`package_type`) — Package / Small Package / Big Package (numeric IDs 0/1/2).
- **Default number of packages to deliver to an address** (`package_address`) — number; depends on `item_sizes = 0`.
- **Default number of packets to deliver to a locker** (`package_locker`) — number; depends on `item_sizes = 0`.
- **Choose a content description** (`content`) — Product name / SKU / barcode / Order number (Sameday adds "Order number", not present on other couriers).

### Additional settings — Box 2 (`parcel_and_waybill_settings`)
- **Enable cash on delivery** (`cd`) — switch.
- **Insurance** (`insurance`) — switch.
- **Open before payment** (`open_before_test`) — switch; help-text: *"This option can only be used for delivery to an address."*
- **Create return waybill** (`return_waybill`) — switch. The four fields below all depend on `return_waybill = 1`:
  - **Add cash on delivery to return waybill** (`return_waybill_cod`) — switch.
  - **Add insurance to return waybill** (`return_waybill_insurance`) — switch.
  - **Select return service** (`return_waybill_service`) — select against `/admin/api/sameday/services`.
  - **How many days return waybill is valid** (`return_waybill_days`) — number, 1–365.

Defaults out of the box: sender pays; address channel on; Sameday-calculator (real-time API quote) pricing.

## Business rules

- **EasyBox is Sameday's locker network.** When enabled, customers pick a specific locker at checkout, as ONE of multiple Sameday options. A locker takes up to 20 kg in compartments of 10 / 20 / 39 × 44.5 × 47 cm and is offered only when the cart fits: [[shipping-provider-mech-locker-fit]].
- **PUDO points use the "to office" channel.** A location id under 500000 is an easybox locker, 500000 and above a PUDO point. Services at checkout and in the waybill: address uses `allowed_methods_address`, easybox `allowed_methods_locker`, PUDO the PUDO services in `allowed_methods_office`, falling back to the locker list until one is configured. The "to office" **Type of services** picker lists PUDO delivery services only.
- **Ship from a locker (First Mile).** The waybill modal offers *"I'll leave the parcel in a locker"* / *"Ще оставя пратката в автомат"* for every delivery type. Switching it on shows **Select locker** / **Изберете автомат**, a search of Sameday's points, and a point is then required (*"When First Mile is enabled, please choose a pickup point."*). The waybill names that point as the drop-off and adds Sameday's PDO service option (its commercial terms: verify with Sameday). It is chosen per waybill; the settings have no such switch.
- **"Open before paying" requires sender-pays.** Per the help text: *"The option Open before paying can only be used if the payer of the shipment is the SENDER."* On receiver-pays COD it is silently disabled regardless of the toggle.
- **COD supported per country**, synced via [[orders-sync-cod]]. The platform caps COD at 10000 BGN per order **only when the store currency is `BGN`** (or at the merchant's lower COD maximum). With EUR or RON there is no platform-side cap; Sameday's own limits apply.
- **Currency.** For a recipient in Romania, the cash-on-delivery and insured amounts are converted to RON; otherwise they go in the order's currency. The waybill's cost comes back without a currency and is read in the Sameday account's currency (RON for Romania, EUR for Bulgaria), then converted to the store's currency. When the customer switches payment method (e.g. COD → online), shipping recalculates and Sameday's COD fee disappears.
- **Waybill price sync.** On an order that is not paid or completed, generating the waybill asks *"Do you want to sync the prices?"* / *"Искаш ли да синхронизираш цените?"* (in the Admin API the field is **Обнови сумата на поръчката според товарителницата**). Yes makes the waybill's cost, after the method's own pricing rules, the order's shipping price and recomputes the totals; No changes nothing. A paid order changes only when its recalculation lock (**Забрани преизчисляване на цената за доставка**, the lock in the order totals, not a waybill control) is off ([[order-pipeline-recalculation]]). No order-history entry is written for it. **Уведоми клиента** is in the order's customer card, not the waybill form.
- **Services and cross-border.** The service list is what Sameday's API returns for the account; names like *"Crossborder HD 24H"* are Sameday's, and cross-border use depends on the merchant's Sameday contract (no quote when not covered).
- **Live service.** Quotes and waybills go to Sameday's production service for the country chosen (Bulgaria, Romania or Hungary).

## Per-channel delivery pricing

Each of the **3** channels (address, office, locker) is a separate rate card with its own toggle (`to_address` / `to_office` / `to_locker`) and a **Delivery price calculation** type:

- `calculator` — the real-time Sameday quote.
- `calculator_fixed` — the quote **plus** the **Parcel processing Fee**.
- `free` — the quote, but **free at or above** the **Minimum Order Value for Free Delivery**; adds **Free Delivery Service within the City** and **Intercity** selects.
- `fixed_price` / `fixed_weight` / `price_and_weight` — **Fixed value** tables by cart subtotal, total weight, or both; the quote is ignored.

Calculator types also have an optional **Fallback price** table; every type adds a **per-category** sub-table. Full mechanics: [[shipping-calc-rate-card-fields]] and [[shipping-calc-rate-models]].

## Related

- [[shipping-calc-rate-models]] — rate-table semantics (an empty upper bound means no upper limit).
- [[apps]] — App Store.
- [[apps-cargus]] — sister Romanian courier (often installed alongside; address-only).
- [[apps-boxnow]] — sister locker provider (locker-only; Sameday EasyBox is one option among many).
- [[shipping]] — shipping providers landing.
- [[orders-shipping-waybill]] — waybill generation flow.
- [[orders-sync-cod]] — COD payment sync.
- [[settings-payment-providers]] — COD configuration.
- [[shipping-provider-mechanism]] — common shipping (OmniShip) pattern.

## Open questions

None.
